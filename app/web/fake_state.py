"""Development stand-in for app.engine.pipeline.

Produces a small but realistic state dict with the same shape the real engine returns, so the web layer can be
built and tested before the engine lands. The web layer switches to the real engine automatically when
`app.engine.pipeline` imports. Everything here is labelled FAKE in the UI.
"""
import copy
import json
import os
from datetime import date
from typing import Any, Dict, List, Optional

AS_OF = date(2026, 10, 31)

DEFAULT_RULES: Dict[str, Any] = {
    "auto_apply_exact_ref_match": True,
    "writeoff_threshold": 0.0,
    "amount_tolerance": 0.0,
    "reminder_days": {"courtesy": -5, "first": 7, "second": 21, "final": 45, "escalate": 90},
    "top50_human_only": True,
    "hold_on_open_ticket_days": 30,
    "banned_phrases": ["suspension", "suspend", "legal action", "collections agency", "final notice"],
    "notify_am_before_contact": True,
    "use_claude": False,
}


def _rules_path() -> str:
    return os.environ.get("RULES_PATH", os.path.join(os.getcwd(), "rules.json"))


def load_rules() -> Dict[str, Any]:
    rules = copy.deepcopy(DEFAULT_RULES)
    path = _rules_path()
    if os.path.exists(path):
        try:
            with open(path) as f:
                rules.update(json.load(f))
        except (OSError, ValueError):
            pass
    return rules


def save_rules(rules: Dict[str, Any]) -> None:
    path = _rules_path()
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w") as f:
        json.dump(rules, f, indent=2, sort_keys=True)


# --------------------------------------------------------------------------------------------------------------
# Raw fake records (names and ids taken from the data room so the demo looks familiar)
# --------------------------------------------------------------------------------------------------------------

def _contact(name, email, role, verified=True, issue=None, status="active"):
    return {"name": name, "email": email, "role": role, "status": status, "verified": verified, "issue": issue}


CUSTOMERS = [
    # id, name, plan, arr, top50, rank, am, renewal, method, nps, usage
    ("C1469", "Kingsway Engineering Group", "Growth", 20400, False, 212, "Nadia Sinclair", "2026-12-12", "ach", 8, "flat"),
    ("C1273", "Jessop & Orwell Agency", "Scale", 62688, True, 9, "Nadia Sinclair", "2027-08-26", "ach", 9, "growing"),
    ("C1264", "Westbrook Engineering Group", "Scale", 47904, True, 21, "Nadia Upton", "2027-08-14", "ach", 3, "declining"),
    ("C1361", "Thornfield Consulting Group", "Growth", 39456, False, 61, "Nadia Upton", "2027-09-14", "ach", 7, "flat"),
    ("C1126", "Brandt & Lowell CPAs", "Growth", 6324, False, 301, "Maria Yardley", "2027-10-03", "ach", None, "flat"),
    ("C1188", "Castellano, Crane & Co", "Core", 3672, False, 377, "Hannah Drummond", "2027-10-11", "wire", 8, "growing"),
    ("C1223", "Studio Zeller", "Core", 987, False, 455, "Maria Yardley", "2026-12-02", "ach", None, "flat"),
    ("C1346", "Yardley & Duarte Advisory", "Core", 564, False, 470, "Hannah Drummond", "2026-11-15", "ach", 6, "flat"),
    ("C1505", "Achebe + Pemberton Architects", "Scale", 67968, True, 6, "Nadia Upton", "2027-10-05", "wire", 9, "growing"),
    ("C1154", "Okafor & Nakamura LLP", "Scale", 46848, True, 23, "Nadia Sinclair", "2026-11-22", "wire", 5, "declining"),
    ("C1662", "Pell & Marsh Studio", "Core", 2340, False, 402, "Maria Yardley", "2027-02-01", "card", 7, "flat"),
    ("C1420", "Harrow Analytics", "Growth", 11220, False, 188, "Hannah Drummond", "2027-04-18", "ach", 6, "flat"),
    ("C1301", "Kingsway Consulting Group", "Growth", 10608, False, 196, "Maria Yardley", "2026-11-03", "ach", 7, "flat"),
]

