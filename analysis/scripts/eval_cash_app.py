"""QA harness for the Cash Application agent (read-only; does not modify app/ or data/).

For every row of analysis/testset_cash_app.csv the payment is simulated as UNAPPLIED against the invoice book as it
stood on its received_date (open = issue_date <= received_date and (paid_date blank or paid_date >= received_date)).
The real app.engine.cash_app.run() is then called unchanged on that one-payment world, so the decision rules are
exactly the production ones. Output: analysis/work/eval_cash_app_results.csv + printed summary.
"""
import copy
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from app.engine import cash_app  # noqa: E402
from app.engine.data import load  # noqa: E402
from app.engine.rules import DEFAULT_RULES  # noqa: E402

d0 = load()
rules = copy.deepcopy(DEFAULT_RULES)
inv_all = d0["invoices"].copy()
inv_all["paid_date_ts"] = pd.to_datetime(inv_all["paid_date"])
ts = pd.read_csv(os.path.join(ROOT, "analysis", "testset_cash_app.csv"))
ts["received_date"] = pd.to_datetime(ts["received_date"])

_book = {}


def book_as_of(day):
    if day not in _book:
        inv = inv_all.copy()
        is_open = (inv["issue_date"] <= day) & (inv["paid_date_ts"].isna() | (inv["paid_date_ts"] >= day))
        inv["status"] = is_open.map({True: "open", False: "paid"})
        _book[day] = inv.drop(columns=["paid_date_ts"])
    return _book[day]


rows = []
for _, t in ts.iterrows():
    pay = pd.DataFrame([{"payment_id": t["payment_id"], "received_date": t["received_date"], "amount": float(t["amount"]),
                         "method": t["method"], "payer_name": t["payer_name"],
                         "memo": t["memo"] if isinstance(t["memo"], str) else float("nan"),
                         "applied_date": float("nan"), "invoice_id": float("nan")}])
    d = dict(d0, invoices=book_as_of(t["received_date"]), payments=pay)
    res, _ = cash_app.run(d, rules)
    r = res[0]
    truth = set(t["true_invoice_ids"].split("|"))
    ambiguous = "AMBIGUOUS" in str(t["label_source"])
    pred = set(r["invoice_ids"])
    if ambiguous:
        correct = len(pred) == 1 and pred <= truth
    else:
        correct = pred == truth
    true_cust = inv_all.set_index("invoice_id").loc[sorted(truth)[0], "customer_id"]
    syn_type = ""
    if t["is_synthetic"]:
        reason = str(t["difficulty_reason"])
        syn_type = ("bank_fee" if "bank fee" in reason else "rounding" if "rounding" in reason else
                    "short_pay" if "short" in reason else "combined" if "two invoices" in reason else "other")
    rows.append({"payment_id": t["payment_id"], "is_synthetic": bool(t["is_synthetic"]), "difficulty": t["difficulty"],
                 "syn_type": syn_type, "payer_name": t["payer_name"], "memo": t["memo"], "amount": t["amount"],
                 "truth": "|".join(sorted(truth)), "ambiguous_label": ambiguous,
                 "decision": r["decision"], "pred": "|".join(r["invoice_ids"]), "alternatives": "|".join(r["alternatives"]),
                 "confidence": r["confidence"], "correct": correct,
                 "truth_in_pred_or_alt": bool(truth & (pred | set(r["alternatives"]))),
                 "pred_customer": r["customer_id"], "true_customer": true_cust, "customer_correct": r["customer_id"] == true_cust,
                 "last_reason": r["reasons"][-1], "all_reasons": " || ".join(r["reasons"])})

out = pd.DataFrame(rows)
os.makedirs(os.path.join(ROOT, "analysis", "work"), exist_ok=True)
out.to_csv(os.path.join(ROOT, "analysis", "work", "eval_cash_app_results.csv"), index=False)


def summ(df, label):
    n = len(df)
    if not n:
        return
    aa = df[df.decision == "AUTO_APPLY"]
    pr = df[df.decision == "PROPOSE"]
    ex = df[df.decision == "EXCEPTION"]
    print("%-28s n=%3d | auto %3d (prec %s) | propose %3d (top1 %s) | exception %3d (%.0f%%) | end-to-end correct %.1f%% | customer correct %.1f%%" % (
        label, n, len(aa), "%.1f%%" % (100 * aa.correct.mean()) if len(aa) else "n/a", len(pr),
        "%.1f%%" % (100 * pr.correct.mean()) if len(pr) else "n/a", len(ex), 100.0 * len(ex) / n,
        100 * df.correct.mean(), 100 * df.customer_correct.mean()))


print("=== REAL ===")
real = out[~out.is_synthetic]
summ(real, "real: all")
for k in ("trivial", "easy", "medium", "hard"):
    summ(real[real.difficulty == k], "real: " + k)
print("=== SYNTHETIC ===")
syn = out[out.is_synthetic]
summ(syn, "synthetic: all")
for k in ("bank_fee", "rounding", "short_pay", "combined"):
    summ(syn[syn.syn_type == k], "synthetic: " + k)
print("\nWrong AUTO_APPLY rows:")
print(out[(out.decision == "AUTO_APPLY") & ~out.correct].to_string())
print("\nWrong PROPOSE rows (real):")
w = out[(out.decision == "PROPOSE") & ~out.correct]
print(w[["payment_id", "is_synthetic", "difficulty", "syn_type", "payer_name", "memo", "amount", "truth", "pred", "alternatives", "customer_correct", "last_reason"]].to_string())
print("\nEXCEPTIONS:")
e = out[out.decision == "EXCEPTION"]
print(e[["payment_id", "is_synthetic", "difficulty", "syn_type", "payer_name", "memo", "amount", "truth", "pred_customer", "true_customer", "last_reason"]].to_string())
