"""Account Context agent: one view of each customer with open AR (finance cannot see Zendesk today).

It reads support ticket text to find invoice disputes, cancellation notices and legal threats -- including
tickets marked 'solved' where the customer still says they will not pay. Read-only: it never acts.
"""
import re

import pandas as pd

from . import llm
from .data import AS_OF, domain_of

AGENT = "Account Context"

REFUSAL = [r"will not (?:be )?pay", r"refus\w* to pay", r"overcharg\w+", r"won'?t (?:be )?pay", r"wont (?:be )?pay", r"not (?:be )?paying", r"not authori[sz]ing payment", r"payment is on hold",
           r"paused payment", r"unable to process payment", r"settle once", r"won'?t pay an invoice", r"until (?:it'?s|its) fixed",
           r"void it please", r"cancel and reissue", r"issue a revised invoice", r"remove it and resend", r"we are not paying",
           r"payment (?:is )?on hold", r"pending a corrected invoice", r"not paying for", r"not before", r"we'?ll pay once",
           r"put the whole th", r"reissue it"]
# Unambiguous refusals count in any ticket category (QA T+0:45: "refuse to pay" in a How-to ticket was missed).
STRONG_REFUSAL = [r"will not (?:be )?pay", r"refus\w* to pay", r"won'?t (?:be )?pay", r"wont (?:be )?pay", r"not (?:be )?paying",
                  r"we are not paying", r"not authori[sz]ing payment"]
LEGAL = [r"chargeback", r"contest(?:ing)? the charge", r"consumer affairs", r"lawyer", r"attorney", r"legal action", r"small claims", r"solicitor"]
CANCEL = [r"discontinu\w+ ledgerline", r"termination of services", r"notice of termination", r"cancel(?:l)?ing (?:our )?(?:ledgerline|subscription|account)",
          r"no further direct debits"]
COLLECTIONS_COMPLAINT = [r"already paid", r"chas(?:ed|ing) (?:us|me)", r"reminder (?:email|emails)", r"overdue notice", r"final notice", r"threaten"]


def _any(patterns, text):
    return [p for p in patterns if re.search(p, text, flags=re.I)]


def heuristic_read(t, own_invoices):
    text = "%s\n%s" % (t.get("subject", ""), t.get("body", ""))
    refs = sorted(set(re.findall(r"INV-\d{5}", text)))
    own_refs = [r for r in refs if r in own_invoices]
    refusal, legal, cancel = _any(REFUSAL, text), _any(LEGAL, text), _any(CANCEL, text)
    complaint = _any(COLLECTIONS_COMPLAINT, text)
    kind = "other"
    if legal:
        kind = "legal_threat"
    elif cancel:
        kind = "cancellation"
    elif own_refs:
        # A customer quoting one of their own open Ledgerline invoice numbers is almost always raising a problem with it,
        # whatever category the agent tagged (data shows disputes tagged How-to or untagged).
        kind = "dispute"
    elif _any(STRONG_REFUSAL, text) or (refusal and str(t.get("category")) in ("Billing", "Account change")):
        kind = "dispute"
    about = bool(own_refs or legal or cancel or _any(STRONG_REFUSAL, text) or (refusal and str(t.get("category")) in ("Billing", "Account change")))
    return {
        "about_ledgerline_invoice": about,
        "invoice_ids": own_refs,
        "kind": kind if about else ("product_question" if not complaint else "collections_complaint"),
        "refuses_to_pay_until_fixed": bool(refusal),
        "collections_complaint": bool(complaint),
        "summary": (t.get("subject") or "")[:120],
        "confidence": 0.75 if about else 0.6,
        "source": "rules",
        "signals": refusal + legal + cancel,
    }


