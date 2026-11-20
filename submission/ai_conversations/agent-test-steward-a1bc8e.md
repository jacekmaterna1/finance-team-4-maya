# Build agent: test-steward (log exchanges 2-3)

_Exported from the Claude Code session log. Redactions are explained in the index._

### Jacek · 2026-11-20 17:25:38 UTC
Project root (quote it): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a". Log these Maya exchanges word for word into trail/MAYA_QA.md (Exchange 2 and Exchange 3, with "What we changed because of it"), mark Draft 2 SENT in trail/MAYA_OUTBOX.md with a note that the main thread revised it before sending (newer numbers after a dispute-detection fix; Q1 swapped from bank-fee threshold to failed-card re-runs because analysis/FACTS.md shows the data has no bank fees or short payments), set the counter to 3 of 60 used, and append JOURNAL rows + DECISIONS entries (D8 card re-runs = Priya approves each; D9 Slack-style morning digest; D10 disputes routed to AM, hold released only on AM confirmation; D11 AI off by default until Legal signs a DPA, Bedrock via existing AWS agreement preferred, only ticket text + invoice facts ever sent). Also add to JOURNAL: 11:24 T+0:14 data-analyst finished — Dana's "risen three quarters running" is false quarter-on-quarter (sawtooth $221k/$494k/$209k/$600k) but true year-on-year (+17%, +41%, +23%); at 31 Mar 2026 43% of reported overdue was already-received cash; dispute detection fixed to catch disputes tagged How-to/untagged and now matches the analyst's 14 invoices / $309k exactly.

