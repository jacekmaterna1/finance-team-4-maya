# Demo video: Loom talk track (target 8:00, hard range 7–9 min)

RIG: https://ledgerline-finance-rig.onrender.com. Data as of 2026-10-31. All numbers come from `run_pipeline()` at 11:50 CST on 2026-11-20 and from `analysis/EVAL.md`, `FAILURES.md` and `DISCREPANCIES.md`.

**Before recording (5 min)**
- Wake the Render service: free plan, it sleeps when idle.
- Sign in, then press **Run** once so the queues are fresh.
- Have a terminal open at the project root for the BRANDT replay: `.venv/bin/python analysis/scripts/eval_guardrails.py | grep 1b`.
- Leave Maya on hold. Don't send her anything during the recording.
- Check the subject on Ambrose & Lowell's hold: it renders as `'???'` (T880474). Fix it or pick another hold.

---

## 0:00–0:30 What we chose and why
**Screen:** RIG **Home**.

> I picked one process: collections, with cash application feeding it. Dana says overdue invoices have risen three quarters running, and the board lists cash collection as its number-one worry. Ledgerline already tried a collections tool. Paidly was switched off after it chased a customer whose wire had already arrived. And finance can't see Zendesk, so people with open complaints get chased too. Both are the same problem: the reminder goes out before anyone checks the cash and the tickets. So this is one process, done properly, on Ledgerline's real records.

## 0:30–1:30 The system: who does what
**Screen:** **Architecture** (diagram), then **Team**.

> Four agents run in a fixed order on every cycle.
> - **Cash Application** matches the seven unapplied receipts, $87k in total. It applies a payment automatically only when the amount is exact and the memo quotes the invoice. That's Maya's rule.
> - **Account Context** pulls each customer's tickets, contract, contacts and renewal date into one view.
> - **The Controller** is the safety layer. It holds anything that must not be chased and records the reason.
> - **Collections** drafts the policy reminder, or proposes a card re-run.
>
> **Screen:** click one agent on **Team** to show its manual.
>
> Each agent has a plain-English manual that a person can edit. Right now it all runs on rules. The AI is switched off until Legal agrees the data terms. More on that later.

## 1:30–2:00 The headline
**Screen:** ops page **Today**.

> The ledger shows $633k overdue across 54 invoices.
> - $78k of that is money we've already received but haven't applied.
> - $313k is disputed in support tickets that finance never sees.
> - About $242k is actually collectable.
>
> So most of Dana's overdue problem isn't customers refusing to pay. Today the tool stops 23 wrong chases, drafts 20 reminders for Priya to approve, sends 10 to a person to write, proposes 9 card re-runs, and puts 3 decisions in front of Dana.

## 2:00–4:45 Live walkthrough on real records
**2:00 Kingsway: paid but still showing overdue.** **Screen:** **Cash**, PAY-65805, then **Collections** filtered to Kingsway.
> Kingsway Engineering paid $5,100 on 29 October with no reference. They have two $5,100 invoices open, one of them 111 days overdue. The agent proposes the older one and shows the other as an alternative, but it holds both. Paidly would have chased one of these. Priya confirms which invoice it is, and nothing goes out in the meantime.

**2:35 Riverside: a "solved" ticket that is still a dispute.** **Screen:** **Collections**, INV-25787, open the DISPUTE hold.
> Riverside Partners, $60,576, 35 days overdue. In Zendesk the ticket says "solved". The text says they won't pay until the seat count is fixed. The Controller holds the invoice and routes it to the account manager, Nadia Upton. It also runs a contract check: 46 seats at $88 a month plus a $12,000 platform fee comes to exactly $60,576. So the invoice matches the contract, and the AM goes into the call with evidence. All 14 disputed invoices match their contracts. If every claim turned out to be true, the real exposure would be at most about $25k, against $309k on hold.

**3:15 Card re-run.** **Screen:** **Collections**, Glover Engineering INV-25803, RETRY_CARD, then **Approve**.
> Glover Engineering's $1,836 card payment failed, but a charge on the same card went through on 2 October. So instead of an email, the agent proposes re-running the card. It never charges a card on its own. Priya approves each one, and Dana decides if that should ever change. I'll approve this one.

**3:40 Decisions for Dana.** **Screen:** **Today**, "Decisions for Dana", Northgate Creative INV-25433.
> Northgate Creative, $799, 149 days overdue. Tomorrow the old 150-day rule writes it off automatically. Maya said Dana should decide this morning, so the tool flags it as a decision for Dana today. Two more sit next to it: Hollis Nair at $517, nine days from write-off, and Eastman Engineering at $3,264. Eastman's would break Dana's $2,000 limit. That has already happened nine times, $47k in total, with no approval on record.

