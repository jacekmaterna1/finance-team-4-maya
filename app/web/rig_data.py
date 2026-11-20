"""Data helpers for the RIG (command center): agent roster, manuals, Maya thread, activity feed, build clock."""
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from app import store

WEB_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(WEB_DIR))
MANUALS_DIR = os.environ.get("MANUALS_DIR", os.path.join(ROOT_DIR, "app", "engine", "manuals"))
STANDING = "## Standing instructions from humans"

# Timer started 2026-11-20 11:10 America/Chicago (CST = UTC-6 in November).
BUILD_START = datetime(2026, 11, 20, 17, 10, tzinfo=timezone.utc)

AGENTS: List[Dict[str, Any]] = [
    {
        "slug": "cash", "name": "Cash Application", "manual": "cash_application", "step": 1,
        "kicker": "AGENT 01 · FIN-2",
        "desc": "Matches unapplied bank and card receipts to open invoices, first, so we never chase money we have.",
        "owns": "Unapplied receipts in payments.csv (no invoice id) and the match to an open invoice.",
        "inputs": ["Bank + Stripe receipts (payer, amount, memo)", "Open invoices and AR aging", "Customer names"],
        "outputs": ["AUTO_APPLY (exact amount + invoice reference)", "PROPOSE with reasons", "EXCEPTION (cannot identify)",
                    "'Money already received' hold for the Controller"],
        "alone": ["Apply a receipt when amount AND invoice reference both match exactly, up to the auto-apply cap "
                  "($10,000, Dana to confirm)"],
        "ask": ["Any match without a reference", "Exact matches above the $10,000 auto-apply cap",
                "Ambiguous matches (same amount, several invoices)",
                "Short payments, bank fees, write-offs (threshold $0 until Dana sets it)"],
    },
    {
        "slug": "context", "name": "Account Context", "manual": "account_context", "step": 2,
        "kicker": "AGENT 02 · READ-ONLY",
        "desc": "One view of each customer: tickets, NPS, usage, contract, renewal, contacts. Finance can't see Zendesk today.",
        "owns": "The customer 360 and the reading of support-ticket text (disputes, cancellations, legal threats).",
        "inputs": ["Zendesk tickets", "HubSpot customers + contacts", "Contracts, renewal dates", "Product usage, NPS"],
        "outputs": ["Customer 360", "Dispute / cancellation / legal-threat findings", "Contact verification issues"],
        "alone": ["Read and summarise. It never acts."],
        "ask": ["Nothing: it only informs the Controller and the humans"],
    },
    {
        "slug": "controller", "name": "Controller", "manual": "controller", "step": 3,
        "kicker": "AGENT 03 · GUARDRAILS",
        "desc": "Holds anything that must not go out and routes it to the right person: AM, Priya or Dana.",
        "owns": "Holds and blocks: already paid, dispute, cancellation, escalation, renewal, contact, top-50, 90+ days, wording.",
        "inputs": ["Cash Application matches", "Account Context findings", "Collections policy", "Rules page thresholds"],
        "outputs": ["HOLD with code, reason and route_to", "HUMAN_WRITES for top-50", "Blocked wording"],
        "alone": ["Hold or block"],
        "ask": ["Releasing any hold (disputes need the AM's confirmation)"],
    },
    {
        "slug": "collections", "name": "Collections", "manual": "collections", "step": 4,
        "kicker": "AGENT 04 · FIN-1",
        "desc": "Ranks overdue AR, picks the policy stage and tone, drafts reminders and card re-runs. Never sends.",
        "owns": "Stage, tone and the draft reminder for each unpaid invoice; failed-card follow-up.",
        "inputs": ["Open invoices after Cash Application + Controller", "Collections policy + templates", "Contacts"],
        "outputs": ["DRAFT_REMINDER", "RETRY_CARD proposals", "Morning digest for Priya"],
        "alone": ["Draft and queue"],
        "ask": ["Every send", "Every card re-run (Priya approves each one)"],
    },
]
AGENT_BY_SLUG = {a["slug"]: a for a in AGENTS}
AGENT_BY_NAME = {a["name"]: a for a in AGENTS}

HUMANS = [
    {"name": "Priya Nair", "role": "AR Specialist", "does": "Runs it every morning. Approves applications, drafts and card re-runs; releases holds; edits rules."},
    {"name": "Dana Ruiz", "role": "VP Finance", "does": "Owns thresholds, write-offs (up to $2,000), payment plans and the card re-run policy. Gets 'decisions for Dana'."},
    {"name": "Account managers", "role": "Nadia Sinclair · Nadia Upton · Maria Yardley · Hannah Drummond", "does": "Own disputes and the relationship. A dispute hold is released only when the AM confirms it is settled."},
    {"name": "Maya Lindqvist", "role": "COO · sponsor", "does": "Sets the guardrails. Her test: is Priya still using it in a month?"},
]


