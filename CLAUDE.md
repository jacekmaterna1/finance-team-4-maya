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
5. The timer start time is recorded in `trail/JOURNAL.md` the moment Jacek presses "Begin day one". All T+ times count from it.

## Maya loop (standing instruction from Jacek)
Message Maya ONLY when we need a confirmation (a decision she or Dana owns) or intel (something the data room
can't tell us). No status updates for their own sake. Every draft states `Purpose: Confirmation` or `Purpose: Intel`.
The whole exchange is shown in the RIG's MAYA tab. At each milestone the test-steward drafts one message in
`trail/MAYA_OUTBOX.md`. The main thread sends it via the Maya chat at apply.scaleworks.com/build (Jacek's Chrome),
pastes the reply back, and the steward logs it word for word and records what changed. Budget: 60 messages, aim for ≤ 12.

## Product guardrails (judgment is graded)
- Deterministic code does arithmetic, joins and exact matching. The LLM does fuzzy matching, text reading, tone and explanations.
- No customer-facing send, credit, write-off or ledger change without a human approval in the UI.
- Every agent action → an audit-log row (agent, input refs, decision, confidence, reason, approver).
- If a feature needs data the room doesn't have, generate it, label it SYNTHETIC, and say so.

## Do not
- Touch the Scaleworks site's "Begin day one" button; only Jacek starts the timer.
- Put secrets in the repo. Render env vars hold ANTHROPIC_API_KEY and the Google OAuth client.