CONTACTS = {
    "C1469": [_contact("Oscar Ambrose", "oscar.ambrose@kingswayengineeringgro.example", "Account admin"),
              _contact("Marcus Tan", "marcus.tan@kingswayengineeringgro.example", "Billing contact")],
    "C1273": [_contact("Noah Castellano", "noah.castellano@jessoporwellagency.example", "Account admin"),
              _contact("Joel Okafor", "joel.okafor@jessoporwellagency.example", "Billing contact"),
              _contact("Leo Finch", "leo.finch@jessoporwellagency.example", "Executive sponsor")],
    "C1264": [_contact("Leo Novak", "leo.novak@westbrookengineeringgr.example", "Account admin"),
              _contact("Chloe Sterling", "chloe.sterling@westbrookengineeringgr.example", "Billing contact"),
              _contact("Sofia Nakamura", "sofia.nakamura@westbrookengineeringgr.example", "Executive sponsor")],
    "C1361": [_contact("Renee Wexler", "renee.wexler@thornfieldconsultinggr.example", "Account admin"),
              _contact("Nadia Vance", "nadia.vance@thornfieldconsultinggr.example", "Billing contact")],
    "C1126": [_contact("Emma Sterling", "emma.sterling@brandtlowellcpas.example", "Account admin"),
              _contact("Aisha Garrick", "aisha.garrick@brandtlowellcpas.example", "Billing contact")],
    "C1188": [_contact("Leo Lowell", "leo.lowell@castellanocraneco.example", "Billing contact")],
    "C1223": [_contact("Ines Zeller", "ines.zeller@studiozeller.example", "Account admin and billing")],
    "C1346": [_contact("Rafael Duarte", "rafael.duarte@yardleyduarte.example", "Billing contact")],
    "C1505": [_contact("Grace Pemberton", "grace.pemberton@achebepemberton.example", "Billing contact")],
    "C1154": [_contact("Kenji Nakamura", "kenji.nakamura@okafornakamura.example", "Billing contact"),
              _contact("Ama Okafor", "ama.okafor@okafornakamura.example", "Executive sponsor")],
    "C1662": [_contact("Dara Pell", "dara.pell@pellmarsh.example", "Billing contact", verified=False,
                       issue="Left the firm; still on invoice emails", status="left the firm; still on invoice emails"),
              _contact("Sam Marsh", "sam.marsh@gmail.example", "Account admin", verified=False,
                       issue="Email domain does not match the customer's domain")],
    "C1420": [_contact("Iris Harrow", "iris.harrow@harrowanalytics.example", "Billing contact")],
    "C1301": [_contact("Petra Lind", "petra.lind@kingswayconsultinggrou.example", "Billing contact")],
}

TICKETS = {
    "C1264": [
        {"ticket_id": "T880739", "created_at": "2026-10-02 14:10", "subject": "Invoice total doesn't match our seat count",
         "category": "Billing", "priority": "high", "status": "open",
         "summary": "Customer says the August invoice bills 30 seats; they have 24. Asked for a corrected invoice before paying."},
        {"ticket_id": "T881011", "created_at": "2026-10-28 09:02", "subject": "Still waiting on corrected invoice",
         "category": "Billing", "priority": "urgent", "status": "open",
         "summary": "Follow-up on T880739. Exec sponsor copied. Frustrated about the delay."},
    ],
    "C1154": [
        {"ticket_id": "T880831", "created_at": "2026-10-12 11:45", "subject": "Charged twice after plan change",
         "category": "Billing", "priority": "high", "status": "pending",
         "summary": "After the March billing-engine rewrite the plan change produced a duplicate pro-rata line. Disputing INV-25765."},
    ],
    "C1469": [
        {"ticket_id": "T880184", "created_at": "2026-07-20 20:13", "subject": "Can you check something for me",
         "category": "Billing", "priority": "normal", "status": "solved",
         "summary": "Portal amount vs PDF amount differ by one cent. Answered."},
    ],
    "C1361": [
        {"ticket_id": "T880857", "created_at": "2026-09-30 10:20", "subject": "How do I export timesheets?",
         "category": "How-to", "priority": "low", "status": "solved", "summary": "Answered with help-centre link."},
    ],
}

