"""Append-only store of human actions (approve, reject, edit, override_hold, release_hold, send, apply).

Nothing here sends email or writes to a ledger: every action is a simulated record that shows up in the audit trail.
Rows are never updated or deleted; the latest row for an object is its current human status.
"""
import json
import os
import sqlite3
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

ACTIONS = ("approve", "reject", "edit", "override_hold", "release_hold", "send", "apply", "reply", "resolve")
# object_type values in use: payment, invoice, rules, instruction, manual

_lock = threading.Lock()


def db_path() -> str:
    return os.environ.get("DB_PATH", os.path.join(os.getcwd(), "ledgerline.db"))


def _connect() -> sqlite3.Connection:
    path = db_path()
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _lock, _connect() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS actions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ts TEXT NOT NULL,
                   user_email TEXT NOT NULL,
                   object_type TEXT NOT NULL,
                   object_id TEXT NOT NULL,
                   action TEXT NOT NULL,
                   note TEXT,
                   payload_json TEXT
               )""")
        conn.execute("CREATE INDEX IF NOT EXISTS ix_actions_obj ON actions(object_type, object_id)")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS instructions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ts TEXT NOT NULL,
                   user TEXT NOT NULL,
                   agent TEXT NOT NULL,
                   text TEXT NOT NULL,
                   status TEXT NOT NULL DEFAULT 'proposed',
                   decided_by TEXT,
                   decided_ts TEXT,
                   source TEXT
               )""")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS maya_questions (
                   id TEXT PRIMARY KEY, created_ts TEXT, purpose TEXT, owner TEXT, topic TEXT, text TEXT, why TEXT,
                   changes TEXT, invoices_json TEXT, status TEXT NOT NULL DEFAULT 'proposed', edited_text TEXT,
                   approved_by TEXT, approved_ts TEXT, sent_ts TEXT, sent_message TEXT, reply TEXT, reply_ts TEXT,
                   outcome TEXT, updated_ts TEXT
               )""")
        conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT, ts TEXT, user TEXT)")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS chat (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ts TEXT NOT NULL,
                   user TEXT NOT NULL,
                   agent TEXT,
                   message TEXT NOT NULL,
                   reply TEXT,
                   mode TEXT
               )""")


