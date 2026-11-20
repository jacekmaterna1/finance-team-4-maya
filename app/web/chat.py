"""'Talk to the team': a deterministic intent engine that works with the AI switched off.

POST /api/chat {message, agent?} -> {agent, reply, cards:[{title, lines, link}], actions:[...], mode}
POST /api/rules/apply {rule, value} -> applies a rule change ONLY after the human clicks Apply.
If RIG_CHAT_AI=on, ANTHROPIC_API_KEY is set and rules.use_claude is true, Claude rephrases the deterministic answer.
"""
import difflib
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app import auth, store
from app.web import rig_data
from app.web import state as st

PREFIX = {"@cash": "cash", "@context": "context", "@controller": "controller", "@collections": "collections",
          "@team": "team"}
STOP = set("""a an the and or of to for in on at by is are was were be been what whats what's why how who when where
which about with from this that these those me my we our you your it its do does did done any all can could should
would will please tell show give status summary held hold holds hold's paid pay payment payments invoice invoices
customer customers draft drafts email emails today needs need now set run rerun re help team cash context controller
collections agent agents still not no yes much many there their them""".split())


def _money(v) -> str:
    try:
        return "${:,.0f}".format(float(v))
    except (TypeError, ValueError):
        return "-"


def _money2(v) -> str:
    try:
        return "${:,.2f}".format(float(v))
    except (TypeError, ValueError):
        return "-"


def _norm(s: str) -> str:
    try:
        from app.engine.data import norm_name
        return norm_name(s)
    except Exception:
        s = (s or "").lower().replace("&", " and ").replace("+", " and ")
        return " ".join(re.sub(r"[^a-z0-9 ]", " ", s).split())


# ------------------------------------------------------------------ entity lookup
def find_customers(state, text: str) -> List[Dict[str, Any]]:
    customers = list((state.get("customers") or {}).values())
    msg_tokens = set(t for t in _norm(text).split() if t not in STOP and len(t) >= 3)
    if not msg_tokens:
        return []
    df: Dict[str, int] = {}
    for c in customers:
        for t in set(_norm(c.get("name", "")).split()):
            df[t] = df.get(t, 0) + 1
    inv_amt = {i["invoice_id"]: float(i["amount"] or 0) for i in state["invoices"]}
    held_ids = {i["invoice_id"] for i in state["invoices"] if i["action"] == "HOLD"}
    wants_held = bool(re.search(r"\b(held|hold|holds|blocked)\b", text.lower()))
    scored = []
    for c in customers:
        toks = [t for t in set(_norm(c.get("name", "")).split()) if t not in ("and", "co", "llp", "inc", "ltd")]
        score = 0.0
        for t in toks:
            hit = t in msg_tokens or any(len(m) >= 5 and difflib.SequenceMatcher(None, t, m).ratio() >= 0.88
                                         for m in msg_tokens)
            if hit:
                score += 1.0 if df.get(t, 0) <= 3 else 0.25
        if score >= 1.0:
            opens = c.get("open_invoices") or []
            held = any(x in held_ids for x in opens) if wants_held else False
            scored.append((score, (held, sum(inv_amt.get(x, 0) for x in opens)), c))
    scored.sort(key=lambda x: (-x[0], not x[1][0], -x[1][1]))
    if not scored:
        return []
    best = scored[0][0]
    return [c for s, _, c in scored if s == best][:4]


def _pick_agent(text: str, default: str = "team") -> str:
    t = text.lower()
    if re.search(r"\b(paid|pay|payment|receipt|cash|match|applied|apply|wire|ach)\b", t):
        return "cash"
    if re.search(r"\b(held|hold|holds|block|release|dispute|why)\b", t):
        return "controller"
    if re.search(r"\b(ticket|tickets|contact|contacts|nps|usage|renewal|zendesk)\b", t):
        return "context"
    if re.search(r"\b(draft|email|remind|reminder|tone|card|retry|cc)\b", t):
        return "collections"
    return default


