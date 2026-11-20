"""QA pass 2, sections C (consistency) and D (human-action flows) via FastAPI TestClient.
Uses a throw-away DB, rules file and manuals copy so ./ledgerline.db, ./rules.json and app/engine/manuals are untouched.
Usage: eval_web.py <tmpdir>"""
import json
import os
import re
import shutil
import sys
import time

TMP = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for f in ("l.db", "rules.json"):
    if os.path.exists(os.path.join(TMP, f)):
        os.remove(os.path.join(TMP, f))
shutil.rmtree(os.path.join(TMP, "manuals"), ignore_errors=True)
shutil.copytree(os.path.join(ROOT, "app", "engine", "manuals"), os.path.join(TMP, "manuals"))
os.environ.update(DB_PATH=os.path.join(TMP, "l.db"), RULES_PATH=os.path.join(TMP, "rules.json"), MANUALS_DIR=os.path.join(TMP, "manuals"))
os.environ.pop("GOOGLE_CLIENT_ID", None)
sys.path.insert(0, ROOT)
from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402
from app import store  # noqa: E402
from app.engine.pipeline import run_pipeline  # noqa: E402

c = TestClient(app)
RES = []


def check(sec, name, ok, detail=""):
    RES.append((sec, name, "PASS" if ok else "FAIL", str(detail)[:300]))
    print("[%s] %s %s :: %s" % ("PASS" if ok else "FAIL", sec, name, str(detail)[:300]))


def text(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).replace("&amp;", "&").replace("&#39;", "'")


# ------------------------------------------------------------------ C. consistency
m = run_pipeline()["metrics"]
money = lambda v: "$" + format(v, ",.0f")
need = {"overdue": money(m["overdue_balance"]), "received": money(m["overdue_already_paid"]), "disputed": money(m["overdue_disputed"]),
        "collectable": money(m["overdue_collectable"])}
counts = {"drafts": m["drafts"], "held": m["held"], "card": m["card_retries"], "human": m["human_writes"]}
print("engine metrics:", need, counts)
pages = {"home": "/", "today": "/today", "digest": "/digest", "team": "/team"}
T = {k: text(c.get(v).text) for k, v in pages.items()}
r = c.post("/api/chat", json={"message": "status"})
T["chat status"] = r.json()["reply"] + " " + " ".join(" ".join(x.get("lines") or []) for x in r.json().get("cards", []))
for k, t in T.items():
    missing = [n + "=" + v for n, v in need.items() if v not in t and k not in ("team",)]
    check("C", "money figures on %s" % k, not missing, "missing " + ", ".join(missing) if missing else "all 4 present")
coll = c.get("/collections").text
groups = dict((a, int(n)) for a, n in re.findall(r'href="#g-([A-Z_]+)">[^(]*\((\d+)\)', coll))
check("C", "/collections group counts = engine", groups.get("HOLD") == counts["held"] and groups.get("DRAFT_REMINDER") == counts["drafts"]
      and groups.get("RETRY_CARD") == counts["card"] and groups.get("HUMAN_WRITES") == counts["human"], groups)
dg = T["digest"]
check("C", "digest counts = engine", ("drafted for your approval: %d" % counts["drafts"]) in dg and ("Card re-runs to approve: %d" % counts["card"]) in dg
      and ("Held (not chased): %d" % counts["held"]) in dg and ("write personally: %d" % counts["human"]) in dg, "")
cs = T["chat status"]
check("C", "chat status counts = engine", all(str(v) in cs for v in counts.values()), cs[:300])
for k in ("home", "today"):
    t = T[k]
    nh = re.search(r"(?:Needs a human today|Needs you today) \((\d+)", t)
    check("C", "needs-a-human count on %s" % k, nh is not None and int(nh.group(1)) == counts["held"] + counts["drafts"] + counts["card"] + counts["human"] + m["needs_review"],
          nh.group(0) if nh else "not found")
stale = ["$83,448", "$312,264", "$237,533", "$83k", "$238k", "22 wrong chases", "27 reminders", "11 that need a person"]
for k, path in list(pages.items()) + [("about", "/about"), ("docs", "/docs"), ("architecture", "/architecture"), ("demo", "/demo")]:
    t = text(c.get(path).text)
    hit = [s for s in stale if s in t]
    check("C", "no stale numbers on %s" % k, not hit, hit)

# ------------------------------------------------------------------ D. human-action flows
def status(r):
    return r.status_code


