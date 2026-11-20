"""QA pass 2, section B: FIN-1 policy compliance on EVERY invoice of run_pipeline() (read-only)."""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from app.engine.data import AS_OF, domain_of, load, norm_name  # noqa: E402
from app.engine.pipeline import _am_email, run_pipeline  # noqa: E402
from app.engine.rules import DEFAULT_RULES  # noqa: E402

s = run_pipeline(dict(DEFAULT_RULES))
d = load()
cus = d["customers"].set_index("customer_id")
con = d["contacts"]
inv_book = d["invoices"].set_index("invoice_id")
RES = []


def check(name, bad, n):
    RES.append((name, "PASS" if not bad else "FAIL", n, len(bad), "; ".join(map(str, bad[:8]))))
    print("[%s] %s (%d checked, %d bad) %s" % ("PASS" if not bad else "FAIL", name, n, len(bad), "; ".join(map(str, bad[:8]))))


def expected_stage(true_dpd, ar_status):
    if ar_status == "payment_failed":
        return "card_failed"
    if true_dpd < -5:
        return "not_due"
    if true_dpd < 0:
        return "courtesy"
    if true_dpd < 7:
        return "wait"
    if true_dpd < 21:
        return "first"
    if true_dpd < 45:
        return "second"
    if true_dpd < 90:
        return "final"
    return "escalate"


invs = s["invoices"]
bad = []
for i in invs:
    true_dpd = (AS_OF - pd.Timestamp(i["due_date"])).days
    e = expected_stage(true_dpd, i["ar_status"])
    if e != i["stage"]:
        bad.append("%s due %s true_dpd=%d stage=%s expected=%s" % (i["invoice_id"], i["due_date"], true_dpd, i["stage"], e))
check("B1 stage matches policy (-5/+7/+21/+45/+90) using TRUE days past due", bad, len(invs))
bad = [i["invoice_id"] for i in invs if i["top50"] and i["action"] == "DRAFT_REMINDER"]
check("B2 top-50 never DRAFT_REMINDER", bad, sum(1 for i in invs if i["top50"]))
BLOCK = {"PAID", "MONEY_RECEIVED", "DISPUTE", "CANCELLATION", "LEGAL_RISK", "OPEN_ESCALATION"}
bad = ["%s %s" % (i["invoice_id"], sorted({h["code"] for h in i["holds"]} & BLOCK)) for i in invs if i["draft"] and {h["code"] for h in i["holds"]} & BLOCK]
check("B3 no draft where PAID/MONEY_RECEIVED/DISPUTE/CANCELLATION/LEGAL_RISK/OPEN_ESCALATION", bad, len(invs))

drafts = [i for i in invs if i["draft"]]
print("drafts: %d total (%d DRAFT_REMINDER, %d HUMAN_WRITES)" % (len(drafts), sum(i["action"] == "DRAFT_REMINDER" for i in drafts), sum(i["action"] == "HUMAN_WRITES" for i in drafts)))
banned = [p.lower() for p in DEFAULT_RULES["banned_phrases"]]
b4, b5, b6, b7, b8, b9 = [], [], [], [], [], []
for i in drafts:
    dr = i["draft"]
    text = (dr["subject"] + "\n" + dr["body"]).lower()
    hit = [p for p in banned if p in text]
    if hit:
        b4.append((i["invoice_id"], hit))
    c = cus.loc[i["customer_id"]]
    for e in dr["to"]:
        row = con[(con["email"].str.lower() == e.lower()) & (con["customer_id"] == i["customer_id"])]
        if not len(row):
            b5.append((i["invoice_id"], e, "not in contacts.csv for this customer"))
            continue
        row = row.iloc[0]
        if domain_of(e) != c["domain"]:
            b5.append((i["invoice_id"], e, "domain"))
        if row["status"] != "active":
            b6.append((i["invoice_id"], e, row["status"]))
        if not any(k in row["role"].lower() for k in ("billing", "admin")):
            b5.append((i["invoice_id"], e, "role " + row["role"]))
    am = _am_email(c["account_manager"])
    if am not in dr.get("cc", []):
        b7.append((i["invoice_id"], dr.get("cc")))
    amt = "$" + format(i["amount"], ",.2f")
    for need in (i["invoice_id"], amt):
        if need not in dr["body"]:
            b8.append((i["invoice_id"], "missing " + need))
    if dr["template"] != "courtesy" and i["stage"] != "card_failed" and str(i["due_date"])[:10] not in dr["body"]:
        b8.append((i["invoice_id"], "missing due date"))
    # ledger cross-check: amount/due in draft = invoices.csv
    b = inv_book.loc[i["invoice_id"]]
    if abs(float(b["amount"]) - i["amount"]) > 0.005 or str(b["due_date"])[:10] != str(i["due_date"])[:10]:
        b8.append((i["invoice_id"], "ledger mismatch"))
    if "Priya Nair" not in dr["body"].strip().splitlines()[-2:][0] + dr["body"].strip().splitlines()[-1]:
        b9.append(i["invoice_id"])
