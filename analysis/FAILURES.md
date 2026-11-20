# FAILURES: where the system is wrong, unsure, or could be gamed

QA Evaluator, 2026-11-20 at 11:36 CST. Every case can be reproduced with `analysis/scripts/eval_*.py`. The numbers
are in `analysis/EVAL.md`.

**REAL** means it happens on the records as they are today. **REAL + MUTATION** means a real record changed in
memory in a way the data shows is common. **SYNTHETIC** means injected text or amounts, labelled as such.

Ranked by how much harm a wrong outcome would do.

---

### 1. Abbreviate the payer name and the Paidly failure comes back (REAL + MUTATION). Highest severity.
- **What happened.** We took Brandt & Lowell's real unapplied $6,324 wire (PAY-65766) and changed only the payer to
  `BRANDT`, the way 416 historical receipts arrive truncated.
  - The Cash agent's fuzzy match picked **Studio Brandt** (similarity 0.55), found no matching invoice and raised
    an EXCEPTION.
  - Brandt & Lowell's INV-25806 then got a **DRAFT_REMINDER to aisha.garrick@brandtlowellcpas.example** for money
    already in the bank.
  - The same happens with `KINGSWAY`: INV-25469 is drafted.
  - For `JESSOP` see #3.
- **Why.**
  - The Controller only holds against an unapplied receipt it can tie to a customer (`pipeline.py:34-35`,
    `controller.py:28-33`). An EXCEPTION with `customer_id=None` blocks nothing. One tied to the wrong customer
    blocks the wrong customer.
  - `identify_customer` accepts a lone fuzzy candidate scoring as low as 0.55 (`cash_app.py:42-49`). Short payer
    strings therefore resolve to the shortest customer name that contains the surname.
  - On the real test set, 12 of 80 hard receipts end as exceptions: 11 with no customer, and 1 (PEMBERTON) with
    the wrong customer.
- **Impact.** In the mutated cases, $6,324 + $62,688 + $5,100 would be chased after the money arrived. This is
  exactly the email Maya said gets the tool switched off.
- **What a person should do.** Until this is fixed, Priya must clear the "Payments to confirm" queue **before**
  approving any reminder. Any receipt with no identified customer should freeze reminders for invoices of the same
  amount.
- **Fix idea.**
  - (a) Any EXCEPTION receipt holds every open invoice with the same amount (±fee tolerance) across ALL customers,
    plus every candidate customer's invoices.
  - (b) Only set `customer_id` from a fuzzy match at ≥0.8 confidence; below that, keep the candidates list.
  - (c) Add `BRANDT` and `JESSOP` as permanent regression tests.

### 2. A dispute ticket one day outside the lookback, so a card re-run is proposed for a customer with a chargeback (REAL)
- **What happened.**
  - On 2026-07-02, Drummond Consulting wrote T880019, "DISPUTING CHARGES WITH MY BANK": "You billed us twice for
    the annual plan ... I've opened a chargeback on both payments."
  - Today Drummond's failed card invoice INV-25769 ($658, 68 dpd) is proposed as **RETRY_CARD**.
- **Why.** `dispute_lookback_days` = 120 puts the window start at 2026-07-03, so the ticket is invisible
  (`context.py:93,101`). The legal / chargeback read never runs. Old tickets also drop out silently, so a dispute
  hold disappears on its own once the ticket ages past 120 days, even if nobody settled it.
- **Impact.** $658, but re-charging a card the customer is charging back is a likely CEO-inbox complaint. The same
  silent ageing applies to all 14 disputes ($309k) from late November onward.
- **What a person should do.** Priya should check Drummond's history before approving the re-run. The AM should
  confirm the chargeback is resolved.
- **Fix idea.**
  - Always read legal_threat and chargeback tickets regardless of age.
  - Make dispute holds sticky until an AM releases them, as Maya asked, instead of letting them depend on the
    ticket's age.

### 3. The "Jessop payment" memo fits 8 customers; only the exact payer name saves it (REAL; abbreviated variant is REAL + MUTATION)
- **What happened.**
  - PAY-65750, $62,688, memo "Jessop payment", payer "Jessop & Orwell Agency". Eight customers contain "Jessop"
    (Jessop Legal, Jessop Strategy, Delacroix Jessop & Co, and others).
  - Today the payer name matches exactly, the amount is unique, and INV-25784 (a top-50 account) is held as
    MONEY_RECEIVED. Correct.
  - With the payer changed to `JESSOP`, the Cash agent tagged the receipt to **Jessop Legal (C1402)**.
    - Jessop Legal's invoices would be held for no reason.
    - Jessop & Orwell's $62,688 invoice dropped to HUMAN_WRITES with a **prepared chase draft to
      joel.okafor@jessoporwellagency.example**.
  - With `JESSOP ORWELL` it is handled correctly.
