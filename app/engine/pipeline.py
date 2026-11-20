"""Order-to-Cash pipeline: Cash Application -> Account Context -> Controller -> Collections.

Order matters: cash is applied first so no reminder is ever drafted for money we already have (the Paidly failure).
"""
import re

import pandas as pd

from . import cash_app, collections, context, controller
from .data import AS_OF, load, norm_name
from .rules import load_rules, save_rules  # noqa: F401  (re-exported for the web layer)

COMPLAINT_RX = r"(?:already paid|chas(?:ed|ing) (?:us|me)|reminder email|overdue notice|final notice|threaten)"


def _am_email(name):
    if not isinstance(name, str):
        return None
    return re.sub(r"[^a-z.]", "", name.lower().replace(" ", ".")) + "@ledgerline.com"


IMPL_FEE = {"Growth": 2500.0, "Enterprise": 8000.0}


def contract_check(d, r):
    """Compare an invoice with the contract term covering its issue date. arr = seats x price x 12 + platform fee."""
    inv = d["invoices"].set_index("invoice_id").loc[r["invoice_id"]]
    c = d["contracts"]
    c = c[(c["customer_id"] == r["customer_id"]) & (c["term_start"] <= str(r["issue_date"])) & (c["term_end"] >= str(r["issue_date"]))]
    if not len(c):
        return {"matches": None, "text": "No contract term on file covers the invoice date. AM to check."}
    k = c.iloc[-1]
    if inv["type"] == "implementation":
        exp = IMPL_FEE.get(k["plan"])
        basis = "implementation fee for %s plan" % k["plan"]
    else:
        exp = round(float(k["arr"]) * float(inv["service_period_months"]) / 12.0, 2)
        basis = "%d seats x $%s/seat/month + $%s platform fee (%s plan, term %s to %s), %d-month billing" % (
            k["seats"], format(k["price_per_seat_per_month"], ",.0f"), format(k["platform_fee"], ",.0f"), k["plan"],
            k["term_start"], k["term_end"], inv["service_period_months"])
    ok = exp is not None and abs(exp - float(inv["amount"])) < 0.5
    txt = ("Invoice matches the contract on file: %s = $%s. If the claim rests on something outside the contract (a verbal discount, tax status, a plan change), the AM has to confirm it; otherwise reply with this evidence." % (basis, format(exp, ",.2f"))
           if ok else "Invoice does NOT match the contract (%s = $%s vs invoiced $%s). Likely our error: correct and reissue." % (basis, format(exp or 0, ",.2f"), format(inv["amount"], ",.2f")))
    return {"matches": ok, "expected": exp, "text": txt}


