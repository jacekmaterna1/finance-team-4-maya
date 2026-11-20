"""Cash Application agent: match unapplied receipts to open invoices.

Autonomy (from Maya, T+0:05): apply automatically ONLY when amount and invoice reference both match exactly.
Everything else is a proposal for Priya, with the reasons spelled out.
"""
import difflib
import itertools
import re

from .data import core_tokens, norm_name

AGENT = "Cash Application"
OPEN_STATUSES = ("open", "overdue", "payment_failed")


def _refs_in_memo(memo):
    """Find invoice references in a free-text memo: INV-25845, inv25867, 'Invoice 25937'."""
    if not isinstance(memo, str):
        return []
    out = []
    for m in re.finditer(r"(?:inv(?:oice)?[\s#:\-]*)?(\d{5})", memo, flags=re.I):
        out.append("INV-" + m.group(1))
    return list(dict.fromkeys(out))


def identify_customer(payer_name, customers):
    """Return (customer_id or None, confidence, reason, candidates). Exact normalised name first, then fuzzy."""
    n = norm_name(payer_name)
    exact = customers[customers["norm"] == n]
    if len(exact) == 1:
        r = exact.iloc[0]
        return r["customer_id"], 0.97, "Payer name matches customer '%s' exactly (ignoring case and punctuation)" % r["name"], [r["customer_id"]]
    toks = set(core_tokens(payer_name))
    scored = []
    for _, r in customers.iterrows():
        ct = set(core_tokens(r["name"]))
        if not ct or not toks:
            continue
        jacc = len(ct & toks) / float(len(ct | toks))
        ratio = difflib.SequenceMatcher(None, n, r["norm"]).ratio()
        s = 0.6 * jacc + 0.4 * ratio
        if s > 0.55:
            scored.append((s, r["customer_id"], r["name"]))
    scored.sort(reverse=True)
    if not scored:
        return None, 0.0, "No customer name resembles payer '%s'" % payer_name, []
    # QA (T+0:30): a single weak match (e.g. payer "JESSOP" -> "Jessop Legal" at 0.55) assigned the wrong customer.
    # Only accept a fuzzy match when it is strong AND clearly ahead; otherwise return the candidates and let the
    # amount decide (or a person).
    if scored[0][0] >= 0.75 and (len(scored) == 1 or scored[0][0] - scored[1][0] > 0.15):
        s, cid, name = scored[0]
        return cid, round(min(0.9, s), 2), "Payer name is closest to '%s' (similarity %.2f)" % (name, s), [c for _, c, _ in scored[:6]]
    names = ", ".join("%s (%.2f)" % (nm, s) for s, _, nm in scored[:6])
    return None, 0.3, "Payer name '%s' is not a clear match for any one customer: %s" % (payer_name, names), [c for _, c, _ in scored[:6]]