def explain_customer(state, c: Dict[str, Any], agent: str) -> Tuple[str, List[Dict[str, Any]]]:
    cid = c["customer_id"]
    invs = [i for i in state["invoices"] if i["customer_id"] == cid and
            (i["invoice_id"] in (c.get("open_invoices") or []) or i["action"] != "NO_ACTION")]
    pays = [p for p in state["payments"] if p.get("customer_id") == cid]
    cards: List[Dict[str, Any]] = []
    held = [i for i in invs if i["action"] == "HOLD"]
    lines = []
    if agent in ("cash", "team") and pays:
        for p in pays:
            cards.append({"title": "{} · {} · {}".format(p["payment_id"], _money2(p["amount"]), p["decision"]),
                          "lines": ["Received {} by {} from {}".format(p["received_date"], (p.get("method") or "").upper(),
                                                                       p.get("payer_name"))] +
                          ["Matched to: " + (", ".join(p["invoice_ids"]) or "nothing") +
                           " · confidence {:.0f}%".format(100 * float(p.get("confidence") or 0))] + list(p.get("reasons") or []),
                          "link": "/cash#" + p["payment_id"]})
    if agent in ("controller", "collections", "team", "cash"):
        for i in invs:
            ls = ["{} days past due · stage {} · AM {}".format(i.get("days_past_due"), i.get("stage"),
                                                                  i.get("account_manager") or "-")]
            for h in i.get("holds") or []:
                ls.append("HOLD {}: {}{}".format(h.get("label") or h.get("code"), h.get("detail", ""),
                                                 " → routed to " + h["route_to"] if h.get("route_to") else ""))
            if i.get("draft"):
                ls.append("Draft: \"{}\" to {}".format(i["draft"].get("subject"), ", ".join(i["draft"].get("to") or [])))
            if i.get("retry"):
                ls.append("Card re-run: " + (i["retry"].get("evidence") or ""))
            if not i.get("holds"):
                ls += list(i.get("reasons") or [])[:2]
            cards.append({"title": "{} · {} · {}".format(i["invoice_id"], _money2(i["amount"]), i["action"]),
                          "lines": ls, "link": "/collections#" + i["invoice_id"]})
    if agent == "context" or agent == "team":
        ctx = ["Plan {} · ARR {} · rank {} · AM {} · renewal {}".format(
            c.get("plan"), _money(c.get("current_arr")), c.get("rank") or "-", c.get("account_manager"),
            c.get("renewal_date") or "-")]
        ctx += ["Flag: " + f for f in c.get("flags") or []]
        for t in (c.get("open_tickets") or [])[:3]:
            ctx.append("Open ticket {} ({}): {}".format(t.get("ticket_id"), t.get("priority"), t.get("subject")))
        bad = [x for x in c.get("contacts") or [] if not x.get("verified")]
        if bad:
            ctx.append("Unverified contacts: " + ", ".join("{} ({})".format(x.get("email"), x.get("issue")) for x in bad))
        cards.insert(0, {"title": "{} · customer 360".format(c["name"]), "lines": ctx, "link": "/customers/" + cid})
    open_total = sum(float(i["amount"] or 0) for i in invs if i["invoice_id"] in (c.get("open_invoices") or []))
    lines.append("{}: {} open invoice(s), {} open.".format(c["name"], len(c.get("open_invoices") or []), _money(open_total)))
    if held:
        lines.append("{} held: {}.".format(len(held), "; ".join(
            "{} ({})".format(i["invoice_id"], ", ".join(h.get("label") or h.get("code") for h in i["holds"])) for i in held)))
    unapplied = [p for p in pays if p["decision"] != "AUTO_APPLY"]
    if unapplied:
        lines.append("Unapplied money: " + "; ".join("{} {} → {}".format(p["payment_id"], _money2(p["amount"]),
                                                                          ", ".join(p["invoice_ids"]) or "?") for p in unapplied) + ".")
    drafts = [i for i in invs if i["action"] in ("DRAFT_REMINDER", "HUMAN_WRITES", "RETRY_CARD")]
    if drafts:
        lines.append("Waiting on a person: " + ", ".join("{} ({})".format(i["invoice_id"], i["action"]) for i in drafts) + ".")
    if not held and not drafts and not unapplied:
        lines.append("Nothing needs a person for this customer right now.")
    cards.append({"title": "Open the customer 360", "lines": [], "link": "/customers/" + cid})
    return " ".join(lines), cards


