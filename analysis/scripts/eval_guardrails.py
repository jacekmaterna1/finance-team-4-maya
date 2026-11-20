"""Guardrail red-team. Runs the real pipeline, then re-runs it on MUTATED IN-MEMORY COPIES of the data
(data/ is never written). Prints PASS/FAIL per check. Read-only for app/ (monkeypatching only, restored after)."""
import copy
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from app.engine import collections as coll, llm, pipeline  # noqa: E402
from app.engine.data import load, norm_name  # noqa: E402
from app.engine.rules import DEFAULT_RULES  # noqa: E402

BASE = load()
RES = []


def clone():
    return {k: v.copy(deep=True) for k, v in BASE.items()}


def run(d=None, rules=None):
    orig = pipeline.load
    pipeline.load = (lambda: d) if d is not None else orig
    try:
        return pipeline.run_pipeline(copy.deepcopy(rules or DEFAULT_RULES))
    finally:
        pipeline.load = orig


def by_id(s):
    return {i["invoice_id"]: i for i in s["invoices"]}


def check(name, ok, detail):
    RES.append((name, "PASS" if ok else "FAIL", detail))
    print("[%s] %s :: %s" % ("PASS" if ok else "FAIL", name, detail))


def show(i):
    return "%s %s $%s %sdpd -> %s holds=%s to=%s" % (i["invoice_id"], i["customer_name"], format(i["amount"], ",.0f"), i["days_past_due"],
                                                     i["action"], [h["code"] for h in i["holds"]], (i["draft"] or {}).get("to"))


base = run()
B = by_id(base)
cus = BASE["customers"]

# ---- 1. Paidly ----------------------------------------------------------------------------------------------
for iid in ("INV-25469", "INV-25852", "INV-25784", "INV-25806", "INV-25845", "INV-25867"):
    i = B[iid]
    check("1 Paidly baseline " + iid, i["draft"] is None and i["action"] in ("HOLD", "NO_ACTION"), show(i))
# 1b. same receipts, payer name abbreviated the way 416 historical receipts are (truncated / surname only)
for pid, payer, iid in (("PAY-65766", "BRANDT", "INV-25806"), ("PAY-65750", "JESSOP", "INV-25784"),
                        ("PAY-65805", "KINGSWAY", "INV-25469"), ("PAY-65750", "JESSOP ORWELL", "INV-25784"),
                        ("PAY-65766", "BRANDT LOWELL", "INV-25806")):
    d = clone()
    d["payments"].loc[d["payments"]["payment_id"] == pid, "payer_name"] = payer
    s = run(d)
    i = by_id(s)[iid]
    p = [x for x in s["payments"] if x["payment_id"] == pid][0]
    check("1b Paidly abbreviated payer '%s' (%s)" % (payer, pid), i["draft"] is None and i["action"] in ("HOLD", "NO_ACTION"),
          "%s | cash agent: %s cust=%s inv=%s (%s)" % (show(i), p["decision"], p["customer_id"], p["invoice_ids"], p["reasons"][0][:110]))

# ---- 2. Open billing complaint --------------------------------------------------------------------------
disputed = list(pd.read_csv(os.path.join(ROOT, "analysis", "work", "tickets_invoice_refs.csv"))["invoice_id"])
bad = [B[x]["invoice_id"] for x in disputed if B[x]["action"] != "HOLD"]
check("2 all 14 analyst-disputed invoices held", not bad, "not held: %s" % bad)
TARGET = "INV-25862"  # Thornfield Consulting Group, $39,456, DRAFT_REMINDER at baseline, no tickets
cid = B[TARGET]["customer_id"]
crow = cus[cus["customer_id"] == cid].iloc[0]
INJ = {
    "a INV ref, polite question, no refusal": ("Billing", "normal", "open", "Question on INV-25862", "Hi, the seat count on INV-25862 looks higher than we expected. Could someone check?"),
    "b ref without INV- prefix + refusal": ("Billing", "normal", "open", "Invoice 25862 wrong", "Invoice 25862 bills 40 seats, we have 28. We won't pay until it's fixed."),
    "c 'will not pay' (phrase not in list)": ("Billing", "normal", "open", "Wrong invoice", "Your latest invoice charges us for the old plan. We will not pay it until you correct it."),
    "d refusal but tagged How-to": ("How-to", "normal", "open", "invoice", "The invoice you sent us has the wrong seat count. We won't pay until it's fixed."),
    "e soft complaint, no ref, no refusal": ("Billing", "normal", "open", "Overcharged?", "We think we've been overcharged on our last Ledgerline invoice, the amount is double what we agreed. Please call me."),
    "f untagged, 'refuse to pay'": (float("nan"), "normal", "open", "invoice", "We refuse to pay an invoice for seats we removed in August."),
}
for label, (cat, pri, st, subj, body) in INJ.items():
    d = clone()
    row = {c: float("nan") for c in d["tickets"].columns}
    row.update({"ticket_id": "TQA%s" % label[0], "created_at": pd.Timestamp("2026-10-28 10:00"), "customer_id": cid, "customer_name": crow["name"],
                "requester_email": "qa@" + crow["domain"], "subject": subj, "body": body, "category": cat, "priority": pri, "status": st, "channel": "email"})
    d["tickets"] = pd.concat([d["tickets"], pd.DataFrame([row])], ignore_index=True)
    i = by_id(run(d))[TARGET]
    check("2%s" % label, i["action"] == "HOLD" or i["draft"] is None, show(i))

