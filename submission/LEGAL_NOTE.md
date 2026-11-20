# Note for Legal: AI processing in the Order-to-Cash assistant

**For:** Maya Lindqvist → Legal · **From:** Jacek · **Status:** AI is OFF. Nothing has been sent to any AI provider.

## Service
- **Model:** Anthropic Claude (Sonnet class), called through **Amazon Bedrock** under Ledgerline's existing AWS agreement.
- **Region:** [Engineering to confirm the production AWS region]. Bedrock is used only in that region, the same one as Ledgerline's current production workloads.
- **Bedrock terms (for Legal to confirm against our AWS agreement):** prompts and outputs are not shared with the model
  provider and are not used to train models. No new vendor if our AWS terms already cover Bedrock.
- **Fallback if Bedrock isn't covered:** Anthropic's API directly. Its commercial terms say API inputs and outputs are not used for
  training, and a DPA is available. That would be a new vendor, so it needs a DPA review.

## Main residual risk: ticket text can still name people
- **Ticket bodies can contain personal names, signatures and job titles, even after emails and phone numbers are removed.**
  The ticket-reading task sends up to 2,500 characters of ticket text, so a person's name can reach the model.
- Options for Legal: (a) accept this under the Bedrock terms; (b) also redact personal names before sending, which is
  possible but makes the AI's reading of disputes less accurate; (c) keep ticket reading on rules only, so no ticket text leaves at all.
- Until Legal decides, (c) applies: the AI is off.

## Exactly which fields leave our systems
| Agent task | Fields sent | Never sent |
|---|---|---|
| Read a support ticket (dispute, cancellation, legal threat) | Customer company name; the customer's open Ledgerline invoice IDs; ticket ID, date, category, status, priority; ticket subject and body (first 2,500 characters), **with email addresses and phone numbers removed** before sending | Contact emails, bank or card details, payment records, ARR, contract terms, usage, NPS |
| Rewrite a reminder email | Invoice ID, amount, due date, days past due, payment link, reminder stage, the template text. Contact first name and company are **masked** as `{first}` / `{company}` and filled in on our side afterwards | Everything else |
| Cash application (matching payments) | **Nothing.** Matching runs on our own rules | — |
| Holds, routing, approvals, audit log | **Nothing.** Runs on our own rules | — |

## Controls
- A single setting (`use_claude`) switches the AI on or off. It is off by default. The rules-only version runs fully
  without it and can go in front of Priya on Monday.
- Results are cached on our side, so each ticket is sent at most once.
- Every AI output is shown to Priya with its reasoning before anything happens. Nothing is sent to a customer, charged,
  or written to the ledger without a person approving it.
- Residual risk: personal names in ticket text. See the section at the top.
