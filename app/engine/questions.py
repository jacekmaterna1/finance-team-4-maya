"""Open questions the team needs Maya (or Dana / the AMs through Maya) to answer.

Rule (Jacek, T+0:25): we only write to Maya for a Confirmation (a decision she or Dana owns) or Intel (facts the
data room can't give us). Questions are generated from the current run, so they disappear once the underlying
item is resolved. A person approves each one in the RIG before it is sent; approved questions go out bundled in
one message to save Maya's 60-message budget.
"""
import hashlib

# Disputes the data-room review could not settle from records alone (analysis/DISCREPANCIES.md, check 1).
NEEDS_DECISION = {
    "INV-25787": "Riverside Partners: the invoice bills 46 seats, but they say the workspace merge double-counted people (38 active). Exposure up to $8,448",
    "INV-25765": "Okafor & Nakamura: a verbal 50% second-office discount from their AM is not in the contract. Exposure up to $5,856",
    "INV-25750": "Thackeray Accounting: they claim VAT reverse charge, but our customer record says US. A tax call",
    "INV-25757": "Ellery Consulting: sales tax at their old address. A tax call",
    "INV-25822": "Brandt Ashby IT: billed an annual renewal after moving to monthly. Cash timing only",
}


def _qid(*parts):
    return "Q-" + hashlib.sha1("|".join(parts).encode()).hexdigest()[:8]


def _usd(x):
    return "$" + format(x, ",.0f")