def hold_override_rate() -> Dict[str, Any]:
    """Human override_hold actions / holds reviewed (override + release). Over-holding is the right way to be wrong."""
    acts = [a for a in store.all_actions() if a["object_type"] == "invoice" and a["action"] in ("override_hold", "release_hold")]
    n_over = sum(1 for a in acts if a["action"] == "override_hold")
    n = len(acts)
    return {"overrides": n_over, "reviewed": n, "rate": (n_over / n) if n else None,
            "label": "{:.0f}%".format(100.0 * n_over / n) if n else "no reviews yet",
            "detail": "{} overridden of {} holds reviewed".format(n_over, n) if n else "0 of 0 holds reviewed"}


MISSION = {
    "title": "An Order-to-Cash team for Dana Ruiz (VP Finance)",
    "body": "Collections (FIN-1), plus Cash Application (FIN-2), which feeds it. Customers get chased for invoices "
            "they've already paid because matching payments lags 3–5 days. They also get chased while they have an "
            "open support complaint, because finance can't see support tickets.",
    "promises": ["Never chase money we already have", "Never chase a customer mid-dispute",
                 "A person approves everything that reaches a customer or the ledger"],
}

# "Where we are" track on HOME and TEAM. status: done | current | next. Edit freely.
PROGRESS = [
    ("done", "Chose the process with Maya", "T+0:05"),
    ("done", "Four agents live on real records", "T+0:12"),
    ("done", "Maya approved rules-only go-live with Priya on Monday", "T+0:32"),
    ("done", "Data-room QA: AR ties out, 14 disputes verified against contracts", "T+0:36"),
    ("current", "RIG live on Render for review", "now"),
    ("next", "Monday: Priya walkthrough, Dana decisions, Legal reviews Bedrock note", "Mon"),
    ("next", "+30 days: hold-override rate back to Maya", "+30d"),
]

GO_LIVE = [
    (False, "Dana reviews the Northgate decision ($799, automatic write-off)"),
    (False, "Dana confirms the auto-apply rule (exact amount + invoice reference) and the write-off threshold ($0)"),
    (False, "30-minute walkthrough with Priya (why Reyes was held; how to override or release a hold)"),
    (False, "Engineering fills in the AWS region in the Legal note"),
    (False, "Legal reviews the Bedrock note (ticket text can still name people)"),
    (True, "Rules-only mode, AI off"),
    (True, "Every match, hold release and email needs Priya"),
]


