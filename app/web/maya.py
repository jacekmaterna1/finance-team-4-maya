"""Maya desk: the team's questions for the COO, approved by a person, carried by the operator ("courier").

UI:      /maya (desk above the historical thread), POST /maya/q/{id}/approve|dismiss|outcome|instruction
Courier: GET /api/maya/queue, POST /api/maya/sent, POST /api/maya/reply
         If MAYA_COURIER_TOKEN is set, these require header X-Courier-Token (checked in app.main's auth middleware too).
Every transition is written to the append-only actions store, so it shows in Activity and the audit trail.
"""
import hmac
import os
import re
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from app import auth, store
from app.web import rig_data
from app.web import state as st

MAX_BUNDLE = 1400


def courier_token() -> str:
    return os.environ.get("MAYA_COURIER_TOKEN", "").strip()


def courier_ok(request: Request) -> bool:
    tok = courier_token()
    return bool(tok) and hmac.compare_digest(request.headers.get("X-Courier-Token", ""), tok)


def baseline_used() -> int:
    ob = rig_data.read_rel("trail/MAYA_OUTBOX.md") or ""
    m = re.search(r"Messages used:\s*\**\s*(\d+)", ob, re.I)
    return int(m.group(1)) if m else 0


def purpose_mix(qs: List[Dict[str, Any]]) -> str:
    kinds = []
    for q in qs:
        p = (q.get("purpose") or "").strip() or "Confirmation"
        if p not in kinds:
            kinds.append(p)
    return " and ".join(kinds)


def bundle(qs: List[Dict[str, Any]]) -> str:
    if not qs:
        return ""
    parts = ["({}) {}".format(n, " ".join(q["final_text"].split())) for n, q in enumerate(qs, 1)]
    return "Purpose: {}. {}".format(purpose_mix(qs), " ".join(parts))


def desk() -> Dict[str, Any]:
    proposed = store.maya_questions("proposed")
    approved = store.maya_questions("approved")
    sent = store.maya_questions("sent")
    answered = store.maya_questions("answered")
    b = bundle(approved)
    exchanges: List[Dict[str, Any]] = []
    for q in sorted(sent + answered, key=lambda x: x.get("sent_ts") or ""):
        key = q.get("sent_message") or q.get("sent_ts")
        if exchanges and exchanges[-1]["key"] == key:
            ex = exchanges[-1]
        else:
            ex = {"key": key, "sent_ts": q.get("sent_ts"), "message": q.get("sent_message") or "", "reply": None,
                  "reply_ts": None, "outcomes": []}
            exchanges.append(ex)
        if q.get("reply") and not ex["reply"]:
            ex["reply"], ex["reply_ts"] = q["reply"], q.get("reply_ts")
        if q.get("outcome"):
            ex["outcomes"].append("{}: {}".format(q.get("topic"), q["outcome"]))
    base = baseline_used()
    return {"proposed": proposed, "approved": approved, "sent": sent, "answered": answered,
            "bundle": b, "bundle_len": len(b), "too_long": len(b) > MAX_BUNDLE, "max": MAX_BUNDLE,
            "used": base + store.maya_sent_bundles(), "baseline": base, "budget": 60,
            "resolved": store.maya_questions("resolved"), "dismissed": store.maya_questions("dismissed"),
            "exchanges": exchanges, "error": st._cache.get("maya_error")}


def desk_counts() -> Dict[str, int]:
    return {k: len(store.maya_questions(k)) for k in ("proposed", "approved", "sent", "answered")}


def agent_for(q: Dict[str, Any]) -> Dict[str, Any]:
    t = " ".join(str(q.get(k) or "") for k in ("changes", "topic", "text")).lower()
    if re.search(r"card write|\bholds?\b|\bheld\b|dispute|escalation|\brelease|\broute", t):
        slug = "controller"
    elif re.search(r"auto_apply|cash|receipt|payment|writeoff_threshold|unapplied", t):
        slug = "cash"
    elif re.search(r"draft|remind|email|collections|tone|cc ", t):
        slug = "collections"
    elif re.search(r"ticket text|context|contact", t):
        slug = "context"
    else:
        slug = "controller"
    return rig_data.AGENT_BY_SLUG[slug]


def _get(qid: str) -> Dict[str, Any]:
    q = store.get_maya_question(qid)
    if not q:
        raise HTTPException(404, "question not found")
    return q


