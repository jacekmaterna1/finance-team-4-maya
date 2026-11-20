"""Regression tests for the server-side guardrails found in analysis/QA_PASS_2.md (D2-D6 and polish items).

Run: .venv/bin/python -m pytest -q
Uses a throw-away DB, rules file and manuals dir, so nothing in the repo is touched.
"""
import os
import shutil
import tempfile

_TMP = tempfile.mkdtemp(prefix="ledgerline-tests-")
os.environ["DB_PATH"] = os.path.join(_TMP, "test.db")
os.environ["RULES_PATH"] = os.path.join(_TMP, "rules.json")
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shutil.copytree(os.path.join(_ROOT, "app", "engine", "manuals"), os.path.join(_TMP, "manuals"))
os.environ["MANUALS_DIR"] = os.path.join(_TMP, "manuals")
os.environ.pop("GOOGLE_CLIENT_ID", None)
os.environ.pop("MAYA_COURIER_TOKEN", None)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import store  # noqa: E402
from app.main import app  # noqa: E402
from app.web import state as st  # noqa: E402

client = TestClient(app)
ORIGINAL_RULES = st.load_rules()


@pytest.fixture(autouse=True)
def fresh(tmp_path, monkeypatch):
    """Fresh action store per test; rules restored after each test."""
    monkeypatch.setenv("DB_PATH", str(tmp_path / "actions.db"))
    store.init_db()
    yield
    st.save_rules(dict(ORIGINAL_RULES))
    st.refresh()


def state():
    return st.get_state()


def first(pred):
    for i in state()["invoices"]:
        if pred(i):
            return i
    pytest.skip("no invoice in the data matches this case")


def has_code(i, *codes):
    return any(h.get("code") in codes for h in i.get("holds") or [])


def draft_form(i, **over):
    d = i["draft"]
    form = {"subject": d["subject"], "body": d["body"], "to": ", ".join(d.get("to") or []), "cc": ", ".join(d.get("cc") or [])}
    form.update(over)
    return form


# ---------------------------------------------------------------- SEV-2 #1: dispute holds need the AM, release or override
def test_override_dispute_hold_requires_am_confirmation():
    i = first(lambda x: x["action"] == "HOLD" and has_code(x, "DISPUTE", "CANCELLATION"))
    url = "/collections/{}/hold".format(i["invoice_id"])
    r = client.post(url, data={"kind": "override_hold", "reason": "agent misread the ticket"})
    assert r.status_code == 400
    r = client.post(url, data={"kind": "release_hold", "reason": "settled per AM"})
    assert r.status_code == 400
    r = client.post(url, data={"kind": "override_hold", "reason": "agent misread the ticket", "am_confirmed": "on",
                               "am_name": "Nadia Upton"})
    assert r.status_code in (200, 303)
    assert store.history("invoice", i["invoice_id"])[-1]["payload"]["am_name"] == "Nadia Upton"


def test_override_non_dispute_hold_reason_only():
    i = first(lambda x: x["action"] == "HOLD" and not has_code(x, "DISPUTE", "CANCELLATION"))
    r = client.post("/collections/{}/hold".format(i["invoice_id"]), data={"kind": "override_hold", "reason": "ok"})
    assert r.status_code == 400  # reason too short
    r = client.post("/collections/{}/hold".format(i["invoice_id"]),
                    data={"kind": "override_hold", "reason": "checked the bank portal, not ours"})
    assert r.status_code in (200, 303)


# ---------------------------------------------------------------- SEV-2 #2: send guards
def test_send_on_held_invoice_rejected():
    i = first(lambda x: x["action"] == "HOLD" and has_code(x, "MONEY_RECEIVED"))
    r = client.post("/collections/{}/send".format(i["invoice_id"]),
                    data={"subject": "Invoice", "body": "Hi, a reminder about your invoice.", "to": ""})
    assert r.status_code == 400
    assert not [a for a in store.history("invoice", i["invoice_id"]) if a["action"] == "send"]


def test_send_after_every_hold_lifted_is_allowed():
    i = first(lambda x: x["action"] == "HOLD" and not has_code(x, "DISPUTE", "CANCELLATION"))
    client.post("/collections/{}/hold".format(i["invoice_id"]),
                data={"kind": "override_hold", "reason": "verified with Priya, chase is fine"})
    c = state()["customers"][i["customer_id"]]
    to = [x["email"] for x in c["contacts"] if x.get("verified")]
    if not to:
        pytest.skip("no verified contact")
    r = client.post("/collections/{}/send".format(i["invoice_id"]),
                    data={"subject": "Invoice", "body": "Hi, a quick note about your invoice.", "to": to[0], "cc": ""})
    assert r.status_code in (200, 303)


def test_send_to_unknown_recipient_rejected():
    i = first(lambda x: x["action"] == "DRAFT_REMINDER" and x.get("draft"))
    r = client.post("/collections/{}/send".format(i["invoice_id"]),
                    data=draft_form(i, to="ap@okaforlegal-billing.example"))
    assert r.status_code == 400
    r = client.post("/collections/{}/send".format(i["invoice_id"]),
                    data=draft_form(i, to=", ".join(i["draft"]["to"] + ["someone@else.example"])))
    assert r.status_code == 400


