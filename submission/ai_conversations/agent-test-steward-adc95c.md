# Build agent: test-steward (one-pager + video script)

_Exported from the Claude Code session log. Redactions are explained in the index._

### Jacek · 2026-11-20 17:50:06 UTC
Project root (quote it): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a". Read docs/BRIEF.md (what Scaleworks asks), trail/* (journal, decisions, Maya Q&A), analysis/FACTS.md, EVAL.md, FAILURES.md, DISCREPANCIES.md, submission/LEGAL_NOTE.md and skim app/engine/*.py. Do NOT message Maya (Jacek put Maya on hold) and do not edit app code. Target 20 minutes.

Write:
1. submission/ONE_PAGER.md — HARD limit one printed page (~450–550 words). The RIG's /about page renders it. Sections exactly as the brief asks: **Which process** (FIN-1 Collections with FIN-2 Cash Application as its feeder — and why: Dana's quote, the board's #1 concern, the Paidly failure, finance can't see Zendesk); **What the tool does** (the 4-agent team in run order, the RIG; concrete numbers on the real records: $633k overdue on the ledger = $78k already received + $313k disputed (14 invoices, all matching contract; ≤$25k real exposure) + ~$242k collectable; 23 wrong chases prevented; 9 card re-runs; 2 Dana decisions; auto-apply 81/81 correct in evaluation, disputes 14/14); **What is AI and what stays with a person, and why** (rules vs Claude-when-Legal-allows vs a person — tie to Maya's words: one wrong chase or a threat to a top-50 gets it switched off; Priya must see why and fix it herself; over-holding is the right way to be wrong; AI off until DPA, Bedrock route); **Where it gets things wrong** (2–3 honest bullets: shortened payer names → over-holds; ticket reading 82% precision; invoices have no line items so contract checks can't see fees/tax); **What we'd do with more time** (AM dispute workflow with contract-evidence replies; Slack digest live; Bedrock + Claude ticket reading after DPA, measured against rules; FIN-7 cash forecast agent from the same data; FIN-6 renewal billing checks; 30-day override-rate review with Maya). Plain English, no hype, numbers verified against the analysis files (re-run `"<root>/.venv/bin/python" -c "from app.engine.pipeline import run_pipeline; import json; print(json.dumps(run_pipeline()['metrics'], default=str))"` from <root> to confirm metrics and use those).
2. submission/VIDEO_SCRIPT.md — Loom walkthrough, 7–9 minutes, with timestamps and screen cues on the RIG URL https://ledgerline-finance-rig.onrender.com (tabs: Home, Team, Architecture, Documentation, Activity, Maya, Direct the team, Build log, One pager, Demo; ops pages Today, Cash, Collections, Customers, Digest, Audit, Rules; "Talk to the team" chat). Must include: what we chose and why (30s), the system diagram (who does what), live walkthrough on real records — Kingsway paid-but-overdue, Riverside "solved" ticket dispute with contract check, a card re-run, Northgate decision for Dana, approving one draft, overriding a hold with a reason; directing the team (chat: "why is Riverside held?", "set writeoff_threshold to 50" → Apply; a "from now on…" instruction accepted into the manual); where it gets things wrong (BRANDT shortened payer replay, complaint counter 14→1, Reyes false positive fixed); the Maya channel; what's next. Write it as Jacek's spoken talk track (first person), concise.
3. Update trail/SUBMISSION_CHECKLIST.md statuses and append a JOURNAL row.
Report back in 4 lines with the one-pager word count.

### Jacek · 2026-11-20 17:50:06 UTC
[harness system note omitted]

### Jacek ·  UTC
[harness system note omitted]

Project root (quote it): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a". Read docs/BRIEF.md (what Scaleworks asks), trail/* (journal, decisions, Maya Q&A), analysis/FACTS.md, EVAL.md, FAILURES.md, DISCREPANCIES.md, submission/LEGAL_NOTE.md and skim app/engine/*.py. Do NOT message Maya (Jacek put Maya on hold) and do not edit app code. Target 20 minutes.

Write:
1. submission/ONE_PAGER.md — HARD limit one printed page (~450–550 words). The RIG's /about page renders it. Sections exactly as the brief asks: **Which process** (FIN-1 Collections with FIN-2 Cash Application as its feeder — and why: Dana's quote, the board's #1 concern, the Paidly failure, finance can't see Zendesk); **What the tool does** (the 4-agent team in run order, the RIG; concrete numbers on the real records: $633k overdue on the ledger = $78k already received + $313k disputed (14 invoices, all matching contract; ≤$25k real exposure) + ~$242k collectable; 23 wrong chases prevented; 9 card re-runs; 2 Dana decisions; auto-apply 81/81 correct in evaluation, disputes 14/14); **What is AI and what stays with a person, and why** (rules vs Claude-when-Legal-allows vs a person — tie to Maya's words: one wrong chase or a threat to a top-50 gets it switched off; Priya must see why and fix it herself; over-holding is the right way to be wrong; AI off until DPA, Bedrock route); **Where it gets things wrong** (2–3 honest bullets: shortened payer names → over-holds; ticket reading 82% precision; invoices have no line items so contract checks can't see fees/tax); **What we'd do with more time** (AM dispute workflow with contract-evidence replies; Slack digest live; Bedrock + Claude ticket reading after DPA, measured against rules; FIN-7 cash forecast agent from the same data; FIN-6 renewal billing checks; 30-day override-rate review with Maya). Plain English, no hype, numbers verified against the analysis files (re-run `"<root>/.venv/bin/python" -c "from app.engine.pipeline import run_pipeline; import json; print(json.dumps(run_pipeline()['metrics'], default=str))"` from <root> to confirm metrics and use those).
2. submission/VIDEO_SCRIPT.md — Loom walkthrough, 7–9 minutes, with timestamps and screen cues on the RIG URL https://ledgerline-finance-rig.onrender.com (tabs: Home, Team, Architecture, Documentation, Activity, Maya, Direct the team, Build log, One pager, Demo; ops pages Today, Cash, Collections, Customers, Digest, Audit, Rules; "Talk to the team" chat). Must include: what we chose and why (30s), the system diagram (who does what), live walkthrough on real records — Kingsway paid-but-overdue, Riverside "solved" ticket dispute with contract check, a card re-run, Northgate decision for Dana, approving one draft, overriding a hold with a reason; directing the team (chat: "why is Riverside held?", "set writeoff_threshold to 50" → Apply; a "from now on…" instruction accepted into the manual); where it gets things wrong (BRANDT shortened payer replay, complaint counter 14→1, Reyes false positive fixed); the Maya channel; what's next. Write it as Jacek's spoken talk track (first person), concise.
3. Update trail/SUBMISSION_CHECKLIST.md statuses and append a JOURNAL row.
Report back in 4 lines with the one-pager word count.

[harness system note omitted]

### Claude · 2026-11-20 17:50:10 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls docs trail analysis submission app/engine && wc -w docs/BRIEF.md trail/* analysis/*.md submission/*.md && date",
 "description": "List project files and sizes"
}
```

### Claude · 2026-11-20 17:50:11 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"from app.engine.pipeline import run_pipeline; import json; print(json.dumps(run_pipeline()['metrics'], default=str, indent=1))\"",
 "description": "Run pipeline to get current metrics"
}
```

### Tool · 2026-11-20 17:50:11 UTC
**Tool result:**
```
analysis:
DISCREPANCIES.md
EVAL.md
FACTS.md
FAILURES.md
SCHEMA.md
scripts
testset_cash_app.csv
work

app/engine:
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

docs:
BRIEF.md
PLAN.md

submission:
LEGAL_NOTE.md

trail:
DECISIONS.md
JOURNAL.md
MAYA_OUTBOX.md
MAYA_QA.md
SUBMISSION_CHECKLIST.md
     609 docs/BRIEF.md
    2499 trail/DECISIONS.md
    2291 trail/JOURNAL.md
    1051 trail/MAYA_OUTBOX.md
    2725 trail/MAYA_QA.md
     281 trail/SUBMISSION_CHECKLIST.md
    1835 analysis/DISCREPANCIES.md
    2556 analysis/EVAL.md
    2869 analysis/FACTS.md
    2855 analysis/FAILURES.md
    1351 analysis/SCHEMA.md
     494 submission/LEGAL_NOTE.md
   21416 total
Fri Nov 20 11:50:11 CST 2026
```

### Tool · 2026-11-20 17:50:12 UTC
**Tool result:**
```
{
 "overdue_balance": 633245.0,
 "overdue_count": 54,
 "overdue_already_paid": 78348.0,
 "overdue_disputed": 312922.0,
 "overdue_collectable": 241975.0,
 "open_ar": 1430632.0,
 "cash_found": 87335.0,
 "unapplied_total": 87335.0,
 "chases_prevented": 23,
 "auto_applied": 3,
 "needs_review": 4,
 "held": 21,
 "drafts": 20,
 "human_writes": 10,
 "collections_complaints": 0,
 "collections_complaints_baseline": 2,
 "collections_complaints_baseline_ids": [
  "T880019",
  "T880519"
 ],
 "complaint_keyword_hits": 14,
 "card_retries": 9,
 "dana_decisions": 3
}
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls docs trail analysis submission app/engine && wc -w docs/BRIEF.md trail/* analysis/*.md submission/*.md && date",
 "description": "List project files and sizes"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"from app.engine.pipeline import run_pipeline; import json; print(json.dumps(run_pipeline()['metrics'], default=str, indent=1))\"",
 "description": "Run pipeline to get current metrics"
}
```

### Claude · 2026-11-20 17:50:16 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat docs/BRIEF.md trail/SUBMISSION_CHECKLIST.md trail/JOURNAL.md",
 "description": "Read brief, checklist, journal"
}
```

### Tool · 2026-11-20 17:50:16 UTC
**Tool result:**
```
# Captured brief (read 2026-11-20, pre-start)

## Scaleworks — Ledgerline AI Operator Challenge (apply.scaleworks.com/start)
- Fictional company **Ledgerline**: $8.5m ARR (+6%/yr), 396 customers (professional services firms), $22k ACV,
  46 staff, about break-even. Data as of 2026-10-31.
- **Maya Lindqvist (COO, played by Scaleworks AI)**: "Pick one. Build something that would change how it gets done."
  A person at Scaleworks reads everything and makes every decision.
- Personas: **Dana Ruiz, VP Finance** (overdue invoices up 3 quarters running), Tom Okafor, VP Marketing (demo replies
  take a day), Sam Whitfield, Head of Support (incidents run a week before anyone connects them), Renata Kowalczyk,
  Head of Sales (forecast = judgment on stale data).
- 24 hours from pressing "Begin day one". Any tools.
  Suggested shape: hour 1 read, hour 2 choose and ask Maya, most of it build, last hour record and hand in.
- **Hand in:** the tool (live link or repo, a deck alone is a no), a 5–10 minute demo video, a one-page description,
  and every AI conversation (dead ends included) plus the repo.
- **Judged on:** a tool that changes the job (still used a month later), judgment (what AI should and shouldn't do,
  when it hands over to a person), evidence (works on real records, shows where it gets things wrong).
- Contact before starting: ai@apply.scaleworks.com.

## Finance processes (7 of the 31)
- **FIN-1 Collections and payment reminders**: late, inconsistent reminders. Finance can't see support tickets, so
  customers with open complaints get chased. Failed card payments are rarely followed up.
- **FIN-2 Cash application**: matching lags 3–5 days. Invoices look unpaid when the money has arrived, so customers
  get chased for invoices they already paid.
