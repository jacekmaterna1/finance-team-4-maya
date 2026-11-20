"""Pages and actions. Agents propose; a person approves here. Every human action goes to app.store (append-only)."""
import copy
import csv
import io
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app import auth, store
from app.web import rig_data
from app.web import state as st

WEB_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(WEB_DIR))
STATIC_DIR = os.path.join(WEB_DIR, "static")
TEMPLATE_DIR = os.path.join(WEB_DIR, "templates")
ONE_PAGER = os.path.join(ROOT_DIR, "submission", "ONE_PAGER.md")

templates = Jinja2Templates(directory=TEMPLATE_DIR)

AGENTS = ["Cash Application", "Account Context", "Controller", "Collections"]
ACTION_ORDER = ["HOLD", "RETRY_CARD", "HUMAN_WRITES", "DRAFT_REMINDER", "NO_ACTION"]
RELEASE_NEEDS_AM = ("DISPUTE", "CANCELLATION")
ACTION_TITLES = {
    "HOLD": "Held by the Controller",
    "RETRY_CARD": "Card re-runs to approve",
    "HUMAN_WRITES": "A person writes these (top-50 accounts)",
    "DRAFT_REMINDER": "Drafts awaiting your approval",
    "NO_ACTION": "No action needed",
}
ACTION_HELP = {
    "HOLD": "Nothing goes out until a person releases or overrides the hold. Each hold says which agent raised it and why.",
    "RETRY_CARD": "The card on file has worked since the charge failed, so re-running it should collect the money without emailing anyone. Look at each one and approve it individually (simulated charge: nothing is billed).",
    "HUMAN_WRITES": "Policy: nothing goes to one of the 50 largest accounts without a person reading it first. "
                    "Any draft below is a starting point only.",
    "DRAFT_REMINDER": "Collections drafted these under the collections policy. Edit if you like, then approve. "
                      "Approving marks it sent (simulated: no email leaves this demo).",
    "NO_ACTION": "Not due yet, already paid, or nothing to do this cycle.",
}

RULE_HELP = {
    "auto_apply_exact_ref_match": ("Auto-apply exact matches",
                                   "Cash Application may apply a receipt on its own only when the amount AND the invoice "
                                   "reference match exactly. Everything else waits for a person."),
    "writeoff_threshold": ("Write-off threshold ($)",
                           "Small differences (e.g. bank fees) under this amount may be written off when applying. "
                           "$0 = off until Dana sets it."),
    "amount_tolerance": ("Amount tolerance ($)",
                         "How far a receipt can differ from an invoice and still be proposed as a match."),
    "reminder_days": ("Reminder schedule (days past due)",
                      "When each reminder stage starts. Negative = before the due date. Policy: -5, 7, 21, 45."),
    "top50_human_only": ("Top-50 accounts: a person writes",
                         "When on, the agent never drafts a send-ready email to a top-50 account."),
    "hold_on_open_ticket_days": ("Hold on tickets opened in the last N days",
                                 "An open (or recent) support ticket within this window holds collections."),
    "banned_phrases": ("Banned phrases (one per line)",
                       "The Controller blocks any draft containing these. No threats, no suspension wording."),
    "notify_am_before_contact": ("Tell the account manager first",
                                 "Policy: tell the AM before finance contacts one of their accounts."),
    "fee_tolerance": ("Bank-fee tolerance ($)",
                      "A short payment within this amount is treated as a likely bank fee and proposed as a match "
                      "(still needs a person while the write-off threshold is $0)."),
    "dispute_lookback_days": ("Dispute look-back (days)",
                              "How far back a billing dispute or rewrite complaint still holds collections."),
    "renewal_notice_days": ("Renewal window (days)",
                            "A renewal within this many days counts as 'renewal in flight': tell the AM first."),
    "card_writeoff_warning_days": ("Card write-off warning (days)",
                                   "Warn before a failed card invoice reaches the automatic 150-day write-off."),
    "auto_apply_max_amount": ("Auto-apply limit ($)",
                              "Largest payment Cash Application applies on its own. Larger ones go to Priya even on an "
                              "exact match. Dana to confirm."),
    "use_claude": ("Use Claude for drafts",
                   "When on, Collections asks Claude to write the reminder text (cached). Off = policy templates only."),
}

