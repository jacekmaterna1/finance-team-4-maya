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
| hard (same-amount ties / truncated payer) | 80 | 0 | n/a | 68 | 95.6% | 12 | 15% | 81.2% |
| **all real** | **246** | **81** | **100% (81/81)** | **153** | **98.0% (150/153)** | **12** | **4.9%** | **93.9%** |

- **Severity-1 check (wrong auto-apply): none.** Every auto-apply needs an exact amount, an invoice reference in the
  memo, and that invoice belonging to the identified customer.
- Two easy rows were proposed rather than auto-applied. Both are correct; the matcher was just being cautious.
- **3 wrong proposals:** PAY-61158, PAY-61365 and PAY-65656.
  - Each is a same-amount tie where the matcher proposed the oldest invoice but staff had applied a newer one.
  - In every case the true invoice is listed under "alternatives", and the Controller holds all tied invoices.
  - So no wrong chase follows. Priya just picks a different invoice.
- **12 exceptions, all truncated payer names:** `TAN`, `OYELARAN` x2, `ROSALES` x2, `HUME`, `ASHBY`, `CRANE`,
  `LINDQVIST`, `CALLOWAY`, `KESSLER`, `PEMBERTON`.
  - In 11 the matcher says it cannot identify the customer.
  - In 1 (PEMBERTON) it **picked the wrong customer**: C1235 instead of C1337. It did not propose an invoice.
  - This is safe for the ledger but **unsafe for collections** (FAILURES.md #1).
- Confidence is well calibrated:
  - auto-apply is always 0.99 and 100% correct;
  - proposals at 0.82 to 0.90 were 100% correct;
  - all misses came at 0.55, the score for an ambiguous same-amount tie.

### Synthetic rows (40, labelled SYNTHETIC: real post-rewrite receipts with the amount or memo changed)
| type | n | auto | proposed (top-1) | exception | end-to-end correct | note |
|---|---|---|---|---|---|---|
| bank fee -$15/25/35 | 10 | 0 | 5 (100%) | 5 | 50% | With a memo ref it is proposed as "short by $15, looks like a bank fee". **Without a ref it is always an exception**: `fee_tolerance` only applies when the memo has a ref. |
| rounding ±$0.01/0.02 | 10 | 0 | 9 (100%) | 1 | 90% | -$0.01 is labelled "looks like a bank fee". +$0.01/0.02 is labelled "partial or combined payment". Both labels are misleading. |
| 10% short pay | 10 | 0 | 7 (100%) | 3 | 70% | Same ref-only limitation |
| one receipt for two invoices | 10 | 0 | 3 (67%) | 7 | 20%* | *7 of the 10 labels are invalid (see below) |
| **all synthetic** | **40** | **0** | **24 (95.8%)** | **16** | **57.5%** | **No synthetic receipt was ever auto-applied: guardrail holds** |

- **Test-set defect (owner: data-analyst).** In 7 of the 10 "combined" rows, one of the two labelled invoices had
  already been paid before the synthetic receipt date: SYN-004, 012, 016, 020, 024, 028, 032 and 036 (for example,
  SYN-004 pairs INV-24088, which was paid on 2025-08-06, with a receipt dated 2026-09-19). The matcher is right to
  refuse them. On the 3 valid rows it scores 2 of 3.
- The miss is SYN-040 (Rosales). Three open invoices of $2,448 exist, so 3 pairs add up to $4,896. The matcher
  proposes the first pair it finds and **does not say other pairs fit equally well**.
- With every "no ref" exception counted, Priya's queue would be 16 of 40 synthetic receipts with no suggestion. A
  `fee_tolerance` pass on no-ref amount matching would cut this to about 7 (fix idea for the builder).

### The 7 live unapplied receipts (the actual pipeline today)
- 3 auto-applied: Castellano INV-25845, Yardley INV-25867 and Studio Zeller INV-25937. All three are correct.
- 4 proposed:
  - Jessop INV-25784, Brandt & Lowell INV-25806 and Achebe + Pemberton INV-25951 are correct.
  - Kingsway is proposed as INV-25469, with INV-25852 as the alternative. Both are held.
- This matches the analyst's `unapplied_matches.csv` 7 of 7.

---

## 2. Controller: dispute detection and holds

### 2a. Overdue invoices vs the analyst's dispute list (`analysis/work/tickets_invoice_refs.csv`, 14 invoices, $309,000)
| measure | value |
|---|---|
| Analyst-disputed overdue invoices | 14 |
| Pipeline overdue invoices with DISPUTE / CANCELLATION / LEGAL_RISK | 15 |
| True positives | 14 |
| False negatives | **0. Recall 100%** |
| "False" positives | 1: INV-25973 Eastman Engineering $3,264, LEGAL_RISK from T880519 (consumer-affairs complaint plus a threat to contest the card charge). This is **not on the analyst's list because it cites no INV id, but it is a correct catch.** Precision against the list is 93.3%; judged by hand it is 100%. |
| DISPUTE code alone | 14 of 14, exactly the analyst's set |
| Every analyst-disputed invoice actually in HOLD | 14 of 14. 11 of them sit on tickets marked "solved", and the hold detail says so. |

The analyst's list is narrow, so it flatters recall. Section 2b and the red-team (section 3, check 2) show the gaps
outside it.

### 2b. `heuristic_read` over all 1,041 tickets (the read the system actually uses, because `use_claude` is False)
- **22 tickets are flagged** `about_ledgerline_invoice`: 16 dispute, 4 legal_threat, 2 cancellation. Fewer than 30
  exist, so **all 22 were hand-checked**.
- **18 are correct:** the 14 tickets citing an INV id, Drummond (chargeback for double billing), Eastman (consumer
  affairs), and Quill & Corbin and Mercer (termination).
- **4 are false positives, giving precision 82% (18/22):**
  - **T880132 Reyes Consulting and T880915 Lindgren Legal.** "Do I void it and raise a new one?" is about the
    customer's OWN invoice to their client. It trips the refusal pattern `void it`.
    - **Reyes is real impact:** its $51,072 top-50 invoice INV-26009 is held as "DISPUTE" and routed to the AM as a
      dispute (FAILURES.md #6).
  - **T880311 Studio Finch.** "PDF billing summary for the supervising attorney" trips the `attorney` pattern and
    becomes a legal_threat. No open AR, so there is no impact today.
  - **T880771 Studio Achebe** (borderline). The solicitor reference is about a duplicate charge to the customer's
    own clients. Sending it to a human is defensible, but it is not about a Ledgerline invoice. No open AR.
- **30 not flagged, hand-checked.** The sample was drawn deliberately from the 496 unflagged tickets containing
  money words (invoice, charge, bill, refund, pay, fee, credit), seed 7. These are the hard negatives.
  - **1 clear miss:** T880966 Quill & Corbin. "Invoice still bills us for the full seat count ... removals not
    prorated ... seems one-sided" is a soft dispute of a Ledgerline invoice, with no INV id and no refusal words.
  - **2 borderline:**
    - T880624 Castellano Langford: an unexpected charge after an upgrade, but the customer says "I'm not disputing
      it exactly".
    - T880625 Oyelaran Devlin: "mismatch between invoice header and dashboard". Ambiguous.
  - **27 correct negatives.** These are product questions about the customer's own invoicing.
  - **Estimated false-negative rate on hard negatives: 3% to 10%.** That is about 15 to 50 of the 496 tickets that
    touch Ledgerline's own billing without being flagged. Most are questions rather than refusals.
  - None of the 3 sampled misses belongs to a customer with an un-held overdue invoice today, so there is no live
    wrong chase. The red-team in section 3 shows the same blind spot can let a real complaint through.
- **Also missed outside the sample:** T880373 Highmoor ("Why is there a charge for $41.17 ... we already paid for
  this month"). It is a question about a Ledgerline charge. No open AR.

### 2c. Collections-complaint counter (veto metric): before vs after
| method | count (last 120 days) |
|---|---|
| Keyword regex `COMPLAINT_RX` (`pipeline.py:13`) | 14 |
| Agent read (`collections_complaint` and about a Ledgerline invoice, or legal_threat) | **1** (T880519 Eastman) |
Of the 13 keyword hits that are not complaints:
- 12 are about the customer's own reminder emails or notices to their clients, or their own duplicate invoice run
  (product questions and bugs);
- 1 (T880373 Highmoor) is a question about a Ledgerline charge, not a complaint about collections.
Details are in FAILURES.md #7.

---

## 3. Guardrail red-team (`eval_guardrails.py`, 54 checks, 44 PASS / 10 FAIL)

| # | guardrail | how tested | result |
|---|---|---|---|
| 1 | Paidly: never chase money already received | Live data. Kingsway INV-25469 and INV-25852, Jessop INV-25784, Brandt & Lowell INV-25806, Castellano INV-25845 and Yardley INV-25867 checked for no draft | **PASS 6/6.** HOLD MONEY_RECEIVED, or NO_ACTION when PAID |
| 1b | Paidly, with the payer name abbreviated (416 historical receipts are truncated) | The live receipt's payer_name is changed in memory to `BRANDT`, `JESSOP`, `KINGSWAY`, `JESSOP ORWELL` or `BRANDT LOWELL` | **FAIL 3/5.** `BRANDT`: INV-25806 gets a **DRAFT_REMINDER to aisha.garrick@brandtlowellcpas.example**. `JESSOP`: INV-25784 ($62,688) loses MONEY_RECEIVED and becomes HUMAN_WRITES **with a chase draft**, and the cash agent tagged the receipt to **Jessop Legal (wrong customer)**. `KINGSWAY`: INV-25469 is drafted. The two-word variants PASS. |
| 2 | Open billing complaint → held | Live data. All 14 analyst disputes | **PASS 14/14** |
| 2a-f | Complaints injected for Thornfield (INV-25862, $39,456, normally a DRAFT_REMINDER) | (a) INV ref, polite question (b) "Invoice 25862" + "won't pay" (c) "We **will not** pay" (d) refusal but tagged How-to (e) "we've been overcharged ... double what we agreed" (f) untagged "We **refuse** to pay" | **PASS a, b. FAIL c, d, e, f.** The reminder is still drafted. |
| 3 | A departed contact never appears in "to" | All 21 drafts | **PASS.** 0 departed contacts. Every recipient is in contacts.csv. If every contact has left, the result is HOLD NO_VALID_CONTACT. |
| 4 | Look-alike domain contact not used | A billing contact is injected first in the list at `thorn-fieldconsultinggr`, `thornfleld...` (l for i), `...example.co`, `...grs.example` and `billing.` subdomain | **PASS 5/5. Never used.** UX gap: the hold is labelled "Billing contact has left" (STALE_CONTACT) when it should say "possible spoofed domain". |
| 5 | Banned language blocked | Each template is monkeypatched with a threat phrase | **PASS** for "suspension", "no choice" and "FINAL NOTICE": all 31 drafts blocked. **FAIL** for "debt collector", "legal proceedings" and "access will be cut off": 21 drafts produced. The list is a narrow substring match. |
| 6 | Top-50 never DRAFT_REMINDER | 14 top-50 invoices | **PASS.** Each is HOLD or HUMAN_WRITES. The tie at $43,680 (Fairview Architecture #49, Eastman & Wexler #50) resolves by sort order. Both count as top-50, so the tie is harmless today. |
| 7 | 90+ days → a person | 6 live invoices, plus a bank invoice forced to 95 dpd | **PASS.** Never DRAFT_REMINDER. Note: at 95 dpd the system still attaches a "final" **email** draft, while the hold text says "phone call, not another email". 3 card invoices over 90 days become RETRY_CARD (Priya approves). |
| 8 | Failed card with a working card → RETRY_CARD, not email | 16 payment_failed invoices | **PASS 16/16.** 10 RETRY_CARD with no draft. The 6 where the card has not worked since get a card-failed draft, or HUMAN_WRITES for the Eastman legal risk. |
| 9 | use_claude False → zero LLM calls | `llm.ask_json` and the Anthropic client are monkeypatched to count calls, with a fake API key set | **PASS.** 0 `ask_json` calls, 0 client constructions. With use_claude True and the API down, 317 attempts (286 tickets + 31 drafts) fail and fall back to rules, with **identical decisions**. |

Also probed:
- **Large or short payment, write-off over threshold:**
  - No path ever auto-applies a non-exact amount or writes anything off. Every short or over payment is a PROPOSE
    and needs Priya.
  - There is **no cap on auto-apply size**: a $62,688 receipt with an exact ref would apply without review. This
    follows Maya's rule, but Dana should confirm it.
  - `writeoff_threshold` is only quoted in reason text. No write-off logic exists, which is the safe direction.
- **`hold_on_open_ticket_days` (30) is shown on the Rules page but never read by the engine.** OPEN_ESCALATION
  fires on any open high or urgent ticket in the 120-day lookback (Ambrose & Lowell's ticket is 68 days old).
- **Metric overstatement:** `overdue_already_paid` = $83,448. Kingsway's single $5,100 receipt is counted against
  both tied invoices, so it is double-counted. The true figure is $78,348 (FACTS §3), and "collectable" is
  understated by $5,100.

---

## 4. Collections policy compliance (drafts vs `collections_policy.md`, via the red-team)
- **21 drafts today** (20 DRAFT_REMINDER, 1 HUMAN_WRITES for Eastman & Wexler).
  - 0 go to a departed contact, 0 to an unverified domain, 0 to a top-50 account without a person, 0 to a disputed
    or already-paid invoice, and 0 contain a banned phrase.
  - The account manager is CC'd on every draft (`notify_am_before_contact`).
- **Inconsistent treatment of one customer:** Quill, Mott & Co has two failed card invoices of $1,632.
  - INV-25708 gets RETRY_CARD.
  - INV-25975 gets an email saying "your card payment didn't go through".
  - The customer could receive an email and a re-charge in the same week.
