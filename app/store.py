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

ACTIONS = ("approve", "reject", "edit", "override_hold", "release_hold", "send", "apply")
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