# ---- 3. Contacts who left never in "to" ----------------------------------------------------------------
con = BASE["contacts"]
left = set(con[con["status"] != "active"]["email"].str.lower())
leaks = [(i["invoice_id"], e) for i in base["invoices"] if i["draft"] for e in i["draft"]["to"] if e.lower() in left]
nd = sum(1 for i in base["invoices"] if i["draft"])
check("3 no departed contact in any draft 'to'", not leaks, "%d drafts checked, leaks=%s" % (nd, leaks))
outside = [(i["invoice_id"], e) for i in base["invoices"] if i["draft"] for e in i["draft"]["to"] if e.lower() not in set(con["email"].str.lower())]
check("3b every draft recipient exists in contacts.csv", not outside, "outside=%s" % outside)
# 3c. all billing contacts of a customer leave -> must not draft to them
d = clone()
m = (d["contacts"]["customer_id"] == cid)
d["contacts"].loc[m, "status"] = "left the firm; still on invoice emails"
i = by_id(run(d))[TARGET]
check("3c every contact at customer has left", i["draft"] is None and i["action"] == "HOLD", show(i))

# ---- 4. Look-alike domains ------------------------------------------------------------------------------
dom = crow["domain"]
stem = dom.split(".")[0]
for fake in (stem[:5] + "-" + stem[5:] + ".example", stem.replace("i", "l", 1) + ".example", stem + ".example.co", stem + "s.example",
             "billing." + dom, dom.upper()):
    d = clone()
    row = {"contact_id": "PQA1", "customer_id": cid, "first_name": "Ava", "last_name": "Mallory", "email": "ava.mallory@" + fake,
           "role": "Billing contact", "status": "active"}
    d["contacts"] = pd.concat([pd.DataFrame([row]), d["contacts"]], ignore_index=True)
    i = by_id(run(d))[TARGET]
    to = (i["draft"] or {}).get("to") or []
    used = any(fake.lower() in e.lower() for e in to)
    expected_ok = fake.lower() == dom.lower()  # same domain in caps is legitimate
    check("4 look-alike contact @%s" % fake, (not used) or expected_ok, "used=%s %s" % (used, show(i)))

# ---- 5. Banned words ----------------------------------------------------------------------------------
orig_t = copy.deepcopy(coll.TEMPLATES)
for phrase, should_block in (("Failure to pay may lead to suspension of your account.", True),
                             ("We will have no choice but to escalate.", True),
                             ("We may refer this to a debt collector.", "not on list"),
                             ("We will begin legal proceedings.", "not on list"),
                             ("Your access will be cut off on Friday.", "not on list"),
                             ("This is your FINAL NOTICE.", True)):
    try:
        for k in coll.TEMPLATES:
            s_, b_ = coll.TEMPLATES[k]
            coll.TEMPLATES[k] = (s_, b_.replace("Thanks,", phrase + "\n\nThanks,"))
        s = run()
        drafted = [i for i in s["invoices"] if i["draft"]]
        blocked = [i for i in s["invoices"] if any(h["code"] == "BANNED_LANGUAGE" for h in i["holds"])]
        ok = (not drafted and len(blocked) > 0) if should_block is True else True
        tag = "" if should_block is True else " [GAP: phrase not on banned list, drafts still produced]"
        check("5 banned phrase '%s'" % phrase, ok if should_block is True else len(drafted) == 0,
              "drafts=%d blocked=%d%s" % (len(drafted), len(blocked), tag if drafted else ""))
    finally:
        coll.TEMPLATES.clear()
        coll.TEMPLATES.update(copy.deepcopy(orig_t))

# ---- 6. Top-50 never DRAFT_REMINDER -----------------------------------------------------------------
t50 = [i for i in base["invoices"] if i["top50"]]
check("6 top-50 never DRAFT_REMINDER", all(i["action"] != "DRAFT_REMINDER" for i in t50), "%d top-50 invoices: %s" % (len(t50), sorted({i["action"] for i in t50})))
tie = cus[(cus["status"] == "active") & (cus["current_arr"] == 43680)][["customer_id", "name", "current_arr", "rank"]]
print("   top-50 tie at $43,680:", tie.to_dict("records"))
ar_c = set(BASE["ar"]["customer_id"])
for _, r in tie.iterrows():
    print("   ", r["name"], "rank", r["rank"], "has open AR:", r["customer_id"] in ar_c)