Exchange 2 — sent 11:26 CST (T+0:16), Jacek (sent by Claude Code at Jacek's standing instruction):
"Hi Maya, an update at T+0:15. The four agents now run end to end on the real records. Of the $633k overdue on the ledger, $83k is money we have already received but not applied, $312k is disputed in support tickets finance can't see (14 invoices, plus Eastman Engineering's chargeback threat), and about $238k is genuinely collectable. Most disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 22 wrong chases prevented, 27 reminders drafted for Priya to approve, 11 that need a person to write. Three questions: (1) 10 of the 16 failed card invoices belong to customers whose later card charges went through, and Northgate's $799 is written off automatically tomorrow. May the system re-run a failed charge on a card that works, or does Priya decide each one? (2) Does Priya work best from a morning queue in the tool or a Slack or email digest, and must the account manager approve before a hold is released? (3) Should disputed invoices go to the account manager automatically with the ticket text, or should finance own the fix with support?"

Maya:
"Those numbers are worth showing Dana today, especially the $312k sitting in "solved" tickets. On re-running cards, I'd want Priya to approve each one for now. Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes. Tell Dana about Northgate's $799 this morning so she can decide before it writes off.

I believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool, but ask her directly because she'll be the one using it. For the disputes, I'd send them to the account manager with a summary, because the AMs own the relationship and are walking into renewal calls blind. Finance and support would still fix the billing error together, and the hold should only be released once the AM agrees the dispute is settled.

You're now pushing ticket text and customer financials through these agents. Which AI provider is doing that, and have you confirmed it doesn't train on our data? Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement."

Exchange 3 — sent ~11:28 CST (T+0:18), Jacek:
"Good challenge, and nothing has gone to any AI provider yet. Everything you've seen so far is rules and matching on the records. The provider would be Claude from Anthropic. Under Anthropic's commercial terms, API inputs and outputs are not used to train models, and a DPA is available, but Legal should review it before any real data flows. Since Ledgerline already hosts on AWS, the cleaner route is Claude through Amazon Bedrock under your existing AWS agreement: Amazon doesn't share the data with the model provider or use it for training, and Legal adds no new vendor. Until Legal signs off, the AI stays switched off with one setting. Holds and matching keep working on rules, and drafts come from your own templates. When it's on, only ticket text and invoice facts are sent, never bank details. Taking your other answers: card re-runs become a proposal Priya approves one by one. Northgate goes to Dana as a decision today. Priya gets a short Slack morning digest that links to the queue. Disputes go to the account manager with a summary, and a hold is released only when the AM confirms it's settled."
Maya's reply to exchange 3: not yet received — leave a placeholder "(awaiting reply)".

Code already changed (record in JOURNAL): rules.use_claude now defaults to False; llm.py supports LLM_PROVIDER=bedrock. Then draft Maya message 4 (READY, single line, ≤120 words) for the next milestone "app live on Render" — leave numbers as placeholders like {URL}. Report back in 3 lines.

### Jacek · 2026-11-20 17:25:38 UTC
[harness system note omitted]

### Jacek ·  UTC
[harness system note omitted]

Project root (quote it): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a". Log these Maya exchanges word for word into trail/MAYA_QA.md (Exchange 2 and Exchange 3, with "What we changed because of it"), mark Draft 2 SENT in trail/MAYA_OUTBOX.md with a note that the main thread revised it before sending (newer numbers after a dispute-detection fix; Q1 swapped from bank-fee threshold to failed-card re-runs because analysis/FACTS.md shows the data has no bank fees or short payments), set the counter to 3 of 60 used, and append JOURNAL rows + DECISIONS entries (D8 card re-runs = Priya approves each; D9 Slack-style morning digest; D10 disputes routed to AM, hold released only on AM confirmation; D11 AI off by default until Legal signs a DPA, Bedrock via existing AWS agreement preferred, only ticket text + invoice facts ever sent). Also add to JOURNAL: 11:24 T+0:14 data-analyst finished — Dana's "risen three quarters running" is false quarter-on-quarter (sawtooth $221k/$494k/$209k/$600k) but true year-on-year (+17%, +41%, +23%); at 31 Mar 2026 43% of reported overdue was already-received cash; dispute detection fixed to catch disputes tagged How-to/untagged and now matches the analyst's 14 invoices / $309k exactly.

Exchange 2 — sent 11:26 CST (T+0:16), Jacek (sent by Claude Code at Jacek's standing instruction):
"Hi Maya, an update at T+0:15. The four agents now run end to end on the real records. Of the $633k overdue on the ledger, $83k is money we have already received but not applied, $312k is disputed in support tickets finance can't see (14 invoices, plus Eastman Engineering's chargeback threat), and about $238k is genuinely collectable. Most disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 22 wrong chases prevented, 27 reminders drafted for Priya to approve, 11 that need a person to write. Three questions: (1) 10 of the 16 failed card invoices belong to customers whose later card charges went through, and Northgate's $799 is written off automatically tomorrow. May the system re-run a failed charge on a card that works, or does Priya decide each one? (2) Does Priya work best from a morning queue in the tool or a Slack or email digest, and must the account manager approve before a hold is released? (3) Should disputed invoices go to the account manager automatically with the ticket text, or should finance own the fix with support?"

Maya:
"Those numbers are worth showing Dana today, especially the $312k sitting in "solved" tickets. On re-running cards, I'd want Priya to approve each one for now. Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes. Tell Dana about Northgate's $799 this morning so she can decide before it writes off.

I believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool, but ask her directly because she'll be the one using it. For the disputes, I'd send them to the account manager with a summary, because the AMs own the relationship and are walking into renewal calls blind. Finance and support would still fix the billing error together, and the hold should only be released once the AM agrees the dispute is settled.

You're now pushing ticket text and customer financials through these agents. Which AI provider is doing that, and have you confirmed it doesn't train on our data? Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement."

Exchange 3 — sent ~11:28 CST (T+0:18), Jacek:
"Good challenge, and nothing has gone to any AI provider yet. Everything you've seen so far is rules and matching on the records. The provider would be Claude from Anthropic. Under Anthropic's commercial terms, API inputs and outputs are not used to train models, and a DPA is available, but Legal should review it before any real data flows. Since Ledgerline already hosts on AWS, the cleaner route is Claude through Amazon Bedrock under your existing AWS agreement: Amazon doesn't share the data with the model provider or use it for training, and Legal adds no new vendor. Until Legal signs off, the AI stays switched off with one setting. Holds and matching keep working on rules, and drafts come from your own templates. When it's on, only ticket text and invoice facts are sent, never bank details. Taking your other answers: card re-runs become a proposal Priya approves one by one. Northgate goes to Dana as a decision today. Priya gets a short Slack morning digest that links to the queue. Disputes go to the account manager with a summary, and a hold is released only when the AM confirms it's settled."
Maya's reply to exchange 3: not yet received — leave a placeholder "(awaiting reply)".

Code already changed (record in JOURNAL): rules.use_claude now defaults to False; llm.py supports LLM_PROVIDER=bedrock. Then draft Maya message 4 (READY, single line, ≤120 words) for the next milestone "app live on Render" — leave numbers as placeholders like {URL}. Report back in 3 lines.

[harness system note omitted]

### Claude · 2026-11-20 17:25:42 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls trail submission 2>/dev/null; wc -l trail/*",
 "description": "List trail and submission files"
}
```

### Tool · 2026-11-20 17:25:42 UTC
**Tool result:**
```
trail:
DECISIONS.md
JOURNAL.md
MAYA_OUTBOX.md
MAYA_QA.md
SUBMISSION_CHECKLIST.md
      47 trail/DECISIONS.md
      21 trail/JOURNAL.md
      13 trail/MAYA_OUTBOX.md
      43 trail/MAYA_QA.md
      18 trail/SUBMISSION_CHECKLIST.md
     142 total
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls trail submission 2>/dev/null; wc -l trail/*",
 "description": "List trail and submission files"
}
```

### Claude · 2026-11-20 17:25:45 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && for f in trail/JOURNAL.md trail/MAYA_OUTBOX.md trail/MAYA_QA.md trail/DECISIONS.md; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Show trail file contents"
}
```

### Tool · 2026-11-20 17:25:45 UTC
**Tool result:**
```
=== trail/JOURNAL.md
# Journal — high-level trail of what we did

Timer started: **2026-11-20 ~11:10 CST** (the page showed 23h57m left at 11:13). Deadline ~2026-11-21 11:10 CST.

| Local time | T+ | Who | What | Why |
|---|---|---|---|---|
| 2026-11-20 (pre-start) | — | Jacek + Claude Code | Read the Scaleworks start page (brief, 31 processes, data-room index) and the SpaceXSI Grok-bot accounting article | Understand the test and the reference architecture before starting the clock |
| 2026-11-20 (pre-start) | — | Claude Code | Chose Claude Code subagents over Cowork scheduled tasks for the build team | We need a repo, code execution, a deploy and a git-based paper trail; scheduled tasks are for recurring jobs, not a one-day build |
| 2026-11-20 (pre-start) | — | Claude Code | Narrowed "all of finance" to one process (Collections + Cash Application) run by a 4-agent team | The brief says "Pick one" and prefers one thing working well over five sketched |
| 2026-11-20 (pre-start) | — | Claude Code | Set up the project: CLAUDE.md, 4 build subagents, plan, paper-trail files, prepared Maya questions | Be ready to work the moment the timer starts. No product code before the start |
| 2026-11-20 (pre-start) | — | Jacek | Locked the process: Collections (FIN-1) + Cash Application (FIN-2), run by the 4-agent Order-to-Cash team | Dana's overdue-invoice problem, the board's cash concern, and the brief's "pick one" |
| 11:10 | T+0:00 | Jacek | Pressed "Begin day one" | — |
| 11:11 | T+0:01 | Claude Code | Downloaded the data room zip (51 files) into data/. Found that system python/git are blocked by the Xcode license, so we use the Command Line Tools python 3.9 + a venv | Toolchain workaround, no admin needed |
| 11:13 | T+0:03 | Claude Code | Read collections_policy, process_maps, billing_engine_rewrite, board_update, collections templates, tool_stack | Found that Paidly (a collections tool) was switched off after 6 weeks in 2025, and the 45-day template threatens suspension against policy |
| 11:14 | T+0:04 | Jacek via Claude Code | Told Maya what we're building and asked 3 questions (Paidly, success metric, autonomy) | Jacek asked to brief Maya; 60-message budget, so bundled |
| 11:14 | T+0:04 | data-analyst (background) | Started profiling: schema, evidence numbers, labelled cash-app test set | Evidence for the demo and the one-pager |
| 11:15 | T+0:05 | Maya | Replied. Paidly chased an already-paid wire customer. Priya Nair (AR Specialist) is the real user. Metr
… [result truncated, 17081 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && for f in trail/JOURNAL.md trail/MAYA_OUTBOX.md trail/MAYA_QA.md trail/DECISIONS.md; do echo \"=== $f\"; cat \"$f\"; done",
 "description": "Show trail file contents"
}
```

### Claude · 2026-11-20 17:25:50 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"use_claude\" app | head; grep -n -i \"bedrock\\|LLM_PROVIDER\" app/engine/llm.py | head; grep -n -i \"bank fee\\|short pay\\|sawtooth\\|year-on-year\\|43%\\|309\\|14 invoices\\|quarter\" analysis/FACTS.md | head -20; ls -la trail; date",
 "description": "Verify code changes and facts"
}
```

### Tool · 2026-11-20 17:25:50 UTC
**Tool result:**
```
app/engine/context.py:85:    use_claude = bool(rules.get("use_claude", True))
app/engine/context.py:97:            read = claude_read(td, own, c["name"], use_claude) or heuristic_read(td, own)
app/engine/llm.py:3:If ANTHROPIC_API_KEY is not set (or use_claude is off), every call returns None and callers fall back to
app/engine/rules.py:23:    "use_claude": False,                  # OFF until Legal signs the DPA (Maya, T+0:17). Rules + templates work without it
app/engine/rules.py:40:    "use_claude": "Use Claude to read tickets and draft reminders. Keep OFF until Legal approves the DPA (Bedrock route preferred). Off = rules and templates",
app/engine/collections.py:71:    if rules.get("use_claude", True):
app/engine/collections.py:86:        r = llm.ask_json("draft_v1", system, user, enabled=bool(rules.get("use_claude")), max_tokens=700)
50:    provider = os.environ.get("LLM_PROVIDER", "anthropic")  # "bedrock" keeps data inside Ledgerline's AWS account
56:        client = anthropic.AnthropicBedrock() if provider == "bedrock" else anthropic.Anthropic()
19:## 2. Overdue trend: testing Dana's "risen three quarters running"
20:Method: rebuild the ledger at each date D. An invoice counts if issue_date <= D, due_date < D, and it is not settled by D. Settled means applied_date (ledger view) or received_date (cash view), or the write-off date for written_off rows. Output: `analysis/work/overdue_by_quarter.csv`.
22:| quarter end | overdue $ (ledger) | # | overdue $ (cash already received removed) | overdue >30d $ (ledger) |
34:- **F** Quarter on quarter, the claim is **false**. Overdue goes up, down, up, down, up: 221k → 494k → 209k → 600k. It is strongly seasonal. Month-end peaks fall in Feb-Mar and Aug-Oct, which are the annual-renewal billing waves.
35:- **F** Year on year, the claim is **true** for three straight quarters:
40:- **F** Part of reported "overdue" at each quarter end was cash already in the bank but not yet applied: $57k (Q3'25), $73k (Q4'25), **$210k (Q1'26, 43% of reported overdue)**, $75k (Q2'26) and $71k (Q3'26).
41:- **I** The board's line "overdue rose for three quarters" is defensible only as a year-on-year statement. A sequential chart would show a sawtooth. Cash-application lag inflates the quarter-end number.
78:  - 0 short payments
125:- **F** There is no dispute status or field. Disputes appear only as ticket text that cites a Ledgerline invoice id. **14 tickets cite an INV id, and all 14 invoices are currently overdue: $309,000 = 49% 
… [result truncated, 3502 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"use_claude\" app | head; grep -n -i \"bedrock\\|LLM_PROVIDER\" app/engine/llm.py | head; grep -n -i \"bank fee\\|short pay\\|sawtooth\\|year-on-year\\|43%\\|309\\|14 invoices\\|quarter\" analysis/FACTS.md | head -20; ls -la trail; date",
 "description": "Verify code changes and facts"
}
```

### Claude · 2026-11-20 17:25:56 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 30,40p analysis/FACTS.md; sed -n 70,82p analysis/FACTS.md; sed -n 180,195p analysis/FACTS.md; sed -n 15,30p app/engine/rules.py",
 "description": "Read relevant FACTS and rules sections"
}
```

### Tool · 2026-11-20 17:25:56 UTC
**Tool result:**
```
| 2026-10-31 (today) | 633,245 | 54 | 554,897* | 317,093 |

*Today's cash view subtracts the 5 unapplied receipts that match overdue invoices ($78,348).

- **F** Quarter on quarter, the claim is **false**. Overdue goes up, down, up, down, up: 221k → 494k → 209k → 600k. It is strongly seasonal. Month-end peaks fall in Feb-Mar and Aug-Oct, which are the annual-renewal billing waves.
- **F** Year on year, the claim is **true** for three straight quarters:
  - Q1: 423k → 494k (+17%)
  - Q2: 149k → 209k (+41%)
  - Q3: 488k → 600k (+23%)
  - October: 597k → 633k (+6%)
- **F** Part of reported "overdue" at each quarter end was cash already in the bank but not yet applied: $57k (Q3'25), $73k (Q4'25), **$210k (Q1'26, 43% of reported overdue)**, $75k (Q2'26) and $71k (Q3'26).
  - `Ledgerline subscription` 333
  - `<Surname> payment` about 200
  - blank 102
- **F** 5,108 of 5,801 applied memos contain an invoice ref, and **100% point at the invoice actually applied**. There are no wrong invoice numbers in history.
- **F** Bank payments with no invoice ref in the memo: 693 of 2,559 (27%). That is the real manual workload, consistent with FIN-2's "a third arrive with free-text memo".
- **F** Payer name drift on applied receipts: 19.9% (1,156). 740 are UPPERCASE and 416 are truncated (`MOTT`, `TAN`, `HARBOR CONSULTING`). There are no typos. Surname memos are highly ambiguous because 8 customers contain "Jessop", 12 contain "Brandt" and 16 start with "Studio".
- **F** Same-amount ambiguity: 75 historical bank receipts had 2 or more open invoices of identical amount for that customer. Staff applied to the **oldest open invoice in 68/75 (91%)**.
- **F, traps the brief expected but which are ABSENT from the data:**
  - 0 short payments
  - 0 bank-fee deductions ($15/$25/$35)
  - 0 combined receipts (each payment maps to exactly one invoice, at exactly the invoice amount)
  - 0 overpayments
  - 0 cent-level differences: every invoice and payment is a whole-dollar amount, before and after the 16 Mar rewrite
How the labels were made:
- **ledger_applied (239 rows)**: the invoice_id staff applied in payments.csv. The memo ref, where present, agrees in 100% of cases.
  - All 80 "hard" bank receipts: no memo ref, plus either 2 or more same-amount open invoices or a drifted payer name that fits 3 to 9 customers.
  - 80 sampled "medium": no memo ref, unique exact amount.
  - 60 sampled "easy": memo ref.
  - 20 card ("trivial", Stripe memo).
- **inferred (7 rows)**: the unapplied rec
… [result truncated, 4310 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 30,40p analysis/FACTS.md; sed -n 70,82p analysis/FACTS.md; sed -n 180,195p analysis/FACTS.md; sed -n 15,30p app/engine/rules.py",
 "description": "Read relevant FACTS and rules sections"
}
```

### Claude · 2026-11-20 17:26:01 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls rules.json 2>&1; grep -n \"def load\" -A12 app/engine/rules.py | head -20",
 "description": "Check rules.json and loader merge"
}
```

### Tool · 2026-11-20 17:26:01 UTC
**Tool result:**
```
ls: rules.json: No such file or directory
44:def load_rules():
45-    rules = copy.deepcopy(DEFAULT_RULES)
46-    try:
47-        with open(RULES_PATH, encoding="utf-8") as f:
48-            saved = json.load(f)
49-        for k, v in saved.items():
50-            if k in rules:
51-                rules[k] = v
52-    except (OSError, ValueError):
53-        pass
54-    return rules
55-
56-
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls rules.json 2>&1; grep -n \"def load\" -A12 app/engine/rules.py | head -20",
 "description": "Check rules.json and loader merge"
}
```

### Claude · 2026-11-20 17:26:18 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/MAYA_QA.md <<'EOF'\n\n### Exchange 2 — 11:26 CST, T+0:16\nSent by Claude Code at Jacek's standing instruction. The main thread revised Draft 2 before sending (see MAYA_OUTBOX.md).\n\n**Jacek:** Hi Maya, an update at T+0:15. The four agents now run end to end on the real records. Of the $633k overdue on the ledger, $83k is money we have already received but not applied, $312k is disputed in support tickets finance can't see (14 invoices, plus Eastman Engineering's chargeback threat), and about $238k is genuinely collectable. Most disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 22 wrong chases prevented, 27 reminders drafted for Priya to approve, 11 that need a person to write. Three questions: (1) 10 of the 16 failed card invoices belong to customers whose later card charges went through, and Northgate's $799 is written off automatically tomorrow. May the system re-run a failed charge on a card that works, or does Priya decide each one? (2) Does Priya work best from a morning queue in the tool or a Slack or email digest, and must the account manager approve before a hold is released? (3) Should disputed invoices go to the account manager automatically with the ticket text, or should finance own the fix with support?\n\n**Maya:** Those numbers are worth showing Dana today, especially the $312k sitting in \"solved\" tickets. On re-running cards, I'd want Priya to approve each one for now. Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes. Tell Dana about Northgate's $799 this morning so she can decide before it writes off.\n\nI believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool, but ask her directly because she'll be the one using it. For the disputes, I'd send them to the account manager with a summary, because the AMs own the relationship and are walking into renewal calls blind. Finance and support would still fix the billing error together, and the hold should only be released once the AM agrees the dispute is settled.\n\nYou're now pushing ticket text and customer financials through these agents. Which AI provider is doing that, and have you confirmed it doesn't train on our data? Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement.\n\n**What we changed because of it**\n1. **Card re-runs (D8):** the system never re-charges a card on its own. Where a customer's later card charges succeeded, it proposes a re-run, and Priya approves each one. Whether that ever becomes automatic is Dana's call.\n2. **Northgate $799:** goes to Dana today as a decision, before the 150-day automatic write-off.\n3. **Morning digest (D9):** Priya gets a short Slack-style morning digest that links to the queue, so she doesn't have to log into another tool. Still to confirm with Priya directly, as Maya said.\n4. **Disputes (D10):** routed to the account manager with a summary. Finance and support still fix the billing error together. A dispute hold is released only when the AM confirms it is settled.\n5. **Data and Legal (D11):** Maya's challenge led straight to Exchange 3. `rules.use_claude` now defaults to False, and `app/engine/llm.py` supports `LLM_PROVIDER=bedrock`.\n\n### Exchange 3 — ~11:28 CST, T+0:18\n**Jacek:** Good challenge, and nothing has gone to any AI provider yet. Everything you've seen so far is rules and matching on the records. The provider would be Claude from Anthropic. Under Anthropic's commercial terms, API inputs and outputs are not used to train models, and a DPA is available, but Legal should review it before any real data flows. Since Ledgerline already hosts on AWS, the cleaner route is Claude through Amazon Bedrock under your existing AWS agreement: Amazon doesn't share the data with the model provider or use it for training, and Legal adds no new vendor. Until Legal signs off, the AI stays switched off with one setting. Holds and matching keep working on rules, and drafts come from your own templates. When it's on, only ticket text and invoice facts are sent, never bank details. Taking your other answers: card re-runs become a proposal Priya approves one by one. Northgate goes to Dana as a decision today. Priya gets a short Slack morning digest that links to the queue. Disputes go to the account manager with a summary, and a hold is released only when the AM confirms it's settled.\n\n**Maya:** (awaiting reply)\n\n**What we changed because of it**\n1. AI is off by default (`use_claude: False` in `app/engine/rules.py`). With it off, holds and matching run on rules and drafts come from the policy templates.\n2. `LLM_PROVIDER=bedrock` routes Claude calls through Amazon Bedrock (`anthropic.AnthropicBedrock()` in `app/engine/llm.py`), so the data stays under Ledgerline's existing AWS agreement.\n3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details. (Still to verify in code: the prompts in `context.py` and `collections.py` must not include payment or bank fields.)\nEOF",
 "description": "Append exchanges 2 and 3 to Maya QA log"
}
```

### Tool · 2026-11-20 17:26:19 UTC
**Tool result:**
```
(Bash completed with no output)
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/MAYA_QA.md <<'EOF'\n\n### Exchange 2 — 11:26 CST, T+0:16\nSent by Claude Code at Jacek's standing instruction. The main thread revised Draft 2 before sending (see MAYA_OUTBOX.md).\n\n**Jacek:** Hi Maya, an update at T+0:15. The four agents now run end to end on the real records. Of the $633k overdue on the ledger, $83k is money we have already received but not applied, $312k is disputed in support tickets finance can't see (14 invoices, plus Eastman Engineering's chargeback threat), and about $238k is genuinely collectable. Most disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 22 wrong chases prevented, 27 reminders drafted for Priya to approve, 11 that need a person to write. Three questions: (1) 10 of the 16 failed card invoices belong to customers whose later card charges went through, and Northgate's $799 is written off automatically tomorrow. May the system re-run a failed charge on a card that works, or does Priya decide each one? (2) Does Priya work best from a morning queue in the tool or a Slack or email digest, and must the account manager approve before a hold is released? (3) Should disputed invoices go to the account manager automatically with the ticket text, or should finance own the fix with support?\n\n**Maya:** Those numbers are worth showing Dana today, especially the $312k sitting in \"solved\" tickets. On re-running cards, I'd want Priya to approve each one for now. Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes. Tell Dana about Northgate's $799 this morning so she can decide before it writes off.\n\nI believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool, but ask her directly because she'll be the one using it. For the disputes, I'd send them to the account manager with a summary, because the AMs own the relationship and are walking into renewal calls blind. Finance and support would still fix the billing error together, and the hold should only be released once the AM agrees the dispute is settled.\n\nYou're now pushing ticket text and customer financials through these agents. Which AI provider is doing that, and have you confirmed it doesn't train on our data? Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement.\n\n**What we changed because of it**\n1. **Card re-runs (D8):** the system never re-charges a card on its own. Where a customer's later card charges succeeded, it proposes a re-run, and Priya approves each one. Whether that ever becomes automatic is Dana's call.\n2. **Northgate $799:** goes to Dana today as a decision, before the 150-day automatic write-off.\n3. **Morning digest (D9):** Priya gets a short Slack-style morning digest that links to the queue, so she doesn't have to log into another tool. Still to confirm with Priya directly, as Maya said.\n4. **Disputes (D10):** routed to the account manager with a summary. Finance and support still fix the billing error together. A dispute hold is released only when the AM confirms it is settled.\n5. **Data and Legal (D11):** Maya's challenge led straight to Exchange 3. `rules.use_claude` now defaults to False, and `app/engine/llm.py` supports `LLM_PROVIDER=bedrock`.\n\n### Exchange 3 — ~11:28 CST, T+0:18\n**Jacek:** Good challenge, and nothing has gone to any AI provider yet. Everything you've seen so far is rules and matching on the records. The provider would be Claude from Anthropic. Under Anthropic's commercial terms, API inputs and outputs are not used to train models, and a DPA is available, but Legal should review it before any real data flows. Since Ledgerline already hosts on AWS, the cleaner route is Claude through Amazon Bedrock under your existing AWS agreement: Amazon doesn't share the data with the model provider or use it for training, and Legal adds no new vendor. Until Legal signs off, the AI stays switched off with one setting. Holds and matching keep working on rules, and drafts come from your own templates. When it's on, only ticket text and invoice facts are sent, never bank details. Taking your other answers: card re-runs become a proposal Priya approves one by one. Northgate goes to Dana as a decision today. Priya gets a short Slack morning digest that links to the queue. Disputes go to the account manager with a summary, and a hold is released only when the AM confirms it's settled.\n\n**Maya:** (awaiting reply)\n\n**What we changed because of it**\n1. AI is off by default (`use_claude: False` in `app/engine/rules.py`). With it off, holds and matching run on rules and drafts come from the policy templates.\n2. `LLM_PROVIDER=bedrock` routes Claude calls through Amazon Bedrock (`anthropic.AnthropicBedrock()` in `app/engine/llm.py`), so the data stays under Ledgerline's existing AWS agreement.\n3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details. (Still to verify in code: the prompts in `context.py` and `collections.py` must not include payment or bank fields.)\nEOF",
 "description": "Append exchanges 2 and 3 to Maya QA log"
}
```

### Claude · 2026-11-20 17:26:23 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"def claude_read\" -A30 app/engine/context.py | head -40; sed -n 65,90p app/engine/collections.py",
 "description": "Inspect what data goes into Claude prompts"
}
```

### Tool · 2026-11-20 17:26:23 UTC
**Tool result:**
```
61:def claude_read(t, own_invoices, customer_name, enabled):
62-    system = llm.manual("account_context") or "You read support tickets for a finance team."
63-    user = (
64-        "Customer: %s\nThis customer's open Ledgerline invoices: %s\nTicket %s (%s, category=%s, status=%s, priority=%s)\n"
65-        "Subject: %s\nBody:\n%s\n\nReturn JSON with keys: about_ledgerline_invoice (bool: is the customer disputing or questioning "
66-        "an invoice LEDGERLINE sent THEM, as opposed to asking about invoices they send their own clients in the product), "
67-        "invoice_ids (list of Ledgerline invoice ids it concerns, only from the list above), kind (one of dispute, cancellation, "
68-        "legal_threat, collections_complaint, payment_question, product_question, other), refuses_to_pay_until_fixed (bool), "
69-        "collections_complaint (bool), summary (<=25 words, plain English, for the AR specialist), confidence (0-1)."
70-    ) % (customer_name, ", ".join(own_invoices) or "none", t["ticket_id"], t["created_at"], t.get("category"), t.get("status"),
71-         t.get("priority"), t.get("subject"), str(t.get("body"))[:2500])
72-    r = llm.ask_json("ticket_read_v1", system, user, enabled=enabled)
73-    if not isinstance(r, dict):
74-        return None
75-    r["invoice_ids"] = [i for i in r.get("invoice_ids", []) if i in own_invoices]
76-    r["source"] = "claude"
77-    return r
78-
79-
80-def build(d, rules, customer_ids, cash_results):
81-    cus = d["customers"].set_index("customer_id")
82-    inv, tk, con, nps, use = d["invoices"], d["tickets"], d["contacts"], d["nps"], d["usage"]
83-    open_inv = inv[inv["status"].isin(("open", "overdue", "payment_failed"))]
84-    lookback = AS_OF - pd.Timedelta(days=int(rules.get("dispute_lookback_days", 120)))
85-    use_claude = bool(rules.get("use_claude", True))
86-    out, audit = {}, []
87-    for cid in sorted(set(customer_ids)):
88-        if cid not in cus.index:
89-            continue
90-        c = cus.loc[cid]
91-        own = list(open_inv[open_inv["customer_id"] == cid]["invoice_id"])
            "company": ctx["name"], "first": first, "dpd": inv["days_past_due"],
            "link": "https://pay.ledgerline.com/%s" % inv["invoice_id"]}
    d = {"to": [c["email"] for c in to[:2]], "cc": [am_email] if (am_email and rules.get("notify_am_before_contact", True)) else [],
         "subject": subj_t.format(**vals), "body": body_t.format(**vals), "template": stage_key, "source": "template"}


… [result truncated, 4084 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"def claude_read\" -A30 app/engine/context.py | head -40; sed -n 65,90p app/engine/collections.py",
 "description": "Inspect what data goes into Claude prompts"
}
```

### Claude · 2026-11-20 17:26:31 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && python3 - <<'EOF'\np=\"trail/MAYA_QA.md\"\ns=open(p).read()\nold=\"3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details. (Still to verify in code: the prompts in `context.py` and `collections.py` must not include payment or bank fields.)\"\nnew=\"\"\"3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details.\n   Checked by the test-steward at 11:30 against the code. No bank or payment fields go to Claude in either prompt. **But the drafting prompt (`app/engine/collections.py`) sends more than \"ticket text and invoice facts\":** customer name and plan, last NPS score, usage trend, renewal date and the contact's first name. The ticket prompt (`app/engine/context.py`) sends the customer name, the list of open invoice ids and up to 2,500 characters of ticket body. Either trim the drafting prompt or describe the scope accurately to Maya and Legal (\"ticket text, invoice facts and account context such as plan, NPS, usage trend and renewal date; never bank details\").\"\"\"\nassert old in s\nopen(p,\"w\").write(s.replace(old,new))\nEOF",
 "description": "Record data-scope verification result"
}
```

### Tool · 2026-11-20 17:26:31 UTC
**Tool result:**
```
Exit code 69
You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild -license' from within a Terminal window to review and agree to the Xcode and Apple SDKs license.
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && python3 - <<'EOF'\np=\"trail/MAYA_QA.md\"\ns=open(p).read()\nold=\"3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details. (Still to verify in code: the prompts in `context.py` and `collections.py` must not include payment or bank fields.)\"\nnew=\"\"\"3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details.\n   Checked by the test-steward at 11:30 against the code. No bank or payment fields go to Claude in either prompt. **But the drafting prompt (`app/engine/collections.py`) sends more than \"ticket text and invoice facts\":** customer name and plan, last NPS score, usage trend, renewal date and the contact's first name. The ticket prompt (`app/engine/context.py`) sends the customer name, the list of open invoice ids and up to 2,500 characters of ticket body. Either trim the drafting prompt or describe the scope accurately to Maya and Legal (\"ticket text, invoice facts and account context such as plan, NPS, usage trend and renewal date; never bank details\").\"\"\"\nassert old in s\nopen(p,\"w\").write(s.replace(old,new))\nEOF",
 "description": "Record data-scope verification result"
}
```

### Claude · 2026-11-20 17:26:36 UTC
**Tool call:** `Edit`
```json
{
 "replace_all": false,
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/MAYA_QA.md",
 "old_string": "3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details. (Still to verify in code: the prompts in `context.py` and `collections.py` must not include payment or bank fields.)",
 "new_string": "3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details.\n   The test-steward checked this against the code at 11:30. Neither prompt sends bank or payment fields. **But the drafting prompt (`app/engine/collections.py`) sends more than \"ticket text and invoice facts\":** the customer name and plan, last NPS score, usage trend, renewal date and the contact's first name. The ticket prompt (`app/engine/context.py`) sends the customer name, the open invoice ids and up to 2,500 characters of ticket body. Either trim the drafting prompt or describe the scope to Maya and Legal accurately (\"ticket text, invoice facts and account context such as plan, NPS, usage trend and renewal date; never bank details\")."
}
```

### Tool · 2026-11-20 17:26:37 UTC
**Tool result:**
```
The file /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/MAYA_QA.md has been updated successfully.
```

### Claude ·  UTC
**Tool call:** `Edit`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/MAYA_QA.md",
 "old_string": "3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details. (Still to verify in code: the prompts in `context.py` and `collections.py` must not include payment or bank fields.)",
 "new_string": "3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details.\n   The test-steward checked this against the code at 11:30. Neither prompt sends bank or payment fields. **But the drafting prompt (`app/engine/collections.py`) sends more than \"ticket text and invoice facts\":** the customer name and plan, last NPS score, usage trend, renewal date and the contact's first name. The ticket prompt (`app/engine/context.py`) sends the customer name, the open invoice ids and up to 2,500 characters of ticket body. Either trim the drafting prompt or describe the scope to Maya and Legal accurately (\"ticket text, invoice facts and account context such as plan, NPS, usage trend and renewal date; never bank details\")."
}
```

### Claude · 2026-11-20 17:27:03 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/MAYA_OUTBOX.md",
 "content": "# Maya outbox — drafts written by the test-steward, sent by the main thread\n\nMessages used: **3 of 60** (Exchange 3 sent ~11:28; Maya's reply not yet received)\n\n## Draft 1 — what we're building (SENT 11:14, T+0:04)\nSee MAYA_QA.md, exchange 1.\n\n## Draft 2 — first results on real records (SENT 11:26, T+0:16, revised by the main thread before sending)\nThe words actually sent are in MAYA_QA.md, exchange 2. The main thread revised this draft before sending it:\n- **Newer numbers.** Dispute detection was fixed between 11:23 and 11:26 to catch disputes in tickets tagged How-to or left untagged. Disputed went from $264k to $312k, collectable from $286k to $238k, chases prevented from 20 to 22, drafts for Priya from 28 to 27, needs-a-person from 12 to 11.\n- **Q1 swapped.** It asked about Dana's bank-fee write-off threshold. It was replaced with a question about re-running failed cards, because `analysis/FACTS.md` shows the real data has 0 bank-fee deductions and 0 short payments, so that question would have used up a message on a case that doesn't occur.\n- AM written out as \"account manager\".\n\nOriginal draft as written at 11:23 (kept for the record, NOT what was sent):\n\n> Hi Maya, the four agents now run end to end on real records. Of the $633k overdue on the ledger, $83k is money we already received, $264k is disputed in support, and about $286k is genuinely collectable. Many disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 20 wrong chases prevented, 28 reminders drafted for Priya to approve, 12 that need a person to write. Three questions: (1) What is Dana's write-off threshold for bank-fee short payments? Could you relay it or give your best guess? (2) Does Priya work best from a morning queue in the tool or a Slack/email digest, and must the AM approve before a hold is released? (3) Should disputed invoices go to the AM automatically with the ticket text, or should finance own the fix with support?\n\n## Draft 3 — AI provider and data (SENT ~11:28, T+0:18, written by the main thread)\nSee MAYA_QA.md, exchange 3.\n\n## Draft 4 — app live on Render (READY, drafted 11:30, T+0:20; send at the \"live on Render\" milestone)\nSingle line: paste as is, no line breaks. 110 words. Fill in the placeholders from the deployed app before sending. If Maya has already answered on Bedrock/Legal by then, drop the second question.\n\nHi Maya, the tool is live at {URL}. Sign in with your Scaleworks Google account. It opens on Priya's morning queue: {N_DRAFTS} reminders to approve, {N_HOLDS} holds with the reason for each, and {N_CARD} card re-runs waiting for her approval. The AI is switched off, so everything you see runs on rules and your templates. Two things worth trying: open Kingsway to see why both $5,100 invoices are held, and open Riverside Partners to see the \"solved\" ticket that blocks the chase. Two questions: could Priya spend ten minutes in it today and tell us what she would change, and has Legal said whether the Bedrock route works for them?\n\nBefore sending, check: (a) the SSO allowlist actually admits Maya's address (D5 restricts sign-in to scaleworks.com plus Jacek's emails); (b) the card re-run proposals and AM-confirmed hold release (D8, D10) are really in the deployed build, or else take them out of the message; (c) the numbers match the live dashboard, not this file.\n"
}
```

### Tool · 2026-11-20 17:27:03 UTC
**Tool result:**
```
The file /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/MAYA_OUTBOX.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/MAYA_OUTBOX.md",
 "content": "# Maya outbox — drafts written by the test-steward, sent by the main thread\n\nMessages used: **3 of 60** (Exchange 3 sent ~11:28; Maya's reply not yet received)\n\n## Draft 1 — what we're building (SENT 11:14, T+0:04)\nSee MAYA_QA.md, exchange 1.\n\n## Draft 2 — first results on real records (SENT 11:26, T+0:16, revised by the main thread before sending)\nThe words actually sent are in MAYA_QA.md, exchange 2. The main thread revised this draft before sending it:\n- **Newer numbers.** Dispute detection was fixed between 11:23 and 11:26 to catch disputes in tickets tagged How-to or left untagged. Disputed went from $264k to $312k, collectable from $286k to $238k, chases prevented from 20 to 22, drafts for Priya from 28 to 27, needs-a-person from 12 to 11.\n- **Q1 swapped.** It asked about Dana's bank-fee write-off threshold. It was replaced with a question about re-running failed cards, because `analysis/FACTS.md` shows the real data has 0 bank-fee deductions and 0 short payments, so that question would have used up a message on a case that doesn't occur.\n- AM written out as \"account manager\".\n\nOriginal draft as written at 11:23 (kept for the record, NOT what was sent):\n\n> Hi Maya, the four agents now run end to end on real records. Of the $633k overdue on the ledger, $83k is money we already received, $264k is disputed in support, and about $286k is genuinely collectable. Many disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 20 wrong chases prevented, 28 reminders drafted for Priya to approve, 12 that need a person to write. Three questions: (1) What is Dana's write-off threshold for bank-fee short payments? Could you relay it or give your best guess? (2) Does Priya work best from a morning queue in the tool or a Slack/email digest, and must the AM approve before a hold is released? (3) Should disputed invoices go to the AM automatically with the ticket text, or should finance own the fix with support?\n\n## Draft 3 — AI provider and data (SENT ~11:28, T+0:18, written by the main thread)\nSee MAYA_QA.md, exchange 3.\n\n## Draft 4 — app live on Render (READY, drafted 11:30, T+0:20; send at the \"live on Render\" milestone)\nSingle line: paste as is, no line breaks. 110 words. Fill in the placeholders from the deployed app before sending. If Maya has already answered on Bedrock/Legal by then, drop the second question.\n\nHi Maya, the tool is live at {URL}. Sign in with your Scaleworks Google account. It opens on Priya's morning queue: {N_DRAFTS} reminders to approve, {N_HOLDS} holds with the reason for each, and {N_CARD} card re-runs waiting for her approval. The AI is switched off, so everything you see runs on rules and your templates. Two things worth trying: open Kingsway to see why both $5,100 invoices are held, and open Riverside Partners to see the \"solved\" ticket that blocks the chase. Two questions: could Priya spend ten minutes in it today and tell us what she would change, and has Legal said whether the Bedrock route works for them?\n\nBefore sending, check: (a) the SSO allowlist actually admits Maya's address (D5 restricts sign-in to scaleworks.com plus Jacek's emails); (b) the card re-run proposals and AM-confirmed hold release (D8, D10) are really in the deployed build, or else take them out of the message; (c) the numbers match the live dashboard, not this file.\n"
}
```

### Claude · 2026-11-20 17:27:09 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"rerun\\|re-run\\|retry_card\\|digest\\|slack\\|am_confirm\\|release\" app --include=*.py | head -20; grep -rn -i \"how-to\\|how_to\\|untagged\" app/engine/*.py | head",
 "description": "Check whether D8-D10 exist in code"
}
```

### Tool · 2026-11-20 17:27:09 UTC
**Tool result:**
```
(eval):1: no matches found: --include=*.py
app/engine/context.py:43:        # whatever category the agent tagged (data shows disputes tagged How-to or untagged).
app/engine/context.py:99:                            "category": t["category"] if isinstance(t["category"], str) else "untagged",
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"rerun\\|re-run\\|retry_card\\|digest\\|slack\\|am_confirm\\|release\" app --include=*.py | head -20; grep -rn -i \"how-to\\|how_to\\|untagged\" app/engine/*.py | head",
 "description": "Check whether D8-D10 exist in code"
}
```

### Claude · 2026-11-20 17:27:12 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i -E \"rerun|re-run|retry|digest|slack|am_confirm|release\" app | grep -v llm_cache | head -20",
 "description": "Search app for D8-D10 implementation"
}
```

### Tool · 2026-11-20 17:27:12 UTC
**Tool result:**
```
app/store.py:1:"""Append-only store of human actions (approve, reject, edit, override_hold, release_hold, send, apply).
app/store.py:13:ACTIONS = ("approve", "reject", "edit", "override_hold", "release_hold", "send", "apply")
app/web/static/style.css:106:.b-human_writes, .b-release_hold { background: var(--purple-soft); color: var(--purple); }
app/web/views.py:34:    "HOLD": "Nothing goes out until a person releases or overrides the hold. Each hold says which agent raised it and why.",
app/web/views.py:147:    # An overridden/released hold becomes a writing job for a person until it is sent or rejected.
app/web/views.py:148:    return s["action"] in ("override_hold", "release_hold", "edit")
app/web/views.py:184:            if s and s["action"] in ("override_hold", "release_hold"):
app/web/views.py:458:        if kind not in ("override_hold", "release_hold"):
app/web/templates/base.html:23:    <form method="post" action="/run" class="inline"><button class="btn btn-run" title="Re-run all four agents on the data room">Run agents</button></form>
app/web/templates/_macros.html:17:  {% elif s.action == 'release_hold' %}Hold released by {{ s.user_email }}
app/web/templates/rules.html:5:<p class="lead">The thresholds the agents work to. Change them here, no engineer needed. Saving re-runs all four agents and shows what changed. Every change is logged.</p>
app/web/templates/rules.html:49:  <div class="btnrow"><button class="btn btn-primary">Save and re-run agents</button></div>
app/web/templates/_invoice.html:4:{% set lifted = s and s.action in ('override_hold', 'release_hold') %}
app/web/templates/_invoice.html:28:          <p class="small">Held: nothing will be drafted or sent. To lift it, type why. Use <b>Release</b> when the reason is resolved (e.g. the AM said go ahead) and <b>Override</b> when the agent got it wrong.</p>
app/web/templates/_invoice.html:31:            <button class="btn btn-secondary" name="kind" value="release_hold">Release hold</button>
app/engine/controller.py:3:Each hold has a code, a plain-English label and the detail Priya needs to decide whether to release it.
app/engine/llm.py:45:    key = hashlib.sha256((task + "\x00" + system + "\x00" + user).encode()).hexdigest()[:24]
app/engine/collections.py:80:            notes.append("since March 2026 the billing engine retries failed cards three times and emails the client after each retry, so they have probably had automated emails already")
app/engine/manuals/collections.md:15:  retry. Acknow
… [result truncated, 2544 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i -E \"rerun|re-run|retry|digest|slack|am_confirm|release\" app | grep -v llm_cache | head -20",
 "description": "Search app for D8-D10 implementation"
}
```

### Claude · 2026-11-20 17:27:27 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/JOURNAL.md <<'EOF'\n| 11:24 | T+0:14 | data-analyst | Finished profiling (`analysis/FACTS.md`). Dana's \"overdue has risen three quarters running\" is **false quarter on quarter**: a seasonal sawtooth of $221k, $494k, $209k, $600k. It is **true year on year**: +17%, +41%, +23%. At 31 Mar 2026, 43% of reported overdue ($210k) was cash already received but not applied. The real data has no bank fees, short payments, combined receipts or overpayments | Evidence for the one-pager and video. It also showed the bank-fee question in Draft 2 would have wasted a Maya message |\n| ~11:24–11:26 | T+0:14 | Claude Code | Fixed dispute detection to read tickets tagged How-to or left untagged, not just billing ones. The engine now finds the same 14 disputed invoices / $309k as the analyst, exactly. New headline: $83k already received, $312k disputed (14 invoices plus Eastman Engineering's chargeback threat), ~$238k genuinely collectable; 22 chases prevented, 27 drafts for Priya, 11 for a person to write | Two independent methods (engine rules and analyst's invoice-id scan) now agree. Before the fix the engine missed ~$45k of disputes |\n| 11:26 | T+0:16 | Claude Code for Jacek | Sent Maya Exchange 2: Draft 2 revised by the main thread (new numbers; bank-fee question replaced with failed-card re-runs) | Report first results and settle three design questions in one message |\n| ~11:27 | T+0:17 | Maya | Replied: Priya approves each card re-run, Dana owns any change. Tell Dana about Northgate's $799 today. Priya likely wants a Slack digest (ask her). Disputes go to the AM with a summary; release a hold only when the AM agrees. Then challenged us: which AI provider, does it train on our data, Legal needs a DPA | D8, D9, D10, D11 |\n| ~11:28 | T+0:18 | Jacek | Sent Maya Exchange 3: nothing has gone to an AI provider yet; Claude via Amazon Bedrock under the existing AWS agreement is preferred; AI off until Legal signs off; only ticket text and invoice facts sent, never bank details. Confirmed her other answers | Answer the data question honestly before it becomes a blocker |\n| ~11:28 | T+0:18 | Claude Code | Code changed: `use_claude` now defaults to False in `app/engine/rules.py`. `app/engine/llm.py` supports `LLM_PROVIDER=bedrock` (AnthropicBedrock client) | Make Exchange 3 true in the product, not just in the message |\n| 11:30 | T+0:20 | test-steward | Logged Exchanges 2 and 3 word for word, D8–D11, drafted Maya message 4. Checked the code: D8 (card re-run proposals), D9 (digest) and D10 (AM confirmation before release) are **decided but not built yet**. The drafting prompt also sends plan, NPS, usage trend and renewal date, which is more than \"ticket text and invoice facts\" | Keep the trail honest about the gap between what we told Maya and what the code does |\nEOF",
 "description": "Append journal rows"
}
```

### Tool · 2026-11-20 17:27:28 UTC
**Tool result:**
```
(Bash completed with no output)
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/JOURNAL.md <<'EOF'\n| 11:24 | T+0:14 | data-analyst | Finished profiling (`analysis/FACTS.md`). Dana's \"overdue has risen three quarters running\" is **false quarter on quarter**: a seasonal sawtooth of $221k, $494k, $209k, $600k. It is **true year on year**: +17%, +41%, +23%. At 31 Mar 2026, 43% of reported overdue ($210k) was cash already received but not applied. The real data has no bank fees, short payments, combined receipts or overpayments | Evidence for the one-pager and video. It also showed the bank-fee question in Draft 2 would have wasted a Maya message |\n| ~11:24–11:26 | T+0:14 | Claude Code | Fixed dispute detection to read tickets tagged How-to or left untagged, not just billing ones. The engine now finds the same 14 disputed invoices / $309k as the analyst, exactly. New headline: $83k already received, $312k disputed (14 invoices plus Eastman Engineering's chargeback threat), ~$238k genuinely collectable; 22 chases prevented, 27 drafts for Priya, 11 for a person to write | Two independent methods (engine rules and analyst's invoice-id scan) now agree. Before the fix the engine missed ~$45k of disputes |\n| 11:26 | T+0:16 | Claude Code for Jacek | Sent Maya Exchange 2: Draft 2 revised by the main thread (new numbers; bank-fee question replaced with failed-card re-runs) | Report first results and settle three design questions in one message |\n| ~11:27 | T+0:17 | Maya | Replied: Priya approves each card re-run, Dana owns any change. Tell Dana about Northgate's $799 today. Priya likely wants a Slack digest (ask her). Disputes go to the AM with a summary; release a hold only when the AM agrees. Then challenged us: which AI provider, does it train on our data, Legal needs a DPA | D8, D9, D10, D11 |\n| ~11:28 | T+0:18 | Jacek | Sent Maya Exchange 3: nothing has gone to an AI provider yet; Claude via Amazon Bedrock under the existing AWS agreement is preferred; AI off until Legal signs off; only ticket text and invoice facts sent, never bank details. Confirmed her other answers | Answer the data question honestly before it becomes a blocker |\n| ~11:28 | T+0:18 | Claude Code | Code changed: `use_claude` now defaults to False in `app/engine/rules.py`. `app/engine/llm.py` supports `LLM_PROVIDER=bedrock` (AnthropicBedrock client) | Make Exchange 3 true in the product, not just in the message |\n| 11:30 | T+0:20 | test-steward | Logged Exchanges 2 and 3 word for word, D8–D11, drafted Maya message 4. Checked the code: D8 (card re-run proposals), D9 (digest) and D10 (AM confirmation before release) are **decided but not built yet**. The drafting prompt also sends plan, NPS, usage trend and renewal date, which is more than \"ticket text and invoice facts\" | Keep the trail honest about the gap between what we told Maya and what the code does |\nEOF",
 "description": "Append journal rows"
}
```

### Claude · 2026-11-20 17:27:32 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 36,50p app/engine/context.py",
 "description": "Read dispute detection comment"
}
```

### Tool · 2026-11-20 17:27:33 UTC
**Tool result:**
```
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
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 36,50p app/engine/context.py",
 "description": "Read dispute detection comment"
}
```

### Claude · 2026-11-20 17:27:37 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -i '' 's/| Fixed dispute detection to read tickets tagged How-to or left untagged, not just billing ones\\. /| Fixed dispute detection: a ticket quoting one of the customer'\"'\"'s own open Ledgerline invoice ids now counts as a dispute whatever its category, so disputes tagged How-to or left untagged are caught (`app\\/engine\\/context.py`). /; s/Before the fix the engine missed ~\\$45k of disputes/Before the fix the engine counted $48k less as disputed ($264k vs $312k)/' trail/JOURNAL.md && grep -c \"own open Ledgerline invoice ids\" trail/JOURNAL.md; grep -c '\\$48k less' trail/JOURNAL.md",
 "description": "Correct dispute-fix journal wording"
}
```

### Tool · 2026-11-20 17:27:38 UTC
**Tool result:**
```
1
1
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -i '' 's/| Fixed dispute detection to read tickets tagged How-to or left untagged, not just billing ones\\. /| Fixed dispute detection: a ticket quoting one of the customer'\"'\"'s own open Ledgerline invoice ids now counts as a dispute whatever its category, so disputes tagged How-to or left untagged are caught (`app\\/engine\\/context.py`). /; s/Before the fix the engine missed ~\\$45k of disputes/Before the fix the engine counted $48k less as disputed ($264k vs $312k)/' trail/JOURNAL.md && grep -c \"own open Ledgerline invoice ids\" trail/JOURNAL.md; grep -c '\\$48k less' trail/JOURNAL.md",
 "description": "Correct dispute-fix journal wording"
}
```

### Claude · 2026-11-20 17:27:40 UTC
Now the DECISIONS entries.

### Claude · 2026-11-20 17:28:00 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/DECISIONS.md <<'EOF'\n\n## D8 — Failed-card re-runs: the system proposes, Priya approves each one (T+0:17)\n- Options: (a) re-run a failed charge automatically when the same customer's later card charges went through; (b) propose the re-run and have Priya approve each one; (c) leave failed cards out of scope.\n- Choice: (b). The Collections agent proposes a re-run, with the evidence that the card now works, and Priya approves or rejects each one. Making it automatic is Dana's call, not ours.\n- Why: Maya (Exchange 2): \"Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes.\" Charging money is customer-facing and hard to undo, so it stays with a person.\n- Evidence: 10 of the 16 failed-card invoices belong to customers whose later card charges succeeded (engine run, T+0:15). Northgate's $799 is written off automatically by policy at 150 days, tomorrow. That goes to Dana as a decision today, as Maya asked.\n- Status at 11:30: **decided, not built.** No re-run proposal exists in `app/` yet. The current build drafts a card-failed reminder and warns at 140 days (`card_writeoff_warning_days`).\n\n## D9 — Priya gets a short Slack-style morning digest that links to the queue (T+0:17)\n- Options: (a) Priya logs into the tool's morning queue; (b) a Slack or email digest that links to the queue.\n- Choice: (b), with the queue staying the place where she approves. The digest says how many drafts, holds, card re-runs and decisions are waiting, and links to each.\n- Why: Maya: \"I believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool.\" Maya's own success test is whether Priya is still using it in a month (Exchange 1), so we go to where Priya already works.\n- Open: Maya told us to ask Priya directly. Not yet asked. For the demo, the digest is a generated message (shown in the app or posted to a test webhook). No real Slack workspace is connected.\n- Status at 11:30: **decided, not built.**\n\n## D10 — Disputes go to the account manager; a dispute hold is released only on AM confirmation (T+0:17)\n- Options: (a) route disputed invoices to the AM automatically with the ticket summary; (b) finance owns the fix with support and the AM is just informed.\n- Choice: (a) for ownership of the customer conversation. Finance and support still fix the billing error together. A DISPUTE hold can only be released once the AM confirms it is settled, and the release records who confirmed.\n- Why: Maya: \"the AMs own the relationship and are walking into renewal calls blind.\" $312k of overdue is disputed, mostly in tickets marked \"solved\", so the AM is the one person who can confirm the customer actually agrees it is fixed.\n- Evidence: 14 disputed invoices / $309k, where engine and analyst agree exactly (T+0:14), plus Eastman Engineering's chargeback threat. 11 of the 14 have a \"solved\" ticket and an uncorrected invoice (`analysis/FACTS.md`).\n- Status at 11:30: **decided, not built.** Today any signed-in user can release a hold by typing a reason (`app/web/templates/_invoice.html`, `app/store.py`). The gate needs an \"AM confirmed\" field, or AM-only release for DISPUTE holds.\n\n## D11 — AI is off by default until Legal signs a DPA; Bedrock preferred; only ticket text and invoice facts sent (T+0:18)\n- Options: (a) call the Anthropic API directly now; (b) Anthropic API under Anthropic's commercial terms plus DPA, after Legal review; (c) Claude via Amazon Bedrock under Ledgerline's existing AWS agreement, after Legal sign-off; (d) no LLM at all.\n- Choice: (c) preferred, (b) as the alternative. Until Legal signs off, the AI is off: `use_claude` defaults to False. Holds and matching run on rules, and drafts come from the policy templates.\n- Why: Maya (Exchange 2): \"Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement.\" Ledgerline already hosts on AWS, so Bedrock adds no new vendor. Under Anthropic's commercial terms API data is not used for training, and Bedrock does not share data with the model provider. Both claims are as stated in Exchange 3; Legal still has to review.\n- What it costs: with the AI off, the ticket reading falls back to rules. That works on this data because the engine now matches the analyst's 14 disputes exactly, but phrasing the rules don't know will be missed. The \"reading\" job that justified the LLM (D6) only switches on after Legal approves. The demo must say this plainly.\n- Evidence: `app/engine/rules.py` (`\"use_claude\": False`), `app/engine/llm.py` (`LLM_PROVIDER=bedrock` uses `anthropic.AnthropicBedrock()`). The cache in D6 means demo runs with the AI on make no live calls.\n- Gap found at 11:30: the promise is \"only ticket text and invoice facts, never bank details\". No bank fields are sent. But the drafting prompt (`app/engine/collections.py`) also sends customer name, plan, last NPS, usage trend, renewal date and the contact's first name. Either trim it or describe the scope to Maya accurately. Small inconsistency too: `context.py` and `collections.py` still use `rules.get(\"use_claude\", True)` as a fallback. That is harmless while `load_rules()` merges the defaults, but should be `False`.\nEOF",
 "description": "Append decisions D8-D11"
}
```

### Tool · 2026-11-20 17:28:00 UTC
**Tool result:**
```
(Bash completed with no output)
```

### Claude ·  UTC
Now the DECISIONS entries.
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/DECISIONS.md <<'EOF'\n\n## D8 — Failed-card re-runs: the system proposes, Priya approves each one (T+0:17)\n- Options: (a) re-run a failed charge automatically when the same customer's later card charges went through; (b) propose the re-run and have Priya approve each one; (c) leave failed cards out of scope.\n- Choice: (b). The Collections agent proposes a re-run, with the evidence that the card now works, and Priya approves or rejects each one. Making it automatic is Dana's call, not ours.\n- Why: Maya (Exchange 2): \"Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes.\" Charging money is customer-facing and hard to undo, so it stays with a person.\n- Evidence: 10 of the 16 failed-card invoices belong to customers whose later card charges succeeded (engine run, T+0:15). Northgate's $799 is written off automatically by policy at 150 days, tomorrow. That goes to Dana as a decision today, as Maya asked.\n- Status at 11:30: **decided, not built.** No re-run proposal exists in `app/` yet. The current build drafts a card-failed reminder and warns at 140 days (`card_writeoff_warning_days`).\n\n## D9 — Priya gets a short Slack-style morning digest that links to the queue (T+0:17)\n- Options: (a) Priya logs into the tool's morning queue; (b) a Slack or email digest that links to the queue.\n- Choice: (b), with the queue staying the place where she approves. The digest says how many drafts, holds, card re-runs and decisions are waiting, and links to each.\n- Why: Maya: \"I believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool.\" Maya's own success test is whether Priya is still using it in a month (Exchange 1), so we go to where Priya already works.\n- Open: Maya told us to ask Priya directly. Not yet asked. For the demo, the digest is a generated message (shown in the app or posted to a test webhook). No real Slack workspace is connected.\n- Status at 11:30: **decided, not built.**\n\n## D10 — Disputes go to the account manager; a dispute hold is released only on AM confirmation (T+0:17)\n- Options: (a) route disputed invoices to the AM automatically with the ticket summary; (b) finance owns the fix with support and the AM is just informed.\n- Choice: (a) for ownership of the customer conversation. Finance and support still fix the billing error together. A DISPUTE hold can only be released once the AM confirms it is settled, and the release records who confirmed.\n- Why: Maya: \"the AMs own the relationship and are walking into renewal calls blind.\" $312k of overdue is disputed, mostly in tickets marked \"solved\", so the AM is the one person who can confirm the customer actually agrees it is fixed.\n- Evidence: 14 disputed invoices / $309k, where engine and analyst agree exactly (T+0:14), plus Eastman Engineering's chargeback threat. 11 of the 14 have a \"solved\" ticket and an uncorrected invoice (`analysis/FACTS.md`).\n- Status at 11:30: **decided, not built.** Today any signed-in user can release a hold by typing a reason (`app/web/templates/_invoice.html`, `app/store.py`). The gate needs an \"AM confirmed\" field, or AM-only release for DISPUTE holds.\n\n## D11 — AI is off by default until Legal signs a DPA; Bedrock preferred; only ticket text and invoice facts sent (T+0:18)\n- Options: (a) call the Anthropic API directly now; (b) Anthropic API under Anthropic's commercial terms plus DPA, after Legal review; (c) Claude via Amazon Bedrock under Ledgerline's existing AWS agreement, after Legal sign-off; (d) no LLM at all.\n- Choice: (c) preferred, (b) as the alternative. Until Legal signs off, the AI is off: `use_claude` defaults to False. Holds and matching run on rules, and drafts come from the policy templates.\n- Why: Maya (Exchange 2): \"Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement.\" Ledgerline already hosts on AWS, so Bedrock adds no new vendor. Under Anthropic's commercial terms API data is not used for training, and Bedrock does not share data with the model provider. Both claims are as stated in Exchange 3; Legal still has to review.\n- What it costs: with the AI off, the ticket reading falls back to rules. That works on this data because the engine now matches the analyst's 14 disputes exactly, but phrasing the rules don't know will be missed. The \"reading\" job that justified the LLM (D6) only switches on after Legal approves. The demo must say this plainly.\n- Evidence: `app/engine/rules.py` (`\"use_claude\": False`), `app/engine/llm.py` (`LLM_PROVIDER=bedrock` uses `anthropic.AnthropicBedrock()`). The cache in D6 means demo runs with the AI on make no live calls.\n- Gap found at 11:30: the promise is \"only ticket text and invoice facts, never bank details\". No bank fields are sent. But the drafting prompt (`app/engine/collections.py`) also sends customer name, plan, last NPS, usage trend, renewal date and the contact's first name. Either trim it or describe the scope to Maya accurately. Small inconsistency too: `context.py` and `collections.py` still use `rules.get(\"use_claude\", True)` as a fallback. That is harmless while `load_rules()` merges the defaults, but should be `False`.\nEOF",
 "description": "Append decisions D8-D11"
}
```

### Claude · 2026-11-20 17:28:08 UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "1. Updated: Exchanges 2 and 3 are logged word for word in `trail/MAYA_QA.md`, each with \"What we changed because of it\". Maya's reply to Exchange 3 is marked \"(awaiting reply)\". `trail/MAYA_OUTBOX.md` now shows Draft 2 as SENT, with your revision note and the original text kept, and the counter at 3 of 60. I added 7 rows to `trail/JOURNAL.md` covering 11:24 to 11:30: the analyst's findings, the dispute fix (now 14 invoices / $309k), Exchanges 2 and 3, and the `use_claude`/Bedrock code change. `trail/DECISIONS.md` has D8 to D11.\n\n2. At risk: we told Maya about things the code doesn't do yet. D8 card re-run proposals, the D9 digest and the D10 AM-confirmed hold release are decided but not built (today any signed-in user can release a hold). The \"only ticket text and invoice facts\" promise is also too narrow: the drafting prompt in `app/engine/collections.py` also sends plan, NPS, usage trend, renewal date and the contact's first name. No bank fields are sent. Small one: `context.py` and `collections.py` still fall back to `rules.get(\"use_claude\", True)`. The trail records all of this as gaps.\n\n3. Draft 4 is READY in `trail/MAYA_OUTBOX.md`: one line, 110 words, with {URL}, {N_DRAFTS}, {N_HOLDS} and {N_CARD} placeholders. Before sending, check that the SSO allowlist lets Maya in and that D8 and D10 are in the live build, or cut those lines. Folder: \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/\""
}
```

### Tool · 2026-11-20 17:28:08 UTC
**Tool result:**
```
{"success":true,"message":"Report delivered to your caller."}
```