def build_open_questions(state):
    inv = state["invoices"]
    by_id = {i["invoice_id"]: i for i in inv}
    qs = []

    # 1. Holds that exist only because of an open high-priority PRODUCT ticket (policy says hold; arguably too cautious).
    prod = [i for i in inv if i["action"] == "HOLD" and {h["code"] for h in i["holds"]} <= {"OPEN_ESCALATION", "TOP50", "RENEWAL_SOON", "STALE_CONTACT"}
            and any(h["code"] == "OPEN_ESCALATION" for h in i["holds"])]
    if prod:
        per = {}
        for i in prod:
            per.setdefault(i["customer_name"], []).append(i["amount"])
        names = "; ".join("%s (%d invoice%s, %s)" % (c, len(a), "s" if len(a) > 1 else "", _usd(sum(a))) for c, a in per.items())
        qs.append({"id": _qid("product-escalation", *sorted(i["invoice_id"] for i in prod)), "purpose": "Confirmation", "owner": "Maya",
                   "topic": "Holds caused only by open product tickets",
                   "text": "Policy says don't chase during an open escalation, so we're holding %s because each has an open high-priority product ticket, not a billing complaint. Should these stay held until support closes the ticket, or can Priya chase them?" % names,
                   "why": "Over-holding is safe but costs cash. These are the only holds not caused by money received, a dispute or a legal threat.",
                   "changes": "Controller rule for OPEN_ESCALATION (product vs billing tickets)", "invoices": [i["invoice_id"] for i in prod]})

    # 2. Dana's thresholds before Monday.
    r = state["rules"]
    qs.append({"id": _qid("dana-thresholds", str(r.get("auto_apply_max_amount")), str(r.get("writeoff_threshold"))), "purpose": "Confirmation", "owner": "Dana via Maya",
               "topic": "Dana's two thresholds for Monday",
               "text": "For Dana before Monday: the agent applies a payment by itself only when the amount and invoice number match exactly and it's under %s; everything else goes to Priya. Write-offs stay at %s, meaning never automatic. Does Dana confirm both numbers?" % (_usd(r.get("auto_apply_max_amount", 10000)), _usd(r.get("writeoff_threshold", 0))),
               "why": "Maya: Dana must see the auto-apply threshold before go-live. Without a cap, a $62,688 receipt could apply with nobody looking.",
               "changes": "rules.auto_apply_max_amount, rules.writeoff_threshold", "invoices": []})

    # 3. Dana decisions: card write-offs.
    dana = [i for i in inv if any((h.get("route_to") or "").startswith("Dana") for h in i["holds"])]
    if dana:
        bits = []
        for i in dana:
            codes = {h["code"] for h in i["holds"]}
            if "WRITEOFF_OVER_LIMIT" in codes:
                bits.append("%s %s would auto-write-off above her $2,000 limit%s" % (i["customer_name"], _usd(i["amount"]), " (they also threatened a chargeback)" if "LEGAL_RISK" in codes else ""))
            else:
                n = max(0, 150 - i["days_past_due"])
                bits.append("%s %s writes off %s although their card has since worked" % (i["customer_name"], _usd(i["amount"]), "tomorrow" if n <= 1 else "in %d days" % n))
        qs.append({"id": _qid("dana-writeoffs", *sorted(i["invoice_id"] for i in dana)), "purpose": "Confirmation", "owner": "Dana via Maya",
                   "topic": "Card write-offs that need Dana",
                   "text": "Dana's call on card write-offs: %s. Re-run the card, call the customer, or let it write off?" % "; ".join(bits),
                   "why": "Policy writes off unpaid card invoices at 150 days. Nine past auto write-offs ($47,251) went over Dana's limit without her.",
                   "changes": "Card re-run approvals for these invoices", "invoices": [i["invoice_id"] for i in dana]})

    # 4. Disputes that need an AM or tax decision.
    open_ids = [k for k in NEEDS_DECISION if k in by_id and by_id[k]["action"] == "HOLD"]
    if open_ids:
        qs.append({"id": _qid("am-disputes", *open_ids), "purpose": "Intel", "owner": "Account managers via Maya",
                   "topic": "Disputes our records can't settle",
                   "text": "All 14 disputed invoices match their contracts, but %d need a person to decide: %s. Can you get the account managers (and whoever owns tax) to rule on these this week, so Priya can release or credit them?" % (len(open_ids), "; ".join(NEEDS_DECISION[k].split(":")[0] for k in open_ids)),
                   "why": "Total exposure is about $25k, against about $313k held over disputes. The other 9 can be released with a reply quoting the contract.",
                   "changes": "Release or credit per dispute; AM confirms release (rule from Maya, T+0:17)", "invoices": open_ids,
                   "detail": [NEEDS_DECISION[k] for k in open_ids]})

    # 5. Cancellation notice not reflected anywhere.
    canc = [i for i in inv if any(h["code"] == "CANCELLATION" for h in i["holds"])]
    for i in canc:
        cust = state["customers"].get(i["customer_id"], {})
        qs.append({"id": _qid("cancellation", i["customer_id"]), "purpose": "Confirmation", "owner": "Maya",
                   "topic": "Cancellation notice nobody acted on",
                   "text": "%s gave written notice to cancel (their ticket in August), but nothing in billing reflects it and their renewal date is %s. Should finance stop the renewal and agree a final balance instead of chasing %s?" % (i["customer_name"], cust.get("renewal_date") or "soon", _usd(i["amount"])),
                   "why": "Chasing or renewing a customer who has cancelled is the kind of message that reaches the CEO.",
                   "changes": "Hold stays; renewal invoicing flagged", "invoices": [i["invoice_id"]]})

    # 6. Intel: invoice PDFs.
    qs.append({"id": _qid("invoice-pdfs"), "purpose": "Intel", "owner": "Maya",
               "topic": "Invoice line items",
               "text": "Our invoice records carry one total per invoice, with no line items, tax or credit notes, so we can't see fees like Westbrook's implementation charge. Could someone send the PDF of INV-25730, so we can check that what customers see matches the ledger?",
               "why": "Several dispute claims contradict our records (plan names, payment method, country). The PDF settles whether the customer or the data is wrong.",
               "changes": "Contract check reads line items", "invoices": ["INV-25730"]})
    return qs
