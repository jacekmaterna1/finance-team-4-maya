"""Thin Claude wrapper with a disk cache so the demo is fast and repeatable.

If ANTHROPIC_API_KEY is not set (or use_claude is off), every call returns None and callers fall back to
deterministic logic. Cached answers are committed to the repo, so the deployed app shows Claude's output
without needing to call the API on each page load.
"""
import hashlib
import json
import os
import threading

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llm_cache.json")
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")
_lock = threading.Lock()
_cache = None


def _load_cache():
    global _cache
    if _cache is None:
        try:
            with open(CACHE_PATH, encoding="utf-8") as f:
                _cache = json.load(f)
        except (OSError, ValueError):
            _cache = {}
    return _cache


def _save_cache():
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(_cache, f, indent=1, sort_keys=True)


def manual(name):
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manuals", name + ".md")
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def ask_json(task, system, user, enabled=True, max_tokens=900):
    """Return parsed JSON from Claude, or None. Results are cached by (task, system, user)."""
    key = hashlib.sha256((task + "\x00" + system + "\x00" + user).encode()).hexdigest()[:24]
    with _lock:
        cache = _load_cache()
        if key in cache:
            return cache[key]
    provider = os.environ.get("LLM_PROVIDER", "anthropic")  # "bedrock" keeps data inside Ledgerline's AWS account
    if not enabled or (provider == "anthropic" and not os.environ.get("ANTHROPIC_API_KEY")):
        return None
    try:
        import anthropic

        client = anthropic.AnthropicBedrock() if provider == "bedrock" else anthropic.Anthropic()
        msg = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system + "\n\nRespond with a single JSON object only. No prose, no code fences.",
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
        if text.startswith("```"):
            text = text.strip("`")
            text = text[text.find("{"):]
        data = json.loads(text[text.find("{"): text.rfind("}") + 1])
    except Exception as e:  # network, auth, parse: fall back, never break the pipeline
        print("[llm] %s failed: %s" % (task, e))
        return None
    with _lock:
        _cache[key] = data
        _save_cache()
    return data