def redact(text):
    """Remove email addresses and phone numbers before ticket text leaves our systems (see submission/LEGAL_NOTE.md)."""
    text = re.sub(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", "[email]", str(text))
    return re.sub(r"\+?\d[\d ()\-]{7,}\d", "[phone]", text)


def claude_read(t, own_invoices, customer_name, enabled):
    if not enabled:
        return None
    system = llm.manual("account_context") or "You read support tickets for a finance team."
    t = dict(t, subject=redact(t.get("subject")), body=redact(t.get("body")))
    user = (
        "Customer: %s\nThis customer's open Ledgerline invoices: %s\nTicket %s (%s, category=%s, status=%s, priority=%s)\n"
        "Subject: %s\nBody:\n%s\n\nReturn JSON with keys: about_ledgerline_invoice (bool: is the customer disputing or questioning "
        "an invoice LEDGERLINE sent THEM, as opposed to asking about invoices they send their own clients in the product), "
        "invoice_ids (list of Ledgerline invoice ids it concerns, only from the list above), kind (one of dispute, cancellation, "
        "legal_threat, collections_complaint, payment_question, product_question, other), refuses_to_pay_until_fixed (bool), "
        "collections_complaint (bool), summary (<=25 words, plain English, for the AR specialist), confidence (0-1)."
    ) % (customer_name, ", ".join(own_invoices) or "none", t["ticket_id"], t["created_at"], t.get("category"), t.get("status"),
         t.get("priority"), t.get("subject"), str(t.get("body"))[:2500])
    r = llm.ask_json("ticket_read_v1", system, user, enabled=enabled)
    if not isinstance(r, dict):
        return None
    r["invoice_ids"] = [i for i in r.get("invoice_ids", []) if i in own_invoices]
    r["source"] = "claude"
    return r


def build(d, rules, customer_ids, cash_results):
    cus = d["customers"].set_index("customer_id")
    inv, tk, con, nps, use = d["invoices"], d["tickets"], d["contacts"], d["nps"], d["usage"]
    open_inv = inv[inv["status"].isin(("open", "overdue", "payment_failed"))]
    issue_by_id = dict(zip(open_inv["invoice_id"], open_inv["issue_date"]))
    # Read a full year of tickets: legal threats and cancellation notices stay relevant longer than ordinary disputes
    # (QA T+0:30: Drummond's chargeback ticket fell one day outside a 120-day window). The Controller applies the
    # shorter dispute window itself.
    lookback = AS_OF - pd.Timedelta(days=max(365, int(rules.get("dispute_lookback_days", 120))))
    use_claude = bool(rules.get("use_claude", False))
    out, audit = {}, []
    for cid in sorted(set(customer_ids)):
        if cid not in cus.index:
            continue
        c = cus.loc[cid]
        own = list(open_inv[open_inv["customer_id"] == cid]["invoice_id"])
        ctk = tk[(tk["customer_id"] == cid) & (tk["created_at"] >= lookback)].sort_values("created_at", ascending=False)
        tickets = []
        for _, t in ctk.iterrows():
            td = t.to_dict()
            td["created_at"] = t["created_at"].strftime("%Y-%m-%d %H:%M")
            # Only invoices that existed when the ticket was written can be what it is about (QA/analyst: Reyes was a
            # false positive because the ticket predates INV-26009).
            own_then = [i for i in own if issue_by_id.get(i, t["created_at"]) <= t["created_at"]]
            read = claude_read(td, own_then, c["name"], use_claude) or heuristic_read(td, own_then)
            tickets.append({"ticket_id": t["ticket_id"], "created_at": td["created_at"], "subject": t["subject"],
                            "category": t["category"] if isinstance(t["category"], str) else "untagged",
                            "priority": t["priority"], "status": t["status"], "requester_email": t["requester_email"],
                            "body": str(t["body"]), "read": read, "summary": read.get("summary")})
            if read.get("about_ledgerline_invoice"):
                audit.append({"agent": AGENT, "object_type": "ticket", "object_id": t["ticket_id"], "decision": read.get("kind"),
                              "confidence": read.get("confidence", 0.7),
                              "reason": "%s: %s (read by %s)" % (c["name"], read.get("summary"), read.get("source"))})
        # contacts: verified = email domain matches the customer's website domain and the person is still there
        contacts = []
        for _, p in con[con["customer_id"] == cid].iterrows():
            issue = None
            dom = domain_of(p["email"])
            if p["status"] != "active":
                issue = "Left the firm but still on invoice emails"
            elif dom != c["domain"]:
                issue = "Email domain %s does not match the customer's domain %s" % (dom, c["domain"])
            contacts.append({"name": "%s %s" % (p["first_name"], p["last_name"]), "email": p["email"], "role": p["role"],
                             "status": p["status"], "verified": issue is None, "issue": issue})
        n = nps[nps["customer_id"] == cid].sort_values("responded_on")
        u = use[use["customer_id"] == cid].sort_values("month")
        trend = "unknown"
        if len(u) >= 6:
            recent, prior = u["active_users"].tail(3).mean(), u["active_users"].iloc[-6:-3].mean()
            if prior > 0:
                ch = (recent - prior) / prior
                trend = "falling (%+.0f%%)" % (ch * 100) if ch < -0.15 else ("rising (%+.0f%%)" % (ch * 100) if ch > 0.15 else "steady")
        flags = []
        renewal = c["renewal_date"] if isinstance(c["renewal_date"], str) else None
        if renewal:
            days = (pd.Timestamp(renewal) - AS_OF).days
            if 0 <= days <= int(rules.get("renewal_notice_days", 45)):
                flags.append("Renewal in %d days (%s)" % (days, renewal))
        if trend.startswith("falling"):
            flags.append("Usage %s" % trend)
        if len(n) and n["score"].iloc[-1] <= 6:
            flags.append("Last NPS score %d (detractor)" % n["score"].iloc[-1])
        unapplied = [p["payment_id"] for p in cash_results if p["customer_id"] == cid]
        out[cid] = {
            "customer_id": cid, "name": c["name"], "plan": c["plan"], "status": c["status"],
            "current_arr": float(c["current_arr"]), "rank": int(c["rank"]) if pd.notna(c["rank"]) else None,
            "top50": bool(pd.notna(c["rank"]) and c["rank"] <= 50), "account_manager": c["account_manager"],
            "renewal_date": renewal, "payment_method": c["payment_method"], "website": c["website"],
            "open_tickets": [t for t in tickets if t["status"] in ("open", "pending")],
            "recent_tickets": tickets,
            "billing_complaint": any(t["read"].get("about_ledgerline_invoice") for t in tickets),
            "nps_last": int(n["score"].iloc[-1]) if len(n) else None,
            "usage_trend": trend, "contacts": contacts, "open_invoices": own, "unapplied_payments": unapplied, "flags": flags,
        }
    return out, audit
