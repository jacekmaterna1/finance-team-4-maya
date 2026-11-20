# Ledgerline Order-to-Cash team: one page

**Live:** https://ledgerline-finance-rig.onrender.com · **Repo (public):** https://github.com/jacekmaterna1/finance-team-4-maya · **Demo video:** https://www.loom.com/share/abfc8277ba614367861637206a2a7d5b · Data as of 2026-10-31

## Which process
**FIN-1 Collections, with FIN-2 Cash Application as its feeder.** Overdue invoices are up year on year, and cash is the board's #1 worry. Paidly was switched off in 2025 after chasing a customer whose wire had already arrived. Finance can't see Zendesk, so customers with open complaints get chased too. Collections only works if cash application runs first.

## What the tool does
Four agents run in order, each with a manual that only people edit: **Cash Application** matches unapplied receipts → **Account Context** reads tickets, contract, contacts and renewal → **Controller** holds anything that must not go out, and says why → **Collections** drafts the reminder or proposes a card re-run. Priya works in the RIG: she approves, edits or overrides each item, and every click is logged.

On the real records, $633k overdue across 54 invoices breaks down as **$78k already received** (not yet applied), **$313k disputed in support** (14 invoices, mostly on tickets marked "solved"; all 14 match their contract, so real exposure is at most about $25k) and **about $242k collectable**.

It stops 23 wrong chases, drafts 33 policy-stage reminders (courtesy notes included) for approval, sends 4 to a person to write, proposes 9 card re-runs and raises 3 decisions for Dana. On past receipts, every automatic match was correct (59 of 59 with the $10k cap), and all 14 disputes were held.

## What is AI and what stays with a person, and why
Maya: one wrong chase, or a message that reads like a threat to a top-50 account, gets it switched off, and Priya must see why and fix it herself. So:
- **Rules:** matching, holds, contact and domain checks, banned phrases, templates. Predictable, and Priya can edit every rule.
- **Claude, once Legal allows:** reading ticket text (a dispute of our invoice, or a question about the customer's own invoicing?) and rewording drafts. **Off until Legal signs off on the data terms**, then through Amazon Bedrock under the existing AWS agreement. The rules-only version goes to Priya on Monday.
- **A person:** every email, card charge, proposed match and hold release. Account managers release dispute holds, Dana owns write-offs and thresholds. When unsure, it holds: "Over-holding is the right way to be wrong."

## Where it gets things wrong
- **Shortened payer names** ("BRANDT") broke the never-chase-paid rule. The fix holds every invoice of that amount, which over-holds until Priya names the payer.
- **Ticket reading is rules-based** (82% precise on flagged tickets). It once read a customer's question about their own client's invoice as a dispute. That's fixed, but wording it hasn't seen will still slip through.
- **No line items on invoices**, so the contract check can't see disputed fees or tax. Five disputes need an account manager or tax decision.

## Limitation, and our recommendation to Scaleworks
Maya only exists in the Scaleworks web chat, so an operator (our Claude Code session driving a browser) carries approved questions to her and her replies back. **Recommendation: expose Maya as an MCP server, so the RIG connects to her directly.**

## What we'd do with more time
**Make Maya directly reachable from the RIG:** with Maya exposed as an MCP server, the RIG gets a "Connect Maya" panel showing "Maya is connected". Approved questions go straight to her and her answers land on the desk, with no operator, during the challenge or after it closes. The RIG would also expose its own MCP endpoint, so any MCP client (Claude, Cowork, or Maya's own agent) can read the team's status and act on it · an account-manager dispute workflow with contract-evidence replies · the Slack morning digest, live · Claude ticket reading through Bedrock after Legal, measured against the rules · a FIN-7 cash forecast agent and FIN-6 renewal billing checks on the same data · a 30-day review of the hold-override rate with Maya.