def build_router(render, user_of) -> APIRouter:
    r = APIRouter()

    @r.get("/maya", response_class=HTMLResponse)
    async def maya_page(request: Request):
        st.get_state()  # make sure questions are synced at least once
        return render(request, "rig_maya.html", {"t": rig_data.parse_maya(), "d": desk(), "tab": "maya"})

    @r.post("/maya/q/{qid}/approve")
    async def approve(request: Request, qid: str, text: str = Form("")):
        user = user_of(request)
        q = _get(qid)
        if q["status"] != "proposed":
            raise HTTPException(400, "Already " + q["status"])
        text = " ".join(text.split()) or q["text"]
        store.update_maya_question(qid, status="approved", edited_text=text if text != q["text"] else None,
                                   approved_by=user, approved_ts=store._now())
        store.record(user, "maya_question", qid, "approve", "Approved question for Maya: " + (q.get("topic") or ""),
                     {"edited": text != q["text"], "text": text, "purpose": q.get("purpose")})
        return RedirectResponse("/maya#approved", status_code=303)

    @r.post("/maya/q/{qid}/dismiss")
    async def dismiss(request: Request, qid: str, reason: str = Form("")):
        user = user_of(request)
        q = _get(qid)
        if q["status"] not in ("proposed", "approved"):
            raise HTTPException(400, "Already " + q["status"])
        store.update_maya_question(qid, status="dismissed", outcome="Dismissed: " + (reason.strip() or "no reason given"))
        store.record(user, "maya_question", qid, "reject", "Dismissed question for Maya: {} ({})".format(
            q.get("topic"), reason.strip() or "no reason given"), {"purpose": q.get("purpose")})
        return RedirectResponse("/maya#desk", status_code=303)

    @r.post("/maya/q/{qid}/unapprove")
    async def unapprove(request: Request, qid: str):
        user = user_of(request)
        q = _get(qid)
        if q["status"] != "approved":
            raise HTTPException(400, "Only approved questions can go back")
        store.update_maya_question(qid, status="proposed")
        store.record(user, "maya_question", qid, "edit", "Moved back to proposed: " + (q.get("topic") or ""), {})
        return RedirectResponse("/maya#desk", status_code=303)

    @r.post("/maya/q/{qid}/outcome")
    async def outcome(request: Request, qid: str, outcome: str = Form("")):
        user = user_of(request)
        q = _get(qid)
        store.update_maya_question(qid, outcome=outcome.strip())
        store.record(user, "maya_question", qid, "edit", "What we changed because of Maya's answer: " + outcome.strip(),
                     {"topic": q.get("topic")})
        return RedirectResponse("/maya#answered", status_code=303)

    @r.post("/maya/q/{qid}/instruction")
    async def to_instruction(request: Request, qid: str):
        user = user_of(request)
        q = _get(qid)
        if not q.get("reply"):
            raise HTTPException(400, "No answer from Maya yet")
        a = agent_for(q)
        basis = q.get("outcome") or " ".join((q.get("reply") or "").split())[:600]
        text = "Per Maya ({}, {}): {}".format(q["id"], q.get("topic") or "", basis)
        iid = store.add_instruction(user, a["name"], text, source="maya")
        store.record(user, "maya_question", qid, "edit", "Turned Maya's answer into proposed instruction #{} for {}".format(
            iid, a["name"]), {"instruction_id": iid})
        return RedirectResponse("/direct#instructions", status_code=303)

    # ---------------- courier API (the operator's Claude Code session carries messages to and from Maya)
    def _courier_actor(request: Request) -> str:
        if courier_token():
            if not courier_ok(request):
                raise HTTPException(401, "X-Courier-Token required")
            return "courier"
        return "courier" if not auth.current_user(request) or auth.dev_mode() else auth.current_user(request)

    @r.get("/api/maya/queue")
    async def queue(request: Request):
        if courier_token() and not courier_ok(request) and not (auth.current_user(request) and not auth.dev_mode()):
            raise HTTPException(401, "X-Courier-Token required")
        approved = store.maya_questions("approved")
        b = bundle(approved)
        return JSONResponse({"bundle_text": b, "question_ids": [q["id"] for q in approved],
                             "purpose_mix": purpose_mix(approved), "chars": len(b), "too_long": len(b) > MAX_BUNDLE})

    async def _body(request: Request) -> Dict[str, Any]:
        try:
            body = await request.json()
        except ValueError:
            raise HTTPException(400, "JSON body required")
        ids = body.get("question_ids")
        if not isinstance(ids, list) or not ids:
            raise HTTPException(400, "question_ids (non-empty list) required")
        return body

    @r.post("/api/maya/sent")
    async def sent(request: Request):
        actor = _courier_actor(request)
        body = await _body(request)
        ts = str(body.get("ts") or store._now())
        message = str(body.get("message") or "")
        done, skipped = [], []
        for qid in body["question_ids"]:
            q = store.get_maya_question(str(qid))
            if not q or q["status"] not in ("approved", "proposed"):
                skipped.append(qid)
                continue
            store.update_maya_question(q["id"], status="sent", sent_ts=ts, sent_message=message or bundle([q]))
            store.record(actor, "maya_question", q["id"], "send", "Sent to Maya: " + (q.get("topic") or ""),
                         {"ts": ts, "chars": len(message)})
            done.append(q["id"])
        return JSONResponse({"ok": True, "sent": done, "skipped": skipped})

    @r.post("/api/maya/reply")
    async def reply(request: Request):
        actor = _courier_actor(request)
        body = await _body(request)
        ts = str(body.get("ts") or store._now())
        text = str(body.get("reply") or "").strip()
        if not text:
            raise HTTPException(400, "reply required")
        done, skipped = [], []
        for qid in body["question_ids"]:
            q = store.get_maya_question(str(qid))
            if not q or q["status"] not in ("sent", "approved", "answered"):
                skipped.append(qid)
                continue
            store.update_maya_question(q["id"], status="answered", reply=text, reply_ts=ts)
            store.record(actor, "maya_question", q["id"], "reply", "Maya answered: " + (q.get("topic") or ""),
                         {"ts": ts, "reply": text[:2000]})
            done.append(q["id"])
        return JSONResponse({"ok": True, "answered": done, "skipped": skipped})

    return r
