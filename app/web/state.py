"""In-memory cache of the pipeline state.

Uses the real engine (app.engine.pipeline) when it imports, otherwise the fake in app/web/fake_state.py.
The import is retried on every refresh, so once the engine lands a POST /run picks it up without a restart.
"""
import importlib
import threading
import time
import traceback
from typing import Any, Dict, Optional

_lock = threading.Lock()
_cache: Dict[str, Any] = {"state": None, "source": None, "error": None, "ran_at": None, "seconds": None}


def _backend():
    """Return (module, source, error)."""
    try:
        mod = importlib.import_module("app.engine.pipeline")
        for name in ("run_pipeline", "load_rules", "save_rules"):
            if not hasattr(mod, name):
                raise ImportError("app.engine.pipeline has no " + name)
        return mod, "engine", None
    except Exception as exc:  # engine missing or broken: fall back, but say so loudly in the UI
        from app.web import fake_state
        return fake_state, "fake", "{}: {}".format(type(exc).__name__, exc)


def load_rules() -> Dict[str, Any]:
    mod, _, _ = _backend()
    return mod.load_rules()


def save_rules(rules: Dict[str, Any]) -> None:
    mod, _, _ = _backend()
    mod.save_rules(rules)


def refresh() -> Dict[str, Any]:
    with _lock:
        mod, source, err = _backend()
        t0 = time.time()
        try:
            state = mod.run_pipeline(rules=mod.load_rules())
        except Exception as exc:
            if source == "engine":
                from app.web import fake_state
                err = "Engine run failed, showing fake data: {}: {}\n{}".format(
                    type(exc).__name__, exc, traceback.format_exc(limit=3))
                source = "fake"
                state = fake_state.run_pipeline(rules=fake_state.load_rules())
            else:
                raise
        _cache.update(state=state, source=source, error=err, ran_at=_now_cst(),
                      seconds=round(time.time() - t0, 2))
        sync_maya(state)
        return state


def sync_maya(state: Dict[str, Any]) -> None:
    """Upsert the team's open questions for Maya (engine: app.engine.questions). Never breaks a run."""
    try:
        from app.engine.questions import build_open_questions
        from app import store
        store.sync_maya_questions(build_open_questions(state))
    except Exception as exc:
        _cache["maya_error"] = "{}: {}".format(type(exc).__name__, exc)


def get_state() -> Dict[str, Any]:
    if _cache["state"] is None:
        return refresh()
    return _cache["state"]


def info() -> Dict[str, Optional[Any]]:
    return {k: _cache[k] for k in ("source", "error", "ran_at", "seconds")}


def _now_cst() -> str:
    from datetime import datetime, timedelta, timezone
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("America/Chicago")
    except Exception:
        tz = timezone(timedelta(hours=-6))
    return datetime.now(timezone.utc).astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