STAGE_LABELS = {"courtesy": "Courtesy (pre-due)", "first": "1st reminder", "second": "2nd reminder",
                "final": "Final reminder", "escalate": "Escalate", "card_failed": "Card failed", "not_due": "Not due"}


# ------------------------------------------------------------------------------------------------ jinja filters
def _money(v, cents=False):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "-"
    s = "{:,.2f}".format(abs(v)) if cents else "{:,.0f}".format(abs(v))
    return ("-$" if v < 0 else "$") + s


def _pct(v):
    try:
        return "{:.0f}%".format(float(v) * 100)
    except (TypeError, ValueError):
        return "-"


templates.env.filters["money"] = _money
templates.env.filters["money2"] = lambda v: _money(v, cents=True)
templates.env.filters["pct"] = _pct
templates.env.filters["stage"] = lambda s: STAGE_LABELS.get(s, s or "-")
templates.env.filters["humanize"] = lambda s: (s or "").replace("_", " ").capitalize()


# ------------------------------------------------------------------------------------------------ helpers
def _render(request: Request, name: str, ctx: Dict[str, Any], status_code: int = 200):
    base = {
        "user": auth.current_user(request),
        "dev_mode": auth.dev_mode(),
        "engine": st.info(),
        "path": request.url.path,
        "as_of": st.get_state().get("as_of"),
        "ai_on": ai_on(st.get_state()),
        "clock": rig_data.build_clock(),
        "agents_meta": rig_data.AGENTS,
    }
    base.update(ctx)
    return templates.TemplateResponse(request, name, base, status_code=status_code)


def _is_htmx(request: Request) -> bool:
    return bool(request.headers.get("HX-Request"))


def _user(request: Request) -> str:
    u = auth.current_user(request)
    if not u:
        raise HTTPException(401, "login required")
    return u


def _find(items: List[Dict[str, Any]], key: str, value: str) -> Dict[str, Any]:
    for it in items:
        if it.get(key) == value:
            return it
    raise HTTPException(404, "{} {} not found".format(key, value))


def _status(latest: Dict[str, Dict[str, Any]], otype: str, oid: str) -> Optional[Dict[str, Any]]:
    return latest.get(otype + ":" + oid)


def payment_pending(p: Dict[str, Any], latest) -> bool:
    return p["decision"] in ("PROPOSE", "EXCEPTION") and _status(latest, "payment", p["payment_id"]) is None


def invoice_pending(i: Dict[str, Any], latest) -> bool:
    s = _status(latest, "invoice", i["invoice_id"])
    if i["action"] == "NO_ACTION":
        return False
    if s is None:
        return True
    # An overridden/released hold becomes a writing job for a person until it is sent or rejected.
    return s["action"] in ("override_hold", "release_hold", "edit")


def live_counts(state, latest) -> Dict[str, int]:
    inv = state["invoices"]
    return {
        "drafts_pending": sum(1 for i in inv if i["action"] == "DRAFT_REMINDER" and invoice_pending(i, latest)),
        "holds_open": sum(1 for i in inv if i["action"] == "HOLD" and _status(latest, "invoice", i["invoice_id"]) is None),
        "human_pending": sum(1 for i in inv if i["action"] == "HUMAN_WRITES" and invoice_pending(i, latest)),
        "proposals_pending": sum(1 for p in state["payments"] if payment_pending(p, latest)),
        "card_retries_pending": sum(1 for i in inv if i["action"] == "RETRY_CARD" and invoice_pending(i, latest)),
    }


def _one_line(i: Dict[str, Any]) -> str:
    if i.get("holds"):
        h = i["holds"][0]
        more = " (+{} more)".format(len(i["holds"]) - 1) if len(i["holds"]) > 1 else ""
        return "{}: {}{}".format(h.get("label", h.get("code")), h.get("detail", ""), more)
    return " ".join(i.get("reasons") or []) or "-"