check("B4 drafts contain no banned phrase", b4, len(drafts))
check("B5 recipients are verified contacts (in contacts.csv, domain match, billing/admin role)", b5, len(drafts))
check("B6 never a 'left the firm' contact", b6, len(drafts))
check("B7 account manager cc'd", b7, len(drafts))
check("B8 invoice id / amount / due date in body and equal to the ledger", b8, len(drafts))
check("B9 signed off by Priya", b9, len(drafts))
# false-positive blocks from substring banned phrases (e.g. 'court' inside 'courtesy')
fp = [(i["invoice_id"], h["detail"]) for i in invs for h in i["holds"] if h["code"] == "BANNED_LANGUAGE"]
check("B4b no draft blocked by banned list at baseline (substring false positives)", fp, len(invs))

pays = d["payments"]
b10 = []
for i in invs:
    codes = {h["code"] for h in i["holds"]}
    if i["action"] == "RETRY_CARD":
        later = pays[(pays["method"] == "card") & (pays["payer_name"].map(norm_name) == norm_name(i["customer_name"])) & (pays["received_date"] > pd.Timestamp(i["issue_date"]))]
        if not len(later):
            b10.append((i["invoice_id"], "no later card charge"))
        if codes & {"MONEY_RECEIVED", "DISPUTE", "CANCELLATION", "OPEN_ESCALATION", "NO_VALID_CONTACT", "LEGAL_RISK"}:
            b10.append((i["invoice_id"], sorted(codes)))
        if i["draft"]:
            b10.append((i["invoice_id"], "draft attached"))
check("B10 card re-runs only with a later successful card charge and no hard hold / legal risk", b10, sum(i["action"] == "RETRY_CARD" for i in invs))
b11 = []
for i in invs:
    dana = any(str(h.get("route_to", "")).startswith("Dana") for h in i["holds"])
    should = i["ar_status"] == "payment_failed" and (150 - i["days_past_due"] <= 10 or i["amount"] > 2000)
    if dana != should:
        b11.append((i["invoice_id"], i["customer_name"], i["amount"], i["days_past_due"], "dana=%s expected=%s" % (dana, should)))
check("B11 Dana decisions = card invoices <=10 days from 150-day write-off or > $2,000", b11, len(invs))
print("Dana list:", [(i["invoice_id"], i["customer_name"], i["amount"], i["days_past_due"]) for i in invs if any(str(h.get("route_to", "")).startswith("Dana") for h in i["holds"])])
true_neg = [(i["invoice_id"], i["customer_name"], (AS_OF - pd.Timestamp(i["due_date"])).days, i["stage"], i["action"]) for i in invs if -5 <= (AS_OF - pd.Timestamp(i["due_date"])).days < 0]
print("Invoices due in the next 1-5 days (policy: courtesy note):", true_neg)
pd.DataFrame(RES, columns=["check", "result", "n", "bad", "examples"]).to_csv(os.path.join(ROOT, "analysis", "work", "eval_policy_results.csv"), index=False)