- FIN-3 Month-end close: takes 8 days, commentary written from scratch, variances explained from memory.
- FIN-4 Board KPI pack: pulled by hand from 4 systems, definitions drift.
- FIN-5 Vendor bills and SaaS spend: nobody owns it, renewals noticed after they've gone through.
- FIN-6 Renewal invoicing and billing changes: wrong seats, prices and contacts lead to disputes.
- FIN-7 Revenue and cash forecast: churn and collections assumptions are guesses.
(Other areas: Sales 6, Marketing 5, CS 5, Support 5, Ops 3. Full list in the data room's processes.md.)

## Data room (51 files, Jan 2023 → 2026-10-31, opens on Begin)
Finance: invoices (6,062), payments (5,808, unmatched = no invoice id), ar_aging (117), pnl_monthl
… [result truncated, 19621 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat docs/BRIEF.md trail/SUBMISSION_CHECKLIST.md trail/JOURNAL.md",
 "description": "Read brief, checklist, journal"
}
```

### Claude · 2026-11-20 17:50:22 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat trail/MAYA_QA.md trail/DECISIONS.md",
 "description": "Read Maya QA and decisions"
}
```

### Tool · 2026-11-20 17:50:22 UTC
**Tool result:**
```
<persisted-output>
Output too large (30.7KB). Full output saved to: /Users/jacekmaterna/.claude/projects/-Users-jacekmaterna-Library-Application-Support-Claude-scratch-workspaces-e69441d8-02c7-4ae1-82fa-e65f61df0516-362a2cee-265f-40fd-99ca-8b843a81ad27-scratch-2026-11-20-a3ea2a/603a7d18-df39-4b28-94b6-4623216101e2/tool-results/bep6f2wz4.txt

Preview (first 2KB):
# Maya Q&A (log word for word: "What you ask is part of what we read")

Messages used: **5 of 60** (target: 12 or fewer). The count of 5 comes from the main thread at 11:42. Only 4 messages from Jacek are logged below, so one message is unaccounted for. Check it against the counter on the challenge page.
Rule since T+0:25 (Jacek): write to Maya only for a **Confirmation** (a decision she or Dana owns) or **Intel** (facts the data room can't give). Never a pure status update.

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
...
</persisted-output>
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat trail/MAYA_QA.md trail/DECISIONS.md",
 "description": "Read Maya QA and decisions"
}
```

### Claude · 2026-11-20 17:50:25 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"^## \\|^### \\|^\\*\\*Maya\\|^> \" trail/MAYA_QA.md | head -80",
 "description": "Outline Maya QA headings and quotes"
}
```

### Tool · 2026-11-20 17:50:25 UTC
**Tool result:**
```
6:## Prepared questions (refine after the data-room read, ask in hour 2)
27:## Log
30:### Exchange 1 — 11:14 CST, T+0:04
33:**Maya:** Hi, Maya here. I am around all day, so ask whenever something comes up. What are you thinking of building?
37:**Maya:** Hi Jacek. Paidly chased a long-standing customer who had already paid by wire, because the money took days to be matched, and nobody had tested that case before it went live. That, along with the reminder sequence the CEO personally shut down after a customer complained to him, is what would get this switched off: one wrong chase or one message that reads like a threat to a top-50 account. Dana would also drop it if Priya can't see why it held or drafted something and fix it herself, because Priya is the one who has to run it.
50:### Exchange 2 — 11:26 CST, T+0:16
55:**Maya:** Those numbers are worth showing Dana today, especially the $312k sitting in "solved" tickets. On re-running cards, I'd want Priya to approve each one for now. Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes. Tell Dana about Northgate's $799 this morning so she can decide before it writes off.
68:### Exchange 3 — ~11:28 CST, T+0:18
73:**Maya:** That's the answer I needed. Bedrock under the AWS agreement we already have is the route I'd rather take to Legal, but they'll want to confirm our current terms actually cover Bedrock before I'd call it "no new vendor." Send me a short note naming the service, the region, and exactly which fields leave our systems, and I'll put it in front of them this week. I also like that the rules-only version works without the AI switched on, because that could be in front of Priya on Monday while Legal reviews. Before then, tell me what it got wrong on the real records. I'd rather hear about the misses from you than from a customer.
84:### Exchange 4 — ~11:42 CST, T+0:32
89:**Maya:** Yes, Monday with the rules-only version, as long as Priya approves every match, release and email, and Dana has seen the Northgate decision and the auto-apply threshold before then. Over-holding is the right way to be wrong. Reyes costs Priya a minute, but a BRANDT-style chase would cost us a customer, so track how often she overrides a hold and bring me that number in a month. Fill in the actual AWS region in the note, and expect Legal to point out that ticket text can still name people even with emails and ph
… [result truncated, 2619 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"^## \\|^### \\|^\\*\\*Maya\\|^> \" trail/MAYA_QA.md | head -80",
 "description": "Outline Maya QA headings and quotes"
}
```

### Claude · 2026-11-20 17:50:30 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 27,120p trail/MAYA_QA.md | grep -v \"^$\" | cut -c1-600; grep -n \"^## \\|^### \" trail/DECISIONS.md",
 "description": "Read Maya log and decision headings"
}
```

### Tool · 2026-11-20 17:50:30 UTC
**Tool result:**
```
## Log
Budget: Maya allows 60 messages. Bundle questions. Running count at the top of this file and in MAYA_OUTBOX.md.
### Exchange 1 — 11:14 CST, T+0:04
Maya opened the chat before Jacek wrote.
**Maya:** Hi, Maya here. I am around all day, so ask whenever something comes up. What are you thinking of building?
**Jacek:** Hi Maya, Jacek here. I'm taking on cash collection for Dana: Collections (FIN-1) together with Cash Application (FIN-2). From the policy and process maps they look like one problem. Customers get chased for invoices whose money has already arrived but isn't applied yet, and get chased while they have an open complaint because finance can't see Zendesk. I'm building a small team of AI agents, each owning one job. One matches unapplied bank receipts to invoices. One pulls each customer's tickets, usage, contract and renewal into one view. One drafts the right reminder under your colle
**Maya:** Hi Jacek. Paidly chased a long-standing customer who had already paid by wire, because the money took days to be matched, and nobody had tested that case before it went live. That, along with the reminder sequence the CEO personally shut down after a customer complained to him, is what would get this switched off: one wrong chase or one message that reads like a threat to a top-50 account. Dana would also drop it if Priya can't see why it held or drafted something and fix it herself, because Priya is the one who has to run it.
On the number, I believe Dana would look at the overdue balance first and treat complaints about collections as the veto, though she'd confirm. What I'll be checking is whether Priya is still using it in a month.
On autonomy, my understanding is that applying exact matches on amount and invoice reference is close to what the team already does without thinking twice, so Dana may be comfortable with that. Write-offs, partial matches and anything that goes to a customer would go through Dana or Priya. Dana sets the threshold, so ask her before you build that in.
**What we changed because of it**
1. Cash Application runs **before** Collections on every cycle. Any unapplied receipt that plausibly covers an invoice is a hard block on chasing it (the Paidly failure becomes test case #1).
2. No threatening language anywhere. The 45-day "FINAL NOTICE: suspension" template is retired; the Controller blocks suspension/legal wording outright. Top-50 accounts always go to a person.
3. **Priya is the primary user.** Every hold or draft shows 
… [result truncated, 12677 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 27,120p trail/MAYA_QA.md | grep -v \"^$\" | cut -c1-600; grep -n \"^## \\|^### \" trail/DECISIONS.md",
 "description": "Read Maya log and decision headings"
}
```

### Claude · 2026-11-20 17:50:33 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat analysis/EVAL.md; sed -n 1,200p analysis/FAILURES.md",
 "description": "Read eval and failures"
}
```

### Tool · 2026-11-20 17:50:33 UTC
**Tool result:**
```
# EVAL: how well the agents work on the real records

QA Evaluator. Run on 2026-11-20 at 11:36 CST against the code as it stood then. The builder was still editing:
`context.py` and `data.py` changed during the run, so the numbers were re-run at 11:36. Data as of 2026-10-31.
Nothing in `app/` or `data/` was changed. The scripts are re-runnable:

| script | what it does | output |
|---|---|---|
| `analysis/scripts/eval_cash_app.py` | replays the 286 test payments against the invoice book as it stood on each received date | `analysis/work/eval_cash_app_results.csv`, `.log` |
| `analysis/scripts/eval_controller.py` | checks dispute detection against the analyst's list, and reads all 1,041 tickets | `analysis/work/eval_ticket_reads.csv`, `eval_ticket_sample_*.csv`, `.log` |
| `analysis/scripts/eval_guardrails.py` | red-teams the real pipeline using changed copies of the data held in memory | `analysis/work/eval_guardrails_results.csv`, `.log` |

**Headline**
- **0 wrong automatic applications in 81** (real data).
- Proposals put the right invoice first 98.0% of the time (real data).
- The Controller held all 14 of the analyst's disputed invoices (recall 100%).
- **44 of 54 guardrail checks pass.** The 10 failures fall into three gaps:
  - a receipt whose customer cannot be identified blocks nothing (the Paidly case returns);
  - complaint wording outside the keyword lists gets through;
  - the banned-phrase list is narrow.

---

## 1. Cash Application (test set `analysis/testset_cash_app.csv`, 286 rows)

**Harness.** For each test payment, the invoice book is rebuilt as it stood on the receipt date. An invoice counts as
open if `issue_date <= received_date` and (`paid_date` is blank or `paid_date >= received_date`). The payment is
then fed in as the only unapplied receipt, and the **production `cash_app.run()` is called unchanged** with
DEFAULT_RULES, so no rule is re-implemented. An answer counts as correct when the proposed invoice set equals the
label. For PAY-65805 (Kingsway), which is ambiguous, either invoice is accepted.

