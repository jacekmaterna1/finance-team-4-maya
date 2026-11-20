"""Rules Priya can change herself from the Rules page. Defaults follow docs/collections_policy.md and Maya's answers."""
import copy
import json
import os

DEFAULT_RULES = {
    # Cash Application
    "auto_apply_exact_ref_match": True,   # Maya: exact amount + invoice reference is what the team already does
    "auto_apply_max_amount": 10000.0,     # above this, even an exact match is a proposal. Dana to confirm (QA T+0:37)
    "amount_tolerance": 0.0,              # $ difference still treated as "same amount" for a proposal
    "fee_tolerance": 50.0,                # short by up to this much = likely bank fee -> proposal + write-off approval
    "writeoff_threshold": 0.0,            # Dana sets this. 0 = no automatic write-offs at all
    # Collections stages (days relative to due date) -- collections_policy.md
    "reminder_days": {"courtesy": -5, "first": 7, "second": 21, "final": 45, "escalate": 90},
    # Controller
    "top50_human_only": True,             # policy: nothing to a top-50 account without a person reading it
    "hold_on_open_ticket_days": 120,       # open/pending high-priority ticket in this window = escalation hold
    "dispute_lookback_days": 120,         # how far back to read tickets for disputes ("solved" tickets included)
    "renewal_notice_days": 45,            # flag to AM if renewal is this close
    "card_writeoff_warning_days": 140,    # policy auto-writes off card invoices at 150 days
    "notify_am_before_contact": True,     # policy: tell the AM before finance contacts their account
    "banned_phrases": ["suspend", "suspension", "legal action", "collections agency", "final notice",
                       "third-party", "costs of collection", "no choice",
                       "debt collector", "legal proceedings", "cut off", "court", "credit rating"],
    "use_claude": False,                  # OFF until Legal signs the DPA (Maya, T+0:17). Rules + templates work without it
}

RULES_PATH = os.environ.get("RULES_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "rules.json"))

LABELS = {
    "auto_apply_exact_ref_match": "Apply payments automatically when amount AND invoice reference match exactly",
    "auto_apply_max_amount": "Largest payment applied automatically ($) — larger ones go to Priya even on an exact match. Dana to confirm",
    "amount_tolerance": "Amount tolerance for proposing a match ($)",
    "fee_tolerance": "Short payment treated as a likely bank fee, up to ($)",
    "writeoff_threshold": "Write off small differences automatically up to ($) — set by Dana; 0 = never",
    "top50_human_only": "Top-50 accounts: a person writes every message",
    "hold_on_open_ticket_days": "Hold if a high/urgent support ticket is open from the last N days",
    "dispute_lookback_days": "Read support tickets from the last N days for invoice disputes",
    "renewal_notice_days": "Flag to account manager when renewal is within N days",
    "card_writeoff_warning_days": "Warn before the 150-day automatic card write-off at N days",
    "notify_am_before_contact": "CC the account manager on every reminder",
    "banned_phrases": "Words a reminder may never contain (needs VP Finance sign-off)",
    "use_claude": "Use Claude to read tickets and draft reminders. Keep OFF until Legal approves the DPA (Bedrock route preferred). Off = rules and templates",
}


def load_rules():
    rules = copy.deepcopy(DEFAULT_RULES)
    try:
        with open(RULES_PATH, encoding="utf-8") as f:
            saved = json.load(f)
        for k, v in saved.items():
            if k in rules:
                rules[k] = v
    except (OSError, ValueError):
        pass
    return rules


def save_rules(rules):
    merged = load_rules()
    for k, v in rules.items():
        if k in DEFAULT_RULES:
            merged[k] = v
    os.makedirs(os.path.dirname(os.path.abspath(RULES_PATH)), exist_ok=True)
    with open(RULES_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    return merged