def needs_you(state, latest) -> List[Dict[str, Any]]:
    out = []
    for p in state["payments"]:
        if payment_pending(p, latest):
            out.append({"kind": "payment", "id": p["payment_id"], "amount": p["amount"],
                        "customer": p.get("customer_name") or p.get("payer_name"),
                        "customer_id": p.get("customer_id"),
                        "badge": p["decision"], "what": "Confirm cash application" if p["decision"] == "PROPOSE"
                        else "Identify payer", "reason": (p.get("reasons") or ["-"])[-1] if p["decision"] == "EXCEPTION"
                        else " ".join(p.get("reasons") or []), "link": "/cash#" + p["payment_id"]})
    whats = {"HOLD": "Review hold", "HUMAN_WRITES": "Write to customer yourself", "DRAFT_REMINDER": "Approve draft",
             "RETRY_CARD": "Approve card re-run"}
    for i in state["invoices"]:
        if invoice_pending(i, latest):
            s = _status(latest, "invoice", i["invoice_id"])
            what = whats.get(i["action"], i["action"])
            if s and s["action"] in ("override_hold", "release_hold"):
                what = "Hold lifted: write or approve the message"
            out.append({"kind": "invoice", "id": i["invoice_id"], "amount": i["amount"], "customer": i["customer_name"],
                        "customer_id": i["customer_id"], "badge": i["action"], "what": what,
                        "reason": _one_line(i), "link": "/collections#" + i["invoice_id"],
                        "dpd": i.get("days_past_due")})
    out.sort(key=lambda x: -float(x["amount"] or 0))
    return out


def dana_decisions(state) -> List[Dict[str, Any]]:
    out = []
    for i in state["invoices"]:
        hs = [h for h in i.get("holds") or [] if str(h.get("route_to") or "").startswith("Dana")]
        if hs:
            out.append({"i": i, "holds": hs})
    out.sort(key=lambda x: -float(x["i"]["amount"] or 0))
    return out


def ai_on(state) -> bool:
    return bool((state.get("rules") or {}).get("use_claude"))


EMOJI = {":white_check_mark:": "\u2705", ":eyes:": "\U0001F440", ":rotating_light:": "\U0001F6A8",
         ":email:": "\U0001F4E7", ":credit_card:": "\U0001F4B3", ":raised_hand:": "\u270B", ":hand:": "\u270B",
         ":writing_hand:": "\u270D\uFE0F", ":warning:": "\u26A0\uFE0F", ":moneybag:": "\U0001F4B0"}


def slack_to_html(text: str) -> str:
    """Render Slack mrkdwn (*bold*, <url|text>, <url>, :emoji:) to safe HTML."""
    from markupsafe import escape
    parts = []
    pos = 0
    for m in re.finditer(r"<([^<>|\s]+)(?:\|([^<>]+))?>", text):
        parts.append(str(escape(text[pos:m.start()])))
        url, label = m.group(1), m.group(2) or m.group(1)
        if re.match(r"^(https?://|/)", url):
            parts.append('<a href="{}" target="_blank" rel="noopener">{}</a>'.format(escape(url), escape(label)))
        else:
            parts.append(str(escape(m.group(0))))
        pos = m.end()
    parts.append(str(escape(text[pos:])))
    html = "".join(parts)
    html = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<b>\1</b>", html)
    for k, v in EMOJI.items():
        html = html.replace(k, v)
    return html  # newlines kept; the template uses white-space: pre-wrap


def _safe_back(request: Request, default: str = "/") -> str:
    ref = request.headers.get("referer") or ""
    m = re.match(r"^https?://[^/]+(/[^\s]*)$", ref)
    path = m.group(1) if m else default
    return path if path.startswith("/") and not path.startswith("//") else default


# ------------------------------------------------------------------------------------------------ rules form
def _flatten_rules(rules: Dict[str, Any]) -> List[Dict[str, Any]]:
    fields = []
    for key in sorted(rules.keys(), key=lambda k: (list(RULE_HELP.keys()).index(k) if k in RULE_HELP else 99, k)):
        val = rules[key]
        label, help_ = RULE_HELP.get(key, (key.replace("_", " ").capitalize(), ""))
        if isinstance(val, bool):
            kind = "bool"
        elif isinstance(val, (int, float)):
            kind = "number"
        elif isinstance(val, dict) and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in val.values()):
            kind = "numdict"
        elif isinstance(val, list) and all(isinstance(v, str) for v in val):
            kind = "lines"
        elif isinstance(val, str):
            kind = "text"
        else:
            kind = "json"
        fields.append({"key": key, "label": label, "help": help_, "kind": kind, "value": val,
                       "json": json.dumps(val, indent=2) if kind == "json" else None})
    return fields