- **Why.** The same mechanics as #1. The memo surname is never used to rank candidates. Only 1 of the 8 Jessop
  customers has an open $62,688 invoice, and that was never consulted.
- **Impact.** $62,688 on a top-50 account. This is the Paidly scenario on the largest receipt in the data. The money
  has also sat unapplied for 10 working days, against a 3-to-5-day policy.
- **What a person should do.** Apply PAY-65750 to INV-25784 today. When a surname memo fits several customers, check
  the remitter's bank account details, not the name.
- **Fix idea.** When the name is ambiguous, search every customer whose name contains the memo surname for an exact
  open amount. If exactly one fits, propose it, and never send `customer_id` to the wrong account.

### 4. Complaints worded outside the keyword lists are not held (SYNTHETIC injection into a real account)
- **What happened.** Tickets were injected for Thornfield Consulting (INV-25862, $39,456, normally a
  DRAFT_REMINDER). The reminder was **still drafted** for:
  - "We **will not** pay it until you correct it" (Billing, open);
  - "We **refuse to pay** an invoice for seats we removed" (untagged);
  - "The invoice has the wrong seat count. We won't pay until it's fixed" tagged **How-to**;
  - "We think we've been overcharged ... double what we agreed. Please call me" (Billing, open, normal).
- **Why.** `heuristic_read` (`context.py`) only flags a ticket when one of these holds:
  - it cites an `INV-#####` ref;
  - it contains one of 22 exact refusal phrases ("will not pay" and "refuse to pay" are not among them) **and** is
    tagged Billing or Account change;
  - it contains a legal or cancellation pattern.
  Disputes tagged How-to are only caught if they cite the INV id. The real data shows 4 of 14 disputes were not
  tagged Billing.
- **Impact.** Chasing a customer mid-complaint is the second failure Maya named. The analyst's 14 all cite an INV id,
  so the live data hides this gap.
- **What a person should do.** Before approving a draft, glance at the customer's tickets from the last 30 days.
  The customer page shows them.
- **Fix idea.**
  - Hold on any open or pending ticket in the Billing / Account change category, or any untagged one, regardless of
    phrasing.
  - Widen the refusal regex (will not / refuse / dispute / overcharg).
  - Use the Claude read once Legal approves. This is exactly the fuzzy reading the LLM is for.

### 5. Ticket marked "solved" while the dispute is unresolved (REAL)
- **What happened.**
  - 11 of the 14 disputed invoices ($309,000 in total) sit on tickets marked **solved**. Example: Riverside Partners
    INV-25787, $60,576. The customer wrote "We've paused payment pending a corrected invoice"; the ticket was closed
    and the invoice never reissued.
  - The system catches all 11 by reading the text, and the hold says "marked solved but the customer said they won't
    pay".
  - It is still unsure in two ways:
    - (a) T881039 Delacroix, Jessop ("I'll hold off paying until someone can confirm") is caught only because it
      quotes INV-25834. Its refusal wording matches no pattern.
    - (b) Nothing in the data records that the dispute was settled. The hold can only end through the 120-day
      ageing in #2 or an AM click.
- **Impact.** $309,000 (49% of overdue) depends on ticket text, not on any status field.
- **What a person should do.**
  - The AM confirms each one with the customer.
  - Finance issues the corrected invoice and a credit note.
  - Support should stop closing billing tickets before the invoice is fixed.
- **Fix idea.** A hold release that needs an AM, with a reason, written to the audit log. Report "solved but still
  disputed" back to the support lead weekly.

### 6. Reyes Consulting's $51,072 invoice held as a "dispute" because the customer asked about voiding their OWN invoice (REAL)
- **What happened.** T880132 (Billing, solved): "Sent an invoice yesterday to the wrong contact with the wrong
  amount on it. Do I void it and raise a new one?" This is about Reyes's invoice to its own client.
  - The refusal pattern `void it` fires, and the category is Billing, so the read becomes a dispute with no invoice
    id.
  - Result: Reyes's top-50 invoice INV-26009 ($51,072, not due yet) is **HOLD / DISPUTE**, routed to the AM as a
    Ledgerline billing dispute.
  - The same false read hits Lindgren Legal (T880915). They have no open AR.
  - `attorney` also turns Studio Finch's "PDF for the supervising attorney" into a **legal threat**.
