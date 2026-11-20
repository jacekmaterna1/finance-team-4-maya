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
| INV-25765 | Okafor & Nakamura (top-50) | 46,848 | 50% off 3 months for second office | **Can't tell.** There is no contract change for a second office (33 seats, flat since 2023). A discount over 10% needs the Head of Sales and is first-year only. | ≤ $5,856 |
| INV-25764 | Castell Eng. | 6,324 | downgraded "pro→standard", billed a full month | **We're right per contract**: Growth, 31 seats, until 2027-02-22. No plans called pro or standard exist. The invoice is quarterly (08-23), and the downgrade date (10-03) is after it. After the rewrite, a plan change goes on the *next* invoice. | about $1,070 on the next invoice |
| INV-25822 | Brandt Ashby IT | 26,112 | moved annual Enterprise→monthly "Team" | **We're right on the amount**: the plan is Growth, there is no "Team" plan, and the record says annual billing. **Can't verify** the confirmation screen they mention. | $0 revenue. If proven: void and rebill 12 × $2,176 (cash timing only) |
| INV-25750 | Thackeray Accounting | 7,896 | 20% VAT added, should be reverse charge | **Can't tell**: tax is excluded from all amounts in the data. The base amount is correct. The customer record says **United States**, so a VAT reverse charge is implausible: either the master record or the tax engine is wrong. | tax line only (about $1,579 if 20% was charged) |
| INV-25757 | Ellery Consulting | 13,056 | sales tax on old address | **Can't tell** (tax not in data). Base amount is correct. | rate difference only |
| INV-25811 | Wexler Media | 1,224 | 15% multi-year discount | **We're right**: pricing says multi-year discounts are not offered, they renewed at list price, and they are billed monthly, not annually. | $183.60/month if an AM overrode policy |
| INV-25718 | Mercer & Banerjee | 3,876 | time-tracking module cancelled | **We're right**: there are no priced modules, and 19×68×3 = 3,876. **Separate risk:** termination notice T880514 ("discontinuing… effect from 30 June", Billing, solved) is not reflected anywhere. Renewal is 2026-11-12. | the next renewal invoice ($3,876/quarter) is at risk |
| INV-25662 | Upton & Bell (top-50) | 44,064 | late fee after a card outage on our side | **We're right**: 54×68×12 exactly, with no late fee in the ledger. The customer pays by **wire**, not card. | $0 |
| INV-25711 | Oyelaran Devlin | 2,820 | migration fee should have been waived | **We're right**: 20×47×3 exactly. No migration-fee item exists. | $0 |
| INV-25539 | Banerjee Petrov | 2,652 | portal fee + setup line | **We're right**: the portal is included in Core/Growth, and 13×68×3 = 2,652. Usage shows the portal still **in use** Jul–Oct. | $0 |
| INV-25834 | Delacroix, Jessop & Co | 41,568 | 3 seats for leavers | **We're right per contract**: renewed at 28 seats on 09-09, with 23–27 active users. Can't tell whether they asked to reduce. | $3,168 |
| INV-26009 | Reyes Consulting | 51,072 | — | **FALSE POSITIVE (QA agent is correct).** T880132 (07-15) is about Reyes's own client invoice and predates INV-26009 (issued 10-17). It has no INV reference. The invoice is open and due 11-16. | — |

- Sum of exposure upper bounds if every claim were proven (I): about $25k, including a $1.6k VAT estimate but not Ellery's unknown tax difference. That compares with **$309,000** of overdue invoices on hold over these disputes.
- **I** "Held → fix": 9 of the 14 can be released with a contract-evidence reply. The ledger cannot settle the other 5; each needs one AM or tax decision:
  - Riverside: seat expansion
  - Okafor & Nakamura: verbal discount
  - Thackeray: country or VAT
  - Ellery: tax address
  - Brandt Ashby: billing-frequency change
- **I** These customers' claims often contradict our own master data: wrong plan names, wrong payment method, wrong country. Either the claims are mistaken, or the invoice PDF and the data room disagree. Before sending, finance should pull one PDF (for example INV-25730) to confirm which.
- **Correction to FACTS.md:** the dispute count stays at 14 / $309,000. Reyes was never in my 14; Delacroix is in it.

