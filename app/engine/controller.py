"""Controller agent: decides what must NOT go out, and who has to write what. It can hold or block, never send.

Each hold has a code, a plain-English label and the detail Priya needs to decide whether to release it.
"""
AGENT = "Controller"

HARD_HOLDS = {"MONEY_RECEIVED", "DISPUTE", "CANCELLATION", "OPEN_ESCALATION", "NO_VALID_CONTACT"}
HUMAN_CODES = {"LEGAL_RISK", "TOP50", "ESCALATE_90", "CARD_WRITEOFF_SOON"}


def holds_for(inv, ctx, cash_by_invoice, cash_by_customer, rules, unidentified=None):
    holds = []
    iid, dpd = inv["invoice_id"], inv["days_past_due"]

    # 1. The Paidly failure: never chase money we already have.
    if iid in cash_by_invoice:
        p = cash_by_invoice[iid]
        if p["decision"] == "AUTO_APPLY":
            holds.append({"code": "PAID", "label": "Paid: applied by the Cash Application agent",
                          "detail": "%s for $%s received %s, matched on amount and invoice reference." % (p["payment_id"], format(p["amount"], ",.2f"), p["received_date"]),
                          "agent": "Cash Application"})
        else:
            holds.append({"code": "MONEY_RECEIVED", "label": "Money already received, not applied yet",
                          "detail": "%s for $%s received %s looks like payment for this invoice (%s). Confirm the match on Cash application; do not chase." %
                                    (p["payment_id"], format(p["amount"], ",.2f"), p["received_date"], p["reasons"][-1]),
                          "agent": "Cash Application"})
    else:
        for p in cash_by_customer.get(inv["customer_id"], []):
            if abs(p["amount"] - inv["amount"]) < 0.01 or p["decision"] == "EXCEPTION":
                holds.append({"code": "MONEY_RECEIVED", "label": "Unapplied payment from this customer",
                              "detail": "%s for $%s received %s is not applied to any invoice yet. It may cover this one." % (p["payment_id"], format(p["amount"], ",.2f"), p["received_date"]),
                              "agent": "Cash Application"})
                break
    # QA severity-1 fix (T+0:31): a receipt we cannot tie to a customer (e.g. payer shortened to "BRANDT") must still
    # stop the chase of any invoice it could be paying.
    if not any(h["code"] in ("PAID", "MONEY_RECEIVED") for h in holds):
        for p in unidentified or []:
            if abs(p["amount"] - inv["amount"]) < 0.01:
                holds.append({"code": "MONEY_RECEIVED", "label": "Possible payment from an unidentified payer",
                              "detail": "%s for $%s from '%s' received %s is not tied to any customer yet, and it matches this invoice's amount. Identify the payer before chasing." %
                                        (p["payment_id"], format(p["amount"], ",.2f"), p["payer_name"], p["received_date"]),
                              "agent": "Cash Application"})
                break

    # 2. What support knows and finance doesn't.
    import pandas as _pd0
    dispute_since = (_pd0.Timestamp("2026-10-31") - _pd0.Timedelta(days=int(rules.get("dispute_lookback_days", 120)))).strftime("%Y-%m-%d")
    for t in (ctx or {}).get("recent_tickets", []):
        r = t["read"]
        if not r.get("about_ledgerline_invoice"):
            continue
        names_this = iid in r.get("invoice_ids", [])
        names_none = not r.get("invoice_ids")
        if r.get("kind") == "legal_threat":
            holds.append({"code": "LEGAL_RISK", "label": "Legal or chargeback threat in support",
                          "detail": "%s (%s, status %s): %s. VP Finance must handle; no automated message." % (t["ticket_id"], t["created_at"][:10], t["status"], r.get("summary")),
                          "agent": "Account Context"})
        elif r.get("kind") == "cancellation":
            holds.append({"code": "CANCELLATION", "label": "Customer gave notice to cancel",
                          "detail": "%s (%s): %s. Confirm the final amount owing with the account manager before any reminder." % (t["ticket_id"], t["created_at"][:10], r.get("summary")),
                          "agent": "Account Context"})
        elif r.get("kind") == "dispute" and t["created_at"][:10] >= dispute_since and (names_this or (names_none and r.get("refuses_to_pay_until_fixed"))):
            solved = " The ticket is marked '%s' but the customer said they won't pay until it is fixed." % t["status"] if t["status"] == "solved" and r.get("refuses_to_pay_until_fixed") else ""
            holds.append({"code": "DISPUTE", "label": "Invoice disputed in support",
                          "detail": "%s (%s): %s.%s Account manager decides when to resume (policy)." % (t["ticket_id"], t["created_at"][:10], r.get("summary"), solved),
                          "agent": "Account Context"})
    import pandas as _pd
    window = _pd.Timestamp("2026-10-31") - _pd.Timedelta(days=int(rules.get("hold_on_open_ticket_days", 30)))
    for t in (ctx or {}).get("open_tickets", []):
        recent = _pd.Timestamp(t["created_at"]) >= window or t["status"] == "open"
        if t["priority"] in ("high", "urgent") and recent:
            holds.append({"code": "OPEN_ESCALATION", "label": "Open high-priority support ticket",
                          "detail": "%s '%s' is %s (%s priority). Policy: don't chase during an open escalation until the AM says so." % (t["ticket_id"], t["subject"], t["status"], t["priority"]),
                          "agent": "Account Context"})
            break

    # 3. Who it can go to.
    contacts = (ctx or {}).get("contacts", [])
    billing_ok = [c for c in contacts if c["verified"] and "billing" in c["role"].lower()]
    admin_ok = [c for c in contacts if c["verified"] and "admin" in c["role"].lower()]
    stale = [c for c in contacts if c["issue"] and "billing" in c["role"].lower()]
    if not billing_ok and not admin_ok:
        holds.append({"code": "NO_VALID_CONTACT", "label": "No verified billing contact",
                      "detail": "No active contact whose email matches the customer's domain. Ask the AM for the right person.", "agent": "Controller"})
    elif stale:
        holds.append({"code": "STALE_CONTACT", "label": "Billing contact has left",
                      "detail": "%s (%s). Excluded from the draft; sent to %s instead." % (stale[0]["email"], stale[0]["issue"], (billing_ok or admin_ok)[0]["email"]),
                      "agent": "Controller"})

    # 4. Who has to write it.
    if ctx and ctx.get("top50") and rules.get("top50_human_only", True):
        holds.append({"code": "TOP50", "label": "Top-50 account (#%s by ARR)" % ctx.get("rank"),
                      "detail": "Policy: nothing goes to a top-50 account without a person reading it first. The draft is a starting point only.", "agent": "Controller"})
    if dpd >= rules["reminder_days"]["escalate"]:
        holds.append({"code": "ESCALATE_90", "label": "90+ days overdue",
                      "detail": "Escalate to VP Finance (process map): phone call and payment-plan offer, not another email.", "agent": "Controller"})
    if inv["ar_status"] == "payment_failed" and dpd >= int(rules.get("card_writeoff_warning_days", 140)):
        holds.append({"code": "CARD_WRITEOFF_SOON", "label": "Automatic card write-off in %d days" % max(0, 150 - dpd),
                      "detail": "Policy writes off card invoices unpaid at 150 days. Decide now: call the customer or let it write off.", "agent": "Controller"})
    for f in (ctx or {}).get("flags", []):
        if f.startswith("Renewal"):
            holds.append({"code": "RENEWAL_SOON", "label": f, "detail": "Tell the account manager before finance contacts the account.", "agent": "Account Context"})
    return holds


def decide(inv, holds, stage):
    codes = {h["code"] for h in holds}
    if "PAID" in codes:
        return "NO_ACTION"
    if codes & HARD_HOLDS:
        return "HOLD"
    # Review T+0:48: a top-50 invoice that isn't due yet needs no message at all, so it shouldn't sit in Priya's
    # "write it yourself" queue. Legal risk and card write-off decisions still surface whatever the stage.
    if stage in ("not_due", "wait") and not (codes & {"LEGAL_RISK", "CARD_WRITEOFF_SOON", "ESCALATE_90"}):
        return "NO_ACTION"
    if codes & HUMAN_CODES:
        return "HUMAN_WRITES"
    if stage == "not_due" or stage == "wait":
        return "NO_ACTION"
    return "DRAFT_REMINDER"


def check_draft(draft, rules):
    """Block any draft containing banned (threatening) language. Returns list of problems."""
    if not draft:
        return []
    import re as _re
    text = (draft.get("subject", "") + "\n" + draft.get("body", "")).lower()
    # word-boundary match (QA: "court" must not match "courtesy")
    return [p for p in rules.get("banned_phrases", []) if _re.search(r"\b" + _re.escape(p.lower()) + r"\b", text)]