def _parse_rules(form, current: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    new = copy.deepcopy(current)
    errors = []
    for f in _flatten_rules(current):
        k, kind, old = f["key"], f["kind"], f["value"]
        try:
            if kind == "bool":
                new[k] = form.get(k) in ("on", "true", "1")
            elif kind == "number":
                raw = (form.get(k) or "").strip()
                if raw == "":
                    continue
                new[k] = int(raw) if isinstance(old, int) and re.match(r"^-?\d+$", raw) else float(raw)
            elif kind == "numdict":
                d = dict(old)
                for sub, subold in old.items():
                    raw = (form.get(k + "." + sub) or "").strip()
                    if raw != "":
                        d[sub] = int(raw) if isinstance(subold, int) and re.match(r"^-?\d+$", raw) else float(raw)
                new[k] = d
            elif kind == "lines":
                new[k] = [ln.strip() for ln in (form.get(k) or "").splitlines() if ln.strip()]
            elif kind == "text":
                new[k] = form.get(k, old)
            else:
                new[k] = json.loads(form.get(k) or "null")
        except (ValueError, TypeError) as exc:
            errors.append("{}: {}".format(f["label"], exc))
    if isinstance(new.get("writeoff_threshold"), (int, float)) and new["writeoff_threshold"] < 0:
        errors.append("Write-off threshold cannot be negative.")
    if isinstance(new.get("amount_tolerance"), (int, float)) and new["amount_tolerance"] < 0:
        errors.append("Amount tolerance cannot be negative.")
    return new, errors


def _snapshot(state) -> Dict[str, Any]:
    m = dict(state.get("metrics") or {})
    acts = {}
    for i in state["invoices"]:
        acts[i["action"]] = acts.get(i["action"], 0) + 1
    decs = {}
    for p in state["payments"]:
        decs[p["decision"]] = decs.get(p["decision"], 0) + 1
    return {"metrics": m, "actions": acts, "decisions": decs,
            "inv_action": {i["invoice_id"]: i["action"] for i in state["invoices"]},
            "pay_decision": {p["payment_id"]: p["decision"] for p in state["payments"]}}


def _diff(before, after) -> Dict[str, Any]:
    rows = []
    for group, label in (("metrics", "Metric"), ("actions", "Invoices: "), ("decisions", "Payments: ")):
        keys = sorted(set(before[group]) | set(after[group]))
        for k in keys:
            b, a = before[group].get(k, 0), after[group].get(k, 0)
            if b != a:
                rows.append({"name": (k.replace("_", " ") if group == "metrics" else label + k), "before": b, "after": a})
    moved = []
    for iid, a in after["inv_action"].items():
        b = before["inv_action"].get(iid)
        if b != a:
            moved.append({"id": iid, "kind": "invoice", "before": b or "-", "after": a})
    for pid, a in after["pay_decision"].items():
        b = before["pay_decision"].get(pid)
        if b != a:
            moved.append({"id": pid, "kind": "payment", "before": b or "-", "after": a})
    return {"rows": rows, "moved": moved}


# ------------------------------------------------------------------------------------------------ video embed
EMBED_HOSTS = ("loom.com", "youtube.com", "youtu.be", "youtube-nocookie.com", "drive.google.com")


def embed_url(url: str) -> str:
    url = url.strip()
    m = re.search(r"loom\.com/(?:share|embed)/([A-Za-z0-9]+)", url)
    if m:
        return "https://www.loom.com/embed/" + m.group(1)
    m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]+)", url)
    if m:
        return "https://www.youtube.com/embed/" + m.group(1)
    m = re.search(r"drive\.google\.com/file/d/([A-Za-z0-9_-]+)", url)
    if m:
        return "https://drive.google.com/file/d/{}/preview".format(m.group(1))
    return url


def demo_video_url() -> str:
    return (store.get_setting("demo_video_url") or os.environ.get("DEMO_VIDEO_URL", "")).strip()


def valid_video_url(url: str) -> bool:
    m = re.match(r"^https://([^/\s]+)/\S*$", url.strip())
    if not m:
        return False
    host = m.group(1).lower()
    return any(host == h or host.endswith("." + h) for h in EMBED_HOSTS)