**4:05 Approve one draft.** **Screen:** **Collections**, Thornfield Consulting INV-25862, open the draft and **Approve/Send**.
> This is a normal case. Thornfield, $39,456, 17 days overdue. The contact is verified, there's no ticket and no payment waiting, so the agent drafted the friendly first reminder and copied the AM. I can edit it. I approve it, and it goes to the audit log under my name.

**4:25 Override a hold with a reason.** **Screen:** **Collections**, Ambrose & Lowell INV-25897, **Override hold**, type the reason, then **Audit**.
> Some holds are over-cautious, and that's deliberate. Ambrose & Lowell is held because a high-priority ticket is open. But the ticket is a product bug, not a billing complaint. I override the hold and type "product bug, not a billing dispute, AM agrees". The audit log keeps who did it, when and why. Maya wants the override rate after a month. If it's high, the rules are too tight.

## 4:45–5:50 Directing the team
**Screen:** **Talk to the team** chat, then **Direct the team**, then **Rules**.

> Priya doesn't need an engineer to change how this works.
> - **Type:** "why is Riverside held?" The team answers with the ticket, the contract check, and who can release the hold.
> - **Type:** "set writeoff_threshold to 50". Nothing changes yet. It shows an **Apply** button, and only my click applies it. **Click Apply.** Then go to **Rules** to show the new value and what changed on the re-run.
> - **Type:** "from now on cc Dana on anything over $40k". That's logged as a proposed instruction. In **Direct the team** I accept it, and it goes into the Collections agent's manual. Until a person accepts it, the manual doesn't change.

## 5:50–7:05 Where it gets things wrong
**Screen:** terminal, then **Documentation** (FAILURES.md), then **Build log**.

> **The BRANDT replay.** **Screen:** terminal, `eval_guardrails.py`, the 1b lines.
> This was the worst thing we found. We took Brandt & Lowell's real $6,324 wire and shortened the payer name to "BRANDT", which is how 416 past receipts arrived. The matcher tied it to Studio Brandt, and the tool drafted a reminder to Brandt & Lowell for money already in the bank. That's the Paidly failure again. We found it, not a customer. The fix: a payment we can't tie to one customer now holds every overdue invoice of the same amount. BRANDT, JESSOP and KINGSWAY now pass. The cost is some extra holds, which Priya clears.
>
> **The complaint counter, 14 down to 1.** **Screen:** **Build log** or FAILURES #7.
> Maya's veto metric is complaints about collections. A keyword count said 14. We checked all 14 by hand, and 13 were customers asking about their own reminder emails, because Ledgerline is invoicing software. The real number is 1, Eastman Engineering. If we'd shipped the keyword count, the veto metric would have looked 14 times worse than it was.
>
> **The Reyes false positive.** **Screen:** **Customers**, Reyes Consulting.
> Reyes asked, "do I void it and raise a new one?" That was about their own client's invoice. But it held a $51k invoice as a dispute. It's fixed now: the ticket came before the invoice and quotes no Ledgerline invoice. Overall, ticket reading is 82% precise.
>
> **What still slips through.** A refusal in a ticket tagged "How-to" with no invoice number still gets a draft. We have two red-team cases for that, and Priya checks the customer's recent tickets before approving. This is exactly the kind of reading Claude should do once Legal says yes.

## 7:05–7:40 The Maya channel
**Screen:** **Maya** tab, scroll through the exchanges and the "What we changed" notes.

> I treated Maya as the COO I report to. I wrote only when I needed a decision or facts the data room couldn't give: five messages out of sixty. Every answer changed the build. Her Paidly story made cash application run first. Her card answer means Priya approves every re-run. Her Legal challenge turned the AI off by default and moved it to Bedrock. And she approved going live with the rules-only version for Priya on Monday, with every match, release and email approved by a person.

## 7:40–8:10 What's next
**Screen:** **One pager**.

> With more time, I'd build four things.
> - A dispute workflow for account managers, with a reply that quotes the contract.
> - The Slack morning digest for Priya, switched on.
> - Claude reading tickets through Bedrock once Legal signs off, measured against the rules.
> - A cash-forecast agent built on the same data, plus renewal billing checks.
>
> And in thirty days I'd sit down with Maya and look at the override rate. That number tells us whether Priya is still using this.

**End:** RIG **Home**. About 1,300 words including screen cues, roughly 8 to 8.5 minutes at a normal pace. If it runs long, cut the "What still slips through" paragraph first.
