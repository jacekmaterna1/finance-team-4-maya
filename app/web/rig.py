"""The RIG: command center for the finance agent team. Home, Team, Architecture, Activity, Maya, Direct, Build log."""
from collections import Counter
from typing import Any, Dict, List

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app import store
from app.web import rig_data
from app.web import state as st
import os

from app.web.views import (_render, _user, dana_decisions, demo_video_url, embed_url, live_counts, needs_you,
                           valid_video_url)

from app.web.maya import desk_counts as maya_desk_counts

REPO_URL = "https://github.com/jacekmaterna1/finance-team-4-maya"


def agent_stats(state, slug: str) -> Dict[str, Any]:
    m = state["metrics"]
    customers = state.get("customers") or {}
    if slug == "cash":
        return {"headline": "{} auto-applied · {} to confirm".format(m.get("auto_applied", 0), m.get("needs_review", 0)),
                "big": "${:,.0f}".format(m.get("cash_found", 0) or 0), "big_label": "cash found in unapplied receipts",
                "counts": [("Auto-applied", m.get("auto_applied", 0)), ("Proposals", m.get("needs_review", 0)),
                           ("Cash found", "${:,.0f}".format(m.get("cash_found", 0) or 0))]}
    if slug == "context":
        kinds = Counter(a.get("decision") for a in state.get("audit", []) if a.get("agent") == "Account Context")
        return {"headline": "{} customers profiled".format(len(customers)),
                "big": "${:,.0f}".format(m.get("overdue_disputed", 0) or 0), "big_label": "disputed in support tickets",
                "counts": [("Customers", len(customers)), ("Disputes", kinds.get("dispute", 0)),
                           ("Cancellations", kinds.get("cancellation", 0)), ("Legal threats", kinds.get("legal_threat", 0))]}
    if slug == "controller":
        ov = rig_data.hold_override_rate()
        return {"headline": "{} held · override rate {}".format(m.get("held", 0), ov["label"]),
                "big": str(m.get("chases_prevented", 0)), "big_label": "wrong chases prevented",
                "counts": [("Held", m.get("held", 0)), ("Person writes", m.get("human_writes", 0)),
                           ("Dana decisions", m.get("dana_decisions", 0)), ("Override rate", ov["label"])]}
    return {"headline": "{} drafts · {} card re-runs".format(m.get("drafts", 0), m.get("card_retries", 0)),
            "big": str(m.get("drafts", 0)), "big_label": "reminders drafted for Priya",
            "counts": [("Drafts", m.get("drafts", 0)), ("Card re-runs", m.get("card_retries", 0)),
                       ("Emails sent alone", 0)]}


def agent_queue(state, slug: str, latest) -> List[Dict[str, Any]]:
    from app.web.views import invoice_pending, payment_pending
    if slug == "cash":
        return [{"id": p["payment_id"], "amount": p["amount"], "who": p.get("customer_name") or p.get("payer_name"),
                 "what": p["decision"], "link": "/cash#" + p["payment_id"]}
                for p in state["payments"] if payment_pending(p, latest)]
    if slug == "context":
        return [{"id": c["customer_id"], "amount": None, "who": c["name"], "what": "; ".join(c.get("flags") or []),
                 "link": "/customers/" + c["customer_id"]}
                for c in (state.get("customers") or {}).values() if c.get("billing_complaint")][:25]
    acts = ("HOLD",) if slug == "controller" else ("DRAFT_REMINDER", "HUMAN_WRITES", "RETRY_CARD")
    rows = [{"id": i["invoice_id"], "amount": i["amount"], "who": i["customer_name"],
             "what": i["action"] + (": " + ", ".join(h.get("label") or h.get("code") for h in i["holds"]) if i.get("holds") else ""),
             "link": "/collections#" + i["invoice_id"]}
            for i in state["invoices"] if i["action"] in acts and invoice_pending(i, latest)]
    rows.sort(key=lambda x: -float(x["amount"] or 0))
    return rows


def decisions(state, name: str, n: int) -> List[Dict[str, Any]]:
    return [a for a in state.get("audit", []) if a.get("agent") == name][-n:][::-1]