def explain_invoice(state, iid: str) -> Optional[Tuple[str, List[Dict[str, Any]]]]:
    i = next((x for x in state["invoices"] if x["invoice_id"].upper() == iid.upper()), None)
    if not i:
        return None
    c = (state.get("customers") or {}).get(i["customer_id"]) or {"customer_id": i["customer_id"], "name": i["customer_name"]}
    reply, cards = explain_customer(state, c, "controller")
    cards = [x for x in cards if x["title"].startswith(i["invoice_id"])] + [cards[-1]]
    head = "{} for {} ({}) is {}.".format(i["invoice_id"], i["customer_name"], _money2(i["amount"]), i["action"])
    if i.get("holds"):
        head += " Held because: " + "; ".join("{}{}".format(h.get("label") or h.get("code"),
                                                           " (routed to {})".format(h["route_to"]) if h.get("route_to") else "")
                                             for h in i["holds"]) + "."
    else:
        head += " " + " ".join(i.get("reasons") or [])
    return head, cards


def explain_payment(state, pid: str) -> Optional[Tuple[str, List[Dict[str, Any]]]]:
    p = next((x for x in state["payments"] if x["payment_id"].upper() == pid.upper()), None)
    if not p:
        return None
    return ("{} ({} from {}) is {}: {}".format(p["payment_id"], _money2(p["amount"]), p.get("payer_name"), p["decision"],
                                               " ".join(p.get("reasons") or [])),
            [{"title": "Open on Cash application", "lines": [], "link": "/cash#" + p["payment_id"]}])


# ------------------------------------------------------------------ other intents
def team_summary(state, agent: str) -> Tuple[str, List[Dict[str, Any]]]:
    m = state["metrics"]
    per = {
        "cash": "Cash Application: {} auto-applied (exact amount + reference), {} proposals for Priya, {} found in "
                "unapplied receipts.".format(m.get("auto_applied", 0), m.get("needs_review", 0), _money(m.get("cash_found"))),
        "context": "Account Context: profiled {} customers; {} with an open billing complaint; disputes worth {} found in "
                   "support tickets.".format(len(state.get("customers") or {}),
                                             sum(1 for c in (state.get("customers") or {}).values() if c.get("billing_complaint")),
                                             _money(m.get("overdue_disputed"))),
        "controller": "Controller: {} invoices held, {} chases prevented, {} for a person to write, {} decisions for "
                      "Dana.".format(m.get("held", 0), m.get("chases_prevented", 0), m.get("human_writes", 0),
                                     m.get("dana_decisions", 0)),
        "collections": "Collections: {} reminders drafted for Priya, {} card re-runs to approve. Nothing sent without a "
                       "person.".format(m.get("drafts", 0), m.get("card_retries", 0)),
    }
    head = "Overdue {} across {} invoices: {} already received, {} disputed, {} collectable. Complaints caused: {}.".format(
        _money(m.get("overdue_balance")), m.get("overdue_count"), _money(m.get("overdue_already_paid")),
        _money(m.get("overdue_disputed")), _money(m.get("overdue_collectable")), m.get("collections_complaints", 0))
    if agent in per:
        return per[agent], [{"title": rig_data.AGENT_BY_SLUG[agent]["name"], "lines": [per[agent]],
                             "link": "/agents/" + agent}]
    return head, [{"title": "What each agent did this run", "lines": list(per.values()), "link": "/team"}]


def holds_summary(state) -> Tuple[str, List[Dict[str, Any]]]:
    groups: Dict[str, Dict[str, Any]] = {}
    for i in state["invoices"]:
        for h in i.get("holds") or []:
            g = groups.setdefault(h.get("code"), {"label": h.get("label"), "n": 0, "amt": 0.0, "ex": []})
            g["n"] += 1
            g["amt"] += float(i["amount"] or 0)
            if len(g["ex"]) < 3:
                g["ex"].append("{} {} {}".format(i["invoice_id"], i["customer_name"], _money(i["amount"])))
    rows = sorted(groups.items(), key=lambda kv: -kv[1]["amt"])
    cards = [{"title": "{} · {} invoice(s) · {}".format(code, g["n"], _money(g["amt"])),
              "lines": [g["label"] or ""] + g["ex"], "link": "/collections#g-HOLD"} for code, g in rows]
    n = sum(1 for i in state["invoices"] if i["action"] == "HOLD")
    return "{} invoices are held. Holds by reason, largest $ first (an invoice can carry several):".format(n), cards