def run_pipeline(rules=None):
    rules = rules or load_rules()
    d = load()
    audit = []

    # 1. Cash Application
    payments, a = cash_app.run(d, rules)
    audit += a
    cash_by_invoice, cash_by_customer = {}, {}
    for p in payments:
        for iid in p["invoice_ids"] + p.get("alternatives", []):
            cash_by_invoice.setdefault(iid, p)
        if not p["invoice_ids"] and p["customer_id"]:
            cash_by_customer.setdefault(p["customer_id"], []).append(p)
    unidentified = [p for p in payments if not p["customer_id"] or (p["decision"] == "EXCEPTION" and not p["invoice_ids"])]

    # 2. Account Context for every customer with unpaid invoices or unapplied cash
    ar = d["ar"].copy()
    cust_ids = set(ar["customer_id"]) | {p["customer_id"] for p in payments if p["customer_id"]}
    ctxs, a = context.build(d, rules, cust_ids, payments)
    audit += a

    # 3 + 4. Controller and Collections per unpaid invoice
    invoices = []
    for _, r in ar.sort_values("amount", ascending=False).iterrows():
        inv = {"invoice_id": r["invoice_id"], "customer_id": r["customer_id"], "customer_name": r["customer_name"],
               "amount": float(r["amount"]), "issue_date": r["issue_date"], "due_date": r["due_date"],
               "days_past_due": int(r["days_past_due"]), "ar_status": r["status"], "bucket": r["bucket"], "plan": r["plan"]}
        ctx = ctxs.get(r["customer_id"])
        stage = collections.stage_for(inv["days_past_due"], inv["ar_status"], rules)
        holds = controller.holds_for(inv, ctx, cash_by_invoice, cash_by_customer, rules, unidentified)
        action = controller.decide(inv, holds, stage)
        drafted = None
        if action in ("DRAFT_REMINDER", "HUMAN_WRITES") and ctx and not any(h["code"] == "LEGAL_RISK" for h in holds):
            drafted = collections.draft(inv, ctx, stage, rules, _am_email(ctx.get("account_manager")))
            problems = controller.check_draft(drafted, rules)
            if problems:
                holds.append({"code": "BANNED_LANGUAGE", "label": "Draft blocked: threatening language",
                              "detail": "Draft contained: %s. Needs VP Finance sign-off." % ", ".join(problems), "agent": "Controller"})
                drafted, action = None, "HOLD"
        # Failed card where the customer's card has since worked: propose a re-run. Priya approves each one (Maya, T+0:17).
        retry = None
        if inv["ar_status"] == "payment_failed":
            later = d["payments"][(d["payments"]["method"] == "card") & (d["payments"]["payer_name"].map(norm_name) == norm_name(r["customer_name"]))
                                  & (d["payments"]["received_date"] > pd.Timestamp(r["issue_date"]))].sort_values("received_date")
            blocked = {h["code"] for h in holds} & (controller.HARD_HOLDS | {"LEGAL_RISK"})
            if len(later) and action != "HOLD" and not blocked:  # never re-charge a customer threatening a chargeback
                lp = later.iloc[-1]
                retry = {"card_works": True, "evidence": "%s: card charge of $%s succeeded on %s" % (lp["payment_id"], format(lp["amount"], ",.2f"), lp["received_date"].strftime("%Y-%m-%d")),
                         "needs": "Priya approves the re-run"}
                action = "RETRY_CARD"
                drafted = None
        if any(h["code"] == "CARD_WRITEOFF_SOON" for h in holds):
            for h in holds:
                if h["code"] == "CARD_WRITEOFF_SOON":
                    h["label"] = "Decision for Dana today: " + h["label"]
                    h["route_to"] = "Dana Ruiz (VP Finance)"
        # Contract check (discrepancy sweep, T+0:35): does the disputed invoice match the contract on file?
        for h in holds:
            if h["code"] == "DISPUTE":
                h["contract_check"] = contract_check(d, r)
        if inv["ar_status"] == "payment_failed" and inv["amount"] > 2000:
            holds.append({"code": "WRITEOFF_OVER_LIMIT", "label": "Auto write-off would exceed Dana's $2,000 limit",
                          "detail": "Card invoices write off automatically at 150 days, but write-offs over $2,000 need the VP Finance. 9 past auto write-offs ($47,251) breached this limit.",
                          "agent": "Controller", "route_to": "Dana Ruiz (VP Finance)"})
        for h in holds:
            if h["code"] in ("DISPUTE", "CANCELLATION"):
                h["route_to"] = (ctx or {}).get("account_manager")
                h["release_requires"] = "Account manager confirms the dispute is settled (Maya, T+0:17)"
        reasons = [h["label"] for h in holds] or (["Stage: %s" % stage] if action != "NO_ACTION" else [])
        if retry:
            reasons = ["Card works again (%s). Re-run the failed charge?" % retry["evidence"]] + reasons
        if action == "NO_ACTION" and stage in ("not_due", "wait") and not holds:
            reasons = ["Not due yet" if stage == "not_due" else "Next reminder at day %d" % rules["reminder_days"]["first"]]
        invoices.append(dict(inv, stage=stage, action=action, holds=holds, draft=drafted, retry=retry,
                             top50=bool(ctx and ctx.get("top50")), account_manager=(ctx or {}).get("account_manager"),
                             reasons=reasons))
        audit.append({"agent": "Controller" if action in ("HOLD", "HUMAN_WRITES") else "Collections", "object_type": "invoice",
                      "object_id": r["invoice_id"], "decision": action, "confidence": 0.9 if holds else 0.8,
                      "reason": "%s $%s, %d days past due: %s" % (r["customer_name"], format(r["amount"], ",.0f"), r["days_past_due"], "; ".join(reasons) or stage)})

    # Metrics (Dana's number first: overdue balance; complaints are the veto)
    overdue = [i for i in invoices if i["days_past_due"] > 0]
    ledger_overdue = sum(i["amount"] for i in overdue)
    # Count each receipt once (Kingsway's one $5,100 payment holds two invoices; QA T+0:30 found it double-counted).
    held_paid = [i for i in overdue if any(h["code"] in ("PAID", "MONEY_RECEIVED") for h in i["holds"])]
    pays_for_overdue = {}
    for i in held_paid:
        p = cash_by_invoice.get(i["invoice_id"])
        key = p["payment_id"] if p else i["invoice_id"]
        pays_for_overdue[key] = min(p["amount"], pays_for_overdue.get(key, 0) + i["amount"]) if p else i["amount"]
    paid_or_received = sum(pays_for_overdue.values())
    disputed = sum(i["amount"] for i in overdue if any(h["code"] in ("DISPUTE", "CANCELLATION", "LEGAL_RISK") for h in i["holds"])
                   and not any(h["code"] in ("PAID", "MONEY_RECEIVED") for h in i["holds"]))
    # Veto metric: complaints about how LEDGERLINE chased the customer, as read by the Account Context agent.
    # (A keyword count finds 14 "reminder" tickets in 120 days, but 13 are customers asking about their OWN reminder
    # emails to their clients -- a product feature. That miscount is in the failure gallery.)
    keyword_hits = int(d["tickets"][d["tickets"]["created_at"] >= AS_OF - pd.Timedelta(days=120)]["body"].fillna("")
                       .str.contains(COMPLAINT_RX, case=False, regex=True).sum())
    complaints = sorted({t["ticket_id"] for c in ctxs.values() for t in c["recent_tickets"]
                         if t["read"].get("kind") == "legal_threat" or t["read"].get("collections_complaint") and t["read"].get("about_ledgerline_invoice")})
    prevented_codes = {"PAID", "MONEY_RECEIVED", "DISPUTE", "CANCELLATION", "LEGAL_RISK", "OPEN_ESCALATION"}
    metrics = {
        "overdue_balance": ledger_overdue,
        "overdue_count": len(overdue),
        "overdue_already_paid": paid_or_received,
        "overdue_disputed": disputed,
        "overdue_collectable": ledger_overdue - paid_or_received - disputed,
        "open_ar": float(ar["amount"].sum()),
        "cash_found": sum(p["matched_amount"] for p in payments if p["invoice_ids"]),
        "unapplied_total": sum(p["amount"] for p in payments),
        "chases_prevented": sum(1 for i in overdue if any(h["code"] in prevented_codes for h in i["holds"])),
        "auto_applied": sum(1 for p in payments if p["decision"] == "AUTO_APPLY"),
        "needs_review": sum(1 for p in payments if p["decision"] != "AUTO_APPLY"),
        "held": sum(1 for i in invoices if i["action"] == "HOLD"),
        "drafts": sum(1 for i in invoices if i["action"] == "DRAFT_REMINDER"),
        "human_writes": sum(1 for i in invoices if i["action"] == "HUMAN_WRITES"),
        "collections_complaints": 0,                       # caused by this tool since go-live (nothing has been sent)
        "collections_complaints_baseline": len(complaints),  # existing, last 120 days, read by the agent
        "collections_complaints_baseline_ids": complaints,
        "complaint_keyword_hits": keyword_hits,
        "card_retries": sum(1 for i in invoices if i["action"] == "RETRY_CARD"),
        "dana_decisions": sum(1 for i in invoices if any(h.get("route_to", "").startswith("Dana") for h in i["holds"])),
    }
    for i, row in enumerate(audit):
        row.setdefault("ts", "2026-10-31T07:%02d:%02d" % (i // 60 % 60, i % 60))
    return {"as_of": AS_OF.strftime("%Y-%m-%d"), "metrics": metrics, "payments": payments, "invoices": invoices,
            "customers": ctxs, "audit": audit, "rules": rules}


if __name__ == "__main__":
    import json
    s = run_pipeline()
    print(json.dumps(s["metrics"], indent=1))