# ------------------------------------------------------------------------------------------------ routes
def build_router() -> APIRouter:
    r = APIRouter()

    # ---------------- Today
    @r.get("/today", response_class=HTMLResponse)
    async def today(request: Request):
        state = st.get_state()
        latest = store.latest_by_object()
        items = needs_you(state, latest)
        m = state["metrics"]
        customers = state.get("customers") or {}
        strip = [
            {"name": "Cash Application", "does": "Matches unapplied receipts to open invoices. Applies exact amount + "
             "invoice-reference matches on its own; proposes everything else.",
             "counts": ["{} auto-applied".format(m.get("auto_applied", 0)),
                        "{} for review".format(m.get("needs_review", 0)),
                        "{} cash found".format(_money(m.get("cash_found", 0)))]},
            {"name": "Account Context", "does": "Builds a 360 of each customer: tickets, NPS, usage, contract, renewal, "
             "contacts. Read only.",
             "counts": ["{} customers profiled".format(len(customers)),
                        "{} with billing complaints".format(sum(1 for c in customers.values() if c.get("billing_complaint"))),
                        "{} unverified contacts".format(sum(1 for c in customers.values() for x in c.get("contacts", [])
                                                            if not x.get("verified")))]},
            {"name": "Controller", "does": "Guardrails. Holds anything that shouldn't go out: money already received, "
             "open complaint, rewrite dispute, renewal in flight, unverified contact, banned wording.",
             "counts": ["{} invoices held".format(m.get("held", 0)),
                        "{} chases prevented".format(m.get("chases_prevented", 0))]},
            {"name": "Collections", "does": "Ranks overdue AR, picks stage and tone under the collections policy, drafts "
             "the reminder. Never sends.",
             "counts": ["{} drafts".format(m.get("drafts", 0)),
                        "{} card re-runs".format(m.get("card_retries", 0)),
                        "{} for a person to write".format(m.get("human_writes", 0))]},
        ]
        return _render(request, "today.html", {"m": m, "items": items[:40], "n_items": len(items),
                                               "items_total": sum(float(x["amount"] or 0) for x in items),
                                               "live": live_counts(state, latest), "strip": strip,
                                               "dana": dana_decisions(state)})

    @r.post("/run")
    async def run_agents(request: Request):
        _user(request)
        st.refresh()
        return RedirectResponse(_safe_back(request), status_code=303)

    # ---------------- Cash application
    @r.get("/cash", response_class=HTMLResponse)
    async def cash(request: Request, show: str = "all"):
        state = st.get_state()
        latest = store.latest_by_object()
        order = {"EXCEPTION": 0, "PROPOSE": 1, "AUTO_APPLY": 2}
        pays = sorted(state["payments"], key=lambda p: (order.get(p["decision"], 3), -float(p["amount"] or 0)))
        if show != "all":
            pays = [p for p in pays if p["decision"] == show]
        counts = {}
        for p in state["payments"]:
            counts[p["decision"]] = counts.get(p["decision"], 0) + 1
        return _render(request, "cash.html", {"payments": pays, "latest": latest, "show": show, "counts": counts,
                                              "invoices": {i["invoice_id"]: i for i in state["invoices"]}})

    def _payment_response(request: Request, pid: str):
        state = st.get_state()
        p = _find(state["payments"], "payment_id", pid)
        if _is_htmx(request):
            return templates.TemplateResponse(request, "_payment.html", {
                "p": p, "latest": store.latest_by_object(), "open": True,
                "invoices": {i["invoice_id"]: i for i in state["invoices"]}})
        return RedirectResponse("/cash#" + pid, status_code=303)

    @r.post("/cash/{pid}/approve")
    async def cash_approve(request: Request, pid: str, note: str = Form("")):
        p = _find(st.get_state()["payments"], "payment_id", pid)
        store.record(_user(request), "payment", pid, "apply",
                     note or "Approved application (simulated ledger write).",
                     {"invoice_ids": p["invoice_ids"], "amount": p["amount"], "difference": p.get("difference"),
                      "agent_decision": p["decision"], "agent_confidence": p.get("confidence")})
        return _payment_response(request, pid)

    @r.post("/cash/{pid}/reject")
    async def cash_reject(request: Request, pid: str, note: str = Form("")):
        p = _find(st.get_state()["payments"], "payment_id", pid)
        store.record(_user(request), "payment", pid, "reject", note or "Rejected proposed match.",
                     {"invoice_ids": p["invoice_ids"], "agent_decision": p["decision"]})
        return _payment_response(request, pid)

    @r.post("/cash/{pid}/undo")
    async def cash_undo(request: Request, pid: str, note: str = Form("")):
        p = _find(st.get_state()["payments"], "payment_id", pid)
        store.record(_user(request), "payment", pid, "reject",
                     note or "Undid the agent's auto-application (simulated ledger reversal).",
                     {"undo": True, "invoice_ids": p["invoice_ids"], "agent_decision": p["decision"]})
        return _payment_response(request, pid)

    # ---------------- Collections
    @r.get("/collections", response_class=HTMLResponse)
    async def collections(request: Request, q: str = ""):
        state = st.get_state()
        latest = store.latest_by_object()
        invs = state["invoices"]
        if q:
            ql = q.lower()
            invs = [i for i in invs if ql in i["invoice_id"].lower() or ql in (i.get("customer_name") or "").lower()]
        groups = []
        for a in ACTION_ORDER:
            rows = sorted([i for i in invs if i["action"] == a], key=lambda i: -float(i["amount"] or 0))
            groups.append({"action": a, "title": ACTION_TITLES[a], "help": ACTION_HELP[a], "rows": rows,
                           "total": sum(float(i["amount"] or 0) for i in rows)})
        return _render(request, "collections.html", {"groups": groups, "latest": latest, "q": q,
                                                     "customers": state.get("customers") or {}})

    def _invoice_response(request: Request, iid: str):
        state = st.get_state()
        i = _find(state["invoices"], "invoice_id", iid)
        if _is_htmx(request):
            return templates.TemplateResponse(request, "_invoice.html", {
                "i": i, "latest": store.latest_by_object(), "open": True,
                "customers": state.get("customers") or {}})
        return RedirectResponse("/collections#" + iid, status_code=303)

    @r.post("/collections/{iid}/send")
    async def inv_send(request: Request, iid: str, subject: str = Form(""), body: str = Form(""),
                       to: str = Form(""), note: str = Form("")):
        user = _user(request)
        i = _find(st.get_state()["invoices"], "invoice_id", iid)
        d = i.get("draft") or {}
        if not body.strip():
            raise HTTPException(400, "The email body is empty.")
        banned = [b for b in (st.get_state().get("rules") or {}).get("banned_phrases", [])
                  if b and b.lower() in (subject + "\n" + body).lower()]
        if banned:
            raise HTTPException(400, "Blocked by the Controller: the email contains banned wording: " + ", ".join(banned))
        edited = (subject.strip() != (d.get("subject") or "").strip()) or (body.strip() != (d.get("body") or "").strip())
        payload = {"to": [x.strip() for x in to.split(",") if x.strip()] or d.get("to", []), "cc": d.get("cc", []),
                   "subject": subject, "body": body, "template": d.get("template"), "source": d.get("source"),
                   "edited": edited, "agent_action": i["action"]}
        if edited and d:
            store.record(user, "invoice", iid, "edit", "Edited the agent's draft before approving.",
                         {"before": {"subject": d.get("subject"), "body": d.get("body")},
                          "after": {"subject": subject, "body": body}})
        store.record(user, "invoice", iid, "send",
                     note or "Approved & marked sent (simulated: no email leaves this demo).", payload)
        return _invoice_response(request, iid)

    @r.post("/collections/{iid}/reject")
    async def inv_reject(request: Request, iid: str, note: str = Form("")):
        i = _find(st.get_state()["invoices"], "invoice_id", iid)
        store.record(_user(request), "invoice", iid, "reject", note or "Rejected the draft. Nothing sent.",
                     {"agent_action": i["action"]})
        return _invoice_response(request, iid)

    @r.post("/collections/{iid}/hold")
    async def inv_hold(request: Request, iid: str, reason: str = Form(""), kind: str = Form("override_hold"),
                       am_confirmed: str = Form(""), am_name: str = Form("")):
        i = _find(st.get_state()["invoices"], "invoice_id", iid)
        if kind not in ("override_hold", "release_hold"):
            raise HTTPException(400, "bad kind")
        if len(reason.strip()) < 5:
            raise HTTPException(400, "Type a reason (at least a few words) to lift a hold.")
        holds = i.get("holds") or []
        payload = {"holds": [h.get("code") for h in holds], "agent_action": i["action"],
                   "route_to": [h.get("route_to") for h in holds if h.get("route_to")]}
        needs_am = [h for h in holds if h.get("code") in RELEASE_NEEDS_AM]
        if kind == "release_hold" and needs_am:
            if am_confirmed not in ("on", "true", "1") or len(am_name.strip()) < 2:
                raise HTTPException(400, "Releasing a dispute or cancellation hold needs the box 'Account manager "
                                         "confirmed the dispute is settled' ticked and the account manager's name.")
            payload.update({"am_confirmed": True, "am_name": am_name.strip(),
                            "release_requires": [h.get("release_requires") for h in needs_am if h.get("release_requires")]})
        store.record(_user(request), "invoice", iid, kind, reason.strip(), payload)
        return _invoice_response(request, iid)

    @r.post("/collections/{iid}/card_retry")
    async def inv_card_retry(request: Request, iid: str, decision: str = Form(""), note: str = Form("")):
        i = _find(st.get_state()["invoices"], "invoice_id", iid)
        if i["action"] != "RETRY_CARD":
            raise HTTPException(400, "This invoice is not a card re-run.")
        if decision not in ("approve", "reject"):
            raise HTTPException(400, "bad decision")
        default = ("Approved card re-run (simulated charge: nothing is billed from this demo)." if decision == "approve"
                   else "Rejected card re-run. Not charged.")
        store.record(_user(request), "invoice", iid, decision, note.strip() or default,
                     {"kind": "card_retry", "retry": i.get("retry"), "amount": i["amount"]})
        return _invoice_response(request, iid)

    # ---------------- Customers
    @r.get("/customers", response_class=HTMLResponse)
    async def customers(request: Request, q: str = "", all: int = 0):
        state = st.get_state()
        inv_by_id = {i["invoice_id"]: i for i in state["invoices"]}
        rows = []
        for c in (state.get("customers") or {}).values():
            open_ids = c.get("open_invoices") or []
            if not all and not open_ids:
                continue
            if q and q.lower() not in (c.get("name") or "").lower() and q.lower() not in c["customer_id"].lower():
                continue
            invs = [inv_by_id[x] for x in open_ids if x in inv_by_id]
            rows.append({"c": c, "open_ar": sum(float(i["amount"] or 0) for i in invs),
                         "overdue": sum(float(i["amount"] or 0) for i in invs if (i.get("days_past_due") or 0) > 0),
                         "max_dpd": max([i.get("days_past_due") or 0 for i in invs] or [0]),
                         "held": sum(1 for i in invs if i["action"] == "HOLD")})
        rows.sort(key=lambda x: -x["open_ar"])
        ctx = {"rows": rows, "q": q, "all": all}
        if _is_htmx(request) and request.headers.get("HX-Target") == "cust-rows":
            return templates.TemplateResponse(request, "_customer_rows.html", ctx)
        return _render(request, "customers.html", ctx)

    @r.get("/customers/{cid}", response_class=HTMLResponse)
    async def customer(request: Request, cid: str):
        state = st.get_state()
        c = (state.get("customers") or {}).get(cid)
        if not c:
            raise HTTPException(404, "customer not found")
        invs = [i for i in state["invoices"] if i["customer_id"] == cid]
        pays = [p for p in state["payments"] if p.get("customer_id") == cid]
        audit = [a for a in state.get("audit", []) if a.get("object_id") in
                 ({cid} | {i["invoice_id"] for i in invs} | {p["payment_id"] for p in pays})]
        return _render(request, "customer.html", {"c": c, "invoices": invs, "payments": pays,
                                                  "latest": store.latest_by_object(), "audit": audit[-30:]})

    # ---------------- Audit
    def _audit_rows(state, agent: str = "", q: str = "") -> List[Dict[str, Any]]:
        rows = []
        for a in state.get("audit", []):
            rows.append({"ts": a.get("ts", ""), "who": a.get("agent", ""), "kind": "agent",
                         "object_type": a.get("object_type", ""), "object_id": a.get("object_id", ""),
                         "decision": a.get("decision", ""), "confidence": a.get("confidence"),
                         "reason": a.get("reason", "")})
        for h in store.all_actions():
            rows.append({"ts": h["ts"], "who": "Human: " + h["user_email"], "kind": "human",
                         "object_type": h["object_type"], "object_id": h["object_id"],
                         "decision": h["action"], "confidence": None, "reason": h.get("note") or "",
                         "payload": h.get("payload")})
        if agent == "Human":
            rows = [x for x in rows if x["kind"] == "human"]
        elif agent:
            rows = [x for x in rows if x["who"] == agent]
        if q:
            ql = q.lower()
            rows = [x for x in rows if ql in (x["object_id"] or "").lower() or ql in (x["reason"] or "").lower()
                    or ql in (x["decision"] or "").lower()]
        rows.sort(key=lambda x: str(x["ts"]), reverse=True)
        return rows

    @r.get("/audit", response_class=HTMLResponse)
    async def audit(request: Request, agent: str = "", q: str = "", limit: int = 500):
        state = st.get_state()
        rows = _audit_rows(state, agent, q)
        agents = sorted({a.get("agent", "") for a in state.get("audit", [])} | set(AGENTS))
        return _render(request, "audit.html", {"rows": rows[:limit], "n": len(rows), "agent": agent, "q": q,
                                               "agents": agents + ["Human"], "limit": limit})

    @r.get("/audit.csv")
    async def audit_csv(request: Request, agent: str = "", q: str = ""):
        rows = _audit_rows(st.get_state(), agent, q)
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["ts", "who", "object_type", "object_id", "decision", "confidence", "reason", "payload"])
        for x in rows:
            w.writerow([x["ts"], x["who"], x["object_type"], x["object_id"], x["decision"],
                        "" if x["confidence"] is None else x["confidence"], x["reason"],
                        json.dumps(x.get("payload")) if x.get("payload") else ""])
        return Response(buf.getvalue(), media_type="text/csv",
                        headers={"Content-Disposition": "attachment; filename=ledgerline_audit.csv"})

    # ---------------- Rules
    @r.get("/rules", response_class=HTMLResponse)
    async def rules_page(request: Request):
        rules = st.load_rules()
        changes = [a for a in store.all_actions() if a["object_type"] == "rules"][-10:][::-1]
        return _render(request, "rules.html", {"fields": _flatten_rules(rules), "result": None, "errors": [],
                                               "history": changes})

    @r.post("/rules", response_class=HTMLResponse)
    async def rules_save(request: Request):
        user = _user(request)
        form = await request.form()
        current = st.load_rules()
        new, errors = _parse_rules(form, current)
        history = [a for a in store.all_actions() if a["object_type"] == "rules"][-10:][::-1]
        if errors:
            return _render(request, "rules.html", {"fields": _flatten_rules(new), "result": None, "errors": errors,
                                                   "history": history}, status_code=400)
        changed = {k: {"before": current.get(k), "after": new.get(k)} for k in new if new.get(k) != current.get(k)}
        before = _snapshot(st.get_state())
        if changed:
            st.save_rules(new)
        after_state = st.refresh()
        result = _diff(before, _snapshot(after_state))
        result["changed"] = changed
        if changed:
            note = (form.get("note") or "").strip() or "Changed " + ", ".join(sorted(changed))
            store.record(user, "rules", "rules", "edit", note,
                         {"changed": changed, "impact": result["rows"], "moved": result["moved"][:50]})
            history = [a for a in store.all_actions() if a["object_type"] == "rules"][-10:][::-1]
        return _render(request, "rules.html", {"fields": _flatten_rules(st.load_rules()), "result": result,
                                               "errors": [], "history": history})

    # ---------------- Morning digest
    @r.get("/digest", response_class=HTMLResponse)
    async def digest(request: Request):
        state = st.get_state()
        text, error = None, None
        try:
            from app.engine.digest import build_digest
            base = os.environ.get("BASE_URL", "").rstrip("/") or str(request.base_url).rstrip("/")
            text = build_digest(state, base_url=base)
        except Exception as exc:
            error = "{}: {}".format(type(exc).__name__, exc)
        return _render(request, "digest.html", {"html": slack_to_html(text) if text else None, "raw": text,
                                                "error": error})

    # ---------------- About
    @r.get("/about", response_class=HTMLResponse)
    async def about(request: Request):
        html = None
        if os.path.exists(ONE_PAGER):
            import markdown
            with open(ONE_PAGER, encoding="utf-8") as f:
                html = markdown.markdown(f.read(), extensions=["tables", "fenced_code", "sane_lists"])
        video = demo_video_url()
        return _render(request, "about.html", {"html": html, "video": embed_url(video) if video else None})

    return r