def record(user_email: str, object_type: str, object_id: str, action: str, note: str = "",
           payload: Optional[Dict[str, Any]] = None) -> int:
    if action not in ACTIONS:
        raise ValueError("unknown action " + action)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with _lock, _connect() as conn:
        cur = conn.execute(
            "INSERT INTO actions (ts, user_email, object_type, object_id, action, note, payload_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (ts, user_email, object_type, object_id, action, note or "", json.dumps(payload or {}, default=str)))
        return int(cur.lastrowid)


def _row(r: sqlite3.Row) -> Dict[str, Any]:
    d = dict(r)
    try:
        d["payload"] = json.loads(d.get("payload_json") or "{}")
    except ValueError:
        d["payload"] = {}
    return d


def all_actions() -> List[Dict[str, Any]]:
    with _connect() as conn:
        return [_row(r) for r in conn.execute("SELECT * FROM actions ORDER BY id")]


def latest_by_object() -> Dict[str, Dict[str, Any]]:
    """Map 'object_type:object_id' -> latest action row."""
    out: Dict[str, Dict[str, Any]] = {}
    for a in all_actions():
        out[a["object_type"] + ":" + a["object_id"]] = a
    return out


def history(object_type: str, object_id: str) -> List[Dict[str, Any]]:
    with _connect() as conn:
        return [_row(r) for r in conn.execute(
            "SELECT * FROM actions WHERE object_type = ? AND object_id = ? ORDER BY id", (object_type, object_id))]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------ instructions (humans -> agents)
INSTRUCTION_STATUSES = ("proposed", "accepted", "rejected")


def add_instruction(user: str, agent: str, text: str, source: str = "form") -> int:
    with _lock, _connect() as conn:
        cur = conn.execute("INSERT INTO instructions (ts, user, agent, text, status, source) VALUES (?, ?, ?, ?, ?, ?)",
                           (_now(), user, agent, text.strip(), "proposed", source))
        return int(cur.lastrowid)


def instructions(agent: Optional[str] = None) -> List[Dict[str, Any]]:
    with _connect() as conn:
        if agent:
            rows = conn.execute("SELECT * FROM instructions WHERE agent = ? ORDER BY id DESC", (agent,))
        else:
            rows = conn.execute("SELECT * FROM instructions ORDER BY id DESC")
        return [dict(r) for r in rows]


def get_instruction(iid: int) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        r = conn.execute("SELECT * FROM instructions WHERE id = ?", (iid,)).fetchone()
        return dict(r) if r else None


def decide_instruction(iid: int, status: str, user: str) -> None:
    if status not in INSTRUCTION_STATUSES:
        raise ValueError(status)
    with _lock, _connect() as conn:
        conn.execute("UPDATE instructions SET status = ?, decided_by = ?, decided_ts = ? WHERE id = ?",
                     (status, user, _now(), iid))


# ------------------------------------------------------------------ chat turns
def add_chat(user: str, agent: str, message: str, reply: str, mode: str) -> int:
    with _lock, _connect() as conn:
        cur = conn.execute("INSERT INTO chat (ts, user, agent, message, reply, mode) VALUES (?, ?, ?, ?, ?, ?)",
                           (_now(), user, agent, message, reply, mode))
        return int(cur.lastrowid)


def chats(limit: int = 500) -> List[Dict[str, Any]]:
    with _connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM chat ORDER BY id DESC LIMIT ?", (limit,))]


# ------------------------------------------------------------------ settings (e.g. demo_video_url)
def get_setting(key: str) -> Optional[str]:
    with _connect() as conn:
        r = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return r["value"] if r else None


def set_setting(key: str, value: str, user: str) -> None:
    with _lock, _connect() as conn:
        conn.execute("INSERT INTO settings (key, value, ts, user) VALUES (?, ?, ?, ?) "
                     "ON CONFLICT(key) DO UPDATE SET value = excluded.value, ts = excluded.ts, user = excluded.user",
                     (key, value, _now(), user))


# ------------------------------------------------------------------ Maya desk (questions the team wants to ask the COO)
MAYA_STATUSES = ("proposed", "approved", "sent", "answered", "dismissed", "resolved")


def _mq(r: sqlite3.Row) -> Dict[str, Any]:
    d = dict(r)
    try:
        d["invoices"] = json.loads(d.get("invoices_json") or "[]")
    except ValueError:
        d["invoices"] = []
    d["final_text"] = d.get("edited_text") or d.get("text") or ""
    return d


def sync_maya_questions(qs: List[Dict[str, Any]]) -> Dict[str, int]:
    """Insert new questions as proposed; refresh text of still-proposed ones; never downgrade a status.
    A proposed question that no longer appears is marked resolved (by data)."""
    now = _now()
    seen = set()
    added = resolved = 0
    with _lock, _connect() as conn:
        for q in qs:
            qid = str(q.get("id"))
            seen.add(qid)
            row = conn.execute("SELECT status FROM maya_questions WHERE id = ?", (qid,)).fetchone()
            vals = (q.get("purpose"), q.get("owner"), q.get("topic"), q.get("text"), q.get("why"), q.get("changes"),
                    json.dumps(q.get("invoices") or []))
            if row is None:
                conn.execute("INSERT INTO maya_questions (id, created_ts, purpose, owner, topic, text, why, changes, "
                             "invoices_json, status, updated_ts) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'proposed', ?)",
                             (qid, now) + vals + (now,))
                added += 1
            elif row["status"] in ("proposed", "resolved"):
                conn.execute("UPDATE maya_questions SET purpose=?, owner=?, topic=?, text=?, why=?, changes=?, "
                             "invoices_json=?, status='proposed', updated_ts=? WHERE id=?", vals + (now, qid))
        for r in conn.execute("SELECT id FROM maya_questions WHERE status = 'proposed'").fetchall():
            if r["id"] not in seen:
                conn.execute("UPDATE maya_questions SET status='resolved', outcome=COALESCE(outcome, ?), updated_ts=? "
                             "WHERE id=?", ("Resolved by data: the issue no longer appears in the records.", now, r["id"]))
                resolved += 1
    return {"added": added, "resolved": resolved}


def maya_questions(status: Optional[str] = None) -> List[Dict[str, Any]]:
    with _connect() as conn:
        if status:
            rows = conn.execute("SELECT * FROM maya_questions WHERE status = ? ORDER BY created_ts, id", (status,))
        else:
            rows = conn.execute("SELECT * FROM maya_questions ORDER BY created_ts, id")
        return [_mq(r) for r in rows]


def get_maya_question(qid: str) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        r = conn.execute("SELECT * FROM maya_questions WHERE id = ?", (qid,)).fetchone()
        return _mq(r) if r else None


def update_maya_question(qid: str, **fields) -> None:
    allowed = {"status", "edited_text", "approved_by", "approved_ts", "sent_ts", "sent_message", "reply", "reply_ts",
               "outcome"}
    fields = {k: v for k, v in fields.items() if k in allowed}
    if not fields:
        return
    if "status" in fields and fields["status"] not in MAYA_STATUSES:
        raise ValueError(fields["status"])
    sets = ", ".join("{} = ?".format(k) for k in fields) + ", updated_ts = ?"
    with _lock, _connect() as conn:
        conn.execute("UPDATE maya_questions SET " + sets + " WHERE id = ?", tuple(fields.values()) + (_now(), qid))


def maya_sent_bundles() -> int:
    with _connect() as conn:
        r = conn.execute("SELECT COUNT(DISTINCT COALESCE(sent_message, sent_ts)) AS n FROM maya_questions "
                         "WHERE status IN ('sent', 'answered') AND (sent_message IS NOT NULL OR sent_ts IS NOT NULL)").fetchone()
        return int(r["n"] or 0)
