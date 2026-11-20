# Submission checklist (owned by test-steward)

Last updated: 11:55 CST, T+0:45.

## The four hand-ins
- [ ] **Tool**: live Render URL with Google SSO (reviewer emails on the allow-list or a demo login path), plus a repo whose README gets it running locally in a few minutes
  - Status 11:46: the service exists at https://ledgerline-finance-rig.onrender.com. It is on Render's free plan, which sleeps when idle; Starter is recommended but needs Jacek's OK. Repo: jacekmaterna1/finance-team-4-maya.
  - Still not tested: reviewer sign-in in an incognito window; README steps from a clean clone (the data zip is unpacked at start-up); the audit log surviving a restart.
- [ ] **Demo video**: 5–10 minutes, on Ledgerline's real data: what we chose, why, how, the tool working, and **where it gets things wrong**
  - Status 11:55: script ready in `submission/VIDEO_SCRIPT.md`. It runs about 8 minutes and has timestamps and screen cues.
  - It covers six real records: Kingsway, Riverside, the Glover card re-run, Northgate for Dana, the Thornfield draft and the Ambrose & Lowell override.
  - It covers three failure cases: the BRANDT replay, the complaint counter going from 14 to 1, and Reyes. It also names the open gap: a How-to-tagged refusal still gets a draft.
  - Not recorded yet. Before recording, check:
    - The script names Documentation and Demo tabs, but the RIG nav (base.html) doesn't have them yet. Re-cue the script, or the builder adds the tabs.
    - The Ambrose & Lowell hold shows the ticket subject as `'???'`.
- [x] **One page**: the process, what the tool does, what is AI vs. what stays with a person and why, what we'd do with more time
  - Status 11:55: `submission/ONE_PAGER.md`, 540 words, numbers re-run from `run_pipeline()` at 11:50. The /about page renders it.
  - Still to do: check that it prints on one page from /about.
- [ ] **Your working**: every AI conversation (dead ends included, plus the pre-start planning session, labelled) and the repo link
  - Not started. This happens at the end: export from ~/.claude/projects/ into `submission/ai_conversations/` with an index.

## Grading self-check
- [x] Changes the job: would Dana still use it in a month? What does her day look like with it?
  - Priya works the RIG queue. Dana gets 3 decisions. Go-live is rules-only on Monday (Maya, Exchange 4). The 30-day check is the hold-override rate.
- [x] Judgment: AI vs. human split stated and enforced in code (approval queue, holds, contact checks)
  - `use_claude` defaults to False. Every email, card re-run, match and release needs a person. Rule changes from chat only apply on a human click.
- [x] Evidence: numbers from analysis/EVAL.md, at least 2 failure cases shown in the video
  - Automatic matches 81 of 81 correct. Disputes 14 of 14 held. Ticket-read precision 82%.
  - Guardrail re-run at 11:52: 51 pass, 3 fail. The 2 real fails are 2d and 2f, refusals tagged How-to or untagged. The third, check 8 (Drummond), now goes to a person by design, so that test needs updating.
  - EVAL.md still says 44/54, from 11:36, before the fixes. The qa-evaluator should refresh it.

## Admin
- [x] Timer start time recorded in trail/JOURNAL.md (~11:10 CST)
- [x] Maya Q&A logged word for word (Exchanges 1–4, 5 of 60 used; recheck count vs challenge page)
- [ ] Secrets not in repo; reviewer access to the live link tested in an incognito window
- [ ] Submitted before T+24:00 (target: T+7:00)