INVOICES = [
    # id, cust, amount, issue, due, ar_status
    ("INV-25469", "C1469", 5100.00, "2026-06-12", "2026-07-12", "overdue"),
    ("INV-25852", "C1469", 5100.00, "2026-09-12", "2026-10-12", "overdue"),
    ("INV-25784", "C1273", 62688.00, "2026-08-26", "2026-09-25", "overdue"),
    ("INV-25730", "C1264", 47904.00, "2026-08-14", "2026-09-13", "overdue"),
    ("INV-25765", "C1154", 46848.00, "2026-08-23", "2026-09-22", "overdue"),
    ("INV-25862", "C1361", 39456.00, "2026-09-14", "2026-10-14", "overdue"),
    ("INV-25806", "C1126", 6324.00, "2026-09-03", "2026-10-03", "overdue"),
    ("INV-25845", "C1188", 3672.00, "2026-09-11", "2026-10-11", "overdue"),
    ("INV-25937", "C1223", 987.00, "2026-10-03", "2026-11-02", "open"),
    ("INV-25867", "C1346", 564.00, "2026-09-15", "2026-10-15", "overdue"),
    ("INV-25951", "C1505", 8000.00, "2026-10-05", "2026-11-04", "open"),
    ("INV-25950", "C1505", 67968.00, "2026-10-05", "2026-11-04", "open"),
    ("INV-25990", "C1662", 195.00, "2026-10-01", "2026-10-01", "overdue"),
    ("INV-25601", "C1420", 2805.00, "2026-07-01", "2026-07-31", "overdue"),
    ("INV-25888", "C1301", 10608.00, "2026-09-20", "2026-10-20", "overdue"),
]

PAYMENTS = [
    # id, received, amount, method, payer, memo, cust, decision, invoices, conf, reasons
    ("PAY-65805", "2026-10-29", 5100.00, "ach", "Kingsway Engineering Group", "", "C1469", "PROPOSE", ["INV-25469"], 0.78,
     ["Payer name matches customer Kingsway Engineering Group exactly.",
      "Amount $5,100.00 equals two open invoices (INV-25469 and INV-25852); no invoice reference in the memo.",
      "Oldest-first: proposed INV-25469 (111 days overdue). A person must confirm which invoice it pays."]),
    ("PAY-65750", "2026-10-17", 62688.00, "ach", "Jessop & Orwell Agency", "Jessop payment", "C1273", "PROPOSE", ["INV-25784"], 0.91,
     ["Payer name matches customer; amount equals the only open invoice of $62,688.00.",
      "Memo has no invoice reference, so not eligible for auto-apply.",
      "Top-50 account: Paidly-style wrong chase risk. Invoice held until applied."]),
    ("PAY-65766", "2026-10-19", 6324.00, "ach", "BRANDT & LOWELL CPAS", "Ledgerline subscription", "C1126", "PROPOSE", ["INV-25806"], 0.88,
     ["Payer name matches Brandt & Lowell CPAs after normalising case and '&'.",
      "Amount equals the only open invoice; memo has no invoice reference."]),
    ("PAY-65806", "2026-10-30", 3672.00, "wire", "Castellano, Crane & Co", "INV-25845", "C1188", "AUTO_APPLY", ["INV-25845"], 0.99,
     ["Memo contains invoice reference INV-25845.", "Amount equals the invoice amount exactly ($3,672.00)."]),
    ("PAY-65807", "2026-10-30", 987.00, "ach", "Studio Zeller", "Invoice 25937", "C1223", "AUTO_APPLY", ["INV-25937"], 0.98,
     ["Memo 'Invoice 25937' resolves to INV-25937.", "Amount equals the invoice amount exactly ($987.00)."]),
    ("PAY-65808", "2026-10-31", 564.00, "ach", "YARDLEY & DUARTE ADVISORY", "inv25867 Yardley", "C1346", "AUTO_APPLY", ["INV-25867"], 0.97,
     ["Memo 'inv25867' resolves to INV-25867.", "Amount equals the invoice amount exactly ($564.00)."]),
    ("PAY-65796", "2026-10-27", 7975.00, "wire", "ACHEBE + PEMBERTON ARCHITECTS", "", "C1505", "PROPOSE", ["INV-25951"], 0.74,
     ["Payer name matches Achebe + Pemberton Architects.",
      "Short by $25.00 against INV-25951 ($8,000.00): looks like an incoming wire fee.",
      "Write-off threshold is $0 until Dana sets it, so the $25.00 difference needs a person."]),
    ("PAY-65811", "2026-10-31", 1240.00, "check", "H. MORLEY", "", None, "EXCEPTION", [], 0.20,
     ["No customer or contact matches payer 'H. MORLEY'.",
      "No open invoice for $1,240.00. Needs a person to identify the payer."]),
]


def _days_past_due(due: str) -> int:
    y, m, d = (int(x) for x in due.split("-"))
    return (AS_OF - date(y, m, d)).days


