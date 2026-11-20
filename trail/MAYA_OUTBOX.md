# Maya outbox — drafts written by the test-steward, sent by the main thread

Messages used: 4 of 60 (verified on the challenge page at T+0:50: "56 messages left")

Rule since T+0:25 (Jacek): a draft goes to Maya only for a **Confirmation** (a decision she or Dana owns) or **Intel** (facts the data room can't give). No pure status updates. Every draft starts with a `Purpose:` line. Drafts 1 to 3 predate the rule, so their Purpose lines were added afterwards.

## Draft 1 — what we're building (SENT 11:14, T+0:04)
Purpose: Intel (added afterwards: Paidly history, Dana's success metric, day-one autonomy).
See MAYA_QA.md, exchange 1.

## Draft 2 — first results on real records (SENT 11:26, T+0:16, revised by the main thread before sending)
Purpose: Confirmation (added afterwards: card re-runs, Priya's digest, dispute routing).
The words actually sent are in MAYA_QA.md, exchange 2. The main thread revised this draft before sending it:
- **Newer numbers.** Dispute detection was fixed between 11:23 and 11:26 to catch disputes in tickets tagged How-to or left untagged. Disputed went from $264k to $312k, collectable from $286k to $238k, chases prevented from 20 to 22, drafts for Priya from 28 to 27, needs-a-person from 12 to 11.
- **Q1 swapped.** It asked about Dana's bank-fee write-off threshold. It was replaced with a question about re-running failed cards, because `analysis/FACTS.md` shows the real data has 0 bank-fee deductions and 0 short payments, so that question would have used up a message on a case that doesn't occur.
- AM written out as "account manager".

Original draft as written at 11:23 (kept for the record, NOT what was sent):

> Hi Maya, the four agents now run end to end on real records. Of the $633k overdue on the ledger, $83k is money we already received, $264k is disputed in support, and about $286k is genuinely collectable. Many disputes sit in tickets marked solved where the customer still refuses to pay, like Riverside Partners' $60.6k seat double-count. Kingsway paid $5,100 on 29 Oct with no reference and has two $5,100 invoices open, so we hold both instead of guessing. Net: 20 wrong chases prevented, 28 reminders drafted for Priya to approve, 12 that need a person to write. Three questions: (1) What is Dana's write-off threshold for bank-fee short payments? Could you relay it or give your best guess? (2) Does Priya work best from a morning queue in the tool or a Slack/email digest, and must the AM approve before a hold is released? (3) Should disputed invoices go to the AM automatically with the ticket text, or should finance own the fix with support?

## Draft 3 — AI provider and data (SENT ~11:28, T+0:18, written by the main thread)
Purpose: Confirmation (added afterwards: answered Maya's data challenge and confirmed her Exchange 2 answers).
See MAYA_QA.md, exchange 3.

## Draft 4 — app live on Render (ON HOLD at T+0:32, drafted 11:30, T+0:20; do not send as written)
Purpose: none that qualifies under the T+0:25 rule. Why it is on hold: it is mostly a status update. Its first question (Priya trying the tool) is overtaken by Maya's "book thirty minutes with Priya" (Exchange 4). Its second question (Legal) is answered: Maya takes the note to Legal this week. Send the live link to Maya only together with a real Confirmation or Intel ask.

Single line: paste as is, no line breaks. 110 words. Fill in the placeholders from the deployed app before sending. If Maya has already answered on Bedrock/Legal by then, drop the second question.

Hi Maya, the tool is live at {URL}. Sign in with your Scaleworks Google account. It opens on Priya's morning queue: {N_DRAFTS} reminders to approve, {N_HOLDS} holds with the reason for each, and {N_CARD} card re-runs waiting for her approval. The AI is switched off, so everything you see runs on rules and your templates. Two things worth trying: open Kingsway to see why both $5,100 invoices are held, and open Riverside Partners to see the "solved" ticket that blocks the chase. Two questions: could Priya spend ten minutes in it today and tell us what she would change, and has Legal said whether the Bedrock route works for them?

Before sending, check: (a) the SSO allowlist actually admits Maya's address (D5 restricts sign-in to scaleworks.com plus Jacek's emails); (b) the card re-run proposals and AM-confirmed hold release (D8, D10) are really in the deployed build, or else take them out of the message; (c) the numbers match the live dashboard, not this file.

## Draft 5 — note for Legal, misses on real records, Monday go-live (SENT ~11:42, T+0:32, written by the main thread)
Purpose: Confirmation (can the rules-only version go in front of Priya on Monday?).
The exact words sent and Maya's reply are in MAYA_QA.md, Exchange 4. She said yes, on conditions.

## Draft 6 — Dana's two decisions before Monday (READY, drafted 11:46, T+0:36)
Purpose: Confirmation (two decisions Dana owns, plus how they reach her).
Single line: paste as is. About 110 words. Send soon. By the data room's date, Northgate writes off **tomorrow**, and Maya already asked in Exchange 2 for Dana to hear about it "this morning". If Dana's answers reach Jacek another way first, drop that question.

Purpose: Confirmation. Monday it is, and I'll book the thirty minutes with Priya. Dana needs to make two calls before then: will you take them to her, or should I send them to her directly? (1) Northgate Creative's $799 card invoice (INV-25433) is written off automatically tomorrow at 150 days. Should Priya re-run the card, should we chase it, or should it be written off? (2) The tool applies a payment on its own only when the amount and the invoice reference both match exactly. It got 81 out of 81 right on past receipts, but there is no size limit, so a $62,688 receipt with an exact reference would apply without anyone looking. Should Dana set a cap, say $10,000, above which Priya approves?

Evidence: `analysis/FACTS.md` section 6 (Northgate INV-25433 auto write-off), `analysis/EVAL.md` (auto-apply 81/81, "no cap on auto-apply size"). The $10,000 figure is our example only, not a recommendation from the data.
