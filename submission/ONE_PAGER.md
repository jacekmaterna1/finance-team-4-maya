# Ledgerline Order-to-Cash team: one page

**Live:** https://ledgerline-finance-rig.onrender.com · Data as of 2026-10-31

## Which process
**FIN-1 Collections, with FIN-2 Cash Application as its feeder.** Dana says overdue invoices have risen three quarters running (true year on year), and cash collection is the board's #1 worry. Paidly was switched off in 2025 after chasing a customer whose wire had already arrived. Finance can't see Zendesk, so customers with open complaints get chased too. Collections only works if cash application runs first.

## What the tool does
Four agents run in order, each with a manual people can edit:
1. **Cash Application** matches unapplied receipts.
2. **Account Context** reads tickets, contract, contacts and renewal.
3. **Controller** holds anything that must not be chased, and says why.
4. **Collections** drafts the reminder or proposes a card re-run.

Priya works in the RIG. She approves, edits or overrides each item, and every click is logged.

On the real records, $633k overdue across 54 invoices breaks down as:
- **$78k already received**, not yet applied.
- **$313k disputed in support**: 14 invoices, most on tickets marked "solved". All 14 equal their contract amount, so real exposure is at most about $25k.
- **About $242k collectable.**

It stops 23 wrong chases, drafts 20 reminders for approval, sends 10 to a person to write, proposes 9 card re-runs and raises 3 decisions for Dana. Tested on past receipts, automatic matches were 81 of 81 correct, and all 14 disputes were held.

## What is AI and what stays with a person, and why
Maya: one wrong chase, or a message that reads like a threat to a top-50 account, gets it switched off. Priya must see why and fix it herself. So:
- **Rules:** matching, holds, contact and look-alike domain checks, banned phrases, templates. Predictable, and Priya can edit every rule.
- **Claude, once Legal allows:** reading ticket text (a dispute of our invoice, or a question about the customer's own invoicing?) and rewording drafts. **Off until Legal signs off on the data terms**, then through Amazon Bedrock under the existing AWS agreement. The rules-only version goes to Priya on Monday.
- **A person:** every email, card charge, proposed match and hold release. Account managers release dispute holds, Dana owns write-offs and thresholds, and people write for top-50 and 90+ day accounts. When unsure, it holds: "Over-holding is the right way to be wrong."

## Where it gets things wrong
- **Shortened payer names** ("BRANDT") broke the never-chase-paid rule. The fix holds every invoice of that amount, which over-holds.
- **Ticket reading is 82% precise** (18 of 22). It held Reyes's $51k invoice over a question about its own client. Some refusals tagged How-to still slip through.
- **No line items on invoices**, so the contract check can't see disputed fees or tax. Five disputes need an account manager or tax decision.

## What we'd do with more time
- An account-manager dispute workflow, with replies that quote the contract evidence.
- The Slack morning digest, live.
- Claude ticket reading through Bedrock after Legal signs off, measured against the rules.
- A FIN-7 cash forecast agent on the same data, and FIN-6 renewal billing checks.
- A 30-day review of the hold-override rate with Maya.
