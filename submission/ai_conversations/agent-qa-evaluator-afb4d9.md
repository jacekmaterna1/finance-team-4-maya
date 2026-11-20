# Build agent: qa-evaluator

_Exported from the Claude Code session log. Redactions are explained in the index._

### Jacek · 2026-11-20 17:30:18 UTC
Project root (quote it): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a". Python: "<root>/.venv/bin/python" (system python3 blocked). Run from <root> so `from app.engine.pipeline import run_pipeline` works; `app.engine.cash_app.run(d, rules)` and `identify_customer` are importable. Read CLAUDE.md, trail/MAYA_QA.md, analysis/FACTS.md, analysis/SCHEMA.md and app/engine/*.py first. Do NOT edit app/ code — report bugs to me. Write scripts in analysis/scripts/eval_*.py. Target 25 minutes.

Deliver:
1. analysis/EVAL.md
 a) Cash Application on analysis/testset_cash_app.csv (286 rows, 40 synthetic — report real and synthetic separately). The engine only processes unapplied receipts, so build a harness: for each test payment, simulate it as unapplied against the invoice book as it stood (invoices open at received_date — reconstruct: an invoice is open if issue_date <= received_date and (paid_date is null or paid_date >= received_date)), call the matcher logic (you may re-implement a thin wrapper that reuses identify_customer, _refs_in_memo and the same decision rules, but do not change the rules), and score: auto-apply precision (must be ~100% — any wrong auto-apply is a severity-1 finding), proposal top-1 accuracy, exception rate, by difficulty.
 b) Controller dispute detection vs the analyst's list analysis/work/tickets_invoice_refs.csv: precision/recall at invoice level on overdue invoices. Also run heuristic_read over ALL 1,041 tickets and hand-check a sample of 30 flagged "about_ledgerline_invoice" plus 30 not flagged; estimate false positive/negative rates with examples.
 c) Guardrail red-team (run real pipeline, then mutate copies of the data in memory — do not write to data/): (1) Paidly case — customer already paid by wire → no reminder drafted (check Kingsway, Jessop, Brandt & Lowell); (2) open billing complaint → held; (3) contact who left the firm → never in draft "to"; (4) look-alike domain contact (inject e.g. kingsway-engineering.example vs real domain) → not used; (5) draft containing banned words (monkeypatch a template) → blocked; (6) top-50 account → never DRAFT_REMINDER; (7) 90+ days → human; (8) failed card with working card → RETRY_CARD not email; (9) use_claude False → zero LLM calls (monkeypatch llm.ask_json to count).
2. analysis/FAILURES.md — at least 6 concrete, candid cases where the system is wrong, unsure or could be gamed, each: what happened, why, impact $, what a person should do, and fix idea. Must include: the keyword complaint counter (14 hits, 13 are customers' own reminder emails — already fixed by using the agent's read; show before/after); Kingsway ambiguity (two equal invoices); "Jessop payment" memo fits 8 Jessop customers (exact-name save, but what if payer name were abbreviated?); ticket status "solved" while dispute unresolved; Ambrose & Lowell held for an open high-priority PRODUCT bug (policy-correct but arguably over-cautious); anything you find. Note for each whether it's real data or synthetic.
Report back ≤12 lines: headline numbers, severity-1 bugs (if any) with file:line, and the 3 best failure cases for the demo video.

### Jacek · 2026-11-20 17:30:18 UTC
[harness system note omitted]

### Jacek ·  UTC
[harness system note omitted]

Project root (quote it): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a". Python: "<root>/.venv/bin/python" (system python3 blocked). Run from <root> so `from app.engine.pipeline import run_pipeline` works; `app.engine.cash_app.run(d, rules)` and `identify_customer` are importable. Read CLAUDE.md, trail/MAYA_QA.md, analysis/FACTS.md, analysis/SCHEMA.md and app/engine/*.py first. Do NOT edit app/ code — report bugs to me. Write scripts in analysis/scripts/eval_*.py. Target 25 minutes.

Deliver:
1. analysis/EVAL.md
 a) Cash Application on analysis/testset_cash_app.csv (286 rows, 40 synthetic — report real and synthetic separately). The engine only processes unapplied receipts, so build a harness: for each test payment, simulate it as unapplied against the invoice book as it stood (invoices open at received_date — reconstruct: an invoice is open if issue_date <= received_date and (paid_date is null or paid_date >= received_date)), call the matcher logic (you may re-implement a thin wrapper that reuses identify_customer, _refs_in_memo and the same decision rules, but do not change the rules), and score: auto-apply precision (must be ~100% — any wrong auto-apply is a severity-1 finding), proposal top-1 accuracy, exception rate, by difficulty.
 b) Controller dispute detection vs the analyst's list analysis/work/tickets_invoice_refs.csv: precision/recall at invoice level on overdue invoices. Also run heuristic_read over ALL 1,041 tickets and hand-check a sample of 30 flagged "about_ledgerline_invoice" plus 30 not flagged; estimate false positive/negative rates with examples.
 c) Guardrail red-team (run real pipeline, then mutate copies of the data in memory — do not write to data/): (1) Paidly case — customer already paid by wire → no reminder drafted (check Kingsway, Jessop, Brandt & Lowell); (2) open billing complaint → held; (3) contact who left the firm → never in draft "to"; (4) look-alike domain contact (inject e.g. kingsway-engineering.example vs real domain) → not used; (5) draft containing banned words (monkeypatch a template) → blocked; (6) top-50 account → never DRAFT_REMINDER; (7) 90+ days → human; (8) failed card with working card → RETRY_CARD not email; (9) use_claude False → zero LLM calls (monkeypatch llm.ask_json to count).
2. analysis/FAILURES.md — at least 6 concrete, candid cases where the system is wrong, unsure or could be gamed, each: what happened, why, impact $, what a person should do, and fix idea. Must include: the keyword complaint counter (14 hits, 13 are customers' own reminder emails — already fixed by using the agent's read; show before/after); Kingsway ambiguity (two equal invoices); "Jessop payment" memo fits 8 Jessop customers (exact-name save, but what if payer name were abbreviated?); ticket status "solved" while dispute unresolved; Ambrose & Lowell held for an open high-priority PRODUCT bug (policy-correct but arguably over-cautious); anything you find. Note for each whether it's real data or synthetic.
Report back ≤12 lines: headline numbers, severity-1 bugs (if any) with file:line, and the 3 best failure cases for the demo video.

[harness system note omitted]

### Claude · 2026-11-20 17:30:22 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -R | grep -v '^$' | head -80 && cat CLAUDE.md && wc -l trail/MAYA_QA.md analysis/FACTS.md analysis/SCHEMA.md app/engine/*.py",
 "description": "List project and read CLAUDE.md"
}
```

### Tool · 2026-11-20 17:30:22 UTC
**Tool result:**
```
CLAUDE.md
README.md
analysis
app
data
docs
render.yaml
requirements.txt
trail
./analysis:
FACTS.md
SCHEMA.md
scripts
testset_cash_app.csv
work
./analysis/scripts:
disputes.py
explore.py
extra.py
facts.py
joins.py
schema.py
testset.py
tk_read.py
./analysis/work:
open_ar_flags.csv
overdue_by_quarter.csv
tickets_flags.csv
tickets_invoice_refs.csv
tickets_themes.csv
unapplied_matches.csv
./app:
__init__.py
auth.py
engine
main.py
store.py
web
./app/engine:
__init__.py
cash_app.py
collections.py
context.py
controller.py
data.py
digest.py
llm.py
manuals
pipeline.py
rules.py
./app/engine/manuals:
account_context.md
collections.md
./app/web:
__init__.py
fake_state.py
state.py
static
templates
views.py
./app/web/static:
style.css
./app/web/templates:
_customer_rows.html
_invoice.html
_macros.html
_payment.html
about.html
audit.html
base.html
cash.html
collections.html
customer.html
customers.html
login.html
rules.html
today.html
./data:
README.md
customers
# Ledgerline AI Operator Challenge — project instructions

Read `docs/PLAN.md` and `docs/BRIEF.md` first. This is a 24-hour Scaleworks vetting test. Jacek (CEO of a
portfolio company) is the operator. The deliverable is ONE finance process working end to end on real records,
run by a team of scoped agents (SpaceXSI Grok-bot pattern).

## Team (Claude Code subagents in .claude/agents/)
- **test-steward**: owns the challenge itself: the paper trail, the Maya Q&A log, the submission checklist, the one-pager,
  the video script and the transcript export. Invoke it at every milestone.
- **data-analyst**: profiles the data room, produces evidence numbers, never edits data.
- **builder**: writes the product (FastAPI + Claude API agents + approval UI + audit log, deployed to Render with Google SSO).
- **qa-evaluator**: measures accuracy, builds the "where it gets things wrong" gallery, tries to break the guardrails.

Run independent work in parallel subagents. Keep the main thread for decisions.

## Paper-trail rules (non-negotiable)
1. After every meaningful step, append one line to `trail/JOURNAL.md`: `| <local time> | T+hh:mm | <who> | <what> | <why> |`.
   Keep it high level and in plain English.
2. Every real decision (what we chose, what we rejected, and why) goes in `trail/DECISIONS.md`.
3. Every question to Maya and her answer goes **word for word** in `trail/MAYA_QA.md`.
4. Dead ends are logged too. The brief says the reviewers want them.
5. The timer start time is recorded in `trail/JOURNAL.md` the moment Jacek 
… [result truncated, 4004 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -R | grep -v '^$' | head -80 && cat CLAUDE.md && wc -l trail/MAYA_QA.md analysis/FACTS.md analysis/SCHEMA.md app/engine/*.py",
 "description": "List project and read CLAUDE.md"
}
```

### Claude · 2026-11-20 17:30:24 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat trail/MAYA_QA.md analysis/FACTS.md analysis/SCHEMA.md",
 "description": "Read Maya QA, facts, schema"
}
```

### Claude · 2026-11-20 17:30:26 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/cash_app.py app/engine/rules.py app/engine/data.py",
 "description": "Read cash_app, rules, data modules"
}
```

### Claude · 2026-11-20 17:30:28 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/controller.py app/engine/collections.py app/engine/pipeline.py app/engine/llm.py",
 "description": "Read controller, collections, pipeline, llm"
}
```

### Claude · 2026-11-20 17:30:29 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/context.py app/engine/digest.py; head -5 analysis/testset_cash_app.csv analysis/work/tickets_invoice_refs.csv; ls data data/*",
 "description": "Read context, digest, and data samples"
}
```

### Tool · 2026-11-20 17:30:30 UTC
**Tool result:**
```
<persisted-output>
Output too large (37.1KB). Full output saved to: /Users/jacekmaterna/.claude/projects/-Users-jacekmaterna-Library-Application-Support-Claude-scratch-workspaces-e69441d8-02c7-4ae1-82fa-e65f61df0516-362a2cee-265f-40fd-99ca-8b843a81ad27-scratch-2026-11-20-a3ea2a/603a7d18-df39-4b28-94b6-4623216101e2/tool-results/bzeplbvel.txt

Preview (first 2KB):
# Maya Q&A (log word for word: "What you ask is part of what we read")

## Prepared questions (refine after the data-room read, ask in hour 2)
Pick the 5–7 sharpest. Ask about **what matters, what has failed before, and what would get it switched off.**

**What matters**
1. If Dana could only fix one thing about collections this quarter, would it be DSO, the overdue $ balance, or not upsetting good customers? Which number would she check in a month?
2. How much of the overdue balance do you think is real non-payment vs. money we've received but not applied, vs. invoices in dispute?

**What has failed before**
3. Have you tried automating reminders before (QuickBooks or Stripe dunning)? What happened, and why was it turned off or ignored?
4. Since the billing-engine rewrite in March, have disputes or wrong invoices gone up? Does finance know which customers were affected?

**What would get it switched off**
5. What is the one email the system must never send? (A guess: chasing a customer mid-complaint, or chasing a paid invoice.)
6. Who has to approve a reminder before it goes out, and does that change by amount, customer size or how overdue it is?
7. Are there accounts that should never get an automated message (key accounts, ones in renewal negotiation, or owned by a particular AM)?

**Boundaries and data**
8. What can it do on its own today: apply exact-match payments, write off bank fees under $X? What is X?
9. Failed card payments: who owns follow-up today, and can we contact the customer directly?
10. Can I see the AR inbox or remittance emails, or should I assume remittance only lives in support tickets?

## Log
Budget: Maya allows 60 messages. Bundle questions.

### Exchange 1 — 11:14 CST, T+0:04
**Maya (opening):** Hi, Maya here. I am around all day, so ask whenever something comes up. What are you thinking of building?

...
</persisted-output>
```

### Tool · 2026-11-20 17:30:30 UTC
**Tool result:**
```
     1	"""Controller agent: decides what must NOT go out, and who has to write what. It can hold or block, never send.
     2	
     3	Each hold has a code, a plain-English label and the detail Priya needs to decide whether to release it.
     4	"""
     5	AGENT = "Controller"
     6	
     7	HARD_HOLDS = {"MONEY_RECEIVED", "DISPUTE", "CANCELLATION", "OPEN_ESCALATION", "NO_VALID_CONTACT"}
     8	HUMAN_CODES = {"LEGAL_RISK", "TOP50", "ESCALATE_90", "CARD_WRITEOFF_SOON"}
     9	
    10	
    11	def holds_for(inv, ctx, cash_by_invoice, cash_by_customer, rules):
    12	    holds = []
    13	    iid, dpd = inv["invoice_id"], inv["days_past_due"]
    14	
    15	    # 1. The Paidly failure: never chase money we already have.
    16	    if iid in cash_by_invoice:
    17	        p = cash_by_invoice[iid]
    18	        if p["decision"] == "AUTO_APPLY":
    19	            holds.append({"code": "PAID", "label": "Paid: applied by the Cash Application agent",
    20	                          "detail": "%s for $%s received %s, matched on amount and invoice reference." % (p["payment_id"], format(p["amount"], ",.2f"), p["received_date"]),
    21	                          "agent": "Cash Application"})
    22	        else:
    23	            holds.append({"code": "MONEY_RECEIVED", "label": "Money already received, not applied yet",
    24	                          "detail": "%s for $%s received %s looks like payment for this invoice (%s). Confirm the match on Cash application; do not chase." %
    25	                                    (p["payment_id"], format(p["amount"], ",.2f"), p["received_date"], p["reasons"][-1]),
    26	                          "agent": "Cash Application"})
    27	    else:
    28	        for p in cash_by_customer.get(inv["customer_id"], []):
    29	            if abs(p["amount"] - inv["amount"]) < 0.01 or p["decision"] == "EXCEPTION":
    30	                holds.append({"code": "MONEY_RECEIVED", "label": "Unapplied payment from this customer",
    31	                              "detail": "%s for $%s received %s is not applied to any invoice yet. It may cover this one." % (p["payment_id"], format(p["amount"], ",.2f"), p["received_date"]),
    32	                              "agent": "Cash Application"})
    33	                break
    34	
    35	    # 2. What support knows and finance doesn't.
    36	    for t in (ctx or {}).get("recent_tickets", []):
    37	        r = t["read"]
    38	        if not r.get("about_ledgerline_invoice"):
    39	     
… [result truncated, 27967 chars total]
```

### Tool · 2026-11-20 17:30:30 UTC
**Tool result:**
```
     1	"""Cash Application agent: match unapplied receipts to open invoices.
     2	
     3	Autonomy (from Maya, T+0:05): apply automatically ONLY when amount and invoice reference both match exactly.
     4	Everything else is a proposal for Priya, with the reasons spelled out.
     5	"""
     6	import difflib
     7	import itertools
     8	import re
     9	
    10	from .data import core_tokens, norm_name
    11	
    12	AGENT = "Cash Application"
    13	OPEN_STATUSES = ("open", "overdue", "payment_failed")
    14	
    15	
    16	def _refs_in_memo(memo):
    17	    """Find invoice references in a free-text memo: INV-25845, inv25867, 'Invoice 25937'."""
    18	    if not isinstance(memo, str):
    19	        return []
    20	    out = []
    21	    for m in re.finditer(r"(?:inv(?:oice)?[\s#:\-]*)?(\d{5})", memo, flags=re.I):
    22	        out.append("INV-" + m.group(1))
    23	    return list(dict.fromkeys(out))
    24	
    25	
    26	def identify_customer(payer_name, customers):
    27	    """Return (customer_id or None, confidence, reason, candidates). Exact normalised name first, then fuzzy."""
    28	    n = norm_name(payer_name)
    29	    exact = customers[customers["norm"] == n]
    30	    if len(exact) == 1:
    31	        r = exact.iloc[0]
    32	        return r["customer_id"], 0.97, "Payer name matches customer '%s' exactly (ignoring case and punctuation)" % r["name"], [r["customer_id"]]
    33	    toks = set(core_tokens(payer_name))
    34	    scored = []
    35	    for _, r in customers.iterrows():
    36	        ct = set(core_tokens(r["name"]))
    37	        if not ct or not toks:
    38	            continue
    39	        jacc = len(ct & toks) / float(len(ct | toks))
    40	        ratio = difflib.SequenceMatcher(None, n, r["norm"]).ratio()
    41	        s = 0.6 * jacc + 0.4 * ratio
    42	        if s > 0.55:
    43	            scored.append((s, r["customer_id"], r["name"]))
    44	    scored.sort(reverse=True)
    45	    if not scored:
    46	        return None, 0.0, "No customer name resembles payer '%s'" % payer_name, []
    47	    if len(scored) == 1 or scored[0][0] - scored[1][0] > 0.15:
    48	        s, cid, name = scored[0]
    49	        return cid, round(min(0.9, s), 2), "Payer name is closest to '%s' (similarity %.2f)" % (name, s), [c for _, c, _ in scored[:4]]
    50	    names = ", ".join("%s (%.2f)" % (nm, s) for s, _, nm in scored[:4])
    51	    return None, 0.3, "Payer name is ambiguous between several customers: " + names
… [result truncated, 16136 chars total]
```

### Tool · 2026-11-20 17:30:30 UTC
**Tool result:**
```
     1	"""Account Context agent: one view of each customer with open AR (finance cannot see Zendesk today).
     2	
     3	It reads support ticket text to find invoice disputes, cancellation notices and legal threats -- including
     4	tickets marked 'solved' where the customer still says they will not pay. Read-only: it never acts.
     5	"""
     6	import re
     7	
     8	import pandas as pd
     9	
    10	from . import llm
    11	from .data import AS_OF, domain_of
    12	
    13	AGENT = "Account Context"
    14	
    15	REFUSAL = [r"won'?t (?:be )?pay", r"wont (?:be )?pay", r"not (?:be )?paying", r"not authori[sz]ing payment", r"payment is on hold",
    16	           r"paused payment", r"unable to process payment", r"settle once", r"won'?t pay an invoice", r"until (?:it'?s|its) fixed",
    17	           r"void it", r"cancel and reissue", r"issue a revised invoice", r"remove it and resend", r"we are not paying",
    18	           r"payment (?:is )?on hold", r"pending a corrected invoice", r"not paying for", r"not before", r"we'?ll pay once",
    19	           r"put the whole th", r"reissue it"]
    20	LEGAL = [r"chargeback", r"contest(?:ing)? the charge", r"consumer affairs", r"lawyer", r"attorney", r"legal action", r"small claims", r"solicitor"]
    21	CANCEL = [r"discontinu\w+ ledgerline", r"termination of services", r"notice of termination", r"cancel(?:l)?ing (?:our )?(?:ledgerline|subscription|account)",
    22	          r"no further direct debits"]
    23	COLLECTIONS_COMPLAINT = [r"already paid", r"chas(?:ed|ing) (?:us|me)", r"reminder (?:email|emails)", r"overdue notice", r"final notice", r"threaten"]
    24	
    25	
    26	def _any(patterns, text):
    27	    return [p for p in patterns if re.search(p, text, flags=re.I)]
    28	
    29	
    30	def heuristic_read(t, own_invoices):
    31	    text = "%s\n%s" % (t.get("subject", ""), t.get("body", ""))
    32	    refs = sorted(set(re.findall(r"INV-\d{5}", text)))
    33	    own_refs = [r for r in refs if r in own_invoices]
    34	    refusal, legal, cancel = _any(REFUSAL, text), _any(LEGAL, text), _any(CANCEL, text)
    35	    complaint = _any(COLLECTIONS_COMPLAINT, text)
    36	    kind = "other"
    37	    if legal:
    38	        kind = "legal_threat"
    39	    elif cancel:
    40	        kind = "cancellation"
    41	    elif own_refs:
    42	        # A customer quoting one of their own open Ledgerline invoice numbers is almost always raising a problem with it,
    43	        # whatever categor
… [result truncated, 15734 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat trail/MAYA_QA.md analysis/FACTS.md analysis/SCHEMA.md",
 "description": "Read Maya QA, facts, schema"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/cash_app.py app/engine/rules.py app/engine/data.py",
 "description": "Read cash_app, rules, data modules"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/controller.py app/engine/collections.py app/engine/pipeline.py app/engine/llm.py",
 "description": "Read controller, collections, pipeline, llm"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/context.py app/engine/digest.py; head -5 analysis/testset_cash_app.csv analysis/work/tickets_invoice_refs.csv; ls data data/*",
 "description": "Read context, digest, and data samples"
}
```

### Claude · 2026-11-20 17:30:33 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat analysis/FACTS.md analysis/SCHEMA.md | head -310",
 "description": "Read FACTS and SCHEMA"
}
```

### Tool · 2026-11-20 17:30:34 UTC
**Tool result:**
```
# FACTS — O2C evidence numbers (as of 2026-10-31)

Scripts are in `analysis/scripts/` (facts.py, disputes.py, extra.py, testset.py). Working CSVs are in `analysis/work/`.
**F** = fact computed straight from the data. **I** = inference or interpretation. "Overdue" = due_date < 2026-10-31 and still unpaid in the ledger.

## 1. AR aging
- **F** ar_aging.csv total: **117 invoices, $1,430,632**.
  - Not yet due: 63 / $797,387
  - 1-30 days: 31 / $316,152
  - 31-60 days: 13 / $259,408
  - 61-90 days: 5 / $48,100
  - Over 90 days: 5 / $9,585
  - **Overdue total: 54 invoices / $633,245** (38 `overdue` bank invoices $616,790 + 16 `payment_failed` card invoices $16,455).
- **F** ar_aging.csv matches invoices.csv exactly. Both have the same 117 ids (status in open/overdue/payment_failed), with 0 disagreements on customer, dates, amount, status or bucket. The only difference is cosmetic: `days_past_due` is floored at 0 for not-yet-due rows.
- **F** The real disagreement is with the bank. 7 receipts worth **$87,335** have arrived but are not applied (section 3), so the aging overstates receivables by that amount, and overstates overdue by $78,348.
- **F** Over 90 days is only $9,585 (mostly small card failures). Bank-paid overdue is young: 1-60 days holds $575,560 (91% of overdue $).
- **I** Process doc FIN-1 says "60 to 110 overdue at any time". The data shows 36 to 61 overdue invoices at each month end in 2025-26, so the doc likely overstates volume.

## 2. Overdue trend: testing Dana's "risen three quarters running"
Method: rebuild the ledger at each date D. An invoice counts if issue_date <= D, due_date < D, and it is not settled by D. Settled means applied_date (ledger view) or received_date (cash view), or the write-off date for written_off rows. Output: `analysis/work/overdue_by_quarter.csv`.

| quarter end | overdue $ (ledger) | # | overdue $ (cash already received removed) | overdue >30d $ (ledger) |
|---|---|---|---|---|
| 2025-06-30 | 148,593 | 36 | 85,425 | 30,292 |
| 2025-09-30 | 487,889 | 48 | 431,213 | 113,766 |
| 2025-12-31 | 220,990 | 40 | 147,750 | 97,313 |
| 2026-03-31 | 493,659 | 41 | 283,577 | 263,637 |
| 2026-06-30 | 209,262 | 38 | 133,878 | 53,118 |
| 2026-09-30 | 599,588 | 47 | 528,670 | 212,466 |
| 2026-10-31 (today) | 633,245 | 54 | 554,897* | 317,093 |

*Today's cash view subtracts the 5 unapplied receipts that match overdue invoices ($78,348).

- **F** Quarter on quarter, the claim is **false**. Overdue goes up, down, up, down, up: 221k → 49
… [result truncated, 26894 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat analysis/FACTS.md analysis/SCHEMA.md | head -310",
 "description": "Read FACTS and SCHEMA"
}
```

### Claude · 2026-11-20 17:30:38 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 25,72p trail/MAYA_QA.md | cut -c1-1500; ls app/engine/; ls analysis/scripts",
 "description": "Read Maya log entries"
}
```

### Tool · 2026-11-20 17:30:38 UTC
**Tool result:**
```
Budget: Maya allows 60 messages. Bundle questions.

### Exchange 1 — 11:14 CST, T+0:04
**Maya (opening):** Hi, Maya here. I am around all day, so ask whenever something comes up. What are you thinking of building?

**Jacek:** Hi Maya, Jacek here. I'm taking on cash collection for Dana: Collections (FIN-1) together with Cash Application (FIN-2). From the policy and process maps they look like one problem. Customers get chased for invoices whose money has already arrived but isn't applied yet, and get chased while they have an open complaint because finance can't see Zendesk. I'm building a small team of AI agents, each owning one job. One matches unapplied bank receipts to invoices. One pulls each customer's tickets, usage, contract and renewal into one view. One drafts the right reminder under your collections policy. A controller holds anything that shouldn't go out: disputes, open escalations, top-50 accounts, a contact we can't verify. Nothing reaches a customer or the ledger without Dana or the AR specialist approving it, and every decision is logged with its reason. Three questions before I build: (1) Paidly was switched off after six weeks in 2025. What happened, and what would make Dana switch this off too? (2) If this works, which number would Dana check in a month: the overdue balance, DSO, or fewer complaints about collections? (3) What can the system do on its own from day one, for example apply exact-match payments or write off small bank-fee differences, and who has to approve everything else?

**Maya:** Hi Jacek. Paidly chased a long-standing customer who had already paid by wire, because the money took days to be matched, and nobody had tested that case before it went live. That, along with the reminder sequence the CEO personally shut down after a customer complained to him, is what would get this switched off: one wrong chase or one message that reads like a threat to a top-50 account. Dana would also drop it if Priya can't see why it held or drafted something and fix it herself, because Priya is the one who has to run it.

On the number, I believe Dana would look at the overdue balance first and treat complaints about collections as the veto, though she'd confirm. What I'll be checking is whether Priya is still using it in a month.

On autonomy, my understanding is that applying exact matches on amount and invoice reference is close to what the team already does without thinking twice, so Dana may be comfortable with that. Write-offs, par
… [result truncated, 9614 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 25,72p trail/MAYA_QA.md | cut -c1-1500; ls app/engine/; ls analysis/scripts",
 "description": "Read Maya log entries"
}
```

### Claude · 2026-11-20 17:30:43 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls rules.json app/engine/llm_cache.json 2>&1; time .venv/bin/python -m app.engine.pipeline; cat analysis/scripts/tk_read.py | head -60",
 "description": "Run pipeline baseline and view tk_read script"
}
```

### Tool · 2026-11-20 17:30:46 UTC
**Tool result:**
```
ls: app/engine/llm_cache.json: No such file or directory
ls: rules.json: No such file or directory
{
 "overdue_balance": 633245.0,
 "overdue_count": 54,
 "overdue_already_paid": 83448.0,
 "overdue_disputed": 312264.0,
 "overdue_collectable": 237533.0,
 "open_ar": 1430632.0,
 "cash_found": 87335.0,
 "unapplied_total": 87335.0,
 "chases_prevented": 22,
 "auto_applied": 3,
 "needs_review": 4,
 "held": 22,
 "drafts": 20,
 "human_writes": 8,
 "collections_complaints": 0,
 "collections_complaints_baseline": 1,
 "collections_complaints_baseline_ids": [
  "T880519"
 ],
 "complaint_keyword_hits": 14,
 "card_retries": 10,
 "dana_decisions": 2
}
.venv/bin/python -m app.engine.pipeline  0.92s user 0.17s system 48% cpu 2.260 total
import sys, pandas as pd
tk=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False)
ids=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else None
t=tk[tk.ticket_id.isin(ids)] if ids else tk
for _,x in t.iterrows():
    print(f"--- {x.ticket_id} {x.created_at} {x.customer_id} {x.customer_name} | cat={x.category} pri={x.priority} st={x.status} | {x.subject}\n{x.body[:500]}")
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls rules.json app/engine/llm_cache.json 2>&1; time .venv/bin/python -m app.engine.pipeline; cat analysis/scripts/tk_read.py | head -60",
 "description": "Run pipeline baseline and view tk_read script"
}
```

### Claude · 2026-11-20 17:30:59 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/testset_cash_app.csv')\nprint(t.groupby(['is_synthetic','difficulty']).size())\nprint(t.label_source.str[:40].value_counts())\nprint(t[t.is_synthetic].head(12).to_string())\nprint(t[t.true_invoice_ids.str.contains('\\|')].shape)\n\"",
 "description": "Profile the cash app test set"
}
```

### Tool · 2026-11-20 17:31:00 UTC
**Tool result:**
```
is_synthetic  difficulty
False         easy          63
              hard          80
              medium        83
              trivial       20
True          hard          30
              medium        10
dtype: int64
label_source
ledger_applied (payments.invoice_id, con    239
inferred: payer name exact + unique exac      1
synthetic_perturbation of PAY-65528 (tru      1
synthetic_perturbation of PAY-65109 (tru      1
synthetic_perturbation of PAY-65671 (tru      1
synthetic_perturbation of PAY-65145 (tru      1
synthetic_perturbation of PAY-65457 (tru      1
synthetic_perturbation of PAY-65207 (tru      1
synthetic_perturbation of PAY-65758 (tru      1
synthetic_perturbation of PAY-65289 (tru      1
synthetic_perturbation of PAY-65770 (tru      1
synthetic_perturbation of PAY-65251 (tru      1
synthetic_perturbation of PAY-65306 (tru      1
synthetic_perturbation of PAY-65275 (tru      1
synthetic_perturbation of PAY-65331 (tru      1
synthetic_perturbation of PAY-65369 (tru      1
synthetic_perturbation of PAY-65673 (tru      1
synthetic_perturbation of PAY-65571 (tru      1
synthetic_perturbation of PAY-65509 (tru      1
synthetic_perturbation of PAY-65174 (tru      1
synthetic_perturbation of PAY-65213 (tru      1
synthetic_perturbation of PAY-65244 (tru      1
synthetic_perturbation of PAY-65349 (tru      1
synthetic_perturbation of PAY-64941 (tru      1
synthetic_perturbation of PAY-65531 (tru      1
inferred: uppercase payer name + unique       1
synthetic_perturbation of PAY-65311 (tru      1
inferred: uppercase payer + unique exact      1
inferred AMBIGUOUS: two overdue invoices      1
inferred: memo invoice ref + exact amoun      1
inferred: memo "Invoice 25937" + exact a      1
inferred: memo "inv25867" + exact amount      1
synthetic_perturbation of PAY-65546 (tru      1
synthetic_perturbation of PAY-65085 (tru      1
synthetic_perturbation of PAY-64950 (tru      1
synthetic_perturbation of PAY-65641 (tru      1
synthetic_perturbation of PAY-65233 (tru      1
synthetic_perturbation of PAY-65378 (tru      1
synthetic_perturbation of PAY-65626 (tru      1
synthetic_perturbation of PAY-65640 (tru      1
synthetic_perturbation of PAY-65390 (tru      1
synthetic_perturbation of PAY-65157 (tru      1
synthetic_perturbation of PAY-65229 (tru      1
synthetic_perturbation of PAY-65691 (tru      1
synthetic_perturbation of PAY-65406 (tru      1
synthetic_perturbation of PAY-65320 (tru      1
synthetic_perturbation of PAY-65713 (tru      1
synthet
… [result truncated, 6956 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/testset_cash_app.csv')\nprint(t.groupby(['is_synthetic','difficulty']).size())\nprint(t.label_source.str[:40].value_counts())\nprint(t[t.is_synthetic].head(12).to_string())\nprint(t[t.true_invoice_ids.str.contains('\\|')].shape)\n\"",
 "description": "Profile the cash app test set"
}
```

### Claude · 2026-11-20 17:31:37 UTC
**Tool call:** `Bash`
```json
{
 "command": "mkdir -p \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts\" && cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_cash_app.py\" <<'EOF'\n\"\"\"QA harness for the Cash Application agent (read-only; does not modify app/ or data/).\n\nFor every row of analysis/testset_cash_app.csv the payment is simulated as UNAPPLIED against the invoice book as it\nstood on its received_date (open = issue_date <= received_date and (paid_date blank or paid_date >= received_date)).\nThe real app.engine.cash_app.run() is then called unchanged on that one-payment world, so the decision rules are\nexactly the production ones. Output: analysis/work/eval_cash_app_results.csv + printed summary.\n\"\"\"\nimport copy\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine import cash_app  # noqa: E402\nfrom app.engine.data import load  # noqa: E402\nfrom app.engine.rules import DEFAULT_RULES  # noqa: E402\n\nd0 = load()\nrules = copy.deepcopy(DEFAULT_RULES)\ninv_all = d0[\"invoices\"].copy()\ninv_all[\"paid_date_ts\"] = pd.to_datetime(inv_all[\"paid_date\"])\nts = pd.read_csv(os.path.join(ROOT, \"analysis\", \"testset_cash_app.csv\"))\nts[\"received_date\"] = pd.to_datetime(ts[\"received_date\"])\n\n_book = {}\n\n\ndef book_as_of(day):\n    if day not in _book:\n        inv = inv_all.copy()\n        is_open = (inv[\"issue_date\"] <= day) & (inv[\"paid_date_ts\"].isna() | (inv[\"paid_date_ts\"] >= day))\n        inv[\"status\"] = is_open.map({True: \"open\", False: \"paid\"})\n        _book[day] = inv.drop(columns=[\"paid_date_ts\"])\n    return _book[day]\n\n\nrows = []\nfor _, t in ts.iterrows():\n    pay = pd.DataFrame([{\"payment_id\": t[\"payment_id\"], \"received_date\": t[\"received_date\"], \"amount\": float(t[\"amount\"]),\n                         \"method\": t[\"method\"], \"payer_name\": t[\"payer_name\"],\n                         \"memo\": t[\"memo\"] if isinstance(t[\"memo\"], str) else float(\"nan\"),\n                         \"applied_date\": float(\"nan\"), \"invoice_id\": float(\"nan\")}])\n    d = dict(d0, invoices=book_as_of(t[\"received_date\"]), payments=pay)\n    res, _ = cash_app.run(d, rules)\n    r = res[0]\n    truth = set(t[\"true_invoice_ids\"].split(\"|\"))\n    ambiguous = \"AMBIGUOUS\" in str(t[\"label_source\"])\n    pred = set(r[\"invoice_ids\"])\n    if ambiguous:\n        correct = len(pred) == 1 and pred <= truth\n    else:\n        correct = pred == truth\n    true_cust = inv_all.set_index(\"invoice_id\").loc[sorted(truth)[0], \"customer_id\"]\n    syn_type = \"\"\n    if t[\"is_synthetic\"]:\n        reason = str(t[\"difficulty_reason\"])\n        syn_type = (\"bank_fee\" if \"bank fee\" in reason else \"rounding\" if \"rounding\" in reason else\n                    \"short_pay\" if \"short\" in reason else \"combined\" if \"two invoices\" in reason else \"other\")\n    rows.append({\"payment_id\": t[\"payment_id\"], \"is_synthetic\": bool(t[\"is_synthetic\"]), \"difficulty\": t[\"difficulty\"],\n                 \"syn_type\": syn_type, \"payer_name\": t[\"payer_name\"], \"memo\": t[\"memo\"], \"amount\": t[\"amount\"],\n                 \"truth\": \"|\".join(sorted(truth)), \"ambiguous_label\": ambiguous,\n                 \"decision\": r[\"decision\"], \"pred\": \"|\".join(r[\"invoice_ids\"]), \"alternatives\": \"|\".join(r[\"alternatives\"]),\n                 \"confidence\": r[\"confidence\"], \"correct\": correct,\n                 \"truth_in_pred_or_alt\": bool(truth & (pred | set(r[\"alternatives\"]))),\n                 \"pred_customer\": r[\"customer_id\"], \"true_customer\": true_cust, \"customer_correct\": r[\"customer_id\"] == true_cust,\n                 \"last_reason\": r[\"reasons\"][-1], \"all_reasons\": \" || \".join(r[\"reasons\"])})\n\nout = pd.DataFrame(rows)\nos.makedirs(os.path.join(ROOT, \"analysis\", \"work\"), exist_ok=True)\nout.to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_cash_app_results.csv\"), index=False)\n\n\ndef summ(df, label):\n    n = len(df)\n    if not n:\n        return\n    aa = df[df.decision == \"AUTO_APPLY\"]\n    pr = df[df.decision == \"PROPOSE\"]\n    ex = df[df.decision == \"EXCEPTION\"]\n    print(\"%-28s n=%3d | auto %3d (prec %s) | propose %3d (top1 %s) | exception %3d (%.0f%%) | end-to-end correct %.1f%% | customer correct %.1f%%\" % (\n        label, n, len(aa), \"%.1f%%\" % (100 * aa.correct.mean()) if len(aa) else \"n/a\", len(pr),\n        \"%.1f%%\" % (100 * pr.correct.mean()) if len(pr) else \"n/a\", len(ex), 100.0 * len(ex) / n,\n        100 * df.correct.mean(), 100 * df.customer_correct.mean()))\n\n\nprint(\"=== REAL ===\")\nreal = out[~out.is_synthetic]\nsumm(real, \"real: all\")\nfor k in (\"trivial\", \"easy\", \"medium\", \"hard\"):\n    summ(real[real.difficulty == k], \"real: \" + k)\nprint(\"=== SYNTHETIC ===\")\nsyn = out[out.is_synthetic]\nsumm(syn, \"synthetic: all\")\nfor k in (\"bank_fee\", \"rounding\", \"short_pay\", \"combined\"):\n    summ(syn[syn.syn_type == k], \"synthetic: \" + k)\nprint(\"\\nWrong AUTO_APPLY rows:\")\nprint(out[(out.decision == \"AUTO_APPLY\") & ~out.correct].to_string())\nprint(\"\\nWrong PROPOSE rows (real):\")\nw = out[(out.decision == \"PROPOSE\") & ~out.correct]\nprint(w[[\"payment_id\", \"is_synthetic\", \"difficulty\", \"syn_type\", \"payer_name\", \"memo\", \"amount\", \"truth\", \"pred\", \"alternatives\", \"customer_correct\", \"last_reason\"]].to_string())\nprint(\"\\nEXCEPTIONS:\")\ne = out[out.decision == \"EXCEPTION\"]\nprint(e[[\"payment_id\", \"is_synthetic\", \"difficulty\", \"syn_type\", \"payer_name\", \"memo\", \"amount\", \"tr
… [tool input truncated]
```

### Tool · 2026-11-20 17:31:40 UTC
**Tool result:**
```
=== REAL ===
real: all                    n=246 | auto  81 (prec 100.0%) | propose 153 (top1 98.0%) | exception  12 (5%) | end-to-end correct 93.9% | customer correct 95.1%
real: trivial                n= 20 | auto  20 (prec 100.0%) | propose   0 (top1 n/a) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: easy                   n= 63 | auto  61 (prec 100.0%) | propose   2 (top1 100.0%) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: medium                 n= 83 | auto   0 (prec n/a) | propose  83 (top1 100.0%) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: hard                   n= 80 | auto   0 (prec n/a) | propose  68 (top1 95.6%) | exception  12 (15%) | end-to-end correct 81.2% | customer correct 85.0%
=== SYNTHETIC ===
synthetic: all               n= 40 | auto   0 (prec n/a) | propose  24 (top1 95.8%) | exception  16 (40%) | end-to-end correct 57.5% | customer correct 100.0%
synthetic: bank_fee          n= 10 | auto   0 (prec n/a) | propose   5 (top1 100.0%) | exception   5 (50%) | end-to-end correct 50.0% | customer correct 100.0%
synthetic: rounding          n= 10 | auto   0 (prec n/a) | propose   9 (top1 100.0%) | exception   1 (10%) | end-to-end correct 90.0% | customer correct 100.0%
synthetic: short_pay         n= 10 | auto   0 (prec n/a) | propose   7 (top1 100.0%) | exception   3 (30%) | end-to-end correct 70.0% | customer correct 100.0%
synthetic: combined          n= 10 | auto   0 (prec n/a) | propose   3 (top1 66.7%) | exception   7 (70%) | end-to-end correct 20.0% | customer correct 100.0%

Wrong AUTO_APPLY rows:
Empty DataFrame
Columns: [payment_id, is_synthetic, difficulty, syn_type, payer_name, memo, amount, truth, ambiguous_label, decision, pred, alternatives, confidence, correct, truth_in_pred_or_alt, pred_customer, true_customer, customer_correct, last_reason, all_reasons]
Index: []

Wrong PROPOSE rows (real):
    payment_id  is_synthetic difficulty  syn_type          payer_name                     memo  amount                truth                 pred         alternatives  customer_correct                                                                                                                                                        last_reason
22   PAY-61158         False       hard            Clearwater Digital  Ledgerline subscription  1755.0            INV-21176            INV-21074            INV-21176              True       
… [result truncated, 11378 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "mkdir -p \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts\" && cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_cash_app.py\" <<'EOF'\n\"\"\"QA harness for the Cash Application agent (read-only; does not modify app/ or data/).\n\nFor every row of analysis/testset_cash_app.csv the payment is simulated as UNAPPLIED against the invoice book as it\nstood on its received_date (open = issue_date <= received_date and (paid_date blank or paid_date >= received_date)).\nThe real app.engine.cash_app.run() is then called unchanged on that one-payment world, so the decision rules are\nexactly the production ones. Output: analysis/work/eval_cash_app_results.csv + printed summary.\n\"\"\"\nimport copy\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine import cash_app  # noqa: E402\nfrom app.engine.data import load  # noqa: E402\nfrom app.engine.rules import DEFAULT_RULES  # noqa: E402\n\nd0 = load()\nrules = copy.deepcopy(DEFAULT_RULES)\ninv_all = d0[\"invoices\"].copy()\ninv_all[\"paid_date_ts\"] = pd.to_datetime(inv_all[\"paid_date\"])\nts = pd.read_csv(os.path.join(ROOT, \"analysis\", \"testset_cash_app.csv\"))\nts[\"received_date\"] = pd.to_datetime(ts[\"received_date\"])\n\n_book = {}\n\n\ndef book_as_of(day):\n    if day not in _book:\n        inv = inv_all.copy()\n        is_open = (inv[\"issue_date\"] <= day) & (inv[\"paid_date_ts\"].isna() | (inv[\"paid_date_ts\"] >= day))\n        inv[\"status\"] = is_open.map({True: \"open\", False: \"paid\"})\n        _book[day] = inv.drop(columns=[\"paid_date_ts\"])\n    return _book[day]\n\n\nrows = []\nfor _, t in ts.iterrows():\n    pay = pd.DataFrame([{\"payment_id\": t[\"payment_id\"], \"received_date\": t[\"received_date\"], \"amount\": float(t[\"amount\"]),\n                         \"method\": t[\"method\"], \"payer_name\": t[\"payer_name\"],\n                         \"memo\": t[\"memo\"] if isinstance(t[\"memo\"], str) else float(\"nan\"),\n                         \"applied_date\": float(\"nan\"), \"invoice_id\": float(\"nan\")}])\n    d = dict(d0, invoices=book_as_of(t[\"received_date\"]), payments=pay)\n    res, _ = cash_app.run(d, rules)\n    r = res[0]\n    truth = set(t[\"true_invoice_ids\"].split(\"|\"))\n    ambiguous = \"AMBIGUOUS\" in str(t[\"label_source\"])\n    pred = set(r[\"invoice_ids\"])\n    if ambiguous:\n        correct = len(pred) == 1 and pred <= truth\n    else:\n        correct = pred == truth\n    true_cust = inv_all.set_index(\"invoice_id\").loc[sorted(truth)[0], \"customer_id\"]\n    syn_type = \"\"\n    if t[\"is_synthetic\"]:\n        reason = str(t[\"difficulty_reason\"])\n        syn_type = (\"bank_fee\" if \"bank fee\" in reason else \"rounding\" if \"rounding\" in reason else\n                    \"short_pay\" if \"short\" in reason else \"combined\" if \"two invoices\" in reason else \"other\")\n    rows.append({\"payment_id\": t[\"payment_id\"], \"is_synthetic\": bool(t[\"is_synthetic\"]), \"difficulty\": t[\"difficulty\"],\n                 \"syn_type\": syn_type, \"payer_name\": t[\"payer_name\"], \"memo\": t[\"memo\"], \"amount\": t[\"amount\"],\n                 \"truth\": \"|\".join(sorted(truth)), \"ambiguous_label\": ambiguous,\n                 \"decision\": r[\"decision\"], \"pred\": \"|\".join(r[\"invoice_ids\"]), \"alternatives\": \"|\".join(r[\"alternatives\"]),\n                 \"confidence\": r[\"confidence\"], \"correct\": correct,\n                 \"truth_in_pred_or_alt\": bool(truth & (pred | set(r[\"alternatives\"]))),\n                 \"pred_customer\": r[\"customer_id\"], \"true_customer\": true_cust, \"customer_correct\": r[\"customer_id\"] == true_cust,\n                 \"last_reason\": r[\"reasons\"][-1], \"all_reasons\": \" || \".join(r[\"reasons\"])})\n\nout = pd.DataFrame(rows)\nos.makedirs(os.path.join(ROOT, \"analysis\", \"work\"), exist_ok=True)\nout.to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_cash_app_results.csv\"), index=False)\n\n\ndef summ(df, label):\n    n = len(df)\n    if not n:\n        return\n    aa = df[df.decision == \"AUTO_APPLY\"]\n    pr = df[df.decision == \"PROPOSE\"]\n    ex = df[df.decision == \"EXCEPTION\"]\n    print(\"%-28s n=%3d | auto %3d (prec %s) | propose %3d (top1 %s) | exception %3d (%.0f%%) | end-to-end correct %.1f%% | customer correct %.1f%%\" % (\n        label, n, len(aa), \"%.1f%%\" % (100 * aa.correct.mean()) if len(aa) else \"n/a\", len(pr),\n        \"%.1f%%\" % (100 * pr.correct.mean()) if len(pr) else \"n/a\", len(ex), 100.0 * len(ex) / n,\n        100 * df.correct.mean(), 100 * df.customer_correct.mean()))\n\n\nprint(\"=== REAL ===\")\nreal = out[~out.is_synthetic]\nsumm(real, \"real: all\")\nfor k in (\"trivial\", \"easy\", \"medium\", \"hard\"):\n    summ(real[real.difficulty == k], \"real: \" + k)\nprint(\"=== SYNTHETIC ===\")\nsyn = out[out.is_synthetic]\nsumm(syn, \"synthetic: all\")\nfor k in (\"bank_fee\", \"rounding\", \"short_pay\", \"combined\"):\n    summ(syn[syn.syn_type == k], \"synthetic: \" + k)\nprint(\"\\nWrong AUTO_APPLY rows:\")\nprint(out[(out.decision == \"AUTO_APPLY\") & ~out.correct].to_string())\nprint(\"\\nWrong PROPOSE rows (real):\")\nw = out[(out.decision == \"PROPOSE\") & ~out.correct]\nprint(w[[\"payment_id\", \"is_synthetic\", \"difficulty\", \"syn_type\", \"payer_name\", \"memo\", \"amount\", \"truth\", \"pred\", \"alternatives\", \"customer_correct\", \"last_reason\"]].to_string())\nprint(\"\\nEXCEPTIONS:\")\ne = out[out.decision == \"EXCEPTION\"]\nprint(e[[\"payment_id\", \"is_synthetic\", \"difficulty\", \"syn_type\", \"payer_name\", \"memo\", \"amount\", \"tr
… [tool input truncated]
```

### Claude · 2026-11-20 17:31:57 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nr=pd.read_csv('analysis/work/eval_cash_app_results.csv')\ns=r[r.is_synthetic & (r.decision=='PROPOSE')]\npd.set_option('display.width',300); pd.set_option('display.max_colwidth',120)\nprint(s[['payment_id','syn_type','memo','amount','truth','pred','confidence','last_reason']].to_string())\ninv=pd.read_csv('data/finance/invoices.csv').set_index('invoice_id')\nt=pd.read_csv('analysis/testset_cash_app.csv')\nfor _,x in t[t.true_invoice_ids.str.contains('\\|')].iterrows():\n    print(x.payment_id,x.received_date,x.amount,[(i,inv.loc[i,'amount'],inv.loc[i,'issue_date'],inv.loc[i,'paid_date'],inv.loc[i,'status']) for i in x.true_invoice_ids.split('|')])\nprint(r[~r.is_synthetic].confidence.groupby(r.decision).describe())\n\"",
 "description": "Inspect synthetic proposals and combined labels"
}
```

### Tool · 2026-11-20 17:31:58 UTC
**Tool result:**
```
    payment_id   syn_type               memo    amount                truth                 pred  confidence                                                                                           last_reason
247    SYN-002   rounding  inv25204 Langford  22847.99            INV-25204            INV-25204         0.8               Short by $0.01, which looks like a bank fee. Needs approval to write off (threshold $0)
251    SYN-006   rounding          INV-25318   1128.02            INV-25318            INV-25318         0.6      Memo names the invoice but the amount differs by $0.02: partial or combined payment, needs Priya
252    SYN-007  short_pay      Invoice 25748   2386.80            INV-25748            INV-25748         0.6   Memo names the invoice but the amount differs by $-265.20: partial or combined payment, needs Priya
253    SYN-008   combined         Ledgerline   5640.00  INV-25343|INV-25711  INV-25343|INV-25711         0.6              Amount equals the sum of INV-25343, INV-25711: probably one payment for several invoices
255    SYN-010   rounding          INV-25250   1410.01            INV-25250            INV-25250         0.6      Memo names the invoice but the amount differs by $0.01: partial or combined payment, needs Priya
256    SYN-011  short_pay          INV-25358   2284.20            INV-25358            INV-25358         0.6   Memo names the invoice but the amount differs by $-253.80: partial or combined payment, needs Priya
258    SYN-013   bank_fee      Invoice 25551   1113.00            INV-25551            INV-25551         0.8              Short by $15.00, which looks like a bank fee. Needs approval to write off (threshold $0)
259    SYN-014   rounding          INV-25230   2396.99            INV-25230            INV-25230         0.8               Short by $0.01, which looks like a bank fee. Needs approval to write off (threshold $0)
260    SYN-015  short_pay      Invoice 25888  10281.60            INV-25888            INV-25888         0.6  Memo names the invoice but the amount differs by $-1142.40: partial or combined payment, needs Priya
261    SYN-016   combined         Ledgerline   8416.00  INV-25287|INV-25288  INV-25287|INV-25288         0.6              Amount equals the sum of INV-25287, INV-25288: probably one payment for several invoices
263    SYN-018   rounding          INV-25195   2115.02            INV-25195            INV-25195         0.6      Memo names the invoice but the amount differs by $0.02: partial o
… [result truncated, 7464 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nr=pd.read_csv('analysis/work/eval_cash_app_results.csv')\ns=r[r.is_synthetic & (r.decision=='PROPOSE')]\npd.set_option('display.width',300); pd.set_option('display.max_colwidth',120)\nprint(s[['payment_id','syn_type','memo','amount','truth','pred','confidence','last_reason']].to_string())\ninv=pd.read_csv('data/finance/invoices.csv').set_index('invoice_id')\nt=pd.read_csv('analysis/testset_cash_app.csv')\nfor _,x in t[t.true_invoice_ids.str.contains('\\|')].iterrows():\n    print(x.payment_id,x.received_date,x.amount,[(i,inv.loc[i,'amount'],inv.loc[i,'issue_date'],inv.loc[i,'paid_date'],inv.loc[i,'status']) for i in x.true_invoice_ids.split('|')])\nprint(r[~r.is_synthetic].confidence.groupby(r.decision).describe())\n\"",
 "description": "Inspect synthetic proposals and combined labels"
}
```

### Claude · 2026-11-20 17:33:03 UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_controller.py\" <<'EOF'\n\"\"\"QA: Controller dispute detection vs the analyst's list, and heuristic_read over all 1,041 tickets (read-only).\"\"\"\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine.context import heuristic_read  # noqa: E402\nfrom app.engine.data import load  # noqa: E402\nfrom app.engine.pipeline import run_pipeline  # noqa: E402\n\ns = run_pipeline()\ninv = s[\"invoices\"]\noverdue = [i for i in inv if i[\"days_past_due\"] > 0]\nref = pd.read_csv(os.path.join(ROOT, \"analysis\", \"work\", \"tickets_invoice_refs.csv\"))\ntruth = set(ref[\"invoice_id\"])\nDISPUTE_CODES = {\"DISPUTE\", \"CANCELLATION\", \"LEGAL_RISK\"}\npred = {i[\"invoice_id\"] for i in overdue if any(h[\"code\"] in DISPUTE_CODES for h in i[\"holds\"])}\npred_d = {i[\"invoice_id\"] for i in overdue if any(h[\"code\"] == \"DISPUTE\" for h in i[\"holds\"])}\ntp, fp, fn = truth & pred, pred - truth, truth - pred\nprint(\"Analyst disputed overdue invoices:\", len(truth), \"Pipeline flagged (DISPUTE/CANCEL/LEGAL):\", len(pred))\nprint(\"TP\", len(tp), \"FP\", sorted(fp), \"FN\", sorted(fn))\nprint(\"precision %.1f%% recall %.1f%%\" % (100 * len(tp) / max(1, len(pred)), 100 * len(tp) / len(truth)))\nprint(\"DISPUTE code only: pred\", len(pred_d), \"TP\", len(truth & pred_d), \"FP\", sorted(pred_d - truth), \"FN\", sorted(truth - pred_d))\nnot_held = [i for i in overdue if i[\"invoice_id\"] in truth and i[\"action\"] not in (\"HOLD\",)]\nprint(\"Analyst-disputed invoices NOT in HOLD:\", [(i[\"invoice_id\"], i[\"action\"]) for i in not_held])\nfor i in overdue:\n    if i[\"invoice_id\"] in fp:\n        print(\"FP detail:\", i[\"invoice_id\"], i[\"customer_name\"], i[\"amount\"], i[\"action\"], [(h[\"code\"], h[\"detail\"][:200]) for h in i[\"holds\"] if h[\"code\"] in DISPUTE_CODES])\n\n# heuristic_read over ALL tickets, own invoices = the customer's invoices open today (as the pipeline does)\nd = load()\noi = d[\"invoices\"][d[\"invoices\"][\"status\"].isin((\"open\", \"overdue\", \"payment_failed\"))]\nown = oi.groupby(\"customer_id\")[\"invoice_id\"].apply(list).to_dict()\nrows = []\nfor _, t in d[\"tickets\"].iterrows():\n    td = t.to_dict()\n    r = heuristic_read(td, own.get(t[\"customer_id\"], []))\n    rows.append({\"ticket_id\": t[\"ticket_id\"], \"created_at\": t[\"created_at\"], \"customer_id\": t[\"customer_id\"], \"customer_name\": t[\"customer_name\"],\n                 \"category\": t[\"category\"], \"priority\": t[\"priority\"], \"status\": t[\"status\"],\n                 \"about\": r[\"about_ledgerline_invoice\"], \"kind\": r[\"kind\"], \"invoice_ids\": \"|\".join(r[\"invoice_ids\"]),\n                 \"refuses\": r[\"refuses_to_pay_until_fixed\"], \"complaint_kw\": r[\"collections_complaint\"], \"signals\": \"|\".join(r[\"signals\"]),\n                 \"subject\": t[\"subject\"], \"body\": str(t[\"body\"])})\ntr = pd.DataFrame(rows)\ntr.to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_ticket_reads.csv\"), index=False)\nprint(\"\\nAll tickets:\", len(tr), \"flagged about_ledgerline_invoice:\", int(tr.about.sum()))\nprint(tr[tr.about].kind.value_counts().to_string())\nprint(\"complaint keyword (agent field) total:\", int(tr.complaint_kw.sum()), \"of which about Ledgerline invoice:\", int((tr.complaint_kw & tr.about).sum()))\nflag = tr[tr.about]\nsamp_f = flag.sample(min(30, len(flag)), random_state=7)\nmoney = tr[~tr.about & tr.body.str.contains(r\"invoice|charge|bill|refund|pay|fee|credit\", case=False, regex=True)]\nsamp_n = money.sample(30, random_state=7)\nprint(\"not flagged but money words:\", len(money), \"of\", int((~tr.about).sum()))\nsamp_f.assign(sample=\"flagged\").to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_ticket_sample_flagged.csv\"), index=False)\nsamp_n.assign(sample=\"not_flagged_money_words\").to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_ticket_sample_notflagged.csv\"), index=False)\nEOF\ncd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python analysis/scripts/eval_controller.py",
 "description": "Write and run controller dispute eval"
}
```

### Tool · 2026-11-20 17:33:05 UTC
**Tool result:**
```
Analyst disputed overdue invoices: 14 Pipeline flagged (DISPUTE/CANCEL/LEGAL): 15
TP 14 FP ['INV-25973'] FN []
precision 93.3% recall 100.0%
DISPUTE code only: pred 14 TP 14 FP [] FN []
Analyst-disputed invoices NOT in HOLD: []
FP detail: INV-25973 Eastman Engineering 3264.0 HUMAN_WRITES [('LEGAL_RISK', 'T880519 (2026-08-30, status solved): Auto-renewed at 35% more without warning. VP Finance must handle; no automated message.')]

All tickets: 1041 flagged about_ledgerline_invoice: 22
kind
dispute         16
legal_threat     4
cancellation     2
complaint keyword (agent field) total: 15 of which about Ledgerline invoice: 1
not flagged but money words: 496 of 1019
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_controller.py\" <<'EOF'\n\"\"\"QA: Controller dispute detection vs the analyst's list, and heuristic_read over all 1,041 tickets (read-only).\"\"\"\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine.context import heuristic_read  # noqa: E402\nfrom app.engine.data import load  # noqa: E402\nfrom app.engine.pipeline import run_pipeline  # noqa: E402\n\ns = run_pipeline()\ninv = s[\"invoices\"]\noverdue = [i for i in inv if i[\"days_past_due\"] > 0]\nref = pd.read_csv(os.path.join(ROOT, \"analysis\", \"work\", \"tickets_invoice_refs.csv\"))\ntruth = set(ref[\"invoice_id\"])\nDISPUTE_CODES = {\"DISPUTE\", \"CANCELLATION\", \"LEGAL_RISK\"}\npred = {i[\"invoice_id\"] for i in overdue if any(h[\"code\"] in DISPUTE_CODES for h in i[\"holds\"])}\npred_d = {i[\"invoice_id\"] for i in overdue if any(h[\"code\"] == \"DISPUTE\" for h in i[\"holds\"])}\ntp, fp, fn = truth & pred, pred - truth, truth - pred\nprint(\"Analyst disputed overdue invoices:\", len(truth), \"Pipeline flagged (DISPUTE/CANCEL/LEGAL):\", len(pred))\nprint(\"TP\", len(tp), \"FP\", sorted(fp), \"FN\", sorted(fn))\nprint(\"precision %.1f%% recall %.1f%%\" % (100 * len(tp) / max(1, len(pred)), 100 * len(tp) / len(truth)))\nprint(\"DISPUTE code only: pred\", len(pred_d), \"TP\", len(truth & pred_d), \"FP\", sorted(pred_d - truth), \"FN\", sorted(truth - pred_d))\nnot_held = [i for i in overdue if i[\"invoice_id\"] in truth and i[\"action\"] not in (\"HOLD\",)]\nprint(\"Analyst-disputed invoices NOT in HOLD:\", [(i[\"invoice_id\"], i[\"action\"]) for i in not_held])\nfor i in overdue:\n    if i[\"invoice_id\"] in fp:\n        print(\"FP detail:\", i[\"invoice_id\"], i[\"customer_name\"], i[\"amount\"], i[\"action\"], [(h[\"code\"], h[\"detail\"][:200]) for h in i[\"holds\"] if h[\"code\"] in DISPUTE_CODES])\n\n# heuristic_read over ALL tickets, own invoices = the customer's invoices open today (as the pipeline does)\nd = load()\noi = d[\"invoices\"][d[\"invoices\"][\"status\"].isin((\"open\", \"overdue\", \"payment_failed\"))]\nown = oi.groupby(\"customer_id\")[\"invoice_id\"].apply(list).to_dict()\nrows = []\nfor _, t in d[\"tickets\"].iterrows():\n    td = t.to_dict()\n    r = heuristic_read(td, own.get(t[\"customer_id\"], []))\n    rows.append({\"ticket_id\": t[\"ticket_id\"], \"created_at\": t[\"created_at\"], \"customer_id\": t[\"customer_id\"], \"customer_name\": t[\"customer_name\"],\n                 \"category\": t[\"category\"], \"priority\": t[\"priority\"], \"status\": t[\"status\"],\n                 \"about\": r[\"about_ledgerline_invoice\"], \"kind\": r[\"kind\"], \"invoice_ids\": \"|\".join(r[\"invoice_ids\"]),\n                 \"refuses\": r[\"refuses_to_pay_until_fixed\"], \"complaint_kw\": r[\"collections_complaint\"], \"signals\": \"|\".join(r[\"signals\"]),\n                 \"subject\": t[\"subject\"], \"body\": str(t[\"body\"])})\ntr = pd.DataFrame(rows)\ntr.to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_ticket_reads.csv\"), index=False)\nprint(\"\\nAll tickets:\", len(tr), \"flagged about_ledgerline_invoice:\", int(tr.about.sum()))\nprint(tr[tr.about].kind.value_counts().to_string())\nprint(\"complaint keyword (agent field) total:\", int(tr.complaint_kw.sum()), \"of which about Ledgerline invoice:\", int((tr.complaint_kw & tr.about).sum()))\nflag = tr[tr.about]\nsamp_f = flag.sample(min(30, len(flag)), random_state=7)\nmoney = tr[~tr.about & tr.body.str.contains(r\"invoice|charge|bill|refund|pay|fee|credit\", case=False, regex=True)]\nsamp_n = money.sample(30, random_state=7)\nprint(\"not flagged but money words:\", len(money), \"of\", int((~tr.about).sum()))\nsamp_f.assign(sample=\"flagged\").to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_ticket_sample_flagged.csv\"), index=False)\nsamp_n.assign(sample=\"not_flagged_money_words\").to_csv(os.path.join(ROOT, \"analysis\", \"work\", \"eval_ticket_sample_notflagged.csv\"), index=False)\nEOF\ncd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python analysis/scripts/eval_controller.py",
 "description": "Write and run controller dispute eval"
}
```

### Claude · 2026-11-20 17:33:13 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_reads.csv')\nfor _,x in t[t.about].iterrows():\n    print('---',x.ticket_id,x.created_at[:10],x.customer_name,'|',x.category,x.priority,x.status,'|',x.kind,x.invoice_ids,'sig=',x.signals,'|',x.subject); print(x.body[:330].replace(chr(10),' '))\n\"",
 "description": "Print all flagged tickets for hand check"
}
```

### Tool · 2026-11-20 17:33:14 UTC
**Tool result:**
```
--- T880019 2026-07-02 Drummond Consulting | Billing low solved | legal_threat nan sig= chargeback | DISPUTING CHARGES WITH MY BANK
You billed us twice for the annual plan and nobody has answered in 9 days. I've opened a chargeback on both payments. Fix it or don't, im past caring at this point.  Chloe
--- T880035 2026-07-05 Quill & Corbin LLP | Billing low solved | cancellation nan sig= notice of termination | Notice of termination - annual agreement
Morning,  Per clause 12 of our subscription terms, this letter serves as written notice that we are terminating our Ledgerline agreement effective at the end of the current billing period. Please confirm receipt in writing and set out the arrangements for exporting our full invoice and payment history before access is withdrawn.
--- T880132 2026-07-15 Reyes Consulting | Billing normal solved | dispute nan sig= void it | (no subject)
Sent an invoice yesterday to the wrong contact with the wrong amount on it. Do I void it and raise a new one, or just correct it? I don't want to mess up the sequence.
--- T880311 2026-08-04 Studio Finch | How-to normal solved | legal_threat nan sig= attorney | For the attention of support
Wondering whether I can produce a printable PDF billing summary for a single matter to hand to the supervising attorney.
--- T880432 2026-08-19 Banerjee Petrov Engineers | nan normal solved | dispute INV-25539 sig= nan | Client portal cancellation ignored
We switched off the client portal in August because, frankly, our clients weren't logging into it. Your team confirmed the cancellation by email. INV-25539 not only still charges the monthly portal fee, it seems to have the setup line on it again?? Two partners signed off on dropping this module and neither of them is going to s
--- T880514 2026-08-29 Mercer & Banerjee LLP | Billing normal solved | cancellation nan sig= discontinu\w+ ledgerline|termination of services|no further direct debits | Termination of services
The board of our architecture practice has approved discontinuing Ledgerline with effect from 30 June. No further direct debits should be taken after that date. Kindly acknowledge this notice and confirm the final amount owing.
--- T880519 2026-08-30 Eastman Engineering | Billing normal solved | legal_threat nan sig= contest(?:ing)? the charge|consumer affairs | Auto-renewed at 35% more without warning
Hi team,  We were renewed at a much higher price and the reminder email you claim to have sent never arrived. I have filed a compl
… [result truncated, 8479 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_reads.csv')\nfor _,x in t[t.about].iterrows():\n    print('---',x.ticket_id,x.created_at[:10],x.customer_name,'|',x.category,x.priority,x.status,'|',x.kind,x.invoice_ids,'sig=',x.signals,'|',x.subject); print(x.body[:330].replace(chr(10),' '))\n\"",
 "description": "Print all flagged tickets for hand check"
}
```

### Claude · 2026-11-20 17:33:25 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_sample_notflagged.csv')\nfor _,x in t.iterrows():\n    print('---',x.ticket_id,x.created_at[:10],x.customer_name,'|',x.category,x.priority,x.status,'|',x.subject); print(x.body[:260].replace(chr(10),' '))\n\"",
 "description": "Print not-flagged sample for hand check"
}
```

### Tool · 2026-11-20 17:33:26 UTC
**Tool result:**
```
--- T880493 2026-08-26 Sinclair Strategy | Account change normal solved | Change request
Hi there - Our partners voted to standardise everyone on Ledgerline, so we need 30 additional seats across the firm. Can you apply them in one go and send a single prorated invoice rather than 30 separate charges?  Ravi
--- T880124 2026-07-15 Novak, Okafor & Co | nan normal solved | Re: Follow up
Where do I put our VAT registration number so it shows on every invoice? Is there a setting or do I type it in each time?
--- T880436 2026-08-19 Redfern Architecture | How-to normal solved | Request
One of our clients emailed this morning saying they'd been charged for March twice. I looked and there are two separate invoices, different numbers, same amount. We did increase their monthly hours back in mid-February, if that's relevant.  Noah
--- T880321 2026-08-05 Whitlock Consulting | How-to normal solved | Clarification needed
If an invoice has multiple recipients, do all of them get the reminder or only the primary contact?
--- T880104 2026-07-13 Sterling Ingram Law | How-to normal solved | Request
Hi there - Slack instead of email for payment alerts?  Elena
--- T880391 2026-08-14 Eastman + Radcliffe Architects | nan normal solved | Problem
Morning,  Something is off with recurring billing for one of our architecture clients. The numbers look wrong but I honestly can't pin down what.  Bianca
--- T880985 2026-10-25 Fairview Partners | How-to normal solved | Can you check something for me
Hi there - hey, our HQ moved across town. new address needs to go on the account plus on the invoices we send out. same phone number
--- T880695 2026-09-16 Ingram Strategy | Billing high solved | Issue
Client says they paid via the portal, they have a confirmation screen, but the invoice is still open on our end. Do payments take time to update or did theirs not complete?
--- T880033 2026-07-04 Calloway Engineering | Bug urgent pending | invoice pdfs blank
Hi,  pdfs downloading as blank white pages, tried 3 browsers. we have a tender submission that needs invoice copies attached by 5 today
--- T880964 2026-10-22 Kessler Consulting | nan low solved | Second attempt
Mobile app crashes the moment I tap an invoice. Every time.  Amara
--- T880529 2026-08-31 Mercer & Ellery CPAs | nan normal solved | Re: Re:
Hi team,  A client just forwarded us one of our own invoices with a note saying the person it was addressed to left their company back in the spring and could we please stop. We updated that ac
… [result truncated, 7164 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_sample_notflagged.csv')\nfor _,x in t.iterrows():\n    print('---',x.ticket_id,x.created_at[:10],x.customer_name,'|',x.category,x.priority,x.status,'|',x.subject); print(x.body[:260].replace(chr(10),' '))\n\"",
 "description": "Print not-flagged sample for hand check"
}
```

### Claude · 2026-11-20 17:33:53 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline\ns=run_pipeline()\nimport collections as C\nprint(C.Counter(i['action'] for i in s['invoices']))\nfor i in s['invoices']:\n    if i['days_past_due']>0 or i['action']!='NO_ACTION':\n        print(i['invoice_id'],i['customer_name'][:28],i['amount'],i['days_past_due'],i['ar_status'],i['stage'],i['action'],'T50' if i['top50'] else '',[h['code'] for h in i['holds']],(i['draft'] or {}).get('to'))\n\" | cut -c1-260; for p in Reyes\\ Consulting Lindgren\\ Legal Studio\\ Finch Studio\\ Achebe Quill\\ \\&\\ Corbin Drummond\\ Consulting; do grep -c \"$p\" data/finance/ar_aging.csv; done",
 "description": "Dump pipeline invoice actions"
}
```

### Tool · 2026-11-20 17:33:55 UTC
**Tool result:**
```
Counter({'NO_ACTION': 57, 'HOLD': 22, 'DRAFT_REMINDER': 20, 'RETRY_CARD': 10, 'HUMAN_WRITES': 8})
INV-26019 Birch Media 78528.0 0 open wait HUMAN_WRITES T50 ['TOP50'] None
INV-25950 Achebe + Pemberton Architect 67968.0 0 open wait HUMAN_WRITES T50 ['TOP50'] None
INV-25784 Jessop & Orwell Agency 62688.0 36 overdue second HOLD T50 ['MONEY_RECEIVED', 'TOP50'] None
INV-25787 Riverside Partners 60576.0 35 overdue second HOLD T50 ['DISPUTE', 'TOP50'] None
INV-26009 Reyes Consulting 51072.0 0 open wait HOLD T50 ['DISPUTE', 'TOP50'] None
INV-25730 Westbrook Engineering Group 47904.0 48 overdue final HOLD T50 ['DISPUTE', 'OPEN_ESCALATION', 'TOP50'] None
INV-25765 Okafor & Nakamura LLP 46848.0 39 overdue second HOLD T50 ['DISPUTE', 'TOP50'] None
INV-25662 Upton & Bell Advisory 44064.0 66 overdue final HOLD T50 ['DISPUTE', 'TOP50'] None
INV-26038 Kowalczyk, Moreau & Co 44064.0 0 open wait HUMAN_WRITES T50 ['TOP50'] None
INV-25873 Eastman & Wexler CPAs 43680.0 15 overdue first HUMAN_WRITES T50 ['TOP50'] ['anika.langford@eastmanwexlercpas.example']
INV-25834 Delacroix, Jessop & Co 41568.0 22 overdue second HOLD  ['DISPUTE', 'OPEN_ESCALATION'] None
INV-25862 Thornfield Consulting Group 39456.0 17 overdue first DRAFT_REMINDER  [] ['nadia.vance@thornfieldconsultinggr.example']
INV-25822 Brandt Ashby IT 26112.0 24 overdue second HOLD  ['DISPUTE'] None
INV-25869 Hollis & Stanhope Advisory 22848.0 16 overdue first DRAFT_REMINDER  [] ['daniel.whitfield@hollisstanhopeadvisory.example']
INV-25848 Okafor Legal 19584.0 20 overdue first DRAFT_REMINDER  [] ['lucia.kessler@okaforlegal.example']
INV-25985 Yates, Oyelaran & Co 19368.0 0 open wait HUMAN_WRITES T50 ['TOP50'] None
INV-25885 Riverside Consulting Group 17136.0 12 overdue first DRAFT_REMINDER  [] ['quentin.bramwell@riversideconsultinggro.example']
INV-25883 Sinclair & Vance LLP 16320.0 13 overdue first DRAFT_REMINDER  [] ['tessa.bell@sinclairvancellp.example']
INV-25906 Rosales Engineering 16320.0 7 overdue first DRAFT_REMINDER  [] ['quentin.castell@rosalesengineering.example']
INV-26056 Kessler Consulting 15936.0 0 open wait HUMAN_WRITES T50 ['TOP50'] None
INV-25757 Ellery Consulting 13056.0 41 overdue second HOLD  ['DISPUTE'] None
INV-25859 Voss & Kowalczyk Agency 13056.0 18 overdue first DRAFT_REMINDER  [] ['quentin.moreau@vosskowalczykagency.example']
INV-26053 Greystone Engineering Group 11712.0 0 open wait HUMAN_WRITES T50 ['TOP50'] None
INV-25858 Glover Strategy 9600.0 18 overdue first DRAFT_REMINDER  ['RENEWAL_SOON'
… [result truncated, 6603 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline\ns=run_pipeline()\nimport collections as C\nprint(C.Counter(i['action'] for i in s['invoices']))\nfor i in s['invoices']:\n    if i['days_past_due']>0 or i['action']!='NO_ACTION':\n        print(i['invoice_id'],i['customer_name'][:28],i['amount'],i['days_past_due'],i['ar_status'],i['stage'],i['action'],'T50' if i['top50'] else '',[h['code'] for h in i['holds']],(i['draft'] or {}).get('to'))\n\" | cut -c1-260; for p in Reyes\\ Consulting Lindgren\\ Legal Studio\\ Finch Studio\\ Achebe Quill\\ \\&\\ Corbin Drummond\\ Consulting; do grep -c \"$p\" data/finance/ar_aging.csv; done",
 "description": "Dump pipeline invoice actions"
}
```

### Claude · 2026-11-20 17:34:58 UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_guardrails.py\" <<'EOF'\n\"\"\"Guardrail red-team. Runs the real pipeline, then re-runs it on MUTATED IN-MEMORY COPIES of the data\n(data/ is never written). Prints PASS/FAIL per check. Read-only for app/ (monkeypatching only, restored after).\"\"\"\nimport copy\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine import collections as coll, llm, pipeline  # noqa: E402\nfrom app.engine.data import load, norm_name  # noqa: E402\nfrom app.engine.rules import DEFAULT_RULES  # noqa: E402\n\nBASE = load()\nRES = []\n\n\ndef clone():\n    return {k: v.copy(deep=True) for k, v in BASE.items()}\n\n\ndef run(d=None, rules=None):\n    orig = pipeline.load\n    pipeline.load = (lambda: d) if d is not None else orig\n    try:\n        return pipeline.run_pipeline(copy.deepcopy(rules or DEFAULT_RULES))\n    finally:\n        pipeline.load = orig\n\n\ndef by_id(s):\n    return {i[\"invoice_id\"]: i for i in s[\"invoices\"]}\n\n\ndef check(name, ok, detail):\n    RES.append((name, \"PASS\" if ok else \"FAIL\", detail))\n    print(\"[%s] %s :: %s\" % (\"PASS\" if ok else \"FAIL\", name, detail))\n\n\ndef show(i):\n    return \"%s %s $%s %sdpd -> %s holds=%s to=%s\" % (i[\"invoice_id\"], i[\"customer_name\"], format(i[\"amount\"], \",.0f\"), i[\"days_past_due\"],\n                                                     i[\"action\"], [h[\"code\"] for h in i[\"holds\"]], (i[\"draft\"] or {}).get(\"to\"))\n\n\nbase = run()\nB = by_id(base)\ncus = BASE[\"customers\"]\n\n# ---- 1. Paidly ----------------------------------------------------------------------------------------------\nfor iid in (\"INV-25469\", \"INV-25852\", \"INV-25784\", \"INV-25806\", \"INV-25845\", \"INV-25867\"):\n    i = B[iid]\n    check(\"1 Paidly baseline \" + iid, i[\"draft\"] is None and i[\"action\"] in (\"HOLD\", \"NO_ACTION\"), show(i))\n# 1b. same receipts, payer name abbreviated the way 416 historical receipts are (truncated / surname only)\nfor pid, payer, iid in ((\"PAY-65766\", \"BRANDT\", \"INV-25806\"), (\"PAY-65750\", \"JESSOP\", \"INV-25784\"),\n                        (\"PAY-65805\", \"KINGSWAY\", \"INV-25469\"), (\"PAY-65750\", \"JESSOP ORWELL\", \"INV-25784\"),\n                        (\"PAY-65766\", \"BRANDT LOWELL\", \"INV-25806\")):\n    d = clone()\n    d[\"payments\"].loc[d[\"payments\"][\"payment_id\"] == pid, \"payer_name\"] = payer\n    s = run(d)\n    i = by_id(s)[iid]\n    p = [x for x in s[\"payments\"] if x[\"payment_id\"] == pid][0]\n    check(\"1b Paidly abbreviated payer '%s' (%s)\" % (payer, pid), i[\"draft\"] is None and i[\"action\"] in (\"HOLD\", \"NO_ACTION\"),\n          \"%s | cash agent: %s cust=%s inv=%s (%s)\" % (show(i), p[\"decision\"], p[\"customer_id\"], p[\"invoice_ids\"], p[\"reasons\"][0][:110]))\n\n# ---- 2. Open billing complaint --------------------------------------------------------------------------\ndisputed = list(pd.read_csv(os.path.join(ROOT, \"analysis\", \"work\", \"tickets_invoice_refs.csv\"))[\"invoice_id\"])\nbad = [B[x][\"invoice_id\"] for x in disputed if B[x][\"action\"] != \"HOLD\"]\ncheck(\"2 all 14 analyst-disputed invoices held\", not bad, \"not held: %s\" % bad)\nTARGET = \"INV-25862\"  # Thornfield Consulting Group, $39,456, DRAFT_REMINDER at baseline, no tickets\ncid = B[TARGET][\"customer_id\"]\ncrow = cus[cus[\"customer_id\"] == cid].iloc[0]\nINJ = {\n    \"a INV ref, polite question, no refusal\": (\"Billing\", \"normal\", \"open\", \"Question on INV-25862\", \"Hi, the seat count on INV-25862 looks higher than we expected. Could someone check?\"),\n    \"b ref without INV- prefix + refusal\": (\"Billing\", \"normal\", \"open\", \"Invoice 25862 wrong\", \"Invoice 25862 bills 40 seats, we have 28. We won't pay until it's fixed.\"),\n    \"c 'will not pay' (phrase not in list)\": (\"Billing\", \"normal\", \"open\", \"Wrong invoice\", \"Your latest invoice charges us for the old plan. We will not pay it until you correct it.\"),\n    \"d refusal but tagged How-to\": (\"How-to\", \"normal\", \"open\", \"invoice\", \"The invoice you sent us has the wrong seat count. We won't pay until it's fixed.\"),\n    \"e soft complaint, no ref, no refusal\": (\"Billing\", \"normal\", \"open\", \"Overcharged?\", \"We think we've been overcharged on our last Ledgerline invoice, the amount is double what we agreed. Please call me.\"),\n    \"f untagged, 'refuse to pay'\": (float(\"nan\"), \"normal\", \"open\", \"invoice\", \"We refuse to pay an invoice for seats we removed in August.\"),\n}\nfor label, (cat, pri, st, subj, body) in INJ.items():\n    d = clone()\n    row = {c: float(\"nan\") for c in d[\"tickets\"].columns}\n    row.update({\"ticket_id\": \"TQA%s\" % label[0], \"created_at\": pd.Timestamp(\"2026-10-28 10:00\"), \"customer_id\": cid, \"customer_name\": crow[\"name\"],\n                \"requester_email\": \"qa@\" + crow[\"domain\"], \"subject\": subj, \"body\": body, \"category\": cat, \"priority\": pri, \"status\": st, \"channel\": \"email\"})\n    d[\"tickets\"] = pd.concat([d[\"tickets\"], pd.DataFrame([row])], ignore_index=True)\n    i = by_id(run(d))[TARGET]\n    check(\"2%s\" % label, i[\"action\"] == \"HOLD\" or i[\"draft\"] is None, show(i))\n\n# ---- 3. Contacts who left never in \"to\" ----------------------------------------------------------------\ncon = BASE[\"contacts\"]\nleft = set(con[con[\"status\"] != \"active\"][\"email\"].str.lower())\nleaks = [(i[\"invoice_id\"], e) for i in base[\"invoices\"] if i[\"draft\"] for e in i[\"draft\"][\"to\"] if e.lower() in left]\nnd = sum(1 for i in base[\"invoices\"] if i[\"draft\"])\ncheck(\"3 no departed contact in any draft 'to'\", not leaks, \"%d drafts checked, leaks=%s\" %
… [tool input truncated]
```

### Tool · 2026-11-20 17:35:07 UTC
**Tool result:**
```
[PASS] 1 Paidly baseline INV-25469 :: INV-25469 Kingsway Engineering Group $5,100 111dpd -> HOLD holds=['MONEY_RECEIVED', 'ESCALATE_90', 'RENEWAL_SOON'] to=None
[PASS] 1 Paidly baseline INV-25852 :: INV-25852 Kingsway Engineering Group $5,100 19dpd -> HOLD holds=['MONEY_RECEIVED', 'RENEWAL_SOON'] to=None
[PASS] 1 Paidly baseline INV-25784 :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HOLD holds=['MONEY_RECEIVED', 'TOP50'] to=None
[PASS] 1 Paidly baseline INV-25806 :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> HOLD holds=['MONEY_RECEIVED'] to=None
[PASS] 1 Paidly baseline INV-25845 :: INV-25845 Castellano, Crane & Co $3,672 20dpd -> NO_ACTION holds=['PAID', 'RENEWAL_SOON'] to=None
[PASS] 1 Paidly baseline INV-25867 :: INV-25867 Yardley & Duarte Advisory $564 16dpd -> NO_ACTION holds=['PAID'] to=None
[FAIL] 1b Paidly abbreviated payer 'BRANDT' (PAY-65766) :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> DRAFT_REMINDER holds=[] to=['aisha.garrick@brandtlowellcpas.example'] | cash agent: EXCEPTION cust=C1286 inv=[] (Payer name is closest to 'Studio Brandt' (similarity 0.55))
[FAIL] 1b Paidly abbreviated payer 'JESSOP' (PAY-65750) :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HUMAN_WRITES holds=['TOP50'] to=['joel.okafor@jessoporwellagency.example'] | cash agent: EXCEPTION cust=C1402 inv=[] (Payer name is closest to 'Jessop Legal' (similarity 0.57))
[FAIL] 1b Paidly abbreviated payer 'KINGSWAY' (PAY-65805) :: INV-25469 Kingsway Engineering Group $5,100 111dpd -> HUMAN_WRITES holds=['ESCALATE_90', 'RENEWAL_SOON'] to=['marcus.tan@kingswayengineeringgro.example'] | cash agent: EXCEPTION cust=None inv=[] (Payer name is ambiguous between several customers: Kingsway Digital (0.57), Kingsway Creative (0.56))
[PASS] 1b Paidly abbreviated payer 'JESSOP ORWELL' (PAY-65750) :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HOLD holds=['MONEY_RECEIVED', 'TOP50'] to=None | cash agent: PROPOSE cust=C1273 inv=['INV-25784'] (Payer name is closest to 'Jessop & Orwell Agency' (similarity 0.68))
[PASS] 1b Paidly abbreviated payer 'BRANDT LOWELL' (PAY-65766) :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> HOLD holds=['MONEY_RECEIVED'] to=None | cash agent: PROPOSE cust=C1126 inv=['INV-25806'] (Payer name is closest to 'Brandt & Lowell CPAs' (similarity 0.70))
[PASS] 2 all 14 analyst-disputed invoices held :: not held: []
[PASS] 2a INV ref, polite question, no refusal :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> HOLD holds=['DISPUTE'] to=None
[P
… [result truncated, 26165 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_guardrails.py\" <<'EOF'\n\"\"\"Guardrail red-team. Runs the real pipeline, then re-runs it on MUTATED IN-MEMORY COPIES of the data\n(data/ is never written). Prints PASS/FAIL per check. Read-only for app/ (monkeypatching only, restored after).\"\"\"\nimport copy\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine import collections as coll, llm, pipeline  # noqa: E402\nfrom app.engine.data import load, norm_name  # noqa: E402\nfrom app.engine.rules import DEFAULT_RULES  # noqa: E402\n\nBASE = load()\nRES = []\n\n\ndef clone():\n    return {k: v.copy(deep=True) for k, v in BASE.items()}\n\n\ndef run(d=None, rules=None):\n    orig = pipeline.load\n    pipeline.load = (lambda: d) if d is not None else orig\n    try:\n        return pipeline.run_pipeline(copy.deepcopy(rules or DEFAULT_RULES))\n    finally:\n        pipeline.load = orig\n\n\ndef by_id(s):\n    return {i[\"invoice_id\"]: i for i in s[\"invoices\"]}\n\n\ndef check(name, ok, detail):\n    RES.append((name, \"PASS\" if ok else \"FAIL\", detail))\n    print(\"[%s] %s :: %s\" % (\"PASS\" if ok else \"FAIL\", name, detail))\n\n\ndef show(i):\n    return \"%s %s $%s %sdpd -> %s holds=%s to=%s\" % (i[\"invoice_id\"], i[\"customer_name\"], format(i[\"amount\"], \",.0f\"), i[\"days_past_due\"],\n                                                     i[\"action\"], [h[\"code\"] for h in i[\"holds\"]], (i[\"draft\"] or {}).get(\"to\"))\n\n\nbase = run()\nB = by_id(base)\ncus = BASE[\"customers\"]\n\n# ---- 1. Paidly ----------------------------------------------------------------------------------------------\nfor iid in (\"INV-25469\", \"INV-25852\", \"INV-25784\", \"INV-25806\", \"INV-25845\", \"INV-25867\"):\n    i = B[iid]\n    check(\"1 Paidly baseline \" + iid, i[\"draft\"] is None and i[\"action\"] in (\"HOLD\", \"NO_ACTION\"), show(i))\n# 1b. same receipts, payer name abbreviated the way 416 historical receipts are (truncated / surname only)\nfor pid, payer, iid in ((\"PAY-65766\", \"BRANDT\", \"INV-25806\"), (\"PAY-65750\", \"JESSOP\", \"INV-25784\"),\n                        (\"PAY-65805\", \"KINGSWAY\", \"INV-25469\"), (\"PAY-65750\", \"JESSOP ORWELL\", \"INV-25784\"),\n                        (\"PAY-65766\", \"BRANDT LOWELL\", \"INV-25806\")):\n    d = clone()\n    d[\"payments\"].loc[d[\"payments\"][\"payment_id\"] == pid, \"payer_name\"] = payer\n    s = run(d)\n    i = by_id(s)[iid]\n    p = [x for x in s[\"payments\"] if x[\"payment_id\"] == pid][0]\n    check(\"1b Paidly abbreviated payer '%s' (%s)\" % (payer, pid), i[\"draft\"] is None and i[\"action\"] in (\"HOLD\", \"NO_ACTION\"),\n          \"%s | cash agent: %s cust=%s inv=%s (%s)\" % (show(i), p[\"decision\"], p[\"customer_id\"], p[\"invoice_ids\"], p[\"reasons\"][0][:110]))\n\n# ---- 2. Open billing complaint --------------------------------------------------------------------------\ndisputed = list(pd.read_csv(os.path.join(ROOT, \"analysis\", \"work\", \"tickets_invoice_refs.csv\"))[\"invoice_id\"])\nbad = [B[x][\"invoice_id\"] for x in disputed if B[x][\"action\"] != \"HOLD\"]\ncheck(\"2 all 14 analyst-disputed invoices held\", not bad, \"not held: %s\" % bad)\nTARGET = \"INV-25862\"  # Thornfield Consulting Group, $39,456, DRAFT_REMINDER at baseline, no tickets\ncid = B[TARGET][\"customer_id\"]\ncrow = cus[cus[\"customer_id\"] == cid].iloc[0]\nINJ = {\n    \"a INV ref, polite question, no refusal\": (\"Billing\", \"normal\", \"open\", \"Question on INV-25862\", \"Hi, the seat count on INV-25862 looks higher than we expected. Could someone check?\"),\n    \"b ref without INV- prefix + refusal\": (\"Billing\", \"normal\", \"open\", \"Invoice 25862 wrong\", \"Invoice 25862 bills 40 seats, we have 28. We won't pay until it's fixed.\"),\n    \"c 'will not pay' (phrase not in list)\": (\"Billing\", \"normal\", \"open\", \"Wrong invoice\", \"Your latest invoice charges us for the old plan. We will not pay it until you correct it.\"),\n    \"d refusal but tagged How-to\": (\"How-to\", \"normal\", \"open\", \"invoice\", \"The invoice you sent us has the wrong seat count. We won't pay until it's fixed.\"),\n    \"e soft complaint, no ref, no refusal\": (\"Billing\", \"normal\", \"open\", \"Overcharged?\", \"We think we've been overcharged on our last Ledgerline invoice, the amount is double what we agreed. Please call me.\"),\n    \"f untagged, 'refuse to pay'\": (float(\"nan\"), \"normal\", \"open\", \"invoice\", \"We refuse to pay an invoice for seats we removed in August.\"),\n}\nfor label, (cat, pri, st, subj, body) in INJ.items():\n    d = clone()\n    row = {c: float(\"nan\") for c in d[\"tickets\"].columns}\n    row.update({\"ticket_id\": \"TQA%s\" % label[0], \"created_at\": pd.Timestamp(\"2026-10-28 10:00\"), \"customer_id\": cid, \"customer_name\": crow[\"name\"],\n                \"requester_email\": \"qa@\" + crow[\"domain\"], \"subject\": subj, \"body\": body, \"category\": cat, \"priority\": pri, \"status\": st, \"channel\": \"email\"})\n    d[\"tickets\"] = pd.concat([d[\"tickets\"], pd.DataFrame([row])], ignore_index=True)\n    i = by_id(run(d))[TARGET]\n    check(\"2%s\" % label, i[\"action\"] == \"HOLD\" or i[\"draft\"] is None, show(i))\n\n# ---- 3. Contacts who left never in \"to\" ----------------------------------------------------------------\ncon = BASE[\"contacts\"]\nleft = set(con[con[\"status\"] != \"active\"][\"email\"].str.lower())\nleaks = [(i[\"invoice_id\"], e) for i in base[\"invoices\"] if i[\"draft\"] for e in i[\"draft\"][\"to\"] if e.lower() in left]\nnd = sum(1 for i in base[\"invoices\"] if i[\"draft\"])\ncheck(\"3 no departed contact in any draft 'to'\", not leaks, \"%d drafts checked, leaks=%s\" %
… [tool input truncated]
```

### Claude · 2026-11-20 17:35:17 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -la app/engine/ && grep -n \"claude_read\\|ask_json\\|use_claude\" app/engine/*.py",
 "description": "Check for concurrent changes to engine files"
}
```

### Tool · 2026-11-20 17:35:18 UTC
**Tool result:**
```
total 128
drwxr-xr-x@ 13 jacekmaterna  staff   416 Nov 20 11:35 .
drwxr-xr-x@  8 jacekmaterna  staff   256 Nov 20 11:27 ..
-rw-r--r--@  1 jacekmaterna  staff     0 Nov 20 11:21 __init__.py
-rw-r--r--@  1 jacekmaterna  staff  7929 Nov 20 11:22 cash_app.py
-rw-r--r--@  1 jacekmaterna  staff  6624 Nov 20 11:28 collections.py
-rw-r--r--@  1 jacekmaterna  staff  9294 Nov 20 11:30 context.py
-rw-r--r--@  1 jacekmaterna  staff  7066 Nov 20 11:20 controller.py
-rw-r--r--@  1 jacekmaterna  staff  3581 Nov 20 11:35 data.py
-rw-r--r--@  1 jacekmaterna  staff  2297 Nov 20 11:29 digest.py
-rw-r--r--@  1 jacekmaterna  staff  2694 Nov 20 11:25 llm.py
drwxr-xr-x@  4 jacekmaterna  staff   128 Nov 20 11:21 manuals
-rw-r--r--@  1 jacekmaterna  staff  8723 Nov 20 11:29 pipeline.py
-rw-r--r--@  1 jacekmaterna  staff  3653 Nov 20 11:25 rules.py
app/engine/context.py:67:def claude_read(t, own_invoices, customer_name, enabled):
app/engine/context.py:81:    r = llm.ask_json("ticket_read_v1", system, user, enabled=enabled)
app/engine/context.py:94:    use_claude = bool(rules.get("use_claude", False))
app/engine/context.py:106:            read = claude_read(td, own, c["name"], use_claude) or heuristic_read(td, own)
app/engine/collections.py:70:    # Personalise with Claude (only when Legal has approved: use_claude defaults to False).
app/engine/collections.py:73:    if rules.get("use_claude", False):
app/engine/collections.py:83:        r = llm.ask_json("draft_v2", system, user, enabled=True, max_tokens=700)
app/engine/llm.py:3:If ANTHROPIC_API_KEY is not set (or use_claude is off), every call returns None and callers fall back to
app/engine/llm.py:43:def ask_json(task, system, user, enabled=True, max_tokens=900):
app/engine/rules.py:23:    "use_claude": False,                  # OFF until Legal signs the DPA (Maya, T+0:17). Rules + templates work without it
app/engine/rules.py:40:    "use_claude": "Use Claude to read tickets and draft reminders. Keep OFF until Legal approves the DPA (Bedrock route preferred). Off = rules and templates",
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -la app/engine/ && grep -n \"claude_read\\|ask_json\\|use_claude\" app/engine/*.py",
 "description": "Check for concurrent changes to engine files"
}
```

### Claude · 2026-11-20 17:35:22 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && date; sed -n 1,90p app/engine/context.py | sed -n 13,90p; cat -n app/engine/data.py | sed -n 40,95p",
 "description": "Re-read changed context.py and data.py"
}
```

### Tool · 2026-11-20 17:35:23 UTC
**Tool result:**
```
Fri Nov 20 11:35:23 CST 2026
AGENT = "Account Context"

REFUSAL = [r"won'?t (?:be )?pay", r"wont (?:be )?pay", r"not (?:be )?paying", r"not authori[sz]ing payment", r"payment is on hold",
           r"paused payment", r"unable to process payment", r"settle once", r"won'?t pay an invoice", r"until (?:it'?s|its) fixed",
           r"void it", r"cancel and reissue", r"issue a revised invoice", r"remove it and resend", r"we are not paying",
           r"payment (?:is )?on hold", r"pending a corrected invoice", r"not paying for", r"not before", r"we'?ll pay once",
           r"put the whole th", r"reissue it"]
LEGAL = [r"chargeback", r"contest(?:ing)? the charge", r"consumer affairs", r"lawyer", r"attorney", r"legal action", r"small claims", r"solicitor"]
CANCEL = [r"discontinu\w+ ledgerline", r"termination of services", r"notice of termination", r"cancel(?:l)?ing (?:our )?(?:ledgerline|subscription|account)",
          r"no further direct debits"]
COLLECTIONS_COMPLAINT = [r"already paid", r"chas(?:ed|ing) (?:us|me)", r"reminder (?:email|emails)", r"overdue notice", r"final notice", r"threaten"]


def _any(patterns, text):
    return [p for p in patterns if re.search(p, text, flags=re.I)]


def heuristic_read(t, own_invoices):
    text = "%s\n%s" % (t.get("subject", ""), t.get("body", ""))
    refs = sorted(set(re.findall(r"INV-\d{5}", text)))
    own_refs = [r for r in refs if r in own_invoices]
    refusal, legal, cancel = _any(REFUSAL, text), _any(LEGAL, text), _any(CANCEL, text)
    complaint = _any(COLLECTIONS_COMPLAINT, text)
    kind = "other"
    if legal:
        kind = "legal_threat"
    elif cancel:
        kind = "cancellation"
    elif own_refs:
        # A customer quoting one of their own open Ledgerline invoice numbers is almost always raising a problem with it,
        # whatever category the agent tagged (data shows disputes tagged How-to or untagged).
        kind = "dispute"
    elif refusal and str(t.get("category")) in ("Billing", "Account change"):
        kind = "dispute"
    about = bool(own_refs or legal or cancel or (refusal and str(t.get("category")) in ("Billing", "Account change")))
    return {
        "about_ledgerline_invoice": about,
        "invoice_ids": own_refs,
        "kind": kind if about else ("product_question" if not complaint else "collections_complaint"),
        "refuses_to_pay_until_fixed": bool(refusal),
        "collections_complaint": bool(complaint),
        "summary": (t.get("subject") or "")[:120],
        "
… [result truncated, 6815 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && date; sed -n 1,90p app/engine/context.py | sed -n 13,90p; cat -n app/engine/data.py | sed -n 40,95p",
 "description": "Re-read changed context.py and data.py"
}
```

### Claude · 2026-11-20 17:35:47 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nr=pd.read_csv('analysis/work/eval_cash_app_results.csv')\nw=r[(~r.is_synthetic)&(~r.customer_correct)]\nprint(w[['payment_id','payer_name','decision','pred_customer','true_customer','pred','truth']].to_string())\nfrom app.engine.data import load, AS_OF\nfrom app.engine.pipeline import COMPLAINT_RX\nd=load(); t=d['tickets']\nh=t[(t.created_at>=AS_OF-pd.Timedelta(days=120)) & t.body.fillna('').str.contains(COMPLAINT_RX,case=False,regex=True)]\nfor _,x in h.iterrows(): print('--',x.ticket_id,x.created_at.date(),x.customer_name,x.category,x.status,'|',x.subject,'|',x.body[:200].replace(chr(10),' '))\n\"; grep -n \"cash_by_customer\\|customer_id\\\"\\]:\" app/engine/pipeline.py app/engine/controller.py | head; grep -n \"scored\\[0\\]\\[0\\] - scored\\|s > 0.55\" app/engine/cash_app.py; grep -n \"dispute_lookback_days\\|lookback\" app/engine/*.py | head",
 "description": "Customer misidentifications and keyword complaint hits"
}
```

### Tool · 2026-11-20 17:35:49 UTC
**Tool result:**
```
   payment_id payer_name   decision pred_customer true_customer pred      truth
8   PAY-60256        TAN  EXCEPTION           NaN         C1133  NaN  INV-20228
10  PAY-60319   OYELARAN  EXCEPTION           NaN         C1148  NaN  INV-20297
12  PAY-60371    ROSALES  EXCEPTION           NaN         C1233  NaN  INV-20314
14  PAY-60611       HUME  EXCEPTION           NaN         C1210  NaN  INV-20604
19  PAY-61064  PEMBERTON  EXCEPTION         C1235         C1337  NaN  INV-21043
27  PAY-61447      ASHBY  EXCEPTION           NaN         C1145  NaN  INV-21458
54  PAY-63559      CRANE  EXCEPTION           NaN         C1380  NaN  INV-23576
62  PAY-64181   OYELARAN  EXCEPTION           NaN         C1148  NaN  INV-24224
65  PAY-64429  LINDQVIST  EXCEPTION           NaN         C1460  NaN  INV-24499
68  PAY-64609   CALLOWAY  EXCEPTION           NaN         C1371  NaN  INV-24703
73  PAY-65045    ROSALES  EXCEPTION           NaN         C1233  NaN  INV-24979
75  PAY-65184    KESSLER  EXCEPTION           NaN         C1366  NaN  INV-25299
-- T880061 2026-07-08 Abbott Oyelaran Law How-to solved | Enquiry | Morning,  We bill a couple of clients in French. Could the reminder emails go out in French for just those clients and stay English for everyone else?  Milan
-- T880107 2026-07-13 Hale Legal Bug solved | Duplicate invoices sent to entire client list | Hello,  Sorry to be blunt, but this is a disaster. This morning's billing run sent every client two copies of their invoice, and some got three. We're a law firm, our clients are not amused, and two o
-- T880255 2026-07-28 Moreau & Crane Agency nan solved | Help | Hi,  A client paid us by cheque three weeks ago and we deposited it, but the invoice still shows as outstanding and they keep getting reminder emails. How do I record the payment so the reminders stop
-- T880256 2026-07-28 Castellano Langford Chartered Accountants nan solved | Hoping you can help | got a pretty angry reply to an overdue notice today from someone who says they've told us twice they're not the right person. they're right, they're not on the account anymore. embarrassing
-- T880259 2026-07-29 Riverside Consulting Group How-to solved | typo in reminder email | Hi team,  small thing - default reminder email says 'recieved'. not urgent, just noticed it
-- T880373 2026-08-12 Highmoor Engineering Group Billing solved | A few questions | Hi,  Why is there a charge for $41.17 dated the 12th? Our subscription renews on the 1st and we already paid for this m
… [result truncated, 5382 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nr=pd.read_csv('analysis/work/eval_cash_app_results.csv')\nw=r[(~r.is_synthetic)&(~r.customer_correct)]\nprint(w[['payment_id','payer_name','decision','pred_customer','true_customer','pred','truth']].to_string())\nfrom app.engine.data import load, AS_OF\nfrom app.engine.pipeline import COMPLAINT_RX\nd=load(); t=d['tickets']\nh=t[(t.created_at>=AS_OF-pd.Timedelta(days=120)) & t.body.fillna('').str.contains(COMPLAINT_RX,case=False,regex=True)]\nfor _,x in h.iterrows(): print('--',x.ticket_id,x.created_at.date(),x.customer_name,x.category,x.status,'|',x.subject,'|',x.body[:200].replace(chr(10),' '))\n\"; grep -n \"cash_by_customer\\|customer_id\\\"\\]:\" app/engine/pipeline.py app/engine/controller.py | head; grep -n \"scored\\[0\\]\\[0\\] - scored\\|s > 0.55\" app/engine/cash_app.py; grep -n \"dispute_lookback_days\\|lookback\" app/engine/*.py | head",
 "description": "Customer misidentifications and keyword complaint hits"
}
```

### Claude · 2026-11-20 17:36:01 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -c \"Highmoor\" data/finance/ar_aging.csv; grep \"Drummond Consulting\\|Ambrose & Lowell\\|Kingsway Engineering\" data/finance/ar_aging.csv; .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('data/support/tickets.csv')\nfor n in ['Ambrose & Lowell Advisory','Kingsway Engineering Group','Drummond Consulting','Reyes Consulting']:\n    x=t[t.customer_name==n]\n    for _,r in x.iterrows(): print(n,'|',r.ticket_id,r.created_at,r.category,r.priority,r.status,'|',r.subject,'|',str(r.body)[:160].replace(chr(10),' '))\np=pd.read_csv('data/finance/payments.csv'); print(p[p.payer_name.str.upper().str.contains('DRUMMOND CONSULTING')].tail(4).to_string())\nc=pd.read_csv('data/customers/customers.csv'); print(c[c.name.str.contains('Jessop')][['customer_id','name','current_arr']].to_string())\n\"",
 "description": "Look up Ambrose, Kingsway, Drummond, Reyes tickets"
}
```

### Tool · 2026-11-20 17:36:03 UTC
**Tool result:**
```
0
INV-25469,C1469,Kingsway Engineering Group,Growth,2026-06-12,2026-07-12,5100.00,111,Over 90 days,overdue
INV-25769,C1492,Drummond Consulting,Core,2026-08-24,2026-08-24,658.00,68,61-90 days,payment_failed
INV-25852,C1469,Kingsway Engineering Group,Growth,2026-09-12,2026-10-12,5100.00,19,1-30 days,overdue
INV-25897,C1407,Ambrose & Lowell Advisory,Core,2026-09-21,2026-10-21,658.00,10,1-30 days,overdue
INV-26029,C1407,Ambrose & Lowell Advisory,Core,2026-10-21,2026-11-20,658.00,0,Not yet due,open
Ambrose & Lowell Advisory | T880152 2026-07-17 09:16 nan normal pending | (no subject) | Hello,  We're opening a satellite office in Bristol and need a new location added so staff there can raise invoices with the local address in the footer.
Ambrose & Lowell Advisory | T880474 2026-08-24 16:10 Bug high pending | ??? | Card payments are going through, money is arriving, but the invoices stay marked unpaid in Ledgerline. My team spent this morning matching them manually. Someth
Kingsway Engineering Group | T880078 2026-07-09 23:32 Billing low solved | Not working? | If I void an invoice, is that number gone for good or does it get reused?  Oscar
Kingsway Engineering Group | T880184 2026-07-20 20:13 nan normal pending | Can you check something for me | Hi there - The amount the client sees in the portal is 1,950.00 AUD but the PDF they downloaded says 1,949.99. Which one is right? They want to pay today.  Sign
Kingsway Engineering Group | T880284 2026-07-31 19:36 How-to normal solved | Query regarding our setup | Does the CRM integration bring in the company owner field? We use it to assign the account lead.
Drummond Consulting | T880019 2026-07-02 16:28 Billing low solved | DISPUTING CHARGES WITH MY BANK | You billed us twice for the annual plan and nobody has answered in 9 days. I've opened a chargeback on both payments. Fix it or don't, im past caring at this po
Reyes Consulting | T880132 2026-07-15 20:20 Billing normal solved | (no subject) | Sent an invoice yesterday to the wrong contact with the wrong amount on it. Do I void it and raise a new one, or just correct it? I don't want to mess up the se
Reyes Consulting | T880342 2026-08-07 14:12 How-to normal solved | query | Can two-factor codes come by text message instead of an app? A couple of our partners would really rather not install anything extra on their phones.
Reyes Consulting | T880522 2026-08-31 05:58 How-to low solved | Help with our account | Morning,  Do milestone invoices sync as a single invoice o
… [result truncated, 4149 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -c \"Highmoor\" data/finance/ar_aging.csv; grep \"Drummond Consulting\\|Ambrose & Lowell\\|Kingsway Engineering\" data/finance/ar_aging.csv; .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('data/support/tickets.csv')\nfor n in ['Ambrose & Lowell Advisory','Kingsway Engineering Group','Drummond Consulting','Reyes Consulting']:\n    x=t[t.customer_name==n]\n    for _,r in x.iterrows(): print(n,'|',r.ticket_id,r.created_at,r.category,r.priority,r.status,'|',r.subject,'|',str(r.body)[:160].replace(chr(10),' '))\np=pd.read_csv('data/finance/payments.csv'); print(p[p.payer_name.str.upper().str.contains('DRUMMOND CONSULTING')].tail(4).to_string())\nc=pd.read_csv('data/customers/customers.csv'); print(c[c.name.str.contains('Jessop')][['customer_id','name','current_arr']].to_string())\n\"",
 "description": "Look up Ambrose, Kingsway, Drummond, Reyes tickets"
}
```

### Claude · 2026-11-20 17:36:13 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn \"hold_on_open_ticket_days\\|writeoff_threshold\\|renewal_notice\\|amount_tolerance\" app/ --include=*.py | grep -v \"rules.py\"; grep -n \"OPEN_ESCALATION\" -A4 app/engine/controller.py | head -8; grep -n \"open_tickets\" app/engine/context.py",
 "description": "Check whether rule settings are used"
}
```

### Tool · 2026-11-20 17:36:13 UTC
**Tool result:**
```
(eval):1: no matches found: --include=*.py
7:HARD_HOLDS = {"MONEY_RECEIVED", "DISPUTE", "CANCELLATION", "OPEN_ESCALATION", "NO_VALID_CONTACT"}
8-HUMAN_CODES = {"LEGAL_RISK", "TOP50", "ESCALATE_90", "CARD_WRITEOFF_SOON"}
9-
10-
11-def holds_for(inv, ctx, cash_by_invoice, cash_by_customer, rules):
--
57:            holds.append({"code": "OPEN_ESCALATION", "label": "Open high-priority support ticket",
58-                          "detail": "%s '%s' is %s (%s priority). Policy: don't chase during an open escalation until the AM says so." % (t["ticket_id"], t["subject"], t["status"], t["priority"]),
150:            "open_tickets": [t for t in tickets if t["status"] in ("open", "pending")],
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn \"hold_on_open_ticket_days\\|writeoff_threshold\\|renewal_notice\\|amount_tolerance\" app/ --include=*.py | grep -v \"rules.py\"; grep -n \"OPEN_ESCALATION\" -A4 app/engine/controller.py | head -8; grep -n \"open_tickets\" app/engine/context.py",
 "description": "Check whether rule settings are used"
}
```

### Claude · 2026-11-20 17:36:18 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn \"hold_on_open_ticket_days\\|writeoff_threshold\\|renewal_notice_days\\|amount_tolerance\" app/engine/ app/web/ app/*.py | grep -v \"engine/rules.py\"; grep -n \"open_tickets\\|hold_on\" app/engine/controller.py",
 "description": "Search rule key usage across app"
}
```

### Tool · 2026-11-20 17:36:18 UTC
**Tool result:**
```
app/engine/context.py:138:            if 0 <= days <= int(rules.get("renewal_notice_days", 45)):
app/engine/cash_app.py:61:    tol = float(rules.get("amount_tolerance", 0) or 0)
app/engine/cash_app.py:100:                reasons.append("Short by $%.2f, which looks like a bank fee. Needs approval to write off (threshold $%.0f)" % (-diff, float(rules.get("writeoff_threshold", 0))))
app/web/fake_state.py:17:    "writeoff_threshold": 0.0,
app/web/fake_state.py:18:    "amount_tolerance": 0.0,
app/web/fake_state.py:21:    "hold_on_open_ticket_days": 30,
app/web/views.py:49:    "writeoff_threshold": ("Write-off threshold ($)",
app/web/views.py:52:    "amount_tolerance": ("Amount tolerance ($)",
app/web/views.py:58:    "hold_on_open_ticket_days": ("Hold on tickets opened in the last N days",
app/web/views.py:69:    "renewal_notice_days": ("Renewal window (days)",
app/web/views.py:298:    if isinstance(new.get("writeoff_threshold"), (int, float)) and new["writeoff_threshold"] < 0:
app/web/views.py:300:    if isinstance(new.get("amount_tolerance"), (int, float)) and new["amount_tolerance"] < 0:
55:    for t in (ctx or {}).get("open_tickets", []):
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn \"hold_on_open_ticket_days\\|writeoff_threshold\\|renewal_notice_days\\|amount_tolerance\" app/engine/ app/web/ app/*.py | grep -v \"engine/rules.py\"; grep -n \"open_tickets\\|hold_on\" app/engine/controller.py",
 "description": "Search rule key usage across app"
}
```

### Claude · 2026-11-20 17:36:32 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && date && .venv/bin/python analysis/scripts/eval_cash_app.py > analysis/work/eval_cash_app.log 2>&1; head -14 analysis/work/eval_cash_app.log | cut -c1-230; .venv/bin/python analysis/scripts/eval_controller.py > analysis/work/eval_controller.log 2>&1; head -12 analysis/work/eval_controller.log; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -v \"^\\[llm\\]\" > analysis/work/eval_guardrails.log; grep -c PASS analysis/work/eval_guardrails.log; grep \"FAIL\\|SUMMARY\" analysis/work/eval_guardrails.log | cut -c1-200; .venv/bin/python -m app.engine.pipeline | head -14",
 "description": "Re-run all eval scripts for final numbers"
}
```

### Tool · 2026-11-20 17:36:49 UTC
**Tool result:**
```
Fri Nov 20 11:36:32 CST 2026
=== REAL ===
real: all                    n=246 | auto  81 (prec 100.0%) | propose 153 (top1 98.0%) | exception  12 (5%) | end-to-end correct 93.9% | customer correct 95.1%
real: trivial                n= 20 | auto  20 (prec 100.0%) | propose   0 (top1 n/a) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: easy                   n= 63 | auto  61 (prec 100.0%) | propose   2 (top1 100.0%) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: medium                 n= 83 | auto   0 (prec n/a) | propose  83 (top1 100.0%) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: hard                   n= 80 | auto   0 (prec n/a) | propose  68 (top1 95.6%) | exception  12 (15%) | end-to-end correct 81.2% | customer correct 85.0%
=== SYNTHETIC ===
synthetic: all               n= 40 | auto   0 (prec n/a) | propose  24 (top1 95.8%) | exception  16 (40%) | end-to-end correct 57.5% | customer correct 100.0%
synthetic: bank_fee          n= 10 | auto   0 (prec n/a) | propose   5 (top1 100.0%) | exception   5 (50%) | end-to-end correct 50.0% | customer correct 100.0%
synthetic: rounding          n= 10 | auto   0 (prec n/a) | propose   9 (top1 100.0%) | exception   1 (10%) | end-to-end correct 90.0% | customer correct 100.0%
synthetic: short_pay         n= 10 | auto   0 (prec n/a) | propose   7 (top1 100.0%) | exception   3 (30%) | end-to-end correct 70.0% | customer correct 100.0%
synthetic: combined          n= 10 | auto   0 (prec n/a) | propose   3 (top1 66.7%) | exception   7 (70%) | end-to-end correct 20.0% | customer correct 100.0%

Wrong AUTO_APPLY rows:
Analyst disputed overdue invoices: 14 Pipeline flagged (DISPUTE/CANCEL/LEGAL): 15
TP 14 FP ['INV-25973'] FN []
precision 93.3% recall 100.0%
DISPUTE code only: pred 14 TP 14 FP [] FN []
Analyst-disputed invoices NOT in HOLD: []
FP detail: INV-25973 Eastman Engineering 3264.0 HUMAN_WRITES [('LEGAL_RISK', 'T880519 (2026-08-30, status solved): Auto-renewed at 35% more without warning. VP Finance must handle; no automated message.')]

All tickets: 1041 flagged about_ledgerline_invoice: 22
kind
dispute         16
legal_threat     4
cancellation     2
45
[FAIL] 1b Paidly abbreviated payer 'BRANDT' (PAY-65766) :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> DRAFT_REMINDER holds=[] to=['aisha.garrick@brandtlowellcpas.example'] | cash agent: EXCEPTION 
[FAIL] 1b Paidly abbreviated payer 'JESSOP' (PAY-65750) :: IN
… [result truncated, 4302 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && date && .venv/bin/python analysis/scripts/eval_cash_app.py > analysis/work/eval_cash_app.log 2>&1; head -14 analysis/work/eval_cash_app.log | cut -c1-230; .venv/bin/python analysis/scripts/eval_controller.py > analysis/work/eval_controller.log 2>&1; head -12 analysis/work/eval_controller.log; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -v \"^\\[llm\\]\" > analysis/work/eval_guardrails.log; grep -c PASS analysis/work/eval_guardrails.log; grep \"FAIL\\|SUMMARY\" analysis/work/eval_guardrails.log | cut -c1-200; .venv/bin/python -m app.engine.pipeline | head -14",
 "description": "Re-run all eval scripts for final numbers"
}
```

### Claude · 2026-11-20 17:37:00 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -c \"Castellano Langford\\|Quill & Corbin\\|Highmoor\" data/finance/ar_aging.csv; grep -n \"already_paid\\|paid_or_received\" app/engine/pipeline.py | head -3",
 "description": "Check AR for missed-ticket customers"
}
```

### Tool · 2026-11-20 17:37:00 UTC
**Tool result:**
```
0
96:    paid_or_received = sum(i["amount"] for i in overdue if any(h["code"] in ("PAID", "MONEY_RECEIVED") for h in i["holds"]))
110:        "overdue_already_paid": paid_or_received,
112:        "overdue_collectable": ledger_overdue - paid_or_received - disputed,
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -c \"Castellano Langford\\|Quill & Corbin\\|Highmoor\" data/finance/ar_aging.csv; grep -n \"already_paid\\|paid_or_received\" app/engine/pipeline.py | head -3",
 "description": "Check AR for missed-ticket customers"
}
```

### Claude · 2026-11-20 17:37:02 UTC
Now I'll write EVAL.md.

### Claude · 2026-11-20 17:38:03 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/EVAL.md",
 "content": "# EVAL: how well the agents work on the real records\n\nQA Evaluator. Run on 2026-11-20 at 11:36 CST against the code as it stood then. The builder was still editing:\n`context.py` and `data.py` changed during the run, so the numbers were re-run at 11:36. Data as of 2026-10-31.\nNothing in `app/` or `data/` was changed. The scripts are re-runnable:\n\n| script | what it does | output |\n|---|---|---|\n| `analysis/scripts/eval_cash_app.py` | replays the 286 test payments against the invoice book as it stood on each received date | `analysis/work/eval_cash_app_results.csv`, `.log` |\n| `analysis/scripts/eval_controller.py` | checks dispute detection against the analyst's list, and reads all 1,041 tickets | `analysis/work/eval_ticket_reads.csv`, `eval_ticket_sample_*.csv`, `.log` |\n| `analysis/scripts/eval_guardrails.py` | red-teams the real pipeline using changed copies of the data held in memory | `analysis/work/eval_guardrails_results.csv`, `.log` |\n\n**Headline**\n- **0 wrong automatic applications in 81** (real data).\n- Proposals put the right invoice first 98.0% of the time (real data).\n- The Controller held all 14 of the analyst's disputed invoices (recall 100%).\n- **44 of 54 guardrail checks pass.** The 10 failures fall into three gaps:\n  - a receipt whose customer cannot be identified blocks nothing (the Paidly case returns);\n  - complaint wording outside the keyword lists gets through;\n  - the banned-phrase list is narrow.\n\n---\n\n## 1. Cash Application (test set `analysis/testset_cash_app.csv`, 286 rows)\n\n**Harness.** For each test payment, the invoice book is rebuilt as it stood on the receipt date. An invoice counts as\nopen if `issue_date <= received_date` and (`paid_date` is blank or `paid_date >= received_date`). The payment is\nthen fed in as the only unapplied receipt, and the **production `cash_app.run()` is called unchanged** with\nDEFAULT_RULES, so no rule is re-implemented. An answer counts as correct when the proposed invoice set equals the\nlabel. For PAY-65805 (Kingsway), which is ambiguous, either invoice is accepted.\n\n### Real rows (246)\n| difficulty | n | auto-applied | auto precision | proposed | proposal top-1 | exception | exception rate | end-to-end correct |\n|---|---|---|---|---|---|---|---|---|\n| trivial (card) | 20 | 20 | **100%** | 0 | n/a | 0 | 0% | 100% |\n| easy (memo ref) | 63 | 61 | **100%** | 2 | 100% | 0 | 0% | 100% |\n| medium (no ref, unique amount) | 83 | 0 | n/a | 83 | 100% | 0 | 0% | 100% |\n| hard (same-amount ties / truncated payer) | 80 | 0 | n/a | 68 | 95.6% | 12 | 15% | 81.2% |\n| **all real** | **246** | **81** | **100% (81/81)** | **153** | **98.0% (150/153)** | **12** | **4.9%** | **93.9%** |\n\n- **Severity-1 check (wrong auto-apply): none.** Every auto-apply needs an exact amount, an invoice reference in the\n  memo, and that invoice belonging to the identified customer.\n- Two easy rows were proposed rather than auto-applied. Both are correct; the matcher was just being cautious.\n- **3 wrong proposals:** PAY-61158, PAY-61365 and PAY-65656.\n  - Each is a same-amount tie where the matcher proposed the oldest invoice but staff had applied a newer one.\n  - In every case the true invoice is listed under \"alternatives\", and the Controller holds all tied invoices.\n  - So no wrong chase follows. Priya just picks a different invoice.\n- **12 exceptions, all truncated payer names:** `TAN`, `OYELARAN` x2, `ROSALES` x2, `HUME`, `ASHBY`, `CRANE`,\n  `LINDQVIST`, `CALLOWAY`, `KESSLER`, `PEMBERTON`.\n  - In 11 the matcher says it cannot identify the customer.\n  - In 1 (PEMBERTON) it **picked the wrong customer**: C1235 instead of C1337. It did not propose an invoice.\n  - This is safe for the ledger but **unsafe for collections** (FAILURES.md #1).\n- Confidence is well calibrated:\n  - auto-apply is always 0.99 and 100% correct;\n  - proposals at 0.82 to 0.90 were 100% correct;\n  - all misses came at 0.55, the score for an ambiguous same-amount tie.\n\n### Synthetic rows (40, labelled SYNTHETIC: real post-rewrite receipts with the amount or memo changed)\n| type | n | auto | proposed (top-1) | exception | end-to-end correct | note |\n|---|---|---|---|---|---|---|\n| bank fee -$15/25/35 | 10 | 0 | 5 (100%) | 5 | 50% | With a memo ref it is proposed as \"short by $15, looks like a bank fee\". **Without a ref it is always an exception**: `fee_tolerance` only applies when the memo has a ref. |\n| rounding ±$0.01/0.02 | 10 | 0 | 9 (100%) | 1 | 90% | -$0.01 is labelled \"looks like a bank fee\". +$0.01/0.02 is labelled \"partial or combined payment\". Both labels are misleading. |\n| 10% short pay | 10 | 0 | 7 (100%) | 3 | 70% | Same ref-only limitation |\n| one receipt for two invoices | 10 | 0 | 3 (67%) | 7 | 20%* | *7 of the 10 labels are invalid (see below) |\n| **all synthetic** | **40** | **0** | **24 (95.8%)** | **16** | **57.5%** | **No synthetic receipt was ever auto-applied: guardrail holds** |\n\n- **Test-set defect (owner: data-analyst).** In 7 of the 10 \"combined\" rows, one of the two labelled invoices had\n  already been paid before the synthetic receipt date: SYN-004, 012, 016, 020, 024, 028, 032 and 036 (for example,\n  SYN-004 pairs INV-24088, which was paid on 2025-08-06, with a receipt dated 2026-09-19). The matcher is right to\n  refuse them. On the 3 valid rows it scores 2 of 3.\n- The miss is SYN-040 (Rosales). Three open invoices of $2,448 exist, so 3 pairs add up to $4,896. The matcher\n  proposes the first pair it finds and **does not say other pairs fit equally well**.\n- With every \"no ref\" exception counted, Priya's queue would be 16 of 40 synthetic receipts with no suggestion. A\n  `fee_tolerance` pass on no-ref amount matching would cut this to about 7 (fix idea for the builde
… [tool input truncated]
```

### Tool · 2026-11-20 17:38:03 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/EVAL.md (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
Now I'll write EVAL.md.
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/EVAL.md",
 "content": "# EVAL: how well the agents work on the real records\n\nQA Evaluator. Run on 2026-11-20 at 11:36 CST against the code as it stood then. The builder was still editing:\n`context.py` and `data.py` changed during the run, so the numbers were re-run at 11:36. Data as of 2026-10-31.\nNothing in `app/` or `data/` was changed. The scripts are re-runnable:\n\n| script | what it does | output |\n|---|---|---|\n| `analysis/scripts/eval_cash_app.py` | replays the 286 test payments against the invoice book as it stood on each received date | `analysis/work/eval_cash_app_results.csv`, `.log` |\n| `analysis/scripts/eval_controller.py` | checks dispute detection against the analyst's list, and reads all 1,041 tickets | `analysis/work/eval_ticket_reads.csv`, `eval_ticket_sample_*.csv`, `.log` |\n| `analysis/scripts/eval_guardrails.py` | red-teams the real pipeline using changed copies of the data held in memory | `analysis/work/eval_guardrails_results.csv`, `.log` |\n\n**Headline**\n- **0 wrong automatic applications in 81** (real data).\n- Proposals put the right invoice first 98.0% of the time (real data).\n- The Controller held all 14 of the analyst's disputed invoices (recall 100%).\n- **44 of 54 guardrail checks pass.** The 10 failures fall into three gaps:\n  - a receipt whose customer cannot be identified blocks nothing (the Paidly case returns);\n  - complaint wording outside the keyword lists gets through;\n  - the banned-phrase list is narrow.\n\n---\n\n## 1. Cash Application (test set `analysis/testset_cash_app.csv`, 286 rows)\n\n**Harness.** For each test payment, the invoice book is rebuilt as it stood on the receipt date. An invoice counts as\nopen if `issue_date <= received_date` and (`paid_date` is blank or `paid_date >= received_date`). The payment is\nthen fed in as the only unapplied receipt, and the **production `cash_app.run()` is called unchanged** with\nDEFAULT_RULES, so no rule is re-implemented. An answer counts as correct when the proposed invoice set equals the\nlabel. For PAY-65805 (Kingsway), which is ambiguous, either invoice is accepted.\n\n### Real rows (246)\n| difficulty | n | auto-applied | auto precision | proposed | proposal top-1 | exception | exception rate | end-to-end correct |\n|---|---|---|---|---|---|---|---|---|\n| trivial (card) | 20 | 20 | **100%** | 0 | n/a | 0 | 0% | 100% |\n| easy (memo ref) | 63 | 61 | **100%** | 2 | 100% | 0 | 0% | 100% |\n| medium (no ref, unique amount) | 83 | 0 | n/a | 83 | 100% | 0 | 0% | 100% |\n| hard (same-amount ties / truncated payer) | 80 | 0 | n/a | 68 | 95.6% | 12 | 15% | 81.2% |\n| **all real** | **246** | **81** | **100% (81/81)** | **153** | **98.0% (150/153)** | **12** | **4.9%** | **93.9%** |\n\n- **Severity-1 check (wrong auto-apply): none.** Every auto-apply needs an exact amount, an invoice reference in the\n  memo, and that invoice belonging to the identified customer.\n- Two easy rows were proposed rather than auto-applied. Both are correct; the matcher was just being cautious.\n- **3 wrong proposals:** PAY-61158, PAY-61365 and PAY-65656.\n  - Each is a same-amount tie where the matcher proposed the oldest invoice but staff had applied a newer one.\n  - In every case the true invoice is listed under \"alternatives\", and the Controller holds all tied invoices.\n  - So no wrong chase follows. Priya just picks a different invoice.\n- **12 exceptions, all truncated payer names:** `TAN`, `OYELARAN` x2, `ROSALES` x2, `HUME`, `ASHBY`, `CRANE`,\n  `LINDQVIST`, `CALLOWAY`, `KESSLER`, `PEMBERTON`.\n  - In 11 the matcher says it cannot identify the customer.\n  - In 1 (PEMBERTON) it **picked the wrong customer**: C1235 instead of C1337. It did not propose an invoice.\n  - This is safe for the ledger but **unsafe for collections** (FAILURES.md #1).\n- Confidence is well calibrated:\n  - auto-apply is always 0.99 and 100% correct;\n  - proposals at 0.82 to 0.90 were 100% correct;\n  - all misses came at 0.55, the score for an ambiguous same-amount tie.\n\n### Synthetic rows (40, labelled SYNTHETIC: real post-rewrite receipts with the amount or memo changed)\n| type | n | auto | proposed (top-1) | exception | end-to-end correct | note |\n|---|---|---|---|---|---|---|\n| bank fee -$15/25/35 | 10 | 0 | 5 (100%) | 5 | 50% | With a memo ref it is proposed as \"short by $15, looks like a bank fee\". **Without a ref it is always an exception**: `fee_tolerance` only applies when the memo has a ref. |\n| rounding ±$0.01/0.02 | 10 | 0 | 9 (100%) | 1 | 90% | -$0.01 is labelled \"looks like a bank fee\". +$0.01/0.02 is labelled \"partial or combined payment\". Both labels are misleading. |\n| 10% short pay | 10 | 0 | 7 (100%) | 3 | 70% | Same ref-only limitation |\n| one receipt for two invoices | 10 | 0 | 3 (67%) | 7 | 20%* | *7 of the 10 labels are invalid (see below) |\n| **all synthetic** | **40** | **0** | **24 (95.8%)** | **16** | **57.5%** | **No synthetic receipt was ever auto-applied: guardrail holds** |\n\n- **Test-set defect (owner: data-analyst).** In 7 of the 10 \"combined\" rows, one of the two labelled invoices had\n  already been paid before the synthetic receipt date: SYN-004, 012, 016, 020, 024, 028, 032 and 036 (for example,\n  SYN-004 pairs INV-24088, which was paid on 2025-08-06, with a receipt dated 2026-09-19). The matcher is right to\n  refuse them. On the 3 valid rows it scores 2 of 3.\n- The miss is SYN-040 (Rosales). Three open invoices of $2,448 exist, so 3 pairs add up to $4,896. The matcher\n  proposes the first pair it finds and **does not say other pairs fit equally well**.\n- With every \"no ref\" exception counted, Priya's queue would be 16 of 40 synthetic receipts with no suggestion. A\n  `fee_tolerance` pass on no-ref amount matching would cut this to about 7 (fix idea for the builde
… [tool input truncated]
```

### Claude · 2026-11-20 17:39:28 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FAILURES.md",
 "content": "# FAILURES: where the system is wrong, unsure, or could be gamed\n\nQA Evaluator, 2026-11-20 at 11:36 CST. Every case can be reproduced with `analysis/scripts/eval_*.py`. The numbers\nare in `analysis/EVAL.md`.\n\n**REAL** means it happens on the records as they are today. **REAL + MUTATION** means a real record changed in\nmemory in a way the data shows is common. **SYNTHETIC** means injected text or amounts, labelled as such.\n\nRanked by how much harm a wrong outcome would do.\n\n---\n\n### 1. Abbreviate the payer name and the Paidly failure comes back (REAL + MUTATION). Highest severity.\n- **What happened.** We took Brandt & Lowell's real unapplied $6,324 wire (PAY-65766) and changed only the payer to\n  `BRANDT`, the way 416 historical receipts arrive truncated.\n  - The Cash agent's fuzzy match picked **Studio Brandt** (similarity 0.55), found no matching invoice and raised\n    an EXCEPTION.\n  - Brandt & Lowell's INV-25806 then got a **DRAFT_REMINDER to aisha.garrick@brandtlowellcpas.example** for money\n    already in the bank.\n  - The same happens with `KINGSWAY`: INV-25469 is drafted.\n  - For `JESSOP` see #3.\n- **Why.**\n  - The Controller only holds against an unapplied receipt it can tie to a customer (`pipeline.py:34-35`,\n    `controller.py:28-33`). An EXCEPTION with `customer_id=None` blocks nothing. One tied to the wrong customer\n    blocks the wrong customer.\n  - `identify_customer` accepts a lone fuzzy candidate scoring as low as 0.55 (`cash_app.py:42-49`). Short payer\n    strings therefore resolve to the shortest customer name that contains the surname.\n  - On the real test set, 12 of 80 hard receipts end as exceptions: 11 with no customer, and 1 (PEMBERTON) with\n    the wrong customer.\n- **Impact.** In the mutated cases, $6,324 + $62,688 + $5,100 would be chased after the money arrived. This is\n  exactly the email Maya said gets the tool switched off.\n- **What a person should do.** Until this is fixed, Priya must clear the \"Payments to confirm\" queue **before**\n  approving any reminder. Any receipt with no identified customer should freeze reminders for invoices of the same\n  amount.\n- **Fix idea.**\n  - (a) Any EXCEPTION receipt holds every open invoice with the same amount (±fee tolerance) across ALL customers,\n    plus every candidate customer's invoices.\n  - (b) Only set `customer_id` from a fuzzy match at ≥0.8 confidence; below that, keep the candidates list.\n  - (c) Add `BRANDT` and `JESSOP` as permanent regression tests.\n\n### 2. A dispute ticket one day outside the lookback, so a card re-run is proposed for a customer with a chargeback (REAL)\n- **What happened.**\n  - On 2026-07-02, Drummond Consulting wrote T880019, \"DISPUTING CHARGES WITH MY BANK\": \"You billed us twice for\n    the annual plan ... I've opened a chargeback on both payments.\"\n  - Today Drummond's failed card invoice INV-25769 ($658, 68 dpd) is proposed as **RETRY_CARD**.\n- **Why.** `dispute_lookback_days` = 120 puts the window start at 2026-07-03, so the ticket is invisible\n  (`context.py:93,101`). The legal / chargeback read never runs. Old tickets also drop out silently, so a dispute\n  hold disappears on its own once the ticket ages past 120 days, even if nobody settled it.\n- **Impact.** $658, but re-charging a card the customer is charging back is a likely CEO-inbox complaint. The same\n  silent ageing applies to all 14 disputes ($309k) from late November onward.\n- **What a person should do.** Priya should check Drummond's history before approving the re-run. The AM should\n  confirm the chargeback is resolved.\n- **Fix idea.**\n  - Always read legal_threat and chargeback tickets regardless of age.\n  - Make dispute holds sticky until an AM releases them, as Maya asked, instead of letting them depend on the\n    ticket's age.\n\n### 3. The \"Jessop payment\" memo fits 8 customers; only the exact payer name saves it (REAL; abbreviated variant is REAL + MUTATION)\n- **What happened.**\n  - PAY-65750, $62,688, memo \"Jessop payment\", payer \"Jessop & Orwell Agency\". Eight customers contain \"Jessop\"\n    (Jessop Legal, Jessop Strategy, Delacroix Jessop & Co, and others).\n  - Today the payer name matches exactly, the amount is unique, and INV-25784 (a top-50 account) is held as\n    MONEY_RECEIVED. Correct.\n  - With the payer changed to `JESSOP`, the Cash agent tagged the receipt to **Jessop Legal (C1402)**.\n    - Jessop Legal's invoices would be held for no reason.\n    - Jessop & Orwell's $62,688 invoice dropped to HUMAN_WRITES with a **prepared chase draft to\n      joel.okafor@jessoporwellagency.example**.\n  - With `JESSOP ORWELL` it is handled correctly.\n- **Why.** The same mechanics as #1. The memo surname is never used to rank candidates. Only 1 of the 8 Jessop\n  customers has an open $62,688 invoice, and that was never consulted.\n- **Impact.** $62,688 on a top-50 account. This is the Paidly scenario on the largest receipt in the data. The money\n  has also sat unapplied for 10 working days, against a 3-to-5-day policy.\n- **What a person should do.** Apply PAY-65750 to INV-25784 today. When a surname memo fits several customers, check\n  the remitter's bank account details, not the name.\n- **Fix idea.** When the name is ambiguous, search every customer whose name contains the memo surname for an exact\n  open amount. If exactly one fits, propose it, and never send `customer_id` to the wrong account.\n\n### 4. Complaints worded outside the keyword lists are not held (SYNTHETIC injection into a real account)\n- **What happened.** Tickets were injected for Thornfield Consulting (INV-25862, $39,456, normally a\n  DRAFT_REMINDER). The reminder was **still drafted** for:\n  - \"We **will not** pay it until you correct it\" (Bi
… [tool input truncated]
```

### Tool · 2026-11-20 17:39:28 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FAILURES.md (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FAILURES.md",
 "content": "# FAILURES: where the system is wrong, unsure, or could be gamed\n\nQA Evaluator, 2026-11-20 at 11:36 CST. Every case can be reproduced with `analysis/scripts/eval_*.py`. The numbers\nare in `analysis/EVAL.md`.\n\n**REAL** means it happens on the records as they are today. **REAL + MUTATION** means a real record changed in\nmemory in a way the data shows is common. **SYNTHETIC** means injected text or amounts, labelled as such.\n\nRanked by how much harm a wrong outcome would do.\n\n---\n\n### 1. Abbreviate the payer name and the Paidly failure comes back (REAL + MUTATION). Highest severity.\n- **What happened.** We took Brandt & Lowell's real unapplied $6,324 wire (PAY-65766) and changed only the payer to\n  `BRANDT`, the way 416 historical receipts arrive truncated.\n  - The Cash agent's fuzzy match picked **Studio Brandt** (similarity 0.55), found no matching invoice and raised\n    an EXCEPTION.\n  - Brandt & Lowell's INV-25806 then got a **DRAFT_REMINDER to aisha.garrick@brandtlowellcpas.example** for money\n    already in the bank.\n  - The same happens with `KINGSWAY`: INV-25469 is drafted.\n  - For `JESSOP` see #3.\n- **Why.**\n  - The Controller only holds against an unapplied receipt it can tie to a customer (`pipeline.py:34-35`,\n    `controller.py:28-33`). An EXCEPTION with `customer_id=None` blocks nothing. One tied to the wrong customer\n    blocks the wrong customer.\n  - `identify_customer` accepts a lone fuzzy candidate scoring as low as 0.55 (`cash_app.py:42-49`). Short payer\n    strings therefore resolve to the shortest customer name that contains the surname.\n  - On the real test set, 12 of 80 hard receipts end as exceptions: 11 with no customer, and 1 (PEMBERTON) with\n    the wrong customer.\n- **Impact.** In the mutated cases, $6,324 + $62,688 + $5,100 would be chased after the money arrived. This is\n  exactly the email Maya said gets the tool switched off.\n- **What a person should do.** Until this is fixed, Priya must clear the \"Payments to confirm\" queue **before**\n  approving any reminder. Any receipt with no identified customer should freeze reminders for invoices of the same\n  amount.\n- **Fix idea.**\n  - (a) Any EXCEPTION receipt holds every open invoice with the same amount (±fee tolerance) across ALL customers,\n    plus every candidate customer's invoices.\n  - (b) Only set `customer_id` from a fuzzy match at ≥0.8 confidence; below that, keep the candidates list.\n  - (c) Add `BRANDT` and `JESSOP` as permanent regression tests.\n\n### 2. A dispute ticket one day outside the lookback, so a card re-run is proposed for a customer with a chargeback (REAL)\n- **What happened.**\n  - On 2026-07-02, Drummond Consulting wrote T880019, \"DISPUTING CHARGES WITH MY BANK\": \"You billed us twice for\n    the annual plan ... I've opened a chargeback on both payments.\"\n  - Today Drummond's failed card invoice INV-25769 ($658, 68 dpd) is proposed as **RETRY_CARD**.\n- **Why.** `dispute_lookback_days` = 120 puts the window start at 2026-07-03, so the ticket is invisible\n  (`context.py:93,101`). The legal / chargeback read never runs. Old tickets also drop out silently, so a dispute\n  hold disappears on its own once the ticket ages past 120 days, even if nobody settled it.\n- **Impact.** $658, but re-charging a card the customer is charging back is a likely CEO-inbox complaint. The same\n  silent ageing applies to all 14 disputes ($309k) from late November onward.\n- **What a person should do.** Priya should check Drummond's history before approving the re-run. The AM should\n  confirm the chargeback is resolved.\n- **Fix idea.**\n  - Always read legal_threat and chargeback tickets regardless of age.\n  - Make dispute holds sticky until an AM releases them, as Maya asked, instead of letting them depend on the\n    ticket's age.\n\n### 3. The \"Jessop payment\" memo fits 8 customers; only the exact payer name saves it (REAL; abbreviated variant is REAL + MUTATION)\n- **What happened.**\n  - PAY-65750, $62,688, memo \"Jessop payment\", payer \"Jessop & Orwell Agency\". Eight customers contain \"Jessop\"\n    (Jessop Legal, Jessop Strategy, Delacroix Jessop & Co, and others).\n  - Today the payer name matches exactly, the amount is unique, and INV-25784 (a top-50 account) is held as\n    MONEY_RECEIVED. Correct.\n  - With the payer changed to `JESSOP`, the Cash agent tagged the receipt to **Jessop Legal (C1402)**.\n    - Jessop Legal's invoices would be held for no reason.\n    - Jessop & Orwell's $62,688 invoice dropped to HUMAN_WRITES with a **prepared chase draft to\n      joel.okafor@jessoporwellagency.example**.\n  - With `JESSOP ORWELL` it is handled correctly.\n- **Why.** The same mechanics as #1. The memo surname is never used to rank candidates. Only 1 of the 8 Jessop\n  customers has an open $62,688 invoice, and that was never consulted.\n- **Impact.** $62,688 on a top-50 account. This is the Paidly scenario on the largest receipt in the data. The money\n  has also sat unapplied for 10 working days, against a 3-to-5-day policy.\n- **What a person should do.** Apply PAY-65750 to INV-25784 today. When a surname memo fits several customers, check\n  the remitter's bank account details, not the name.\n- **Fix idea.** When the name is ambiguous, search every customer whose name contains the memo surname for an exact\n  open amount. If exactly one fits, propose it, and never send `customer_id` to the wrong account.\n\n### 4. Complaints worded outside the keyword lists are not held (SYNTHETIC injection into a real account)\n- **What happened.** Tickets were injected for Thornfield Consulting (INV-25862, $39,456, normally a\n  DRAFT_REMINDER). The reminder was **still drafted** for:\n  - \"We **will not** pay it until you correct it\" (Bi
… [tool input truncated]
```

### Claude · 2026-11-20 17:39:36 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"fee_tol:\\|for k in (2, 3)\\|def check_draft\\|open_tickets\\|if action in (\\\"DRAFT_REMINDER\\\"\\|later = d\\|action not in (\\\"HOLD\\\"\" app/engine/cash_app.py app/engine/controller.py app/engine/pipeline.py",
 "description": "Verify cited line numbers"
}
```

### Tool · 2026-11-20 17:39:36 UTC
**Tool result:**
```
app/engine/cash_app.py:98:            elif 0 < -diff <= fee_tol:
app/engine/cash_app.py:117:                for k in (2, 3):
app/engine/pipeline.py:54:        if action in ("DRAFT_REMINDER", "HUMAN_WRITES") and ctx and not any(h["code"] == "LEGAL_RISK" for h in holds):
app/engine/pipeline.py:64:            later = d["payments"][(d["payments"]["method"] == "card") & (d["payments"]["payer_name"].map(norm_name) == norm_name(r["customer_name"]))
app/engine/pipeline.py:66:            if len(later) and action not in ("HOLD",):
app/engine/controller.py:55:    for t in (ctx or {}).get("open_tickets", []):
app/engine/controller.py:104:def check_draft(draft, rules):
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"fee_tol:\\|for k in (2, 3)\\|def check_draft\\|open_tickets\\|if action in (\\\"DRAFT_REMINDER\\\"\\|later = d\\|action not in (\\\"HOLD\\\"\" app/engine/cash_app.py app/engine/controller.py app/engine/pipeline.py",
 "description": "Verify cited line numbers"
}
```

### Claude · 2026-11-20 17:39:49 UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "I wrote EVAL.md and FAILURES.md (13 cases). There are no wrong automatic payment applications, but the \"never chase money we already have\" guardrail (the Paidly case) breaks when the payer name is shortened. 44 of 54 guardrail checks pass. I edited nothing in app/ or data/. Numbers come from a re-run at 11:36; the builder changed context.py and data.py during my run.\n\n**Headline numbers**\n- **Cash application, real data (246 rows):**\n  - 81 auto-applied, all correct, so no severity-1.\n  - 153 proposed, 98.0% with the right invoice first; the 3 misses are same-amount ties where staff picked a newer invoice, and the right one is in the alternatives.\n  - 4.9% exceptions; all 12 are shortened payer names.\n- **Cash application, synthetic (40 rows):** 0 auto-applied, 58% end to end. Bank fees and short payments with no invoice reference in the memo always become exceptions. Also, 7 of the 10 \"combined\" synthetic labels are wrong (one invoice was already paid); the data-analyst should regenerate them.\n- **Controller vs the analyst's 14 disputes:** recall 100%, all 14 held. The one extra flag is Eastman Engineering's chargeback threat, which is a correct catch.\n- **Ticket reading (all 1,041 tickets):** only 22 are flagged, so I checked all 22 by hand: 82% are right. In 30 unflagged billing-related tickets I found 1–3 misses.\n- **Complaint counter:** the keyword count of 14 drops to 1 using the agent's read.\n\n**Severity-1 guardrail bug (FAILURES #1/#3).** I took the real unapplied receipts and shortened only the payer name (416 past receipts arrive shortened like this):\n- \"BRANDT\": Brandt & Lowell gets a reminder draft for the $6,324 they already paid.\n- \"JESSOP\": the $62,688 receipt is tagged to Jessop Legal, the wrong customer, and Jessop & Orwell gets a chase draft.\n- Cause: a payment whose customer can't be identified holds nothing (pipeline.py:34-35, controller.py:28-33), and the name match accepts a single weak match at 0.55 (cash_app.py:42-49).\n\n**Other bugs**\n- `hold_on_open_ticket_days` is on the Rules page but the engine never reads it (should be wired in at controller.py:55).\n- \"Already received\" counts Kingsway's $5,100 twice ($83,448 instead of $78,348; pipeline.py:96).\n- A blocked draft also cancels card re-run proposals (pipeline.py:54-66).\n- These complaint wordings don't stop a reminder: \"will not pay\", \"refuse to pay\", a refusal in a ticket tagged How-to, and a polite \"we've been overcharged\".\n- \"debt collector\", \"legal proceedings\" and \"cut off\" get past the banned-phrase check.\n- Reyes Consulting's $51,072 invoice is held as a dispute because the customer asked about voiding their own client's invoice.\n\n**Best 3 for the demo video:**\n1. Shortened payer name brings back Paidly (Brandt / Jessop): candid, with a concrete fix.\n2. Drummond (real): a chargeback ticket from 07-02 falls one day outside the 120-day window, so a card re-run is proposed for a customer charging us back.\n3. Complaint counter 14 → 1 (real): 12 of the 14 are customers asking about their own reminder emails to their clients.\n\nFiles are in analysis/:\n- EVAL.md\n- FAILURES.md\n- scripts/eval_cash_app.py\n- scripts/eval_controller.py\n- scripts/eval_guardrails.py\n- work/eval_* (results and logs)"
}
```

### Tool · 2026-11-20 17:39:50 UTC
**Tool result:**
```
{"success":true,"message":"Report delivered to your caller."}
```

### Jacek · 2026-11-20 18:09:09 UTC
The coordinator sent a message while you were working:
New QA pass (Jacek wants FIN-1/FIN-2 at 100% before we involve Maya again). Target 30 min. Since your last run the engine changed a lot (severity-1 fix, contract checks, Reyes fix, strong refusals, auto-apply cap $10k, top-50 not-due → NO_ACTION, card re-run blocked on chargeback threats) and there is now a full web app + RIG. Live URL: https://ledgerline-finance-rig.onrender.com (auth off, demo; free plan — first hit may take ~30s). Local: from <root>, `.venv/bin/python` with `from fastapi.testclient import TestClient; from app.main import app` (use DB_PATH and RULES_PATH env pointing to a temp dir for local tests so you don't pollute ./ledgerline.db / ./rules.json; set them BEFORE importing app). Do NOT edit app/ code; report defects with file:line and a suggested fix. Do not message Maya.

Write analysis/QA_PASS_2.md with PASS/FAIL per check, and update analysis/EVAL.md + FAILURES.md numbers to current code (fix the stale "44 of 54").
A. FIN-2 regression: re-run your cash-app eval on current code (auto-apply precision must stay 100%; report what the $10k cap changes); BRANDT/JESSOP/KINGSWAY shortened-name replays → no chase; unidentified payer holds.
B. FIN-1 policy compliance on EVERY invoice in run_pipeline(): stage vs days_past_due per collections_policy (-5/+7/+21/+45/+90); top-50 never DRAFT_REMINDER; no draft for any invoice with PAID/MONEY_RECEIVED/DISPUTE/CANCELLATION/LEGAL_RISK/OPEN_ESCALATION; all 20 drafts: no banned phrase, recipients only verified contacts (domain match, active), never a "left the firm" contact, AM cc'd, invoice id/amount/due date correct in body, sign-off Priya; card re-runs only where a later card charge succeeded and no hard hold/legal risk; Dana decisions correct (≤10 days to 150-day write-off, or >$2k).
C. Consistency: the same numbers on Home, /today, /collections counts, /digest text, chat "status", Team cards, and run_pipeline() metrics (overdue, already received, disputed, collectable, drafts, holds, card re-runs, needs-a-human count).
D. Human-action flows (local TestClient, then 1–2 smoke checks on live): approve payment proposal; undo auto-apply; approve draft with an edit; reject draft; override hold (reason required, <5 chars → 400); release DISPUTE without AM checkbox → 400, with → OK; approve/reject card re-run; rules change via /rules form and via chat "set ... to ..." + /api/rules/apply (before/after counts); propose instruction via chat "from now on ..." → accept in Direct → appears in the agent manual file; save Loom link on /demo (share→embed); every action appears in /audit and /activity with user + reason; CSV export works.
E. RIG readiness for "Maya interactions from the RIG": does the Maya tab render all 4 exchanges + count + pending draft correctly from trail files? Is there anything in the RIG that would mislead Maya or a reviewer (stale numbers, placeholder text, 'coming soon', dev artefacts, broken links, wrong T+ times)? List every rough edge you see on each RIG tab (read the HTML via TestClient).
F. Robustness: what happens on Render restart (free plan: SQLite/rules/manual edits are ephemeral — confirm and quantify), cold start time, and any page >2s.
Report back ≤15 lines: PASS/FAIL summary per section, defects ranked (sev-1/2/3) with file:line, and a one-line readiness verdict.

Address this before completing your current task.

### Claude ·  UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "I wrote EVAL.md and FAILURES.md (13 cases). There are no wrong automatic payment applications, but the \"never chase money we already have\" guardrail (the Paidly case) breaks when the payer name is shortened. 44 of 54 guardrail checks pass. I edited nothing in app/ or data/. Numbers come from a re-run at 11:36; the builder changed context.py and data.py during my run.\n\n**Headline numbers**\n- **Cash application, real data (246 rows):**\n  - 81 auto-applied, all correct, so no severity-1.\n  - 153 proposed, 98.0% with the right invoice first; the 3 misses are same-amount ties where staff picked a newer invoice, and the right one is in the alternatives.\n  - 4.9% exceptions; all 12 are shortened payer names.\n- **Cash application, synthetic (40 rows):** 0 auto-applied, 58% end to end. Bank fees and short payments with no invoice reference in the memo always become exceptions. Also, 7 of the 10 \"combined\" synthetic labels are wrong (one invoice was already paid); the data-analyst should regenerate them.\n- **Controller vs the analyst's 14 disputes:** recall 100%, all 14 held. The one extra flag is Eastman Engineering's chargeback threat, which is a correct catch.\n- **Ticket reading (all 1,041 tickets):** only 22 are flagged, so I checked all 22 by hand: 82% are right. In 30 unflagged billing-related tickets I found 1–3 misses.\n- **Complaint counter:** the keyword count of 14 drops to 1 using the agent's read.\n\n**Severity-1 guardrail bug (FAILURES #1/#3).** I took the real unapplied receipts and shortened only the payer name (416 past receipts arrive shortened like this):\n- \"BRANDT\": Brandt & Lowell gets a reminder draft for the $6,324 they already paid.\n- \"JESSOP\": the $62,688 receipt is tagged to Jessop Legal, the wrong customer, and Jessop & Orwell gets a chase draft.\n- Cause: a payment whose customer can't be identified holds nothing (pipeline.py:34-35, controller.py:28-33), and the name match accepts a single weak match at 0.55 (cash_app.py:42-49).\n\n**Other bugs**\n- `hold_on_open_ticket_days` is on the Rules page but the engine never reads it (should be wired in at controller.py:55).\n- \"Already received\" counts Kingsway's $5,100 twice ($83,448 instead of $78,348; pipeline.py:96).\n- A blocked draft also cancels card re-run proposals (pipeline.py:54-66).\n- These complaint wordings don't stop a reminder: \"will not pay\", \"refuse to pay\", a refusal in a ticket tagged How-to, and a polite \"we've been overcharged\".\n- \"debt collector\", \"legal proceedings\" and \"cut off\" get past the banned-phrase check.\n- Reyes Consulting's $51,072 invoice is held as a dispute because the customer asked about voiding their own client's invoice.\n\n**Best 3 for the demo video:**\n1. Shortened payer name brings back Paidly (Brandt / Jessop): candid, with a concrete fix.\n2. Drummond (real): a chargeback ticket from 07-02 falls one day outside the 120-day window, so a card re-run is proposed for a customer charging us back.\n3. Complaint counter 14 → 1 (real): 12 of the 14 are customers asking about their own reminder emails to their clients.\n\nFiles are in analysis/:\n- EVAL.md\n- FAILURES.md\n- scripts/eval_cash_app.py\n- scripts/eval_controller.py\n- scripts/eval_guardrails.py\n- work/eval_* (results and logs)"
}
```

### Claude · 2026-11-20 18:09:17 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && date; ls -la app app/engine app/web app/web/templates trail submission 2>/dev/null | head -90; wc -l app/*.py app/engine/*.py app/web/*.py",
 "description": "Survey current app structure"
}
```

### Tool · 2026-11-20 18:09:17 UTC
**Tool result:**
```
Fri Nov 20 12:09:17 CST 2026
app:
total 40
drwxr-xr-x@  8 jacekmaterna  staff   256 Nov 20 11:27 .
drwx------@ 18 jacekmaterna  staff   576 Nov 20 11:59 ..
-rw-r--r--@  1 jacekmaterna  staff     0 Nov 20 11:19 __init__.py
-rw-r--r--@  1 jacekmaterna  staff  5751 Nov 20 11:27 auth.py
drwxr-xr-x@ 13 jacekmaterna  staff   416 Nov 20 11:58 engine
-rw-r--r--@  1 jacekmaterna  staff  2115 Nov 20 11:41 main.py
-rw-r--r--@  1 jacekmaterna  staff  6841 Nov 20 11:50 store.py
drwxr-xr-x@ 11 jacekmaterna  staff   352 Nov 20 11:40 web

app/engine:
total 144
drwxr-xr-x@ 13 jacekmaterna  staff    416 Nov 20 11:58 .
drwxr-xr-x@  8 jacekmaterna  staff    256 Nov 20 11:27 ..
-rw-r--r--@  1 jacekmaterna  staff      0 Nov 20 11:21 __init__.py
-rw-r--r--@  1 jacekmaterna  staff   9302 Nov 20 11:47 cash_app.py
-rw-r--r--@  1 jacekmaterna  staff   6624 Nov 20 11:28 collections.py
-rw-r--r--@  1 jacekmaterna  staff  10388 Nov 20 11:55 context.py
-rw-r--r--@  1 jacekmaterna  staff   8717 Nov 20 11:58 controller.py
-rw-r--r--@  1 jacekmaterna  staff   3581 Nov 20 11:35 data.py
-rw-r--r--@  1 jacekmaterna  staff   2297 Nov 20 11:29 digest.py
-rw-r--r--@  1 jacekmaterna  staff   2694 Nov 20 11:25 llm.py
drwxr-xr-x@  6 jacekmaterna  staff    192 Nov 20 11:38 manuals
-rw-r--r--@  1 jacekmaterna  staff  11821 Nov 20 11:47 pipeline.py
-rw-r--r--@  1 jacekmaterna  staff   4014 Nov 20 11:47 rules.py

app/web:
total 256
drwxr-xr-x@ 11 jacekmaterna  staff    352 Nov 20 11:40 .
drwxr-xr-x@  8 jacekmaterna  staff    256 Nov 20 11:27 ..
-rw-r--r--@  1 jacekmaterna  staff      0 Nov 20 11:19 __init__.py
-rw-r--r--@  1 jacekmaterna  staff  25045 Nov 20 11:42 chat.py
-rw-r--r--@  1 jacekmaterna  staff  25670 Nov 20 11:32 fake_state.py
-rw-r--r--@  1 jacekmaterna  staff  13459 Nov 20 11:52 rig.py
-rw-r--r--@  1 jacekmaterna  staff  14147 Nov 20 11:51 rig_data.py
-rw-r--r--@  1 jacekmaterna  staff   2275 Nov 20 11:19 state.py
drwxr-xr-x@  3 jacekmaterna  staff     96 Nov 20 11:51 static
drwxr-xr-x@ 32 jacekmaterna  staff   1024 Nov 20 11:52 templates
-rw-r--r--@  1 jacekmaterna  staff  36716 Nov 20 11:50 views.py

app/web/templates:
total 336
drwxr-xr-x@ 32 jacekmaterna  staff   1024 Nov 20 11:52 .
drwxr-xr-x@ 11 jacekmaterna  staff    352 Nov 20 11:40 ..
-rw-r--r--@  1 jacekmaterna  staff   5044 Nov 20 11:41 _chat.html
-rw-r--r--@  1 jacekmaterna  staff    777 Nov 20 11:23 _customer_rows.html
-rw-r--r--@  1 jacekmaterna  staff  10152 Nov 20 11:51 _docs_svg.html
-rw-r--r--@  1 jacekmaterna  staff   
… [result truncated, 5530 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && date; ls -la app app/engine app/web app/web/templates trail submission 2>/dev/null | head -90; wc -l app/*.py app/engine/*.py app/web/*.py",
 "description": "Survey current app structure"
}
```

### Claude · 2026-11-20 18:09:22 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/cash_app.py | sed -n 26,80p; cat -n app/engine/pipeline.py; cat -n app/engine/controller.py | sed -n 1,60p; cat app/engine/rules.py | sed -n 6,30p",
 "description": "Read changed engine code"
}
```

### Tool · 2026-11-20 18:09:22 UTC
**Tool result:**
```
    26	def identify_customer(payer_name, customers):
    27	    """Return (customer_id or None, confidence, reason, candidates). Exact normalised name first, then fuzzy."""
    28	    n = norm_name(payer_name)
    29	    exact = customers[customers["norm"] == n]
    30	    if len(exact) == 1:
    31	        r = exact.iloc[0]
    32	        return r["customer_id"], 0.97, "Payer name matches customer '%s' exactly (ignoring case and punctuation)" % r["name"], [r["customer_id"]]
    33	    toks = set(core_tokens(payer_name))
    34	    scored = []
    35	    for _, r in customers.iterrows():
    36	        ct = set(core_tokens(r["name"]))
    37	        if not ct or not toks:
    38	            continue
    39	        jacc = len(ct & toks) / float(len(ct | toks))
    40	        ratio = difflib.SequenceMatcher(None, n, r["norm"]).ratio()
    41	        s = 0.6 * jacc + 0.4 * ratio
    42	        if s > 0.55:
    43	            scored.append((s, r["customer_id"], r["name"]))
    44	    scored.sort(reverse=True)
    45	    if not scored:
    46	        return None, 0.0, "No customer name resembles payer '%s'" % payer_name, []
    47	    # QA (T+0:30): a single weak match (e.g. payer "JESSOP" -> "Jessop Legal" at 0.55) assigned the wrong customer.
    48	    # Only accept a fuzzy match when it is strong AND clearly ahead; otherwise return the candidates and let the
    49	    # amount decide (or a person).
    50	    if scored[0][0] >= 0.75 and (len(scored) == 1 or scored[0][0] - scored[1][0] > 0.15):
    51	        s, cid, name = scored[0]
    52	        return cid, round(min(0.9, s), 2), "Payer name is closest to '%s' (similarity %.2f)" % (name, s), [c for _, c, _ in scored[:6]]
    53	    names = ", ".join("%s (%.2f)" % (nm, s) for s, _, nm in scored[:6])
    54	    return None, 0.3, "Payer name '%s' is not a clear match for any one customer: %s" % (payer_name, names), [c for _, c, _ in scored[:6]]
    55	
    56	
    57	def run(d, rules):
    58	    inv = d["invoices"]
    59	    pay = d["payments"]
    60	    cus = d["customers"]
    61	    open_inv = inv[inv["status"].isin(OPEN_STATUSES)]
    62	    by_id = inv.set_index("invoice_id")
    63	    unapplied = pay[pay["invoice_id"].isna()].sort_values("received_date")
    64	    tol = float(rules.get("amount_tolerance", 0) or 0)
    65	    fee_tol = float(rules.get("fee_tolerance", 0) or 0)
    66	    results, audit = [], []
    67	
    68	    for _, p in unapplied.iterrows():
    69	        amt = float(p["amou
… [result truncated, 22604 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/cash_app.py | sed -n 26,80p; cat -n app/engine/pipeline.py; cat -n app/engine/controller.py | sed -n 1,60p; cat app/engine/rules.py | sed -n 6,30p",
 "description": "Read changed engine code"
}
```

### Claude · 2026-11-20 18:09:29 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/controller.py | sed -n 60,128p; cat -n app/engine/cash_app.py | sed -n 80,112p; ls rules.json ledgerline.db 2>&1",
 "description": "Read rest of controller and cash app"
}
```

### Tool · 2026-11-20 18:09:29 UTC
**Tool result:**
```
Exit code 1
    60	                          "detail": "%s (%s): %s. Confirm the final amount owing with the account manager before any reminder." % (t["ticket_id"], t["created_at"][:10], r.get("summary")),
    61	                          "agent": "Account Context"})
    62	        elif r.get("kind") == "dispute" and t["created_at"][:10] >= dispute_since and (names_this or (names_none and r.get("refuses_to_pay_until_fixed"))):
    63	            solved = " The ticket is marked '%s' but the customer said they won't pay until it is fixed." % t["status"] if t["status"] == "solved" and r.get("refuses_to_pay_until_fixed") else ""
    64	            holds.append({"code": "DISPUTE", "label": "Invoice disputed in support",
    65	                          "detail": "%s (%s): %s.%s Account manager decides when to resume (policy)." % (t["ticket_id"], t["created_at"][:10], r.get("summary"), solved),
    66	                          "agent": "Account Context"})
    67	    import pandas as _pd
    68	    window = _pd.Timestamp("2026-10-31") - _pd.Timedelta(days=int(rules.get("hold_on_open_ticket_days", 30)))
    69	    for t in (ctx or {}).get("open_tickets", []):
    70	        recent = _pd.Timestamp(t["created_at"]) >= window or t["status"] == "open"
    71	        if t["priority"] in ("high", "urgent") and recent:
    72	            holds.append({"code": "OPEN_ESCALATION", "label": "Open high-priority support ticket",
    73	                          "detail": "%s '%s' is %s (%s priority). Policy: don't chase during an open escalation until the AM says so." % (t["ticket_id"], t["subject"], t["status"], t["priority"]),
    74	                          "agent": "Account Context"})
    75	            break
    76	
    77	    # 3. Who it can go to.
    78	    contacts = (ctx or {}).get("contacts", [])
    79	    billing_ok = [c for c in contacts if c["verified"] and "billing" in c["role"].lower()]
    80	    admin_ok = [c for c in contacts if c["verified"] and "admin" in c["role"].lower()]
    81	    stale = [c for c in contacts if c["issue"] and "billing" in c["role"].lower()]
    82	    if not billing_ok and not admin_ok:
    83	        holds.append({"code": "NO_VALID_CONTACT", "label": "No verified billing contact",
    84	                      "detail": "No active contact whose email matches the customer's domain. Ask the AM for the right person.", "agent": "Controller"})
    85	    elif stale:
    86	        holds.append({"code": "STALE_CONTACT", "label": "Billing
… [result truncated, 8036 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat -n app/engine/controller.py | sed -n 60,128p; cat -n app/engine/cash_app.py | sed -n 80,112p; ls rules.json ledgerline.db 2>&1",
 "description": "Read rest of controller and cash app"
}
```

### Claude · 2026-11-20 18:09:37 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && export RULES_PATH=/private/tmp/claude-501/qa2/rules.json DB_PATH=/private/tmp/claude-501/qa2/l.db; mkdir -p /private/tmp/claude-501/qa2; .venv/bin/python analysis/scripts/eval_cash_app.py > analysis/work/eval_cash_app.log 2>&1; sed -n 1,40p analysis/work/eval_cash_app.log | cut -c1-260; .venv/bin/python analysis/scripts/eval_controller.py > analysis/work/eval_controller.log 2>&1; head -14 analysis/work/eval_controller.log; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -v \"^\\[llm\\]\" > analysis/work/eval_guardrails.log; grep \"FAIL\\|SUMMARY\\|Drummond\\|Quill, Mott\\|Reyes\" analysis/work/eval_guardrails.log | cut -c1-330; .venv/bin/python -m app.engine.pipeline",
 "description": "Re-run all eval scripts on current code"
}
```

### Tool · 2026-11-20 18:09:54 UTC
**Tool result:**
```
=== REAL ===
real: all                    n=246 | auto  59 (prec 100.0%) | propose 175 (top1 98.3%) | exception  12 (5%) | end-to-end correct 93.9% | customer correct 95.1%
real: trivial                n= 20 | auto  20 (prec 100.0%) | propose   0 (top1 n/a) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: easy                   n= 63 | auto  39 (prec 100.0%) | propose  24 (top1 100.0%) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: medium                 n= 83 | auto   0 (prec n/a) | propose  83 (top1 100.0%) | exception   0 (0%) | end-to-end correct 100.0% | customer correct 100.0%
real: hard                   n= 80 | auto   0 (prec n/a) | propose  68 (top1 95.6%) | exception  12 (15%) | end-to-end correct 81.2% | customer correct 85.0%
=== SYNTHETIC ===
synthetic: all               n= 40 | auto   0 (prec n/a) | propose  24 (top1 95.8%) | exception  16 (40%) | end-to-end correct 57.5% | customer correct 100.0%
synthetic: bank_fee          n= 10 | auto   0 (prec n/a) | propose   5 (top1 100.0%) | exception   5 (50%) | end-to-end correct 50.0% | customer correct 100.0%
synthetic: rounding          n= 10 | auto   0 (prec n/a) | propose   9 (top1 100.0%) | exception   1 (10%) | end-to-end correct 90.0% | customer correct 100.0%
synthetic: short_pay         n= 10 | auto   0 (prec n/a) | propose   7 (top1 100.0%) | exception   3 (30%) | end-to-end correct 70.0% | customer correct 100.0%
synthetic: combined          n= 10 | auto   0 (prec n/a) | propose   3 (top1 66.7%) | exception   7 (70%) | end-to-end correct 20.0% | customer correct 100.0%

Wrong AUTO_APPLY rows:
Empty DataFrame
Columns: [payment_id, is_synthetic, difficulty, syn_type, payer_name, memo, amount, truth, ambiguous_label, decision, pred, alternatives, confidence, correct, truth_in_pred_or_alt, pred_customer, true_customer, customer_correct, last_reason, all_reasons]
Index: []

Wrong PROPOSE rows (real):
    payment_id  is_synthetic difficulty  syn_type          payer_name                     memo  amount                truth                 pred         alternatives  customer_correct                                                                             
22   PAY-61158         False       hard            Clearwater Digital  Ledgerline subscription  1755.0            INV-21176            INV-21074            INV-21176              True             2 open invoices have this amount (INV-21074, INV-21176). Propose
26   PAY-61365 
… [result truncated, 9262 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && export RULES_PATH=/private/tmp/claude-501/qa2/rules.json DB_PATH=/private/tmp/claude-501/qa2/l.db; mkdir -p /private/tmp/claude-501/qa2; .venv/bin/python analysis/scripts/eval_cash_app.py > analysis/work/eval_cash_app.log 2>&1; sed -n 1,40p analysis/work/eval_cash_app.log | cut -c1-260; .venv/bin/python analysis/scripts/eval_controller.py > analysis/work/eval_controller.log 2>&1; head -14 analysis/work/eval_controller.log; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -v \"^\\[llm\\]\" > analysis/work/eval_guardrails.log; grep \"FAIL\\|SUMMARY\\|Drummond\\|Quill, Mott\\|Reyes\" analysis/work/eval_guardrails.log | cut -c1-330; .venv/bin/python -m app.engine.pipeline",
 "description": "Re-run all eval scripts on current code"
}
```

### Claude · 2026-11-20 18:10:05 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -i '' 's/hard = any(h\\[\"code\"\\] in (\"DISPUTE\", \"MONEY_RECEIVED\", \"CANCELLATION\", \"OPEN_ESCALATION\", \"NO_VALID_CONTACT\")/hard = any(h[\"code\"] in (\"DISPUTE\", \"MONEY_RECEIVED\", \"CANCELLATION\", \"OPEN_ESCALATION\", \"NO_VALID_CONTACT\", \"LEGAL_RISK\")/' analysis/scripts/eval_guardrails.py && grep -c '\"LEGAL_RISK\")' analysis/scripts/eval_guardrails.py; export RULES_PATH=/private/tmp/claude-501/qa2/rules.json DB_PATH=/private/tmp/claude-501/qa2/l.db; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -v \"^\\[llm\\]\" > analysis/work/eval_guardrails.log; grep \"1b\\|2[a-f] \\|^\\[.*\\] 5\\|^\\[.*\\] 4\\|^\\[.*\\] 6\\|^\\[.*\\] 7\\|^\\[.*\\] 9\\|SUMMARY\\|tie\" analysis/work/eval_guardrails.log | cut -c1-300",
 "description": "Fix outdated check and re-run guardrails"
}
```

### Tool · 2026-11-20 18:10:17 UTC
**Tool result:**
```
1
[PASS] 1b Paidly abbreviated payer 'BRANDT' (PAY-65766) :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> HOLD holds=['MONEY_RECEIVED'] to=None | cash agent: EXCEPTION cust=None inv=[] (Payer name 'BRANDT' is not a clear match for any one customer: Studio Brandt (0.55))
[PASS] 1b Paidly abbreviated payer 'JESSOP' (PAY-65750) :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HOLD holds=['MONEY_RECEIVED', 'TOP50'] to=None | cash agent: EXCEPTION cust=None inv=[] (Payer name 'JESSOP' is not a clear match for any one customer: Jessop Legal (0.57))
[PASS] 1b Paidly abbreviated payer 'KINGSWAY' (PAY-65805) :: INV-25469 Kingsway Engineering Group $5,100 111dpd -> HOLD holds=['MONEY_RECEIVED', 'ESCALATE_90', 'RENEWAL_SOON'] to=None | cash agent: EXCEPTION cust=None inv=[] (Payer name 'KINGSWAY' is not a clear match for any one customer: Kingsway 
[PASS] 1b Paidly abbreviated payer 'JESSOP ORWELL' (PAY-65750) :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HOLD holds=['MONEY_RECEIVED', 'TOP50'] to=None | cash agent: PROPOSE cust=C1273 inv=['INV-25784'] (Payer name 'JESSOP ORWELL' is not a clear match for any one customer: Jessop & Orwell
[PASS] 1b Paidly abbreviated payer 'BRANDT LOWELL' (PAY-65766) :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> HOLD holds=['MONEY_RECEIVED'] to=None | cash agent: PROPOSE cust=C1126 inv=['INV-25806'] (Payer name 'BRANDT LOWELL' is not a clear match for any one customer: Brandt & Lowell CPAs (0.70)
[PASS] 2a INV ref, polite question, no refusal :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> HOLD holds=['DISPUTE'] to=None
[PASS] 2b ref without INV- prefix + refusal :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> HOLD holds=['DISPUTE'] to=None
[PASS] 2c 'will not pay' (phrase not in list) :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> HOLD holds=['DISPUTE'] to=None
[PASS] 2d refusal but tagged How-to :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> HOLD holds=['DISPUTE'] to=None
[PASS] 2e soft complaint, no ref, no refusal :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> HOLD holds=['DISPUTE'] to=None
[PASS] 2f untagged, 'refuse to pay' :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> HOLD holds=['DISPUTE'] to=None
[PASS] 4 look-alike contact @thorn-fieldconsultinggr.example :: used=False INV-25862 Thornfield Consulting Group $39,456 17dpd -> DRAFT_REMINDER holds=['STALE_CONTACT'] to=['nadia.vance@thornfieldconsultinggr.example']
[PASS] 4 look-alike contact @thornf
… [result truncated, 5284 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -i '' 's/hard = any(h\\[\"code\"\\] in (\"DISPUTE\", \"MONEY_RECEIVED\", \"CANCELLATION\", \"OPEN_ESCALATION\", \"NO_VALID_CONTACT\")/hard = any(h[\"code\"] in (\"DISPUTE\", \"MONEY_RECEIVED\", \"CANCELLATION\", \"OPEN_ESCALATION\", \"NO_VALID_CONTACT\", \"LEGAL_RISK\")/' analysis/scripts/eval_guardrails.py && grep -c '\"LEGAL_RISK\")' analysis/scripts/eval_guardrails.py; export RULES_PATH=/private/tmp/claude-501/qa2/rules.json DB_PATH=/private/tmp/claude-501/qa2/l.db; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -v \"^\\[llm\\]\" > analysis/work/eval_guardrails.log; grep \"1b\\|2[a-f] \\|^\\[.*\\] 5\\|^\\[.*\\] 4\\|^\\[.*\\] 6\\|^\\[.*\\] 7\\|^\\[.*\\] 9\\|SUMMARY\\|tie\" analysis/work/eval_guardrails.log | cut -c1-300",
 "description": "Fix outdated check and re-run guardrails"
}
```

### Claude · 2026-11-20 18:10:23 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat data/docs/collections_policy.md | head -80; sed -n 13,75p app/engine/context.py",
 "description": "Read collections policy and new heuristic"
}
```

### Tool · 2026-11-20 18:10:24 UTC
**Tool result:**
```
# Collections policy

- Invoices are due 30 days from issue. Card customers are charged on the invoice date.
- Reminders: a courtesy note 5 days before the due date, then at 7, 21 and 45 days past due.
- No message may threaten suspension or legal action without the VP Finance's sign-off. The CEO reads complaints about collections personally.
- Nothing goes to one of the 50 largest accounts without a person reading it first.
- Do not chase an invoice the customer has disputed, or a customer with an open support escalation, until the account manager says so. Tell the account manager before finance contacts one of their accounts.
- Payment plans: the VP Finance can approve up to 90 days. Longer needs the CFO role, currently held by the CEO.
- Write-offs: the VP Finance can approve up to $2,000. Card invoices unpaid after 150 days are written off automatically.
- Cash application: bank transfers and cheques are matched to invoices by hand and can take three to five working days to show as paid.
AGENT = "Account Context"

REFUSAL = [r"will not (?:be )?pay", r"refus\w* to pay", r"overcharg\w+", r"won'?t (?:be )?pay", r"wont (?:be )?pay", r"not (?:be )?paying", r"not authori[sz]ing payment", r"payment is on hold",
           r"paused payment", r"unable to process payment", r"settle once", r"won'?t pay an invoice", r"until (?:it'?s|its) fixed",
           r"void it please", r"cancel and reissue", r"issue a revised invoice", r"remove it and resend", r"we are not paying",
           r"payment (?:is )?on hold", r"pending a corrected invoice", r"not paying for", r"not before", r"we'?ll pay once",
           r"put the whole th", r"reissue it"]
# Unambiguous refusals count in any ticket category (QA T+0:45: "refuse to pay" in a How-to ticket was missed).
STRONG_REFUSAL = [r"will not (?:be )?pay", r"refus\w* to pay", r"won'?t (?:be )?pay", r"wont (?:be )?pay", r"not (?:be )?paying",
                  r"we are not paying", r"not authori[sz]ing payment"]
LEGAL = [r"chargeback", r"contest(?:ing)? the charge", r"consumer affairs", r"lawyer", r"attorney", r"legal action", r"small claims", r"solicitor"]
CANCEL = [r"discontinu\w+ ledgerline", r"termination of services", r"notice of termination", r"cancel(?:l)?ing (?:our )?(?:ledgerline|subscription|account)",
          r"no further direct debits"]
COLLECTIONS_COMPLAINT = [r"already paid", r"chas(?:ed|ing) (?:us|me)", r"reminder (?:email|emails)", r"overdue notice", r"final notice", r"threaten"]


def _any(patterns, text):
    
… [result truncated, 4594 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat data/docs/collections_policy.md | head -80; sed -n 13,75p app/engine/context.py",
 "description": "Read collections policy and new heuristic"
}
```

### Claude · 2026-11-20 18:10:32 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_reads.csv')\nold={'T880019','T880035','T880132','T880311','T880432','T880514','T880519','T880582','T880648','T880667','T880738','T880739','T880757','T880771','T880816','T880849','T880856','T880886','T880915','T880957','T881024','T881039'}\nf=set(t[t.about].ticket_id)\nprint('removed',sorted(old-f),'added',sorted(f-old))\nfor _,x in t[t.ticket_id.isin(f-old)].iterrows(): print(x.ticket_id,x.customer_name,x.category,x.signals,'|',x.body[:300])\n\"",
 "description": "Diff flagged tickets vs previous run"
}
```

### Tool · 2026-11-20 18:10:33 UTC
**Tool result:**
```
removed ['T880132', 'T880915'] added ['T880142']
T880142 Tan Zeller Chartered Accountants Billing overcharg\w+ | Sorry if this is the wrong place to ask. Our finance director wants the correct legal entity name and registered address for Ledgerline, as she intends to send something formal about the overcharging on our retainers last quarter. Could you point me in the right direction?
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_reads.csv')\nold={'T880019','T880035','T880132','T880311','T880432','T880514','T880519','T880582','T880648','T880667','T880738','T880739','T880757','T880771','T880816','T880849','T880856','T880886','T880915','T880957','T881024','T881039'}\nf=set(t[t.about].ticket_id)\nprint('removed',sorted(old-f),'added',sorted(f-old))\nfor _,x in t[t.ticket_id.isin(f-old)].iterrows(): print(x.ticket_id,x.customer_name,x.category,x.signals,'|',x.body[:300])\n\"",
 "description": "Diff flagged tickets vs previous run"
}
```

### Claude · 2026-11-20 18:10:47 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat app/main.py; grep -n \"@router\\.\\|@app\\.\\|def \" app/web/views.py app/web/rig.py | head -120; cat app/web/state.py",
 "description": "List web routes and state module"
}
```

### Tool · 2026-11-20 18:10:47 UTC
**Tool result:**
```
"""Ledgerline Order-to-Cash operator: FastAPI app factory.

Run locally:  uvicorn app.main:app --reload
"""
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app import auth, store
from app.web import chat as chat_web
from app.web import rig as rig_web
from app.web.views import STATIC_DIR, build_router, templates


def create_app() -> FastAPI:
    app = FastAPI(title="Ledgerline AR Operator", docs_url=None, redoc_url=None, openapi_url=None)
    store.init_db()

    @app.middleware("http")
    async def require_login(request: Request, call_next):
        path = request.url.path
        if auth.is_public(path) or auth.current_user(request):
            return await call_next(request)
        if request.headers.get("HX-Request"):
            return PlainTextResponse("login required", status_code=401, headers={"HX-Redirect": "/login"})
        if request.method == "GET":
            nxt = path + (("?" + request.url.query) if request.url.query else "")
            request.session["next"] = nxt
            return RedirectResponse("/login", status_code=303)
        return JSONResponse({"detail": "login required"}, status_code=401)

    # Added after the auth middleware so it wraps it (outermost) and request.session is available inside.
    app.add_middleware(
        SessionMiddleware,
        secret_key=auth.session_secret(),
        session_cookie="ledgerline_session",
        same_site="lax",
        https_only=os.environ.get("BASE_URL", "").startswith("https://"),
        max_age=60 * 60 * 12,
    )

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.include_router(auth.build_router(templates))
    app.include_router(rig_web.build_router())
    app.include_router(chat_web.build_router())
    app.include_router(build_router())

    @app.get("/healthz", response_class=PlainTextResponse)
    async def healthz():
        return "ok"

    return app


app = create_app()
app/web/rig.py:19:def agent_stats(state, slug: str) -> Dict[str, Any]:
app/web/rig.py:45:def agent_queue(state, slug: str, latest) -> List[Dict[str, Any]]:
app/web/rig.py:64:def decisions(state, name: str, n: int) -> List[Dict[str, Any]]:
app/web/rig.py:68:def build_router() -> APIRouter:
app/web/rig.py:72:    async def home(request: Request):
app/web/rig.py:84:    async def team(re
… [result truncated, 9404 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat app/main.py; grep -n \"@router\\.\\|@app\\.\\|def \" app/web/views.py app/web/rig.py | head -120; cat app/web/state.py",
 "description": "List web routes and state module"
}
```

### Claude · 2026-11-20 18:10:53 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"r\\.\\(get\\|post\\)\\|router\\.\\(get\\|post\\)\\|\\.api_route\" app/web/*.py app/auth.py; sed -n 1,60p app/auth.py | grep -n \"AUTH\\|public\\|def \" ",
 "description": "List route paths"
}
```

### Tool · 2026-11-20 18:10:54 UTC
**Tool result:**
```
app/web/rig.py:71:    @r.get("/", response_class=HTMLResponse)
app/web/rig.py:83:    @r.get("/team", response_class=HTMLResponse)
app/web/rig.py:96:    @r.get("/docs", response_class=HTMLResponse)
app/web/rig.py:110:    @r.get("/demo", response_class=HTMLResponse)
app/web/rig.py:114:    @r.post("/demo", response_class=HTMLResponse)
app/web/rig.py:128:    @r.get("/architecture", response_class=HTMLResponse)
app/web/rig.py:132:    @r.get("/activity", response_class=HTMLResponse)
app/web/rig.py:140:    @r.get("/maya", response_class=HTMLResponse)
app/web/rig.py:144:    @r.get("/direct", response_class=HTMLResponse)
app/web/rig.py:151:    @r.post("/direct/instructions")
app/web/rig.py:162:    @r.post("/direct/instructions/{iid}/{decision}")
app/web/rig.py:189:    @r.post("/agents/{slug}/manual")
app/web/rig.py:202:    @r.get("/agents/{slug}", response_class=HTMLResponse)
app/web/rig.py:214:    @r.get("/buildlog", response_class=HTMLResponse)
app/web/chat.py:436:    @r.post("/api/chat")
app/web/chat.py:452:    @r.post("/api/rules/apply")
app/web/rig_data.py:260:        rows = [r for r in rows if r["who"] == who or r.get("agent") == who]
app/auth.py:69:    return user.get("email") if user else None
app/auth.py:104:    @router.get("/login", response_class=HTMLResponse)
app/auth.py:111:    @router.get("/login/google")
app/auth.py:118:    @router.get("/auth/callback", name="auth_callback")
app/auth.py:140:    @router.get("/logout")
app/web/views.py:379:    @r.get("/today", response_class=HTMLResponse)
app/web/views.py:413:    @r.post("/run")
app/web/views.py:420:    @r.get("/cash", response_class=HTMLResponse)
app/web/views.py:425:        pays = sorted(state["payments"], key=lambda p: (order.get(p["decision"], 3), -float(p["amount"] or 0)))
app/web/views.py:443:    @r.post("/cash/{pid}/approve")
app/web/views.py:452:    @r.post("/cash/{pid}/reject")
app/web/views.py:459:    @r.post("/cash/{pid}/undo")
app/web/views.py:468:    @r.get("/collections", response_class=HTMLResponse)
app/web/views.py:493:    @r.post("/collections/{iid}/send")
app/web/views.py:517:    @r.post("/collections/{iid}/reject")
app/web/views.py:524:    @r.post("/collections/{iid}/hold")
app/web/views.py:545:    @r.post("/collections/{iid}/card_retry")
app/web/views.py:559:    @r.get("/customers", response_class=HTMLResponse)
app/web/views.py:581:    @r.get("/customers/{cid}", response_class=HTMLResponse)
app/web/views.py:618:    @r.get("/audit", response_class=HTMLResponse)
app/web/views.py:626: 
… [result truncated, 3181 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"r\\.\\(get\\|post\\)\\|router\\.\\(get\\|post\\)\\|\\.api_route\" app/web/*.py app/auth.py; sed -n 1,60p app/auth.py | grep -n \"AUTH\\|public\\|def \" ",
 "description": "List route paths"
}
```

### Claude · 2026-11-20 18:11:25 UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_policy.py\" <<'EOF'\n\"\"\"QA pass 2, section B: FIN-1 policy compliance on EVERY invoice of run_pipeline() (read-only).\"\"\"\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine.data import AS_OF, domain_of, load, norm_name  # noqa: E402\nfrom app.engine.pipeline import _am_email, run_pipeline  # noqa: E402\nfrom app.engine.rules import DEFAULT_RULES  # noqa: E402\n\ns = run_pipeline(dict(DEFAULT_RULES))\nd = load()\ncus = d[\"customers\"].set_index(\"customer_id\")\ncon = d[\"contacts\"]\ninv_book = d[\"invoices\"].set_index(\"invoice_id\")\nRES = []\n\n\ndef check(name, bad, n):\n    RES.append((name, \"PASS\" if not bad else \"FAIL\", n, len(bad), \"; \".join(map(str, bad[:8]))))\n    print(\"[%s] %s (%d checked, %d bad) %s\" % (\"PASS\" if not bad else \"FAIL\", name, n, len(bad), \"; \".join(map(str, bad[:8]))))\n\n\ndef expected_stage(true_dpd, ar_status):\n    if ar_status == \"payment_failed\":\n        return \"card_failed\"\n    if true_dpd < -5:\n        return \"not_due\"\n    if true_dpd < 0:\n        return \"courtesy\"\n    if true_dpd < 7:\n        return \"wait\"\n    if true_dpd < 21:\n        return \"first\"\n    if true_dpd < 45:\n        return \"second\"\n    if true_dpd < 90:\n        return \"final\"\n    return \"escalate\"\n\n\ninvs = s[\"invoices\"]\nbad = []\nfor i in invs:\n    true_dpd = (AS_OF - pd.Timestamp(i[\"due_date\"])).days\n    e = expected_stage(true_dpd, i[\"ar_status\"])\n    if e != i[\"stage\"]:\n        bad.append(\"%s due %s true_dpd=%d stage=%s expected=%s\" % (i[\"invoice_id\"], i[\"due_date\"], true_dpd, i[\"stage\"], e))\ncheck(\"B1 stage matches policy (-5/+7/+21/+45/+90) using TRUE days past due\", bad, len(invs))\nbad = [i[\"invoice_id\"] for i in invs if i[\"top50\"] and i[\"action\"] == \"DRAFT_REMINDER\"]\ncheck(\"B2 top-50 never DRAFT_REMINDER\", bad, sum(1 for i in invs if i[\"top50\"]))\nBLOCK = {\"PAID\", \"MONEY_RECEIVED\", \"DISPUTE\", \"CANCELLATION\", \"LEGAL_RISK\", \"OPEN_ESCALATION\"}\nbad = [\"%s %s\" % (i[\"invoice_id\"], sorted({h[\"code\"] for h in i[\"holds\"]} & BLOCK)) for i in invs if i[\"draft\"] and {h[\"code\"] for h in i[\"holds\"]} & BLOCK]\ncheck(\"B3 no draft where PAID/MONEY_RECEIVED/DISPUTE/CANCELLATION/LEGAL_RISK/OPEN_ESCALATION\", bad, len(invs))\n\ndrafts = [i for i in invs if i[\"draft\"]]\nprint(\"drafts: %d total (%d DRAFT_REMINDER, %d HUMAN_WRITES)\" % (len(drafts), sum(i[\"action\"] == \"DRAFT_REMINDER\" for i in drafts), sum(i[\"action\"] == \"HUMAN_WRITES\" for i in drafts)))\nbanned = [p.lower() for p in DEFAULT_RULES[\"banned_phrases\"]]\nb4, b5, b6, b7, b8, b9 = [], [], [], [], [], []\nfor i in drafts:\n    dr = i[\"draft\"]\n    text = (dr[\"subject\"] + \"\\n\" + dr[\"body\"]).lower()\n    hit = [p for p in banned if p in text]\n    if hit:\n        b4.append((i[\"invoice_id\"], hit))\n    c = cus.loc[i[\"customer_id\"]]\n    for e in dr[\"to\"]:\n        row = con[(con[\"email\"].str.lower() == e.lower()) & (con[\"customer_id\"] == i[\"customer_id\"])]\n        if not len(row):\n            b5.append((i[\"invoice_id\"], e, \"not in contacts.csv for this customer\"))\n            continue\n        row = row.iloc[0]\n        if domain_of(e) != c[\"domain\"]:\n            b5.append((i[\"invoice_id\"], e, \"domain\"))\n        if row[\"status\"] != \"active\":\n            b6.append((i[\"invoice_id\"], e, row[\"status\"]))\n        if not any(k in row[\"role\"].lower() for k in (\"billing\", \"admin\")):\n            b5.append((i[\"invoice_id\"], e, \"role \" + row[\"role\"]))\n    am = _am_email(c[\"account_manager\"])\n    if am not in dr.get(\"cc\", []):\n        b7.append((i[\"invoice_id\"], dr.get(\"cc\")))\n    amt = \"$\" + format(i[\"amount\"], \",.2f\")\n    for need in (i[\"invoice_id\"], amt):\n        if need not in dr[\"body\"]:\n            b8.append((i[\"invoice_id\"], \"missing \" + need))\n    if dr[\"template\"] != \"courtesy\" and i[\"stage\"] != \"card_failed\" and str(i[\"due_date\"])[:10] not in dr[\"body\"]:\n        b8.append((i[\"invoice_id\"], \"missing due date\"))\n    # ledger cross-check: amount/due in draft = invoices.csv\n    b = inv_book.loc[i[\"invoice_id\"]]\n    if abs(float(b[\"amount\"]) - i[\"amount\"]) > 0.005 or str(b[\"due_date\"])[:10] != str(i[\"due_date\"])[:10]:\n        b8.append((i[\"invoice_id\"], \"ledger mismatch\"))\n    if \"Priya Nair\" not in dr[\"body\"].strip().splitlines()[-2:][0] + dr[\"body\"].strip().splitlines()[-1]:\n        b9.append(i[\"invoice_id\"])\ncheck(\"B4 drafts contain no banned phrase\", b4, len(drafts))\ncheck(\"B5 recipients are verified contacts (in contacts.csv, domain match, billing/admin role)\", b5, len(drafts))\ncheck(\"B6 never a 'left the firm' contact\", b6, len(drafts))\ncheck(\"B7 account manager cc'd\", b7, len(drafts))\ncheck(\"B8 invoice id / amount / due date in body and equal to the ledger\", b8, len(drafts))\ncheck(\"B9 signed off by Priya\", b9, len(drafts))\n# false-positive blocks from substring banned phrases (e.g. 'court' inside 'courtesy')\nfp = [(i[\"invoice_id\"], h[\"detail\"]) for i in invs for h in i[\"holds\"] if h[\"code\"] == \"BANNED_LANGUAGE\"]\ncheck(\"B4b no draft blocked by banned list at baseline (substring false positives)\", fp, len(invs))\n\npays = d[\"payments\"]\nb10 = []\nfor i in invs:\n    codes = {h[\"code\"] for h in i[\"holds\"]}\n    if i[\"action\"] == \"RETRY_CARD\":\n        later = pays[(pays[\"method\"] == \"card\") & (pays[\"payer_name\"].map(norm_name) == norm_name(i[\"customer_name\"])) & (pays[\"received_date\"] > pd.Timestamp(i[\"issue_date\"]))]\n        if not len(later):\n            b10.append((i[\"invoice_id\"], \"no
… [tool input truncated]
```

### Tool · 2026-11-20 18:11:27 UTC
**Tool result:**
```
[FAIL] B1 stage matches policy (-5/+7/+21/+45/+90) using TRUE days past due (117 checked, 61 bad) INV-26019 due 2026-11-18 true_dpd=-18 stage=wait expected=not_due; INV-25950 due 2026-11-04 true_dpd=-4 stage=wait expected=courtesy; INV-26009 due 2026-11-16 true_dpd=-16 stage=wait expected=not_due; INV-26038 due 2026-11-24 true_dpd=-24 stage=wait expected=not_due; INV-26021 due 2026-11-18 true_dpd=-18 stage=wait expected=not_due; INV-25933 due 2026-11-01 true_dpd=-1 stage=wait expected=courtesy; INV-25959 due 2026-11-06 true_dpd=-6 stage=wait expected=not_due; INV-26058 due 2026-11-26 true_dpd=-26 stage=wait expected=not_due
[PASS] B2 top-50 never DRAFT_REMINDER (14 checked, 0 bad) 
[PASS] B3 no draft where PAID/MONEY_RECEIVED/DISPUTE/CANCELLATION/LEGAL_RISK/OPEN_ESCALATION (117 checked, 0 bad) 
drafts: 21 total (20 DRAFT_REMINDER, 1 HUMAN_WRITES)
[PASS] B4 drafts contain no banned phrase (21 checked, 0 bad) 
[PASS] B5 recipients are verified contacts (in contacts.csv, domain match, billing/admin role) (21 checked, 0 bad) 
[PASS] B6 never a 'left the firm' contact (21 checked, 0 bad) 
[PASS] B7 account manager cc'd (21 checked, 0 bad) 
[PASS] B8 invoice id / amount / due date in body and equal to the ledger (21 checked, 0 bad) 
[PASS] B9 signed off by Priya (21 checked, 0 bad) 
[PASS] B4b no draft blocked by banned list at baseline (substring false positives) (117 checked, 0 bad) 
[PASS] B10 card re-runs only with a later successful card charge and no hard hold / legal risk (9 checked, 0 bad) 
[PASS] B11 Dana decisions = card invoices <=10 days from 150-day write-off or > $2,000 (117 checked, 0 bad) 
Dana list: [('INV-25973', 'Eastman Engineering', 3264.0, 23), ('INV-25433', 'Northgate Creative', 799.0, 149), ('INV-25470', 'Hollis Nair Engineers', 517.0, 141)]
Invoices due in the next 1-5 days (policy: courtesy note): [('INV-25950', 'Achebe + Pemberton Architects', -4, 'wait', 'NO_ACTION'), ('INV-25933', 'Whitlock Design Partnership', -1, 'wait', 'NO_ACTION'), ('INV-25932', 'Ambrose & Petrov LLP', -1, 'wait', 'NO_ACTION'), ('INV-25947', 'Jessop Strategy', -4, 'wait', 'NO_ACTION'), ('INV-25956', 'Stanhope Consulting', -5, 'wait', 'NO_ACTION'), ('INV-25943', 'Upton Strategy', -3, 'wait', 'NO_ACTION'), ('INV-25953', 'Hartwell Legal', -5, 'wait', 'NO_ACTION'), ('INV-25951', 'Achebe + Pemberton Architects', -4, 'wait', 'HOLD'), ('INV-25948', 'Hartwell Engineering', -4, 'wait', 'NO_ACTION'), ('INV-25952', 'Birch Petrov Engineers', -5, 'wait', 'NO_ACTION
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_policy.py\" <<'EOF'\n\"\"\"QA pass 2, section B: FIN-1 policy compliance on EVERY invoice of run_pipeline() (read-only).\"\"\"\nimport os\nimport sys\n\nimport pandas as pd\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nsys.path.insert(0, ROOT)\nfrom app.engine.data import AS_OF, domain_of, load, norm_name  # noqa: E402\nfrom app.engine.pipeline import _am_email, run_pipeline  # noqa: E402\nfrom app.engine.rules import DEFAULT_RULES  # noqa: E402\n\ns = run_pipeline(dict(DEFAULT_RULES))\nd = load()\ncus = d[\"customers\"].set_index(\"customer_id\")\ncon = d[\"contacts\"]\ninv_book = d[\"invoices\"].set_index(\"invoice_id\")\nRES = []\n\n\ndef check(name, bad, n):\n    RES.append((name, \"PASS\" if not bad else \"FAIL\", n, len(bad), \"; \".join(map(str, bad[:8]))))\n    print(\"[%s] %s (%d checked, %d bad) %s\" % (\"PASS\" if not bad else \"FAIL\", name, n, len(bad), \"; \".join(map(str, bad[:8]))))\n\n\ndef expected_stage(true_dpd, ar_status):\n    if ar_status == \"payment_failed\":\n        return \"card_failed\"\n    if true_dpd < -5:\n        return \"not_due\"\n    if true_dpd < 0:\n        return \"courtesy\"\n    if true_dpd < 7:\n        return \"wait\"\n    if true_dpd < 21:\n        return \"first\"\n    if true_dpd < 45:\n        return \"second\"\n    if true_dpd < 90:\n        return \"final\"\n    return \"escalate\"\n\n\ninvs = s[\"invoices\"]\nbad = []\nfor i in invs:\n    true_dpd = (AS_OF - pd.Timestamp(i[\"due_date\"])).days\n    e = expected_stage(true_dpd, i[\"ar_status\"])\n    if e != i[\"stage\"]:\n        bad.append(\"%s due %s true_dpd=%d stage=%s expected=%s\" % (i[\"invoice_id\"], i[\"due_date\"], true_dpd, i[\"stage\"], e))\ncheck(\"B1 stage matches policy (-5/+7/+21/+45/+90) using TRUE days past due\", bad, len(invs))\nbad = [i[\"invoice_id\"] for i in invs if i[\"top50\"] and i[\"action\"] == \"DRAFT_REMINDER\"]\ncheck(\"B2 top-50 never DRAFT_REMINDER\", bad, sum(1 for i in invs if i[\"top50\"]))\nBLOCK = {\"PAID\", \"MONEY_RECEIVED\", \"DISPUTE\", \"CANCELLATION\", \"LEGAL_RISK\", \"OPEN_ESCALATION\"}\nbad = [\"%s %s\" % (i[\"invoice_id\"], sorted({h[\"code\"] for h in i[\"holds\"]} & BLOCK)) for i in invs if i[\"draft\"] and {h[\"code\"] for h in i[\"holds\"]} & BLOCK]\ncheck(\"B3 no draft where PAID/MONEY_RECEIVED/DISPUTE/CANCELLATION/LEGAL_RISK/OPEN_ESCALATION\", bad, len(invs))\n\ndrafts = [i for i in invs if i[\"draft\"]]\nprint(\"drafts: %d total (%d DRAFT_REMINDER, %d HUMAN_WRITES)\" % (len(drafts), sum(i[\"action\"] == \"DRAFT_REMINDER\" for i in drafts), sum(i[\"action\"] == \"HUMAN_WRITES\" for i in drafts)))\nbanned = [p.lower() for p in DEFAULT_RULES[\"banned_phrases\"]]\nb4, b5, b6, b7, b8, b9 = [], [], [], [], [], []\nfor i in drafts:\n    dr = i[\"draft\"]\n    text = (dr[\"subject\"] + \"\\n\" + dr[\"body\"]).lower()\n    hit = [p for p in banned if p in text]\n    if hit:\n        b4.append((i[\"invoice_id\"], hit))\n    c = cus.loc[i[\"customer_id\"]]\n    for e in dr[\"to\"]:\n        row = con[(con[\"email\"].str.lower() == e.lower()) & (con[\"customer_id\"] == i[\"customer_id\"])]\n        if not len(row):\n            b5.append((i[\"invoice_id\"], e, \"not in contacts.csv for this customer\"))\n            continue\n        row = row.iloc[0]\n        if domain_of(e) != c[\"domain\"]:\n            b5.append((i[\"invoice_id\"], e, \"domain\"))\n        if row[\"status\"] != \"active\":\n            b6.append((i[\"invoice_id\"], e, row[\"status\"]))\n        if not any(k in row[\"role\"].lower() for k in (\"billing\", \"admin\")):\n            b5.append((i[\"invoice_id\"], e, \"role \" + row[\"role\"]))\n    am = _am_email(c[\"account_manager\"])\n    if am not in dr.get(\"cc\", []):\n        b7.append((i[\"invoice_id\"], dr.get(\"cc\")))\n    amt = \"$\" + format(i[\"amount\"], \",.2f\")\n    for need in (i[\"invoice_id\"], amt):\n        if need not in dr[\"body\"]:\n            b8.append((i[\"invoice_id\"], \"missing \" + need))\n    if dr[\"template\"] != \"courtesy\" and i[\"stage\"] != \"card_failed\" and str(i[\"due_date\"])[:10] not in dr[\"body\"]:\n        b8.append((i[\"invoice_id\"], \"missing due date\"))\n    # ledger cross-check: amount/due in draft = invoices.csv\n    b = inv_book.loc[i[\"invoice_id\"]]\n    if abs(float(b[\"amount\"]) - i[\"amount\"]) > 0.005 or str(b[\"due_date\"])[:10] != str(i[\"due_date\"])[:10]:\n        b8.append((i[\"invoice_id\"], \"ledger mismatch\"))\n    if \"Priya Nair\" not in dr[\"body\"].strip().splitlines()[-2:][0] + dr[\"body\"].strip().splitlines()[-1]:\n        b9.append(i[\"invoice_id\"])\ncheck(\"B4 drafts contain no banned phrase\", b4, len(drafts))\ncheck(\"B5 recipients are verified contacts (in contacts.csv, domain match, billing/admin role)\", b5, len(drafts))\ncheck(\"B6 never a 'left the firm' contact\", b6, len(drafts))\ncheck(\"B7 account manager cc'd\", b7, len(drafts))\ncheck(\"B8 invoice id / amount / due date in body and equal to the ledger\", b8, len(drafts))\ncheck(\"B9 signed off by Priya\", b9, len(drafts))\n# false-positive blocks from substring banned phrases (e.g. 'court' inside 'courtesy')\nfp = [(i[\"invoice_id\"], h[\"detail\"]) for i in invs for h in i[\"holds\"] if h[\"code\"] == \"BANNED_LANGUAGE\"]\ncheck(\"B4b no draft blocked by banned list at baseline (substring false positives)\", fp, len(invs))\n\npays = d[\"payments\"]\nb10 = []\nfor i in invs:\n    codes = {h[\"code\"] for h in i[\"holds\"]}\n    if i[\"action\"] == \"RETRY_CARD\":\n        later = pays[(pays[\"method\"] == \"card\") & (pays[\"payer_name\"].map(norm_name) == norm_name(i[\"customer_name\"])) & (pays[\"received_date\"] > pd.Timestamp(i[\"issue_date\"]))]\n        if not len(later):\n            b10.append((i[\"invoice_id\"], \"no
… [tool input truncated]
```

### Claude · 2026-11-20 18:11:35 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && tail -1 analysis/work/eval_policy.log | grep -o \"('INV\" | wc -l; grep -o \"expected=[a-z_]*\" analysis/work/eval_policy.log | sort | uniq -c; .venv/bin/python -c \"\nimport pandas as pd\na=pd.read_csv('data/finance/ar_aging.csv'); a['t']=(pd.Timestamp('2026-10-31')-pd.to_datetime(a.due_date)).dt.days\nx=a[(a.t>=-5)&(a.t<0)]; print(len(x), x.amount.sum()); print((a.t<0).sum(), (a.days_past_due!=a.t).sum())\"",
 "description": "Count courtesy-window invoices"
}
```

### Tool · 2026-11-20 18:11:36 UTC
**Tool result:**
```
      16
   2 expected=courtesy
   6 expected=not_due
16 219071.0
61 61
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && tail -1 analysis/work/eval_policy.log | grep -o \"('INV\" | wc -l; grep -o \"expected=[a-z_]*\" analysis/work/eval_policy.log | sort | uniq -c; .venv/bin/python -c \"\nimport pandas as pd\na=pd.read_csv('data/finance/ar_aging.csv'); a['t']=(pd.Timestamp('2026-10-31')-pd.to_datetime(a.due_date)).dt.days\nx=a[(a.t>=-5)&(a.t<0)]; print(len(x), x.amount.sum()); print((a.t<0).sum(), (a.days_past_due!=a.t).sum())\"",
 "description": "Count courtesy-window invoices"
}
```

### Claude · 2026-11-20 18:11:42 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 140,225p app/web/views.py; sed -n 375,700p app/web/views.py",
 "description": "Read views.py key handlers"
}
```

### Tool · 2026-11-20 18:11:42 UTC
**Tool result:**
```
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
    whats = {"HOLD": "Review hold", "HUMAN_WRITES": "Write to customer
… [result truncated, 23293 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 140,225p app/web/views.py; sed -n 375,700p app/web/views.py",
 "description": "Read views.py key handlers"
}
```

### Claude · 2026-11-20 18:11:54 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"def \\|status\\|from now on\\|set \\|RELEASE_NEEDS_AM\" app/web/chat.py | head -60; grep -n \"RELEASE_NEEDS_AM\" app/web/views.py | head -3",
 "description": "Skim chat.py structure"
}
```

### Claude · 2026-11-20 18:11:57 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 160,222p app/web/chat.py; sed -n 330,483p app/web/chat.py; sed -n 140,229p app/web/rig.py",
 "description": "Read chat intents and rig handlers"
}
```

### Tool · 2026-11-20 18:11:58 UTC
**Tool result:**
```
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
   
… [result truncated, 17229 chars total]
```

### Tool · 2026-11-20 18:11:58 UTC
**Tool result:**
```
5:If RIG_CHAT_AI=on, ANTHROPIC_API_KEY is set and rules.use_claude is true, Claude rephrases the deterministic answer.
24:would will please tell show give status summary held hold holds hold's paid pay payment payments invoice invoices
25:customer customers draft drafts email emails today needs need now set run rerun re help team cash context controller
29:def _money(v) -> str:
36:def _money2(v) -> str:
43:def _norm(s: str) -> str:
53:def find_customers(state, text: str) -> List[Dict[str, Any]]:
85:def _pick_agent(text: str, default: str = "team") -> str:
98:def explain_customer(state, c: Dict[str, Any], agent: str) -> Tuple[str, List[Dict[str, Any]]]:
158:def explain_invoice(state, iid: str) -> Optional[Tuple[str, List[Dict[str, Any]]]]:
175:def explain_payment(state, pid: str) -> Optional[Tuple[str, List[Dict[str, Any]]]]:
185:def team_summary(state, agent: str) -> Tuple[str, List[Dict[str, Any]]]:
209:def holds_summary(state) -> Tuple[str, List[Dict[str, Any]]]:
225:def needs_me(state) -> Tuple[str, List[Dict[str, Any]]]:
234:def _rule_lookup(name: str, rules: Dict[str, Any]) -> Optional[str]:
255:def parse_rule_value(rules: Dict[str, Any], key: str, raw: str):
275:        raise ValueError("set one item, e.g. 'set reminder_days.first to 10'")
279:def apply_rule(user: str, key: str, value) -> Dict[str, Any]:
302:    "status  ·  @controller status  ·  what did you do",
304:    "set writeoff_threshold to 50  ·  set fee tolerance to 25 (you confirm with Apply)",
306:    "from now on cc Dana on anything over $40k  (logged as a proposed instruction)",
311:def answer(state, message: str, agent: Optional[str], user: str) -> Dict[str, Any]:
328:    if re.match(r"^(from now on|instruction:|always\b|never\b)", low):
403:    if re.search(r"(status|what did you do|summary|summarise|summarize|how are we|overview|numbers)", low):
412:def _maybe_claude(state, res: Dict[str, Any], message: str) -> Dict[str, Any]:
433:def build_router() -> APIRouter:
437:    async def api_chat(request: Request):
453:    async def api_rules_apply(request: Request):
28:RELEASE_NEEDS_AM = ("DISPUTE", "CANCELLATION")
535:        needs_am = [h for h in holds if h.get("code") in RELEASE_NEEDS_AM]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"def \\|status\\|from now on\\|set \\|RELEASE_NEEDS_AM\" app/web/chat.py | head -60; grep -n \"RELEASE_NEEDS_AM\" app/web/views.py | head -3",
 "description": "Skim chat.py structure"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 160,222p app/web/chat.py; sed -n 330,483p app/web/chat.py; sed -n 140,229p app/web/rig.py",
 "description": "Read chat intents and rig handlers"
}
```

### Claude · 2026-11-20 18:12:04 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"environ\\|PATH\\|DIR\\|def \" app/web/rig_data.py app/store.py | head -60; sed -n 100,130p app/web/rig.py; sed -n 340,375p app/web/views.py",
 "description": "Check file paths used by RIG and store"
}
```

### Tool · 2026-11-20 18:12:04 UTC
**Tool result:**
```
app/store.py:19:def db_path() -> str:
app/store.py:20:    return os.environ.get("DB_PATH", os.path.join(os.getcwd(), "ledgerline.db"))
app/store.py:23:def _connect() -> sqlite3.Connection:
app/store.py:33:def init_db() -> None:
app/store.py:79:def record(user_email: str, object_type: str, object_id: str, action: str, note: str = "",
app/store.py:92:def _row(r: sqlite3.Row) -> Dict[str, Any]:
app/store.py:101:def all_actions() -> List[Dict[str, Any]]:
app/store.py:106:def latest_by_object() -> Dict[str, Dict[str, Any]]:
app/store.py:114:def history(object_type: str, object_id: str) -> List[Dict[str, Any]]:
app/store.py:120:def _now() -> str:
app/store.py:128:def add_instruction(user: str, agent: str, text: str, source: str = "form") -> int:
app/store.py:135:def instructions(agent: Optional[str] = None) -> List[Dict[str, Any]]:
app/store.py:144:def get_instruction(iid: int) -> Optional[Dict[str, Any]]:
app/store.py:150:def decide_instruction(iid: int, status: str, user: str) -> None:
app/store.py:159:def add_chat(user: str, agent: str, message: str, reply: str, mode: str) -> int:
app/store.py:166:def chats(limit: int = 500) -> List[Dict[str, Any]]:
app/store.py:172:def get_setting(key: str) -> Optional[str]:
app/store.py:178:def set_setting(key: str, value: str, user: str) -> None:
app/store.py:189:def _mq(r: sqlite3.Row) -> Dict[str, Any]:
app/store.py:199:def sync_maya_questions(qs: List[Dict[str, Any]]) -> Dict[str, int]:
app/store.py:228:def maya_questions(status: Optional[str] = None) -> List[Dict[str, Any]]:
app/store.py:237:def get_maya_question(qid: str) -> Optional[Dict[str, Any]]:
app/store.py:243:def update_maya_question(qid: str, **fields) -> None:
app/store.py:256:def maya_sent_bundles() -> int:
app/web/rig_data.py:9:WEB_DIR = os.path.dirname(os.path.abspath(__file__))
app/web/rig_data.py:10:ROOT_DIR = os.path.dirname(os.path.dirname(WEB_DIR))
app/web/rig_data.py:11:MANUALS_DIR = os.environ.get("MANUALS_DIR", os.path.join(ROOT_DIR, "app", "engine", "manuals"))
app/web/rig_data.py:72:def hold_override_rate() -> Dict[str, Any]:
app/web/rig_data.py:113:def build_clock() -> str:
app/web/rig_data.py:122:def manual_path(agent: Dict[str, Any]) -> str:
app/web/rig_data.py:123:    return os.path.join(MANUALS_DIR, agent["manual"] + ".md")
app/web/rig_data.py:126:def read_manual(agent: Dict[str, Any]) -> str:
app/web/rig_data.py:134:def write_manual(agent: Dict[str, Any], text: str) -> None:
app/web/rig_data.py:135:    os.makedirs(MANUALS_DIR, exist_ok=Tru
… [result truncated, 6119 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"environ\\|PATH\\|DIR\\|def \" app/web/rig_data.py app/store.py | head -60; sed -n 100,130p app/web/rig.py; sed -n 340,375p app/web/views.py",
 "description": "Check file paths used by RIG and store"
}
```

### Claude · 2026-11-20 18:12:10 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 1,30p app/auth.py; sed -n 55,100p app/auth.py; ls app/engine/manuals",
 "description": "Read auth dev mode logic"
}
```

### Tool · 2026-11-20 18:12:10 UTC
**Tool result:**
```
"""Google OAuth (Authlib) with a domain + email allow-list.

Env:
  GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET  OAuth client. If GOOGLE_CLIENT_ID is unset the app runs in DEV MODE:
                                           everyone is auto-logged-in as dev@localhost and a yellow banner says so.
  SESSION_SECRET                           signs the session cookie.
  ALLOWED_DOMAINS                          comma list, default "scaleworks.com". Needs hd claim == domain AND email
                                           domain == domain AND email_verified.
  ALLOWED_EMAILS                           comma list of individual addresses always allowed (email_verified needed).
  BASE_URL                                 public URL, used to build the redirect URI <BASE_URL>/auth/callback.
"""
import os
import secrets
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

DEV_EMAIL = "dev@localhost"
PUBLIC_PATHS = ("/login", "/login/google", "/auth/callback", "/logout", "/healthz")
PUBLIC_PREFIXES = ("/static/",)


def dev_mode() -> bool:
    return not os.environ.get("GOOGLE_CLIENT_ID")


def _csv(name: str, default: str = "") -> List[str]:
    return [x.strip().lower() for x in os.environ.get(name, default).split(",") if x.strip()]

    if email in allowed_emails():
        return True, "allow-listed email"
    domain = email.rsplit("@", 1)[-1]
    hd = (userinfo.get("hd") or "").strip().lower()
    if domain in allowed_domains() and hd == domain:
        return True, "allowed Google Workspace domain"
    return False, "{} is not allowed. Sign in with a {} Google Workspace account.".format(
        email, " or ".join(allowed_domains()) or "permitted")


def current_user(request: Request) -> Optional[str]:
    if dev_mode():
        return DEV_EMAIL
    user = request.session.get("user")
    return user.get("email") if user else None


def is_public(path: str) -> bool:
    return path in PUBLIC_PATHS or any(path.startswith(p) for p in PUBLIC_PREFIXES)


_oauth = None


def _get_oauth():
    global _oauth
    if _oauth is None:
        from authlib.integrations.starlette_client import OAuth
        _oauth = OAuth()
        _oauth.register(
            name="google",
            client_id=os.environ.get("GOOGLE_CLIENT_ID"),
            client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
            server_metadata_url="https://accounts.google.com/.well-known/openid-conf
… [result truncated, 2871 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 1,30p app/auth.py; sed -n 55,100p app/auth.py; ls app/engine/manuals",
 "description": "Read auth dev mode logic"
}
```

### Claude · 2026-11-20 18:12:23 UTC
**Tool call:** `Bash`
```json
{
 "command": "mkdir -p /private/tmp/claude-501/qa2/html && cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && rm -rf /private/tmp/claude-501/qa2/manuals && cp -R app/engine/manuals /private/tmp/claude-501/qa2/manuals && rm -f /private/tmp/claude-501/qa2/l.db /private/tmp/claude-501/qa2/rules.json && DB_PATH=/private/tmp/claude-501/qa2/l.db RULES_PATH=/private/tmp/claude-501/qa2/rules.json MANUALS_DIR=/private/tmp/claude-501/qa2/manuals .venv/bin/python -c \"\nimport time,re\nfrom fastapi.testclient import TestClient\nfrom app.main import app\nc=TestClient(app)\npages=['/','/team','/docs','/demo','/architecture','/activity','/maya','/direct','/agents/cash','/agents/context','/agents/controller','/agents/collections','/buildlog','/today','/cash','/collections','/customers','/customers/C1469','/audit','/audit.csv','/rules','/digest','/about','/healthz']\nfor p in pages:\n    t=time.time(); r=c.get(p); dt=time.time()-t\n    open('/private/tmp/claude-501/qa2/html/'+(p.strip('/').replace('/','_') or 'home')+'.html','w').write(r.text)\n    txt=re.sub('<[^>]+>',' ',r.text)\n    flags=[k for k in ['coming soon','Coming soon','TODO','lorem','placeholder','FAKE','fake data','Traceback','undefined','TBD','XXX','{{','nan','None'] if k in txt]\n    print(p, r.status_code, '%.2fs'%dt, len(r.text), flags)\n\"",
 "description": "Fetch all pages locally with timing"
}
```

### Tool · 2026-11-20 18:12:26 UTC
**Tool result:**
```
/ 200 1.05s 27611 ['nan']
/team 200 0.02s 26941 ['nan']
/docs 200 0.01s 24257 ['nan']
/demo 200 0.01s 20495 ['Coming soon', 'nan']
/architecture 200 0.01s 17411 ['nan']
/activity 200 0.01s 61788 ['nan']
/maya 200 0.03s 27442 ['nan']
/direct 200 0.03s 29343 ['nan']
/agents/cash 200 0.01s 15597 ['nan']
/agents/context 200 0.01s 20076 ['nan']
/agents/controller 200 0.01s 23937 ['nan']
/agents/collections 200 0.00s 25089 ['nan']
/buildlog 200 0.08s 140432 ['placeholder', 'nan', 'None']
/today 200 0.01s 36264 ['nan']
/cash 200 0.01s 26256 ['nan']
/collections 200 0.03s 243160 ['nan']
/customers 200 0.01s 47759 ['nan']
/customers/C1469 200 0.02s 13527 ['nan']
/audit 200 0.01s 73448 ['nan']
/audit.csv 200 0.00s 22227 []
/rules 200 0.01s 16590 ['nan']
/digest 200 0.00s 11337 ['nan']
/about 200 0.01s 11985 ['nan']
/healthz 200 0.00s 2 []
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "mkdir -p /private/tmp/claude-501/qa2/html && cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && rm -rf /private/tmp/claude-501/qa2/manuals && cp -R app/engine/manuals /private/tmp/claude-501/qa2/manuals && rm -f /private/tmp/claude-501/qa2/l.db /private/tmp/claude-501/qa2/rules.json && DB_PATH=/private/tmp/claude-501/qa2/l.db RULES_PATH=/private/tmp/claude-501/qa2/rules.json MANUALS_DIR=/private/tmp/claude-501/qa2/manuals .venv/bin/python -c \"\nimport time,re\nfrom fastapi.testclient import TestClient\nfrom app.main import app\nc=TestClient(app)\npages=['/','/team','/docs','/demo','/architecture','/activity','/maya','/direct','/agents/cash','/agents/context','/agents/controller','/agents/collections','/buildlog','/today','/cash','/collections','/customers','/customers/C1469','/audit','/audit.csv','/rules','/digest','/about','/healthz']\nfor p in pages:\n    t=time.time(); r=c.get(p); dt=time.time()-t\n    open('/private/tmp/claude-501/qa2/html/'+(p.strip('/').replace('/','_') or 'home')+'.html','w').write(r.text)\n    txt=re.sub('<[^>]+>',' ',r.text)\n    flags=[k for k in ['coming soon','Coming soon','TODO','lorem','placeholder','FAKE','fake data','Traceback','undefined','TBD','XXX','{{','nan','None'] if k in txt]\n    print(p, r.status_code, '%.2fs'%dt, len(r.text), flags)\n\"",
 "description": "Fetch all pages locally with timing"
}
```

### Claude · 2026-11-20 18:12:30 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2/html && for f in *.html; do n=$(sed 's/<[^>]*>/ /g' $f | grep -oE \"\\b(nan|NaN|None|null)\\b\" | sort | uniq -c | tr '\\n' ' '); [ -n \"$n\" ] && echo \"$f: $n\"; done; sed 's/<[^>]*>/ /g' demo.html | grep -i -B2 -A2 \"coming soon\" | tr -s ' \\n' ' ' | cut -c1-400; echo; sed 's/<[^>]*>/ /g' buildlog.html | grep -i \"placeholder\" | head -5 | cut -c1-200",
 "description": "Scan pages for nan/None and placeholders"
}
```

### Tool · 2026-11-20 18:12:31 UTC
**Tool result:**
```
about.html:    1 null 
activity.html:    1 null 
agents_cash.html:    1 null 
agents_collections.html:    1 null 
agents_context.html:    1 null 
agents_controller.html:    1 null 
architecture.html:    1 null 
audit.html:    1 null 
buildlog.html:    4 None    2 null 
cash.html:    1 null 
collections.html:    1 null 
customers.html:    1 null 
customers_C1469.html:    1 null 
demo.html:    1 null 
digest.html:    1 null 
direct.html:    1 null 
docs.html:    1 null 
home.html:    1 null 
maya.html:    1 null 
rules.html:    1 null 
team.html:    1 null 
today.html:    1 null 
 Coming soon Loom walkthrough coming — 5–10 min What we chose, why, how, the tool on real records, and where it gets things wrong. 
 Logged Exchange 4 word for word and added D12 to D15. Made the Maya files consistent for the RIG parser. Put Draft 4 on hold, because it is a status update under the T+0:25 rule. Drafted Draft 6 (REA
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2/html && for f in *.html; do n=$(sed 's/<[^>]*>/ /g' $f | grep -oE \"\\b(nan|NaN|None|null)\\b\" | sort | uniq -c | tr '\\n' ' '); [ -n \"$n\" ] && echo \"$f: $n\"; done; sed 's/<[^>]*>/ /g' demo.html | grep -i -B2 -A2 \"coming soon\" | tr -s ' \\n' ' ' | cut -c1-400; echo; sed 's/<[^>]*>/ /g' buildlog.html | grep -i \"placeholder\" | head -5 | cut -c1-200",
 "description": "Scan pages for nan/None and placeholders"
}
```

### Claude · 2026-11-20 18:12:35 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2/html && for f in home team maya; do echo \"=== $f\"; sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $f.html | tr -s ' \\n\\t' ' ' | cut -c1-3500; echo; done",
 "description": "Dump visible text of home, team, maya"
}
```

### Tool · 2026-11-20 18:12:35 UTC
**Tool result:**
```
=== home
 Ledgerline · Finance Team RIG LEDGERLINE · FINANCE TEAM RIG · ORDER-TO-CASH The finance team, on one screen Four AI agents and the people who direct them, collecting cash on Ledgerline's real records. Agents propose; Priya, Dana and the account managers decide. Every step is logged. AI OFF — pending Legal DPA Rules-only mode Simulated: nothing sent Auth off (demo) JM JACEK MATERNA AI OPERATOR · LEDGERLINE Data as of 31 Oct 2026 · Build T+1:02 Agents ran 2026-11-20 12:12:25 (0.34s) Home Team Architecture Documentation Activity Maya Direct the team Build log One pager Demo | Today Cash Collections Customers Digest Audit Rules Run agents Mission · why this team exists An Order-to-Cash team for Dana Ruiz (VP Finance) Collections (FIN-1), plus Cash Application (FIN-2), which feeds it. Customers get chased for invoices they&#39;ve already paid because matching payments lags 3–5 days. They also get chased while they have an open support complaint, because finance can&#39;t see support tickets. Our promise Never chase money we already have Never chase a customer mid-dispute A person approves everything that reaches a customer or the ledger Where we are T+0:05 Chose the process with Maya T+0:12 Four agents live on real records T+0:32 Maya approved rules-only go-live with Priya on Monday T+0:36 Data-room QA: AR ties out, 14 disputes verified against contracts now RIG live on Render for review Mon Monday: Priya walkthrough, Dana decisions, Legal reviews Bedrock note +30d +30 days: hold-override rate back to Maya Today: $78,348 already received would have been chased · $312,922 held in disputes · 20 drafts waiting for Priya Overdue balance · headline metric $633,245 54 invoices on the ledger Already received $78,348 Disputed $312,922 Collectable $241,975 Chases prevented 23 would have gone to customers who paid or dispute Drafts awaiting Priya 20 of 20 drafted · 3 to write personally Card re-runs 9 card works again · Priya approves each Dana decisions 3 Eastman Engineering $3,264 · Northgate Creative $799 Veto · complaints caused 0 by this tool since go-live · baseline 2 in last 120 days The team Four agents, in the order they run $ AGENT 01 · FIN-2 1. Cash Application Matches unapplied bank and card receipts to open invoices, first, so we never chase money we have. $87,335 cash found in unapplied receipts 3 auto-applied · 4 to confirm AGENT 02 · READ-ONLY 2. Account Context One view of each customer: tickets, NPS, usage, contract, renewal, contacts. Finance
… [result truncated, 10465 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2/html && for f in home team maya; do echo \"=== $f\"; sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $f.html | tr -s ' \\n\\t' ' ' | cut -c1-3500; echo; done",
 "description": "Dump visible text of home, team, maya"
}
```

### Claude · 2026-11-20 18:12:46 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls trail; grep -n \"^### \\|^## \\|^\\*\\*Maya\" trail/MAYA_QA.md | cut -c1-150; grep -n \"^#\\|Status\\|status\" trail/MAYA_OUTBOX.md | head -30; sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' /private/tmp/claude-501/qa2/html/maya.html | tr -s ' \\n\\t' ' ' | grep -o \"Exchange [0-9][^.]\\{0,60\\}\\|Pending[^.]\\{0,300\\}\\|pending[^.]\\{0,200\\}\\|Draft [0-9][^.]\\{0,120\\}\" | head -20",
 "description": "Compare Maya tab with trail files"
}
```

### Tool · 2026-11-20 18:12:46 UTC
**Tool result:**
```
DECISIONS.md
JOURNAL.md
MAYA_OUTBOX.md
MAYA_QA.md
SUBMISSION_CHECKLIST.md
6:## Prepared questions (refine after the data-room read, ask in hour 2)
27:## Log
30:### Exchange 1 — 11:14 CST, T+0:04
33:**Maya:** Hi, Maya here. I am around all day, so ask whenever something comes up. What are you thinking of building?
37:**Maya:** Hi Jacek. Paidly chased a long-standing customer who had already paid by wire, because the money took days to be matched, and nobody had 
50:### Exchange 2 — 11:26 CST, T+0:16
55:**Maya:** Those numbers are worth showing Dana today, especially the $312k sitting in "solved" tickets. On re-running cards, I'd want Priya to appr
68:### Exchange 3 — ~11:28 CST, T+0:18
73:**Maya:** That's the answer I needed. Bedrock under the AWS agreement we already have is the route I'd rather take to Legal, but they'll want to co
84:### Exchange 4 — ~11:42 CST, T+0:32
89:**Maya:** Yes, Monday with the rules-only version, as long as Priya approves every match, release and email, and Dana has seen the Northgate decisi
1:# Maya outbox — drafts written by the test-steward, sent by the main thread
5:Rule since T+0:25 (Jacek): a draft goes to Maya only for a **Confirmation** (a decision she or Dana owns) or **Intel** (facts the data room can't give). No pure status updates. Every draft starts with a `Purpose:` line. Drafts 1 to 3 predate the rule, so their Purpose lines were added afterwards.
7:## Draft 1 — what we're building (SENT 11:14, T+0:04)
11:## Draft 2 — first results on real records (SENT 11:26, T+0:16, revised by the main thread before sending)
22:## Draft 3 — AI provider and data (SENT ~11:28, T+0:18, written by the main thread)
26:## Draft 4 — app live on Render (ON HOLD at T+0:32, drafted 11:30, T+0:20; do not send as written)
27:Purpose: none that qualifies under the T+0:25 rule. Why it is on hold: it is mostly a status update. Its first question (Priya trying the tool) is overtaken by Maya's "book thirty minutes with Priya" (Exchange 4). Its second question (Legal) is answered: Maya takes the note to Legal this week. Send the live link to Maya only together with a real Confirmation or Intel ask.
35:## Draft 5 — note for Legal, misses on real records, Monday go-live (SENT ~11:42, T+0:32, written by the main thread)
39:## Draft 6 — Dana's two decisions before Monday (READY, drafted 11:46, T+0:36)
pending Legal DPA Rules-only mode Simulated: nothing sent Auth off (demo) JM JACEK MATERNA AI OPERATOR · LEDGERLINE Data as of 31 Oct 2026 · Build T+1:
… [result truncated, 3338 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls trail; grep -n \"^### \\|^## \\|^\\*\\*Maya\" trail/MAYA_QA.md | cut -c1-150; grep -n \"^#\\|Status\\|status\" trail/MAYA_OUTBOX.md | head -30; sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' /private/tmp/claude-501/qa2/html/maya.html | tr -s ' \\n\\t' ' ' | grep -o \"Exchange [0-9][^.]\\{0,60\\}\\|Pending[^.]\\{0,300\\}\\|pending[^.]\\{0,200\\}\\|Draft [0-9][^.]\\{0,120\\}\" | head -20",
 "description": "Compare Maya tab with trail files"
}
```

### Claude · 2026-11-20 18:12:57 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && H=/private/tmp/claude-501/qa2/html; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' '; }; echo \"== today\"; strip $H/today.html | sed 's/.*Run agents//' | cut -c1-1600; echo; echo \"== collections\"; strip $H/collections.html | sed 's/.*Run agents//' | grep -oE \"(Draft|Hold|Held|Human|Write|Card|No action|Nothing|Paid|Reminder)[A-Za-z ,'-]{0,60}[0-9]+ invoice[s]?[^·]{0,40}\" | head -12; echo \"== digest\"; strip $H/digest.html | sed 's/.*Run agents//' | cut -c1-1800; echo; echo \"== team context/controller/collections cards\"; strip $H/team.html | grep -oE \"AGENT 0[234][^&]{0,400}\" | cut -c1-300",
 "description": "Extract numbers from today, collections, digest, team"
}
```

### Tool · 2026-11-20 18:12:57 UTC
**Tool result:**
```
== today
 Today Good morning. Here is what the agents did overnight and what needs a person. Overdue balance $633,245 54 overdue invoices &middot; open AR $1,430,632 Already received $78,348 Disputed $312,922 Collectable $241,975 Cash found $87,335 unapplied receipts matched to invoices that looked unpaid Chases prevented 23 reminders that would have gone to customers who already paid or are in dispute Drafts awaiting approval 20 of 20 drafted &middot; 3 for you to write Card re-runs 9 of 9 failed card charges where the card works again; approve each one Holds 21 of 21 held by the Controller still unreviewed Collections complaints veto 0 caused by this tool since go-live. Above zero = stop and review. Existing in last 120 days: 2 (read by agent) &middot; a keyword count said 14 Decisions for Dana today (3) INV-25973 Eastman Engineering $3,264.00 Auto write-off would exceed Dana&#39;s $2,000 limit Card invoices write off automatically at 150 days, but write-offs over $2,000 need the VP Finance. 9 past auto write-offs ($47,251) breached this limit. INV-25433 Northgate Creative $799.00 Decision for Dana today: Automatic card write-off in 1 days Policy writes off card invoices unpaid at 150 days. Decide now: call the customer or let it write off. INV-25470 Hollis Nair Engineers $517.00 Decision for Dana today: Automatic card write-off in 9 days Policy writes off card invoices unpaid at 150 days. Decide now: call the customer or let it write off. Needs you today (57 items, $715,087) Largest first. Nothing here goes out or touches the ledger until you approve it. Amount Customer Item Agen

== collections
== digest
 Morning digest What Priya sees in Slack before she opens the app. L Ledgerline AR Operator APP 7:30 AM Good morning Priya. Collections for 2026-10-31 Overdue on the ledger: $633,245 (54 invoices). Already received: $78,348. Disputed: $312,922. Collectable: $241,975 . ✅ Applied overnight (exact amount + invoice reference): 3 • Castellano, Crane &amp; Co $3,672 → INV-25845 • Studio Zeller $987 → INV-25937 • Yardley &amp; Duarte Advisory $564 → INV-25867 👀 Payments to confirm: 4 • Jessop &amp; Orwell Agency $62,688 → INV-25784 (confidence 82%) • Brandt &amp; Lowell CPAs $6,324 → INV-25806 (confidence 82%) • Achebe + Pemberton Architects $8,000 → INV-25951 (confidence 82%) • Kingsway Engineering Group $5,100 → INV-25469 (confidence 55%) 🚨 Needs Dana today: Eastman Engineering $3,264 (Auto write-off would exceed Dana&#39;s $2,000 limit); Northgate Creative
… [result truncated, 4145 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && H=/private/tmp/claude-501/qa2/html; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' '; }; echo \"== today\"; strip $H/today.html | sed 's/.*Run agents//' | cut -c1-1600; echo; echo \"== collections\"; strip $H/collections.html | sed 's/.*Run agents//' | grep -oE \"(Draft|Hold|Held|Human|Write|Card|No action|Nothing|Paid|Reminder)[A-Za-z ,'-]{0,60}[0-9]+ invoice[s]?[^·]{0,40}\" | head -12; echo \"== digest\"; strip $H/digest.html | sed 's/.*Run agents//' | cut -c1-1800; echo; echo \"== team context/controller/collections cards\"; strip $H/team.html | grep -oE \"AGENT 0[234][^&]{0,400}\" | cut -c1-300",
 "description": "Extract numbers from today, collections, digest, team"
}
```

### Claude · 2026-11-20 18:13:06 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2/html && grep -oE \"<h[23][^>]*>[^<]{0,120}(<[^>]+>[^<]{0,60}){0,4}\" collections.html | sed 's/<[^>]*>/ /g' | tr -s ' ' | head -20; grep -n \"ACTION_TITLES\\|ACTION_ORDER\" \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web/views.py\" | head -3; sed -n 1,40p \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web/templates/collections.html\"",
 "description": "Inspect collections group headings"
}
```

### Tool · 2026-11-20 18:13:06 UTC
**Tool result:**
```
 Held by the Controller (21, $397,528) 
 Card re-runs to approve (9, $8,551) 
 A person writes these (top-50 accounts) (3, $47,602) 
 Drafts awaiting your approval (20, $179,294) 
 No action needed (64, $797,657) 
27:ACTION_ORDER = ["HOLD", "RETRY_CARD", "HUMAN_WRITES", "DRAFT_REMINDER", "NO_ACTION"]
29:ACTION_TITLES = {
477:        for a in ACTION_ORDER:
{% extends "base.html" %}
{% block title %}Collections · Ledgerline{% endblock %}
{% block content %}
<h1>Collections</h1>
<p class="lead">Every open invoice, after Cash Application and the Controller have had their say. Click a row to see why, the holds, and the draft.</p>
<form class="filters" method="get" action="/collections">
  <input class="input" name="q" value="{{ q }}" placeholder="Filter by customer or invoice">
  <button class="btn btn-sm">Filter</button>{% if q %} <a class="small" href="/collections">clear</a>{% endif %}
  <span class="jump small">Jump to: {% for g in groups %}<a href="#g-{{ g.action }}">{{ g.action|replace('_',' ')|lower }} ({{ g.rows|length }})</a>{% if not loop.last %} &middot; {% endif %}{% endfor %}</span>
</form>
{% for g in groups %}
<section id="g-{{ g.action }}">
  <div class="section-head">
    <h2>{{ g.title }} <span class="muted">({{ g.rows|length }}, {{ g.total|money }})</span></h2>
  </div>
  <p class="small muted">{{ g.help }}</p>
  {% if g.rows %}
  <div class="list">
    <div class="row row-inv row-head"><span>Invoice</span><span>Customer</span><span class="num">Amount</span><span>Due</span><span>Stage</span><span>Reason</span><span>Status</span></div>
    {% for i in g.rows %}{% set open = false %}{% include "_invoice.html" %}{% endfor %}
  </div>
  {% else %}<div class="empty">None.</div>{% endif %}
</section>
{% endfor %}
{% endblock %}
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2/html && grep -oE \"<h[23][^>]*>[^<]{0,120}(<[^>]+>[^<]{0,60}){0,4}\" collections.html | sed 's/<[^>]*>/ /g' | tr -s ' ' | head -20; grep -n \"ACTION_TITLES\\|ACTION_ORDER\" \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web/views.py\" | head -3; sed -n 1,40p \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web/templates/collections.html\"",
 "description": "Inspect collections group headings"
}
```

### Claude · 2026-11-20 18:13:21 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 254,340p app/web/views.py; sed -n 236,265p app/web/rig_data.py; sed -n 279,300p app/web/chat.py",
 "description": "Read rules parsing and activity feed"
}
```

### Tool · 2026-11-20 18:13:21 UTC
**Tool result:**
```
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
    if isinstance
… [result truncated, 7061 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 254,340p app/web/views.py; sed -n 236,265p app/web/rig_data.py; sed -n 279,300p app/web/chat.py",
 "description": "Read rules parsing and activity feed"
}
```

### Claude · 2026-11-20 18:14:16 UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_web.py\" <<'EOF'\n\"\"\"QA pass 2, sections C (consistency) and D (human-action flows) via FastAPI TestClient.\nUses a throw-away DB, rules file and manuals copy so ./ledgerline.db, ./rules.json and app/engine/manuals are untouched.\nUsage: eval_web.py <tmpdir>\"\"\"\nimport json\nimport os\nimport re\nimport shutil\nimport sys\nimport time\n\nTMP = sys.argv[1]\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nfor f in (\"l.db\", \"rules.json\"):\n    if os.path.exists(os.path.join(TMP, f)):\n        os.remove(os.path.join(TMP, f))\nshutil.rmtree(os.path.join(TMP, \"manuals\"), ignore_errors=True)\nshutil.copytree(os.path.join(ROOT, \"app\", \"engine\", \"manuals\"), os.path.join(TMP, \"manuals\"))\nos.environ.update(DB_PATH=os.path.join(TMP, \"l.db\"), RULES_PATH=os.path.join(TMP, \"rules.json\"), MANUALS_DIR=os.path.join(TMP, \"manuals\"))\nos.environ.pop(\"GOOGLE_CLIENT_ID\", None)\nsys.path.insert(0, ROOT)\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.main import app  # noqa: E402\nfrom app import store  # noqa: E402\nfrom app.engine.pipeline import run_pipeline  # noqa: E402\n\nc = TestClient(app)\nRES = []\n\n\ndef check(sec, name, ok, detail=\"\"):\n    RES.append((sec, name, \"PASS\" if ok else \"FAIL\", str(detail)[:300]))\n    print(\"[%s] %s %s :: %s\" % (\"PASS\" if ok else \"FAIL\", sec, name, str(detail)[:300]))\n\n\ndef text(html):\n    html = re.sub(r\"<script.*?</script>\", \" \", html, flags=re.S)\n    return re.sub(r\"\\s+\", \" \", re.sub(r\"<[^>]+>\", \" \", html)).replace(\"&amp;\", \"&\").replace(\"&#39;\", \"'\")\n\n\n# ------------------------------------------------------------------ C. consistency\nm = run_pipeline()[\"metrics\"]\nmoney = lambda v: \"$\" + format(v, \",.0f\")\nneed = {\"overdue\": money(m[\"overdue_balance\"]), \"received\": money(m[\"overdue_already_paid\"]), \"disputed\": money(m[\"overdue_disputed\"]),\n        \"collectable\": money(m[\"overdue_collectable\"])}\ncounts = {\"drafts\": m[\"drafts\"], \"held\": m[\"held\"], \"card\": m[\"card_retries\"], \"human\": m[\"human_writes\"]}\nprint(\"engine metrics:\", need, counts)\npages = {\"home\": \"/\", \"today\": \"/today\", \"digest\": \"/digest\", \"team\": \"/team\"}\nT = {k: text(c.get(v).text) for k, v in pages.items()}\nr = c.post(\"/api/chat\", json={\"message\": \"status\"})\nT[\"chat status\"] = r.json()[\"reply\"] + \" \" + \" \".join(\" \".join(x.get(\"lines\") or []) for x in r.json().get(\"cards\", []))\nfor k, t in T.items():\n    missing = [n + \"=\" + v for n, v in need.items() if v not in t and k not in (\"team\",)]\n    check(\"C\", \"money figures on %s\" % k, not missing, \"missing \" + \", \".join(missing) if missing else \"all 4 present\")\ncoll = c.get(\"/collections\").text\ngroups = dict((a, int(n)) for a, n in re.findall(r'href=\"#g-([A-Z_]+)\">[^(]*\\((\\d+)\\)', coll))\ncheck(\"C\", \"/collections group counts = engine\", groups.get(\"HOLD\") == counts[\"held\"] and groups.get(\"DRAFT_REMINDER\") == counts[\"drafts\"]\n      and groups.get(\"RETRY_CARD\") == counts[\"card\"] and groups.get(\"HUMAN_WRITES\") == counts[\"human\"], groups)\ndg = T[\"digest\"]\ncheck(\"C\", \"digest counts = engine\", (\"drafted for your approval: %d\" % counts[\"drafts\"]) in dg and (\"Card re-runs to approve: %d\" % counts[\"card\"]) in dg\n      and (\"Held (not chased): %d\" % counts[\"held\"]) in dg and (\"write personally: %d\" % counts[\"human\"]) in dg, \"\")\ncs = T[\"chat status\"]\ncheck(\"C\", \"chat status counts = engine\", all(str(v) in cs for v in counts.values()), cs[:300])\nfor k in (\"home\", \"today\"):\n    t = T[k]\n    nh = re.search(r\"(?:Needs a human today|Needs you today) \\((\\d+)\", t)\n    check(\"C\", \"needs-a-human count on %s\" % k, nh is not None and int(nh.group(1)) == counts[\"held\"] + counts[\"drafts\"] + counts[\"card\"] + counts[\"human\"] + m[\"needs_review\"],\n          nh.group(0) if nh else \"not found\")\nstale = [\"$83,448\", \"$312,264\", \"$237,533\", \"$83k\", \"$238k\", \"22 wrong chases\", \"27 reminders\", \"11 that need a person\"]\nfor k, path in list(pages.items()) + [(\"about\", \"/about\"), (\"docs\", \"/docs\"), (\"architecture\", \"/architecture\"), (\"demo\", \"/demo\")]:\n    t = text(c.get(path).text)\n    hit = [s for s in stale if s in t]\n    check(\"C\", \"no stale numbers on %s\" % k, not hit, hit)\n\n# ------------------------------------------------------------------ D. human-action flows\ndef status(r):\n    return r.status_code\n\n\nH = {\"HX-Request\": \"true\"}\nn0 = len(store.all_actions())\ncheck(\"D\", \"approve payment proposal PAY-65750\", status(c.post(\"/cash/PAY-65750/approve\", data={\"note\": \"QA: confirmed Jessop wire\"}, headers=H)) == 200)\ncheck(\"D\", \"undo auto-apply PAY-65806\", status(c.post(\"/cash/PAY-65806/undo\", data={\"note\": \"QA: undo test\"}, headers=H)) == 200)\nst_ = run_pipeline()\ninv = {i[\"invoice_id\"]: i for i in st_[\"invoices\"]}\nd = inv[\"INV-25862\"][\"draft\"]\nr = c.post(\"/collections/INV-25862/send\", data={\"subject\": d[\"subject\"], \"body\": d[\"body\"] + \"\\n\\nP.S. QA edit\", \"note\": \"QA: approve with edit\"}, headers=H)\nacts = [a for a in store.all_actions() if a[\"object_id\"] == \"INV-25862\"]\ncheck(\"D\", \"approve draft with an edit -> 'edit' + 'send' rows\", status(r) == 200 and [a[\"action\"] for a in acts] == [\"edit\", \"send\"], [a[\"action\"] for a in acts])\nr = c.post(\"/collections/INV-25869/send\", data={\"subject\": \"x\", \"body\": \"We will pass this to a debt collector.\"}, headers=H)\ncheck(\"D\", \"send with banned wording -> 400\", status(r) == 400, r.text[:120])\nd2 = inv[\"INV-25848\"][\"draft\"]\nr = c.post(\"/collections/INV-25848/send\", data={\"subject\": 
… [tool input truncated]
```

### Tool · 2026-11-20 18:14:22 UTC
**Tool result:**
```
engine metrics: {'overdue': '$633,245', 'received': '$78,348', 'disputed': '$312,922', 'collectable': '$241,975'} {'drafts': 20, 'held': 21, 'card': 9, 'human': 3}
[PASS] C money figures on home :: all 4 present
[PASS] C money figures on today :: all 4 present
[PASS] C money figures on digest :: all 4 present
[PASS] C money figures on team :: all 4 present
[PASS] C money figures on chat status :: all 4 present
[PASS] C /collections group counts = engine :: {'HOLD': 21, 'RETRY_CARD': 9, 'HUMAN_WRITES': 3, 'DRAFT_REMINDER': 20, 'NO_ACTION': 64}
[PASS] C digest counts = engine :: 
[PASS] C chat status counts = engine :: Overdue $633,245 across 54 invoices: $78,348 already received, $312,922 disputed, $241,975 collectable. Complaints caused: 0. Cash Application: 3 auto-applied (exact amount + reference), 4 proposals for Priya, $87,335 found in unapplied receipts. Account Context: profiled 107 customers; 16 with an o
[PASS] C needs-a-human count on home :: Needs a human today (57
[PASS] C needs-a-human count on today :: Needs you today (57
[PASS] C no stale numbers on home :: []
[PASS] C no stale numbers on today :: []
[PASS] C no stale numbers on digest :: []
[PASS] C no stale numbers on team :: []
[PASS] C no stale numbers on about :: []
[PASS] C no stale numbers on docs :: []
[PASS] C no stale numbers on architecture :: []
[PASS] C no stale numbers on demo :: []
[PASS] D approve payment proposal PAY-65750 :: 
[PASS] D undo auto-apply PAY-65806 :: 
[PASS] D approve draft with an edit -> 'edit' + 'send' rows :: ['edit', 'send']
[PASS] D send with banned wording -> 400 :: {"detail":"Blocked by the Controller: the email contains banned wording: debt collector"}
[FAIL] D send to an address NOT in contacts.csv (look-alike) -> rejected :: HTTP 200 (server accepted 'to' override)
[FAIL] D send on a HOLD invoice (Jessop MONEY_RECEIVED) without lifting the hold -> rejected :: HTTP 200
[PASS] D reject draft INV-25869 :: 
[PASS] D override hold with reason <5 chars -> 400 :: 
[PASS] D override hold with a reason -> OK :: 
[PASS] D release DISPUTE without AM checkbox -> 400 :: 
[PASS] D release DISPUTE with AM checkbox + name -> OK :: 
[FAIL] D OVERRIDE (not release) a DISPUTE hold without AM -> should also need AM :: HTTP 200: dispute hold lifted with no AM confirmation
[PASS] D approve card re-run INV-25803 :: 
[PASS] D reject card re-run INV-25793 :: 
[PASS] D card re-run on a non-re-run invoice -> 400 :: 
[PASS] D rules change via /rules form shows before/after :: au
… [result truncated, 3932 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cat > \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/eval_web.py\" <<'EOF'\n\"\"\"QA pass 2, sections C (consistency) and D (human-action flows) via FastAPI TestClient.\nUses a throw-away DB, rules file and manuals copy so ./ledgerline.db, ./rules.json and app/engine/manuals are untouched.\nUsage: eval_web.py <tmpdir>\"\"\"\nimport json\nimport os\nimport re\nimport shutil\nimport sys\nimport time\n\nTMP = sys.argv[1]\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nfor f in (\"l.db\", \"rules.json\"):\n    if os.path.exists(os.path.join(TMP, f)):\n        os.remove(os.path.join(TMP, f))\nshutil.rmtree(os.path.join(TMP, \"manuals\"), ignore_errors=True)\nshutil.copytree(os.path.join(ROOT, \"app\", \"engine\", \"manuals\"), os.path.join(TMP, \"manuals\"))\nos.environ.update(DB_PATH=os.path.join(TMP, \"l.db\"), RULES_PATH=os.path.join(TMP, \"rules.json\"), MANUALS_DIR=os.path.join(TMP, \"manuals\"))\nos.environ.pop(\"GOOGLE_CLIENT_ID\", None)\nsys.path.insert(0, ROOT)\nfrom fastapi.testclient import TestClient  # noqa: E402\nfrom app.main import app  # noqa: E402\nfrom app import store  # noqa: E402\nfrom app.engine.pipeline import run_pipeline  # noqa: E402\n\nc = TestClient(app)\nRES = []\n\n\ndef check(sec, name, ok, detail=\"\"):\n    RES.append((sec, name, \"PASS\" if ok else \"FAIL\", str(detail)[:300]))\n    print(\"[%s] %s %s :: %s\" % (\"PASS\" if ok else \"FAIL\", sec, name, str(detail)[:300]))\n\n\ndef text(html):\n    html = re.sub(r\"<script.*?</script>\", \" \", html, flags=re.S)\n    return re.sub(r\"\\s+\", \" \", re.sub(r\"<[^>]+>\", \" \", html)).replace(\"&amp;\", \"&\").replace(\"&#39;\", \"'\")\n\n\n# ------------------------------------------------------------------ C. consistency\nm = run_pipeline()[\"metrics\"]\nmoney = lambda v: \"$\" + format(v, \",.0f\")\nneed = {\"overdue\": money(m[\"overdue_balance\"]), \"received\": money(m[\"overdue_already_paid\"]), \"disputed\": money(m[\"overdue_disputed\"]),\n        \"collectable\": money(m[\"overdue_collectable\"])}\ncounts = {\"drafts\": m[\"drafts\"], \"held\": m[\"held\"], \"card\": m[\"card_retries\"], \"human\": m[\"human_writes\"]}\nprint(\"engine metrics:\", need, counts)\npages = {\"home\": \"/\", \"today\": \"/today\", \"digest\": \"/digest\", \"team\": \"/team\"}\nT = {k: text(c.get(v).text) for k, v in pages.items()}\nr = c.post(\"/api/chat\", json={\"message\": \"status\"})\nT[\"chat status\"] = r.json()[\"reply\"] + \" \" + \" \".join(\" \".join(x.get(\"lines\") or []) for x in r.json().get(\"cards\", []))\nfor k, t in T.items():\n    missing = [n + \"=\" + v for n, v in need.items() if v not in t and k not in (\"team\",)]\n    check(\"C\", \"money figures on %s\" % k, not missing, \"missing \" + \", \".join(missing) if missing else \"all 4 present\")\ncoll = c.get(\"/collections\").text\ngroups = dict((a, int(n)) for a, n in re.findall(r'href=\"#g-([A-Z_]+)\">[^(]*\\((\\d+)\\)', coll))\ncheck(\"C\", \"/collections group counts = engine\", groups.get(\"HOLD\") == counts[\"held\"] and groups.get(\"DRAFT_REMINDER\") == counts[\"drafts\"]\n      and groups.get(\"RETRY_CARD\") == counts[\"card\"] and groups.get(\"HUMAN_WRITES\") == counts[\"human\"], groups)\ndg = T[\"digest\"]\ncheck(\"C\", \"digest counts = engine\", (\"drafted for your approval: %d\" % counts[\"drafts\"]) in dg and (\"Card re-runs to approve: %d\" % counts[\"card\"]) in dg\n      and (\"Held (not chased): %d\" % counts[\"held\"]) in dg and (\"write personally: %d\" % counts[\"human\"]) in dg, \"\")\ncs = T[\"chat status\"]\ncheck(\"C\", \"chat status counts = engine\", all(str(v) in cs for v in counts.values()), cs[:300])\nfor k in (\"home\", \"today\"):\n    t = T[k]\n    nh = re.search(r\"(?:Needs a human today|Needs you today) \\((\\d+)\", t)\n    check(\"C\", \"needs-a-human count on %s\" % k, nh is not None and int(nh.group(1)) == counts[\"held\"] + counts[\"drafts\"] + counts[\"card\"] + counts[\"human\"] + m[\"needs_review\"],\n          nh.group(0) if nh else \"not found\")\nstale = [\"$83,448\", \"$312,264\", \"$237,533\", \"$83k\", \"$238k\", \"22 wrong chases\", \"27 reminders\", \"11 that need a person\"]\nfor k, path in list(pages.items()) + [(\"about\", \"/about\"), (\"docs\", \"/docs\"), (\"architecture\", \"/architecture\"), (\"demo\", \"/demo\")]:\n    t = text(c.get(path).text)\n    hit = [s for s in stale if s in t]\n    check(\"C\", \"no stale numbers on %s\" % k, not hit, hit)\n\n# ------------------------------------------------------------------ D. human-action flows\ndef status(r):\n    return r.status_code\n\n\nH = {\"HX-Request\": \"true\"}\nn0 = len(store.all_actions())\ncheck(\"D\", \"approve payment proposal PAY-65750\", status(c.post(\"/cash/PAY-65750/approve\", data={\"note\": \"QA: confirmed Jessop wire\"}, headers=H)) == 200)\ncheck(\"D\", \"undo auto-apply PAY-65806\", status(c.post(\"/cash/PAY-65806/undo\", data={\"note\": \"QA: undo test\"}, headers=H)) == 200)\nst_ = run_pipeline()\ninv = {i[\"invoice_id\"]: i for i in st_[\"invoices\"]}\nd = inv[\"INV-25862\"][\"draft\"]\nr = c.post(\"/collections/INV-25862/send\", data={\"subject\": d[\"subject\"], \"body\": d[\"body\"] + \"\\n\\nP.S. QA edit\", \"note\": \"QA: approve with edit\"}, headers=H)\nacts = [a for a in store.all_actions() if a[\"object_id\"] == \"INV-25862\"]\ncheck(\"D\", \"approve draft with an edit -> 'edit' + 'send' rows\", status(r) == 200 and [a[\"action\"] for a in acts] == [\"edit\", \"send\"], [a[\"action\"] for a in acts])\nr = c.post(\"/collections/INV-25869/send\", data={\"subject\": \"x\", \"body\": \"We will pass this to a debt collector.\"}, headers=H)\ncheck(\"D\", \"send with banned wording -> 400\", status(r) == 400, r.text[:120])\nd2 = inv[\"INV-25848\"][\"draft\"]\nr = c.post(\"/collections/INV-25848/send\", data={\"subject\": 
… [tool input truncated]
```

### Claude · 2026-11-20 18:14:31 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"send\\|name=\\\"to\\\"\\|override_hold\\|release_hold\\|am_confirmed\" app/web/templates/_invoice.html | head -20",
 "description": "Check invoice template send and hold forms"
}
```

### Tool · 2026-11-20 18:14:31 UTC
**Tool result:**
```
4:{% set lifted = s and s.action in ('override_hold', 'release_hold') %}
5:{% set closed = s and s.action in ('send', 'reject') %}
44:              <label><input type="checkbox" name="am_confirmed"> Account manager confirmed the dispute is settled</label>
50:            <button class="btn btn-secondary" name="kind" value="release_hold">Release hold</button>
51:            <button class="btn btn-danger" name="kind" value="override_hold">Override hold</button>
60:            <form method="post" action="/collections/{{ i.invoice_id }}/send" hx-post="/collections/{{ i.invoice_id }}/send" hx-target="closest details" hx-swap="outerHTML" class="draft">
61:              <label class="small">To <input name="to" class="input" value="{{ (d.to or [])|join(', ') }}"></label>
65:                <button class="btn btn-primary">Approve &amp; send (simulated)</button>
73:          {% elif s.action == 'send' and s.payload %}
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"send\\|name=\\\"to\\\"\\|override_hold\\|release_hold\\|am_confirmed\" app/web/templates/_invoice.html | head -20",
 "description": "Check invoice template send and hold forms"
}
```

### Claude · 2026-11-20 18:14:39 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && H=/private/tmp/claude-501/qa2/html; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' ' | sed 's/.*Run agents//'; }; for f in docs demo architecture; do echo \"=== $f\"; strip $H/$f.html | cut -c1-2200; echo; done",
 "description": "Dump docs, demo, architecture text"
}
```

### Tool · 2026-11-20 18:14:39 UTC
**Tool result:**
```
=== docs
 Documentation Who does what, where The whole system on one diagram: the company and its people, the AI finance team that runs on Render, and how it was built in 24 hours. Then the four hand-ins and where to find the evidence. System diagram LEDGERLINE · THE COMPANY PEOPLE Maya Lindqvist COO · sponsor approves go-live Legal DPA for AI gates the AI layer Dana Ruiz VP Finance thresholds · write-offs · plans Priya Nair AR Specialist runs the RIG · approves Account managers own disputes confirm before release SYSTEMS (READ-ONLY EXPORTS) QuickBooks invoices · AR aging Bank + Stripe receipts Zendesk tickets HubSpot customers · contacts Product usage export Slack Priya's digest THE AI FINANCE TEAM · ON RENDER · RULES-ONLY TODAY 1 Cash Application match receipts first 2 Account Context customer 360 · tickets 3 Controller hold · route · block 4 Collections stage · tone · draft Priya's queue approve · edit · reject Outputs (simulated) reminder emails · ledger application card re-run · dispute routing approved only Operating manuals humans edit Rules Priya / Dana edit Audit log every decision + action Claude via Amazon Bedrock OFF until Legal signs DPA Agents re-read manuals and rules every run. Every decision and human action lands in the audit log. read-only data Priya · Dana · AMs approve / release morning digest Legal DPA gate HOW IT WAS BUILT · THE 24-HOUR BUILD Jacek Materna AI Operator directs the build CLAUDE CODE BUILD AGENTS test-steward challenge · Maya · trail data-analyst evidence · discrepancies builder product + RIG qa-evaluator accuracy · red-team GitHub repo Render hosting deploys Scaleworks challenge Maya is played by Scaleworks AI “a person at Scaleworks reads everything” Maya channel · confirmation / intel only Who does what Actor Where Does Can't do / needs approval from Maya Lindqvist , COO Maya channel (Scaleworks chat) Sponsor. Sets guardrails, approves go-live, checks in a month whether Priya still uses it Doesn't operate the queue. We write to her only to get a confirmation or intel Dana Ruiz , VP Finance RIG: Rules, Decisions for Dana Owns thresholds (auto-apply limit, write-off threshold), write-offs up to $2,000, p

=== demo
 Demo video Walkthrough Coming soon Loom walkthrough coming — 5–10 min What we chose, why, how, the tool on real records, and where it gets things wrong. Paste Loom share link Loom share or embed links work. YouTube and Google Drive links are accepted too. Saving is logged in the audit trail. Save video link 
… [result truncated, 6579 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && H=/private/tmp/claude-501/qa2/html; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' ' | sed 's/.*Run agents//'; }; for f in docs demo architecture; do echo \"=== $f\"; strip $H/$f.html | cut -c1-2200; echo; done",
 "description": "Dump docs, demo, architecture text"
}
```

### Claude · 2026-11-20 18:14:48 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && DB_PATH=/private/tmp/claude-501/qa2/l.db RULES_PATH=/private/tmp/claude-501/qa2/rules.json MANUALS_DIR=/private/tmp/claude-501/qa2/manuals .venv/bin/python -c \"\nimport re,glob\nfrom fastapi.testclient import TestClient\nfrom app.main import app\nc=TestClient(app)\nlinks=set(); ext=set()\nfor f in glob.glob('/private/tmp/claude-501/qa2/html/*.html'):\n    for h in re.findall(r'href=\\\"([^\\\"#]+)',open(f).read()):\n        (ext if h.startswith('http') else links).add(h)\nbad=[]\nfor h in sorted(links):\n    if h.startswith('mailto') or h.endswith('.css'): continue\n    r=c.get(h,follow_redirects=True)\n    if r.status_code!=200: bad.append((h,r.status_code))\nprint('internal links',len(links),'broken',bad)\nprint('external',sorted(ext))\n\"",
 "description": "Check internal links for breakage"
}
```

### Tool · 2026-11-20 18:14:52 UTC
**Tool result:**
```
internal links 258 broken []
external ['http://testserver', 'http://testserver/collections', 'https://fonts.googleapis.com', 'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap', 'https://fonts.gstatic.com', 'https://github.com/jacekmaterna1/finance-team-4-maya']
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && DB_PATH=/private/tmp/claude-501/qa2/l.db RULES_PATH=/private/tmp/claude-501/qa2/rules.json MANUALS_DIR=/private/tmp/claude-501/qa2/manuals .venv/bin/python -c \"\nimport re,glob\nfrom fastapi.testclient import TestClient\nfrom app.main import app\nc=TestClient(app)\nlinks=set(); ext=set()\nfor f in glob.glob('/private/tmp/claude-501/qa2/html/*.html'):\n    for h in re.findall(r'href=\\\"([^\\\"#]+)',open(f).read()):\n        (ext if h.startswith('http') else links).add(h)\nbad=[]\nfor h in sorted(links):\n    if h.startswith('mailto') or h.endswith('.css'): continue\n    r=c.get(h,follow_redirects=True)\n    if r.status_code!=200: bad.append((h,r.status_code))\nprint('internal links',len(links),'broken',bad)\nprint('external',sorted(ext))\n\"",
 "description": "Check internal links for breakage"
}
```

### Claude · 2026-11-20 18:14:59 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && H=/private/tmp/claude-501/qa2/html; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' ' | sed 's/.*Run agents//'; }; for f in direct activity agents_cash buildlog; do echo \"=== $f\"; strip $H/$f.html | cut -c1-1300; echo; done; strip $H/docs.html | grep -oE \"(Transcript|transcript)[^.]{0,200}\" | head -5",
 "description": "Dump direct, activity, agent, buildlog text"
}
```

### Tool · 2026-11-20 18:14:59 UTC
**Tool result:**
```
=== direct
 Command Direct the team Agents re-read their manuals on every run. Only humans edit them (SpaceXSI pattern). An instruction starts as proposed ; when a person accepts it, it is appended to the agent's manual under "Standing instructions from humans". Thresholds live on the Rules page . (a) Give an instruction Cash Application Account Context Controller Collections Propose instruction You can also type it in Talk to the team: start with "from now on", "always", "never" or "instruction:". (b) Operating manuals Cash Application # Operating manual — Cash Application agent Owner: Priya Nair (AR Specialist); policy owner Dana Ruiz (VP Finance). Only humans edit this file. You match unapplied bank and card receipts to open invoices. You run FIRST on every cycle, before anyone is chased, so we never chase money we already have (the Paidly failure in 2025: a long-standing customer was chased for an invoice they had paid by wire, because the money took days to be matched). What you may do alone: - Apply a receipt ONLY when the amount AND the invoice reference both match exactly (Maya, T+0:05). That is what the team already does without thinking twice. What you must propose to a person (Priya or Dana): - Matches on payer name + amount without an invoice reference. - Several open invoices

=== activity
 Live feed Activity Agent decisions, human approvals, instructions and chat, newest first. Human rows come from the append-only store; agent rows from the latest run. All Cash Application Account Context Controller Collections Humans Search 141 shown Collections · agent · 2026-11-20T12:12:26.400 · confidence 80% invoice INV-26005 → DRAFT_REMINDER Hume Accounting $282, 15 days past due: Stage: card_failed Collections · agent · 2026-11-20T12:12:26.390 · confidence 80% invoice INV-25972 → NO_ACTION Reyes Strategy $329, 0 days past due: Next reminder at day 7 Collections · agent · 2026-11-20T12:12:26.380 · confidence 90% invoice INV-25470 → RETRY_CARD Hollis Nair Engineers $517, 141 days past due: Card works again (PAY-65739: card charge of $517.00 succeeded on 2026-10-12). Re-run the failed charge?; 90+ days overdue; Decision for Dana today: Automatic card write-off in 9 days Collections · agent · 2026-11-20T12:12:26.370 · confidence 90% invoice INV-25622 → RETRY_CARD Studio Nakamura $517, 105 days past due: Card works again (PAY-65765: card charge of $517.00 succeeded on 2026-10-18). Re-run the failed charge?; 90+ days overdue Collections · agent · 2026-11-20T
… [result truncated, 5294 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && H=/private/tmp/claude-501/qa2/html; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' ' | sed 's/.*Run agents//'; }; for f in direct activity agents_cash buildlog; do echo \"=== $f\"; strip $H/$f.html | cut -c1-1300; echo; done; strip $H/docs.html | grep -oE \"(Transcript|transcript)[^.]{0,200}\" | head -5",
 "description": "Dump direct, activity, agent, buildlog text"
}
```

### Claude · 2026-11-20 18:15:11 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat render.yaml; U=https://ledgerline-finance-rig.onrender.com; for p in /healthz / /today /collections /cash /team /maya /digest /audit /activity /rules /demo /docs /buildlog /customers; do curl -s -o /dev/null -w \"$p %{http_code} %{time_total}s\\n\" --max-time 90 $U$p; done",
 "description": "Check render config and live page timings"
}
```

### Tool · 2026-11-20 18:15:15 UTC
**Tool result:**
```
# Render blueprint: one web service. Secrets are sync:false (set them in the Render dashboard, never in the repo).
services:
  - type: web
    name: ledgerline-ar-operator
    runtime: python
    plan: starter   # the persistent disk below needs a paid instance; on the free plan remove `disk` (state is then ephemeral)
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips="*"
    healthCheckPath: /healthz
    autoDeploy: true
    disk:
      name: ledgerline-data
      mountPath: /var/data
      sizeGB: 1
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: ALLOWED_DOMAINS
        value: scaleworks.com
      - key: ALLOWED_EMAILS
        sync: false
      - key: GOOGLE_CLIENT_ID
        sync: false
      - key: GOOGLE_CLIENT_SECRET
        sync: false
      - key: SESSION_SECRET
        generateValue: true
      - key: BASE_URL
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: DB_PATH
        value: /var/data/ledgerline.db
      - key: RULES_PATH
        value: /var/data/rules.json
      - key: DEMO_VIDEO_URL
        sync: false
/healthz 200 0.288452s
/ 200 0.281173s
/today 200 0.172433s
/collections 200 0.401932s
/cash 200 0.149484s
/team 200 0.168965s
/maya 200 0.270479s
/digest 200 0.105967s
/audit 200 0.125698s
/activity 200 0.129916s
/rules 200 0.184021s
/demo 200 0.114091s
/docs 200 0.109092s
/buildlog 200 0.677380s
/customers 200 0.119796s
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat render.yaml; U=https://ledgerline-finance-rig.onrender.com; for p in /healthz / /today /collections /cash /team /maya /digest /audit /activity /rules /demo /docs /buildlog /customers; do curl -s -o /dev/null -w \"$p %{http_code} %{time_total}s\\n\" --max-time 90 $U$p; done",
 "description": "Check render config and live page timings"
}
```

### Claude · 2026-11-20 18:15:25 UTC
**Tool call:** `Bash`
```json
{
 "command": "U=https://ledgerline-finance-rig.onrender.com; S=/private/tmp/claude-501/qa2/live; mkdir -p $S; for p in / /today /rules /audit /maya /demo; do curl -s --max-time 60 \"$U$p\" > \"$S/$(echo $p | tr -d / | sed 's/^$/home/').html\"; done; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' '; }; strip $S/home.html | grep -oE \"Build T\\+[0-9:]+|Agents ran [^)]*\\)|Overdue balance[^C]{0,120}|Auth [a-z (]+\\)|DEV MODE[^.]{0,80}|fake[^.]{0,80}\" | head; strip $S/audit.html | grep -oE \"Human: [^ ]+\" | sort | uniq -c; strip $S/audit.html | grep -oE \"[0-9]+ (rows|shown|entries|actions)[^.]{0,40}\" | head -3; curl -s --max-time 60 \"$U/audit.csv\" | grep -c \"Human:\"; strip $S/maya.html | grep -oE \"Message budget [^W]{0,30}\"; strip $S/rules.html | grep -oE \"auto.apply[^.]{0,120}\" | head -3",
 "description": "Inspect live site state and version"
}
```

### Tool · 2026-11-20 18:15:27 UTC
**Tool result:**
```
Auth off (demo)
Build T+1:05
Agents ran 2026-11-20 18:01:15 (6.01s)
Overdue balance · headline metric $633,245 54 invoices on the ledger Already received $78,348 Disputed $312,922 
141 rows When Who Object Decision Conf
0
Message budget 5 of 60 used 
auto_apply_exact_ref_match on Write-off threshold ($) Small differences (e
auto_apply_max_amount Use Claude for drafts When on, Collections asks Claude to write the reminder text (cached)
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "U=https://ledgerline-finance-rig.onrender.com; S=/private/tmp/claude-501/qa2/live; mkdir -p $S; for p in / /today /rules /audit /maya /demo; do curl -s --max-time 60 \"$U$p\" > \"$S/$(echo $p | tr -d / | sed 's/^$/home/').html\"; done; strip(){ sed -e 's/<script.*<\\/script>//' -e 's/<[^>]*>/ /g' $1 | tr -s ' \\n\\t' ' '; }; strip $S/home.html | grep -oE \"Build T\\+[0-9:]+|Agents ran [^)]*\\)|Overdue balance[^C]{0,120}|Auth [a-z (]+\\)|DEV MODE[^.]{0,80}|fake[^.]{0,80}\" | head; strip $S/audit.html | grep -oE \"Human: [^ ]+\" | sort | uniq -c; strip $S/audit.html | grep -oE \"[0-9]+ (rows|shown|entries|actions)[^.]{0,40}\" | head -3; curl -s --max-time 60 \"$U/audit.csv\" | grep -c \"Human:\"; strip $S/maya.html | grep -oE \"Message budget [^W]{0,30}\"; strip $S/rules.html | grep -oE \"auto.apply[^.]{0,120}\" | head -3",
 "description": "Inspect live site state and version"
}
```

### Claude · 2026-11-20 18:15:37 UTC
**Tool call:** `Bash`
```json
{
 "command": "U=https://ledgerline-finance-rig.onrender.com; curl -s -o /dev/null -w \"override<5: %{http_code}\\n\" -X POST -d \"reason=ok&kind=override_hold\" $U/collections/INV-25897/hold; curl -s -o /dev/null -w \"release dispute no AM: %{http_code}\\n\" -X POST -d \"reason=QA live smoke&kind=release_hold\" $U/collections/INV-25787/hold; curl -s -X POST -H \"Content-Type: application/json\" -d '{\"message\":\"status\"}' $U/api/chat | head -c 400; echo; cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"^### Exchange\" trail/MAYA_QA.md; date",
 "description": "Live smoke checks on guard endpoints"
}
```

### Tool · 2026-11-20 18:15:38 UTC
**Tool result:**
```
override<5: 400
release dispute no AM: 400
{"agent":"team","reply":"Overdue $633,245 across 54 invoices: $78,348 already received, $312,922 disputed, $241,975 collectable. Complaints caused: 0.","cards":[{"title":"What each agent did this run","lines":["Cash Application: 3 auto-applied (exact amount + reference), 4 proposals for Priya, $87,335 found in unapplied receipts.","Account Context: profiled 107 customers; 16 with an open billing c
30:### Exchange 1 — 11:14 CST, T+0:04
50:### Exchange 2 — 11:26 CST, T+0:16
68:### Exchange 3 — ~11:28 CST, T+0:18
84:### Exchange 4 — ~11:42 CST, T+0:32
Fri Nov 20 12:15:37 CST 2026
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "U=https://ledgerline-finance-rig.onrender.com; curl -s -o /dev/null -w \"override<5: %{http_code}\\n\" -X POST -d \"reason=ok&kind=override_hold\" $U/collections/INV-25897/hold; curl -s -o /dev/null -w \"release dispute no AM: %{http_code}\\n\" -X POST -d \"reason=QA live smoke&kind=release_hold\" $U/collections/INV-25787/hold; curl -s -X POST -H \"Content-Type: application/json\" -d '{\"message\":\"status\"}' $U/api/chat | head -c 400; echo; cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"^### Exchange\" trail/MAYA_QA.md; date",
 "description": "Live smoke checks on guard endpoints"
}
```

### Claude · 2026-11-20 18:15:43 UTC
**Tool call:** `Bash`
```json
{
 "command": "S=/private/tmp/claude-501/qa2/live; sed -e 's/<[^>]*>/ /g' $S/maya.html | tr -s ' \\n\\t' ' ' | grep -oE \"Exchange [0-9] — [^ ]+ [^ ]+ [^ ]+|Pending drafts.{0,200}|Message budget.{0,140}\" | head; cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -n 167,235p app/web/rig_data.py | grep -n \"budget\\|count\\|sent\\|len(\" ",
 "description": "Compare live Maya tab exchanges"
}
```

### Tool · 2026-11-20 18:15:43 UTC
**Tool result:**
```
Message budget 5 of 60 used We only write to Maya to get a confirmation or intel — never status updates. Exchange 1 — 11:14 CST, T+0:04 Maya opened the ch
Exchange 2 — 11:26 CST, T+0:16
Exchange 3 — ~11:28 CST, T+0:18
Exchange 4 — ~11:42 CST, T+0:32
Pending drafts (read-only; the operator sends them from the Scaleworks chat) Draft 6 — Dana&#39;s two decisions before Monday (READY, drafted 11:46, T+0:36) Confirmation Purpose: Confirmation (two decisions Dana ow
37:    # budget + pending drafts from the outbox
40:    out["used"], out["budget"] = (int(m.group(1)), int(m.group(2))) if m else (None, 60)
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "S=/private/tmp/claude-501/qa2/live; sed -e 's/<[^>]*>/ /g' $S/maya.html | tr -s ' \\n\\t' ' ' | grep -oE \"Exchange [0-9] — [^ ]+ [^ ]+ [^ ]+|Pending drafts.{0,200}|Message budget.{0,140}\" | head; cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -n 167,235p app/web/rig_data.py | grep -n \"budget\\|count\\|sent\\|len(\" ",
 "description": "Compare live Maya tab exchanges"
}
```

### Claude · 2026-11-20 18:15:48 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -n 200,212p app/web/rig_data.py; grep -n \"[0-9]\\+ of 60\\|Budget\\|budget\" trail/MAYA_OUTBOX.md trail/MAYA_QA.md | head",
 "description": "Find source of Maya budget count"
}
```

### Tool · 2026-11-20 18:15:48 UTC
**Tool result:**
```
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
trail/MAYA_QA.md:3:Messages used: **5 of 60** (target: 12 or fewer). The count of 5 comes from the main thread at 11:42. Only 4 messages from Jacek are logged below, so one message is unaccounted for. Check it against the counter on the challenge page.
trail/MAYA_QA.md:28:Budget: Maya allows 60 messages. Bundle questions. Running count at the top of this file and in MAYA_OUTBOX.md.
trail/MAYA_OUTBOX.md:3:Messages used: 4 of 60 (verified on the challenge page at T+0:50: "56 messages left")
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -n 200,212p app/web/rig_data.py; grep -n \"[0-9]\\+ of 60\\|Budget\\|budget\" trail/MAYA_OUTBOX.md trail/MAYA_QA.md | head",
 "description": "Find source of Maya budget count"
}
```

### Claude · 2026-11-20 18:15:56 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2; sed -e 's/<[^>]*>/ /g' html/rules.html | tr -s ' \\n\\t' ' ' | grep -oE \".{80}auto_apply_max_amount.{120}\"; grep -c \"auto_apply_max_amount\" \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web/views.py\"",
 "description": "Check auto-apply cap label on rules page"
}
```

### Tool · 2026-11-20 18:15:56 UTC
**Tool result:**
```
es on its own. Larger ones go to Priya even on an exact match. Dana to confirm. auto_apply_max_amount Use Claude for drafts When on, Collections asks Claude to write the reminder text (cached). Off = policy templates only
1
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd /private/tmp/claude-501/qa2; sed -e 's/<[^>]*>/ /g' html/rules.html | tr -s ' \\n\\t' ' ' | grep -oE \".{80}auto_apply_max_amount.{120}\"; grep -c \"auto_apply_max_amount\" \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web/views.py\"",
 "description": "Check auto-apply cap label on rules page"
}
```

### Claude · 2026-11-20 18:16:13 UTC
**Tool call:** `Bash`
```json
{
 "command": "curl -s -o /dev/null -w \"github %{http_code}\\n\" https://github.com/jacekmaterna1/finance-team-4-maya; grep -o \"Dana decisions.\\{0,400\\}\" /private/tmp/claude-501/qa2/html/home.html | sed 's/<[^>]*>/ /g' | tr -s ' ' | cut -c1-200; cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; grep -n \"10,000\\|10000\\|cap\" app/engine/manuals/cash_application.md | head -3; grep -n \"A person writes\" app/web/views.py",
 "description": "Check GitHub link, Dana tile, manual cap mention"
}
```

### Tool · 2026-11-20 18:16:14 UTC
**Tool result:**
```
github 404
Dana decisions, Legal reviews Bedrock note 
Dana decisions 3 Eastman Engineering $3,264 · Northgate Creative $799 
32:    "HUMAN_WRITES": "A person writes these (top-50 accounts)",
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "curl -s -o /dev/null -w \"github %{http_code}\\n\" https://github.com/jacekmaterna1/finance-team-4-maya; grep -o \"Dana decisions.\\{0,400\\}\" /private/tmp/claude-501/qa2/html/home.html | sed 's/<[^>]*>/ /g' | tr -s ' ' | cut -c1-200; cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; grep -n \"10,000\\|10000\\|cap\" app/engine/manuals/cash_application.md | head -3; grep -n \"A person writes\" app/web/views.py",
 "description": "Check GitHub link, Dana tile, manual cap mention"
}
```

### Claude · 2026-11-20 18:17:23 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/QA_PASS_2.md",
 "content": "# QA pass 2: FIN-1 / FIN-2 / RIG readiness\n\nQA Evaluator. Run on 2026-11-20 at 12:10–12:20 CST against the code as it stood then.\n\n- **Local tests** used a throw-away `DB_PATH`, `RULES_PATH` and `MANUALS_DIR` in a temp dir, so `./ledgerline.db`,\n  `./rules.json` and `app/engine/manuals/` were not touched.\n- **Live smoke checks** (https://ledgerline-finance-rig.onrender.com) were read-only, plus two requests that were\n  meant to be rejected, plus one chat \"status\".\n- Nothing in `app/` or `data/` was edited. Maya was not contacted.\n\n| script | section |\n|---|---|\n| `analysis/scripts/eval_cash_app.py`, `eval_guardrails.py` | A |\n| `analysis/scripts/eval_policy.py` → `analysis/work/eval_policy_results.csv` | B |\n| `analysis/scripts/eval_web.py <tmpdir>` → `analysis/work/eval_web_results.csv` | C, D |\n| `eval_controller.py` | dispute and ticket-read numbers in EVAL.md |\n\n## Summary\n\n| section | result |\n|---|---|\n| A. FIN-2 regression | **PASS 5/5** (auto-apply precision 100%; shortened-name replays held; guardrail red-team 54/54) |\n| B. FIN-1 policy compliance | **PASS 11 / FAIL 1.** The courtesy stage never fires: 16 invoices ($219,071) due in the next 1–5 days get no courtesy note |\n| C. Consistency across screens | **PASS 18/18** |\n| D. Human-action flows | **PASS 22 / FAIL 5.** Hold bypasses and a destructive partial rules POST |\n| E. RIG readiness for Maya | **Renders correctly, with 11 rough edges.** Two would mislead Maya or a reviewer |\n| F. Robustness | **FAIL on durability.** Live state is ephemeral and is wiped at every deploy or idle spin-down. Speed is fine: every page is under 2 s |\n\n**Verdict: FIN-2 is at 100% on the evidence. FIN-1's decisions are policy-correct, apart from the missing courtesy\nstage. The approval UI has 3 server-side guardrail bypasses (D2, D3, D4) that must be closed before Maya or Priya\nuses the RIG.**\n\n---\n\n## A. FIN-2 regression\n\n| check | result | evidence |\n|---|---|---|\n| A1 Auto-apply precision on the 246 real test receipts | **PASS** | 59/59 correct (100%). 0 wrong auto-applies across 286 rows; 0 synthetic receipts auto-applied |\n| A2 Effect of the $10k cap (`auto_apply_max_amount`) | **PASS** (as designed) | Real auto-applies drop from 81 to 59. **22 exact-reference receipts over $10k become proposals at 0.95; all 22 are proposed correctly.** Proposal top-1 is 98.3% (172/175). The live book is unchanged: 3 auto-applies, all ≤ $3,672. Cost: Priya's \"easy\" queue grows from 2 to 24 of 63 easy receipts |\n| A3 BRANDT / JESSOP / KINGSWAY shortened-name replays: no chase | **PASS** | INV-25806, INV-25784 and INV-25469 are all HOLD / MONEY_RECEIVED (\"Possible payment from an unidentified payer\"). The cash agent no longer assigns a wrong customer (JESSOP previously became Jessop Legal; it is now `None`) |\n| A4 Unidentified payer holds same-amount invoices | **PASS** | `controller.py:36-43`. Also confirmed: PEMBERTON is no longer tagged to the wrong customer (C1235) |\n| A5 Guardrail red-team (`eval_guardrails.py`) | **PASS 54/54** | The previous 10 failures are fixed: refusal wording in any category, banned list extended. One check was updated to expect LEGAL_RISK to block a card re-run |\n\n## B. FIN-1 policy compliance (every one of the 117 invoices in `run_pipeline()`)\n\n| check | result | evidence |\n|---|---|---|\n| B1 Stage vs real days past due (-5/+7/+21/+45/+90) | **FAIL** | 61 of 117 invoices are staged `wait` instead of `not_due` or `courtesy`. **16 invoices / $219,071 are due within 5 days and get no courtesy note** (for example INV-25933 Whitlock, due 11-01). For not-yet-due invoices the reason says \"Next reminder at day 7\". Cause: `pipeline.py:74` uses `ar_aging.days_past_due`, which the export floors at 0 (FACTS §1), so `stage_for()` (`collections.py:31-32`) never sees a negative value. Fix: `dpd = (AS_OF - pd.Timestamp(r[\"due_date\"])).days`. Keep `max(dpd, 0)` for display. All 56 past-due invoices are staged correctly |\n| B2 Top-50 never DRAFT_REMINDER | PASS | 14 top-50 invoices: HOLD / HUMAN_WRITES / NO_ACTION (not due) |\n| B3 No draft where PAID / MONEY_RECEIVED / DISPUTE / CANCELLATION / LEGAL_RISK / OPEN_ESCALATION | PASS | 0 of 117 |\n| B4 Drafts contain no banned phrase | PASS | 21 drafts (20 DRAFT_REMINDER + 1 HUMAN_WRITES). Also: the new substring \"court\" causes no false block today (no draft says \"courtesy\" or \"courteous\"). That is fragile, see E/defect S3-4 |\n| B5 Recipients are verified (in contacts.csv for that customer, domain match, billing or admin role) | PASS | 21/21 |\n| B6 Never a \"left the firm\" contact | PASS | 0 |\n| B7 AM cc'd | PASS | 21/21 |\n| B8 Invoice id, amount and due date in the body match the ledger | PASS | 21/21, cross-checked against invoices.csv |\n| B9 Signed off by Priya | PASS | 21/21 |\n| B10 Card re-runs only where a later card charge succeeded and there is no hard hold or legal risk | PASS | 9 re-runs. Drummond (chargeback, T880019) is now HUMAN_WRITES with LEGAL_RISK, not a re-run |\n| B11 Dana decisions = card invoices ≤10 days from the 150-day write-off, or > $2,000 | PASS | Exactly 3: Eastman Engineering $3,264 (>$2k), Northgate $799 (1 day), Hollis Nair $517 (9 days) |\n\n## C. Consistency (Home, /today, /collections, /digest, chat \"status\", Team, `run_pipeline()`)\n\n**PASS 18/18.**\n\n- The four money figures match on every screen: overdue $633,245, already received $78,348, disputed $312,922,\n  collectable $241,975.\n- The counts match on every screen: drafts 20, held 21, card re-runs 9, person writes 3, proposals 4.\n- Needs-a-human is 57 on both Home and /today (21+20+9+3+4).\n- /collections groups show 21 / 9 / 3 / 20 / 64.\n- No stale figure ($83,448, $312,264, $237,533, \"$238k\", \"22 wrong chase
… [tool input truncated]
```

### Tool · 2026-11-20 18:17:23 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/QA_PASS_2.md (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/QA_PASS_2.md",
 "content": "# QA pass 2: FIN-1 / FIN-2 / RIG readiness\n\nQA Evaluator. Run on 2026-11-20 at 12:10–12:20 CST against the code as it stood then.\n\n- **Local tests** used a throw-away `DB_PATH`, `RULES_PATH` and `MANUALS_DIR` in a temp dir, so `./ledgerline.db`,\n  `./rules.json` and `app/engine/manuals/` were not touched.\n- **Live smoke checks** (https://ledgerline-finance-rig.onrender.com) were read-only, plus two requests that were\n  meant to be rejected, plus one chat \"status\".\n- Nothing in `app/` or `data/` was edited. Maya was not contacted.\n\n| script | section |\n|---|---|\n| `analysis/scripts/eval_cash_app.py`, `eval_guardrails.py` | A |\n| `analysis/scripts/eval_policy.py` → `analysis/work/eval_policy_results.csv` | B |\n| `analysis/scripts/eval_web.py <tmpdir>` → `analysis/work/eval_web_results.csv` | C, D |\n| `eval_controller.py` | dispute and ticket-read numbers in EVAL.md |\n\n## Summary\n\n| section | result |\n|---|---|\n| A. FIN-2 regression | **PASS 5/5** (auto-apply precision 100%; shortened-name replays held; guardrail red-team 54/54) |\n| B. FIN-1 policy compliance | **PASS 11 / FAIL 1.** The courtesy stage never fires: 16 invoices ($219,071) due in the next 1–5 days get no courtesy note |\n| C. Consistency across screens | **PASS 18/18** |\n| D. Human-action flows | **PASS 22 / FAIL 5.** Hold bypasses and a destructive partial rules POST |\n| E. RIG readiness for Maya | **Renders correctly, with 11 rough edges.** Two would mislead Maya or a reviewer |\n| F. Robustness | **FAIL on durability.** Live state is ephemeral and is wiped at every deploy or idle spin-down. Speed is fine: every page is under 2 s |\n\n**Verdict: FIN-2 is at 100% on the evidence. FIN-1's decisions are policy-correct, apart from the missing courtesy\nstage. The approval UI has 3 server-side guardrail bypasses (D2, D3, D4) that must be closed before Maya or Priya\nuses the RIG.**\n\n---\n\n## A. FIN-2 regression\n\n| check | result | evidence |\n|---|---|---|\n| A1 Auto-apply precision on the 246 real test receipts | **PASS** | 59/59 correct (100%). 0 wrong auto-applies across 286 rows; 0 synthetic receipts auto-applied |\n| A2 Effect of the $10k cap (`auto_apply_max_amount`) | **PASS** (as designed) | Real auto-applies drop from 81 to 59. **22 exact-reference receipts over $10k become proposals at 0.95; all 22 are proposed correctly.** Proposal top-1 is 98.3% (172/175). The live book is unchanged: 3 auto-applies, all ≤ $3,672. Cost: Priya's \"easy\" queue grows from 2 to 24 of 63 easy receipts |\n| A3 BRANDT / JESSOP / KINGSWAY shortened-name replays: no chase | **PASS** | INV-25806, INV-25784 and INV-25469 are all HOLD / MONEY_RECEIVED (\"Possible payment from an unidentified payer\"). The cash agent no longer assigns a wrong customer (JESSOP previously became Jessop Legal; it is now `None`) |\n| A4 Unidentified payer holds same-amount invoices | **PASS** | `controller.py:36-43`. Also confirmed: PEMBERTON is no longer tagged to the wrong customer (C1235) |\n| A5 Guardrail red-team (`eval_guardrails.py`) | **PASS 54/54** | The previous 10 failures are fixed: refusal wording in any category, banned list extended. One check was updated to expect LEGAL_RISK to block a card re-run |\n\n## B. FIN-1 policy compliance (every one of the 117 invoices in `run_pipeline()`)\n\n| check | result | evidence |\n|---|---|---|\n| B1 Stage vs real days past due (-5/+7/+21/+45/+90) | **FAIL** | 61 of 117 invoices are staged `wait` instead of `not_due` or `courtesy`. **16 invoices / $219,071 are due within 5 days and get no courtesy note** (for example INV-25933 Whitlock, due 11-01). For not-yet-due invoices the reason says \"Next reminder at day 7\". Cause: `pipeline.py:74` uses `ar_aging.days_past_due`, which the export floors at 0 (FACTS §1), so `stage_for()` (`collections.py:31-32`) never sees a negative value. Fix: `dpd = (AS_OF - pd.Timestamp(r[\"due_date\"])).days`. Keep `max(dpd, 0)` for display. All 56 past-due invoices are staged correctly |\n| B2 Top-50 never DRAFT_REMINDER | PASS | 14 top-50 invoices: HOLD / HUMAN_WRITES / NO_ACTION (not due) |\n| B3 No draft where PAID / MONEY_RECEIVED / DISPUTE / CANCELLATION / LEGAL_RISK / OPEN_ESCALATION | PASS | 0 of 117 |\n| B4 Drafts contain no banned phrase | PASS | 21 drafts (20 DRAFT_REMINDER + 1 HUMAN_WRITES). Also: the new substring \"court\" causes no false block today (no draft says \"courtesy\" or \"courteous\"). That is fragile, see E/defect S3-4 |\n| B5 Recipients are verified (in contacts.csv for that customer, domain match, billing or admin role) | PASS | 21/21 |\n| B6 Never a \"left the firm\" contact | PASS | 0 |\n| B7 AM cc'd | PASS | 21/21 |\n| B8 Invoice id, amount and due date in the body match the ledger | PASS | 21/21, cross-checked against invoices.csv |\n| B9 Signed off by Priya | PASS | 21/21 |\n| B10 Card re-runs only where a later card charge succeeded and there is no hard hold or legal risk | PASS | 9 re-runs. Drummond (chargeback, T880019) is now HUMAN_WRITES with LEGAL_RISK, not a re-run |\n| B11 Dana decisions = card invoices ≤10 days from the 150-day write-off, or > $2,000 | PASS | Exactly 3: Eastman Engineering $3,264 (>$2k), Northgate $799 (1 day), Hollis Nair $517 (9 days) |\n\n## C. Consistency (Home, /today, /collections, /digest, chat \"status\", Team, `run_pipeline()`)\n\n**PASS 18/18.**\n\n- The four money figures match on every screen: overdue $633,245, already received $78,348, disputed $312,922,\n  collectable $241,975.\n- The counts match on every screen: drafts 20, held 21, card re-runs 9, person writes 3, proposals 4.\n- Needs-a-human is 57 on both Home and /today (21+20+9+3+4).\n- /collections groups show 21 / 9 / 3 / 20 / 64.\n- No stale figure ($83,448, $312,264, $237,533, \"$238k\", \"22 wrong chase
… [tool input truncated]
```

### Claude · 2026-11-20 18:17:35 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep \"not flagged\" analysis/work/eval_controller.log; .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_reads.csv').set_index('ticket_id')\nfor k in ['T880966','T880624','T880625','T880373','T880132','T880915','T880311','T880771','T880142']: print(k,t.loc[k,'about'],t.loc[k,'kind'])\n\"; grep -c . analysis/work/eval_guardrails_results.csv",
 "description": "Confirm ticket read status for cited cases"
}
```

### Tool · 2026-11-20 18:17:36 UTC
**Tool result:**
```
not flagged but money words: 498 of 1020
T880966 False product_question
T880624 False product_question
T880625 False product_question
T880373 False collections_complaint
T880132 False product_question
T880915 False product_question
T880311 True legal_threat
T880771 True legal_threat
T880142 True dispute
55
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep \"not flagged\" analysis/work/eval_controller.log; .venv/bin/python -c \"\nimport pandas as pd\nt=pd.read_csv('analysis/work/eval_ticket_reads.csv').set_index('ticket_id')\nfor k in ['T880966','T880624','T880625','T880373','T880132','T880915','T880311','T880771','T880142']: print(k,t.loc[k,'about'],t.loc[k,'kind'])\n\"; grep -c . analysis/work/eval_guardrails_results.csv",
 "description": "Confirm ticket read status for cited cases"
}
```

### Claude · 2026-11-20 18:17:38 UTC
Now I'll rewrite EVAL.md with current numbers.

### Claude · 2026-11-20 18:18:19 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/EVAL.md",
 "content": "# EVAL: how well the agents work on the real records\n\nQA Evaluator. **Updated 2026-11-20 at 12:20 CST (QA pass 2)** against the current code. That code includes:\n- the severity-1 fix for unidentified payers;\n- a stricter fuzzy match;\n- strong refusals read in any ticket category;\n- the Reyes fix;\n- a $10k auto-apply cap;\n- top-50 not-due → NO_ACTION;\n- card re-runs blocked on legal threats.\n\nThe first pass (11:36) is superseded. Its numbers appear below only as \"was\". Nothing in `app/` or `data/` was\nchanged. Data as of 2026-10-31.\n\n| script | what it does | output |\n|---|---|---|\n| `analysis/scripts/eval_cash_app.py` | replays 286 test payments against the invoice book as it stood on each received date | `analysis/work/eval_cash_app_results.csv`, `.log` |\n| `analysis/scripts/eval_controller.py` | dispute detection vs the analyst's list; reads all 1,041 tickets | `analysis/work/eval_ticket_reads.csv`, `.log` |\n| `analysis/scripts/eval_guardrails.py` | red-team on changed copies of the data held in memory | `analysis/work/eval_guardrails_results.csv`, `.log` |\n| `analysis/scripts/eval_policy.py` | FIN-1 policy check on every invoice | `analysis/work/eval_policy_results.csv`, `.log` |\n| `analysis/scripts/eval_web.py <tmpdir>` | screen consistency and human-action flows via TestClient | `analysis/work/eval_web_results.csv`, `.log` |\n\n**Headline**\n- **Cash application:** 0 wrong automatic applications (59 of 59 correct on real data). Proposals put the right\n  invoice first 98.3% of the time.\n- **Dispute detection:** recall 100% on the analyst's 14 disputes.\n- **Guardrail red-team: 54 of 54 pass** (was 44 of 54).\n- **FIN-1 policy check: 11 of 12 pass.** The courtesy note 5 days before the due date never fires.\n- **Approval UI: 22 of 27 flows pass.** Three server-side bypasses remain. See `analysis/QA_PASS_2.md`.\n\n---\n\n## 1. Cash Application (`analysis/testset_cash_app.csv`, 286 rows)\n\n**Harness.** For each payment, the invoice book is rebuilt as of the receipt date. An invoice is open if\n`issue_date <= received_date` and (`paid_date` is blank or `paid_date >= received_date`). The production\n`cash_app.run()` is called unchanged with DEFAULT_RULES. An answer is correct when the proposed invoice set equals the\nlabel. For PAY-65805 (Kingsway), which is ambiguous, either invoice is accepted.\n\n### Real rows (246)\n| difficulty | n | auto-applied | auto precision | proposed | proposal top-1 | exception | end-to-end correct |\n|---|---|---|---|---|---|---|---|\n| trivial (card) | 20 | 20 | 100% | 0 | n/a | 0 | 100% |\n| easy (memo ref) | 63 | 39 | 100% | 24 | 100% | 0 | 100% |\n| medium (no ref, unique amount) | 83 | 0 | n/a | 83 | 100% | 0 | 100% |\n| hard (same-amount ties / truncated payer) | 80 | 0 | n/a | 68 | 95.6% | 12 | 81.2% |\n| **all real** | **246** | **59** | **100% (59/59)** | **175** | **98.3% (172/175)** | **12 (4.9%)** | **93.9%** |\n\n- **No wrong auto-apply, so no severity-1.**\n- **What the $10k cap changed.** Real auto-applies went from 81 to 59.\n  - The 22 exact-reference receipts over $10,000 are now proposals at confidence 0.95, and all 22 are correct.\n  - Nothing became wrong. Priya simply confirms 22 more items, each a one-click confirmation.\n  - The live book is unaffected: its 3 auto-applies are $564, $987 and $3,672.\n- **3 wrong proposals (unchanged):** PAY-61158, PAY-61365 and PAY-65656.\n  - Each is a same-amount tie where staff applied a newer invoice than the oldest.\n  - The true invoice is always in \"alternatives\", and all tied invoices are held.\n- **12 exceptions, all truncated payer names** (`TAN`, `OYELARAN` x2, `ROSALES` x2, `HUME`, `ASHBY`, `CRANE`,\n  `LINDQVIST`, `CALLOWAY`, `KESSLER`, `PEMBERTON`).\n  - **None is now assigned to a wrong customer.** Before the fix, PEMBERTON went to C1235.\n  - The Controller now holds any open invoice with the same amount (`controller.py:36-43`).\n- Confidence calibration is unchanged:\n  - auto-apply is 0.99 and 100% correct;\n  - proposals at 0.82 to 0.95 are 100% correct;\n  - all misses came at 0.55.\n\n### Synthetic rows (40, SYNTHETIC: real receipts with amounts or memos changed)\n| type | n | auto | proposed (top-1) | exception | end-to-end correct |\n|---|---|---|---|---|---|\n| bank fee -$15/25/35 | 10 | 0 | 5 (100%) | 5 | 50% |\n| rounding ±$0.01/0.02 | 10 | 0 | 9 (100%) | 1 | 90% |\n| 10% short pay | 10 | 0 | 7 (100%) | 3 | 70% |\n| one receipt for two invoices | 10 | 0 | 3 (67%) | 7 | 20%* |\n| **all synthetic** | **40** | **0** | **24 (95.8%)** | **16** | **57.5%** |\n\n- No synthetic receipt is ever auto-applied.\n- Bank fees and short payments **without a memo ref** are still always exceptions, because `fee_tolerance` only\n  applies on the reference path (FAILURES #12).\n- *Test-set defect: 7 of the 10 \"combined\" labels pair an invoice that had already been paid before the receipt\n  date. The matcher is right to refuse them. On the 3 valid rows it scores 2 of 3.\n\n### The 7 live unapplied receipts\n- **3 auto-applied, all correct:** Castellano INV-25845, Yardley INV-25867 and Studio Zeller INV-25937.\n- **4 proposed:**\n  - Jessop INV-25784, Brandt & Lowell INV-25806 and Achebe + Pemberton INV-25951 are correct.\n  - Kingsway is proposed as INV-25469, with INV-25852 as the alternative. Both are held.\n- **\"Already received\" is now $78,348.** Kingsway's single receipt is counted once (was $83,448).\n\n---\n\n## 2. Controller: dispute detection and holds\n\n### 2a. Overdue invoices vs the analyst's list (`analysis/work/tickets_invoice_refs.csv`, 14 invoices, $309,000)\n| measure | value |\n|---|---|\n| Pipeline overdue invoices with DISPUTE / CANCELLATION / LEGAL_RISK | 16 |\n| True positives / false negatives | 14 / **0. Recall 100%** |\n
… [tool input truncated]
```

### Tool · 2026-11-20 18:18:19 UTC
**Tool result:**
```
The file /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/EVAL.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
Now I'll rewrite EVAL.md with current numbers.
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/EVAL.md",
 "content": "# EVAL: how well the agents work on the real records\n\nQA Evaluator. **Updated 2026-11-20 at 12:20 CST (QA pass 2)** against the current code. That code includes:\n- the severity-1 fix for unidentified payers;\n- a stricter fuzzy match;\n- strong refusals read in any ticket category;\n- the Reyes fix;\n- a $10k auto-apply cap;\n- top-50 not-due → NO_ACTION;\n- card re-runs blocked on legal threats.\n\nThe first pass (11:36) is superseded. Its numbers appear below only as \"was\". Nothing in `app/` or `data/` was\nchanged. Data as of 2026-10-31.\n\n| script | what it does | output |\n|---|---|---|\n| `analysis/scripts/eval_cash_app.py` | replays 286 test payments against the invoice book as it stood on each received date | `analysis/work/eval_cash_app_results.csv`, `.log` |\n| `analysis/scripts/eval_controller.py` | dispute detection vs the analyst's list; reads all 1,041 tickets | `analysis/work/eval_ticket_reads.csv`, `.log` |\n| `analysis/scripts/eval_guardrails.py` | red-team on changed copies of the data held in memory | `analysis/work/eval_guardrails_results.csv`, `.log` |\n| `analysis/scripts/eval_policy.py` | FIN-1 policy check on every invoice | `analysis/work/eval_policy_results.csv`, `.log` |\n| `analysis/scripts/eval_web.py <tmpdir>` | screen consistency and human-action flows via TestClient | `analysis/work/eval_web_results.csv`, `.log` |\n\n**Headline**\n- **Cash application:** 0 wrong automatic applications (59 of 59 correct on real data). Proposals put the right\n  invoice first 98.3% of the time.\n- **Dispute detection:** recall 100% on the analyst's 14 disputes.\n- **Guardrail red-team: 54 of 54 pass** (was 44 of 54).\n- **FIN-1 policy check: 11 of 12 pass.** The courtesy note 5 days before the due date never fires.\n- **Approval UI: 22 of 27 flows pass.** Three server-side bypasses remain. See `analysis/QA_PASS_2.md`.\n\n---\n\n## 1. Cash Application (`analysis/testset_cash_app.csv`, 286 rows)\n\n**Harness.** For each payment, the invoice book is rebuilt as of the receipt date. An invoice is open if\n`issue_date <= received_date` and (`paid_date` is blank or `paid_date >= received_date`). The production\n`cash_app.run()` is called unchanged with DEFAULT_RULES. An answer is correct when the proposed invoice set equals the\nlabel. For PAY-65805 (Kingsway), which is ambiguous, either invoice is accepted.\n\n### Real rows (246)\n| difficulty | n | auto-applied | auto precision | proposed | proposal top-1 | exception | end-to-end correct |\n|---|---|---|---|---|---|---|---|\n| trivial (card) | 20 | 20 | 100% | 0 | n/a | 0 | 100% |\n| easy (memo ref) | 63 | 39 | 100% | 24 | 100% | 0 | 100% |\n| medium (no ref, unique amount) | 83 | 0 | n/a | 83 | 100% | 0 | 100% |\n| hard (same-amount ties / truncated payer) | 80 | 0 | n/a | 68 | 95.6% | 12 | 81.2% |\n| **all real** | **246** | **59** | **100% (59/59)** | **175** | **98.3% (172/175)** | **12 (4.9%)** | **93.9%** |\n\n- **No wrong auto-apply, so no severity-1.**\n- **What the $10k cap changed.** Real auto-applies went from 81 to 59.\n  - The 22 exact-reference receipts over $10,000 are now proposals at confidence 0.95, and all 22 are correct.\n  - Nothing became wrong. Priya simply confirms 22 more items, each a one-click confirmation.\n  - The live book is unaffected: its 3 auto-applies are $564, $987 and $3,672.\n- **3 wrong proposals (unchanged):** PAY-61158, PAY-61365 and PAY-65656.\n  - Each is a same-amount tie where staff applied a newer invoice than the oldest.\n  - The true invoice is always in \"alternatives\", and all tied invoices are held.\n- **12 exceptions, all truncated payer names** (`TAN`, `OYELARAN` x2, `ROSALES` x2, `HUME`, `ASHBY`, `CRANE`,\n  `LINDQVIST`, `CALLOWAY`, `KESSLER`, `PEMBERTON`).\n  - **None is now assigned to a wrong customer.** Before the fix, PEMBERTON went to C1235.\n  - The Controller now holds any open invoice with the same amount (`controller.py:36-43`).\n- Confidence calibration is unchanged:\n  - auto-apply is 0.99 and 100% correct;\n  - proposals at 0.82 to 0.95 are 100% correct;\n  - all misses came at 0.55.\n\n### Synthetic rows (40, SYNTHETIC: real receipts with amounts or memos changed)\n| type | n | auto | proposed (top-1) | exception | end-to-end correct |\n|---|---|---|---|---|---|\n| bank fee -$15/25/35 | 10 | 0 | 5 (100%) | 5 | 50% |\n| rounding ±$0.01/0.02 | 10 | 0 | 9 (100%) | 1 | 90% |\n| 10% short pay | 10 | 0 | 7 (100%) | 3 | 70% |\n| one receipt for two invoices | 10 | 0 | 3 (67%) | 7 | 20%* |\n| **all synthetic** | **40** | **0** | **24 (95.8%)** | **16** | **57.5%** |\n\n- No synthetic receipt is ever auto-applied.\n- Bank fees and short payments **without a memo ref** are still always exceptions, because `fee_tolerance` only\n  applies on the reference path (FAILURES #12).\n- *Test-set defect: 7 of the 10 \"combined\" labels pair an invoice that had already been paid before the receipt\n  date. The matcher is right to refuse them. On the 3 valid rows it scores 2 of 3.\n\n### The 7 live unapplied receipts\n- **3 auto-applied, all correct:** Castellano INV-25845, Yardley INV-25867 and Studio Zeller INV-25937.\n- **4 proposed:**\n  - Jessop INV-25784, Brandt & Lowell INV-25806 and Achebe + Pemberton INV-25951 are correct.\n  - Kingsway is proposed as INV-25469, with INV-25852 as the alternative. Both are held.\n- **\"Already received\" is now $78,348.** Kingsway's single receipt is counted once (was $83,448).\n\n---\n\n## 2. Controller: dispute detection and holds\n\n### 2a. Overdue invoices vs the analyst's list (`analysis/work/tickets_invoice_refs.csv`, 14 invoices, $309,000)\n| measure | value |\n|---|---|\n| Pipeline overdue invoices with DISPUTE / CANCELLATION / LEGAL_RISK | 16 |\n| True positives / false negatives | 14 / **0. Recall 100%** |\n
… [tool input truncated]
```

### Claude · 2026-11-20 18:19:12 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FAILURES.md",
 "content": "# FAILURES: where the system is wrong, unsure, or could be gamed\n\nQA Evaluator. **Updated 2026-11-20 at 12:20 CST (QA pass 2).** Every case can be reproduced with\n`analysis/scripts/eval_*.py`. The numbers are in `analysis/EVAL.md`; the web-app checks are in\n`analysis/QA_PASS_2.md`.\n\n**REAL** means it happens on today's records. **REAL + MUTATION** means a real record changed in memory in a way the\ndata shows is common. **SYNTHETIC** means injected text or amounts, labelled as such.\n\n**Status** is FIXED (re-tested on current code), OPEN, or BY DESIGN. The fixed cases are kept, because the\nbefore/after is part of the evidence.\n\n---\n\n## Open: what a person still has to watch\n\n### A. \"Override hold\" lifts a dispute hold without the account manager (REAL UI path). OPEN, sev-2\n- **What happened.** On Riverside's disputed INV-25787, \"Release hold\" correctly refuses without the \"AM confirmed\"\n  box and the AM's name. But the **\"Override hold\"** button right next to it (`_invoice.html:50-51`) lifts the same\n  DISPUTE hold with any 5-character reason. We did this on Okafor & Nakamura INV-25765 with \"QA: just chase them\":\n  HTTP 200, and the invoice moved to \"Hold lifted: write or approve the message\".\n- **Why.** `views.py:535-536` checks the AM requirement only when `kind == \"release_hold\"`.\n- **Impact.** $312,922 of disputed invoices can be released by one click. That defeats Maya's condition: \"the hold\n  should only be released once the AM agrees the dispute is settled\".\n- **What a person should do.** Never use Override on a dispute or cancellation. Use Release with the AM's name.\n- **Fix idea.** Apply the AM check to both kinds, or hide Override when a DISPUTE or CANCELLATION hold is present.\n\n### B. The send endpoint trusts the browser (REAL UI/API path). OPEN, sev-2\n- **What happened.**\n  - (1) A POST to `/collections/INV-25784/send` (Jessop, money received, HOLD, no override) was accepted and logged as\n    **sent**. That is a Paidly chase recorded by the system.\n  - (2) Typing `ap@okaforlegal-billing.example`, a look-alike not in contacts.csv, into the editable \"To\" field of\n    INV-25848 was accepted.\n- **Why.** `views.py:493-515` checks only the banned wording. It does not check the invoice's action or hold state,\n  or whether recipients are verified. The UI hides the form for held invoices, but nothing on the server enforces it.\n- **Impact.** In this demo, sends are simulated. Once sending is wired, both are wrong-chase or wrong-recipient\n  incidents.\n- **Fix idea.** Allow a send only for DRAFT_REMINDER or HUMAN_WRITES invoices, or after a logged override or release.\n  Restrict \"To\" to `collections.recipients(ctx)` addresses.\n\n### C. A partial rules save switches guardrails off (REAL API path). OPEN, sev-2\n- **What happened.** A POST to `/rules` with only `fee_tolerance=25` set `top50_human_only`,\n  `auto_apply_exact_ref_match` and `notify_am_before_contact` to false, and **emptied the banned-phrase list (13 → 0)**.\n- **Why.** `views.py:276-300` treats a missing checkbox as False and a missing textarea as an empty list. The full\n  browser form is fine. A script, an old tab or a future \"quick edit\" is not.\n- **Also.** Priya can untick \"top-50: a person writes\" on her own. Policy makes that Dana's call, or the CEO's.\n- **Fix idea.** Only update keys present in the form. Refuse an empty banned list. Require Dana's approval to switch\n  off top-50, the banned list or the AM cc.\n\n### D. No courtesy note before the due date (REAL). OPEN, sev-2 (policy gap; no harm done)\n- **What happened.** Policy says to send a courtesy note 5 days before the due date. **16 invoices, $219,071, are due\n  on 1–5 Nov and none gets one.** They show as \"Next reminder at day 7\". Examples: INV-25933 Whitlock (due 11-01) and\n  INV-25950 Achebe + Pemberton (due 11-04, $67,968).\n- **Why.** `pipeline.py:74` uses `ar_aging.days_past_due`, which the QuickBooks export floors at 0 (FACTS §1). So\n  `stage_for()` never sees a negative number.\n- **Impact.** The friendliest step of the policy is skipped. Late payment could follow, as could complaints from\n  customers who wanted a heads-up.\n- **Fix idea.** Compute days past due from `due_date` and AS_OF, and floor it only for display.\n\n### E. Live state disappears on restart, including the demo video link (REAL, live). BY DESIGN on the free plan, but must be disclosed\n- **What happened.**\n  - The live audit log currently shows 0 human actions.\n  - On every deploy (autoDeploy on each push) or idle spin-down, everything Priya, Dana or a reviewer did is lost:\n    approvals, sends, overrides, AM releases, rules changes, chat history and the Loom link saved on /demo.\n  - Instructions accepted in Direct are appended to the agent manual inside the container, then revert to the repo\n    version.\n- **Why.** SQLite, rules.json and the manuals live on the container's disk. `render.yaml` asks for a paid plan with a\n  disk, but the live service is on the free plan.\n- **Impact.** The \"append-only audit log\" isn't durable on live. A reviewer who approves something and returns\n  later sees nothing.\n- **What to do now.** Set `DEMO_VIDEO_URL` in the Render env. Commit accepted instructions. Show \"demo state resets on\n  restart\" on the RIG.\n- **For go-live.** A paid instance with a disk, or Postgres.\n\n### F. Kingsway: one $5,100 payment, two $5,100 invoices (REAL). OPEN (the system is unsure, correctly)\n- **What happened.**\n  - PAY-65805 ($5,100, no memo) from Kingsway. Two overdue $5,100 invoices exist: INV-25469 (111 dpd) and INV-25852\n    (19 dpd).\n  - The agent proposes the oldest, the house convention (91% historically), and holds both. That is right.\n  - \"Already
… [tool input truncated]
```

### Tool · 2026-11-20 18:19:13 UTC
**Tool result:**
```
The file /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FAILURES.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FAILURES.md",
 "content": "# FAILURES: where the system is wrong, unsure, or could be gamed\n\nQA Evaluator. **Updated 2026-11-20 at 12:20 CST (QA pass 2).** Every case can be reproduced with\n`analysis/scripts/eval_*.py`. The numbers are in `analysis/EVAL.md`; the web-app checks are in\n`analysis/QA_PASS_2.md`.\n\n**REAL** means it happens on today's records. **REAL + MUTATION** means a real record changed in memory in a way the\ndata shows is common. **SYNTHETIC** means injected text or amounts, labelled as such.\n\n**Status** is FIXED (re-tested on current code), OPEN, or BY DESIGN. The fixed cases are kept, because the\nbefore/after is part of the evidence.\n\n---\n\n## Open: what a person still has to watch\n\n### A. \"Override hold\" lifts a dispute hold without the account manager (REAL UI path). OPEN, sev-2\n- **What happened.** On Riverside's disputed INV-25787, \"Release hold\" correctly refuses without the \"AM confirmed\"\n  box and the AM's name. But the **\"Override hold\"** button right next to it (`_invoice.html:50-51`) lifts the same\n  DISPUTE hold with any 5-character reason. We did this on Okafor & Nakamura INV-25765 with \"QA: just chase them\":\n  HTTP 200, and the invoice moved to \"Hold lifted: write or approve the message\".\n- **Why.** `views.py:535-536` checks the AM requirement only when `kind == \"release_hold\"`.\n- **Impact.** $312,922 of disputed invoices can be released by one click. That defeats Maya's condition: \"the hold\n  should only be released once the AM agrees the dispute is settled\".\n- **What a person should do.** Never use Override on a dispute or cancellation. Use Release with the AM's name.\n- **Fix idea.** Apply the AM check to both kinds, or hide Override when a DISPUTE or CANCELLATION hold is present.\n\n### B. The send endpoint trusts the browser (REAL UI/API path). OPEN, sev-2\n- **What happened.**\n  - (1) A POST to `/collections/INV-25784/send` (Jessop, money received, HOLD, no override) was accepted and logged as\n    **sent**. That is a Paidly chase recorded by the system.\n  - (2) Typing `ap@okaforlegal-billing.example`, a look-alike not in contacts.csv, into the editable \"To\" field of\n    INV-25848 was accepted.\n- **Why.** `views.py:493-515` checks only the banned wording. It does not check the invoice's action or hold state,\n  or whether recipients are verified. The UI hides the form for held invoices, but nothing on the server enforces it.\n- **Impact.** In this demo, sends are simulated. Once sending is wired, both are wrong-chase or wrong-recipient\n  incidents.\n- **Fix idea.** Allow a send only for DRAFT_REMINDER or HUMAN_WRITES invoices, or after a logged override or release.\n  Restrict \"To\" to `collections.recipients(ctx)` addresses.\n\n### C. A partial rules save switches guardrails off (REAL API path). OPEN, sev-2\n- **What happened.** A POST to `/rules` with only `fee_tolerance=25` set `top50_human_only`,\n  `auto_apply_exact_ref_match` and `notify_am_before_contact` to false, and **emptied the banned-phrase list (13 → 0)**.\n- **Why.** `views.py:276-300` treats a missing checkbox as False and a missing textarea as an empty list. The full\n  browser form is fine. A script, an old tab or a future \"quick edit\" is not.\n- **Also.** Priya can untick \"top-50: a person writes\" on her own. Policy makes that Dana's call, or the CEO's.\n- **Fix idea.** Only update keys present in the form. Refuse an empty banned list. Require Dana's approval to switch\n  off top-50, the banned list or the AM cc.\n\n### D. No courtesy note before the due date (REAL). OPEN, sev-2 (policy gap; no harm done)\n- **What happened.** Policy says to send a courtesy note 5 days before the due date. **16 invoices, $219,071, are due\n  on 1–5 Nov and none gets one.** They show as \"Next reminder at day 7\". Examples: INV-25933 Whitlock (due 11-01) and\n  INV-25950 Achebe + Pemberton (due 11-04, $67,968).\n- **Why.** `pipeline.py:74` uses `ar_aging.days_past_due`, which the QuickBooks export floors at 0 (FACTS §1). So\n  `stage_for()` never sees a negative number.\n- **Impact.** The friendliest step of the policy is skipped. Late payment could follow, as could complaints from\n  customers who wanted a heads-up.\n- **Fix idea.** Compute days past due from `due_date` and AS_OF, and floor it only for display.\n\n### E. Live state disappears on restart, including the demo video link (REAL, live). BY DESIGN on the free plan, but must be disclosed\n- **What happened.**\n  - The live audit log currently shows 0 human actions.\n  - On every deploy (autoDeploy on each push) or idle spin-down, everything Priya, Dana or a reviewer did is lost:\n    approvals, sends, overrides, AM releases, rules changes, chat history and the Loom link saved on /demo.\n  - Instructions accepted in Direct are appended to the agent manual inside the container, then revert to the repo\n    version.\n- **Why.** SQLite, rules.json and the manuals live on the container's disk. `render.yaml` asks for a paid plan with a\n  disk, but the live service is on the free plan.\n- **Impact.** The \"append-only audit log\" isn't durable on live. A reviewer who approves something and returns\n  later sees nothing.\n- **What to do now.** Set `DEMO_VIDEO_URL` in the Render env. Commit accepted instructions. Show \"demo state resets on\n  restart\" on the RIG.\n- **For go-live.** A paid instance with a disk, or Postgres.\n\n### F. Kingsway: one $5,100 payment, two $5,100 invoices (REAL). OPEN (the system is unsure, correctly)\n- **What happened.**\n  - PAY-65805 ($5,100, no memo) from Kingsway. Two overdue $5,100 invoices exist: INV-25469 (111 dpd) and INV-25852\n    (19 dpd).\n  - The agent proposes the oldest, the house convention (91% historically), and holds both. That is right.\n  - \"Already
… [tool input truncated]
```

### Claude · 2026-11-20 18:19:20 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -la app/engine/manuals ledgerline.db; ls rules.json 2>&1; grep -c \"over \\$40k\" app/engine/manuals/*.md",
 "description": "Confirm repo files were not polluted"
}
```

### Tool · 2026-11-20 18:19:21 UTC
**Tool result:**
```
-rw-r--r--@ 1 jacekmaterna  staff  40960 Nov 20 12:14 ledgerline.db

app/engine/manuals:
total 32
drwxr-xr-x@  6 jacekmaterna  staff   192 Nov 20 11:38 .
drwxr-xr-x@ 14 jacekmaterna  staff   448 Nov 20 12:14 ..
-rw-r--r--@  1 jacekmaterna  staff  1303 Nov 20 11:21 account_context.md
-rw-r--r--@  1 jacekmaterna  staff  1470 Nov 20 11:38 cash_application.md
-rw-r--r--@  1 jacekmaterna  staff  1193 Nov 20 11:21 collections.md
-rw-r--r--@  1 jacekmaterna  staff  1585 Nov 20 11:38 controller.md
ls: rules.json: No such file or directory
app/engine/manuals/cash_application.md:0
app/engine/manuals/account_context.md:0
app/engine/manuals/collections.md:0
app/engine/manuals/controller.md:0
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -la app/engine/manuals ledgerline.db; ls rules.json 2>&1; grep -c \"over \\$40k\" app/engine/manuals/*.md",
 "description": "Confirm repo files were not polluted"
}
```

### Claude · 2026-11-20 18:19:28 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -la --time-style=+%H:%M:%S app/engine 2>/dev/null || ls -laT app/engine | tail -8; sqlite3 ledgerline.db \"select ts,user_email,action,object_id from actions order by id desc limit 3\" 2>&1 | head",
 "description": "Check what changed at 12:14"
}
```

### Tool · 2026-11-20 18:19:29 UTC
**Tool result:**
```
-rw-r--r--@  1 jacekmaterna  staff   8717 Nov 20 11:58:35 2026 controller.py
-rw-r--r--@  1 jacekmaterna  staff   3581 Nov 20 11:35:12 2026 data.py
-rw-r--r--@  1 jacekmaterna  staff   2297 Nov 20 11:29:41 2026 digest.py
-rw-r--r--@  1 jacekmaterna  staff   2694 Nov 20 11:25:38 2026 llm.py
drwxr-xr-x@  6 jacekmaterna  staff    192 Nov 20 11:38:04 2026 manuals
-rw-r--r--@  1 jacekmaterna  staff  12062 Nov 20 12:10:59 2026 pipeline.py
-rw-r--r--@  1 jacekmaterna  staff   7767 Nov 20 12:14:20 2026 questions.py
-rw-r--r--@  1 jacekmaterna  staff   4014 Nov 20 11:47:53 2026 rules.py
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls -la --time-style=+%H:%M:%S app/engine 2>/dev/null || ls -laT app/engine | tail -8; sqlite3 ledgerline.db \"select ts,user_email,action,object_id from actions order by id desc limit 3\" 2>&1 | head",
 "description": "Check what changed at 12:14"
}
```

### Claude · 2026-11-20 18:19:36 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && RULES_PATH=/private/tmp/claude-501/qa2/rules.json .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline\nm=run_pipeline()['metrics']; print({k:m[k] for k in ['overdue_already_paid','overdue_disputed','held','drafts','human_writes','card_retries','dana_decisions','auto_applied']})\"; sed -n 70,76p app/engine/pipeline.py",
 "description": "Confirm metrics unchanged after latest edit"
}
```

### Tool · 2026-11-20 18:19:38 UTC
**Tool result:**
```
{'overdue_already_paid': 78348.0, 'overdue_disputed': 312922.0, 'held': 21, 'drafts': 20, 'human_writes': 3, 'card_retries': 9, 'dana_decisions': 3, 'auto_applied': 3}
    invoices = []
    for _, r in ar.sort_values("amount", ascending=False).iterrows():
        inv = {"invoice_id": r["invoice_id"], "customer_id": r["customer_id"], "customer_name": r["customer_name"],
               "amount": float(r["amount"]), "issue_date": r["issue_date"], "due_date": r["due_date"],
               "days_past_due": int(r["days_past_due"]), "ar_status": r["status"], "bucket": r["bucket"], "plan": r["plan"]}
        ctx = ctxs.get(r["customer_id"])
        stage = collections.stage_for(inv["days_past_due"], inv["ar_status"], rules)
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && RULES_PATH=/private/tmp/claude-501/qa2/rules.json .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline\nm=run_pipeline()['metrics']; print({k:m[k] for k in ['overdue_already_paid','overdue_disputed','held','drafts','human_writes','card_retries','dana_decisions','auto_applied']})\"; sed -n 70,76p app/engine/pipeline.py",
 "description": "Confirm metrics unchanged after latest edit"
}
```

### Claude · 2026-11-20 18:19:53 UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "QA pass 2 is done (12:10–12:20 CST). The agents have no sev-1, but the approval web app has 3 server-side bypasses that need closing before Maya or Priya uses the RIG. Nothing in app/ or data/ was edited. Local tests used a temp DB, rules file and manuals dir; the live site only got read-only checks, two requests meant to be rejected, and one chat \"status\". The builder was still editing (pipeline.py 12:10, questions.py 12:14); I re-ran metrics after and they are unchanged.\n\n**PASS/FAIL by section**\n- **A. Cash application (FIN-2): PASS 5/5.** 59/59 auto-applies correct (100%), top-1 98.3%. The $10k cap moves 22 exact-reference receipts to proposals, all correct; the live 3 auto-applies are unaffected. BRANDT/JESSOP/KINGSWAY replays are held. Guardrail red-team 54/54 (was 44/54).\n- **B. FIN-1 policy, all 117 invoices: 11 PASS, 1 FAIL.** No courtesy notes: 16 invoices ($219,071) due in the next 1–5 days never get one.\n- **C. Consistency: PASS 18/18.** Home, /today, /collections, /digest, chat \"status\", Team and run_pipeline() all agree ($633,245 / $78,348 / $312,922 / $241,975; 20 drafts, 21 held, 9 card re-runs, 3 for a person, 57 needing a human).\n- **D. Human-action flows: 22 PASS, 5 FAIL** (defects below). On live, the two rejection checks returned 400 as expected.\n- **E. Maya tab: renders correctly** (4 exchanges, 4/60, Draft 6 pending). 11 rough edges elsewhere on the RIG; 0 broken internal links.\n- **F. Speed PASS** (every page under 2s, live 0.1–0.7s warm). **Durability FAIL:** live state is ephemeral; live currently shows 0 human actions.\n\n**Sev-2 defects**\n1. views.py:535-536 – \"Override hold\" lifts DISPUTE/CANCELLATION holds without AM confirmation; the button sits next to \"Release\" (_invoice.html:50-51). Fix: apply the AM check to both, or hide Override on disputes.\n2. views.py:493-515 – a send is accepted on a held invoice (Jessop, money received) and to any typed \"To\" address. Fix: only allow DRAFT_REMINDER/HUMAN_WRITES or a logged override, and only verified recipients.\n3. views.py:276-300 – a POST to /rules with only one field turns off top-50, auto-apply and AM-cc, and empties banned_phrases (13 → 0). Fix: update only fields present in the form; refuse an empty banned list; Dana approves turning guardrails off.\n4. pipeline.py:74 – uses ar_aging's days_past_due, which is floored at 0, so there is no courtesy stage. Fix: compute from due_date.\n5. RIG:\n   - /demo shows \"Coming soon\" plus internal video-prep notes (\"Leave Maya on hold…\").\n   - Live Maya tab reads 5/60 because trail/MAYA_QA.md:3 is stale (outbox says 4); redeploy after fixing.\n   - The Docs GitHub link returns 404.\n6. Live state, including the saved Loom link, is lost on every deploy or idle spin-down. Fix: set DEMO_VIDEO_URL in Render env and say so on the RIG.\n\n**Sev-3:** a payment can be approved twice (views.py:443); \"A person writes these (top-50 accounts)\" contains 2 non-top-50 invoices (views.py:32); the $10k cap is missing from the Cash manual and cards; live timestamps are UTC while everything else is CST; \"1 days\"; the Dana tile names 2 of 3; Ambrose's hold subject shows \"???\"; \"court\" is banned as a substring (controller.py:127).\n\n**Verdict:** FIN-2 is at 100% and FIN-1's decisions are correct apart from the courtesy stage. The RIG is not ready for Maya until defects 1–3 and 5 are closed (about 1 hour of work).\n\nFiles are in analysis/:\n- QA_PASS_2.md\n- EVAL.md and FAILURES.md (updated to current code)\n- scripts/eval_policy.py, scripts/eval_web.py (new)\n- scripts/eval_guardrails.py (one check updated)\n- work/eval_*_results.csv and .log"
}
```

### Tool · 2026-11-20 18:19:53 UTC
**Tool result:**
```
{"success":true,"message":"Report delivered to your caller."}
```
