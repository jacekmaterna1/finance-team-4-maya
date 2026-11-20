"""Export the Claude Code transcripts of this build into readable, redacted markdown for the hand-in.

Usage: python export_transcripts.py <session_dir_with_jsonl> <out_dir>

Kept: every user message, every assistant message, every tool call (name + input), and every tool result
(truncated). Dead ends stay in, as the brief asks.
Redacted: email addresses, personal file listings, the contents of a third-party confidential artifact that was read
only as a design reference, long base64/binary blobs, harness-injected <system-reminder> blocks, and images.
"""
import json
import os
import re
import sys

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.(?:com|net|org|io|co|ai)\b")
B64 = re.compile(r"[A-Za-z0-9+/=]{400,}")
SYSREM = re.compile(r"<system-reminder[^>]*>.*?</system-reminder[^>]*>", re.S)
PERSONAL_FILE_LINE = re.compile(r"^\s*(?:\d{6}\s+\S.*\.pdf|\S+\.pkpass)\s*$", re.I | re.M)  # local folder listing lines
# Words that identify the operator's personal files, stored only as hashes so this public script doesn't name them.
PERSONAL_WORD_HASHES = {"c145648ad1"}


def _personal_line(line):
    import hashlib
    for w in re.findall(r"[A-Za-z]+", line):
        if hashlib.sha1(w.lower().encode()).hexdigest()[:10] in PERSONAL_WORD_HASHES:
            return True
    return False
CONFIDENTIAL_MARKERS = ("cowritten-artifact-html", "CEO Cockpit", "artifact-226d3872")
KEEP_EMAIL_DOMAINS = (".example", "ledgerline.com", "noreply@anthropic.com", "apply.scaleworks.com", "users.noreply.github.com")
MAX_RESULT = 2500

AGENT_NAMES = {
    "a7b26524a9a68eb1b": "data-analyst",
    "a22816c3bdc6db518": "builder",
    "afb4d948dcf306b17": "qa-evaluator",
    "a5c42d147853e8154": "test-steward (Maya draft 2)",
    "a1bc8e386f6156468": "test-steward (log exchanges 2-3)",
    "a42b4316bb2e2fd72": "test-steward (log exchange 4)",
    "adc95cb22ab21b91f": "test-steward (one-pager + video script)",
}


def scrub(text):
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False)
    if any(m in text for m in CONFIDENTIAL_MARKERS):
        return "[Omitted: contents of a confidential TrueLoyal artifact (the CEO RIG), read only as a visual design reference.]"
    text = SYSREM.sub("[harness system note omitted]", text)
    text = PERSONAL_FILE_LINE.sub("[personal file name omitted]", text)
    text = "\n".join("[personal file name omitted]" if _personal_line(l) else l for l in text.split("\n"))
    text = B64.sub("[binary data omitted]", text)

    def _email(m):
        e = m.group(0)
        return e if any(k in e for k in KEEP_EMAIL_DOMAINS) or e.endswith(".example") else "[email redacted]"

    text = re.sub(r"https?://claude\.ai/artifact/[A-Za-z0-9_-]+", "[private artifact link omitted]", text)
    text = re.sub(r"hedgehog\w*", "[other unrelated service]", text, flags=re.I)
    return EMAIL.sub(_email, text)


def block_text(b):
    t = b.get("type")
    if t == "text":
        return scrub(b.get("text", ""))
    if t == "tool_use":
        inp = b.get("input", {})
        s = scrub(json.dumps(inp, ensure_ascii=False, indent=1))
        if len(s) > 6000:
            s = s[:6000] + "\n… [tool input truncated]"
        return "**Tool call:** `%s`\n```json\n%s\n```" % (b.get("name"), s)
    if t == "tool_result":
        c = b.get("content")
        if isinstance(c, list):
            parts = []
            for x in c:
                if x.get("type") == "text":
                    parts.append(x.get("text", ""))
                elif x.get("type") == "image":
                    parts.append("[image omitted]")
            c = "\n".join(parts)
        s = scrub(c or "")
        if len(s) > MAX_RESULT:
            s = s[:MAX_RESULT] + "\n… [result truncated, %d chars total]" % len(s)
        return "**Tool result:**\n```\n%s\n```" % s
    if t == "image":
        return "[image omitted]"
    return ""  # thinking and other internal blocks are not exported


def convert(path, title):
    out = ["# %s" % title, "", "_Exported from the Claude Code session log. Redactions are explained in the index._", ""]
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            msg = ev.get("message") or {}
            role = msg.get("role") or ev.get("type")
            if role not in ("user", "assistant"):
                continue
            content = msg.get("content")
            blocks = [{"type": "text", "text": content}] if isinstance(content, str) else (content or [])
            body = [x for x in (block_text(b) for b in blocks) if x and x.strip()]
            if not body:
                continue
            ts = (ev.get("timestamp") or "")[:19].replace("T", " ")
            who = "Jacek" if role == "user" and not any(b.get("type") == "tool_result" for b in blocks) else ("Tool" if role == "user" else "Claude")
            out.append("### %s · %s UTC" % (who, ts))
            out.extend(body)
            out.append("")
    return "\n".join(out)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    index = ["# AI conversations: index", "",
             "Every AI conversation used in the build, dead ends included, exported from Claude Code. One main session (Jacek ↔ Claude Code, the orchestrator) and seven build-agent sessions it delegated to. The first part of the main session is pre-start planning (read the public brief and the SpaceXSI article, set up the team); the 24-hour timer started at ~11:10 CST.",
             "", "**Redactions:** email addresses; personal file names from a local folder listing; the contents of a confidential TrueLoyal artifact (Jacek's CEO RIG) that was read only as a visual design reference; long binary blobs; harness system notes; images. Assistant private reasoning is not part of the log export. Tool results are truncated at %d characters." % MAX_RESULT, "",
             "| File | Session | Messages |", "|---|---|---|"]
    files = []
    for root, _, names in os.walk(src):
        for n in names:
            if n.endswith(".jsonl"):
                files.append(os.path.join(root, n))
    for p in sorted(files, key=lambda x: ("subagents" in x, x)):
        base = os.path.basename(p)[:-6]
        if "subagents" in p:
            aid = base.replace("agent-", "")
            title = "Build agent: %s" % AGENT_NAMES.get(aid, aid)
            name = "agent-%s.md" % AGENT_NAMES.get(aid, aid).split(" ")[0] + ("" if aid not in AGENT_NAMES else "")
            name = "agent-%s-%s.md" % (AGENT_NAMES.get(aid, "agent").split(" ")[0], aid[:6])
        else:
            title = "Main session: Jacek and Claude Code (orchestrator)"
            name = "00-main-session.md"
        md = convert(p, title)
        with open(os.path.join(dst, name), "w", encoding="utf-8") as f:
            f.write(md)
        index.append("| [%s](%s) | %s | %d |" % (name, name, title, md.count("\n### ")))
    with open(os.path.join(dst, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index) + "\n")
    print("\n".join(index[-len(files) - 0:]))


if __name__ == "__main__":
    main()
