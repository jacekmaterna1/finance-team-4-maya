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

- **F** Quarter on quarter, the claim is **false**. Overdue goes up, down, up, down, up: 221k → 494k → 209k → 600k. It is strongly seasonal. Month-end peaks fall in Feb-Mar and Aug-Oct, which are the annual-renewal billing waves.
- **F** Year on year, the claim is **true** for three straight quarters:
  - Q1: 423k → 494k (+17%)
  - Q2: 149k → 209k (+41%)
  - Q3: 488k → 600k (+23%)
  - October: 597k → 633k (+6%)
- **F** Part of reported "overdue" at each quarter end was cash already in the bank but not yet applied: $57k (Q3'25), $73k (Q4'25), **$210k (Q1'26, 43% of reported overdue)**, $75k (Q2'26) and $71k (Q3'26).
- **I** The board's line "overdue rose for three quarters" is defensible only as a year-on-year statement. A sequential chart would show a sawtooth. Cash-application lag inflates the quarter-end number.

## 3. Unapplied receipts ("chased for money we already have")
Method: payments with blank invoice_id. Payer is resolved to a customer by normalised exact name (letters and digits only, lower-cased). Candidates are that customer's open, overdue or failed invoices issued on or before received_date. A match needs an exact amount, or a memo invoice ref plus amount. Tolerance matching was not needed: every match is exact. Output: `analysis/work/unapplied_matches.csv`.

- **F** **7 unapplied receipts, $87,335**: ACH 5 / $75,663, wire 2 / $11,672. All 7 were received 2026-10-17..10-31, and all 7 have a plausible open invoice.
- **F** **5 match an invoice shown OVERDUE: $78,348 across 5 customers.** 2 match invoices not yet due ($8,987).

| payment | received | $ | payer_name / memo | matches | status | dpd | how |
|---|---|---|---|---|---|---|---|
| PAY-65750 | 10-17 | 62,688 | Jessop & Orwell Agency / "Jessop payment" | INV-25784 (C1273, **top-50**) | overdue | 36 | exact name + unique amount; memo surname fits 8 customers |
| PAY-65766 | 10-19 | 6,324 | BRANDT & LOWELL CPAS / "Ledgerline subscription" | INV-25806 (C1126) | overdue | 28 | uppercase name + unique amount |
| PAY-65805 | 10-29 | 5,100 | Kingsway Engineering Group / (blank) | INV-25469 **or** INV-25852 (C1469) | overdue | 111 / 19 | AMBIGUOUS: two $5,100 overdue invoices |
| PAY-65806 | 10-30 | 3,672 | Castellano, Crane & Co / "INV-25845" | INV-25845 (C1188) | overdue | 20 | memo ref |
| PAY-65808 | 10-31 | 564 | YARDLEY & DUARTE ADVISORY / "inv25867 Yardley" | INV-25867 (C1346) | overdue | 16 | memo ref (INV-26000 also $564, open) |
| PAY-65796 | 10-27 | 8,000 | ACHEBE + PEMBERTON ARCHITECTS / (blank) | INV-25951 (C1505, top-50) | open | -4 | uppercase name + unique amount (implementation fee) |
| PAY-65807 | 10-30 | 987 | Studio Zeller / "Invoice 25937" | INV-25937 (C1223) | open | -2 | memo ref |

- **F** Jessop & Orwell's $62,688 has gone unapplied for 14 calendar days (10 working days). Policy says 3 to 5 working days. The historical maximum ACH lag is 19 days.
- **F, historical scale.** Application lag (applied_date - received_date, calendar days) is 0 for card. For ACH the mean is 4.7 (max 19), for wire 6.9 (max 21) and for check 8.1 (max 23). It has been flat since 2022.
  - Of 2,559 bank-paid invoices, **434 ($4.95M) were paid on time in cash but recorded late in the ledger**.
  - If reminders had run on the policy schedule (+7/+21/+45), **572 invoices ($7.22M) would have been chased at least once after the cash had arrived**. That is 112 invoices / $1.63M with due dates in the last 12 months. There is no reminder log, so this is the exposure, not proof that emails were sent.

## 4. Payment matching patterns (for the FIN-2 matcher)
- **F** Memo formats, by count:
  - `Stripe charge INV-#####` 3,242 (all card, auto-applied same day)
  - `INV-#####` 999
  - `Invoice #####` 571
  - `inv##### <Surname>` about 300
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
- **I** A matcher built only on history would never see these cases. The test set therefore adds clearly marked synthetic perturbations (section 10).

## 5. Overdue invoices with support tickets
Window: tickets that are open or pending at any date, or created 2026-10-01..10-31 (last 30 days). Output: `analysis/work/open_ar_flags.csv`.
- **F** Overdue with an open-or-recent ticket: **29 invoices / $483,342 / 28 customers** (76% of overdue $).
- **F** With an *open/pending* ticket: 13 / $188,365.
- **F** With an open/recent ticket tagged Billing: 8 / $200,828.
- **F** With an open/pending high or urgent ticket (our proxy for "escalation", since there is no escalation field): 3 / $90,130.
  - Westbrook Engineering Group INV-25730 $47,904
  - Delacroix, Jessop & Co INV-25834 $41,568
  - Ambrose & Lowell Advisory INV-25897 $658
- **F** Overdue with any Billing ticket in Jul-Oct: 21 / $326,679.
- **I** The 30-day window misses most disputes. Several dispute tickets are older than 30 days and marked solved (section 8). Use the invoice reference, not ticket recency.

## 6. Failed card payments
- **F** How they appear:
  - invoices `status=payment_failed` (card only, due date = issue date)
  - card invoices `paid` with paid_date > issue_date: a retry worked, 131 historically, 3-10 days later
  - `written_off`: never recovered, written off at exactly 150 days (all 144 cases)
  - There are no failed-attempt rows in payments.csv.
- **F** Currently **16 payment_failed / $16,455** (15 customers, all active; Quill, Mott & Co has 2). For **10 of them ($9,209)** the same customer's *later* card invoices were charged successfully, so the card on file works and the failed invoice was never re-run.
- **F** Auto write-offs coming up:
  - **Northgate Creative INV-25433 $799 on 2026-11-01 (tomorrow)**
  - Hollis Nair Engineers INV-25470 $517 on 11-09
  - Studio Nakamura INV-25622 $517 on 12-15
- **F** History: **144 card invoices written off, $159,192**, 47 / $71,995 of them in the last 12 months. **143 of 144** belonged to customers who later paid other card invoices successfully.
- **F** Post-rewrite (from 16 Mar 2026), 22 recovered late, 8 written off and 16 still failed. Pre-rewrite 2026 was 11 / 8 / 0. Recovery delay is unchanged (mean 6.4 vs 6.6 days).
- **F** Follow-up evidence: there is no dunning or reminder log in the data. Only about 13 tickets mention declines or retries, and most concern the customer's own clients' cards.
- **I** Failed cards are not followed up by people. Recovery happens only through automatic retries or the customer, which matches FIN-1's "rarely followed up".

## 7. Top-50 accounts among overdue
- **F** Top-50 = top 50 customers by customers.current_arr. The cutoff is $43,680 and 2 accounts are tied at it.
- **F** **6 overdue top-50 invoices, $305,760 (48% of overdue $)**:
  - Jessop & Orwell $62,688: unapplied cash
  - Riverside Partners $60,576: disputed
  - Westbrook Engineering Group $47,904: disputed
  - Okafor & Nakamura $46,848: disputed
  - Upton & Bell $44,064: disputed
  - Eastman & Wexler $43,680: sits on the tie at the cutoff
- **I** 5 of the 6 should NOT get a reminder at all: 4 are disputed and 1 is already paid.

## 8. Disputes
- **F** There is no dispute status or field. Disputes appear only as ticket text that cites a Ledgerline invoice id. **14 tickets cite an INV id, and all 14 invoices are currently overdue: $309,000 = 49% of overdue $.** Output: `analysis/work/tickets_invoice_refs.csv`.
- **F** 11 of the 14 tickets are marked `solved`, yet each invoice is unchanged and still overdue. The ticket was closed but the corrected invoice was never issued.
- **F** 4 of 14 (29%) are not tagged Billing (How-to 2, Account change 1, blank 1). A category filter would miss them.
- **F** The dispute reasons are setup and contract errors:
  - implementation fee meant to be waived (Westbrook INV-25730 $47,904)
  - seats double-counted after a workspace merge (Riverside INV-25787 $60,576)
  - missing second-office discount (Okafor & Nakamura INV-25765 $46,848)
  - late fee after a card outage on Ledgerline's side (Upton & Bell INV-25662 $44,064)
  - departed users still billed (Delacroix, Jessop INV-25834 $41,568)
  - annual renewal billed after a move to monthly (Brandt Ashby IT INV-25822 $26,112)
  - wrong sales-tax address (Ellery INV-25757 $13,056)
  - VAT charged wrongly (Thackeray INV-25750 $7,896)
  - full Pro month after a downgrade (Castell INV-25764 $6,324)
  - wrong seat count (Wexler & Hume INV-25712 $4,080)
  - cancelled module still billed (Mercer & Banerjee INV-25718 $3,876; Banerjee Petrov INV-25539 $2,652)
  - migration fee meant to be waived (Oyelaran Devlin INV-25711 $2,820)
  - renewal discount missing (Wexler Media INV-25811 $1,224)
- **F, March 2026 rewrite link: weak in Ledgerline's own AR.** None of the 14 disputes mention the rewrite, and Ledgerline's own invoices have no cent amounts.
  - Tickets that match rewrite themes (rounding 17, proration 36, card retry 13, credit note / duplicate 38, settings moved 43) mostly concern the customer's own invoicing to their clients.
  - Examples: T880180 Westbrook ("itemised charges and total differ by the smallest currency unit", high, pending since 07-20), T880184 Kingsway ("portal 1,950.00 AUD but PDF 1,949.99", pending since 07-20), T880643 Studio Marsh (due date shows 14th, not 15th, which fits the time-zone change).
- **I** Possibly rewrite-related disputes: Castell (plan change mid-cycle, where proration rules changed) and Brandt Ashby (frequency change). Treat this as unproven.

## 9. Billing contacts
- **F** 52 contacts are `left the firm; still on invoice emails`. Every customer still has at least 1 active billing contact. Email domain matches the customer website for 100% of contacts and ticket requesters, so the domain-mismatch trap is absent.
- **F** 5 overdue invoices ($14,058) belong to customers whose billing contacts include one who has left:
  - Wexler & Hume INV-25712 $4,080, also disputed
  - Mercer & Banerjee INV-25718 $3,876, also disputed
  - Oyelaran Strategy INV-25890 $4,692
  - Ellery Achebe CA INV-25912 $799, card failed
  - Bramwell Sinclair CA INV-25969 $611, card failed

## 10. Collections policy vs what happened
| rule | evidence |
|---|---|
| Don't chase disputed invoices | 14 disputed overdue invoices, $309k. 11 have the ticket "solved" with the invoice uncorrected, so finance cannot tell they are still disputed (F). No reminder log exists, so we cannot show reminders were sent (F). |
| Don't chase open escalation | 3 overdue invoices ($90k) with open high/urgent tickets (proxy) (F) |
| Top-50 need a human | 6 overdue, $305,760 (F) |
| Write-offs <= $2k by VP Finance; card auto write-off at 150d | 150-day rule applied exactly (144/144) (F). **9 auto write-offs exceeded $2,000 ($47,251) with no evidence of approval.** The two rules conflict (F/I). |
| Cash applied in 3-5 working days | Median ACH 3, wire 5, check 6 calendar days. Tail up to 23 days. Jessop's $62,688 is at 10 working days today (F). |
| Reminders at -5/+7/+21/+45 | Not testable: no email log (F) |

## 11. Data-quality traps
1. `paid_date` is set on written_off invoices (it is the write-off date). Do not treat paid_date non-null as paid.
2. paid_date = applied date, not cash date. Use payments.received_date for "when did the money arrive".
3. Card invoices are due on the issue date; policy text says 30 days. `open` in ar_aging means not yet due.
4. Payer names: UPPERCASE and truncated variants, and many customers share surnames. Match on normalised name plus amount plus memo, never surname alone.
5. Ticket times are US Central; due dates are date-only. After the rewrite, due dates follow the firm's time zone, which can shift by a day for UK and Canada customers (I).
6. Many "Billing" tickets are about customers' own client invoices. Only the 14 INV-referencing tickets are about Ledgerline AR.
7. Top-50 boundary tie at $43,680.
8. The brief's expected cash-app traps (fees, short or combined payments, cent diffs) do not occur in this data.
9. Ledger state was rebuilt from applied dates. There are no historical status snapshots, so quarter-end figures are reconstructions.

## 12. Test set: `analysis/testset_cash_app.csv` (286 rows)
Columns: payment_id, received_date, amount, method, payer_name, memo, true_invoice_ids (`|`-separated if several), label_source, difficulty, difficulty_reason, n_candidate_customers, n_open_same_amount, is_synthetic.

How the labels were made:
- **ledger_applied (239 rows)**: the invoice_id staff applied in payments.csv. The memo ref, where present, agrees in 100% of cases.
  - All 80 "hard" bank receipts: no memo ref, plus either 2 or more same-amount open invoices or a drifted payer name that fits 3 to 9 customers.
  - 80 sampled "medium": no memo ref, unique exact amount.
  - 60 sampled "easy": memo ref.
  - 20 card ("trivial", Stripe memo).
- **inferred (7 rows)**: the unapplied receipts, labelled by memo ref or a unique exact amount for the named payer. PAY-65805 (Kingsway) carries both INV-25469|INV-25852; oldest-first is the house convention (91% historically), so accept either.
- **synthetic_perturbation (40 rows, SYN-###)**: real post-rewrite bank receipts with the amount or memo changed. Each type has 10 rows:
  - bank fee −$15/25/35
  - cent rounding ±$0.01/0.02
  - 10% short pay
  - one receipt covering two invoices (memo ref removed)
  
  The label is inherited from the ledger. These test traps that are absent from the real data.

Limits:
- The ledger labels assume staff applied correctly. In the 75 ambiguous same-amount cases, 7 were not applied to the oldest invoice. They could be errors or deliberate choices, so judge with care.
- Candidate sets use exact normalised-name or prefix matching. A matcher with better fuzzy matching may find candidates this set does not count.
- Synthetic rows are realistic but invented. Report scores on real and synthetic rows separately.
- For a fair test, the matcher should see only invoices open as of each payment's received_date (rebuild using the applied dates).