def build_clock() -> str:
    d = datetime.now(timezone.utc) - BUILD_START
    if d.total_seconds() < 0:
        d = timedelta(0)
    mins = int(d.total_seconds() // 60)
    return "T+{}:{:02d}".format(mins // 60, mins % 60)


# ------------------------------------------------------------------ manuals
def manual_path(agent: Dict[str, Any]) -> str:
    return os.path.join(MANUALS_DIR, agent["manual"] + ".md")


def read_manual(agent: Dict[str, Any]) -> str:
    try:
        with open(manual_path(agent), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def write_manual(agent: Dict[str, Any], text: str) -> None:
    os.makedirs(MANUALS_DIR, exist_ok=True)
    with open(manual_path(agent), "w", encoding="utf-8") as f:
        f.write(text.replace("\r\n", "\n"))


def append_standing_instruction(agent: Dict[str, Any], line: str) -> None:
    text = read_manual(agent).rstrip("\n")
    if STANDING not in text:
        text += "\n\n" + STANDING + "\n"
    text += "\n- " + line.strip()
    write_manual(agent, text + "\n")


# ------------------------------------------------------------------ markdown files
def md(text: str) -> str:
    import markdown
    return markdown.markdown(text or "", extensions=["tables", "fenced_code", "sane_lists"])


def read_rel(rel: str) -> Optional[str]:
    p = os.path.join(ROOT_DIR, rel)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------------ Maya thread
_SPEAKER = re.compile(r"^\*\*([^*]{1,80}?):\*\*\s*(.*)$", re.S)
_CHANGED = re.compile(r"^\*\*What we changed because of it:?\*\*:?\s*(.*)$", re.S | re.I)


def parse_maya() -> Dict[str, Any]:
    raw = read_rel("trail/MAYA_QA.md") or ""
    out: Dict[str, Any] = {"exchanges": [], "raw_html": md(raw), "ok": False}
    log = raw.split("## Log", 1)[1] if "## Log" in raw else raw
    parts = re.split(r"^###\s+", log, flags=re.M)
    for part in parts[1:]:
        title, _, body = part.partition("\n")
        ex: Dict[str, Any] = {"title": title.strip(), "items": []}
        mode = None
        for block in re.split(r"\n\s*\n", body.strip()):
            block = block.strip()
            if not block:
                continue
            m = _CHANGED.match(block)
            if m:
                ex["items"].append({"kind": "changes", "html_src": m.group(1).strip()})
                mode = "changes"
                continue
            m = _SPEAKER.match(block)
            if m:
                speaker = m.group(1).strip()
                side = "maya" if speaker.lower().startswith("maya") else "team"
                ex["items"].append({"kind": "msg", "side": side, "speaker": speaker if side == "maya" else
                                    ("Jacek / team" + ("" if speaker.lower() == "jacek" else " · " + speaker)),
                                    "html_src": m.group(2).strip()})
                mode = None
                continue
            if mode == "changes":
                ex["items"][-1]["html_src"] += "\n\n" + block
            else:
                ex["items"].append({"kind": "meta", "html_src": block})
        for it in ex["items"]:
            it["html"] = md(it.pop("html_src"))
        if any(it["kind"] == "msg" for it in ex["items"]):
            out["exchanges"].append(ex)
    out["ok"] = bool(out["exchanges"])
    # budget + pending drafts from the outbox
    ob = read_rel("trail/MAYA_OUTBOX.md") or ""
    m = re.search(r"Messages used:\s*\**\s*(\d+)\s*of\s*(\d+)", ob, re.I)
    out["used"], out["budget"] = (int(m.group(1)), int(m.group(2))) if m else (None, 60)
    if out["used"] is None:
        out["used"] = sum(1 for ex in out["exchanges"] for it in ex["items"]
                          if it["kind"] == "msg" and it["side"] == "team")
    drafts = []
    for sec in re.split(r"^##\s+", ob, flags=re.M)[1:]:
        head, _, body = sec.partition("\n")
        hu = head.upper()
        if "SENT" in hu or not ("READY" in hu or "QUEUED" in hu):
            continue
        pm = re.search(r"^\W*Purpose\W*:?\**\s*(.+)$", body, re.M | re.I)
        purpose = pm.group(1).strip() if pm else ""
        kind = "Confirmation" if "confirm" in purpose.lower() else ("Intel" if "intel" in purpose.lower() else "")
        drafts.append({"title": head.strip(), "purpose": purpose, "kind": kind, "html": md(body.strip())})
    out["drafts"] = drafts
    out["outbox_html"] = md(ob) if ob else None
    return out


def latest_maya() -> Optional[Dict[str, Any]]:
    t = parse_maya()
    for ex in reversed(t["exchanges"]):
        msgs = [it for it in ex["items"] if it["kind"] == "msg" and it["side"] == "maya"]
        if msgs:
            return {"title": ex["title"], "html": msgs[-1]["html"],
                    "changes": next((it["html"] for it in ex["items"] if it["kind"] == "changes"), None)}
    return None


# ------------------------------------------------------------------ activity feed
def activity(state: Dict[str, Any], who: str = "", q: str = "", limit: int = 300) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    run_ts = state.get("run_ts")
    for a in state.get("audit", []):
        rows.append({"ts": a.get("ts", ""), "run_ts": run_ts, "who": a.get("agent", ""), "kind": "agent", "title": "{} {} → {}".format(
            a.get("object_type", ""), a.get("object_id", ""), a.get("decision", "")),
            "text": a.get("reason", ""), "confidence": a.get("confidence"), "object_id": a.get("object_id", ""),
            "object_type": a.get("object_type", "")})
    for h in store.all_actions():
        rows.append({"ts": h["ts"], "who": h["user_email"], "kind": "human",
                     "title": "{} {} {}".format(h["action"].replace("_", " "), h["object_type"], h["object_id"]),
                     "text": h.get("note") or "", "confidence": None, "object_id": h["object_id"],
                     "object_type": h["object_type"]})
    for i in store.instructions():
        rows.append({"ts": i["ts"], "who": i["user"], "kind": "instruction",
                     "title": "Instruction to {} ({})".format(i["agent"], i["status"]), "text": i["text"],
                     "confidence": None, "object_id": str(i["id"]), "object_type": "instruction", "agent": i["agent"]})
    for c in store.chats():
        rows.append({"ts": c["ts"], "who": c["user"], "kind": "chat",
                     "title": "Chat with {} ({})".format(c.get("agent") or "team", c.get("mode") or "rules"),
                     "text": "Q: {}  ·  A: {}".format(c["message"], (c.get("reply") or "")[:240]),
                     "confidence": None, "object_id": str(c["id"]), "object_type": "chat"})
    if who == "Humans":
        rows = [r for r in rows if r["kind"] != "agent"]
    elif who:
        rows = [r for r in rows if r["who"] == who or r.get("agent") == who]
    if q:
        ql = q.lower()
        rows = [r for r in rows if ql in (r["title"] + " " + r["text"] + " " + r["who"]).lower()]
    rows.sort(key=lambda r: (str(r.get("run_ts") or r["ts"])[:19], str(r["ts"])), reverse=True)
    return rows[:limit]