def needs_me(state) -> Tuple[str, List[Dict[str, Any]]]:
    from app.web.views import needs_you
    items = needs_you(state, store.latest_by_object())
    cards = [{"title": "{} · {} · {}".format(x["id"], _money(x["amount"]), x["customer"]),
              "lines": [x["what"], (x["reason"] or "")[:220]], "link": x["link"]} for x in items[:8]]
    return "{} items need a person ({} in total). The largest first:".format(
        len(items), _money(sum(float(x["amount"] or 0) for x in items))), cards


def _rule_lookup(name: str, rules: Dict[str, Any]) -> Optional[str]:
    from app.web.views import RULE_HELP
    n = name.strip().lower().replace("-", " ")
    key = n.replace(" ", "_")
    if key in rules:
        return key
    if "." in key and key.split(".")[0] in rules:
        return key
    labels = {k: (RULE_HELP.get(k, (k, ""))[0]).lower() for k in rules}
    for k, lab in labels.items():
        if n in lab or lab.startswith(n):
            return k
    cand = difflib.get_close_matches(key, list(rules.keys()), n=1, cutoff=0.6)
    if cand:
        return cand[0]
    cand = difflib.get_close_matches(n, list(labels.values()), n=1, cutoff=0.5)
    if cand:
        return next(k for k, v in labels.items() if v == cand[0])
    return None


def parse_rule_value(rules: Dict[str, Any], key: str, raw: str):
    raw = raw.strip().rstrip(".").strip()
    if "." in key:
        top, sub = key.split(".", 1)
        old = (rules.get(top) or {}).get(sub)
    else:
        old = rules.get(key)
    if isinstance(old, bool):
        if raw.lower() in ("on", "true", "yes", "1", "enabled"):
            return True, old
        if raw.lower() in ("off", "false", "no", "0", "disabled"):
            return False, old
        raise ValueError("say on or off")
    if isinstance(old, (int, float)):
        num = raw.replace("$", "").replace(",", "").split()[0]
        v = float(num)
        return (int(v) if isinstance(old, int) and v == int(v) else v), old
    if isinstance(old, list):
        return [x.strip() for x in raw.split(",") if x.strip()], old
    if isinstance(old, dict):
        raise ValueError("set one item, e.g. 'set reminder_days.first to 10'")
    return raw, old


def apply_rule(user: str, key: str, value, dana_approved=False, dana_name: str = "") -> Dict[str, Any]:
    from app.web.views import _diff, _snapshot, check_dana, sensitive_changes
    rules = st.load_rules()
    new = json.loads(json.dumps(rules))
    if "." in key:
        top, sub = key.split(".", 1)
        new.setdefault(top, {})[sub] = value
        before_v = (rules.get(top) or {}).get(sub)
    else:
        new[key] = value
        before_v = rules.get(key)
    if key == "banned_phrases" and not value:
        raise ValueError("The banned-phrases list cannot be empty.")
    sens = sensitive_changes(rules, new)
    err = check_dana(sens, dana_approved, dana_name)
    if err:
        raise PermissionError(err)
    before = _snapshot(st.get_state())
    st.save_rules(new)
    after_state = st.refresh()
    diff = _diff(before, _snapshot(after_state))
    store.record(user, "rules", "rules", "edit", "Changed {} from {} to {} (via Talk to the team)".format(key, before_v, value),
                 {"changed": {key: {"before": before_v, "after": value}}, "impact": diff["rows"],
                  "moved": diff["moved"][:50], "source": "chat", "sensitive": sens,
                  "dana_approved": bool(sens), "dana_name": (dana_name or "").strip() or None})
    return {"before": before_v, "after": value, "rows": diff["rows"], "moved": diff["moved"]}


HELP_LINES = [
    "why is Riverside held?  ·  @cash what about Kingsway  ·  INV-25469",
    "status  ·  @controller status  ·  what did you do",
    "holds  ·  what needs me today",
    "set writeoff_threshold to 50  ·  set fee tolerance to 25 (you confirm with Apply)",
    "re-run",
    "from now on cc Dana on anything over $40k  (logged as a proposed instruction)",
    "Address an agent with @cash, @context, @controller, @collections or @team.",
]


