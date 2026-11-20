# EVAL: how well the agents work on the real records

QA Evaluator. **Updated 2026-11-20 at 12:20 CST (QA pass 2)** against the current code. That code includes:
- the severity-1 fix for unidentified payers;
- a stricter fuzzy match;
- strong refusals read in any ticket category;
- the Reyes fix;
- a $10k auto-apply cap;
- top-50 not-due → NO_ACTION;
- card re-runs blocked on legal threats.

The first pass (11:36) is superseded. Its numbers appear below only as "was". Nothing in `app/` or `data/` was
changed. Data as of 2026-10-31.

| script | what it does | output |
|---|---|---|
| `analysis/scripts/eval_cash_app.py` | replays 286 test payments against the invoice book as it stood on each received date | `analysis/work/eval_cash_app_results.csv`, `.log` |
| `analysis/scripts/eval_controller.py` | dispute detection vs the analyst's list; reads all 1,041 tickets | `analysis/work/eval_ticket_reads.csv`, `.log` |
| `analysis/scripts/eval_guardrails.py` | red-team on changed copies of the data held in memory | `analysis/work/eval_guardrails_results.csv`, `.log` |
| `analysis/scripts/eval_policy.py` | FIN-1 policy check on every invoice | `analysis/work/eval_policy_results.csv`, `.log` |
| `analysis/scripts/eval_web.py <tmpdir>` | screen consistency and human-action flows via TestClient | `analysis/work/eval_web_results.csv`, `.log` |

**Headline**
- **Cash application:** 0 wrong automatic applications (59 of 59 correct on real data). Proposals put the right
  invoice first 98.3% of the time.
- **Dispute detection:** recall 100% on the analyst's 14 disputes.
- **Guardrail red-team: 54 of 54 pass** (was 44 of 54).
- **FIN-1 policy check: 11 of 12 pass.** The courtesy note 5 days before the due date never fires.
- **Approval UI: 22 of 27 flows pass.** Three server-side bypasses remain. See `analysis/QA_PASS_2.md`.

---

## 1. Cash Application (`analysis/testset_cash_app.csv`, 286 rows)

**Harness.** For each payment, the invoice book is rebuilt as of the receipt date. An invoice is open if
`issue_date <= received_date` and (`paid_date` is blank or `paid_date >= received_date`). The production
`cash_app.run()` is called unchanged with DEFAULT_RULES. An answer is correct when the proposed invoice set equals the
label. For PAY-65805 (Kingsway), which is ambiguous, either invoice is accepted.

### Real rows (246)
| difficulty | n | auto-applied | auto precision | proposed | proposal top-1 | exception | end-to-end correct |
|---|---|---|---|---|---|---|---|
| trivial (card) | 20 | 20 | 100% | 0 | n/a | 0 | 100% |
| easy (memo ref) | 63 | 39 | 100% | 24 | 100% | 0 | 100% |
| medium (no ref, unique amount) | 83 | 0 | n/a | 83 | 100% | 0 | 100% |
| hard (same-amount ties / truncated payer) | 80 | 0 | n/a | 68 | 95.6% | 12 | 81.2% |
| **all real** | **246** | **59** | **100% (59/59)** | **175** | **98.3% (172/175)** | **12 (4.9%)** | **93.9%** |

- **No wrong auto-apply, so no severity-1.**
- **What the $10k cap changed.** Real auto-applies went from 81 to 59.
  - The 22 exact-reference receipts over $10,000 are now proposals at confidence 0.95, and all 22 are correct.
  - Nothing became wrong. Priya simply confirms 22 more items, each a one-click confirmation.
  - The live book is unaffected: its 3 auto-applies are $564, $987 and $3,672.
- **3 wrong proposals (unchanged):** PAY-61158, PAY-61365 and PAY-65656.
  - Each is a same-amount tie where staff applied a newer invoice than the oldest.
  - The true invoice is always in "alternatives", and all tied invoices are held.
- **12 exceptions, all truncated payer names** (`TAN`, `OYELARAN` x2, `ROSALES` x2, `HUME`, `ASHBY`, `CRANE`,
  `LINDQVIST`, `CALLOWAY`, `KESSLER`, `PEMBERTON`).
  - **None is now assigned to a wrong customer.** Before the fix, PEMBERTON went to C1235.
  - The Controller now holds any open invoice with the same amount (`controller.py:36-43`).
