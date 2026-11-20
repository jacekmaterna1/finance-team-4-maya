# Demo video: Loom talk track (target 8 min, range 7–9)

RIG: https://ledgerline-finance-rig.onrender.com · Repo (public): https://github.com/jacekmaterna1/finance-team-4-maya
Numbers: live run on the data room (as of 2026-10-31). Tabs: **One pager · Cash · Overview · Maya · Documentation · Demo · Your working**, plus **More ▾** (Today, Collections, Customers, Digest, Rules · Team, Architecture, Activity, Direct the team, Audit).

**Before you hit record (2 min)**
- Open the RIG in a clean browser window at full width. It's always on now, so there's no wake-up wait.
- Close other tabs. Turn notifications off.
- Everything you click is written to the audit log. That's fine, and it's part of the evidence.

---

## 0:00–0:40 · What I chose and why — **One pager**
> I'm Jacek. For one day I was Ledgerline's AI Operator. I picked one process and did it properly: collections, with cash application feeding it.
> Three reasons. Overdue invoices are up year on year, and cash is the board's number-one worry. Ledgerline already tried a collections tool: Paidly was switched off after it chased a customer whose wire had already arrived. And finance can't see Zendesk, so customers with open complaints get chased too.
> Both failures are the same mistake: the reminder goes out before anyone checks the cash and the tickets. So cash application has to run first.

## 0:40–1:40 · Who does what — **Documentation** (system diagram)
> This is the whole system on one screen. On the left is Ledgerline: Maya, Dana, Priya, the account managers, Legal, and the systems they use. In the middle are four agents running in a fixed order: Cash Application, Account Context, the Controller, then Collections. At the bottom is how it was built: me directing a team of Claude Code agents, plus GitHub and Render.
> The rule that matters: agents propose and people decide. Nothing reaches a customer, a card or the ledger without a person approving it. Every decision lands in an audit log.
> The AI layer, Claude through Amazon Bedrock, is switched off until Legal signs the data terms. What you're seeing runs on rules Priya can read and edit, and that's the version Maya approved for Priya on Monday.

## 1:40–2:30 · The headline — **Overview**
> The ledger says $633,000 overdue across 54 invoices. The team breaks that down: $78,000 is money we've already received but haven't applied, $313,000 is disputed in support tickets finance never sees, and about $242,000 is genuinely collectable.
> So most of Dana's problem isn't customers refusing to pay. Today it prevents 23 wrong chases, drafts 33 reminders for Priya, proposes 9 card re-runs and puts 3 decisions in front of Dana.
> **Point at** the Monday checklist: everything Maya and Dana still have to sign off.

## 2:30–3:30 · FIN-2, cash first — **Cash**
> Seven receipts arrived without being matched: $87,335, which ties to the unapplied cash on the balance sheet to the dollar. Three were applied automatically, because the amount was exact and the memo quoted the invoice, and they're under a $10,000 cap Dana confirms.
> The other four need Priya. **Click Approve on Brandt & Lowell, $6,324.** The payer name was in capitals and the memo just said "subscription", so it proposes and doesn't apply.
> Kingsway is the interesting one: one $5,100 payment and two open $5,100 invoices. It won't guess. It holds both and asks Priya.

## 3:30–5:00 · FIN-1, collections — **More → Collections**
> **Open Brandt & Lowell, INV-25806:** held as "Money already received". That's the Paidly failure, prevented.
> **Open Riverside Partners, INV-25787, $60,576:** the support ticket is marked "solved", but the customer says they won't pay until the seat count is fixed. Finance couldn't see that before. The contract check shows the invoice matches the contract: 46 seats at $88 plus the $12,000 platform fee. **Click Release without ticking the account-manager box:** refused. Maya's rule is that only the account manager can release a dispute.
> **Open Thornfield Consulting, INV-25862:** a policy reminder in Priya's voice, cc'ing the account manager, with no threats. The old 45-day "suspension" template is retired. **Edit a sentence and click Approve & send.** It's simulated, nothing really leaves. **Then try adding a Gmail address to To:** refused. It only sends to verified contacts.

## 5:00–6:00 · Where it gets things wrong — **Your working**
> I want to show the misses, because that's what decides whether Priya trusts it.
> One: when a bank shortens the payer name, say "BRANDT", the first version would have chased money we already had. The fix holds every invoice of that amount until Priya names the payer. It over-holds, and Maya's words were "over-holding is the right way to be wrong".
> Two: a keyword counter said there were 14 complaints about collections. Thirteen were customers asking about their own reminder emails to their clients. The agent now reads the ticket, and there's one real complaint.
> Three: Maya caught my own arithmetic. I quoted Riverside's seats without the platform fee, she spotted it, and I corrected it before it reached the account managers. It's all in the trail.

## 6:00–7:15 · Working with Maya — **Maya**
> The team raises its own questions, labelled Confirmation or Intel, never status updates. I approve them here, and they go to Maya bundled, to save her message budget. We used 8 of 60.
> Her decisions came straight back into the plan:
> - Eastman gets a call, not a re-run.
> - Northgate and Hollis Nair get a heads-up and then a card re-run.
> - Dana stops the automatic write-offs.
> - Mercer & Banerjee's ignored cancellation stops the renewal.
> - The account managers rule on the five disputes this week.
> **Point at** the limitation callout: today the real Maya only exists in the Scaleworks chat, so an operator carries the messages. My recommendation to Scaleworks is to expose Maya as an MCP server, so the RIG connects to her directly.

## 7:15–8:00 · Direct the team, and close — **Talk to the team** chat
> **Type "why is Kingsway held?"** The Controller explains. **Type "set writeoff_threshold to 50"**: it won't apply without Dana's name. Loosening a guardrail is Dana's call, not mine.
> Close: one process, four agents, a person in charge of every decision, tested on the real records, and honest about where it's wrong. Next would be the account-manager dispute workflow, Claude reading tickets once Legal approves, and connecting to Maya directly. Thanks.

**After recording:** paste the Loom share link on the **Demo** tab (it converts to an embed and is saved on the disk). Then submit on the Scaleworks page.