- **Impact.** $51,072. No wrong email goes out (it is top-50, so a person writes anyway), but the AM walks into a
  renewal call believing there is a dispute that does not exist. Ticket-read precision is 18 of 22 (82%).
- **What a person should do.** Priya or the AM releases the hold after reading the ticket. It takes about 10
  seconds.
- **Fix idea.** Drop `void it` and `reissue it` as refusal signals unless the ticket cites a Ledgerline invoice.
  Treat lawyer / attorney / solicitor as legal only when they appear next to a threat verb.

### 7. The keyword complaint counter said 14; the real number is 1 (REAL, already fixed: before/after)
- **Before.** `COMPLAINT_RX` (`pipeline.py:13`) counted **14** "collections complaints" in 120 days. That number
  would have been the veto metric on Dana's dashboard.
- **Hand check of the 14:**
  - **12** concern the customer's OWN reminder emails or notices to their clients, or their own duplicate invoice
    run. Examples: T880733 "Where do I edit the subject line on reminder emails?"; T880255 "client ... keeps getting
    reminder emails"; T880608 "client paid on time and still got a 'final notice'".
  - **1** (T880373 Highmoor, "Why is there a charge for $41.17 ... we already paid") is a question about a
    Ledgerline charge, not about collections.
  - **1** is real: T880519 Eastman Engineering, renewal price plus a consumer-affairs complaint plus a threat to
    contest the card charge.
- **After.** The metric now uses the agent's read (`collections_complaint` and about a Ledgerline invoice, or
  legal_threat): **1** (T880519). The keyword number is still exported as `complaint_keyword_hits` for transparency.
- **Why it matters.** Ledgerline sells invoicing software, so "reminder", "overdue notice" and "final notice" are
  product vocabulary. A naive counter would have shown the tool's veto metric as 14x worse than reality.
- **Residual risk.** The "after" number depends on the same heuristic as #4 and #6. Treat it as a floor, not a
  certified count.

### 8. Kingsway: one $5,100 payment, two $5,100 invoices (REAL)
- **What happened.**
  - PAY-65805 ($5,100, 10-29, no memo) from Kingsway Engineering Group. Two overdue $5,100 invoices exist:
    INV-25469 (111 dpd) and INV-25852 (19 dpd).
  - The agent proposes the oldest (the house convention, 91% historically) with the other as an alternative, and
    **holds both**. That is correct and cautious.
  - But the dashboard's "already received" counts the money twice: **$83,448 instead of $78,348**, which understates
    "collectable" by $5,100.
  - If Priya applies it to INV-25469 when Kingsway meant INV-25852, the remaining invoice moves between the 19-day
    "first reminder" track and the 90+ escalation track.
- **Impact.** $5,100 is owed either way. The metric is overstated by $5,100.
- **What a person should do.** Ask Kingsway's billing contact which invoice the payment covers before applying.
  Their renewal is close, so tell the AM.
- **Fix idea.** Count each receipt once in `overdue_already_paid` (`pipeline.py:96`). Show "1 payment, 2 candidate
  invoices" in the UI.

### 9. Ambrose & Lowell held for an open high-priority PRODUCT bug (REAL; policy-correct, arguably over-cautious)
- **What happened.**
  - Both of Ambrose & Lowell's $658 invoices are on HOLD / OPEN_ESCALATION: INV-25897 (10 dpd) and INV-26029 (not
    due).
  - The trigger is T880474 (Bug, high, pending since 08-24): "Card payments are going through ... but the invoices
    stay marked unpaid in Ledgerline". That is a bug in the customer's own invoicing, not a dispute of Ledgerline's
    bill.
- **Why.** Policy says don't chase during an open escalation, and "high-priority open ticket" is our stand-in for
  escalation.
  - The Rules page offers "Hold on tickets opened in the last N days" = 30, **but the engine never reads
    `hold_on_open_ticket_days`**. A 68-day-old ticket still holds.
  - Changing that setting does nothing. That breaks Maya's condition that Priya can see why something was held and
    fix it herself.
- **Impact.** $1,316 not chased. The cost is small. Being gentle with a customer whose product bug has been open 68
  days is defensible, but it is the AM's call, not the tool's.