def _stage(dpd: int, method: str, ar_status: str, rd: Dict[str, int]) -> str:
    if method == "card" and dpd >= 0 and ar_status == "overdue":
        return "card_failed"
    if dpd >= rd.get("escalate", 90):
        return "escalate"
    if dpd >= rd.get("final", 45):
        return "final"
    if dpd >= rd.get("second", 21):
        return "second"
    if dpd >= rd.get("first", 7):
        return "first"
    if dpd >= rd.get("courtesy", -5):
        return "courtesy"
    return "not_due"


SUBJECTS = {
    "courtesy": "Upcoming invoice {inv} due {due}",
    "first": "Friendly reminder: invoice {inv}",
    "second": "Invoice {inv} is now {dpd} days past due",
    "final": "Can we help with invoice {inv}?",
    "escalate": "Invoice {inv}: let's find a way forward",
    "card_failed": "Your card payment for {inv} didn't go through",
}


def _draft(inv: Dict[str, Any], cust: Dict[str, Any]) -> Dict[str, Any]:
    billing = [c for c in cust["contacts"] if c["verified"] and "billing" in c["role"].lower()]
    to = [c["email"] for c in (billing or [c for c in cust["contacts"] if c["verified"]])][:1]
    first = (billing[0]["name"].split()[0] if billing else "there")
    stage = inv["stage"]
    subject = SUBJECTS.get(stage, "Invoice {inv}").format(inv=inv["invoice_id"], due=inv["due_date"],
                                                          dpd=inv["days_past_due"])
    amount = "${:,.2f}".format(inv["amount"])
    if stage == "card_failed":
        body = ("Hi {f},\n\nWe tried to charge the card on file for invoice {inv} ({amt}) and the payment didn't go "
                "through. This usually means the card expired or was replaced. You can update it in Settings > "
                "Billing, or reply and we'll send a secure payment link.\n\nThanks,\nPriya\nLedgerline Accounts")
    elif stage == "courtesy":
        body = ("Hi {f},\n\nA quick heads-up that invoice {inv} for {amt} is due on {due}. No action is needed if "
                "it's already scheduled.\n\nThanks,\nPriya\nLedgerline Accounts")
    else:
        body = ("Hi {f},\n\nI'm following up on invoice {inv} for {amt}, which was due on {due}. If it's already on "
                "its way, thank you, and please ignore this note. If anything on the invoice looks wrong, just reply "
                "and I'll sort it out.\n\nThanks,\nPriya\nLedgerline Accounts")
    body = body.format(f=first, inv=inv["invoice_id"], amt=amount, due=inv["due_date"])
    return {"to": to, "cc": [], "subject": subject, "body": body, "template": "collections.md#" + stage,
            "source": "template"}


