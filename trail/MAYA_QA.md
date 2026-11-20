# Maya Q&A (log word for word: "What you ask is part of what we read")

Messages used: **8 of 60** (verified on the challenge page at T+0:50: "56 messages left"). Target: 12 or fewer.
Rule since T+0:25 (Jacek): write to Maya only for a **Confirmation** (a decision she or Dana owns) or **Intel** (facts the data room can't give). Never a pure status update.

## Prepared questions (refine after the data-room read, ask in hour 2)
Pick the 5–7 sharpest. Ask about **what matters, what has failed before, and what would get it switched off.**

**What matters**
1. If Dana could only fix one thing about collections this quarter, would it be DSO, the overdue $ balance, or not upsetting good customers? Which number would she check in a month?
2. How much of the overdue balance do you think is real non-payment vs. money we've received but not applied, vs. invoices in dispute?

**What has failed before**
3. Have you tried automating reminders before (QuickBooks or Stripe dunning)? What happened, and why was it turned off or ignored?
4. Since the billing-engine rewrite in March, have disputes or wrong invoices gone up? Does finance know which customers were affected?

**What would get it switched off**
5. What is the one email the system must never send? (A guess: chasing a customer mid-complaint, or chasing a paid invoice.)
6. Who has to approve a reminder before it goes out, and does that change by amount, customer size or how overdue it is?
7. Are there accounts that should never get an automated message (key accounts, ones in renewal negotiation, or owned by a particular AM)?

**Boundaries and data**
8. What can it do on its own today: apply exact-match payments, write off bank fees under $X? What is X?
9. Failed card payments: who owns follow-up today, and can we contact the customer directly?
10. Can I see the AR inbox or remittance emails, or should I assume remittance only lives in support tickets?

## Log
Budget: Maya allows 60 messages. Bundle questions. Running count at the top of this file and in MAYA_OUTBOX.md.

### Exchange 1 — 11:14 CST, T+0:04
Maya opened the chat before Jacek wrote.

**Maya:** Hi, Maya here. I am around all day, so ask whenever something comes up. What are you thinking of building?

**Jacek:** Hi Maya, Jacek here. I'm taking on cash collection for Dana: Collections (FIN-1) together with Cash Application (FIN-2). From the policy and process maps they look like one problem. Customers get chased for invoices whose money has already arrived but isn't applied yet, and get chased while they have an open complaint because finance can't see Zendesk. I'm building a small team of AI agents, each owning one job. One matches unapplied bank receipts to invoices. One pulls each customer's tickets, usage, contract and renewal into one view. One drafts the right reminder under your collections policy. A controller holds anything that shouldn't go out: disputes, open escalations, top-50 accounts, a contact we can't verify. Nothing reaches a customer or the ledger without Dana or the AR specialist approving it, and every decision is logged with its reason. Three questions before I build: (1) Paidly was switched off after six weeks in 2025. What happened, and what would make Dana switch this off too? (2) If this works, which number would Dana check in a month: the overdue balance, DSO, or fewer complaints about collections? (3) What can the system do on its own from day one, for example apply exact-match payments or write off small bank-fee differences, and who has to approve everything else?

**Maya:** Hi Jacek. Paidly chased a long-standing customer who had already paid by wire, because the money took days to be matched, and nobody had tested that case before it went live. That, along with the reminder sequence the CEO personally shut down after a customer complained to him, is what would get this switched off: one wrong chase or one message that reads like a threat to a top-50 account. Dana would also drop it if Priya can't see why it held or drafted something and fix it herself, because Priya is the one who has to run it.

On the number, I believe Dana would look at the overdue balance first and treat complaints about collections as the veto, though she'd confirm. What I'll be checking is whether Priya is still using it in a month.

On autonomy, my understanding is that applying exact matches on amount and invoice reference is close to what the team already does without thinking twice, so Dana may be comfortable with that. Write-offs, partial matches and anything that goes to a customer would go through Dana or Priya. Dana sets the threshold, so ask her before you build that in.

**What we changed because of it**
1. Cash Application runs **before** Collections on every cycle. Any unapplied receipt that plausibly covers an invoice is a hard block on chasing it (the Paidly failure becomes test case #1).
2. No threatening language anywhere. The 45-day "FINAL NOTICE: suspension" template is retired; the Controller blocks suspension/legal wording outright. Top-50 accounts always go to a person.
3. **Priya is the primary user.** Every hold or draft shows its reasons in plain English, and Priya can override it and edit the rules herself in a Rules page, no engineer needed.
4. Autonomy: auto-apply ONLY exact amount + invoice reference matches. Write-off threshold defaults to **$0 (off)** until Dana sets it. Partial matches, write-offs and every customer email need Priya or Dana.
5. Headline metric on the dashboard: overdue balance. A collections complaint counter is shown as the veto.

### Exchange 2 — 11:26 CST, T+0:16
Sent by Claude Code at Jacek's standing instruction. The main thread revised Draft 2 before sending (see MAYA_OUTBOX.md).

**Jacek:** Hi Maya, an update at T+0:15. The four agents now run end to end on the real records. Of the $633k overdue on the ledger, $83k is money we have already received but not applied, $312k is disputed in support tickets finance can't see (14 invoices, plus Eastman Engineering's chargeback threat), and about $238k is genuinely collectable. Most disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 22 wrong chases prevented, 27 reminders drafted for Priya to approve, 11 that need a person to write. Three questions: (1) 10 of the 16 failed card invoices belong to customers whose later card charges went through, and Northgate's $799 is written off automatically tomorrow. May the system re-run a failed charge on a card that works, or does Priya decide each one? (2) Does Priya work best from a morning queue in the tool or a Slack or email digest, and must the account manager approve before a hold is released? (3) Should disputed invoices go to the account manager automatically with the ticket text, or should finance own the fix with support?

**Maya:** Those numbers are worth showing Dana today, especially the $312k sitting in "solved" tickets. On re-running cards, I'd want Priya to approve each one for now. Charging a customer's card without a person looking is exactly the kind of thing that ends up in the CEO's inbox, and Dana owns the call on whether that ever changes. Tell Dana about Northgate's $799 this morning so she can decide before it writes off.

I believe Priya lives in Slack and would rather get a short morning digest that links to the queue than log into another tool, but ask her directly because she'll be the one using it. For the disputes, I'd send them to the account manager with a summary, because the AMs own the relationship and are walking into renewal calls blind. Finance and support would still fix the billing error together, and the hold should only be released once the AM agrees the dispute is settled.

You're now pushing ticket text and customer financials through these agents. Which AI provider is doing that, and have you confirmed it doesn't train on our data? Legal won't let customer ticket content or financial data go to a new vendor without a data processing agreement.

**What we changed because of it**
1. **Card re-runs (D8):** the system never re-charges a card on its own. Where a customer's later card charges succeeded, it proposes a re-run, and Priya approves each one. Whether that ever becomes automatic is Dana's call.
2. **Northgate $799:** goes to Dana today as a decision, before the 150-day automatic write-off.
3. **Morning digest (D9):** Priya gets a short Slack-style morning digest that links to the queue, so she doesn't have to log into another tool. Still to confirm with Priya directly, as Maya said.
4. **Disputes (D10):** routed to the account manager with a summary. Finance and support still fix the billing error together. A dispute hold is released only when the AM confirms it is settled.
5. **Data and Legal (D11):** Maya's challenge led straight to Exchange 3. `rules.use_claude` now defaults to False, and `app/engine/llm.py` supports `LLM_PROVIDER=bedrock`.

### Exchange 3 — ~11:28 CST, T+0:18
**Jacek:** Good challenge, and nothing has gone to any AI provider yet. Everything you've seen so far is rules and matching on the records. The provider would be Claude from Anthropic. Under Anthropic's commercial terms, API inputs and outputs are not used to train models, and a DPA is available, but Legal should review it before any real data flows. Since Ledgerline already hosts on AWS, the cleaner route is Claude through Amazon Bedrock under your existing AWS agreement: Amazon doesn't share the data with the model provider or use it for training, and Legal adds no new vendor. Until Legal signs off, the AI stays switched off with one setting. Holds and matching keep working on rules, and drafts come from your own templates. When it's on, only ticket text and invoice facts are sent, never bank details. Taking your other answers: card re-runs become a proposal Priya approves one by one. Northgate goes to Dana as a decision today. Priya gets a short Slack morning digest that links to the queue. Disputes go to the account manager with a summary, and a hold is released only when the AM confirms it's settled.

Maya replied at ~11:29, T+0:19.

**Maya:** That's the answer I needed. Bedrock under the AWS agreement we already have is the route I'd rather take to Legal, but they'll want to confirm our current terms actually cover Bedrock before I'd call it "no new vendor." Send me a short note naming the service, the region, and exactly which fields leave our systems, and I'll put it in front of them this week. I also like that the rules-only version works without the AI switched on, because that could be in front of Priya on Monday while Legal reviews. Before then, tell me what it got wrong on the real records. I'd rather hear about the misses from you than from a customer.

**What we changed because of it**
1. AI is off by default (`use_claude: False` in `app/engine/rules.py`). With it off, holds and matching run on rules and drafts come from the policy templates.
2. `LLM_PROVIDER=bedrock` routes Claude calls through Amazon Bedrock (`anthropic.AnthropicBedrock()` in `app/engine/llm.py`), so the data stays under Ledgerline's existing AWS agreement.
3. Data minimisation commitment: when the AI is on, only ticket text and invoice facts are sent, never bank details.
   The test-steward checked this against the code at 11:30. Neither prompt sends bank or payment fields. **But the drafting prompt (`app/engine/collections.py`) sends more than "ticket text and invoice facts":** the customer name and plan, last NPS score, usage trend, renewal date and the contact's first name. The ticket prompt (`app/engine/context.py`) sends the customer name, the open invoice ids and up to 2,500 characters of ticket body. Either trim the drafting prompt or describe the scope to Maya and Legal accurately ("ticket text, invoice facts and account context such as plan, NPS, usage trend and renewal date; never bank details").
   Resolved at 11:31: the drafting prompt was trimmed to invoice facts only, with names masked, and emails and phone numbers are removed from ticket text (JOURNAL 11:31, `submission/LEGAL_NOTE.md`).
4. wrote submission/LEGAL_NOTE.md (service, region, exact fields per task). Added redaction of emails and phone numbers to ticket text before any AI call, and masked names in drafting prompts, so the note is literally true. Framed the rollout as "rules-only on Priya's desk Monday, AI after Legal". The qa-evaluator is producing analysis/FAILURES.md so we tell Maya the misses before she asks again. Reply to send with the note + misses (draft 4).
   (The reply with the note and the misses was sent as Exchange 4, written by the main thread and filed as Draft 5 in MAYA_OUTBOX.md. Draft 4 was put on hold.)

### Exchange 4 — ~11:42 CST, T+0:32
Purpose: Confirmation. Written and sent by the main thread from Jacek's Chrome tab. It answers Maya's two asks from Exchange 3 (the note for Legal, and what it got wrong on the real records) and asks for the go-live decision.

**Jacek:** Two things you asked for, and one confirmation. The note for Legal: Claude through Amazon Bedrock in your existing AWS region. To read tickets it sends the customer's company name, their open invoice numbers and the ticket text, with emails and phone numbers removed. To draft reminders it sends only the invoice number, amount, due date and payment link, with names masked. Payment matching and every hold send nothing. It stays off until Legal agrees. What it got wrong on the real records: when a bank shortens the payer name, say BRANDT instead of Brandt & Lowell CPAs, it couldn't tie the payment to a customer and would have chased the $6,324 they had already paid. That is the Paidly failure, and 416 past receipts arrived shortened like that. It's fixed: an unidentified payment now holds every invoice of the same amount until Priya names the payer. It also missed Drummond Consulting's chargeback threat by one day and proposed re-running their card. That's fixed too. It still over-holds sometimes: it read Reyes Consulting asking about their own client's invoice as a dispute. On that basis, can the rules-only version go in front of Priya on Monday, with every payment match, hold release and email still needing her approval?

**Maya:** Yes, Monday with the rules-only version, as long as Priya approves every match, release and email, and Dana has seen the Northgate decision and the auto-apply threshold before then. Over-holding is the right way to be wrong. Reyes costs Priya a minute, but a BRANDT-style chase would cost us a customer, so track how often she overrides a hold and bring me that number in a month. Fill in the actual AWS region in the note, and expect Legal to point out that ticket text can still name people even with emails and phones removed. Book thirty minutes with Priya before Monday so she sees why it held Reyes and how to correct it herself.

**What we changed because of it**
1. Go-live set for **Monday, rules-only** (AI off). Priya approves every payment match, every hold release and every email (D14).
2. New metric on the RIG: **hold-override rate**, meaning how often Priya overrides a hold. Maya wants that number in a month. Over-holding stays the deliberate trade-off: "Over-holding is the right way to be wrong."
3. Monday checklist card added to the RIG. (a) Dana sees the Northgate $799 decision and the auto-apply rule and threshold. (b) 30-minute walkthrough with Priya: why it held Reyes, and how she corrects it herself. (c) Fill in the AWS region. (d) Legal's residual risk: ticket text can still name people.
4. `submission/LEGAL_NOTE.md`: the region line now reads "[Engineering to confirm the production AWS region]" instead of assuming us-east-1. The residual risk about names in ticket text was moved up into its own section.
5. Still open: how the Northgate and auto-apply decisions reach Dana. Draft 6 in MAYA_OUTBOX.md (READY, 11:46) asks Maya.


### Exchange 5 — ~13:47 CST, T+2:37 (Purpose: Confirmation; sent from the Maya desk/courier after Jacek's approval)
**Jacek:** Purpose: Confirmation. (1) Dana's call on card write-offs: Eastman Engineering $3,264 would auto-write-off above her $2,000 limit (they also threatened a chargeback); Northgate Creative $799 writes off tomorrow although their card has since worked; Hollis Nair Engineers $517 writes off in 9 days although their card has since worked. Re-run the card, call the customer, or let it write off? (2) Policy says don't chase during an open escalation, so we're holding Ambrose & Lowell Advisory (2 invoices, $1,316) because each has an open high-priority product ticket, not a billing complaint. Should these stay held until support closes the ticket, or can Priya chase them? (3) For Dana before Monday: the agent applies a payment by itself only when the amount and invoice number match exactly and it's under $10,000; everything else goes to Priya. Write-offs stay at $0, meaning never automatic. Does Dana confirm both numbers? (4) Mercer & Banerjee LLP gave written notice to cancel (their ticket in August), but nothing in billing reflects it and their renewal date is 2026-11-12. Should finance stop the renewal and agree a final balance instead of chasing $3,876?

**Maya:** I can give you my view, but Dana has to confirm the finance calls herself. Eastman shouldn't be re-run or written off automatically. With a chargeback threat and an amount above her limit, the account manager should call them, and Dana decides what happens after that conversation. For Northgate and Hollis Nair, my instinct is a short heads-up email and then a re-run Priya approves, rather than writing off money from customers whose cards now work. Dana should stop both automatic write-offs today so the clock doesn't make the decision for her.

Keep Ambrose & Lowell held. Chasing a customer about $1,316 while their high-priority product issue is still open is exactly how we get a complaint. Do tell their account manager, and have the hold come up for review if the ticket sits open for more than a couple of weeks.

The exact-match-under-$10,000 rule and the $0 write-off threshold sound right to me, but get Dana's yes in writing. Also confirm the existing automatic write-off is actually switched off, because $0 means nothing if Northgate still goes tomorrow.

On Mercer & Banerjee, yes. Finance should stop the renewal invoice and the account manager should confirm the cancellation with them. After that, agree the $3,876 as a final balance, and only chase it if they dispute something they used. Billing them for a renewal after written notice would turn a quiet churn into an angry one. Please flag it to the Head of Customer Success as well, because a cancellation finance never heard about is a gap we need to close.

**What we changed because of it**
- Eastman: no re-run, no write-off; AM calls, Dana decides. Northgate and Hollis Nair: heads-up email, then a card re-run Priya approves. Dana stops both automatic write-offs today (Monday checklist).
- Ambrose & Lowell stay held; AM told; review if the ticket stays open more than about two weeks.
- $10k exact-match cap and $0 write-offs: Maya agrees; Dana's written yes and confirmation that the automatic card write-off is switched off are on the Monday checklist.
- Mercer & Banerjee: stop the renewal invoice; AM confirms the cancellation; $3,876 becomes a final balance; flag to the Head of Customer Success.


### Exchange 6 — ~13:49 CST, T+2:39 (Purpose: Intel; sent from the Maya desk/courier after Jacek's approval)
**Jacek:** Purpose: Intel. (1) Our invoice records carry one total per invoice, with no line items, tax or credit notes, so we can't see fees like Westbrook's implementation charge. Could someone send the PDF of INV-25730, so we can check that what customers see matches the ledger? (2) All 14 disputed invoices match their contracts, but 5 need a person to decide: Riverside Partners; Okafor & Nakamura; Thackeray Accounting; Ellery Consulting; Brandt Ashby IT. Can you get the account managers (and whoever owns tax) to rule on these this week, so Priya can release or credit them?

**Maya:** I'll ask Priya to send you the PDF of INV-25730 today, and if the line items live in Stripe rather than QuickBooks, she'll know where to pull them. Yes, I'll get the account managers to rule on the five this week. Send me one line per account with the amount, what the customer says and what the contract says, so they can decide in a few minutes. Tax sits with Dana as far as I know, so copy her on anything that turns on tax. Keep in mind that matching the contract only tells us our side, and Riverside clearly thinks the seat count is wrong. I want the AMs to hear the customer out before Priya releases or credits anything.

**What we changed because of it**
- Priya sends the INV-25730 PDF (line items may live in Stripe).
- AMs rule on the five this week; tax items go to Dana. Maya asked for one line per account (sent in exchange 7).


### Exchange 7 — ~13:51 CST, T+2:41 (Purpose: Intel (requested by Maya); sent from the Maya desk/courier after Jacek's approval)
**Jacek:** Purpose: Intel, as you asked, one line per account for the AMs. (1) Riverside Partners, INV-25787, $60,576: customer says the workspace merge double-counted seats (62 billed, 38 people); our invoice bills 46 seats at $88 from the 27 Aug renewal, up from 39 in July, with 38 to 43 active users, so up to $8,448 if they're right. (2) Okafor & Nakamura, INV-25765, $46,848: customer says their AM offered 50% off for three months for a second office; the contract has 33 seats unchanged since 2023 and no discount, so up to $5,856. (3) Brandt Ashby IT, INV-25822, $26,112: customer says they moved from annual to monthly before renewal; the contract renewed annual on 7 Sep at 32 seats, so it's cash timing only, re-bill as 12 x $2,176 if proven. (4) Thackeray Accounting, INV-25750, $7,896: customer says VAT should be reverse charge; our customer record says United States, so it's a tax call for Dana. (5) Ellery Consulting, INV-25757, $13,056: customer says sales tax used their old address; the subscription amount matches the contract, so it's a tax call for Dana. All five stay held until the AM confirms.

**Maya:** This is what I needed, and I'll send it to the AMs today, with Thackeray and Ellery going to Dana. Before I do, check Riverside. 46 seats at $88 for a year is $48,576, not $60,576, and the customer says 62 were billed. So the invoice may not say what our records say, and that PDF matters more than INV-25730. On Thackeray, a customer asking about VAT reverse charge is probably UK-based, so our "United States" record may be the actual error. That's the kind of thing OPS-2 keeps producing, and Dana should know before she rules.

**What we changed because of it**
- Maya spotted that 46 x $88 x 12 is $48,576, not $60,576. Our line had omitted the $12,000 Enterprise platform fee. Correction sent in exchange 8.
- Thackeray's country record may itself be wrong (OPS-2); flag to Dana before she rules.


### Exchange 8 — ~13:53 CST, T+2:43 (Purpose: Confirmation (correction); sent from the Maya desk/courier after Jacek's approval)
**Jacek:** Purpose: Confirmation, and a correction to my Riverside line before it goes to the AMs. I left out the Enterprise platform fee: 46 seats x $88 x 12 is $48,576, plus the $12,000 platform fee, gives $60,576. So the invoice amount is consistent with 46 seats, while 62 seats would have been $77,472. The customer's 62 may come from their own user count after the merge rather than from the invoice. The PDF will settle what they actually see, so Riverside goes first. On Thackeray, agreed: the United States record may be the error, and we'll flag it to Dana as a customer-record problem (OPS-2) before she rules.

**Maya:** Thanks, that adds up. I'll send the corrected Riverside line to the AMs today. That changes what Riverside's AM needs to settle. It's no longer whether the invoice is wrong. It's whether 46 seats was right at the August renewal when they had 38 to 43 active users. The answer is probably in how the merge was handled, and the AM should hear that from the customer before anyone credits the $8,448. Please also check that the $12,000 platform fee shows as its own line on the PDF, because a customer who can't see it will assume they're paying for more seats than they are.

**What we changed because of it**
- Riverside's question for the AM is now whether 46 seats was right at the August renewal (38 to 43 active users); no $8,448 credit until the AM hears the customer.
- Check the $12,000 platform fee shows as its own line on the Riverside PDF (pulled first).
- Lesson for our own outputs: always state the platform fee when quoting Enterprise seat maths.