## 2. AR tie-out — `work/check2_ar_tieout.csv`
- **F** At 2026-10-31, ar_aging total = invoices open/overdue/payment_failed = balance sheet `accounts_receivable` = **$1,430,632**. Gap: $0.
- **F** Balance sheet `unapplied_cash_receipts` = **$87,335** = the 7 payments with no invoice_id. It is carried as a liability, not netted against AR.
- **F** I rebuilt open AR and unapplied cash at every month end from invoice and payment dates. Both tie to the balance sheet to the dollar in **46/46 months**.
- **F** Unapplied cash at month end swings widely: $29k (Apr-26), $233k (Mar-26), $226k (Aug-26). This is the application lag.
- **I** Net receivable is $1,430,632 − $87,335 = **$1,343,297**. AR is overstated by the unapplied cash until it is applied. There are no credit notes in the data, so none can explain a gap.

## 3. Overpayments, duplicates, credits owed, cross-customer application — `work/check3_*.csv`
- **F** Every applied payment exactly equals its invoice amount: 0 overpayments, 0 underpayments.
- **F** No duplicate receipts by (payer, amount, date) or (payer, amount, invoice memo), and no payment received before its invoice was issued.
- **F** Cross-customer: 0 payments whose payer name exactly matches a *different* customer from the one on the invoice. All 5,801 payer names are the invoice customer's name, upper-cased or truncated. `check3_cross_customer.csv` is empty.
- **F** Churned customers: 0 invoices issued on or after the churn date, 0 service periods running more than a month past churn, 0 open AR.
- **F, gap:** tickets mention refunds and duplicate charges, but the data room has no refund or credit-note records, so they cannot be verified:
  - T880946 Wexler & Hume: refund sent to a cancelled card
  - T881021 Studio Marsh: duplicate refund not received
  - T880126 C1377: double charge
- **I** The only money owed to or held for customers in the data is the $87,335 of unapplied receipts.

## 4. Write-offs vs policy — `work/check4_writeoffs.csv`
- **F** 144 write-offs totalling $159,192. All are card invoices, all at exactly 150 days. **0 non-card write-offs.**
- **F** **9 auto write-offs over the $2,000 VP Finance limit, $47,251 in total**, with no approval evidence:

| invoice | customer | $ | written off | customer now |
|---|---|---|---|---|
| INV-20304 | Drummond Strategy | 4,485 | 2023-01-02 | churned |
| INV-22712 | Greystone Digital | 2,535 | 2024-12-01 | active |
| INV-23444 | Eastman Engineering | 3,264 | 2025-06-07 | active |
| INV-23907 | Moreau & Glover Advisory | 4,095 | 2025-10-05 | active |
| INV-24229 | Upton Stanhope Engineers | 5,712 | 2025-12-31 | active |
| INV-24416 | Ellery Legal | **17,520** | 2026-02-14 | active |
| INV-24647 | Haddad Thorne Law | 2,856 | 2026-04-13 | active |
| INV-24749 | Kingsway Digital (implementation fee) | 2,500 | 2026-05-09 | active |
| INV-25261 | Studio Calloway | 4,284 | 2026-09-15 | active |

- **F** 8 of the 9 customers are still active and paying by card. Eastman Engineering is failing again: INV-25973 for $3,264 is `payment_failed` and auto-writes off on 2027-03-07.
- **I** The automatic 150-day rule and the $2k approval limit conflict. The tool should route any card write-off over $2k to the VP Finance before day 150.

## 5. Contract vs invoice amounts — `work/check5_contract_vs_invoice_{open,all}.csv`
- **F** Open invoices: **0 of 117 mismatch**, using expected = arr × period/12 for subscriptions, or the plan's implementation fee (Growth $2,500, Enterprise $8,000).
- **F** All invoices: 0 of 6,062 mismatch, before or after 16 Mar 2026.
  - Every invoice and payment is a whole-dollar amount, so there are no proration or rounding residues.
  - All contract terms starting in 2025 or later are on the 2025 price list.
- **F, minor policy exception:** 23 contract terms are below the plan's minimum seat count.
- **I** The billing-engine rewrite leaves no trace in Ledgerline's own invoices. Its cent-rounding, proration and time-zone effects appear only in customers' tickets about *their* client invoicing. Do not tell Priya that the rewrite caused AR disputes.

## Data limits that matter for Monday
1. No invoice line items, tax, discounts, credit notes or refunds. Disputes about lines can be checked only against the total.
2. There is no record of what the customer actually received (no PDF or email log).
3. Contract terms are the only seat source. Usage `seats_licensed` matches the contract, and `active_users` is the only independent signal.