def test_send_bad_cc_rejected_and_good_send_once():
    i = first(lambda x: x["action"] == "DRAFT_REMINDER" and x.get("draft"))
    url = "/collections/{}/send".format(i["invoice_id"])
    assert client.post(url, data=draft_form(i, cc="friend@gmail.com")).status_code == 400
    assert client.post(url, data=draft_form(i)).status_code in (200, 303)
    assert client.post(url, data=draft_form(i)).status_code == 400  # already sent


def test_send_banned_phrase_word_boundary():
    i = first(lambda x: x["action"] == "DRAFT_REMINDER" and x.get("draft"))
    url = "/collections/{}/send".format(i["invoice_id"])
    r = client.post(url, data=draft_form(i, body=i["draft"]["body"] + "\nOtherwise we will take legal action."))
    assert r.status_code == 400
    banned = [b.lower() for b in state()["rules"].get("banned_phrases", [])]
    if "court" in banned:
        r = client.post(url, data=draft_form(i, body=i["draft"]["body"] + "\nThanks for the courtesy."))
        assert r.status_code in (200, 303)


def test_send_on_retry_card_or_no_action_rejected():
    i = first(lambda x: x["action"] in ("RETRY_CARD", "NO_ACTION"))
    r = client.post("/collections/{}/send".format(i["invoice_id"]), data={"subject": "x", "body": "hello there"})
    assert r.status_code == 400


# ---------------------------------------------------------------- SEV-2 #3: rules
def test_partial_rules_post_leaves_other_fields_alone():
    before = st.load_rules()
    r = client.post("/rules", data={"fee_tolerance": "25"})
    assert r.status_code == 200
    after = st.load_rules()
    for k in ("top50_human_only", "auto_apply_exact_ref_match", "notify_am_before_contact", "banned_phrases"):
        assert after[k] == before[k], k
    assert float(after["fee_tolerance"]) == 25.0


def test_empty_banned_phrases_refused():
    r = client.post("/rules", data={"__present": "banned_phrases", "banned_phrases": ""})
    assert r.status_code == 400
    assert st.load_rules()["banned_phrases"] == ORIGINAL_RULES["banned_phrases"]


@pytest.mark.parametrize("data", [
    {"__present": "top50_human_only"},                       # unticked checkbox = turn off
    {"__present": "notify_am_before_contact"},
    {"__present": "use_claude", "use_claude": "on"},
    {"writeoff_threshold": "100"},
    {"auto_apply_max_amount": "25000"},
])
def test_sensitive_rule_change_needs_dana(data):
    before = st.load_rules()
    r = client.post("/rules", data=data)
    assert r.status_code == 400
    assert st.load_rules() == before
    ok = dict(data, dana_approved="on", dana_name="Dana Ruiz")
    r = client.post("/rules", data=ok)
    assert r.status_code == 200
    rows = [a for a in store.all_actions() if a["object_type"] == "rules"]
    assert rows and rows[-1]["payload"]["dana_name"] == "Dana Ruiz"


def test_chat_rule_apply_needs_dana():
    j = client.post("/api/chat", json={"message": "set writeoff_threshold to 50"}).json()
    assert j["actions"] and j["actions"][0]["needs_dana"] is True
    assert client.post("/api/rules/apply", json={"rule": "writeoff_threshold", "value": 50}).status_code == 400
    r = client.post("/api/rules/apply", json={"rule": "writeoff_threshold", "value": 50, "dana_approved": True,
                                             "dana_name": "Dana Ruiz"})
    assert r.status_code == 200
    assert float(st.load_rules()["writeoff_threshold"]) == 50.0


def test_chat_harmless_rule_needs_no_dana():
    r = client.post("/api/rules/apply", json={"rule": "fee_tolerance", "value": 30})
    assert r.status_code == 200


# ---------------------------------------------------------------- SEV-3
def test_payment_cannot_be_approved_twice():
    p = next((x for x in state()["payments"] if x["decision"] == "PROPOSE"), None)
    if not p:
        pytest.skip("no proposal")
    url = "/cash/{}/approve".format(p["payment_id"])
    assert client.post(url, follow_redirects=False).status_code in (200, 303)
    r = client.post(url, follow_redirects=False)
    assert r.status_code == 409
    assert len([a for a in store.history("payment", p["payment_id"]) if a["action"] == "apply"]) == 1


def test_human_writes_group_label():
    assert "A person writes these (top-50, legal risk, 90+ days)" in client.get("/collections").text


def test_demo_hides_video_script_and_shows_outline():
    html = client.get("/demo").text
    assert "Before recording" not in html and "Leave Maya on hold" not in html
    if "<iframe" not in html:
        assert "recorded by Jacek" in html and "Where it gets things wrong" in html


def test_docs_repo_marked_private():
    assert "private — access on request" in client.get("/docs").text


def test_times_shown_in_cst():
    p = next((x for x in state()["payments"] if x["decision"] == "PROPOSE"), None)
    if p:
        client.post("/cash/{}/approve".format(p["payment_id"]))
    assert "CST" in client.get("/audit").text


def test_every_route_200():
    routes = ["/", "/team", "/architecture", "/docs", "/activity", "/maya", "/direct", "/buildlog", "/about", "/demo",
              "/today", "/cash", "/collections", "/customers", "/digest", "/audit", "/audit.csv", "/rules", "/healthz",
              "/api/maya/queue"] + ["/agents/" + s for s in ("cash", "context", "controller", "collections")]
    bad = [(p, client.get(p).status_code) for p in routes if client.get(p).status_code != 200]
    assert not bad