def answer(state, message: str, agent: Optional[str], user: str) -> Dict[str, Any]:
    text = (message or "").strip()
    if agent == "team":
        agent = None  # the panel default; only an explicit @team prefix pins the whole team
    m = re.match(r"^(@\w+)\s*[:,]?\s*(.*)$", text, re.S)
    if m and m.group(1).lower() in PREFIX:
        agent = PREFIX[m.group(1).lower()]
        text = m.group(2).strip()
    agent = agent if agent in PREFIX.values() else None
    low = text.lower()
    out: Dict[str, Any] = {"agent": agent or "team", "reply": "", "cards": [], "actions": []}

    if not text or low in ("help", "?", "what can you do", "commands") or low.startswith("help"):
        out["reply"] = "Here is what you can ask. Everything runs on rules while the AI is off."
        out["cards"] = [{"title": "Try", "lines": HELP_LINES, "link": None}]
        return out

    if re.match(r"^(from now on|instruction:|always\b|never\b)", low):
        target = agent if agent and agent != "team" else _pick_agent(low, default="collections")
        body = re.sub(r"^instruction:\s*", "", text, flags=re.I)
        iid = store.add_instruction(user, rig_data.AGENT_BY_SLUG[target]["name"], body, source="chat")
        out["agent"] = target
        out["reply"] = ("Logged as a proposed instruction for {} — a human accepts it in Direct the team. Until then the "
                        "agent's manual is unchanged.".format(rig_data.AGENT_BY_SLUG[target]["name"]))
        out["cards"] = [{"title": "Proposed instruction #{}".format(iid), "lines": [body], "link": "/direct#instructions"}]
        return out

    m = re.match(r"^(?:please\s+)?(?:set|change|make)\s+(.+?)\s+(?:to|=)\s+(.+)$", text, re.I)
    if m:
        rules = st.load_rules()
        key = _rule_lookup(m.group(1), rules)
        if not key:
            out["reply"] = "I couldn't find a rule called '{}'. Rules: {}.".format(m.group(1), ", ".join(sorted(rules)))
            return out
        try:
            value, old = parse_rule_value(rules, key, m.group(2))
        except (ValueError, IndexError) as exc:
            out["reply"] = "I couldn't read '{}' as a value for {}: {}.".format(m.group(2), key, exc)
            return out
        if key in ("writeoff_threshold", "amount_tolerance", "fee_tolerance") and isinstance(value, (int, float)) and value < 0:
            out["reply"] = "{} cannot be negative.".format(key)
            return out
        from app.web.views import sensitive_changes
        trial = json.loads(json.dumps(rules))
        if "." in key:
            trial.setdefault(key.split(".")[0], {})[key.split(".", 1)[1]] = value
        else:
            trial[key] = value
        sens = sensitive_changes(rules, trial)
        out["agent"] = "team"
        out["reply"] = "Change {} from {} to {}? Nothing changes until you press Apply. Then the agents re-run and I'll show " \
                       "what moved.".format(key, old, value)
        if sens:
            out["reply"] += " This loosens a guardrail ({}), so Dana must approve it: you'll be asked for her name.".format(
                "; ".join(sens))
        out["cards"] = [{"title": "Proposed rule change", "lines": ["{}: {} → {}".format(key, old, value),
                                                                    "Logged in the audit trail with your name."],
                         "link": "/rules"}]
        out["actions"] = [{"type": "apply_rule", "label": "Apply: {} → {}".format(key, value), "rule": key, "value": value,
                           "needs_dana": bool(sens)}]
        return out

    if re.match(r"^(re-?run|run( the)?( agents| team)?|refresh)\b", low):
        st.refresh()
        reply, cards = team_summary(st.get_state(), "team")
        out["reply"] = "Re-ran all four agents ({}s). {}".format(st.info().get("seconds"), reply)
        out["cards"] = cards
        return out

    inv_ids = re.findall(r"\bINV-?\d{5}\b", text, re.I)
    pay_ids = re.findall(r"\bPAY-?\d{5}\b", text, re.I)
    if inv_ids or pay_ids:
        replies, cards = [], []
        for x in inv_ids[:3]:
            r = explain_invoice(state, x.upper().replace("INV", "INV-").replace("--", "-"))
            if r:
                replies.append(r[0]); cards += r[1]
        for x in pay_ids[:3]:
            r = explain_payment(state, x.upper().replace("PAY", "PAY-").replace("--", "-"))
            if r:
                replies.append(r[0]); cards += r[1]
        if replies:
            out["agent"] = agent or ("cash" if pay_ids and not inv_ids else "controller")
            out["reply"], out["cards"] = " ".join(replies), cards
            return out

    custs = find_customers(state, text)
    if custs:
        who = agent or _pick_agent(low, default="team")
        c = custs[0]
        reply, cards = explain_customer(state, c, who)
        if len(custs) > 1:
            reply += " (Also matched: {}. Say the full name to switch.)".format(", ".join(x["name"] for x in custs[1:]))
        out["agent"], out["reply"], out["cards"] = who, reply, cards
        return out

    if re.search(r"\b(why held|holds?|held|blocked)\b", low):
        out["agent"] = agent or "controller"
        out["reply"], out["cards"] = holds_summary(state)
        return out
    if re.search(r"(needs? me|need me|today|my queue|to do|todo|approve)", low):
        out["reply"], out["cards"] = needs_me(state)
        return out
    if re.search(r"(status|what did you do|summary|summarise|summarize|how are we|overview|numbers)", low):
        out["reply"], out["cards"] = team_summary(state, agent or "team")
        return out

    out["reply"] = ("I didn't catch that. I answer from the live records using rules (the AI is off), so try one of these.")
    out["cards"] = [{"title": "Examples", "lines": HELP_LINES, "link": None}]
    return out


