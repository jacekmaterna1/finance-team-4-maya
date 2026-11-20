# Ledgerline AI Operator Challenge — Plan

Status: PRE-START (timer not started). Written 2026-11-20.

## The one-line pitch
An AI **Order-to-Cash team** for Dana Ruiz (VP Finance): several agents that each own one job,
the way SpaceXSI runs its Grok accounting bots. Together they fix **one** process, Collections (FIN-1),
plus Cash Application (FIN-2), which has to work first. Every action is logged, and a person approves
anything that touches a customer or the ledger.

## Why this process (LOCKED by Jacek, pre-start. Maya can refine scope and guardrails)
- Dana: "Overdue invoices have risen three quarters running." Maya: "cash collection is slipping."
- FIN-1 and FIN-2 are linked: customers get chased for invoices they already paid (cash application lags
  3–5 days) and chased while a complaint is open (finance can't see support tickets). Collections can't be
  fixed without fixing what feeds it.
- The data room has everything we need: invoices, payments (some unmatched), ar_aging, customers,
  contacts, contracts, tickets, nps, usage, collections_policy, collections templates, process_maps,
  billing_engine_rewrite_2026.
- It matches the brief: **one process working end to end on real records**, built by a team of agents.
  That is not five half-built tools.

## Why not "all of finance"
The brief says: *"We would rather see one thing working well than five things sketched."* Also, *"A deck
alone is a no."* We **show** the team architecture (it can grow to cover FIN-3/4/5/6/7) and **prove** it on one
process. The one-pager's "with more time" section says which agent we would add next.

## Runtime agent team (inside the product, Claude API)
| Agent | Owns | Can do alone | Needs a human |
|---|---|---|---|
| **Cash Application Agent** | Match unapplied receipts (payments.csv rows with no invoice id) to open invoices | Exact matches, bank-fee differences under a set amount | Short payments, ambiguous matches, write-offs |
| **Account Context Agent** | One view of each customer: open tickets, NPS, usage, contract, renewal date, billing contacts | Read only | — |
| **Collections Agent** | Rank overdue AR, pick the right action and tone under collections_policy, draft reminders, follow up failed card payments | Drafts and queues | **Every send** (week-2 mode, as in the Grok article) |
| **Controller Agent** | Guardrails: policy checks, holds (open complaint, already paid, disputed after billing rewrite, renewal in flight), contact authorization check (domain must match contacts.csv) | Hold or block | Releasing a hold |

Deterministic code does the arithmetic and the joins. The LLM does fuzzy matching, reads remittance and
ticket text, judges tone, and explains each recommendation. Each decision is written to an **audit log**
the user can browse in the app.

## Deliverables (from the brief)
1. **The tool**: a live Render URL with Google SSO, plus a repo with a README that gets it running in minutes.
2. **Demo video**, 5–10 minutes: what we chose, why, how, the tool working on real records, and where it gets things wrong.
3. **One page**: the process, what the tool does, what is AI and what stays with a person and why, what we'd do with more time.
4. **Your working**: every AI conversation, dead ends included, plus the repo. → `trail/` + exported transcripts.

## Timeline once the timer starts (active time ≈ 6 hours)
| T+ | Work | Owner |
|---|---|---|
| 0:00–0:45 | Download the data room into `data/`. Profile it and find the evidence numbers: overdue invoices that are actually paid, overdue invoices with open tickets, failed card payments | data-analyst |
| 0:45–1:15 | Ask Maya the prepared questions (`trail/MAYA_QA.md`). Lock the process choice. Log the decision | Jacek + test-steward |
| 1:15–4:30 | Build: data layer, then the 4 agents, then the approval queue and audit-trail UI | builder (subagents in parallel) |
| 4:30–5:15 | Evaluation: accuracy against known answers, a failure gallery ("where it gets things wrong") | qa-evaluator |
| 5:15–5:45 | GitHub, Render deploy, Google SSO | builder + Jacek |
| 5:45–6:30 | One-pager, video script, recording, transcript export, submission check | test-steward |

## Rules of engagement
- No product code and no work on the data room before the timer starts. Pre-start work = planning and team setup
  only, and we **disclose** this session in "your working".
- Everything high-level goes in `trail/JOURNAL.md` as it happens, with a timestamp and the elapsed T+ time.
- Questions to Maya and her answers go in `trail/MAYA_QA.md` word for word. The brief says "What you ask is part of what we read."