### Real rows (246)
| difficulty | n | auto-applied | auto precision | proposed | proposal top-1 | exception | exception rate | end-to-end correct |
|---|---|---|---|---|---|---|---|---|
| trivial (card) | 20 | 20 | **100%** | 0 | n/a | 0 | 0% | 100% |
| easy (memo ref) | 63 | 61 | **100%** | 2 | 100% | 0 | 0% | 100% |
| medium (no ref, unique amount) | 83 | 0 | n/a | 83 | 100% | 0 | 0% | 100% |
| hard (same-amount ties / truncated pay
… [result truncated, 29825 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat analysis/EVAL.md; sed -n 1,200p analysis/FAILURES.md",
 "description": "Read eval and failures"
}
```

### Claude · 2026-11-20 17:50:40 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 1,80p analysis/DISCREPANCIES.md; grep -n \"^#\\|line item\" analysis/FACTS.md | head -40; sed -n 1,40p submission/LEGAL_NOTE.md",
 "description": "Read discrepancies, facts outline, legal note"
}
```

### Tool · 2026-11-20 17:50:40 UTC
**Tool result:**
```
# DISCREPANCIES — finance review before handover (as of 2026-10-31)

Scripts: `analysis/scripts/discrepancies.py`, `analysis/scripts/disp_verify.py`. Per-check CSVs are in `analysis/work/check1..5_*.csv`.
**F** = fact computed from the data. **I** = inference. `data/` and `app/` were not touched.

## Headline
The ledger is internally consistent. Every invoice in the data room (6,062 of 6,062) equals the amount derived from its contract term. AR ties to the balance sheet to the dollar in all 46 months.

The open question is not "is our arithmetic wrong" but **"what did the customer see on the invoice document?"** invoices.csv has one amount per invoice, with no line items, no tax and no discounts. None of the disputed extra lines (fees, VAT, late fee, module) exist in the ledger amount. So the evidence finance can send each customer is the contract row and the invoice amount, and an account manager confirms anything verbal.

## 1. The 14 disputes (+ Reyes) — `work/check1_disputes_verdicts.csv`
Method (F): for each invoice I took the contract term covering issue_date. Expected amount = contract arr × service_period_months / 12, where arr = seats × price × 12 + platform fee (this formula holds on all 1,757 contract rows). I then checked customers.csv, usage_monthly.csv (seats, active users, modules) and pricing_and_packaging.md.

**F: all 15 invoices equal their contract amount exactly.** Credit due according to the data: **$0 on every invoice.**

| invoice | customer | $ | claim | verdict | exposure if customer proves it (I) |
|---|---|---|---|---|---|
| INV-25787 | Riverside Partners | 60,576 | 62 seats vs 38 people | **We're right on the invoice**: it bills 46 seats, not 62. **Can't tell** whether the 39→46 expansion at the 08-27 renewal came from the merge. Usage shows 38 active users in Oct, 43 in Sep. | $7,392 (7 seats) to $8,448 (down to 38) |
| INV-25712 | Wexler & Hume | 4,080 | billed 24 users, have 17 | **We're right**: the invoice is for 20 seats, not 24. They renewed at 20 on 08-10, and seat reductions are allowed at renewal only. | $816/quarter if cut to 17 |
| INV-25730 | Westbrook Eng. (top-50) | 47,904 | implementation fee should have been waived | **We're right**: 34×88×12 + 12,000 = 47,904 exactly. The customer has no implementation invoice, the fee applies to new customers only (they have been a customer since 2022), and multi-year deals are not offered. | $0 |
| INV-25765 | Okafor & Nakamura (top-50) | 46,848 | 50% off 3 months for second
… [result truncated, 13201 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -n 1,80p analysis/DISCREPANCIES.md; grep -n \"^#\\|line item\" analysis/FACTS.md | head -40; sed -n 1,40p submission/LEGAL_NOTE.md",
 "description": "Read discrepancies, facts outline, legal note"
}
```

### Claude · 2026-11-20 17:50:46 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline; import json\nr=run_pipeline()\nprint(list(r.keys()))\nfor k,v in r.items():\n    if k!='metrics': print(k, type(v), (len(v) if hasattr(v,'__len__') else ''))\nprint(json.dumps(r.get('dana_decisions', r.get('decisions')), default=str, indent=1)[:3000])\n\" 2>&1 | head -80",
 "description": "Inspect pipeline output structure"
}
```

### Tool · 2026-11-20 17:50:48 UTC
**Tool result:**
```
['as_of', 'metrics', 'payments', 'invoices', 'customers', 'audit', 'rules']
as_of <class 'str'> 10
payments <class 'list'> 7
invoices <class 'list'> 117
customers <class 'dict'> 107
audit <class 'list'> 141
rules <class 'dict'> 14
null
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline; import json\nr=run_pipeline()\nprint(list(r.keys()))\nfor k,v in r.items():\n    if k!='metrics': print(k, type(v), (len(v) if hasattr(v,'__len__') else ''))\nprint(json.dumps(r.get('dana_decisions', r.get('decisions')), default=str, indent=1)[:3000])\n\" 2>&1 | head -80",
 "description": "Inspect pipeline output structure"
}
```

### Claude · 2026-11-20 17:50:53 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline; import json, collections\nr=run_pipeline()\ninv=r['invoices']\nprint(json.dumps(inv[0], default=str, indent=1)[:2500])\nprint(collections.Counter(i.get('action') for i in inv))\n\" 2>&1 | head -120; grep -n \"dana_decisions\\|card_retries\" app/engine/pipeline.py",
 "description": "Inspect invoice record and action counts"
}
```

### Tool · 2026-11-20 17:50:54 UTC
**Tool result:**
```
{
 "invoice_id": "INV-26019",
 "customer_id": "C1080",
 "customer_name": "Birch Media",
 "amount": 78528.0,
 "issue_date": "2026-10-19",
 "due_date": "2026-11-18",
 "days_past_due": 0,
 "ar_status": "open",
 "bucket": "Not yet due",
 "plan": "Enterprise",
 "stage": "wait",
 "action": "HUMAN_WRITES",
 "holds": [
  {
   "code": "TOP50",
   "label": "Top-50 account (#4 by ARR)",
   "detail": "Policy: nothing goes to a top-50 account without a person reading it first. The draft is a starting point only.",
   "agent": "Controller"
  }
 ],
 "draft": null,
 "retry": null,
 "top50": true,
 "account_manager": "Nadia Upton",
 "reasons": [
  "Top-50 account (#4 by ARR)"
 ]
}
Counter({'NO_ACTION': 57, 'HOLD': 21, 'DRAFT_REMINDER': 20, 'HUMAN_WRITES': 10, 'RETRY_CARD': 9})
168:        "card_retries": sum(1 for i in invoices if i["action"] == "RETRY_CARD"),
169:        "dana_decisions": sum(1 for i in invoices if any(h.get("route_to", "").startswith("Dana") for h in i["holds"])),
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline; import json, collections\nr=run_pipeline()\ninv=r['invoices']\nprint(json.dumps(inv[0], default=str, indent=1)[:2500])\nprint(collections.Counter(i.get('action') for i in inv))\n\" 2>&1 | head -120; grep -n \"dana_decisions\\|card_retries\" app/engine/pipeline.py",
 "description": "Inspect invoice record and action counts"
}
```

### Claude · 2026-11-20 17:51:00 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline; import json\nr=run_pipeline()\nfor i in r['invoices']:\n    n=i['customer_name']\n    if any(h.get('route_to','').startswith('Dana') for h in i['holds']) or any(x in n for x in ['Kingsway','Riverside','Reyes','Northgate']) or i['action']=='RETRY_CARD':\n        print(i['invoice_id'],n,i['amount'],i['days_past_due'],i['action'],[(h['code'],h['label'],h.get('route_to')) for h in i['holds']])\n        if 'Riverside' in n: print(json.dumps(i['holds'],indent=1,default=str)[:2500])\n\"",
 "description": "Show key demo records from pipeline"
}
```

### Tool · 2026-11-20 17:51:02 UTC
**Tool result:**
```
INV-25787 Riverside Partners 60576.0 35 HOLD [('DISPUTE', 'Invoice disputed in support', 'Nadia Upton'), ('TOP50', 'Top-50 account (#23 by ARR)', None)]
[
 {
  "code": "DISPUTE",
  "label": "Invoice disputed in support",
  "detail": "T880886 (2026-10-12): Users double counted after workspace merge. The ticket is marked 'solved' but the customer said they won't pay until it is fixed. Account manager decides when to resume (policy).",
  "agent": "Account Context",
  "contract_check": {
   "matches": true,
   "expected": 60576.0,
   "text": "Invoice matches the contract on file: 46 seats x $88/seat/month + $12,000 platform fee (Enterprise plan, term 2026-08-27 to 2027-08-26), 12-month billing = $60,576.00. If the claim rests on something outside the contract (a verbal discount, tax status, a plan change), the AM has to confirm it; otherwise reply with this evidence."
  },
  "route_to": "Nadia Upton",
  "release_requires": "Account manager confirms the dispute is settled (Maya, T+0:17)"
 },
 {
  "code": "TOP50",
  "label": "Top-50 account (#23 by ARR)",
  "detail": "Policy: nothing goes to a top-50 account without a person reading it first. The draft is a starting point only.",
  "agent": "Controller"
 }
]
INV-26009 Reyes Consulting 51072.0 0 HUMAN_WRITES [('TOP50', 'Top-50 account (#34 by ARR)', None)]
INV-25885 Riverside Consulting Group 17136.0 12 DRAFT_REMINDER []
[]
INV-25852 Kingsway Engineering Group 5100.0 19 HOLD [('MONEY_RECEIVED', 'Money already received, not applied yet', None), ('RENEWAL_SOON', 'Renewal in 42 days (2026-12-12)', None)]
INV-25469 Kingsway Engineering Group 5100.0 111 HOLD [('MONEY_RECEIVED', 'Money already received, not applied yet', None), ('ESCALATE_90', '90+ days overdue', None), ('RENEWAL_SOON', 'Renewal in 42 days (2026-12-12)', None)]
INV-25999 Northgate Partners 4080.0 0 NO_ACTION []
INV-25973 Eastman Engineering 3264.0 23 HUMAN_WRITES [('LEGAL_RISK', 'Legal or chargeback threat in support', None), ('WRITEOFF_OVER_LIMIT', "Auto write-off would exceed Dana's $2,000 limit", 'Dana Ruiz (VP Finance)')]
INV-25803 Glover Engineering 1836.0 59 RETRY_CARD []
INV-25708 Quill, Mott & Co 1632.0 83 RETRY_CARD []
INV-25793 Ashgrove Partners 1088.0 64 RETRY_CARD []
INV-25433 Northgate Creative 799.0 149 RETRY_CARD [('ESCALATE_90', '90+ days overdue', None), ('CARD_WRITEOFF_SOON', 'Decision for Dana today: Automatic card write-off in 1 days', 'Dana Ruiz (VP Finance)'), ('RENEWAL_SOON', 'Renewal in 4 days (2026-11-04)', None)]
INV-25912 Ell
… [result truncated, 3073 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline; import json\nr=run_pipeline()\nfor i in r['invoices']:\n    n=i['customer_name']\n    if any(h.get('route_to','').startswith('Dana') for h in i['holds']) or any(x in n for x in ['Kingsway','Riverside','Reyes','Northgate']) or i['action']=='RETRY_CARD':\n        print(i['invoice_id'],n,i['amount'],i['days_past_due'],i['action'],[(h['code'],h['label'],h.get('route_to')) for h in i['holds']])\n        if 'Riverside' in n: print(json.dumps(i['holds'],indent=1,default=str)[:2500])\n\"",
 "description": "Show key demo records from pipeline"
}
```

### Claude · 2026-11-20 17:51:08 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls app app/* | head -50; grep -rhoE \"@(app|router)\\.(get|post)\\(\\\"[^\\\"]+\\\"\" app | sort | uniq | head -60; ls submission; ls -la trail",
 "description": "List app routes and files"
}
```

### Tool · 2026-11-20 17:51:08 UTC
**Tool result:**
```
app/__init__.py
app/auth.py
app/main.py
app/store.py

app:
__init__.py
auth.py
engine
main.py
store.py
web

app/engine:
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

app/web:
__init__.py
chat.py
fake_state.py
rig.py
rig_data.py
state.py
static
templates
views.py
@app.get("/healthz"
@router.get("/auth/callback"
@router.get("/login"
@router.get("/login/google"
@router.get("/logout"
LEGAL_NOTE.md
total 120
drwxr-xr-x@  7 jacekmaterna  staff    224 Nov 20 11:47 .
drwx------@ 18 jacekmaterna  staff    576 Nov 20 11:50 ..
-rw-r--r--@  1 jacekmaterna  staff  15170 Nov 20 11:46 DECISIONS.md
-rw-r--r--@  1 jacekmaterna  staff  13879 Nov 20 11:46 JOURNAL.md
-rw-r--r--@  1 jacekmaterna  staff   6256 Nov 20 11:46 MAYA_OUTBOX.md
-rw-r--r--@  1 jacekmaterna  staff  16217 Nov 20 11:46 MAYA_QA.md
-rw-r--r--@  1 jacekmaterna  staff   1634 Nov 20 11:47 SUBMISSION_CHECKLIST.md
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls app app/* | head -50; grep -rhoE \"@(app|router)\\.(get|post)\\(\\\"[^\\\"]+\\\"\" app | sort | uniq | head -60; ls submission; ls -la trail",
 "description": "List app routes and files"
}
```

