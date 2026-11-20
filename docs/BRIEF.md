# Captured brief (read 2026-11-20, pre-start)

## Scaleworks — Ledgerline AI Operator Challenge (apply.scaleworks.com/start)
- Fictional company **Ledgerline**: $8.5m ARR (+6%/yr), 396 customers (professional services firms), $22k ACV,
  46 staff, about break-even. Data as of 2026-10-31.
- **Maya Lindqvist (COO, played by Scaleworks AI)**: "Pick one. Build something that would change how it gets done."
  A person at Scaleworks reads everything and makes every decision.
- Personas: **Dana Ruiz, VP Finance** (overdue invoices up 3 quarters running), Tom Okafor, VP Marketing (demo replies
  take a day), Sam Whitfield, Head of Support (incidents run a week before anyone connects them), Renata Kowalczyk,
  Head of Sales (forecast = judgment on stale data).
- 24 hours from pressing "Begin day one". Any tools.
  Suggested shape: hour 1 read, hour 2 choose and ask Maya, most of it build, last hour record and hand in.
- **Hand in:** the tool (live link or repo, a deck alone is a no), a 5–10 minute demo video, a one-page description,
  and every AI conversation (dead ends included) plus the repo.
- **Judged on:** a tool that changes the job (still used a month later), judgment (what AI should and shouldn't do,
  when it hands over to a person), evidence (works on real records, shows where it gets things wrong).
- Contact before starting: ai@apply.scaleworks.com.

## Finance processes (7 of the 31)
- **FIN-1 Collections and payment reminders**: late, inconsistent reminders. Finance can't see support tickets, so
  customers with open complaints get chased. Failed card payments are rarely followed up.
- **FIN-2 Cash application**: matching lags 3–5 days. Invoices look unpaid when the money has arrived, so customers
  get chased for invoices they already paid.
- FIN-3 Month-end close: takes 8 days, commentary written from scratch, variances explained from memory.
- FIN-4 Board KPI pack: pulled by hand from 4 systems, definitions drift.
- FIN-5 Vendor bills and SaaS spend: nobody owns it, renewals noticed after they've gone through.
- FIN-6 Renewal invoicing and billing changes: wrong seats, prices and contacts lead to disputes.
- FIN-7 Revenue and cash forecast: churn and collections assumptions are guesses.
(Other areas: Sales 6, Marketing 5, CS 5, Support 5, Ops 3. Full list in the data room's processes.md.)

## Data room (51 files, Jan 2023 → 2026-10-31, opens on Begin)
Finance: invoices (6,062), payments (5,808, unmatched = no invoice id), ar_aging (117), pnl_monthly, balance_sheet,
vendor_bills, arr_movements, payroll. Customers: customers (508), contacts (967), contracts (1,757).
Support: tickets (1,041, full text, Jul–Oct 2026), tickets_monthly, help_center_articles, nps_responses.
Docs: collections_policy.md, templates/collections.md (4 templates), process_maps.md, billing_engine_rewrite_2026.md,
board_update_2026_q3.md, processes.md, tool_stack.md, org_chart.md, sla_policy.md, pricing_and_packaging.md.
Also sales, marketing, product usage and employees files.

## Reference architecture — SpaceXSI "Building an accounting team with Grok Bot" (Nov 16 2026), our summary
- Five bots, each owning **one well-defined accounting job end to end**: Provisioning, Billing, Billing Support,
  Cash Applications, Collections. A person is involved only when judgment or approval is needed.
- Lessons: (1) make the process reliable before handing it to a bot, using purpose-built apps with permitted actions and
  an audit log; (2) give each bot an operating manual that only process owners can edit, which the bot re-reads nightly;
  (3) read access is broad, write access is narrow, and sensitive actions such as credits and refunds need named approvers;
  (4) onboard in 3 weeks: observe → propose with a human approving → run alone with escalation.
- Cash Apps bot: matches exact payments automatically, searches support for remittance advice, writes off bank fees,
  flags short payments to collections.
- Collections bot: customer-facing, verifies the sender against CRM and billing contacts (a look-alike domain is
  rejected), and coordinates with the other bots on refunds after approval.
