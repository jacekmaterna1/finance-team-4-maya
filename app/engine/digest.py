"""Priya's Slack morning digest (Maya, T+0:17: 'Priya lives in Slack ... a short morning digest that links to the queue').

Returns Slack mrkdwn text. In this demo it is shown on a page and not posted; posting is one webhook call.
"""


def _usd(x):
    return "$" + format(x, ",.0f")


def build_digest(state, base_url=""):
    m = state["metrics"]
    inv = state["invoices"]
    pays = state["payments"]
    q = (base_url or "") + "/collections"
    lines = [
        "*Good morning Priya. Collections for %s*" % state["as_of"],
        "Overdue on the ledger: *%s* (%d invoices). Already received: %s. Disputed: %s. Collectable: *%s*." % (
            _usd(m["overdue_balance"]), m["overdue_count"], _usd(m["overdue_already_paid"]), _usd(m["overdue_disputed"]),
            _usd(m["overdue_collectable"])),
        "",
        ":white_check_mark: Applied overnight (exact amount + invoice reference): %d" % m["auto_applied"],
    ]
    for p in pays:
        if p["decision"] == "AUTO_APPLY":
            lines.append("   • %s %s → %s" % (p["customer_name"], _usd(p["amount"]), ", ".join(p["invoice_ids"])))
    lines.append(":eyes: Payments to confirm: %d" % m["needs_review"])
    for p in pays:
        if p["decision"] != "AUTO_APPLY":
            lines.append("   • %s %s → %s (%s)" % (p["customer_name"] or p["payer_name"], _usd(p["amount"]),
                                                 ", ".join(p["invoice_ids"]) or "no match", "confidence %.0f%%" % (100 * p["confidence"])))
    dana = [i for i in inv if any(h.get("route_to", "").startswith("Dana") for h in i["holds"])]
    if dana:
        lines.append(":rotating_light: Needs Dana today: " + "; ".join("%s %s (%s)" % (i["customer_name"], _usd(i["amount"]),
                     next(h["label"] for h in i["holds"] if h.get("route_to", "").startswith("Dana"))) for i in dana))
    lines += [
        ":email: Reminders drafted for your approval: %d" % m["drafts"],
        ":credit_card: Card re-runs to approve: %d" % m.get("card_retries", 0),
        ":raised_hand: Held (not chased): %d. Disputes sent to account managers with a summary." % m["held"],
        ":writing_hand: You or Dana to write personally: %d" % m["human_writes"],
        "",
        "<%s|Open the queue>" % q,
    ]
    return "\n".join(lines)