H = {"HX-Request": "true"}
n0 = len(store.all_actions())
check("D", "approve payment proposal PAY-65750", status(c.post("/cash/PAY-65750/approve", data={"note": "QA: confirmed Jessop wire"}, headers=H)) == 200)
check("D", "undo auto-apply PAY-65806", status(c.post("/cash/PAY-65806/undo", data={"note": "QA: undo test"}, headers=H)) == 200)
st_ = run_pipeline()
inv = {i["invoice_id"]: i for i in st_["invoices"]}
d = inv["INV-25862"]["draft"]
r = c.post("/collections/INV-25862/send", data={"subject": d["subject"], "body": d["body"] + "\n\nP.S. QA edit", "note": "QA: approve with edit"}, headers=H)
acts = [a for a in store.all_actions() if a["object_id"] == "INV-25862"]
check("D", "approve draft with an edit -> 'edit' + 'send' rows", status(r) == 200 and [a["action"] for a in acts] == ["edit", "send"], [a["action"] for a in acts])
r = c.post("/collections/INV-25869/send", data={"subject": "x", "body": "We will pass this to a debt collector."}, headers=H)
check("D", "send with banned wording -> 400", status(r) == 400, r.text[:120])
d2 = inv["INV-25848"]["draft"]
r = c.post("/collections/INV-25848/send", data={"subject": d2["subject"], "body": d2["body"], "to": "ap@okaforlegal-billing.example"}, headers=H)
check("D", "send to an address NOT in contacts.csv (look-alike) -> rejected", status(r) == 400, "HTTP %d (server accepted 'to' override)" % status(r))
r = c.post("/collections/INV-25784/send", data={"subject": "Invoice INV-25784", "body": "Please pay INV-25784."}, headers=H)
check("D", "send on a HOLD invoice (Jessop MONEY_RECEIVED) without lifting the hold -> rejected", status(r) == 400, "HTTP %d" % status(r))
check("D", "reject draft INV-25869", status(c.post("/collections/INV-25869/reject", data={"note": "QA: reject"}, headers=H)) == 200)
check("D", "override hold with reason <5 chars -> 400", status(c.post("/collections/INV-25897/hold", data={"reason": "ok", "kind": "override_hold"}, headers=H)) == 400)
check("D", "override hold with a reason -> OK", status(c.post("/collections/INV-25897/hold", data={"reason": "QA: AM says courtesy note is fine", "kind": "override_hold"}, headers=H)) == 200)
check("D", "release DISPUTE without AM checkbox -> 400", status(c.post("/collections/INV-25787/hold", data={"reason": "QA: settled", "kind": "release_hold"}, headers=H)) == 400)
check("D", "release DISPUTE with AM checkbox + name -> OK", status(c.post("/collections/INV-25787/hold", data={"reason": "QA: AM confirmed credit note", "kind": "release_hold", "am_confirmed": "on", "am_name": "Nadia Upton"}, headers=H)) == 200)
r = c.post("/collections/INV-25765/hold", data={"reason": "QA: just chase them", "kind": "override_hold"}, headers=H)
check("D", "OVERRIDE (not release) a DISPUTE hold without AM -> should also need AM", status(r) == 400, "HTTP %d: dispute hold lifted with no AM confirmation" % status(r))
check("D", "approve card re-run INV-25803", status(c.post("/collections/INV-25803/card_retry", data={"decision": "approve"}, headers=H)) == 200)
check("D", "reject card re-run INV-25793", status(c.post("/collections/INV-25793/card_retry", data={"decision": "reject", "note": "QA"}, headers=H)) == 200)
check("D", "card re-run on a non-re-run invoice -> 400", status(c.post("/collections/INV-25862/card_retry", data={"decision": "approve"}, headers=H)) == 400)

# rules via /rules form (full form, as the browser would send it)
from app.web.views import _flatten_rules  # noqa: E402
from app.web import state as wst  # noqa: E402


def form_from(rules, **over):
    f = {}
    for x in _flatten_rules(rules):
        k, kind, v = x["key"], x["kind"], x["value"]
        if kind == "bool":
            if v:
                f[k] = "on"
        elif kind == "numdict":
            for s, sv in v.items():
                f[k + "." + s] = str(sv)
        elif kind == "lines":
            f[k] = "\n".join(v)
        elif kind == "json":
            f[k] = json.dumps(v)
        else:
            f[k] = str(v)
    f.update(over)
    return f


rules0 = wst.load_rules()
b = wst.get_state()["metrics"]["auto_applied"]
r = c.post("/rules", data=form_from(rules0, auto_apply_max_amount="1000", note="QA: cap test"))
a = wst.get_state()["metrics"]["auto_applied"]
check("D", "rules change via /rules form shows before/after", r.status_code == 200 and a != b and "auto applied" in text(r.text).lower(), "auto_applied %s -> %s" % (b, a))
c.post("/rules", data=form_from(wst.load_rules(), auto_apply_max_amount="10000", note="QA: reset"))
# partial form (e.g. a script or a stale tab) silently turns guardrails off
r = c.post("/rules", data={"fee_tolerance": "25"})
after = wst.load_rules()
lost = [k for k in ("top50_human_only", "auto_apply_exact_ref_match", "notify_am_before_contact") if rules0.get(k) and not after.get(k)]
check("D", "partial /rules POST does not switch guardrails off", not lost and len(after.get("banned_phrases", [])) == len(rules0["banned_phrases"]),
      "after POST {fee_tolerance:25}: turned off %s; banned_phrases %d -> %d" % (lost, len(rules0["banned_phrases"]), len(after.get("banned_phrases", []))))