def _maybe_claude(state, res: Dict[str, Any], message: str) -> Dict[str, Any]:
    res["mode"] = "rules"
    if os.environ.get("RIG_CHAT_AI", "").lower() != "on" or not os.environ.get("ANTHROPIC_API_KEY"):
        return res
    if not (state.get("rules") or {}).get("use_claude"):
        return res
    try:
        from app.engine import llm
        ag = rig_data.AGENT_BY_SLUG.get(res["agent"])
        manual = rig_data.read_manual(ag) if ag else "You speak for Ledgerline's finance agent team."
        out = llm.ask_json("rig_chat_v1", manual + "\n\nRephrase the deterministic answer for Priya in plain English. "
                           "Do not add facts. Return {\"reply\": str}.",
                           json.dumps({"question": message, "answer": res["reply"], "cards": res["cards"]})[:6000])
        if out and isinstance(out.get("reply"), str) and out["reply"].strip():
            res["reply"] = out["reply"].strip()
            res["mode"] = "claude"
    except Exception:
        pass
    return res


def build_router() -> APIRouter:
    r = APIRouter()

    @r.post("/api/chat")
    async def api_chat(request: Request):
        user = auth.current_user(request)
        if not user:
            raise HTTPException(401, "login required")
        try:
            body = await request.json()
        except ValueError:
            body = {}
        message = str(body.get("message") or "")[:2000]
        state = st.get_state()
        res = answer(state, message, body.get("agent"), user)
        res = _maybe_claude(state, res, message)
        store.add_chat(user, res.get("agent") or "team", message, res["reply"], res["mode"])
        return JSONResponse(res)

    @r.post("/api/rules/apply")
    async def api_rules_apply(request: Request):
        user = auth.current_user(request)
        if not user:
            raise HTTPException(401, "login required")
        body = await request.json()
        key = str(body.get("rule") or "")
        rules = st.load_rules()
        top = key.split(".")[0]
        if top not in rules:
            raise HTTPException(400, "unknown rule")
        raw = body.get("value")
        try:
            if isinstance(raw, list):
                value = [str(x) for x in raw]
            elif isinstance(raw, bool):
                value = raw
            else:
                value, _old = parse_rule_value(rules, key, str(raw))
        except (ValueError, IndexError) as exc:
            raise HTTPException(400, str(exc))
        try:
            res = apply_rule(user, key, value, body.get("dana_approved"), str(body.get("dana_name") or ""))
        except PermissionError as exc:
            raise HTTPException(400, str(exc))
        except ValueError as exc:
            raise HTTPException(400, str(exc))
        lines = ["{}: {} → {}".format(x["name"], x["before"], x["after"]) for x in res["rows"]] or ["No counts moved."]
        if res["moved"]:
            lines.append("{} item(s) changed decision, e.g. {}".format(
                len(res["moved"]), ", ".join("{} {}→{}".format(x["id"], x["before"], x["after"]) for x in res["moved"][:4])))
        reply = "Applied: {} {} → {}. Agents re-ran.".format(key, res["before"], res["after"])
        store.add_chat(user, "team", "[Apply] {} = {}".format(key, value), reply, "rules")
        return JSONResponse({"agent": "team", "reply": reply, "mode": "rules",
                             "cards": [{"title": "What changed", "lines": lines, "link": "/rules"}], "actions": []})

    return r