### Claude · 2026-11-20 17:51:14 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web\" && grep -hoE \"\\.(get|post)\\(\\s*\\\"[^\\\"]+\\\"\" *.py | sort -u; ls templates; ls ../engine/manuals; grep -n \"from now on\\|apply\\|set_rule\\|writeoff_threshold\" chat.py | head -30",
 "description": "List web routes, templates, chat features"
}
```

### Tool · 2026-11-20 17:51:15 UTC
**Tool result:**
```
.get("/"
.get("/about"
.get("/activity"
.get("/agents/{slug}"
.get("/architecture"
.get("/audit"
.get("/audit.csv"
.get("/buildlog"
.get("/cash"
.get("/collections"
.get("/customers"
.get("/customers/{cid}"
.get("/digest"
.get("/direct"
.get("/maya"
.get("/rules"
.get("/team"
.get("/today"
.get("ANTHROPIC_API_KEY"
.get("BASE_URL"
.get("DEMO_VIDEO_URL"
.get("HX-Request"
.get("HX-Target"
.get("MANUALS_DIR"
.get("RIG_CHAT_AI"
.get("RULES_PATH"
.get("account_manager"
.get("agent"
.get("amount_tolerance"
.get("as_of"
.get("audit"
.get("auto_applied"
.get("auto_apply_exact_ref_match"
.get("banned_phrases"
.get("billing_complaint"
.get("body"
.get("cancellation"
.get("card_retries"
.get("cash_found"
.get("cc"
.get("chases_prevented"
.get("code"
.get("collections_complaints"
.get("confidence"
.get("contacts"
.get("courtesy"
.get("current_arr"
.get("customer_id"
.get("customer_name"
.get("customers"
.get("dana_decisions"
.get("days_past_due"
.get("decision"
.get("detail"
.get("difference"
.get("dispute"
.get("draft"
.get("drafts"
.get("email"
.get("escalate"
.get("evidence"
.get("final"
.get("first"
.get("flags"
.get("held"
.get("holds"
.get("human_writes"
.get("issue"
.get("label"
.get("legal_threat"
.get("message"
.get("method"
.get("metrics"
.get("mode"
.get("name"
.get("needs_review"
.get("note"
.get("object_id"
.get("object_type"
.get("open_invoices"
.get("open_tickets"
.get("overdue_already_paid"
.get("overdue_balance"
.get("overdue_collectable"
.get("overdue_count"
.get("overdue_disputed"
.get("payer_name"
.get("payload"
.get("plan"
.get("priority"
.get("rank"
.get("reason"
.get("reasons"
.get("referer"
.get("release_requires"
.get("reminder_days"
.get("renewal_date"
.get("reply"
.get("retry"
.get("route_to"
.get("rule"
.get("rules"
.get("second"
.get("seconds"
.get("source"
.get("stage"
.get("subject"
.get("template"
.get("ticket_id"
.get("to"
.get("top50_human_only"
.get("ts"
.get("use_claude"
.get("value"
.get("verified"
.get("writeoff_threshold"
.post("/agents/{slug}/manual"
.post("/api/chat"
.post("/api/rules/apply"
.post("/cash/{pid}/approve"
.post("/cash/{pid}/reject"
.post("/cash/{pid}/undo"
.post("/collections/{iid}/card_retry"
.post("/collections/{iid}/hold"
.post("/collections/{iid}/reject"
.post("/collections/{iid}/send"
.post("/direct/instructions"
.post("/direct/instructions/{iid}/{decision}"
.post("/rules"
.post("/run"
_chat.html
_customer_rows.html
_instr.html
_invoice.html
_macros.html
_payment.html
_thumbs.html
about.html
audit.html
base.ht
… [result truncated, 3714 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/app/web\" && grep -hoE \"\\.(get|post)\\(\\s*\\\"[^\\\"]+\\\"\" *.py | sort -u; ls templates; ls ../engine/manuals; grep -n \"from now on\\|apply\\|set_rule\\|writeoff_threshold\" chat.py | head -30",
 "description": "List web routes, templates, chat features"
}
```

### Claude · 2026-11-20 17:51:21 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rln \"BRANDT\\|Reyes\\|14 → 1\\|14→1\" app/web | head; grep -rn \"BRANDT\" app/web/*.py app/web/templates/*.html | head -8; grep -n \"override\" app/web/templates/_invoice.html app/web/views.py | head -10; sed -n 320,345p app/web/chat.py",
 "description": "Find failure gallery and override UI in web"
}
```

### Tool · 2026-11-20 17:51:22 UTC
**Tool result:**
```
app/web/fake_state.py
app/web/rig_data.py
app/web/fake_state.py:159:    ("PAY-65766", "2026-10-19", 6324.00, "ach", "BRANDT & LOWELL CPAS", "Ledgerline subscription", "C1126", "PROPOSE", ["INV-25806"], 0.88,
app/web/templates/_invoice.html:4:{% set lifted = s and s.action in ('override_hold', 'release_hold') %}
app/web/templates/_invoice.html:51:            <button class="btn btn-danger" name="kind" value="override_hold">Override hold</button>
app/web/views.py:37:    "HOLD": "Nothing goes out until a person releases or overrides the hold. Each hold says which agent raised it and why.",
app/web/views.py:158:    return s["action"] in ("override_hold", "release_hold", "edit")
app/web/views.py:196:            if s and s["action"] in ("override_hold", "release_hold"):
app/web/views.py:525:    async def inv_hold(request: Request, iid: str, reason: str = Form(""), kind: str = Form("override_hold"),
app/web/views.py:528:        if kind not in ("override_hold", "release_hold"):
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
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rln \"BRANDT\\|Reyes\\|14 → 1\\|14→1\" app/web | head; grep -rn \"BRANDT\" app/web/*.py app/web/templates/*.html | head -8; grep -n \"override\" app/web/templates/_invoice.html app/web/views.py | head -10; sed -n 320,345p app/web/chat.py",
 "description": "Find failure gallery and override UI in web"
}
```

### Claude · 2026-11-20 17:51:27 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"BRANDT\\|Reyes\\|complaint\" app/web/rig_data.py | head -15; grep -n \"slug\\\"\\s*:\" app/web/rig_data.py | head; grep -n \"Demo\\|One pager\\|nav\" app/web/templates/base.html | head -20",
 "description": "Locate failure content and nav in RIG"
}
```

### Tool · 2026-11-20 17:51:28 UTC
**Tool result:**
```
86:            "open support complaint, because finance can't see support tickets.",
105:    (False, "30-minute walkthrough with Priya (why Reyes was held; how to override or release a hold)"),
19:        "slug": "cash", "name": "Cash Application", "manual": "cash_application", "step": 1,
31:        "slug": "context", "name": "Account Context", "manual": "account_context", "step": 2,
41:        "slug": "controller", "name": "Controller", "manual": "controller", "step": 3,
51:        "slug": "collections", "name": "Collections", "manual": "collections", "step": 4,
45:<nav class="tabs">
47:  {% set rig_tabs = [('/', 'Home'), ('/team', 'Team'), ('/architecture', 'Architecture'), ('/activity', 'Activity'), ('/maya', 'Maya'), ('/direct', 'Direct the team'), ('/buildlog', 'Build log'), ('/about', 'One pager')] %}
54:</nav>
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -n \"BRANDT\\|Reyes\\|complaint\" app/web/rig_data.py | head -15; grep -n \"slug\\\"\\s*:\" app/web/rig_data.py | head; grep -n \"Demo\\|One pager\\|nav\" app/web/templates/base.html | head -20",
 "description": "Locate failure content and nav in RIG"
}
```

### Claude · 2026-11-20 17:51:36 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls analysis/scripts; time .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -iE \"brandt|jessop|kingsway|PASS|FAIL\" | head -20",
 "description": "Re-run guardrail eval to confirm BRANDT fix",
 "timeout": 180000
}
```

### Tool · 2026-11-20 17:51:46 UTC
**Tool result:**
```
discrepancies.py
disp_verify.py
disputes.py
eval_cash_app.py
eval_controller.py
eval_guardrails.py
explore.py
extra.py
facts.py
joins.py
schema.py
testset.py
tk_read.py
[PASS] 1 Paidly baseline INV-25469 :: INV-25469 Kingsway Engineering Group $5,100 111dpd -> HOLD holds=['MONEY_RECEIVED', 'ESCALATE_90', 'RENEWAL_SOON'] to=None
[PASS] 1 Paidly baseline INV-25852 :: INV-25852 Kingsway Engineering Group $5,100 19dpd -> HOLD holds=['MONEY_RECEIVED', 'RENEWAL_SOON'] to=None
[PASS] 1 Paidly baseline INV-25784 :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HOLD holds=['MONEY_RECEIVED', 'TOP50'] to=None
[PASS] 1 Paidly baseline INV-25806 :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> HOLD holds=['MONEY_RECEIVED'] to=None
[PASS] 1 Paidly baseline INV-25845 :: INV-25845 Castellano, Crane & Co $3,672 20dpd -> NO_ACTION holds=['PAID', 'RENEWAL_SOON'] to=None
[PASS] 1 Paidly baseline INV-25867 :: INV-25867 Yardley & Duarte Advisory $564 16dpd -> NO_ACTION holds=['PAID'] to=None
[PASS] 1b Paidly abbreviated payer 'BRANDT' (PAY-65766) :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> HOLD holds=['MONEY_RECEIVED'] to=None | cash agent: EXCEPTION cust=None inv=[] (Payer name 'BRANDT' is not a clear match for any one customer: Studio Brandt (0.55))
[PASS] 1b Paidly abbreviated payer 'JESSOP' (PAY-65750) :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HOLD holds=['MONEY_RECEIVED', 'TOP50'] to=None | cash agent: EXCEPTION cust=None inv=[] (Payer name 'JESSOP' is not a clear match for any one customer: Jessop Legal (0.57))
[PASS] 1b Paidly abbreviated payer 'KINGSWAY' (PAY-65805) :: INV-25469 Kingsway Engineering Group $5,100 111dpd -> HOLD holds=['MONEY_RECEIVED', 'ESCALATE_90', 'RENEWAL_SOON'] to=None | cash agent: EXCEPTION cust=None inv=[] (Payer name 'KINGSWAY' is not a clear match for any one customer: Kingsway Digital (0.57), Kingsway Creative (0)
[PASS] 1b Paidly abbreviated payer 'JESSOP ORWELL' (PAY-65750) :: INV-25784 Jessop & Orwell Agency $62,688 36dpd -> HOLD holds=['MONEY_RECEIVED', 'TOP50'] to=None | cash agent: PROPOSE cust=C1273 inv=['INV-25784'] (Payer name 'JESSOP ORWELL' is not a clear match for any one customer: Jessop & Orwell Agency (0.68))
[PASS] 1b Paidly abbreviated payer 'BRANDT LOWELL' (PAY-65766) :: INV-25806 Brandt & Lowell CPAs $6,324 28dpd -> HOLD holds=['MONEY_RECEIVED'] to=None | cash agent: PROPOSE cust=C1126 inv=['INV-25806'] (Payer name 'BRANDT LOWELL' is not a clear match for any one customer: Brandt & Lowell CPAs (0.70))
[
… [result truncated, 3828 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls analysis/scripts; time .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -iE \"brandt|jessop|kingsway|PASS|FAIL\" | head -20",
 "description": "Re-run guardrail eval to confirm BRANDT fix",
 "timeout": 180000
}
```

### Claude · 2026-11-20 17:51:52 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -E \"^\\[FAIL\\]|TOTAL|pass|PASS [0-9]\" | tail -15; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -c \"^\\[PASS\\]\"; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -c \"^\\[FAIL\\]\"",
 "description": "Count current guardrail pass and fail results",
 "timeout": 180000
}
```

### Tool · 2026-11-20 17:52:23 UTC
**Tool result:**
```
[FAIL] 2d refusal but tagged How-to :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> DRAFT_REMINDER holds=[] to=['nadia.vance@thornfieldconsultinggr.example']
[FAIL] 2f untagged, 'refuse to pay' :: INV-25862 Thornfield Consulting Group $39,456 17dpd -> DRAFT_REMINDER holds=[] to=['nadia.vance@thornfieldconsultinggr.example']
[FAIL] 8 failed card INV-25769 (card works=True) :: INV-25769 Drummond Consulting $658 68dpd -> HUMAN_WRITES holds=['LEGAL_RISK'] to=None
51
3
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -E \"^\\[FAIL\\]|TOTAL|pass|PASS [0-9]\" | tail -15; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -c \"^\\[PASS\\]\"; .venv/bin/python analysis/scripts/eval_guardrails.py 2>&1 | grep -c \"^\\[FAIL\\]\"",
 "description": "Count current guardrail pass and fail results",
 "timeout": 180000
}
```

### Claude · 2026-11-20 17:52:33 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"board\" analysis/FACTS.md trail/DECISIONS.md docs/PLAN.md | head -12; grep -i -n \"concern\\|cash\\|collect\" data/*board* 2>/dev/null | head; ls data | head -60",
 "description": "Find board concern evidence"
}
```

### Tool · 2026-11-20 17:52:33 UTC
**Tool result:**
```
trail/DECISIONS.md:17:- Why: the brief says "Pick one", "one thing working well than five things sketched". Dana's quote and the board's
analysis/FACTS.md:41:- **I** The board's line "overdue rose for three quarters" is defensible only as a year-on-year statement. A sequential chart would show a sawtooth. Cash-application lag inflates the quarter-end number.
(eval):1: no matches found: data/*board*
README.md
customers
docs
finance
marketing
people
product
sales
support
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"board\" analysis/FACTS.md trail/DECISIONS.md docs/PLAN.md | head -12; grep -i -n \"concern\\|cash\\|collect\" data/*board* 2>/dev/null | head; ls data | head -60",
 "description": "Find board concern evidence"
}
```

### Claude · 2026-11-20 17:52:38 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls data/docs; grep -n -i \"overdue\\|collect\\|concern\\|risk\\|cash\" data/docs/board_update_2026_q3.md | head -20; grep -rn -i \"dana\" data/docs/*.md data/people/* 2>/dev/null | grep -i \"\\\"\" | head -8",
 "description": "Read board update concerns and Dana quotes"
}
```

### Tool · 2026-11-20 17:52:39 UTC
**Tool result:**
```
billing_engine_rewrite_2026.md
board_update_2026_q3.md
collections_policy.md
company_overview.md
icp.md
org_chart.md
pricing_and_packaging.md
process_maps.md
processes.md
sales_playbook.md
sla_policy.md
templates
tool_stack.md
7:Growth stayed slow and the business stayed at break-even. ARR ended the quarter at $8,465,928. New business was $157,308 against churn of $129,504. Collections worsened again and are now the main risk to cash. Support response times are slipping as volume grows with a flat team.
21:| Cash | $2,979,195 |
25:1. **Cash collection.** Overdue receivables have risen for three quarters. Two people handle collections part-time, and one goes on leave in March.
data/people/employees.csv:11:E110,Priya Nair,AR Specialist,Finance,Dana Ruiz,2019-03-08,,"Remote, US",66000
data/people/employees.csv:23:E122,Dana Ruiz,VP Finance,Finance,Alan Brandt,2020-08-10,,"Austin, TX",165000
data/people/employees.csv:26:E125,Marcus Bell,Staff Accountant,Finance,Dana Ruiz,2021-04-02,,"Austin, TX",76000
data/people/employees.csv:42:E141,Ravi Quill,FP&A Analyst,Finance,Dana Ruiz,2024-03-04,,"Austin, TX",88000
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && ls data/docs; grep -n -i \"overdue\\|collect\\|concern\\|risk\\|cash\" data/docs/board_update_2026_q3.md | head -20; grep -rn -i \"dana\" data/docs/*.md data/people/* 2>/dev/null | grep -i \"\\\"\" | head -8",
 "description": "Read board update concerns and Dana quotes"
}
```

### Claude · 2026-11-20 17:52:43 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"dana\" data/docs/*.md data/README.md docs/PLAN.md | head -15; sed -n 20,30p data/docs/board_update_2026_q3.md",
 "description": "Search for Dana quote"
}
```

### Tool · 2026-11-20 17:52:44 UTC
**Tool result:**
```
data/docs/org_chart.md:13:- Dana Ruiz, VP Finance
docs/PLAN.md:6:An AI **Order-to-Cash team** for Dana Ruiz (VP Finance): several agents that each own one job,
docs/PLAN.md:12:- Dana: "Overdue invoices have risen three quarters running." Maya: "cash collection is slipping."
| EBITDA | $113,351 |
| Cash | $2,979,195 |

## What we are worried about

1. **Cash collection.** Overdue receivables have risen for three quarters. Two people handle collections part-time, and one goes on leave in March.
2. **Small-firm churn.** We keep losing the smallest customers within a year or two of signing them.
3. **Speed to lead.** We still take most of a day to answer a demo request.
4. **Support load.** Volume is up, the team is the same size, and we missed the Enterprise response commitment several times this quarter.
5. **Reporting.** This pack took four people most of a week to assemble.
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep -rn -i \"dana\" data/docs/*.md data/README.md docs/PLAN.md | head -15; sed -n 20,30p data/docs/board_update_2026_q3.md",
 "description": "Search for Dana quote"
}
```

### Claude · 2026-11-20 17:53:06 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/ONE_PAGER.md",
 "content": "# Ledgerline Order-to-Cash team: one page\n\n**Live:** https://ledgerline-finance-rig.onrender.com · Data as of 2026-10-31 · Jacek Materna\n\n## Which process\n**FIN-1 Collections, with FIN-2 Cash Application as its feeder.** Dana says overdue invoices have risen three quarters running (true year on year: +17%, +41%, +23%), and cash collection is the board's #1 worry. Paidly was switched off in 2025 after chasing a customer whose wire had already arrived. Finance can't see Zendesk, so customers with open complaints get chased too. Collections only works if cash application runs first.\n\n## What the tool does\nFour agents run in order on every cycle, each with a manual that people can edit:\n1. **Cash Application** matches unapplied receipts to invoices.\n2. **Account Context** reads each customer's tickets, contract, contacts and renewal date.\n3. **Controller** holds anything that must not be chased and explains why.\n4. **Collections** drafts the policy reminder, or proposes a card re-run.\n\nPriya works in the RIG. She approves, edits or overrides each item, and every click goes to an audit log.\n\nOn the real records, the $633k overdue across 54 invoices breaks down as:\n- **$78k already received** but not yet applied.\n- **$313k disputed in support.** 14 invoices, most on tickets marked \"solved\". Every one equals its contract amount, so real exposure is at most about $25k.\n- **About $242k actually collectable.**\n\nThe tool stops 23 wrong chases and drafts 20 reminders for approval. It sends 10 to a person to write, proposes 9 card re-runs and raises 3 decisions for Dana. In testing on past receipts, automatic matches were 81 of 81 correct, and it held all 14 disputes.\n\n## What is AI and what stays with a person, and why\nMaya named the two things that would get it switched off: one wrong chase, or a message that reads like a threat to a top-50 account. She also said Priya must see why the tool acted and be able to fix it herself. So:\n- **Rules:** payment matching, holds, contact and look-alike domain checks, banned phrases and templates. These run the same way every time and Priya can edit every rule.\n- **Claude, once Legal allows:** reading ticket text (is this a dispute of our invoice, or a question about the customer's own invoicing?) and rewording drafts. It stays **off until Legal signs off on the data terms**, then runs through Amazon Bedrock under the existing AWS agreement. The rules-only version goes to Priya on Monday.\n- **A person:** every customer email, card charge, proposed match and hold release. Account managers release dispute holds. Dana makes write-off and threshold calls. People write for top-50 and 90+ day accounts. When unsure, it holds. In Maya's words: \"Over-holding is the right way to be wrong.\"\n\n## Where it gets things wrong\n- **Shortened payer names** (\"BRANDT\") used to break the never-chase-paid rule. We fixed it by holding every invoice of the same amount. That over-holds, and Priya clears the extras.\n- **Ticket reading is 82% precise** (18 of 22). Reyes Consulting's \"do I void it?\" was about its own client, and it held a $51k invoice. Some refusals in tickets tagged How-to still get through.\n- **Invoices have no line items**, so the contract check can't see disputed fees or tax. Five disputes need an account manager or tax decision.\n\n## What we'd do with more time\n- A dispute workflow for account managers, with a reply that quotes the contract evidence.\n- Turn on the Slack morning digest for Priya.\n- Turn on Claude ticket reading through Bedrock after Legal signs off, and measure it against the rules.\n- A FIN-7 cash forecast agent built on the same data, and FIN-6 renewal billing checks.\n- Review the hold-override rate with Maya after 30 days.\n"
}
```

### Claude · 2026-11-20 17:53:09 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && wc -w submission/ONE_PAGER.md",
 "description": "Count one-pager words"
}
```

### Tool · 2026-11-20 17:53:09 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/ONE_PAGER.md (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:53:09 UTC
**Tool result:**
```
     626 submission/ONE_PAGER.md
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/ONE_PAGER.md",
 "content": "# Ledgerline Order-to-Cash team: one page\n\n**Live:** https://ledgerline-finance-rig.onrender.com · Data as of 2026-10-31 · Jacek Materna\n\n## Which process\n**FIN-1 Collections, with FIN-2 Cash Application as its feeder.** Dana says overdue invoices have risen three quarters running (true year on year: +17%, +41%, +23%), and cash collection is the board's #1 worry. Paidly was switched off in 2025 after chasing a customer whose wire had already arrived. Finance can't see Zendesk, so customers with open complaints get chased too. Collections only works if cash application runs first.\n\n## What the tool does\nFour agents run in order on every cycle, each with a manual that people can edit:\n1. **Cash Application** matches unapplied receipts to invoices.\n2. **Account Context** reads each customer's tickets, contract, contacts and renewal date.\n3. **Controller** holds anything that must not be chased and explains why.\n4. **Collections** drafts the policy reminder, or proposes a card re-run.\n\nPriya works in the RIG. She approves, edits or overrides each item, and every click goes to an audit log.\n\nOn the real records, the $633k overdue across 54 invoices breaks down as:\n- **$78k already received** but not yet applied.\n- **$313k disputed in support.** 14 invoices, most on tickets marked \"solved\". Every one equals its contract amount, so real exposure is at most about $25k.\n- **About $242k actually collectable.**\n\nThe tool stops 23 wrong chases and drafts 20 reminders for approval. It sends 10 to a person to write, proposes 9 card re-runs and raises 3 decisions for Dana. In testing on past receipts, automatic matches were 81 of 81 correct, and it held all 14 disputes.\n\n## What is AI and what stays with a person, and why\nMaya named the two things that would get it switched off: one wrong chase, or a message that reads like a threat to a top-50 account. She also said Priya must see why the tool acted and be able to fix it herself. So:\n- **Rules:** payment matching, holds, contact and look-alike domain checks, banned phrases and templates. These run the same way every time and Priya can edit every rule.\n- **Claude, once Legal allows:** reading ticket text (is this a dispute of our invoice, or a question about the customer's own invoicing?) and rewording drafts. It stays **off until Legal signs off on the data terms**, then runs through Amazon Bedrock under the existing AWS agreement. The rules-only version goes to Priya on Monday.\n- **A person:** every customer email, card charge, proposed match and hold release. Account managers release dispute holds. Dana makes write-off and threshold calls. People write for top-50 and 90+ day accounts. When unsure, it holds. In Maya's words: \"Over-holding is the right way to be wrong.\"\n\n## Where it gets things wrong\n- **Shortened payer names** (\"BRANDT\") used to break the never-chase-paid rule. We fixed it by holding every invoice of the same amount. That over-holds, and Priya clears the extras.\n- **Ticket reading is 82% precise** (18 of 22). Reyes Consulting's \"do I void it?\" was about its own client, and it held a $51k invoice. Some refusals in tickets tagged How-to still get through.\n- **Invoices have no line items**, so the contract check can't see disputed fees or tax. Five disputes need an account manager or tax decision.\n\n## What we'd do with more time\n- A dispute workflow for account managers, with a reply that quotes the contract evidence.\n- Turn on the Slack morning digest for Priya.\n- Turn on Claude ticket reading through Bedrock after Legal signs off, and measure it against the rules.\n- A FIN-7 cash forecast agent built on the same data, and FIN-6 renewal billing checks.\n- Review the hold-override rate with Maya after 30 days.\n"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && wc -w submission/ONE_PAGER.md",
 "description": "Count one-pager words"
}
```

### Claude · 2026-11-20 17:53:24 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/ONE_PAGER.md",
 "content": "# Ledgerline Order-to-Cash team: one page\n\n**Live:** https://ledgerline-finance-rig.onrender.com · Data as of 2026-10-31\n\n## Which process\n**FIN-1 Collections, with FIN-2 Cash Application as its feeder.** Dana says overdue invoices have risen three quarters running (true year on year), and cash collection is the board's #1 worry. Paidly was switched off in 2025 after chasing a customer whose wire had already arrived. Finance can't see Zendesk, so customers with open complaints get chased too. Collections only works if cash application runs first.\n\n## What the tool does\nFour agents run in order, each with a manual people can edit:\n1. **Cash Application** matches unapplied receipts.\n2. **Account Context** reads tickets, contract, contacts and renewal.\n3. **Controller** holds anything that must not be chased, and says why.\n4. **Collections** drafts the reminder or proposes a card re-run.\n\nPriya works in the RIG. She approves, edits or overrides each item, and every click is logged.\n\nOn the real records, $633k overdue across 54 invoices breaks down as:\n- **$78k already received**, not yet applied.\n- **$313k disputed in support**: 14 invoices, most on tickets marked \"solved\". All 14 equal their contract amount, so real exposure is at most about $25k.\n- **About $242k collectable.**\n\nIt stops 23 wrong chases, drafts 20 reminders for approval, sends 10 to a person to write, proposes 9 card re-runs and raises 3 decisions for Dana. Tested on past receipts, automatic matches were 81 of 81 correct, and all 14 disputes were held.\n\n## What is AI and what stays with a person, and why\nMaya: one wrong chase, or a message that reads like a threat to a top-50 account, gets it switched off. Priya must see why and fix it herself. So:\n- **Rules:** matching, holds, contact and look-alike domain checks, banned phrases, templates. Predictable, and Priya can edit every rule.\n- **Claude, once Legal allows:** reading ticket text (a dispute of our invoice, or a question about the customer's own invoicing?) and rewording drafts. **Off until Legal signs off on the data terms**, then through Amazon Bedrock under the existing AWS agreement. The rules-only version goes to Priya on Monday.\n- **A person:** every email, card charge, proposed match and hold release. Account managers release dispute holds, Dana owns write-offs and thresholds, and people write for top-50 and 90+ day accounts. When unsure, it holds: \"Over-holding is the right way to be wrong.\"\n\n## Where it gets things wrong\n- **Shortened payer names** (\"BRANDT\") broke the never-chase-paid rule. The fix holds every invoice of that amount, which over-holds.\n- **Ticket reading is 82% precise** (18 of 22). It held Reyes's $51k invoice over a question about its own client. Some refusals tagged How-to still slip through.\n- **No line items on invoices**, so the contract check can't see disputed fees or tax. Five disputes need an account manager or tax decision.\n\n## What we'd do with more time\n- An account-manager dispute workflow, with replies that quote the contract evidence.\n- The Slack morning digest, live.\n- Claude ticket reading through Bedrock after Legal signs off, measured against the rules.\n- A FIN-7 cash forecast agent on the same data, and FIN-6 renewal billing checks.\n- A 30-day review of the hold-override rate with Maya.\n"
}
```

### Claude · 2026-11-20 17:53:27 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && wc -w submission/ONE_PAGER.md",
 "description": "Count one-pager words"
}
```

### Tool · 2026-11-20 17:53:27 UTC
**Tool result:**
```
The file /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/ONE_PAGER.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:53:27 UTC
**Tool result:**
```
     540 submission/ONE_PAGER.md
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/ONE_PAGER.md",
 "content": "# Ledgerline Order-to-Cash team: one page\n\n**Live:** https://ledgerline-finance-rig.onrender.com · Data as of 2026-10-31\n\n## Which process\n**FIN-1 Collections, with FIN-2 Cash Application as its feeder.** Dana says overdue invoices have risen three quarters running (true year on year), and cash collection is the board's #1 worry. Paidly was switched off in 2025 after chasing a customer whose wire had already arrived. Finance can't see Zendesk, so customers with open complaints get chased too. Collections only works if cash application runs first.\n\n## What the tool does\nFour agents run in order, each with a manual people can edit:\n1. **Cash Application** matches unapplied receipts.\n2. **Account Context** reads tickets, contract, contacts and renewal.\n3. **Controller** holds anything that must not be chased, and says why.\n4. **Collections** drafts the reminder or proposes a card re-run.\n\nPriya works in the RIG. She approves, edits or overrides each item, and every click is logged.\n\nOn the real records, $633k overdue across 54 invoices breaks down as:\n- **$78k already received**, not yet applied.\n- **$313k disputed in support**: 14 invoices, most on tickets marked \"solved\". All 14 equal their contract amount, so real exposure is at most about $25k.\n- **About $242k collectable.**\n\nIt stops 23 wrong chases, drafts 20 reminders for approval, sends 10 to a person to write, proposes 9 card re-runs and raises 3 decisions for Dana. Tested on past receipts, automatic matches were 81 of 81 correct, and all 14 disputes were held.\n\n## What is AI and what stays with a person, and why\nMaya: one wrong chase, or a message that reads like a threat to a top-50 account, gets it switched off. Priya must see why and fix it herself. So:\n- **Rules:** matching, holds, contact and look-alike domain checks, banned phrases, templates. Predictable, and Priya can edit every rule.\n- **Claude, once Legal allows:** reading ticket text (a dispute of our invoice, or a question about the customer's own invoicing?) and rewording drafts. **Off until Legal signs off on the data terms**, then through Amazon Bedrock under the existing AWS agreement. The rules-only version goes to Priya on Monday.\n- **A person:** every email, card charge, proposed match and hold release. Account managers release dispute holds, Dana owns write-offs and thresholds, and people write for top-50 and 90+ day accounts. When unsure, it holds: \"Over-holding is the right way to be wrong.\"\n\n## Where it gets things wrong\n- **Shortened payer names** (\"BRANDT\") broke the never-chase-paid rule. The fix holds every invoice of that amount, which over-holds.\n- **Ticket reading is 82% precise** (18 of 22). It held Reyes's $51k invoice over a question about its own client. Some refusals tagged How-to still slip through.\n- **No line items on invoices**, so the contract check can't see disputed fees or tax. Five disputes need an account manager or tax decision.\n\n## What we'd do with more time\n- An account-manager dispute workflow, with replies that quote the contract evidence.\n- The Slack morning digest, live.\n- Claude ticket reading through Bedrock after Legal signs off, measured against the rules.\n- A FIN-7 cash forecast agent on the same data, and FIN-6 renewal billing checks.\n- A 30-day review of the hold-override rate with Maya.\n"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && wc -w submission/ONE_PAGER.md",
 "description": "Count one-pager words"
}
```

### Claude · 2026-11-20 17:53:39 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline\nr=run_pipeline()\nfor i in r['invoices']:\n    if 'Ambrose' in i['customer_name'] or 'Thornfield' in i['customer_name'] or 'Glover Eng' in i['customer_name']:\n        print(i['invoice_id'],i['customer_name'],i['amount'],i['days_past_due'],i['action'],[(h['code'],h['detail'][:120]) for h in i['holds']], (i['draft'] or {}).get('subject'), i.get('retry'))\nfor p in r['payments']: print(p.get('payment_id'),p.get('payer_name'),p.get('amount'),p.get('status') or p.get('decision'))\n\"",
 "description": "Check demo candidates for override and approval"
}
```

### Tool · 2026-11-20 17:53:40 UTC
**Tool result:**
```
INV-25862 Thornfield Consulting Group 39456.0 17 DRAFT_REMINDER [] Invoice INV-25862 — a quick check None
INV-25932 Ambrose & Petrov LLP 21216.0 0 NO_ACTION [] None None
INV-25989 Thornfield Digital 19584.0 0 NO_ACTION [] None None
INV-25967 Ambrose Ashby Law 10608.0 0 NO_ACTION [('STALE_CONTACT', 'mateo.jessop@ambroseashbylaw.example (Left the firm but still on invoice emails). Excluded from the draft; sent to elena')] None None
INV-25944 Ambrose Strategy 2115.0 0 NO_ACTION [] None None
INV-25803 Glover Engineering 1836.0 59 RETRY_CARD [] None {'card_works': True, 'evidence': 'PAY-65695: card charge of $1,836.00 succeeded on 2026-10-02', 'needs': 'Priya approves the re-run'}
INV-26029 Ambrose & Lowell Advisory 658.0 0 HOLD [('OPEN_ESCALATION', "T880474 '???' is pending (high priority). Policy: don't chase during an open escalation until the AM says so.")] None None
INV-25897 Ambrose & Lowell Advisory 658.0 10 HOLD [('OPEN_ESCALATION', "T880474 '???' is pending (high priority). Policy: don't chase during an open escalation until the AM says so.")] None None
PAY-65750 Jessop & Orwell Agency 62688.0 PROPOSE
PAY-65766 BRANDT & LOWELL CPAS 6324.0 PROPOSE
PAY-65796 ACHEBE + PEMBERTON ARCHITECTS 8000.0 PROPOSE
PAY-65805 Kingsway Engineering Group 5100.0 PROPOSE
PAY-65806 Castellano, Crane & Co 3672.0 AUTO_APPLY
PAY-65807 Studio Zeller 987.0 AUTO_APPLY
PAY-65808 YARDLEY & DUARTE ADVISORY 564.0 AUTO_APPLY
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && .venv/bin/python -c \"\nfrom app.engine.pipeline import run_pipeline\nr=run_pipeline()\nfor i in r['invoices']:\n    if 'Ambrose' in i['customer_name'] or 'Thornfield' in i['customer_name'] or 'Glover Eng' in i['customer_name']:\n        print(i['invoice_id'],i['customer_name'],i['amount'],i['days_past_due'],i['action'],[(h['code'],h['detail'][:120]) for h in i['holds']], (i['draft'] or {}).get('subject'), i.get('retry'))\nfor p in r['payments']: print(p.get('payment_id'),p.get('payer_name'),p.get('amount'),p.get('status') or p.get('decision'))\n\"",
 "description": "Check demo candidates for override and approval"
}
```

### Claude · 2026-11-20 17:54:21 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/VIDEO_SCRIPT.md",
 "content": "# Demo video: Loom talk track (target 8:00, hard range 7–9 min)\n\nRIG: https://ledgerline-finance-rig.onrender.com. Data as of 2026-10-31. All numbers come from `run_pipeline()` at 11:5x CST on 2026-11-20 and from `analysis/EVAL.md`, `FAILURES.md` and `DISCREPANCIES.md`.\n\n**Before recording (5 min)**\n- Wake the Render service: free plan, it sleeps when idle.\n- Sign in, then press **Run** once so the queues are fresh.\n- Have a terminal open at the project root for the BRANDT replay: `.venv/bin/python analysis/scripts/eval_guardrails.py | grep 1b`.\n- Leave Maya on hold. Don't send her anything during the recording.\n- Check the subject on Ambrose & Lowell's hold: it renders as `'???'` (T880474). Fix it or pick another hold.\n\n---\n\n## 0:00–0:30 What we chose and why\n**Screen:** RIG **Home**.\n\n> I picked one process: collections, with cash application feeding it. Dana says overdue invoices have risen three quarters running, and the board lists cash collection as its number-one worry. Ledgerline already tried a collections tool. Paidly was switched off after it chased a customer whose wire had already arrived. And finance can't see Zendesk, so people with open complaints get chased too. Both are the same problem: the reminder goes out before anyone checks the cash and the tickets. So this is one process, done properly, on Ledgerline's real records.\n\n## 0:30–1:30 The system: who does what\n**Screen:** **Architecture** (diagram), then **Team**.\n\n> Four agents run in a fixed order on every cycle.\n> - **Cash Application** matches the seven unapplied receipts, $87k in total. It applies a payment automatically only when the amount is exact and the memo quotes the invoice. That's Maya's rule.\n> - **Account Context** pulls each customer's tickets, contract, contacts and renewal date into one view.\n> - **The Controller** is the safety layer. It holds anything that must not be chased and records the reason.\n> - **Collections** drafts the policy reminder, or proposes a card re-run.\n>\n> **Screen:** click one agent on **Team** to show its manual.\n>\n> Each agent has a plain-English manual that a person can edit. Right now it all runs on rules. The AI is switched off until Legal agrees the data terms. More on that later.\n\n## 1:30–2:00 The headline\n**Screen:** ops page **Today**.\n\n> The ledger shows $633k overdue across 54 invoices.\n> - $78k of that is money we've already received but haven't applied.\n> - $313k is disputed in support tickets that finance never sees.\n> - About $242k is actually collectable.\n>\n> So most of Dana's overdue problem isn't customers refusing to pay. Today the tool stops 23 wrong chases, drafts 20 reminders for Priya to approve, sends 10 to a person to write, proposes 9 card re-runs, and puts 3 decisions in front of Dana.\n\n## 2:00–4:45 Live walkthrough on real records\n**2:00 Kingsway: paid but still showing overdue.** **Screen:** **Cash**, PAY-65805, then **Collections** filtered to Kingsway.\n> Kingsway Engineering paid $5,100 on 29 October with no reference. They have two $5,100 invoices open, one of them 111 days overdue. The agent proposes the older one and shows the other as an alternative, but it holds both. Paidly would have chased one of these. Priya confirms which invoice it is, and nothing goes out in the meantime.\n\n**2:35 Riverside: a \"solved\" ticket that is still a dispute.** **Screen:** **Collections**, INV-25787, open the DISPUTE hold.\n> Riverside Partners, $60,576, 35 days overdue. In Zendesk the ticket says \"solved\". The text says they won't pay until the seat count is fixed. The Controller holds the invoice and routes it to the account manager, Nadia Upton. It also runs a contract check: 46 seats at $88 a month plus a $12,000 platform fee comes to exactly $60,576. So the invoice matches the contract, and the AM goes into the call with evidence. All 14 disputed invoices match their contracts. If every claim turned out to be true, the real exposure would be at most about $25k, against $309k on hold.\n\n**3:15 Card re-run.** **Screen:** **Collections**, Glover Engineering INV-25803, RETRY_CARD, then **Approve**.\n> Glover Engineering's $1,836 card payment failed, but a charge on the same card went through on 2 October. So instead of an email, the agent proposes re-running the card. It never charges a card on its own. Priya approves each one, and Dana decides if that should ever change. I'll approve this one.\n\n**3:40 Decisions for Dana.** **Screen:** **Today**, \"Decisions for Dana\", Northgate Creative INV-25433.\n> Northgate Creative, $799, 149 days overdue. Tomorrow the old 150-day rule writes it off automatically. Maya said Dana should decide this morning, so the tool flags it as a decision for Dana today. Two more sit next to it: Hollis Nair at $517, nine days from write-off, and Eastman Engineering at $3,264. Eastman's would break Dana's $2,000 limit. That has already happened nine times, $47k in total, with no approval on record.\n\n**4:05 Approve one draft.** **Screen:** **Collections**, Thornfield Consulting INV-25862, open the draft and **Approve/Send**.\n> This is a normal case. Thornfield, $39,456, 17 days overdue. The contact is verified, there's no ticket and no payment waiting, so the agent drafted the friendly first reminder and copied the AM. I can edit it. I approve it, and it goes to the audit log under my name.\n\n**4:25 Override a hold with a reason.** **Screen:** **Collections**, Ambrose & Lowell INV-25897, **Override hold**, type the reason, then **Audit**.\n> Some holds are over-cautious, and that's deliberate. Ambrose & Lowell is held because a high-priority ticket is open. But the ticket is a product bug, not a billing complaint. I override the hold and type \"product b
… [tool input truncated]
```

### Tool · 2026-11-20 17:54:21 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/VIDEO_SCRIPT.md (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/submission/VIDEO_SCRIPT.md",
 "content": "# Demo video: Loom talk track (target 8:00, hard range 7–9 min)\n\nRIG: https://ledgerline-finance-rig.onrender.com. Data as of 2026-10-31. All numbers come from `run_pipeline()` at 11:5x CST on 2026-11-20 and from `analysis/EVAL.md`, `FAILURES.md` and `DISCREPANCIES.md`.\n\n**Before recording (5 min)**\n- Wake the Render service: free plan, it sleeps when idle.\n- Sign in, then press **Run** once so the queues are fresh.\n- Have a terminal open at the project root for the BRANDT replay: `.venv/bin/python analysis/scripts/eval_guardrails.py | grep 1b`.\n- Leave Maya on hold. Don't send her anything during the recording.\n- Check the subject on Ambrose & Lowell's hold: it renders as `'???'` (T880474). Fix it or pick another hold.\n\n---\n\n## 0:00–0:30 What we chose and why\n**Screen:** RIG **Home**.\n\n> I picked one process: collections, with cash application feeding it. Dana says overdue invoices have risen three quarters running, and the board lists cash collection as its number-one worry. Ledgerline already tried a collections tool. Paidly was switched off after it chased a customer whose wire had already arrived. And finance can't see Zendesk, so people with open complaints get chased too. Both are the same problem: the reminder goes out before anyone checks the cash and the tickets. So this is one process, done properly, on Ledgerline's real records.\n\n## 0:30–1:30 The system: who does what\n**Screen:** **Architecture** (diagram), then **Team**.\n\n> Four agents run in a fixed order on every cycle.\n> - **Cash Application** matches the seven unapplied receipts, $87k in total. It applies a payment automatically only when the amount is exact and the memo quotes the invoice. That's Maya's rule.\n> - **Account Context** pulls each customer's tickets, contract, contacts and renewal date into one view.\n> - **The Controller** is the safety layer. It holds anything that must not be chased and records the reason.\n> - **Collections** drafts the policy reminder, or proposes a card re-run.\n>\n> **Screen:** click one agent on **Team** to show its manual.\n>\n> Each agent has a plain-English manual that a person can edit. Right now it all runs on rules. The AI is switched off until Legal agrees the data terms. More on that later.\n\n## 1:30–2:00 The headline\n**Screen:** ops page **Today**.\n\n> The ledger shows $633k overdue across 54 invoices.\n> - $78k of that is money we've already received but haven't applied.\n> - $313k is disputed in support tickets that finance never sees.\n> - About $242k is actually collectable.\n>\n> So most of Dana's overdue problem isn't customers refusing to pay. Today the tool stops 23 wrong chases, drafts 20 reminders for Priya to approve, sends 10 to a person to write, proposes 9 card re-runs, and puts 3 decisions in front of Dana.\n\n## 2:00–4:45 Live walkthrough on real records\n**2:00 Kingsway: paid but still showing overdue.** **Screen:** **Cash**, PAY-65805, then **Collections** filtered to Kingsway.\n> Kingsway Engineering paid $5,100 on 29 October with no reference. They have two $5,100 invoices open, one of them 111 days overdue. The agent proposes the older one and shows the other as an alternative, but it holds both. Paidly would have chased one of these. Priya confirms which invoice it is, and nothing goes out in the meantime.\n\n**2:35 Riverside: a \"solved\" ticket that is still a dispute.** **Screen:** **Collections**, INV-25787, open the DISPUTE hold.\n> Riverside Partners, $60,576, 35 days overdue. In Zendesk the ticket says \"solved\". The text says they won't pay until the seat count is fixed. The Controller holds the invoice and routes it to the account manager, Nadia Upton. It also runs a contract check: 46 seats at $88 a month plus a $12,000 platform fee comes to exactly $60,576. So the invoice matches the contract, and the AM goes into the call with evidence. All 14 disputed invoices match their contracts. If every claim turned out to be true, the real exposure would be at most about $25k, against $309k on hold.\n\n**3:15 Card re-run.** **Screen:** **Collections**, Glover Engineering INV-25803, RETRY_CARD, then **Approve**.\n> Glover Engineering's $1,836 card payment failed, but a charge on the same card went through on 2 October. So instead of an email, the agent proposes re-running the card. It never charges a card on its own. Priya approves each one, and Dana decides if that should ever change. I'll approve this one.\n\n**3:40 Decisions for Dana.** **Screen:** **Today**, \"Decisions for Dana\", Northgate Creative INV-25433.\n> Northgate Creative, $799, 149 days overdue. Tomorrow the old 150-day rule writes it off automatically. Maya said Dana should decide this morning, so the tool flags it as a decision for Dana today. Two more sit next to it: Hollis Nair at $517, nine days from write-off, and Eastman Engineering at $3,264. Eastman's would break Dana's $2,000 limit. That has already happened nine times, $47k in total, with no approval on record.\n\n**4:05 Approve one draft.** **Screen:** **Collections**, Thornfield Consulting INV-25862, open the draft and **Approve/Send**.\n> This is a normal case. Thornfield, $39,456, 17 days overdue. The contact is verified, there's no ticket and no payment waiting, so the agent drafted the friendly first reminder and copied the AM. I can edit it. I approve it, and it goes to the audit log under my name.\n\n**4:25 Override a hold with a reason.** **Screen:** **Collections**, Ambrose & Lowell INV-25897, **Override hold**, type the reason, then **Audit**.\n> Some holds are over-cautious, and that's deliberate. Ambrose & Lowell is held because a high-priority ticket is open. But the ticket is a product bug, not a billing complaint. I override the hold and type \"product b
… [tool input truncated]
```

### Claude · 2026-11-20 17:54:26 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep \"^>\" submission/VIDEO_SCRIPT.md | wc -w; date +%H:%M",
 "description": "Count spoken words and current time"
}
```

### Tool · 2026-11-20 17:54:27 UTC
**Tool result:**
```
    1308
11:54
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && grep \"^>\" submission/VIDEO_SCRIPT.md | wc -w; date +%H:%M",
 "description": "Count spoken words and current time"
}
```

### Claude · 2026-11-20 17:54:34 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -i '' 's/About 1,250 spoken words, roughly 8 minutes at a normal pace./About 1,300 words including screen cues, roughly 8 to 8.5 minutes at a normal pace. If it runs long, cut the \"What still slips through\" paragraph first./' submission/VIDEO_SCRIPT.md && sed -i '' 's/at 11:5x CST/at 11:50 CST/' submission/VIDEO_SCRIPT.md && tail -1 submission/VIDEO_SCRIPT.md",
 "description": "Fix word-count note in video script"
}
```

### Tool · 2026-11-20 17:54:34 UTC
**Tool result:**
```
**End:** RIG **Home**. About 1,300 words including screen cues, roughly 8 to 8.5 minutes at a normal pace. If it runs long, cut the "What still slips through" paragraph first.
[This command modified 1 file you've previously read: submission/VIDEO_SCRIPT.md. Call Read before editing.]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && sed -i '' 's/About 1,250 spoken words, roughly 8 minutes at a normal pace./About 1,300 words including screen cues, roughly 8 to 8.5 minutes at a normal pace. If it runs long, cut the \"What still slips through\" paragraph first./' submission/VIDEO_SCRIPT.md && sed -i '' 's/at 11:5x CST/at 11:50 CST/' submission/VIDEO_SCRIPT.md && tail -1 submission/VIDEO_SCRIPT.md",
 "description": "Fix word-count note in video script"
}
```

### Claude · 2026-11-20 17:54:36 UTC
Now the checklist and journal.

### Claude · 2026-11-20 17:54:50 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/SUBMISSION_CHECKLIST.md",
 "content": "# Submission checklist (owned by test-steward)\n\nLast updated: 11:55 CST, T+0:45.\n\n## The four hand-ins\n- [ ] **Tool**: live Render URL with Google SSO (reviewer emails on the allow-list or a demo login path), plus a repo whose README gets it running locally in a few minutes\n  - Status 11:46: the service exists at https://ledgerline-finance-rig.onrender.com. It is on Render's free plan, which sleeps when idle; Starter is recommended but needs Jacek's OK. Repo: jacekmaterna1/finance-team-4-maya.\n  - Still not tested: reviewer sign-in in an incognito window; README steps from a clean clone (the data zip is unpacked at start-up); the audit log surviving a restart.\n- [ ] **Demo video**: 5–10 minutes, on Ledgerline's real data: what we chose, why, how, the tool working, and **where it gets things wrong**\n  - Status 11:55: script ready in `submission/VIDEO_SCRIPT.md`. It runs about 8 minutes and has timestamps and screen cues.\n  - It covers six real records: Kingsway, Riverside, the Glover card re-run, Northgate for Dana, the Thornfield draft and the Ambrose & Lowell override.\n  - It covers three failure cases: the BRANDT replay, the complaint counter going from 14 to 1, and Reyes. It also names the open gap: a How-to-tagged refusal still gets a draft.\n  - Not recorded yet. Before recording, check:\n    - The script names Documentation and Demo tabs, but the RIG nav (base.html) doesn't have them yet. Re-cue the script, or the builder adds the tabs.\n    - The Ambrose & Lowell hold shows the ticket subject as `'???'`.\n- [x] **One page**: the process, what the tool does, what is AI vs. what stays with a person and why, what we'd do with more time\n  - Status 11:55: `submission/ONE_PAGER.md`, 540 words, numbers re-run from `run_pipeline()` at 11:50. The /about page renders it.\n  - Still to do: check that it prints on one page from /about.\n- [ ] **Your working**: every AI conversation (dead ends included, plus the pre-start planning session, labelled) and the repo link\n  - Not started. This happens at the end: export from ~/.claude/projects/ into `submission/ai_conversations/` with an index.\n\n## Grading self-check\n- [x] Changes the job: would Dana still use it in a month? What does her day look like with it?\n  - Priya works the RIG queue. Dana gets 3 decisions. Go-live is rules-only on Monday (Maya, Exchange 4). The 30-day check is the hold-override rate.\n- [x] Judgment: AI vs. human split stated and enforced in code (approval queue, holds, contact checks)\n  - `use_claude` defaults to False. Every email, card re-run, match and release needs a person. Rule changes from chat only apply on a human click.\n- [x] Evidence: numbers from analysis/EVAL.md, at least 2 failure cases shown in the video\n  - Automatic matches 81 of 81 correct. Disputes 14 of 14 held. Ticket-read precision 82%.\n  - Guardrail re-run at 11:52: 51 pass, 3 fail. The 2 real fails are 2d and 2f, refusals tagged How-to or untagged. The third, check 8 (Drummond), now goes to a person by design, so that test needs updating.\n  - EVAL.md still says 44/54, from 11:36, before the fixes. The qa-evaluator should refresh it.\n\n## Admin\n- [x] Timer start time recorded in trail/JOURNAL.md (~11:10 CST)\n- [x] Maya Q&A logged word for word (Exchanges 1–4, 5 of 60 used; recheck count vs challenge page)\n- [ ] Secrets not in repo; reviewer access to the live link tested in an incognito window\n- [ ] Submitted before T+24:00 (target: T+7:00)\n"
}
```

### Claude · 2026-11-20 17:54:55 UTC
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/JOURNAL.md <<'EOF'\n| 11:55 | T+0:45 | test-steward | Wrote `submission/ONE_PAGER.md` (540 words) and `submission/VIDEO_SCRIPT.md` (about 8 minutes, six real records, three failure cases), and updated the submission checklist. Re-ran `run_pipeline()` first: $633,245 overdue = $78,348 received + $312,922 disputed + $241,975 collectable; 23 chases prevented, 9 card re-runs. **3** decisions for Dana, not 2: Northgate $799, Hollis Nair $517, and Eastman $3,264 over the $2k limit. Re-ran the guardrail red-team: 51 pass, 3 fail, up from 44/54. BRANDT, JESSOP and KINGSWAY now hold. Refusals tagged How-to or untagged still get a draft (checks 2d and 2f). The Drummond check is now out of date, because Drummond goes to a person by design | Hand-in artifacts drafted from verified numbers. Maya is on hold, so nothing was sent |\nEOF\ntail -2 trail/JOURNAL.md | cut -c1-200",
 "description": "Append journal row"
}
```

### Tool · 2026-11-20 17:54:56 UTC
**Tool result:**
```
The file /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/SUBMISSION_CHECKLIST.md has been updated successfully. (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:54:56 UTC
**Tool result:**
```
| 11:46 | T+0:36 | test-steward | Logged Exchange 4 word for word and added D12 to D15. Made the Maya files consistent for the RIG parser. Put Draft 4 on hold, because it is a status update under the 
| 11:55 | T+0:45 | test-steward | Wrote `submission/ONE_PAGER.md` (540 words) and `submission/VIDEO_SCRIPT.md` (about 8 minutes, six real records, three failure cases), and updated the submission chec
```

### Claude ·  UTC
Now the checklist and journal.
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/trail/SUBMISSION_CHECKLIST.md",
 "content": "# Submission checklist (owned by test-steward)\n\nLast updated: 11:55 CST, T+0:45.\n\n## The four hand-ins\n- [ ] **Tool**: live Render URL with Google SSO (reviewer emails on the allow-list or a demo login path), plus a repo whose README gets it running locally in a few minutes\n  - Status 11:46: the service exists at https://ledgerline-finance-rig.onrender.com. It is on Render's free plan, which sleeps when idle; Starter is recommended but needs Jacek's OK. Repo: jacekmaterna1/finance-team-4-maya.\n  - Still not tested: reviewer sign-in in an incognito window; README steps from a clean clone (the data zip is unpacked at start-up); the audit log surviving a restart.\n- [ ] **Demo video**: 5–10 minutes, on Ledgerline's real data: what we chose, why, how, the tool working, and **where it gets things wrong**\n  - Status 11:55: script ready in `submission/VIDEO_SCRIPT.md`. It runs about 8 minutes and has timestamps and screen cues.\n  - It covers six real records: Kingsway, Riverside, the Glover card re-run, Northgate for Dana, the Thornfield draft and the Ambrose & Lowell override.\n  - It covers three failure cases: the BRANDT replay, the complaint counter going from 14 to 1, and Reyes. It also names the open gap: a How-to-tagged refusal still gets a draft.\n  - Not recorded yet. Before recording, check:\n    - The script names Documentation and Demo tabs, but the RIG nav (base.html) doesn't have them yet. Re-cue the script, or the builder adds the tabs.\n    - The Ambrose & Lowell hold shows the ticket subject as `'???'`.\n- [x] **One page**: the process, what the tool does, what is AI vs. what stays with a person and why, what we'd do with more time\n  - Status 11:55: `submission/ONE_PAGER.md`, 540 words, numbers re-run from `run_pipeline()` at 11:50. The /about page renders it.\n  - Still to do: check that it prints on one page from /about.\n- [ ] **Your working**: every AI conversation (dead ends included, plus the pre-start planning session, labelled) and the repo link\n  - Not started. This happens at the end: export from ~/.claude/projects/ into `submission/ai_conversations/` with an index.\n\n## Grading self-check\n- [x] Changes the job: would Dana still use it in a month? What does her day look like with it?\n  - Priya works the RIG queue. Dana gets 3 decisions. Go-live is rules-only on Monday (Maya, Exchange 4). The 30-day check is the hold-override rate.\n- [x] Judgment: AI vs. human split stated and enforced in code (approval queue, holds, contact checks)\n  - `use_claude` defaults to False. Every email, card re-run, match and release needs a person. Rule changes from chat only apply on a human click.\n- [x] Evidence: numbers from analysis/EVAL.md, at least 2 failure cases shown in the video\n  - Automatic matches 81 of 81 correct. Disputes 14 of 14 held. Ticket-read precision 82%.\n  - Guardrail re-run at 11:52: 51 pass, 3 fail. The 2 real fails are 2d and 2f, refusals tagged How-to or untagged. The third, check 8 (Drummond), now goes to a person by design, so that test needs updating.\n  - EVAL.md still says 44/54, from 11:36, before the fixes. The qa-evaluator should refresh it.\n\n## Admin\n- [x] Timer start time recorded in trail/JOURNAL.md (~11:10 CST)\n- [x] Maya Q&A logged word for word (Exchanges 1–4, 5 of 60 used; recheck count vs challenge page)\n- [ ] Secrets not in repo; reviewer access to the live link tested in an incognito window\n- [ ] Submitted before T+24:00 (target: T+7:00)\n"
}
```
**Tool call:** `Bash`
```json
{
 "command": "cd \"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\" && cat >> trail/JOURNAL.md <<'EOF'\n| 11:55 | T+0:45 | test-steward | Wrote `submission/ONE_PAGER.md` (540 words) and `submission/VIDEO_SCRIPT.md` (about 8 minutes, six real records, three failure cases), and updated the submission checklist. Re-ran `run_pipeline()` first: $633,245 overdue = $78,348 received + $312,922 disputed + $241,975 collectable; 23 chases prevented, 9 card re-runs. **3** decisions for Dana, not 2: Northgate $799, Hollis Nair $517, and Eastman $3,264 over the $2k limit. Re-ran the guardrail red-team: 51 pass, 3 fail, up from 44/54. BRANDT, JESSOP and KINGSWAY now hold. Refusals tagged How-to or untagged still get a draft (checks 2d and 2f). The Drummond check is now out of date, because Drummond goes to a person by design | Hand-in artifacts drafted from verified numbers. Maya is on hold, so nothing was sent |\nEOF\ntail -2 trail/JOURNAL.md | cut -c1-200",
 "description": "Append journal row"
}
```

### Claude · 2026-11-20 17:55:05 UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "1. The one-pager is ready, 540 words, under the five headings you asked for (/about renders it). I re-ran `run_pipeline()` at 11:50 and used those numbers. One differs from your brief: the tool now raises **3 decisions for Dana, not 2**. The three are Northgate $799, Hollis Nair $517, and Eastman $3,264, whose automatic write-off would go over Dana's $2k limit. The one-pager and video say 3.\n2. The video script is ready, about 8 minutes with timestamps and screen cues. It covers Kingsway, Riverside with the contract check, the Glover card re-run, Northgate, approving the Thornfield draft and overriding the Ambrose & Lowell hold. Then the three chat commands and three failures: the BRANDT replay, the complaint counter going from 14 to 1, and Reyes. It ends with the Maya channel and what's next. I updated the checklist and added a journal row for 11:55 (T+0:45). Nothing was sent to Maya and no app code was touched.\n3. Things to fix before recording:\n   - The RIG nav doesn't have the Documentation and Demo tabs yet, so the script points at screens that aren't there.\n   - The Ambrose & Lowell hold shows the ticket subject as `'???'`.\n   - Render's free plan sleeps when idle, so wake the service before recording.\n   - `analysis/EVAL.md` still says 44 of 54 guardrail checks pass. My re-run now gives 51 pass and 3 fail. Two are real: a refusal in a ticket tagged How-to, or not tagged at all, still gets a reminder drafted. The third is out of date, because Drummond now goes to a person on purpose.\n4. Still open: the AI conversation export, testing reviewer sign-in in an incognito window, the README steps from a clean clone, printing the one-pager to check it fits one page, and recording the video.\n\nFiles are in /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a:\n- submission/ONE_PAGER.md\n- submission/VIDEO_SCRIPT.md\n- trail/SUBMISSION_CHECKLIST.md\n- trail/JOURNAL.md"
}
```

### Tool · 2026-11-20 17:55:06 UTC
**Tool result:**
```
{"success":true,"message":"Report delivered to your caller."}
```
