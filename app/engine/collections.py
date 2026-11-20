"""Collections agent: pick the policy stage for each unpaid invoice and draft the reminder.

Templates are Ledgerline's own (docs/templates/collections.md), with two changes agreed from Maya's answer:
the 2021 7-day template is rewritten in the friendlier 21-day voice, and the 45-day 'FINAL NOTICE: suspension'
template is retired. Claude personalises the draft when an API key is set; the Controller checks every draft.
"""
from . import llm

AGENT = "Collections"

TEMPLATES = {
    "courtesy": ("Ledgerline invoice {inv} due {due}",
                 "Hi {first},\n\nA quick heads-up that invoice {inv} for {amount} is due on {due}.\n\nIf {company} pays by card on file, there's nothing you need to do. We'll charge it on the due date. If you pay by bank transfer, our remittance details are on the invoice and under Settings > Billing engine.\n\nIf anything looks off, like the seat count, plan or billing contact, just reply here before the due date and we'll fix it rather than have you pay the wrong amount.\n\nThanks,\nPriya Nair\nLedgerline Billing"),
    "first": ("Invoice {inv} — a quick check",
              "Hi {first},\n\nInvoice {inv} for {amount} was due on {due} and still shows as open on our side.\n\nIf you've already sent it, thank you, and please reply with the payment date so we can match it (bank transfers can take a few days to reach us). If something on the invoice isn't right, tell me and I'll get it corrected before you pay.\n\nYou can pay by card or bank transfer here: {link}\n\nThanks,\nPriya Nair\nLedgerline Billing"),
    "second": ("Invoice {inv} is now {dpd} days overdue",
               "Hi {first},\n\nI'm following up on invoice {inv} for {amount}, which was due on {due} and is still unpaid.\n\nI know these sometimes get stuck in an approval queue or go to someone who's left. If that's what happened, let me know who should be getting our invoices and I'll update the billing contact for {company}.\n\nIf there's a problem with the invoice itself, or you need to split the payment, reply and we can work something out. Otherwise, you can pay here: {link}\n\nThanks,\nPriya Nair\nLedgerline Billing"),
    "final": ("Invoice {inv}: can we sort this out this week?",
              "Hi {first},\n\nInvoice {inv} for {amount} is now {dpd} days past its due date of {due}, and I haven't been able to reach the right person.\n\nI'd like to resolve it with you directly. If cash flow is the issue, we can set up a payment plan. If the invoice is wrong, I'll get it corrected. Could you reply with a time for a 10-minute call this week, or with the date we can expect payment?\n\nPay online: {link}\n\nThanks,\nPriya Nair\nLedgerline Billing"),
    "card_failed": ("Your card payment for invoice {inv} didn't go through",
                    "Hi {first},\n\nThe card payment for invoice {inv} ({amount}) didn't go through, and our automatic retries haven't succeeded either. This usually means the card on file has expired or been replaced.\n\nYou can update the card under Settings > Billing engine, or pay this invoice directly here: {link}\n\nIf you'd rather switch to bank transfer, just reply and I'll send the details.\n\nThanks,\nPriya Nair\nLedgerline Billing"),
}


def stage_for(dpd, ar_status, rules):
    rd = rules["reminder_days"]
    if ar_status == "payment_failed":
        return "card_failed"
    if dpd < rd["courtesy"]:
        return "not_due"
    if dpd < 0:
        return "courtesy"
    if dpd < rd["first"]:
        return "wait"
    if dpd < rd["second"]:
        return "first"
    if dpd < rd["final"]:
        return "second"
    if dpd < rd["escalate"]:
        return "final"
    return "escalate"


def recipients(ctx):
    cs = ctx.get("contacts", []) if ctx else []
    billing = [c for c in cs if c["verified"] and "billing" in c["role"].lower()]
    admin = [c for c in cs if c["verified"] and "admin" in c["role"].lower()]
    return billing or admin


def draft(inv, ctx, stage, rules, am_email=None):
    if stage not in TEMPLATES:
        tmpl_stage = "final" if stage == "escalate" else None
        if not tmpl_stage:
            return None
        stage_key = tmpl_stage
    else:
        stage_key = stage
    to = recipients(ctx)
    if not to:
        return None
    first = to[0]["name"].split()[0]
    subj_t, body_t = TEMPLATES[stage_key]
    vals = {"inv": inv["invoice_id"], "due": inv["due_date"], "amount": "$" + format(inv["amount"], ",.2f"),
            "company": ctx["name"], "first": first, "dpd": inv["days_past_due"],
            "link": "https://pay.ledgerline.com/%s" % inv["invoice_id"]}
    d = {"to": [c["email"] for c in to[:2]], "cc": [am_email] if (am_email and rules.get("notify_am_before_contact", True)) else [],
         "subject": subj_t.format(**vals), "body": body_t.format(**vals), "template": stage_key, "source": "template"}

    # Personalise with Claude (only when Legal has approved: use_claude defaults to False).
    # Data minimisation, as promised to Maya: Claude sees ONLY invoice facts and the template. Names stay as
    # placeholders and are filled in locally afterwards; no plan, NPS, usage, contacts or bank details are sent.
    if rules.get("use_claude", False):
        masked = dict(vals, first="{first}", company="{company}")
        note = ("Since March 2026 the billing engine retries failed cards three times and emails the client after each retry."
                if stage == "card_failed" else "none")
        system = llm.manual("collections")
        user = ("Rewrite this payment reminder in the voice of a thoughtful AR specialist. Keep every fact (invoice id, amount, "
                "dates, link) exactly, and keep the placeholders {first} and {company} as they are. No threats, no mention of "
                "suspension, legal action or agencies. Under 140 words. Stage: %s, %s days past due. Note: %s\n\nSUBJECT: %s\n\n%s\n\n"
                "Return JSON {\"subject\": str, \"body\": str}.") % (stage, inv["days_past_due"], note,
                                                                     subj_t.format(**masked), body_t.format(**masked))
        r = llm.ask_json("draft_v2", system, user, enabled=True, max_tokens=700)
        if isinstance(r, dict) and r.get("body") and inv["invoice_id"] in r["body"]:
            fill = lambda s: s.replace("{first}", first).replace("{company}", ctx["name"])
            d["subject"], d["body"], d["source"] = fill(r.get("subject") or d["subject"]), fill(r["body"]), "claude"
    d["data_sent_to_ai"] = "invoice id, amount, due date, days past due, payment link" if d["source"] == "claude" else "none"
    return d
