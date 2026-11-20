# QA pass 2: FIN-1 / FIN-2 / RIG readiness

QA Evaluator. Run on 2026-11-20 at 12:10–12:20 CST against the code as it stood then.

- **Local tests** used a throw-away `DB_PATH`, `RULES_PATH` and `MANUALS_DIR` in a temp dir, so `./ledgerline.db`,
  `./rules.json` and `app/engine/manuals/` were not touched.
- **Live smoke checks** (https://ledgerline-finance-rig.onrender.com) were read-only, plus two requests that were
  meant to be rejected, plus one chat "status".
- Nothing in `app/` or `data/` was edited. Maya was not contacted.

| script | section |
|---|---|
| `analysis/scripts/eval_cash_app.py`, `eval_guardrails.py` | A |
| `analysis/scripts/eval_policy.py` → `analysis/work/eval_policy_results.csv` | B |
| `analysis/scripts/eval_web.py <tmpdir>` → `analysis/work/eval_web_results.csv` | C, D |
| `eval_controller.py` | dispute and ticket-read numbers in EVAL.md |

## Summary

| section | result |
|---|---|
| A. FIN-2 regression | **PASS 5/5** (auto-apply precision 100%; shortened-name replays held; guardrail red-team 54/54) |
| B. FIN-1 policy compliance | **PASS 11 / FAIL 1.** The courtesy stage never fires: 16 invoices ($219,071) due in the next 1–5 days get no courtesy note |
| C. Consistency across screens | **PASS 18/18** |
| D. Human-action flows | **PASS 22 / FAIL 5.** Hold bypasses and a destructive partial rules POST |
| E. RIG readiness for Maya | **Renders correctly, with 11 rough edges.** Two would mislead Maya or a reviewer |
| F. Robustness | **FAIL on durability.** Live state is ephemeral and is wiped at every deploy or idle spin-down. Speed is fine: every page is under 2 s |

**Verdict: FIN-2 is at 100% on the evidence. FIN-1's decisions are policy-correct, apart from the missing courtesy
stage. The approval UI has 3 server-side guardrail bypasses (D2, D3, D4) that must be closed before Maya or Priya
uses the RIG.**

---

## A. FIN-2 regression

| check | result | evidence |
|---|---|---|
| A1 Auto-apply precision on the 246 real test receipts | **PASS** | 59/59 correct (100%). 0 wrong auto-applies across 286 rows; 0 synthetic receipts auto-applied |
| A2 Effect of the $10k cap (`auto_apply_max_amount`) | **PASS** (as designed) | Real auto-applies drop from 81 to 59. **22 exact-reference receipts over $10k become proposals at 0.95; all 22 are proposed correctly.** Proposal top-1 is 98.3% (172/175). The live book is unchanged: 3 auto-applies, all ≤ $3,672. Cost: Priya's "easy" queue grows from 2 to 24 of 63 easy receipts |
| A3 BRANDT / JESSOP / KINGSWAY shortened-name replays: no chase | **PASS** | INV-25806, INV-25784 and INV-25469 are all HOLD / MONEY_RECEIVED ("Possible payment from an unidentified payer"). The cash agent no longer assigns a wrong customer (JESSOP previously became Jessop Legal; it is now `None`) |
| A4 Unidentified payer holds same-amount invoices | **PASS** | `controller.py:36-43`. Also confirmed: PEMBERTON is no longer tagged to the wrong customer (C1235) |
| A5 Guardrail red-team (`eval_guardrails.py`) | **PASS 54/54** | The previous 10 failures are fixed: refusal wording in any category, banned list extended. One check was updated to expect LEGAL_RISK to block a card re-run |

## B. FIN-1 policy compliance (every one of the 117 invoices in `run_pipeline()`)

| check | result | evidence |
|---|---|---|
| B1 Stage vs real days past due (-5/+7/+21/+45/+90) | **FAIL** | 61 of 117 invoices are staged `wait` instead of `not_due` or `courtesy`. **16 invoices / $219,071 are due within 5 days and get no courtesy note** (for example INV-25933 Whitlock, due 11-01). For not-yet-due invoices the reason says "Next reminder at day 7". Cause: `pipeline.py:74` uses `ar_aging.days_past_due`, which the export floors at 0 (FACTS §1), so `stage_for()` (`collections.py:31-32`) never sees a negative value. Fix: `dpd = (AS_OF - pd.Timestamp(r["due_date"])).days`. Keep `max(dpd, 0)` for display. All 56 past-due invoices are staged correctly |
| B2 Top-50 never DRAFT_REMINDER | PASS | 14 top-50 invoices: HOLD / HUMAN_WRITES / NO_ACTION (not due) |
| B3 No draft where PAID / MONEY_RECEIVED / DISPUTE / CANCELLATION / LEGAL_RISK / OPEN_ESCALATION | PASS | 0 of 117 |
| B4 Drafts contain no banned phrase | PASS | 21 drafts (20 DRAFT_REMINDER + 1 HUMAN_WRITES). Also: the new substring "court" causes no false block today (no draft says "courtesy" or "courteous"). That is fragile, see E/defect S3-4 |
| B5 Recipients are verified (in contacts.csv for that customer, domain match, billing or admin role) | PASS | 21/21 |
| B6 Never a "left the firm" contact | PASS | 0 |
| B7 AM cc'd | PASS | 21/21 |
| B8 Invoice id, amount and due date in the body match the ledger | PASS | 21/21, cross-checked against invoices.csv |
| B9 Signed off by Priya | PASS | 21/21 |
| B10 Card re-runs only where a later card charge succeeded and there is no hard hold or legal risk | PASS | 9 re-runs. Drummond (chargeback, T880019) is now HUMAN_WRITES with LEGAL_RISK, not a re-run |
| B11 Dana decisions = card invoices ≤10 days from the 150-day write-off, or > $2,000 | PASS | Exactly 3: Eastman Engineering $3,264 (>$2k), Northgate $799 (1 day), Hollis Nair $517 (9 days) |

## C. Consistency (Home, /today, /collections, /digest, chat "status", Team, `run_pipeline()`)

**PASS 18/18.**

- The four money figures match on every screen: overdue $633,245, already received $78,348, disputed $312,922,
  collectable $241,975.
- The counts match on every screen: drafts 20, held 21, card re-runs 9, person writes 3, proposals 4.
- Needs-a-human is 57 on both Home and /today (21+20+9+3+4).
- /collections groups show 21 / 9 / 3 / 20 / 64.
- No stale figure ($83,448, $312,264, $237,533, "$238k", "22 wrong chases", "27 reminders") appears on Home, Today,
  Digest, Team, About, Docs, Architecture or Demo.
- The live site shows the same four figures.
- Minor: the chat says "16 with an open billing complaint" (customers), while the Team card says "14 Disputes"
  (tickets). Both are right but read as a contradiction. Label them "customers" and "tickets".

## D. Human-action flows (local TestClient; live smoke checks in the last line)

| check | result |
|---|---|
| Approve payment proposal (PAY-65750) | PASS |
| Undo auto-apply (PAY-65806) | PASS (logged as `reject` with `undo: true`) |
| Approve draft with an edit → `edit` + `send` rows | PASS |
| Send with banned wording → 400 | PASS ("debt collector" blocked server-side) |
| **D2: Send to an address not in contacts.csv (`ap@okaforlegal-billing.example` typed in "To")** | **FAIL: HTTP 200.** The server accepts any "To" (`views.py:493-515`; the field is free text in `_invoice.html:61`). Fix: reject any address that is not a verified contact for that customer, as returned by `collections.recipients(ctx)` |
| **D3: Send on a HOLD invoice (Jessop INV-25784, MONEY_RECEIVED) with no override** | **FAIL: HTTP 200.** A Paidly chase can be recorded as sent by POST. The UI hides the form, but the server does not check (`views.py:493`). Fix: allow send only if action ∈ {DRAFT_REMINDER, HUMAN_WRITES} or the latest human action is override_hold / release_hold |
| Reject draft | PASS |
| Override hold, reason < 5 chars → 400; with a reason → OK | PASS / PASS |
| Release DISPUTE without the AM checkbox → 400; with the box + name → OK | PASS / PASS |
| **D4: Override (not release) a DISPUTE hold without AM** | **FAIL: HTTP 200.** The "Override hold" button sits next to "Release hold" (`_invoice.html:50-51`), and the AM rule is only checked for `kind == "release_hold"` (`views.py:535-536`). Any user can lift a dispute hold with a 5-character reason, which defeats Maya's "release only when the AM agrees". Fix: apply `needs_am` to both kinds, or hide Override when a DISPUTE or CANCELLATION hold is present |
| Approve / reject card re-run; re-run on a non-re-run invoice → 400 | PASS / PASS / PASS |
| Rules via /rules form (full form) shows before/after | PASS (`auto_apply_max_amount` 1000: auto-applied 3 → 2) |
| **D5: Partial /rules POST** (`{fee_tolerance: 25}` only, e.g. a script or a stale tab) | **FAIL.** It silently set `top50_human_only`, `auto_apply_exact_ref_match` and `notify_am_before_contact` to **false** and emptied `banned_phrases` (13 → 0) (`views.py:276-300`: a missing checkbox becomes False and a missing textarea becomes []). Fix: only change keys present in the form (send hidden `field_present` markers). Never accept an empty banned list. Require Dana for turning off top-50, the banned list, or the AM cc |
| Chat "set auto_apply_max_amount to 1000" + /api/rules/apply | PASS (shows "auto applied: 3 → 2, held 21 → 22 ... INV-25845 NO_ACTION→HOLD") |
| Chat "from now on cc Dana on anything over $40k" → accept in Direct → in manual | PASS (appended to `collections.md` in the temp MANUALS_DIR) |
| Loom share link → embed URL; non-video URL → 400 | PASS / PASS |
| Every action in /audit and /activity with user + reason; CSV export | PASS (20 actions) |
| **D6: Approving an already-approved payment** | **FAIL (sev-3)**: a second `apply` row is written (`views.py:443-450`, no state check). Also, approving the ambiguous Kingsway proposal records INV-25469 with no prompt to pick between the two invoices |
| Live smoke | PASS: override with reason "ok" → 400; dispute release without AM → 400; chat status returns the same figures |

## E. RIG readiness for "Maya interactions from the RIG"

**What works.** The Maya tab renders Exchanges 1–4 word for word, with "What we changed" for each, plus pending
Draft 6 (READY, Confirmation). Locally it shows "4 of 60 used", matching MAYA_OUTBOX's verified count. All 258
internal links return 200. There are no tracebacks, no "nan" and no template placeholders.

**Rough edges, in order of how badly they could mislead:**
1. **Live Maya tab says "5 of 60 used"; local says 4.** `trail/MAYA_QA.md:3` still says "5 of 60 ... one message is
   unaccounted for". MAYA_OUTBOX says "4 of 60 (verified ... 56 messages left)". The live deploy is behind the
   repo, or reads the stale line. Fix line 3 of MAYA_QA.md and redeploy.
2. **/demo shows "Coming soon"** and renders `submission/VIDEO_SCRIPT.md` in full, including internal prep notes
   that Maya (and "a person at Scaleworks who reads everything") will see:
   - "Leave Maya on hold. Don't send her anything during the recording."
   - "Check the subject on Ambrose & Lowell's hold: it renders as '???' ... Fix it or pick another hold."
   - the terminal replay instructions.
   Strip the "Before recording" section from the rendered page.
3. **Docs links to https://github.com/jacekmaterna1/finance-team-4-maya, which returns 404** (private or missing).
4. **Collections group title "A person writes these (top-50 accounts)"** (`views.py:32`) holds 3 invoices, and 2 are
   not top-50: Eastman Engineering and Drummond are LEGAL_RISK. Rename it to "A person writes these".
5. **Cash Application card and manual omit the $10k auto-apply cap.** "Can do alone: apply a receipt when amount AND
   invoice reference both match exactly" appears on Team, /agents/cash and `manuals/cash_application.md`. The
   manual is the agent's own spec, so it is now wrong.
6. **Not-yet-due invoices say "Next reminder at day 7"** on Activity, Collections and the Customer page. The policy
   next step is the courtesy note at -5 (B1).
7. **Live "Agents ran 2026-11-20 18:01:15"** is UTC, while the Build clock and every trail time are CST. Local
   shows 12:12. Use one zone and label it.
8. **"Automatic card write-off in 1 days"** (grammar) on Home, Today and Digest.
9. **Home Dana tile says "3"** but names 2 customers (Hollis Nair is cut off with no "+1").
10. **Ambrose & Lowell's hold reads `'???'`.** It is the real ticket subject (T880474). Show "(no subject)" or the
    first words of the body.
11. **Docs says transcripts are in `submission/ai_conversations/`, "Exported at the end of the build".** The folder
    does not exist yet. That is expected, but it must not be forgotten.

There are no stale headline numbers anywhere, and the T+ times in the Maya tab match the journal (start 11:10 CST).

## F. Robustness

| check | result |
|---|---|
| Page speed | **PASS.** Local: every page 0.00–0.08 s once warm. The first hit costs 1.05 s (one pipeline run, 0.34 s engine). Live (warm, 12:14 CST): 0.11–0.68 s for all 15 pages, slowest /buildlog. No page over 2 s. Live engine run at boot: 6.01 s |
| Cold start | **Not observed.** The service was warm. The coordinator's ~30 s estimate is untested. Expect ~30 s spin-up plus a ~6 s first pipeline run |
| Durability on restart | **FAIL (by design on the free plan, but it needs saying).** `render.yaml` declares `plan: starter` with a disk at `/var/data`, but the live service is on the free plan with a different name (`ledgerline-finance-rig`, not `ledgerline-ar-operator`). The live /audit shows **0 human actions**, so earlier activity, if any, is already gone. On every deploy (autoDeploy on each push) and every idle spin-down (about 15 min), these are **all lost**: approvals, edits, sends, overrides, AM releases, card re-run decisions, chat history, rules changes (rules.json), and **the saved Loom link** (stored in SQLite `settings`; it survives only if `DEMO_VIDEO_URL` is set in Render env). Instructions accepted in Direct are appended to `app/engine/manuals/*.md` inside the container and revert to the repo version. The "append-only audit log" therefore isn't durable on live. Fix for the demo: set `DEMO_VIDEO_URL` in env, commit accepted instructions to the repo, and state "demo state resets on restart" on the RIG. For go-live: a paid instance plus a disk, or Postgres |
| Engine failure | `state.py` silently falls back to `fake_state` if the engine throws. The UI has a banner path, which was not triggered today. Worth a test so a reviewer never sees fake numbers unannounced |

## Defects ranked

**Sev-1:** none found. No wrong application of money, and no wrong chase produced by the agents.

**Sev-2** (guardrail bypass, policy gap, or would mislead Maya):
1. `app/web/views.py:535-536`: "Override hold" lifts DISPUTE / CANCELLATION holds without AM confirmation (D4).
2. `app/web/views.py:493-515`: send accepted on held invoices (D3) and to any "To" address (D2).
3. `app/web/views.py:276-300`: a partial rules POST disables top-50, auto-apply and AM-cc and empties the banned list (D5). Also, Priya alone can turn those guardrails off.
4. `app/engine/pipeline.py:74`: the floored `days_past_due` means no courtesy stage (16 invoices, $219,071) (B1).
5. RIG: /demo exposes internal video prep notes; live Maya count reads 5 (repo says 4); GitHub link 404 (E1–E3).
6. Live state is ephemeral, including the Loom link (F).

**Sev-3:**
- duplicate approvals (`views.py:443`);
- mislabelled HUMAN_WRITES group (`views.py:32`);
- the $10k cap is missing from the Cash manual and cards;
- UTC vs CST timestamps;
- "1 days";
- the Dana tile is truncated;
- `'???'` subject;
- `"court"` banned as a substring (`rules.py`). Use word boundaries in `controller.check_draft` (`controller.py:127-128`) and `views.py` send, or "courtesy" may be blocked one day.