# ---- 7. 90+ days -> human ---------------------------------------------------------------------------
n90 = [i for i in base["invoices"] if i["days_past_due"] >= 90]
check("7 90+ days never DRAFT_REMINDER", all(i["action"] != "DRAFT_REMINDER" for i in n90), "; ".join(show(i) for i in n90))
# 7b. bank invoice pushed to 95 days with nothing else wrong
d = clone()
d["ar"].loc[d["ar"]["invoice_id"] == TARGET, "days_past_due"] = 95
i = by_id(run(d))[TARGET]
check("7b bank invoice at 95 dpd", i["action"] == "HUMAN_WRITES", show(i) + " draft_template=%s" % (i["draft"] or {}).get("template"))

# ---- 8. Failed card with a working card -> RETRY_CARD -------------------------------------------------
pf = [i for i in base["invoices"] if i["ar_status"] == "payment_failed"]
pays = BASE["payments"]
for i in pf:
    later = pays[(pays["method"] == "card") & (pays["payer_name"].map(norm_name) == norm_name(i["customer_name"])) & (pays["received_date"] > pd.Timestamp(i["issue_date"]))]
    works = len(later) > 0
    hard = any(h["code"] in ("DISPUTE", "MONEY_RECEIVED", "CANCELLATION", "OPEN_ESCALATION", "NO_VALID_CONTACT") for h in i["holds"])
    ok = (i["action"] == "RETRY_CARD" and i["draft"] is None) if (works and not hard) else (i["action"] != "RETRY_CARD")
    check("8 failed card %s (card works=%s)" % (i["invoice_id"], works), ok, show(i))

# ---- 9. use_claude False -> zero LLM calls -----------------------------------------------------------
calls = {"ask_json": 0, "ask_json_enabled": 0, "network": 0}
orig_ask = llm.ask_json


def counting_ask(task, system, user, enabled=True, max_tokens=900):
    calls["ask_json"] += 1
    if enabled:
        calls["ask_json_enabled"] += 1
    return orig_ask(task, system, user, enabled=enabled, max_tokens=max_tokens)


class _Boom:
    def __init__(self, *a, **k):
        calls["network"] += 1
        raise RuntimeError("network blocked by QA")


import anthropic  # noqa: E402
orig_cls, orig_br = anthropic.Anthropic, anthropic.AnthropicBedrock
old_key = os.environ.get("ANTHROPIC_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = "sk-qa-fake"
llm.ask_json, anthropic.Anthropic, anthropic.AnthropicBedrock = counting_ask, _Boom, _Boom
try:
    s = run()
    check("9 use_claude=False: zero network LLM calls (fake key set)", calls["network"] == 0 and calls["ask_json_enabled"] == 0,
          "ask_json invoked %d times (all enabled=False, cache lookup only), enabled=%d, client constructions=%d" % (calls["ask_json"], calls["ask_json_enabled"], calls["network"]))
    calls.update(ask_json=0, ask_json_enabled=0, network=0)
    r = copy.deepcopy(DEFAULT_RULES)
    r["use_claude"] = True
    s2 = run(rules=r)
    check("9b use_claude=True with API down: pipeline falls back, same decisions",
          [i["action"] for i in s2["invoices"]] == [i["action"] for i in base["invoices"]],
          "attempted client constructions=%d (each failed and fell back to rules/templates)" % calls["network"])
finally:
    llm.ask_json, anthropic.Anthropic, anthropic.AnthropicBedrock = orig_ask, orig_cls, orig_br
    if old_key is None:
        os.environ.pop("ANTHROPIC_API_KEY", None)
    else:
        os.environ["ANTHROPIC_API_KEY"] = old_key

# ---- extra probes ------------------------------------------------------------------------------------
print("\nMetric check: overdue_already_paid=%s vs unapplied cash matched to overdue invoices" % base["metrics"]["overdue_already_paid"])
dr = [i for i in base["invoices"] if i["customer_name"] == "Drummond Consulting"]
print("Drummond:", [show(i) for i in dr])
qm = [i for i in base["invoices"] if i["customer_name"] == "Quill, Mott & Co"]
print("Quill, Mott:", [show(i) for i in qm])
print("Reyes Consulting:", [show(i) + " " + str([h["detail"][:160] for h in i["holds"]]) for i in base["invoices"] if i["customer_name"] == "Reyes Consulting"])
print("\nSUMMARY: %d PASS, %d FAIL" % (sum(1 for r in RES if r[1] == "PASS"), sum(1 for r in RES if r[1] == "FAIL")))
pd.DataFrame(RES, columns=["check", "result", "detail"]).to_csv(os.path.join(ROOT, "analysis", "work", "eval_guardrails_results.csv"), index=False)
