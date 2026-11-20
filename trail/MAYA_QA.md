# Maya Q&A (log word for word: "What you ask is part of what we read")

Messages used: **4 of 60** (verified on the challenge page at T+0:50: "56 messages left"). Target: 12 or fewer.
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