def run(d, rules):
    inv = d["invoices"]
    pay = d["payments"]
    cus = d["customers"]
    open_inv = inv[inv["status"].isin(OPEN_STATUSES)]
    by_id = inv.set_index("invoice_id")
    unapplied = pay[pay["invoice_id"].isna()].sort_values("received_date")
    tol = float(rules.get("amount_tolerance", 0) or 0)
    fee_tol = float(rules.get("fee_tolerance", 0) or 0)
    results, audit = [], []

    for _, p in unapplied.iterrows():
        amt = float(p["amount"])
        reasons = []
        alternatives = []
        decision, invoice_ids, conf = "EXCEPTION", [], 0.0
        cid, cconf, creason, cands = identify_customer(p["payer_name"], cus)
        reasons.append(creason)
        refs = [r for r in _refs_in_memo(p["memo"]) if r in by_id.index]
        if refs:
            reasons.append("Memo '%s' references %s" % (p["memo"], ", ".join(refs)))
            ref_cust = by_id.loc[refs[0], "customer_id"]
            if cid is None:
                cid, cconf = ref_cust, 0.9
                reasons.append("Customer taken from the referenced invoice")
            elif ref_cust != cid:
                reasons.append("WARNING: referenced invoice belongs to a different customer (%s)" % by_id.loc[refs[0], "customer_name"])
        elif isinstance(p["memo"], str) and p["memo"].strip():
            reasons.append("Memo '%s' has no invoice reference" % p["memo"])
        else:
            reasons.append("No memo on the receipt")

        if cid is None and cands:
            # Ambiguous payer: if exactly one candidate customer has an open invoice for exactly this amount, propose it.
            hit = open_inv[open_inv["customer_id"].isin(cands) & ((open_inv["amount"] - amt).abs() < 0.005)]
            if hit["customer_id"].nunique() == 1:
                cid, cconf = hit.iloc[0]["customer_id"], 0.6
                reasons.append("Only %s, among the possible customers, has an open invoice for exactly $%s" % (hit.iloc[0]["customer_name"], format(amt, ",.2f")))
        cand = open_inv[open_inv["customer_id"] == cid] if cid else open_inv.iloc[0:0]
        ref_open = [r for r in refs if r in set(cand["invoice_id"])]

        if ref_open:
            ref_total = float(by_id.loc[ref_open, "amount"].sum())
            diff = round(amt - ref_total, 2)
            cap = float(rules.get("auto_apply_max_amount", 10000) or 0)
            if abs(diff) <= 0.005 and rules.get("auto_apply_exact_ref_match", True) and cconf >= 0.8 and amt > cap:
                decision, invoice_ids, conf = "PROPOSE", ref_open, 0.95
                reasons.append("Exact amount and invoice reference, but $%s is above the $%s auto-apply limit: Priya confirms" % (format(amt, ",.2f"), format(cap, ",.0f")))
            elif abs(diff) <= 0.005 and rules.get("auto_apply_exact_ref_match", True) and cconf >= 0.8:
                decision, invoice_ids, conf = "AUTO_APPLY", ref_open, 0.99
                reasons.append("Amount $%.2f equals %s exactly and the memo names it: applied automatically under Dana's rule" % (amt, ", ".join(ref_open)))
            elif abs(diff) <= tol:
                decision, invoice_ids, conf = "PROPOSE", ref_open, 0.9
                reasons.append("Amount within tolerance of the referenced invoice (difference $%.2f)" % diff)
            elif 0 < -diff <= fee_tol:
                decision, invoice_ids, conf = "PROPOSE", ref_open, 0.8
                reasons.append("Short by $%.2f, which looks like a bank fee. Needs approval to write off (threshold $%.0f)" % (-diff, float(rules.get("writeoff_threshold", 0))))
            else:
                decision, invoice_ids, conf = "PROPOSE", ref_open, 0.6
                reasons.append("Memo names the invoice but the amount differs by $%.2f: partial or combined payment, needs Priya" % diff)
        elif len(cand):
            exact = cand[(cand["amount"] - amt).abs() <= max(tol, 0.005)]
            if len(exact) == 1:
                decision, invoice_ids, conf = "PROPOSE", [exact.iloc[0]["invoice_id"]], round(0.85 * max(cconf, 0.5), 2)
                if cconf < 0.8:
                    conf = round(min(conf, 0.5), 2)
                reasons.append("Exactly one open invoice for this customer has the same amount ($%.2f). No reference, so not applied automatically" % amt)
            elif len(exact) > 1:
                ex = exact.sort_values("due_date")
                decision, invoice_ids, conf = "PROPOSE", [ex.iloc[0]["invoice_id"]], 0.55
                alternatives = list(ex["invoice_id"].iloc[1:])
                reasons.append("%d open invoices have this amount (%s). Proposed the oldest. Whichever it is, the customer has paid one of them, so do not chase both" % (len(ex), ", ".join(ex["invoice_id"])))
            else:
                hit = None
                rows = list(cand.sort_values("due_date").itertuples())
                for k in (2, 3):
                    for combo in itertools.combinations(rows, k):
                        if abs(sum(r.amount for r in combo) - amt) <= max(tol, 0.005):
                            hit = combo
                            break
                    if hit:
                        break
                if hit:
                    decision, invoice_ids, conf = "PROPOSE", [r.invoice_id for r in hit], 0.6
                    reasons.append("Amount equals the sum of %s: probably one payment for several invoices" % ", ".join(invoice_ids))
                else:
                    reasons.append("No open invoice or combination matches $%.2f. Ask the customer which invoice this covers" % amt)
        elif cid is None:
            reasons.append("Cannot identify the customer. Priya should check the bank detail")

        matched = float(by_id.loc[invoice_ids, "amount"].sum()) if invoice_ids else 0.0
        cust_name = cus.set_index("customer_id").loc[cid, "name"] if cid else None
        results.append({
            "payment_id": p["payment_id"],
            "received_date": p["received_date"].strftime("%Y-%m-%d"),
            "amount": amt,
            "method": p["method"],
            "payer_name": p["payer_name"],
            "memo": p["memo"] if isinstance(p["memo"], str) else "",
            "customer_id": cid,
            "customer_name": cust_name,
            "candidates": cands,
            "decision": decision,
            "invoice_ids": list(invoice_ids),
            "alternatives": alternatives,
            "matched_amount": matched,
            "difference": round(amt - matched, 2) if invoice_ids else None,
            "confidence": conf,
            "reasons": reasons,
            "agent": AGENT,
        })
        audit.append({"agent": AGENT, "object_type": "payment", "object_id": p["payment_id"], "decision": decision,
                      "confidence": conf, "reason": reasons[-1]})
    return results, audit
