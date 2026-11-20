"""QA: Controller dispute detection vs the analyst's list, and heuristic_read over all 1,041 tickets (read-only)."""
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from app.engine.context import heuristic_read  # noqa: E402
from app.engine.data import load  # noqa: E402
from app.engine.pipeline import run_pipeline  # noqa: E402

s = run_pipeline()
inv = s["invoices"]
overdue = [i for i in inv if i["days_past_due"] > 0]
ref = pd.read_csv(os.path.join(ROOT, "analysis", "work", "tickets_invoice_refs.csv"))
truth = set(ref["invoice_id"])
DISPUTE_CODES = {"DISPUTE", "CANCELLATION", "LEGAL_RISK"}
pred = {i["invoice_id"] for i in overdue if any(h["code"] in DISPUTE_CODES for h in i["holds"])}
pred_d = {i["invoice_id"] for i in overdue if any(h["code"] == "DISPUTE" for h in i["holds"])}
tp, fp, fn = truth & pred, pred - truth, truth - pred
print("Analyst disputed overdue invoices:", len(truth), "Pipeline flagged (DISPUTE/CANCEL/LEGAL):", len(pred))
print("TP", len(tp), "FP", sorted(fp), "FN", sorted(fn))
print("precision %.1f%% recall %.1f%%" % (100 * len(tp) / max(1, len(pred)), 100 * len(tp) / len(truth)))
print("DISPUTE code only: pred", len(pred_d), "TP", len(truth & pred_d), "FP", sorted(pred_d - truth), "FN", sorted(truth - pred_d))
not_held = [i for i in overdue if i["invoice_id"] in truth and i["action"] not in ("HOLD",)]
print("Analyst-disputed invoices NOT in HOLD:", [(i["invoice_id"], i["action"]) for i in not_held])
for i in overdue:
    if i["invoice_id"] in fp:
        print("FP detail:", i["invoice_id"], i["customer_name"], i["amount"], i["action"], [(h["code"], h["detail"][:200]) for h in i["holds"] if h["code"] in DISPUTE_CODES])

# heuristic_read over ALL tickets, own invoices = the customer's invoices open today (as the pipeline does)
d = load()
oi = d["invoices"][d["invoices"]["status"].isin(("open", "overdue", "payment_failed"))]
own = oi.groupby("customer_id")["invoice_id"].apply(list).to_dict()
rows = []
for _, t in d["tickets"].iterrows():
    td = t.to_dict()
    r = heuristic_read(td, own.get(t["customer_id"], []))
    rows.append({"ticket_id": t["ticket_id"], "created_at": t["created_at"], "customer_id": t["customer_id"], "customer_name": t["customer_name"],
                 "category": t["category"], "priority": t["priority"], "status": t["status"],
                 "about": r["about_ledgerline_invoice"], "kind": r["kind"], "invoice_ids": "|".join(r["invoice_ids"]),
                 "refuses": r["refuses_to_pay_until_fixed"], "complaint_kw": r["collections_complaint"], "signals": "|".join(r["signals"]),
                 "subject": t["subject"], "body": str(t["body"])})
tr = pd.DataFrame(rows)
tr.to_csv(os.path.join(ROOT, "analysis", "work", "eval_ticket_reads.csv"), index=False)
print("\nAll tickets:", len(tr), "flagged about_ledgerline_invoice:", int(tr.about.sum()))
print(tr[tr.about].kind.value_counts().to_string())
print("complaint keyword (agent field) total:", int(tr.complaint_kw.sum()), "of which about Ledgerline invoice:", int((tr.complaint_kw & tr.about).sum()))
flag = tr[tr.about]
samp_f = flag.sample(min(30, len(flag)), random_state=7)
money = tr[~tr.about & tr.body.str.contains(r"invoice|charge|bill|refund|pay|fee|credit", case=False, regex=True)]
samp_n = money.sample(30, random_state=7)
print("not flagged but money words:", len(money), "of", int((~tr.about).sum()))
samp_f.assign(sample="flagged").to_csv(os.path.join(ROOT, "analysis", "work", "eval_ticket_sample_flagged.csv"), index=False)
samp_n.assign(sample="not_flagged_money_words").to_csv(os.path.join(ROOT, "analysis", "work", "eval_ticket_sample_notflagged.csv"), index=False)