- **What a person should do.** Ask the AM whether to send a courtesy note. Fix the bug first.
- **Fix idea.**
  - Wire `hold_on_open_ticket_days` into `controller.py:55`.
  - Split the hold: "billing escalation" stays a hard hold, while a "product bug" becomes a soft flag that the AM
    confirms.

### 10. The banned-phrase list is narrow (SYNTHETIC template injection)
- **What happened.**
  - Templates were monkeypatched to add "We may refer this to a **debt collector**", "We will begin **legal
    proceedings**" and "Your access will be **cut off** on Friday". **All 21 drafts passed** the Controller.
  - "suspension", "no choice" and "FINAL NOTICE" were correctly blocked (31 of 31).
- **Why.** `check_draft` (`controller.py:104-109`) does a plain substring match on 8 phrases.
- **Impact.** Once `use_claude` is on, Claude rewrites the drafts. A threatening paraphrase would pass, and a threat
  to a top-50 account is the other switch-off trigger.
- **Side effect found.** A blocked draft turns the invoice into HOLD **before** the card re-run check runs. The 10
  RETRY_CARD proposals vanished, even though no email would have been sent for them (`pipeline.py:54-71`).
- **What a person should do.** Read every Claude-written draft until the list is broader.
- **Fix idea.**
  - Add debt collector, legal proceedings, court, cut off, disconnect, terminate access, credit rating, and similar.
  - Add a second LLM or classifier "tone check" once the LLM is allowed.
  - Run the banned-language check only on drafts that will actually be used.

### 11. Same customer, two failed cards, two different treatments (REAL)
- **What happened.** Quill, Mott & Co has two failed $1,632 card invoices.
  - INV-25708 (83 dpd) → **RETRY_CARD**, because a later card charge succeeded.
  - INV-25975 (22 dpd) → **DRAFT_REMINDER**: "Your card payment didn't go through ... update the card".
- **Why.** "Card works" is tested per invoice, against payments after that invoice's issue date
  (`pipeline.py:63-65`). No successful charge came after the newer invoice.
- **Impact.** $3,264. The customer may be told to update a card while Priya simultaneously re-charges it.
- **What a person should do.** Treat both together: re-run the older one first, then email only if it fails.
- **Fix idea.** Decide per customer, not per invoice.

### 12. Cash application blind spots on SYNTHETIC traps, plus a test-set defect
- **What happened.**
  - A bank-fee deduction ($15 to $35) or a 10% short pay **with no memo ref** is always an EXCEPTION ("Ask the
    customer which invoice"). This affects 8 of 20 synthetic rows, even though the customer and a near-exact invoice
    are obvious.
  - The labels are misleading: +$0.02 is described as "partial or combined payment", and -$0.01 as "looks like a
    bank fee".
  - For SYN-040, Rosales has three $2,448 invoices. The matcher proposed the first pair adding up to $4,896 and did
    not mention that other pairs fit.
- **Why.** `fee_tolerance` is only applied on the memo-ref path (`cash_app.py:98`). The combination search returns
  its first hit (`cash_app.py:117-123`).
- **Impact.** No wrong money movement (0 synthetic auto-applies), just more manual work for Priya. These traps are
  absent from the real data (FACTS §4).
- **Test-set defect (data-analyst).** 7 of 10 synthetic "combined" rows pair an invoice that had already been paid
  months before the receipt date (for example, SYN-004 includes INV-24088, paid 2025-08-06). The matcher is right
  to refuse them. Regenerate those rows.
- **Fix idea.** Use a no-ref near-amount pass within `fee_tolerance` that returns PROPOSE at 0.6. List every
  combination that fits as an alternative.

### 13. A look-alike domain is blocked but mislabelled (SYNTHETIC injection)
- **What happened.** A "Billing contact" at `thornfleldconsultinggr.example` or `thorn-fieldconsultinggr.example`
  was injected first in the list.
  - It is correctly never used.
  - The hold reads **"Billing contact has left"**, which hides a possible spoofing or fraud signal.
- **Fix idea.** A separate code, SUSPICIOUS_DOMAIN, routed to Dana. Exact-domain matching also excludes legitimate
  subdomains (`billing.<domain>`), so a person must allow-list them.

---

**For the demo video, the three strongest cases:**
1. **#1 or #3 (Paidly with an abbreviated payer name).** It shows candidly that the headline guardrail has a hole,
   with a concrete fix.
2. **#2 (Drummond's chargeback, one day outside the window).** It shows the system's limits on real data.
3. **#7 (complaints, 14 → 1).** It shows why the LLM / agent reading matters, with a real before and after.