def run_pipeline(rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    rules = rules or load_rules()
    rd = rules.get("reminder_days", DEFAULT_RULES["reminder_days"])
    audit: List[Dict[str, Any]] = []

    def log(ts, agent, otype, oid, decision, conf, reason):
        audit.append({"ts": ts, "agent": agent, "object_type": otype, "object_id": oid, "decision": decision,
                      "confidence": conf, "reason": reason})

    customers: Dict[str, Dict[str, Any]] = {}
    for (cid, name, plan, arr, top50, rank, am, renewal, method, nps, usage) in CUSTOMERS:
        tickets = TICKETS.get(cid, [])
        open_t = [t for t in tickets if t["status"] in ("open", "pending")]
        billing_complaint = any(t["category"] == "Billing" for t in open_t)
        contacts = CONTACTS.get(cid, [])
        flags = []
        if top50:
            flags.append("Top-50 account: a person writes every message")
        if billing_complaint:
            flags.append("Open billing complaint in Zendesk")
        if any(not c["verified"] for c in contacts):
            flags.append("Unverified billing contact on file")
        if renewal and "2026-11-01" <= renewal <= "2026-12-31":
            flags.append("Renewal in flight (" + renewal + ")")
        customers[cid] = {
            "customer_id": cid, "name": name, "plan": plan, "current_arr": float(arr), "top50": top50, "rank": rank,
            "account_manager": am, "renewal_date": renewal, "payment_method": method, "open_tickets": open_t,
            "recent_tickets": tickets, "billing_complaint": billing_complaint, "nps_last": nps, "usage_trend": usage,
            "contacts": contacts, "open_invoices": [], "unapplied_payments": [], "flags": flags,
        }
        log("2026-10-31T06:00:10", "Account Context", "customer", cid, "PROFILED", 1.0,
            "Joined tickets, NPS, usage, contract and contacts. Flags: " + (", ".join(flags) or "none") + ".")

    payments = []
    for (pid, rec, amt, method, payer, memo, cid, decision, invs, conf, reasons) in PAYMENTS:
        reasons = list(reasons)
        if decision == "AUTO_APPLY" and not rules.get("auto_apply_exact_ref_match", True):
            decision = "PROPOSE"
            reasons.append("Auto-apply is switched off in Rules, so this exact match waits for a person.")
        inv_amt = sum(i[2] for i in INVOICES if i[0] in invs)
        diff = round(amt - inv_amt, 2) if invs else amt
        payments.append({
            "payment_id": pid, "received_date": rec, "amount": amt, "method": method, "payer_name": payer, "memo": memo,
            "customer_id": cid, "customer_name": customers[cid]["name"] if cid else None, "decision": decision,
            "invoice_ids": invs, "matched_amount": inv_amt if invs else 0.0, "difference": diff, "confidence": conf,
            "reasons": reasons, "agent": "Cash Application",
        })
        if cid and decision != "AUTO_APPLY":
            customers[cid]["unapplied_payments"].append(pid)
        log("2026-10-31T06:00:0" + str(len(payments) % 10), "Cash Application", "payment", pid, decision, conf,
            " ".join(reasons))

    pending_cash = {}
    for p in payments:
        if p["decision"] == "PROPOSE":
            for i in p["invoice_ids"]:
                pending_cash[i] = p
    applied = {i for p in payments if p["decision"] == "AUTO_APPLY" for i in p["invoice_ids"]}

    invoices = []
    m = {"overdue_balance": 0.0, "overdue_count": 0, "open_ar": 0.0, "cash_found": 0.0, "chases_prevented": 0,
         "auto_applied": 0, "needs_review": 0, "held": 0, "drafts": 0, "human_writes": 0, "collections_complaints": 0}
    for (iid, cid, amt, issue, due, ar_status) in INVOICES:
        cust = customers[cid]
        dpd = _days_past_due(due)
        stage = _stage(dpd, cust["payment_method"], ar_status, rd)
        holds = []
        reasons = []
        if iid in pending_cash:
            p = pending_cash[iid]
            holds.append({"code": "ALREADY_PAID", "label": "Money already received",
                          "detail": "{} received ${:,.2f} by {} on {} from {}. It looks like it pays this invoice but "
                                    "hasn't been applied yet. Chasing now would repeat the Paidly mistake.".format(
                                        p["payment_id"], p["amount"], p["method"].upper(), p["received_date"],
                                        p["payer_name"]),
                          "agent": "Controller"})
        if cust["billing_complaint"]:
            t = [t for t in cust["open_tickets"] if t["category"] == "Billing"][0]
            holds.append({"code": "DISPUTE", "label": "Open billing complaint", "route_to": cust["account_manager"],
                          "release_requires": "Account manager confirms the dispute is settled",
                          "detail": "Ticket {} ({}, {}): \"{}\". Policy: don't chase until the account manager "
                                    "({}) says so.".format(t["ticket_id"], t["priority"], t["status"], t["subject"],
                                                           cust["account_manager"]),
                          "agent": "Controller"})
        if cid == "C1154":
            holds.append({"code": "DISPUTE", "label": "Disputed after billing rewrite", "route_to": cust["account_manager"],
                          "release_requires": "Account manager confirms the dispute is settled",
                          "detail": "Customer disputes a duplicate pro-rata line created by the March 2026 billing "
                                    "engine rewrite. Finance must correct the invoice first.",
                          "agent": "Controller"})
        if any(not c["verified"] for c in cust["contacts"]) and not any(c["verified"] for c in cust["contacts"]):
            holds.append({"code": "CONTACT_UNVERIFIED", "label": "No verified billing contact",
                          "detail": "Every contact on file has an issue (left the firm or a domain that doesn't match "
                                    "the customer). Confirm who to write to before sending.",
                          "agent": "Controller"})
        if cid == "C1301" and stage != "not_due":
            holds.append({"code": "RENEWAL_IN_FLIGHT", "label": "Renewal in flight",
                          "detail": "Renewal date 2026-11-03 has passed and the renewal is being negotiated by "
                                    "Maria Yardley. Check with her before contacting.",
                          "agent": "Controller"})

        draft = None
        if iid in applied:
            action = "NO_ACTION"
            reasons.append("Paid: payment auto-applied by Cash Application.")
            ar = "paid (applied today)"
        else:
            ar = ar_status
            if holds:
                action = "HOLD"
                reasons.append("Held by Controller: " + "; ".join(h["label"] for h in holds) + ".")
            elif stage == "not_due":
                action = "NO_ACTION"
                reasons.append("Not due yet; first reminder is a courtesy note {} days before the due date.".format(
                    -rd.get("courtesy", -5)))
            elif cust["top50"] and rules.get("top50_human_only", True):
                action = "HUMAN_WRITES"
                reasons.append("Top-50 account (rank {}): policy says a person writes and reads every message.".format(
                    cust["rank"]))
                draft = _draft({"invoice_id": iid, "amount": amt, "due_date": due, "days_past_due": dpd,
                                "stage": stage}, cust)
                draft["source"] = "template"
            else:
                action = "DRAFT_REMINDER"
                reasons.append("{} days past due, stage '{}'. No holds found by Controller.".format(dpd, stage))
                draft = _draft({"invoice_id": iid, "amount": amt, "due_date": due, "days_past_due": dpd,
                                "stage": stage}, cust)
        if ar.startswith("paid"):
            pass
        else:
            cust["open_invoices"].append(iid)
            m["open_ar"] += amt
            if dpd > 0:
                m["overdue_balance"] += amt
                m["overdue_count"] += 1
        if action == "HOLD":
            m["held"] += 1
        if action == "DRAFT_REMINDER":
            m["drafts"] += 1
        if action == "HUMAN_WRITES":
            m["human_writes"] += 1
        if any(h["code"] == "ALREADY_PAID" for h in holds) or (iid in applied and dpd > 0):
            m["chases_prevented"] += 1
        invoices.append({
            "invoice_id": iid, "customer_id": cid, "customer_name": cust["name"], "amount": amt, "issue_date": issue,
            "due_date": due, "days_past_due": dpd, "ar_status": ar, "stage": stage, "action": action, "holds": holds,
            "draft": draft, "top50": cust["top50"], "account_manager": cust["account_manager"], "reasons": reasons,
        })
        log("2026-10-31T06:00:30", "Controller" if holds else "Collections", "invoice", iid, action,
            0.95 if holds else 0.9, " ".join(reasons))

    for p in payments:
        if p["decision"] == "AUTO_APPLY":
            m["auto_applied"] += 1
        else:
            m["needs_review"] += 1
        if p["decision"] in ("AUTO_APPLY", "PROPOSE") and p["invoice_ids"]:
            m["cash_found"] += p["amount"]

    # Card re-run example (card on file worked again after the failed charge) and a decision routed to Dana.
    invoices.append({
        "invoice_id": "INV-25803", "customer_id": "C1662", "customer_name": customers["C1662"]["name"], "amount": 1836.0,
        "issue_date": "2026-09-02", "due_date": "2026-09-02", "days_past_due": 59, "ar_status": "overdue",
        "stage": "card_failed", "action": "RETRY_CARD", "holds": [], "draft": None, "top50": False,
        "account_manager": customers["C1662"]["account_manager"],
        "retry": {"card_works": True, "evidence": "PAY-65695: card charge of $1,836.00 succeeded on 2026-10-02",
                  "needs": "Priya approves the re-run"},
        "reasons": ["Card works again (PAY-65695 succeeded on 2026-10-02). Re-run the failed charge?"]})
    for i in invoices:
        if i["invoice_id"] == "INV-25990":
            i["holds"].append({"code": "CARD_WRITEOFF_SOON", "label": "Decision for Dana today: card write-off soon",
                               "detail": "Policy writes off card invoices unpaid at 150 days. Decide: call or let it go.",
                               "agent": "Controller", "route_to": "Dana Ruiz (VP Finance)"})
    m.update({"overdue_already_paid": 0.0, "overdue_disputed": 0.0, "overdue_collectable": m["overdue_balance"],
              "collections_complaints_baseline": 1, "complaint_keyword_hits": 14, "card_retries": 1,
              "dana_decisions": 1})
    for i in invoices:
        if i["days_past_due"] > 0 and not i["ar_status"].startswith("paid"):
            codes = {h["code"] for h in i["holds"]}
            if "ALREADY_PAID" in codes:
                m["overdue_already_paid"] += i["amount"]
            elif "DISPUTE" in codes:
                m["overdue_disputed"] += i["amount"]
    m["overdue_collectable"] = m["overdue_balance"] - m["overdue_already_paid"] - m["overdue_disputed"]
    invoices.sort(key=lambda i: -i["amount"])
    return {"as_of": AS_OF.isoformat(), "metrics": m, "payments": payments, "invoices": invoices,
            "customers": customers, "audit": audit, "rules": rules}