- Confidence calibration is unchanged:
  - auto-apply is 0.99 and 100% correct;
  - proposals at 0.82 to 0.95 are 100% correct;
  - all misses came at 0.55.

### Synthetic rows (40, SYNTHETIC: real receipts with amounts or memos changed)
| type | n | auto | proposed (top-1) | exception | end-to-end correct |
|---|---|---|---|---|---|
| bank fee -$15/25/35 | 10 | 0 | 5 (100%) | 5 | 50% |
| rounding ±$0.01/0.02 | 10 | 0 | 9 (100%) | 1 | 90% |
| 10% short pay | 10 | 0 | 7 (100%) | 3 | 70% |
| one receipt for two invoices | 10 | 0 | 3 (67%) | 7 | 20%* |
| **all synthetic** | **40** | **0** | **24 (95.8%)** | **16** | **57.5%** |

- No synthetic receipt is ever auto-applied.
- Bank fees and short payments **without a memo ref** are still always exceptions, because `fee_tolerance` only
  applies on the reference path (FAILURES #12).
- *Test-set defect: 7 of the 10 "combined" labels pair an invoice that had already been paid before the receipt
  date. The matcher is right to refuse them. On the 3 valid rows it scores 2 of 3.

### The 7 live unapplied receipts
- **3 auto-applied, all correct:** Castellano INV-25845, Yardley INV-25867 and Studio Zeller INV-25937.
- **4 proposed:**
  - Jessop INV-25784, Brandt & Lowell INV-25806 and Achebe + Pemberton INV-25951 are correct.
  - Kingsway is proposed as INV-25469, with INV-25852 as the alternative. Both are held.
- **"Already received" is now $78,348.** Kingsway's single receipt is counted once (was $83,448).

---

## 2. Controller: dispute detection and holds

### 2a. Overdue invoices vs the analyst's list (`analysis/work/tickets_invoice_refs.csv`, 14 invoices, $309,000)
| measure | value |
|---|---|
| Pipeline overdue invoices with DISPUTE / CANCELLATION / LEGAL_RISK | 16 |
| True positives / false negatives | 14 / **0. Recall 100%** |
| Outside the list | 2 correct catches, both LEGAL_RISK with no INV id: INV-25973 Eastman Engineering (consumer affairs, contest the charge) and **INV-25769 Drummond Consulting (chargeback for double billing, T880019, now read; previously missed)**. Precision against the list is 87.5%; judged by hand it is 100% |
| DISPUTE code alone | 14 of 14, all in HOLD (11 on tickets marked "solved") |

### 2b. `heuristic_read` over all 1,041 tickets (the read in use while `use_claude` is False)
- **21 are flagged** `about_ledgerline_invoice` (was 22): 15 dispute, 4 legal_threat, 2 cancellation. All 21 were
  hand-checked.
- **19 correct, giving precision 90%** (was 82%).
  - **Fixed:** Reyes T880132 and Lindgren T880915, which were questions about voiding their own client invoices. Reyes's
    $51,072 invoice is no longer held as a dispute.
  - **New flag:** T880142 Tan Zeller ("formal complaint about the overcharging on our retainers"). This is a plausible
    true positive.
- **Still false positives:**
  - T880311 Studio Finch: "attorney" in a PDF question.
  - T880771 Studio Achebe: a solicitor reference about a duplicate charge to the customer's own clients.
  - Neither customer has open AR.
- **Not flagged.** The earlier hand-check of 30 hard negatives still applies. Of those, T880966 (Quill & Corbin,
  seat proration), T880624 and T880625 remain unflagged. The estimated false-negative rate stays at 3% to 10% of the
  498 unflagged tickets that contain money words. None belongs to a customer with an un-held overdue invoice.

### 2c. Collections-complaint counter (veto metric)
| method | count (last 120 days) |
|---|---|
| Keyword regex `COMPLAINT_RX` (`pipeline.py:13`) | 14 |
| Agent read (current) | **2:** T880519 Eastman, plus T880019 Drummond (chargeback, now counted as a legal threat) |
- The 12 keyword hits that are neither of those concern the customers' own reminder emails, notices or invoice runs to
  their clients.
- 1 more (T880373 Highmoor) is a question about a Ledgerline charge.

---

## 3. Guardrail red-team (`eval_guardrails.py`): 54 PASS / 0 FAIL (was 44 / 10)

| # | guardrail | result |
|---|---|---|
| 1 | Paidly, live receipts (Kingsway x2, Jessop, Brandt & Lowell, Castellano, Yardley) | PASS 6/6 |
| 1b | Paidly with the payer shortened (`BRANDT`, `JESSOP`, `KINGSWAY`, `JESSOP ORWELL`, `BRANDT LOWELL`) | **PASS 5/5** (was 2/5). Held as "possible payment from an unidentified payer" |
| 2 | 14 analyst disputes held, plus 6 injected complaint wordings ("will not pay", "refuse to pay", How-to tag, polite overcharge, ...) | **PASS 20/20** (was 16/20) |
| 3 | No departed contact in "to"; every recipient in contacts.csv; all contacts left → NO_VALID_CONTACT | PASS |
| 4 | Look-alike domains (5 variants) never used | PASS (the hold is still labelled "Billing contact has left") |
| 5 | Banned language: suspension, no choice, FINAL NOTICE, debt collector, legal proceedings, cut off | **PASS 6/6** (was 3/6) |
| 6 | Top-50 never DRAFT_REMINDER (14 invoices) | PASS |
| 7 | 90+ days never DRAFT_REMINDER; bank invoice forced to 95 dpd → HUMAN_WRITES | PASS |
| 8 | Failed card: re-run only if the card works and there is no hard hold or legal risk (16 invoices) | PASS. Drummond is now HUMAN_WRITES / LEGAL_RISK instead of a re-run |
| 9 | `use_claude` False → 0 LLM calls; True with the API down → same decisions | PASS |

**Not covered by the engine red-team: the approval UI.** Run through the web app, three guardrails can still be
bypassed (QA_PASS_2 §D):
- "Override hold" lifts a DISPUTE hold without AM confirmation;
- a send is accepted on a held invoice or to any typed address;
- a partial rules POST switches the top-50 and banned-list guardrails off.

---

## 4. Collections policy compliance (all 117 invoices; `eval_policy.py`): 11 of 12 pass
- **Drafts:** 21 (20 reminders + 1 to be written by a person).
- **Every draft passes:**
  - 0 banned phrases, 0 departed or unverified recipients, AM cc'd on all;
  - invoice id, amount and due date match the ledger, and every draft is signed by Priya;
  - none sits on a PAID, MONEY_RECEIVED, DISPUTE, CANCELLATION, LEGAL_RISK or OPEN_ESCALATION invoice;
  - none goes to a top-50 account.
- **9 card re-runs**, each with a later successful card charge and no hard hold.
- **3 Dana decisions**, exactly the expected set: Eastman $3,264 over $2k, Northgate (1 day left), Hollis Nair (9 days
  left).
- **FAIL: the courtesy stage never fires.**
  - `ar_aging.days_past_due` is floored at 0, and the pipeline uses it (`pipeline.py:74`).
  - So **16 invoices ($219,071) due within 5 days get no courtesy note**, and 61 not-yet-due invoices say "Next
    reminder at day 7".
  - All 56 past-due invoices are staged correctly.
- **Still open from pass 1:** Quill, Mott & Co has two failed $1,632 card invoices. One gets a re-run, the other a
  card-failed email.

## 5. Current pipeline metrics (`run_pipeline()`, 12:20 CST); identical on Home, Today, Collections, Digest, chat and Team
| metric | value |
|---|---|
| Overdue | $633,245 (54 invoices) |
| Already received | $78,348 |
| Disputed | $312,922 |
| Collectable | $241,975 |
| Chases prevented | 23 |
| Held | 21 |
| Drafts | 20 |
| Person writes | 3 |
| Card re-runs | 9 |
| Dana decisions | 3 |
| Payments | 3 auto, 4 to confirm |
| Complaint baseline | 2 (keyword count 14) |
