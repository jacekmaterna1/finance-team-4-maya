# QA pass 3 (re-test after fixes) — 2026-11-20 ~12:25 CST, T+1:15

Run by the main thread against the current code, using the QA agent's own scripts plus the builder's regression tests.

| Suite | Result | Notes |
|---|---|---|
| Regression tests (tests/test_web_guards.py) | 23/23 pass | One per QA pass-2 defect |
| FIN-1 policy (eval_policy.py) | 12/12 pass | Courtesy stage now drafted: 16 invoices due within 5 days, 13 drafts, 1 top-50 to a person, 1 held, 1 already paid |
| Consistency across pages (eval_web.py C) | 18/18 pass | |
| Human-action flows (eval_web.py D) | 27/27 in substance | The script expects HTTP 400 for a second approval; the app returns 409 (Conflict) and writes nothing. Test artifact |
| Guardrails (eval_guardrails.py) | 54/54 in substance | Check 7b fakes 95 days by editing ar_aging.days_past_due, which the engine no longer reads (it computes days from due_date since the courtesy fix). Verified directly: INV-25862 moved to 95 days overdue → HUMAN_WRITES (ESCALATE_90) |
| FIN-2 cash application (pass 2) | 100% auto-apply precision, 98.3% proposal top-1 | Unchanged by the fixes |

Closed since pass 2: dispute holds need AM confirmation for both Release and Override; sends only on unheld invoices to verified recipients; partial rules posts can't wipe guardrails and loosening one needs Dana; no double approvals; courtesy stage; word-boundary banned phrases; Maya counter 4/60; demo page without internal notes; CST times; $10k cap shown.

Still open (needs a decision, not code): live state is ephemeral on Render's free plan (Starter + disk keeps it); the GitHub repo is private (reviewers need access, or make it public).