def build_router() -> APIRouter:
    r = APIRouter()

    @r.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        state = st.get_state()
        latest = store.latest_by_object()
        team = [dict(a, stats=agent_stats(state, a["slug"])) for a in rig_data.AGENTS]
        items = needs_you(state, latest)
        return _render(request, "rig_home.html", {
            "m": state["metrics"], "live": live_counts(state, latest), "team": team, "items": items[:12],
            "n_items": len(items), "dana": dana_decisions(state), "maya": rig_data.latest_maya(),
            "override": rig_data.hold_override_rate(), "golive": rig_data.GO_LIVE, "tab": "home",
            "M": rig_data.MISSION, "P": rig_data.PROGRESS, "desk": maya_desk_counts()})

    @r.get("/team", response_class=HTMLResponse)
    async def team(request: Request):
        state = st.get_state()
        rows = []
        for a in rig_data.AGENTS:
            rows.append(dict(a, stats=agent_stats(state, a["slug"]), last=decisions(state, a["name"], 5),
                             instructions=store.instructions(a["name"])))
        return _render(request, "rig_team.html", {"agents": rows, "humans": rig_data.HUMANS, "tab": "team",
                                                  "override": rig_data.hold_override_rate(),
                                                  "M": rig_data.MISSION, "P": rig_data.PROGRESS,
                                                  "m": state["metrics"],
                                                  "live": live_counts(state, store.latest_by_object())})

    @r.get("/docs", response_class=HTMLResponse)
    async def docs(request: Request):
        tdir = os.path.join(rig_data.ROOT_DIR, "submission", "ai_conversations")
        transcripts = sorted(f for f in os.listdir(tdir) if not f.startswith(".")) if os.path.isdir(tdir) else []
        base = os.environ.get("BASE_URL", "").rstrip("/") or str(request.base_url).rstrip("/")
        return _render(request, "rig_docs.html", {"tab": "docs", "transcripts": transcripts, "repo_url": REPO_URL,
                                                  "base_url": base})

    def _demo_ctx(error="", raw=None):
        url = demo_video_url()
        # VIDEO_SCRIPT.md holds internal prep notes, so it is deliberately not rendered here.
        return {"tab": "demo", "video": embed_url(url) if url else None, "raw": raw if raw is not None else url,
                "error": error}

    @r.get("/demo", response_class=HTMLResponse)
    async def demo(request: Request):
        return _render(request, "rig_demo.html", _demo_ctx())

    @r.post("/demo", response_class=HTMLResponse)
    async def demo_save(request: Request, url: str = Form("")):
        user = _user(request)
        url = url.strip()
        if not valid_video_url(url):
            return _render(request, "rig_demo.html", _demo_ctx(
                "Paste an https link from Loom (loom.com/share/... or /embed/...), YouTube or Google Drive.", raw=url),
                status_code=400)
        before = store.get_setting("demo_video_url")
        store.set_setting("demo_video_url", url, user)
        store.record(user, "settings", "demo_video_url", "edit", "Set the demo video link",
                     {"before": before, "after": url, "embed": embed_url(url)})
        return RedirectResponse("/demo", status_code=303)

    @r.get("/architecture", response_class=HTMLResponse)
    async def architecture(request: Request):
        return _render(request, "rig_architecture.html", {"tab": "architecture"})

    @r.get("/activity", response_class=HTMLResponse)
    async def activity(request: Request, who: str = "", q: str = ""):
        state = st.get_state()
        rows = rig_data.activity(state, who, q)
        chips = [a["name"] for a in rig_data.AGENTS] + ["Humans"]
        return _render(request, "rig_activity.html", {"rows": rows, "who": who, "q": q, "chips": chips,
                                                      "tab": "activity"})

    @r.get("/direct", response_class=HTMLResponse)
    async def direct(request: Request, saved: str = ""):
        rows = [dict(a, manual=rig_data.read_manual(a), instructions=store.instructions(a["name"]))
                for a in rig_data.AGENTS]
        return _render(request, "rig_direct.html", {"agents": rows, "all_instr": store.instructions(),
                                                    "saved": saved, "tab": "direct"})

    @r.post("/direct/instructions")
    async def add_instruction(request: Request, agent: str = Form(...), text: str = Form(...)):
        user = _user(request)
        a = rig_data.AGENT_BY_SLUG.get(agent) or rig_data.AGENT_BY_NAME.get(agent)
        if not a:
            raise HTTPException(400, "unknown agent")
        if len(text.strip()) < 5:
            raise HTTPException(400, "Write the instruction in a sentence.")
        store.add_instruction(user, a["name"], text.strip(), source="form")
        return RedirectResponse("/direct#instructions", status_code=303)

    @r.post("/direct/instructions/{iid}/{decision}")
    async def decide_instruction(request: Request, iid: int, decision: str):
        user = _user(request)
        ins = store.get_instruction(iid)
        if not ins:
            raise HTTPException(404, "instruction not found")
        if decision not in ("accept", "reject"):
            raise HTTPException(400, "bad decision")
        if ins["status"] != "proposed":
            raise HTTPException(400, "Already " + ins["status"])
        a = rig_data.AGENT_BY_NAME.get(ins["agent"])
        if decision == "accept":
            line = "{} (proposed by {} on {}; accepted by {})".format(ins["text"], ins["user"], ins["ts"][:10], user)
            if a:
                rig_data.append_standing_instruction(a, line)
            store.decide_instruction(iid, "accepted", user)
            store.record(user, "instruction", str(iid), "approve",
                         "Accepted instruction for {}: {}".format(ins["agent"], ins["text"]),
                         {"agent": ins["agent"], "manual": a["manual"] + ".md" if a else None})
        else:
            store.decide_instruction(iid, "rejected", user)
            store.record(user, "instruction", str(iid), "reject",
                         "Rejected instruction for {}: {}".format(ins["agent"], ins["text"]), {"agent": ins["agent"]})
        back = request.headers.get("referer") or "/direct"
        return RedirectResponse("/direct#instructions" if "/agents/" not in back else
                                "/agents/{}#instructions".format(a["slug"] if a else ""), status_code=303)

    @r.post("/agents/{slug}/manual")
    async def save_manual(request: Request, slug: str, text: str = Form(...), note: str = Form("")):
        user = _user(request)
        a = rig_data.AGENT_BY_SLUG.get(slug)
        if not a:
            raise HTTPException(404, "unknown agent")
        before = rig_data.read_manual(a)
        if text.replace("\r\n", "\n").strip() != before.strip():
            rig_data.write_manual(a, text)
            store.record(user, "manual", a["manual"], "edit", note.strip() or "Edited the {} manual".format(a["name"]),
                         {"agent": a["name"], "chars_before": len(before), "chars_after": len(text)})
        return RedirectResponse("/direct?saved={}#manual-{}".format(slug, slug), status_code=303)

    @r.get("/agents/{slug}", response_class=HTMLResponse)
    async def agent_page(request: Request, slug: str):
        a = rig_data.AGENT_BY_SLUG.get(slug)
        if not a:
            raise HTTPException(404, "unknown agent")
        state = st.get_state()
        latest = store.latest_by_object()
        return _render(request, "rig_agent.html", {
            "a": a, "stats": agent_stats(state, slug), "manual_html": rig_data.md(rig_data.read_manual(a)),
            "instructions": store.instructions(a["name"]), "queue": agent_queue(state, slug, latest)[:30],
            "last": decisions(state, a["name"], 20), "tab": "team", "chat_agent": slug})

    @r.get("/buildlog", response_class=HTMLResponse)
    async def buildlog(request: Request):
        docs = []
        for rel, title, open_ in [("trail/JOURNAL.md", "Journal: every step, timestamped", True),
                                  ("trail/DECISIONS.md", "Decisions: what we chose, what we rejected, why", False),
                                  ("trail/MAYA_QA.md", "Maya Q&A, word for word", False),
                                  ("analysis/FAILURES.md", "Where it gets things wrong", False),
                                  ("analysis/EVAL.md", "Evaluation: accuracy on the real records", False),
                                  ("analysis/DISCREPANCIES.md", "Data-room QA: does the data tie out?", False),
                                  ("submission/LEGAL_NOTE.md", "Note for Legal: AI provider and data", False),
                                  ("analysis/FACTS.md", "Data-room facts (evidence numbers)", False)]:
            txt = rig_data.read_rel(rel)
            docs.append({"rel": rel, "title": title, "html": rig_data.md(txt) if txt else None, "open": open_})
        return _render(request, "rig_buildlog.html", {"docs": docs, "tab": "buildlog"})

    return r