c.post("/rules", data=form_from(rules0, note="QA: restore"))
check("D", "rules restored", wst.load_rules() == rules0, "")
# rules via chat + /api/rules/apply
r = c.post("/api/chat", json={"message": "set auto_apply_max_amount to 1000"}).json()
ok = bool(r.get("actions")) and r["actions"][0]["rule"] == "auto_apply_max_amount"
b = wst.get_state()["metrics"]["auto_applied"]
r2 = c.post("/api/rules/apply", json={"rule": "auto_apply_max_amount", "value": "1000"})
a = wst.get_state()["metrics"]["auto_applied"]
check("D", "chat 'set ... to ...' + /api/rules/apply re-runs with before/after", ok and r2.status_code == 200 and a != b, "auto_applied %s -> %s; reply: %s" % (b, a, r2.json().get("cards", [{}])[0].get("lines")))
c.post("/api/rules/apply", json={"rule": "auto_apply_max_amount", "value": "10000"})
# instruction via chat -> accept -> manual file
r = c.post("/api/chat", json={"message": "from now on cc Dana on anything over $40k", "agent": "collections"}).json()
ins = [i for i in store.instructions() if "over $40k" in i["text"]]
iid = ins[-1]["id"] if ins else None
r3 = c.post("/direct/instructions/%s/accept" % iid, follow_redirects=False) if iid else None
manual_hit = [f for f in os.listdir(os.path.join(TMP, "manuals")) if "over $40k" in open(os.path.join(TMP, "manuals", f)).read()]
check("D", "chat 'from now on ...' -> accept in Direct -> in agent manual", bool(iid) and r3.status_code == 303 and bool(manual_hit), "instruction %s, manuals containing it: %s, agent=%s" % (iid, manual_hit, ins[-1]["agent"] if ins else None))
# Loom link
r = c.post("/demo", data={"url": "https://www.loom.com/share/abc123DEF456"}, follow_redirects=True)
check("D", "Loom share link saved and embedded", "https://www.loom.com/embed/abc123DEF456" in r.text, "")
check("D", "non-video link rejected", c.post("/demo", data={"url": "https://evil.example/x"}).status_code == 400, "")
# audit / activity / csv
acts = store.all_actions()
aud = text(c.get("/audit?agent=Human").text)
actv = text(c.get("/activity?who=Humans").text)
csvt = c.get("/audit.csv").text
miss_a = [a["object_id"] for a in acts if a["object_id"] not in aud]
miss_v = [a["object_id"] for a in acts if a["object_id"] not in actv]
nouser = [a["id"] for a in acts if not a.get("user_email")]
check("D", "every human action in /audit", not miss_a, "%d actions; missing %s" % (len(acts), miss_a[:5]))
check("D", "every human action in /activity", not miss_v, "missing %s" % miss_v[:5])
check("D", "every human action has a user and a reason", not nouser and all(a.get("note") for a in acts), "")
check("D", "CSV export has every human action", all(a["object_id"] in csvt for a in acts) and csvt.startswith("ts,who"), "%d lines" % csvt.count("\n"))
dup = c.post("/cash/PAY-65750/approve", data={"note": "QA: second approve"}, headers=H).status_code
check("D", "approving an already-approved payment is refused", dup == 400, "HTTP %d (second 'apply' row written)" % dup)
ex = c.post("/cash/PAY-65805/approve", data={"note": "QA"}, headers=H).status_code
print("info: approve on ambiguous Kingsway proposal ->", ex, "(records apply to", [a["payload"] for a in store.all_actions() if a["object_id"] == "PAY-65805"][-1:], ")")

import csv as _csv  # noqa: E402
with open(os.path.join(ROOT, "analysis", "work", "eval_web_results.csv"), "w", newline="") as f:
    w = _csv.writer(f)
    w.writerow(["section", "check", "result", "detail"])
    w.writerows(RES)
print("SUMMARY C: %d/%d PASS, D: %d/%d PASS" % (sum(1 for r in RES if r[0] == "C" and r[2] == "PASS"), sum(1 for r in RES if r[0] == "C"),
                                              sum(1 for r in RES if r[0] == "D" and r[2] == "PASS"), sum(1 for r in RES if r[0] == "D")))
