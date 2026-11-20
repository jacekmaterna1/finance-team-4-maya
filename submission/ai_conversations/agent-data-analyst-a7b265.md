# Build agent: data-analyst

_Exported from the Claude Code session log. Redactions are explained in the index._

### Jacek · 2026-11-20 17:14:44 UTC
Project root (use absolute paths, quote them, path has spaces): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a"
Data room is in <root>/data (as-of 2026-10-31 = "today"). Python with pandas: "<root>/.venv/bin/python" (system python3 is blocked; do not use it). Run scripts with -I and write scripts into <root>/analysis/scripts/, outputs into <root>/analysis/.

Context: we are building an AI Order-to-Cash team for Ledgerline's VP Finance (Collections FIN-1 + Cash Application FIN-2). Key docs already read: data/docs/collections_policy.md (reminders at -5, +7, +21, +45 days; don't chase disputed invoices or customers with open support escalation; top-50 accounts need a human; write-offs ≤$2k by VP Finance; card invoices unpaid after 150 days auto written off; bank transfers/cheques matched by hand, 3-5 working days lag), data/docs/billing_engine_rewrite_2026.md (16 Mar 2026: proration by exact days, per-line rounding → cent differences, failed card retries, credit notes on edits, due dates in firm's time zone), docs/tool_stack.md (finance has no Zendesk access; Paidly collections tool switched off after 6 weeks in 2025). Read data/docs/processes.md FIN-1 and FIN-2 sections for owners/volumes.

Deliver FAST (target 25 minutes), in this order, writing each file as soon as it's ready:

1. <root>/analysis/SCHEMA.md — for invoices, payments, ar_aging, customers, contacts, contracts, tickets, nps_responses, usage_monthly, opportunities: columns, dtypes, example row, distinct values of status/category/method-type columns, and join keys with join-failure rates. The builder is waiting on this, so do it first (~5 min).

2. <root>/analysis/FACTS.md — evidence numbers, each with how it was computed:
   - AR aging total + buckets; does ar_aging.csv agree with invoices.csv open status? List disagreements.
   - Overdue trend by quarter end for the last 5 quarters (reconstruct from invoices+payments dates) — test Dana's "risen three quarters running".
   - Unapplied receipts (payments with no invoice_id): count, $, by method; how many plausibly correspond to an invoice shown as open/overdue (same customer, amount equal or within bank-fee / rounding tolerance, date after issue). These are "customers being chased for money we already have". Give $ and count, and top examples.
   - Payer-name / memo patterns in payments that help matching (memos referencing invoice numbers, wrong invoice numbers, combined payments covering several invoices, short payments, bank fee deductions like $15/$25/$35, cent rounding diffs post-rewrite).
   - Open overdue invoices whose customer has an open or recent (last 30 days) support ticket, esp. billing category or escalation; count and $.
   - Failed card payments: how they appear in the data, count, $, whether followed up.
   - Top-50 accounts (by ARR/contract value) among overdue.
   - Disputes: how they show up (invoice status? ticket text?).
   - Billing contacts: overdue invoices where the billing contact looks stale (contact left, domain mismatch with customer).
3. <root>/analysis/testset_cash_app.csv — labelled cases for evaluating a cash-application matcher (payment_id, true_invoice_ids, label_source, difficulty), plus a short note in FACTS.md on how labels were derived (e.g., payments later matched in data, memos, unique amount matches) and its limits.

Separate facts from inferences. Flag data-quality traps (name spelling drift, time zones, duplicates). Do not modify data/. Final report to me: ≤15 lines with the headline numbers and the 3 most demo-worthy concrete customer examples (ids, names, $).

### Jacek · 2026-11-20 17:14:44 UTC
[harness system note omitted]

### Jacek ·  UTC
[harness system note omitted]

Project root (use absolute paths, quote them, path has spaces): "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a"
Data room is in <root>/data (as-of 2026-10-31 = "today"). Python with pandas: "<root>/.venv/bin/python" (system python3 is blocked; do not use it). Run scripts with -I and write scripts into <root>/analysis/scripts/, outputs into <root>/analysis/.

Context: we are building an AI Order-to-Cash team for Ledgerline's VP Finance (Collections FIN-1 + Cash Application FIN-2). Key docs already read: data/docs/collections_policy.md (reminders at -5, +7, +21, +45 days; don't chase disputed invoices or customers with open support escalation; top-50 accounts need a human; write-offs ≤$2k by VP Finance; card invoices unpaid after 150 days auto written off; bank transfers/cheques matched by hand, 3-5 working days lag), data/docs/billing_engine_rewrite_2026.md (16 Mar 2026: proration by exact days, per-line rounding → cent differences, failed card retries, credit notes on edits, due dates in firm's time zone), docs/tool_stack.md (finance has no Zendesk access; Paidly collections tool switched off after 6 weeks in 2025). Read data/docs/processes.md FIN-1 and FIN-2 sections for owners/volumes.

Deliver FAST (target 25 minutes), in this order, writing each file as soon as it's ready:

1. <root>/analysis/SCHEMA.md — for invoices, payments, ar_aging, customers, contacts, contracts, tickets, nps_responses, usage_monthly, opportunities: columns, dtypes, example row, distinct values of status/category/method-type columns, and join keys with join-failure rates. The builder is waiting on this, so do it first (~5 min).

2. <root>/analysis/FACTS.md — evidence numbers, each with how it was computed:
   - AR aging total + buckets; does ar_aging.csv agree with invoices.csv open status? List disagreements.
   - Overdue trend by quarter end for the last 5 quarters (reconstruct from invoices+payments dates) — test Dana's "risen three quarters running".
   - Unapplied receipts (payments with no invoice_id): count, $, by method; how many plausibly correspond to an invoice shown as open/overdue (same customer, amount equal or within bank-fee / rounding tolerance, date after issue). These are "customers being chased for money we already have". Give $ and count, and top examples.
   - Payer-name / memo patterns in payments that help matching (memos referencing invoice numbers, wrong invoice numbers, combined payments covering several invoices, short payments, bank fee deductions like $15/$25/$35, cent rounding diffs post-rewrite).
   - Open overdue invoices whose customer has an open or recent (last 30 days) support ticket, esp. billing category or escalation; count and $.
   - Failed card payments: how they appear in the data, count, $, whether followed up.
   - Top-50 accounts (by ARR/contract value) among overdue.
   - Disputes: how they show up (invoice status? ticket text?).
   - Billing contacts: overdue invoices where the billing contact looks stale (contact left, domain mismatch with customer).
3. <root>/analysis/testset_cash_app.csv — labelled cases for evaluating a cash-application matcher (payment_id, true_invoice_ids, label_source, difficulty), plus a short note in FACTS.md on how labels were derived (e.g., payments later matched in data, memos, unique amount matches) and its limits.

Separate facts from inferences. Flag data-quality traps (name spelling drift, time zones, duplicates). Do not modify data/. Final report to me: ≤15 lines with the headline numbers and the 3 most demo-worthy concrete customer examples (ids, names, $).

[harness system note omitted]

### Claude · 2026-11-20 17:14:48 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R\"; find data -type f | sort | xargs wc -l | tail -50; ls analysis 2>/dev/null; mkdir -p analysis/scripts",
 "description": "List data room files with line counts"
}
```

### Tool · 2026-11-20 17:14:48 UTC
**Tool result:**
```
    1758 data/customers/contracts.csv
     509 data/customers/customers.csv
      16 data/docs/billing_engine_rewrite_2026.md
      33 data/docs/board_update_2026_q3.md
      10 data/docs/collections_policy.md
      45 data/docs/company_overview.md
      24 data/docs/icp.md
      73 data/docs/org_chart.md
      24 data/docs/pricing_and_packaging.md
      86 data/docs/process_maps.md
     615 data/docs/processes.md
      23 data/docs/sales_playbook.md
      19 data/docs/sla_policy.md
      81 data/docs/templates/collections.md
     184 data/docs/templates/nurture.md
      48 data/docs/templates/renewal.md
      63 data/docs/templates/sdr.md
      86 data/docs/templates/support_macro.md
      25 data/docs/tool_stack.md
     118 data/finance/ar_aging.csv
      47 data/finance/arr_movements_monthly.csv
      47 data/finance/balance_sheet_monthly.csv
    6063 data/finance/invoices.csv
    5809 data/finance/payments.csv
     369 data/finance/payroll_monthly.csv
     967 data/finance/pnl_monthly.csv
    1652 data/finance/vendor_bills.csv
     225 data/marketing/blog_posts.csv
     128 data/marketing/competitor_battlecards.md
     231 data/marketing/marketing_spend_monthly.csv
      49 data/marketing/reviews.csv
     415 data/marketing/web_funnel_monthly.csv
      53 data/people/employees.csv
    6956 data/product/usage_monthly.csv
     419 data/sales/deal_notes.csv
   14574 data/sales/leads.csv
    2177 data/sales/opportunities.csv
      27 data/sales/proposals/proposal_OPP-41952.md
      27 data/sales/proposals/proposal_OPP-41988.md
      27 data/sales/proposals/proposal_OPP-41999.md
      27 data/sales/proposals/proposal_OPP-42035.md
      27 data/sales/proposals/proposal_OPP-42065.md
      28 data/sales/proposals/proposal_OPP-42071.md
      27 data/sales/proposals/proposal_OPP-42083.md
      27 data/sales/proposals/proposal_OPP-42084.md
    1494 data/support/help_center_articles.csv
     821 data/support/nps_responses.csv
    2890 data/support/tickets.csv
      47 data/support/tickets_monthly.csv
   50572 total
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R\"; find data -type f | sort | xargs wc -l | tail -50; ls analysis 2>/dev/null; mkdir -p analysis/scripts",
 "description": "List data room files with line counts"
}
```

### Claude · 2026-11-20 17:14:54 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; ls -la; for f in finance/invoices.csv finance/payments.csv finance/ar_aging.csv customers/customers.csv customers/contracts.csv support/tickets.csv support/nps_responses.csv product/usage_monthly.csv sales/opportunities.csv; do echo \"== $f\"; head -3 $f; done; cat docs/collections_policy.md docs/billing_engine_rewrite_2026.md; grep -n -i \"contact\\|listing\\|row\" docs/*.md | head -30",
 "description": "Peek at file headers and key docs"
}
```

### Tool · 2026-11-20 17:14:54 UTC
**Tool result:**
```
total 16
drwxr-xr-x@ 11 jacekmaterna  staff   352 Nov 20 11:11 .
drwx------@  9 jacekmaterna  staff   288 Nov 20 11:14 ..
-rw-r--r--@  1 jacekmaterna  staff  7869 Nov 14 09:31 README.md
drwxr-xr-x@  5 jacekmaterna  staff   160 Nov 14 09:31 customers
drwxr-xr-x@ 15 jacekmaterna  staff   480 Nov 14 09:31 docs
drwxr-xr-x@ 10 jacekmaterna  staff   320 Nov 14 09:31 finance
drwxr-xr-x@  7 jacekmaterna  staff   224 Nov 14 09:31 marketing
drwxr-xr-x@  3 jacekmaterna  staff    96 Nov 14 09:31 people
drwxr-xr-x@  3 jacekmaterna  staff    96 Nov 14 09:31 product
drwxr-xr-x@  6 jacekmaterna  staff   192 Nov 14 09:31 sales
drwxr-xr-x@  6 jacekmaterna  staff   192 Nov 14 09:31 support
== finance/invoices.csv
invoice_id,customer_id,customer_name,type,issue_date,due_date,service_period_months,amount,currency,status,paid_date,payment_method
INV-20001,C1194,Stanhope Engineering,subscription,2022-01-03,2022-02-02,12,5400.00,USD,paid,2022-02-03,check
INV-20002,C1195,Hartwell Engineering,subscription,2022-01-05,2022-02-04,3,3900.00,USD,paid,2022-03-01,ach
== finance/payments.csv
payment_id,received_date,amount,method,payer_name,memo,applied_date,invoice_id
PAY-60001,2022-01-12,405.00,card,Corbin Design Partnership,Stripe charge INV-20013,2022-01-12,INV-20013
PAY-60002,2022-01-18,585.00,card,Okafor Consulting,Stripe charge INV-20017,2022-01-18,INV-20017
== finance/ar_aging.csv
invoice_id,customer_id,customer_name,plan,issue_date,due_date,amount,days_past_due,bucket,status
INV-25433,C1029,Northgate Creative,Core,2026-06-04,2026-06-04,799.00,149,Over 90 days,payment_failed
INV-25469,C1469,Kingsway Engineering Group,Growth,2026-06-12,2026-07-12,5100.00,111,Over 90 days,overdue
== customers/customers.csv
customer_id,name,website,industry,country,employees,plan,status,signup_date,churn_date,churn_reason,billing_frequency,payment_method,current_seats,current_arr,renewal_date,account_manager,acquisition_channel,accounting_integration
C1001,Lowell Consulting,lowellconsulting.example,Management consultancy,United States,28,Core,churned,2019-01-01,2026-01-01,Low adoption,annual,wire,0,0,,Nadia Upton,,none
C1002,Quill + Ingram Architects,quillingramarchitects.example,Architecture practice,United States,75,Growth,active,2019-01-09,,,annual,ach,19,15504,2027-01-09,Maria Yardley,,none
== customers/contracts.csv
customer_id,term_start,term_end,plan,seats,price_per_seat_per_month,platform_fee,arr,change_type,prior_arr
C1001,2023-01-01,2023-12-31,Core,18,45,0,9720,in force at 1 Jan 2023,
C1001,
… [result truncated, 9784 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; ls -la; for f in finance/invoices.csv finance/payments.csv finance/ar_aging.csv customers/customers.csv customers/contracts.csv support/tickets.csv support/nps_responses.csv product/usage_monthly.csv sales/opportunities.csv; do echo \"== $f\"; head -3 $f; done; cat docs/collections_policy.md docs/billing_engine_rewrite_2026.md; grep -n -i \"contact\\|listing\\|row\" docs/*.md | head -30",
 "description": "Peek at file headers and key docs"
}
```

### Claude · 2026-11-20 17:14:57 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; cat README.md; ls -la customers; grep -n \"FIN-1\\|FIN-2\" -A30 docs/processes.md | head -90",
 "description": "Read README and FIN process sections"
}
```

### Tool · 2026-11-20 17:14:58 UTC
**Tool result:**
```
# Ledgerline data room

Ledgerline is a fictional B2B software company. Everything here was invented for the Scaleworks AI Operator Challenge: no real company, person or customer is described. Use any of it, in any way, to build your tool.

- **As-of date:** 2026-10-31. Treat that as today.
- **History:** January 2023 to October 2026.
- **Currency:** US dollars throughout. Amounts exclude sales tax.
- **Start with:** `docs/company_overview.md`, then `docs/processes.md`.

## Files

### Documents

| File | Size | What it is |
|---|---|---|
| `docs/templates/collections.md` | document | Collections reminders: the 4 templates in use today. |
| `docs/templates/nurture.md` | document | Lead nurture sequences: the 9 templates in use today. |
| `docs/templates/sdr.md` | document | Sales development replies: the 3 templates in use today. |
| `docs/templates/support_macro.md` | document | Support macros: the 4 templates in use today. |
| `docs/templates/renewal.md` | document | Renewal emails: the 2 templates in use today. |
| `docs/billing_engine_rewrite_2026.md` | document | What changed in the product when the billing engine was replaced in March 2026. |
| `docs/company_overview.md` | document | What Ledgerline sells, who to, and the headline numbers. |
| `docs/org_chart.md` | document | Who works where and who they report to. |
| `docs/pricing_and_packaging.md` | document | The internal price list, plan contents and discount rules. |
| `docs/tool_stack.md` | document | Which tools the company uses, for what, and the gaps between them. |
| `docs/icp.md` | document | The ideal customer profile document, as last written by marketing. |
| `docs/sales_playbook.md` | document | How inbound leads are meant to be handled and routed, and the rules for replies. |
| `docs/sla_policy.md` | document | Support response commitments and the rules for sensitive tickets. |
| `docs/collections_policy.md` | document | The rules finance follows when chasing overdue invoices. |
| `docs/board_update_2026_q3.md` | document | The most recent board update, with the quarter's numbers and the leadership's stated concerns. |
| `docs/processes.md` | document | The 31 business processes you can choose from, with owner, volume, steps and pain. |
| `docs/process_maps.md` | document | Flow diagrams for collections, cash application, inbound leads, ticket triage and renewals. |

### Customers

| File | Size | What it is |
|---|---|---|
| `customers/customers.csv` | 508 rows | Every customer, acti
… [result truncated, 10568 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; cat README.md; ls -la customers; grep -n \"FIN-1\\|FIN-2\" -A30 docs/processes.md | head -90",
 "description": "Read README and FIN process sections"
}
```

### Claude · 2026-11-20 17:15:05 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/schema.py",
 "content": "import sys, os, pandas as pd\nD = sys.argv[1]\nfiles = {\n 'invoices':'finance/invoices.csv','payments':'finance/payments.csv','ar_aging':'finance/ar_aging.csv',\n 'customers':'customers/customers.csv','contacts':'customers/contacts.csv','contracts':'customers/contracts.csv',\n 'tickets':'support/tickets.csv','nps_responses':'support/nps_responses.csv','usage_monthly':'product/usage_monthly.csv',\n 'opportunities':'sales/opportunities.csv'}\nexpected = {'invoices':6062,'payments':5808,'ar_aging':117,'customers':508,'contacts':967,'contracts':1757,\n 'tickets':1041,'nps_responses':820,'usage_monthly':6955,'opportunities':2176}\ndf = {k: pd.read_csv(os.path.join(D,v), dtype=str, keep_default_na=False) for k,v in files.items()}\nfor k,d in df.items():\n    print(f\"\\n### {k} ({files[k]}) rows={len(d)} expected={expected[k]}\")\n    print(\"cols:\", list(d.columns))\n    print(\"example:\", d.iloc[0].to_dict() if k!='tickets' else {c:(d.iloc[0][c][:80]) for c in d.columns})\n    for c in d.columns:\n        n = d[c].nunique()\n        blank = (d[c]=='').sum()\n        if n <= 15:\n            print(f\"  {c}: blanks={blank} values={d[c].value_counts().to_dict()}\")\n        else:\n            print(f\"  {c}: nunique={n} blanks={blank}\")\n"
}
```

### Claude · 2026-11-20 17:15:06 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/schema.py\" \"$R/data\"",
 "description": "Run schema profiling script"
}
```

### Tool · 2026-11-20 17:15:07 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/schema.py (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:15:08 UTC
**Tool result:**
```
### invoices (finance/invoices.csv) rows=6062 expected=6062
cols: ['invoice_id', 'customer_id', 'customer_name', 'type', 'issue_date', 'due_date', 'service_period_months', 'amount', 'currency', 'status', 'paid_date', 'payment_method']
example: {'invoice_id': 'INV-20001', 'customer_id': 'C1194', 'customer_name': 'Stanhope Engineering', 'type': 'subscription', 'issue_date': '2022-01-03', 'due_date': '2022-02-02', 'service_period_months': '12', 'amount': '5400.00', 'currency': 'USD', 'status': 'paid', 'paid_date': '2022-02-03', 'payment_method': 'check'}
  invoice_id: nunique=6062 blanks=0
  customer_id: nunique=508 blanks=0
  customer_name: nunique=508 blanks=0
  type: blanks=0 values={'subscription': 5938, 'implementation': 124}
  issue_date: nunique=1555 blanks=0
  due_date: nunique=1578 blanks=0
  service_period_months: blanks=0 values={'1': 3784, '3': 1188, '12': 1090}
  amount: nunique=322 blanks=0
  currency: blanks=0 values={'USD': 6062}
  status: blanks=0 values={'paid': 5801, 'written_off': 144, 'open': 63, 'overdue': 38, 'payment_failed': 16}
  paid_date: nunique=1628 blanks=117
  payment_method: blanks=0 values={'card': 3402, 'ach': 1789, 'wire': 681, 'check': 190}

### payments (finance/payments.csv) rows=5808 expected=5808
cols: ['payment_id', 'received_date', 'amount', 'method', 'payer_name', 'memo', 'applied_date', 'invoice_id']
example: {'payment_id': 'PAY-60001', 'received_date': '2022-01-12', 'amount': '405.00', 'method': 'card', 'payer_name': 'Corbin Design Partnership', 'memo': 'Stripe charge INV-20013', 'applied_date': '2022-01-12', 'invoice_id': 'INV-20013'}
  payment_id: nunique=5808 blanks=0
  received_date: nunique=1632 blanks=0
  amount: nunique=318 blanks=0
  method: blanks=0 values={'card': 3242, 'ach': 1728, 'wire': 655, 'check': 183}
  payer_name: nunique=845 blanks=0
  memo: nunique=5199 blanks=102
  applied_date: nunique=1625 blanks=7
  invoice_id: nunique=5802 blanks=7

### ar_aging (finance/ar_aging.csv) rows=117 expected=117
cols: ['invoice_id', 'customer_id', 'customer_name', 'plan', 'issue_date', 'due_date', 'amount', 'days_past_due', 'bucket', 'status']
example: {'invoice_id': 'INV-25433', 'customer_id': 'C1029', 'customer_name': 'Northgate Creative', 'plan': 'Core', 'issue_date': '2026-06-04', 'due_date': '2026-06-04', 'amount': '799.00', 'days_past_due': '149', 'bucket': 'Over 90 days', 'status': 'payment_failed'}
  invoice_id: nunique=117 blanks=0
  customer_id: nunique=107 blanks=0
  customer_name: nunique=107 blanks
… [result truncated, 13215 chars total]
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/schema.py",
 "content": "import sys, os, pandas as pd\nD = sys.argv[1]\nfiles = {\n 'invoices':'finance/invoices.csv','payments':'finance/payments.csv','ar_aging':'finance/ar_aging.csv',\n 'customers':'customers/customers.csv','contacts':'customers/contacts.csv','contracts':'customers/contracts.csv',\n 'tickets':'support/tickets.csv','nps_responses':'support/nps_responses.csv','usage_monthly':'product/usage_monthly.csv',\n 'opportunities':'sales/opportunities.csv'}\nexpected = {'invoices':6062,'payments':5808,'ar_aging':117,'customers':508,'contacts':967,'contracts':1757,\n 'tickets':1041,'nps_responses':820,'usage_monthly':6955,'opportunities':2176}\ndf = {k: pd.read_csv(os.path.join(D,v), dtype=str, keep_default_na=False) for k,v in files.items()}\nfor k,d in df.items():\n    print(f\"\\n### {k} ({files[k]}) rows={len(d)} expected={expected[k]}\")\n    print(\"cols:\", list(d.columns))\n    print(\"example:\", d.iloc[0].to_dict() if k!='tickets' else {c:(d.iloc[0][c][:80]) for c in d.columns})\n    for c in d.columns:\n        n = d[c].nunique()\n        blank = (d[c]=='').sum()\n        if n <= 15:\n            print(f\"  {c}: blanks={blank} values={d[c].value_counts().to_dict()}\")\n        else:\n            print(f\"  {c}: nunique={n} blanks={blank}\")\n"
}
```
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/schema.py\" \"$R/data\"",
 "description": "Run schema profiling script"
}
```

### Claude · 2026-11-20 17:15:25 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/joins.py",
 "content": "import sys, os, re, pandas as pd\nD = sys.argv[1]\nr = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv')\ncus=r('customers/customers.csv'); con=r('customers/contacts.csv'); ctr=r('customers/contracts.csv')\ntk=r('support/tickets.csv'); nps=r('support/nps_responses.csv'); us=r('product/usage_monthly.csv'); opp=r('sales/opportunities.csv')\ncid=set(cus.customer_id); name=dict(zip(cus.customer_id,cus.name))\ndef rate(lbl, s, ref):\n    s=s[s!='']; miss=(~s.isin(ref)).sum(); print(f\"{lbl}: n={len(s)} missing={miss} ({miss/len(s):.2%})\")\ndef namedrift(lbl, df, idc, nc):\n    m=df[df[idc].isin(cid)]; d=m[m[nc]!=m[idc].map(name)]\n    print(f\"{lbl} name!=customers.name: {len(d)}/{len(m)} rows, {d[idc].nunique()} customers\")\n    print(d[[idc,nc]].drop_duplicates().assign(master=lambda x:x[idc].map(name)).head(8).to_string())\nrate('invoices.customer_id->customers', inv.customer_id, cid); namedrift('invoices',inv,'customer_id','customer_name')\nrate('ar_aging.invoice_id->invoices', ar.invoice_id, set(inv.invoice_id)); rate('ar_aging.customer_id->customers', ar.customer_id, cid); namedrift('ar_aging',ar,'customer_id','customer_name')\nrate('payments.invoice_id->invoices', pay.invoice_id, set(inv.invoice_id))\nprint('payments invoice_id dup:', pay[pay.invoice_id!=''].invoice_id.duplicated().sum())\n# payer name vs invoice customer\np=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amount','status','payment_method']],on='invoice_id',how='left',suffixes=('','_inv'))\npm=p[p.payer_name!=p.customer_name]\nprint(f\"payer_name != invoice customer_name: {len(pm)}/{len(p)} ({len(pm)/len(p):.1%})\")\nprint(pm[['payer_name','customer_name','method']].sample(15,random_state=1).to_string())\nprint('payer_name exact match to any customers.name:', pay.payer_name.isin(set(cus.name)).mean())\nrate('contacts.customer_id', con.customer_id, cid); rate('contracts.customer_id', ctr.customer_id, cid)\nrate('tickets.customer_id', tk.customer_id, cid); namedrift('tickets',tk,'customer_id','customer_name')\nrate('nps.customer_id', nps.customer_id, cid); rate('usage.customer_id', us.customer_id, cid)\nrate('opps.customer_id', opp.customer_id, cid); namedrift('opps',opp,'customer_id','account_name')\n# email domain vs website\ndom=lambda e: e.split('@')[-1].lower()\nweb=dict(zip(cus.customer_id,cus.website.str.lower()))\ncon['dom_ok']=[dom(e)==web.get(c) for e,c in zip(con.email,con.customer_id)]\nprint('contacts domain != website:', (~con.dom_ok).sum(), con[~con.dom_ok][['customer_id','email','role','status']].head(10).to_string())\ntk['dom_ok']=[dom(e)==web.get(c) for e,c in zip(tk.requester_email,tk.customer_id)]\nprint('tickets requester domain != website:', (~tk.dom_ok).sum(), tk[~tk.dom_ok][['customer_id','requester_email']].head(5).to_string())\n# billing contacts per customer\nbill=con[con.role.str.contains('billing',case=False)]\nprint('customers with no billing contact:', len(cid-set(bill.customer_id)))\nprint('customers whose all billing contacts left:', (bill.groupby('customer_id').status.apply(lambda s:(s!='active').all())).sum())\n# memo patterns\nprint(pay.memo.str.replace(r'\\d','#',regex=True).value_counts().head(40).to_string())\nprint(pay[pay.invoice_id==''].to_string())\n"
}
```

### Claude · 2026-11-20 17:15:27 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/joins.py\" \"$R/data\"",
 "description": "Run join-failure and memo pattern analysis"
}
```

### Tool · 2026-11-20 17:15:27 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/joins.py (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:15:29 UTC
**Tool result:**
```
invoices.customer_id->customers: n=6062 missing=0 (0.00%)
invoices name!=customers.name: 0/6062 rows, 0 customers
Empty DataFrame
Columns: [customer_id, customer_name, master]
Index: []
ar_aging.invoice_id->invoices: n=117 missing=0 (0.00%)
ar_aging.customer_id->customers: n=117 missing=0 (0.00%)
ar_aging name!=customers.name: 0/117 rows, 0 customers
Empty DataFrame
Columns: [customer_id, customer_name, master]
Index: []
payments.invoice_id->invoices: n=5801 missing=0 (0.00%)
payments invoice_id dup: 0
payer_name != invoice customer_name: 1156/5801 (19.9%)
                            payer_name                     customer_name method
4868  TAN ZELLER CHARTERED ACCOUNTANTS  Tan Zeller Chartered Accountants   wire
952                    PETROV STRATEGY                   Petrov Strategy    ach
3270                NORTHGATE CREATIVE                Northgate Creative   card
5237            ROSALES IYER ENGINEERS            Rosales Iyer Engineers    ach
4755                GLOVER ENGINEERING                Glover Engineering   card
4620                      HADDAD MEDIA                      Haddad Media   card
2816              LAKESHORE CONSULTING        Lakeshore Consulting Group   card
404                     MBEKI STRATEGY                    Mbeki Strategy    ach
1039                              MOTT                   Mott Consulting   card
3446        KESSLER DESIGN PARTNERSHIP        Kessler Design Partnership   card
255                                TAN                    Tan Consulting   wire
3980         CORBIN DESIGN PARTNERSHIP         Corbin Design Partnership   card
3744                 HARBOR CONSULTING           Harbor Consulting Group   card
432                   STUDIO KOWALCZYK                  Studio Kowalczyk   card
1538                      ZELLER LEGAL                      Zeller Legal   card
payer_name exact match to any customers.name: 0.8004476584022039
contacts.customer_id: n=967 missing=0 (0.00%)
contracts.customer_id: n=1757 missing=0 (0.00%)
tickets.customer_id: n=1041 missing=0 (0.00%)
tickets name!=customers.name: 0/1041 rows, 0 customers
Empty DataFrame
Columns: [customer_id, customer_name, master]
Index: []
nps.customer_id: n=820 missing=0 (0.00%)
usage.customer_id: n=6955 missing=0 (0.00%)
opps.customer_id: n=1645 missing=0 (0.00%)
opps name!=customers.name: 0/1645 rows, 0 customers
Empty DataFrame
Columns: [customer_id, account_name, master]
Index: []
contacts domain != website: 0 Empty DataFrame
Columns: [customer_id, email
… [result truncated, 4989 chars total]
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/joins.py",
 "content": "import sys, os, re, pandas as pd\nD = sys.argv[1]\nr = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv')\ncus=r('customers/customers.csv'); con=r('customers/contacts.csv'); ctr=r('customers/contracts.csv')\ntk=r('support/tickets.csv'); nps=r('support/nps_responses.csv'); us=r('product/usage_monthly.csv'); opp=r('sales/opportunities.csv')\ncid=set(cus.customer_id); name=dict(zip(cus.customer_id,cus.name))\ndef rate(lbl, s, ref):\n    s=s[s!='']; miss=(~s.isin(ref)).sum(); print(f\"{lbl}: n={len(s)} missing={miss} ({miss/len(s):.2%})\")\ndef namedrift(lbl, df, idc, nc):\n    m=df[df[idc].isin(cid)]; d=m[m[nc]!=m[idc].map(name)]\n    print(f\"{lbl} name!=customers.name: {len(d)}/{len(m)} rows, {d[idc].nunique()} customers\")\n    print(d[[idc,nc]].drop_duplicates().assign(master=lambda x:x[idc].map(name)).head(8).to_string())\nrate('invoices.customer_id->customers', inv.customer_id, cid); namedrift('invoices',inv,'customer_id','customer_name')\nrate('ar_aging.invoice_id->invoices', ar.invoice_id, set(inv.invoice_id)); rate('ar_aging.customer_id->customers', ar.customer_id, cid); namedrift('ar_aging',ar,'customer_id','customer_name')\nrate('payments.invoice_id->invoices', pay.invoice_id, set(inv.invoice_id))\nprint('payments invoice_id dup:', pay[pay.invoice_id!=''].invoice_id.duplicated().sum())\n# payer name vs invoice customer\np=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amount','status','payment_method']],on='invoice_id',how='left',suffixes=('','_inv'))\npm=p[p.payer_name!=p.customer_name]\nprint(f\"payer_name != invoice customer_name: {len(pm)}/{len(p)} ({len(pm)/len(p):.1%})\")\nprint(pm[['payer_name','customer_name','method']].sample(15,random_state=1).to_string())\nprint('payer_name exact match to any customers.name:', pay.payer_name.isin(set(cus.name)).mean())\nrate('contacts.customer_id', con.customer_id, cid); rate('contracts.customer_id', ctr.customer_id, cid)\nrate('tickets.customer_id', tk.customer_id, cid); namedrift('tickets',tk,'customer_id','customer_name')\nrate('nps.customer_id', nps.customer_id, cid); rate('usage.customer_id', us.customer_id, cid)\nrate('opps.customer_id', opp.customer_id, cid); namedrift('opps',opp,'customer_id','account_name')\n# email domain vs website\ndom=lambda e: e.split('@')[-1].lower()\nweb=dict(zip(cus.customer_id,cus.website.str.lower()))\ncon['dom_ok']=[dom(e)==web.get(c) for e,c in zip(con.email,con.customer_id)]\nprint('contacts domain != website:', (~con.dom_ok).sum(), con[~con.dom_ok][['customer_id','email','role','status']].head(10).to_string())\ntk['dom_ok']=[dom(e)==web.get(c) for e,c in zip(tk.requester_email,tk.customer_id)]\nprint('tickets requester domain != website:', (~tk.dom_ok).sum(), tk[~tk.dom_ok][['customer_id','requester_email']].head(5).to_string())\n# billing contacts per customer\nbill=con[con.role.str.contains('billing',case=False)]\nprint('customers with no billing contact:', len(cid-set(bill.customer_id)))\nprint('customers whose all billing contacts left:', (bill.groupby('customer_id').status.apply(lambda s:(s!='active').all())).sum())\n# memo patterns\nprint(pay.memo.str.replace(r'\\d','#',regex=True).value_counts().head(40).to_string())\nprint(pay[pay.invoice_id==''].to_string())\n"
}
```
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/joins.py\" \"$R/data\"",
 "description": "Run join-failure and memo pattern analysis"
}
```

### Claude · 2026-11-20 17:15:54 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/explore.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD = sys.argv[1]\nr = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv'); cus=r('customers/customers.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float); ar['amt']=ar.amount.astype(float)\n# payer name drift classes\np=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amt','issue_date','due_date','status','paid_date','payment_method']],on='invoice_id',suffixes=('','_inv'))\ndef cls(a,b):\n    if a==b: return 'exact'\n    if a==b.upper(): return 'uppercase'\n    if b.lower().startswith(a.lower()): return 'truncated'\n    if a.lower() in b.lower(): return 'substring'\n    return 'other'\np['ncls']=[cls(a,b) for a,b in zip(p.payer_name,p.customer_name)]\nprint(p.ncls.value_counts()); print(p[p.ncls=='other'][['payer_name','customer_name']].drop_duplicates().head(30).to_string())\nprint(pd.crosstab(p.ncls,p.method))\n# amount diffs\np['diff']=(p.amt-p.amt_inv).round(2)\nprint('amount diff distribution:'); print(p['diff'].value_counts().head(25))\nprint(p[p['diff']!=0][['payment_id','received_date','amt','amt_inv','diff','method','memo','invoice_id']].head(40).to_string())\n# method mismatch\nprint('method mismatch:', (p.method!=p.payment_method).sum())\n# memo referencing invoice id vs applied\ndef memo_inv(m):\n    x=re.findall(r'(?:INV-?|inv|Invoice )\\s?(\\d{5})',m); return ['INV-'+i for i in x]\np['memo_inv']=p.memo.map(memo_inv)\np['memo_n']=p.memo_inv.map(len)\np['memo_ok']=[ (i in l) if l else None for i,l in zip(p.invoice_id,p.memo_inv)]\nprint('memo refs count:', p.memo_n.value_counts().to_dict()); print('memo ref equals applied:', p.memo_ok.value_counts(dropna=False).to_dict())\nprint(p[p.memo_ok==False][['payment_id','received_date','amt','amt_inv','memo','invoice_id','customer_name','payer_name']].head(30).to_string())\n# lag\np['lag']=(pd.to_datetime(p.applied_date)-pd.to_datetime(p.received_date)).dt.days\nprint('apply lag by method:'); print(p.groupby('method').lag.describe())\np['pd_vs_applied']=(p.paid_date==p.applied_date)\nprint('invoice paid_date == applied_date:', p.pd_vs_applied.mean(), ' paid_date==received:', (p.paid_date==p.received_date).mean())\n# statuses of invoices that have payments\nprint(p.status.value_counts())\n# recent applied after as-of?\nprint('applied after 2026-10-31:', (p.applied_date>'2026-10-31').sum(), 'received after:', (pay.received_date>'2026-10-31').sum())\nprint('max dates', pay.received_date.max(), pay.applied_date.max(), inv.issue_date.max())\n# open invoices\nop=inv[inv.status.isin(['open','overdue','payment_failed'])]\nprint(op.groupby(['status','payment_method']).amt.agg(['count','sum']))\nm=ar.merge(inv,on='invoice_id',suffixes=('_ar','_inv'))\nfor c in ['customer_id','issue_date','due_date','status']:\n    print(c,'disagree', (m[c+'_ar']!=m[c+'_inv']).sum())\nprint('amount disagree', (m.amt_ar!=m.amt_inv).sum())\nprint('open in invoices not in ar:', len(set(op.invoice_id)-set(ar.invoice_id)), 'ar not open in invoices:', len(set(ar.invoice_id)-set(op.invoice_id)))\n# days past due recompute\nasof=pd.Timestamp('2026-10-31')\nm['dpd_calc']=(asof-pd.to_datetime(m.due_date_inv)).dt.days\nprint('dpd disagree', (m.dpd_calc!=m.days_past_due.astype(int)).sum()); print(m[m.dpd_calc!=m.days_past_due.astype(int)][['invoice_id','due_date_inv','days_past_due','dpd_calc','bucket']].head(20).to_string())\ndef bk(d): return 'Not yet due' if d<=0 else '1-30 days' if d<=30 else '31-60 days' if d<=60 else '61-90 days' if d<=90 else 'Over 90 days'\nm['bk_calc']=m.dpd_calc.map(bk); print('bucket disagree', (m.bk_calc!=m.bucket).sum()); print(m[m.bk_calc!=m.bucket][['invoice_id','due_date_inv','days_past_due','dpd_calc','bucket','bk_calc','status_ar']].to_string())\n# status vs due\nprint(pd.crosstab(m.status_ar,m.bk_calc))\nprint(ar.groupby('bucket').amt.agg(['count','sum'])); print('total', ar.amt.sum())\n# due date = issue +30 check\ninv['dd']=(pd.to_datetime(inv.due_date)-pd.to_datetime(inv.issue_date)).dt.days\nprint(pd.crosstab(inv.dd, inv.payment_method))\nprint(pd.crosstab(inv.dd, inv.issue_date>='2026-03-16'))\n# written off\nwo=inv[inv.status=='written_off']; print('written off', len(wo), wo.amt.sum()); print(wo.groupby([wo.payment_method, wo.issue_date.str[:4]]).amt.agg(['count','sum']))\nprint(wo[wo.paid_date!=''].head())\n# pay after write-off? payments against written off\nprint('payments to written_off invoices', (p.status=='written_off').sum())\n# unapplied\nun=pay[pay.invoice_id=='']\nfor _,u in un.iterrows():\n    print('\\nUNAPPLIED',u.payment_id,u.received_date,u.amt,u.method,u.payer_name,'|',u.memo)\n    key=u.payer_name.lower().split()[0].strip(',')\n    c=cus[cus.name.str.lower().str.contains(re.escape(key))]\n    print(c[['customer_id','name','payment_method','current_arr','billing_frequency']].to_string())\n    print(inv[inv.customer_id.isin(c.customer_id)&(inv.issue_date>='2026-01-01')][['invoice_id','customer_id','issue_date','due_date','amt','status','paid_date','payment_method']].to_string())\n"
}
```

### Claude · 2026-11-20 17:15:56 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/explore.py\" \"$R/data\" 2>&1",
 "description": "Explore payment matching, AR agreement, unapplied receipts"
}
```

### Tool · 2026-11-20 17:15:56 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/explore.py (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:15:58 UTC
**Tool result:**
```
ncls
exact        4645
uppercase     740
truncated     416
Name: count, dtype: int64
Empty DataFrame
Columns: [payer_name, customer_name]
Index: []
method      ach  card  check  wire
ncls                              
exact      1386  2597    155   507
truncated    78   286      8    44
uppercase   259   359     20   102
amount diff distribution:
diff
0.0    5801
Name: count, dtype: int64
Empty DataFrame
Columns: [payment_id, received_date, amt, amt_inv, diff, method, memo, invoice_id]
Index: []
method mismatch: 0
memo refs count: {1: 5108, 0: 693}
memo ref equals applied: {True: 5108, None: 693}
Empty DataFrame
Columns: [payment_id, received_date, amt, amt_inv, memo, invoice_id, customer_name, payer_name]
Index: []
apply lag by method:
         count      mean       std  min  25%  50%   75%   max
method                                                       
ach     1723.0  4.663958  4.849442  1.0  2.0  3.0   6.0  19.0
card    3242.0  0.000000  0.000000  0.0  0.0  0.0   0.0   0.0
check    183.0  8.103825  5.164879  4.0  5.0  6.0  10.0  23.0
wire     653.0  6.924962  5.171198  3.0  4.0  5.0   9.0  21.0
invoice paid_date == applied_date: 1.0  paid_date==received: 0.5588691604895708
status
paid    5801
Name: count, dtype: int64
applied after 2026-10-31: 0 received after: 0
max dates 2026-10-31 2026-10-30 2026-10-28
                               count       sum
status         payment_method                 
open           ach                42  338439.0
               check               6  225072.0
               wire               15  233876.0
overdue        ach                24  316978.0
               check               1   41568.0
               wire               13  258244.0
payment_failed card               16   16455.0
customer_id disagree 0
issue_date disagree 0
due_date disagree 0
status disagree 0
amount disagree 0
open in invoices not in ar: 0 ar not open in invoices: 0
dpd disagree 61
   invoice_id due_date_inv days_past_due  dpd_calc       bucket
52  INV-25932   2026-11-01             0        -1  Not yet due
53  INV-25933   2026-11-01             0        -1  Not yet due
54  INV-25935   2026-11-01             0        -1  Not yet due
55  INV-25937   2026-11-02             0        -2  Not yet due
56  INV-25941   2026-11-03             0        -3  Not yet due
57  INV-25943   2026-11-03             0        -3  Not yet due
58  INV-25944   2026-11-03             0        -3  Not yet due
59  INV-25945   2026-11-03             0        -3  Not y
… [result truncated, 27924 chars total]
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/explore.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD = sys.argv[1]\nr = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv'); cus=r('customers/customers.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float); ar['amt']=ar.amount.astype(float)\n# payer name drift classes\np=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amt','issue_date','due_date','status','paid_date','payment_method']],on='invoice_id',suffixes=('','_inv'))\ndef cls(a,b):\n    if a==b: return 'exact'\n    if a==b.upper(): return 'uppercase'\n    if b.lower().startswith(a.lower()): return 'truncated'\n    if a.lower() in b.lower(): return 'substring'\n    return 'other'\np['ncls']=[cls(a,b) for a,b in zip(p.payer_name,p.customer_name)]\nprint(p.ncls.value_counts()); print(p[p.ncls=='other'][['payer_name','customer_name']].drop_duplicates().head(30).to_string())\nprint(pd.crosstab(p.ncls,p.method))\n# amount diffs\np['diff']=(p.amt-p.amt_inv).round(2)\nprint('amount diff distribution:'); print(p['diff'].value_counts().head(25))\nprint(p[p['diff']!=0][['payment_id','received_date','amt','amt_inv','diff','method','memo','invoice_id']].head(40).to_string())\n# method mismatch\nprint('method mismatch:', (p.method!=p.payment_method).sum())\n# memo referencing invoice id vs applied\ndef memo_inv(m):\n    x=re.findall(r'(?:INV-?|inv|Invoice )\\s?(\\d{5})',m); return ['INV-'+i for i in x]\np['memo_inv']=p.memo.map(memo_inv)\np['memo_n']=p.memo_inv.map(len)\np['memo_ok']=[ (i in l) if l else None for i,l in zip(p.invoice_id,p.memo_inv)]\nprint('memo refs count:', p.memo_n.value_counts().to_dict()); print('memo ref equals applied:', p.memo_ok.value_counts(dropna=False).to_dict())\nprint(p[p.memo_ok==False][['payment_id','received_date','amt','amt_inv','memo','invoice_id','customer_name','payer_name']].head(30).to_string())\n# lag\np['lag']=(pd.to_datetime(p.applied_date)-pd.to_datetime(p.received_date)).dt.days\nprint('apply lag by method:'); print(p.groupby('method').lag.describe())\np['pd_vs_applied']=(p.paid_date==p.applied_date)\nprint('invoice paid_date == applied_date:', p.pd_vs_applied.mean(), ' paid_date==received:', (p.paid_date==p.received_date).mean())\n# statuses of invoices that have payments\nprint(p.status.value_counts())\n# recent applied after as-of?\nprint('applied after 2026-10-31:', (p.applied_date>'2026-10-31').sum(), 'received after:', (pay.received_date>'2026-10-31').sum())\nprint('max dates', pay.received_date.max(), pay.applied_date.max(), inv.issue_date.max())\n# open invoices\nop=inv[inv.status.isin(['open','overdue','payment_failed'])]\nprint(op.groupby(['status','payment_method']).amt.agg(['count','sum']))\nm=ar.merge(inv,on='invoice_id',suffixes=('_ar','_inv'))\nfor c in ['customer_id','issue_date','due_date','status']:\n    print(c,'disagree', (m[c+'_ar']!=m[c+'_inv']).sum())\nprint('amount disagree', (m.amt_ar!=m.amt_inv).sum())\nprint('open in invoices not in ar:', len(set(op.invoice_id)-set(ar.invoice_id)), 'ar not open in invoices:', len(set(ar.invoice_id)-set(op.invoice_id)))\n# days past due recompute\nasof=pd.Timestamp('2026-10-31')\nm['dpd_calc']=(asof-pd.to_datetime(m.due_date_inv)).dt.days\nprint('dpd disagree', (m.dpd_calc!=m.days_past_due.astype(int)).sum()); print(m[m.dpd_calc!=m.days_past_due.astype(int)][['invoice_id','due_date_inv','days_past_due','dpd_calc','bucket']].head(20).to_string())\ndef bk(d): return 'Not yet due' if d<=0 else '1-30 days' if d<=30 else '31-60 days' if d<=60 else '61-90 days' if d<=90 else 'Over 90 days'\nm['bk_calc']=m.dpd_calc.map(bk); print('bucket disagree', (m.bk_calc!=m.bucket).sum()); print(m[m.bk_calc!=m.bucket][['invoice_id','due_date_inv','days_past_due','dpd_calc','bucket','bk_calc','status_ar']].to_string())\n# status vs due\nprint(pd.crosstab(m.status_ar,m.bk_calc))\nprint(ar.groupby('bucket').amt.agg(['count','sum'])); print('total', ar.amt.sum())\n# due date = issue +30 check\ninv['dd']=(pd.to_datetime(inv.due_date)-pd.to_datetime(inv.issue_date)).dt.days\nprint(pd.crosstab(inv.dd, inv.payment_method))\nprint(pd.crosstab(inv.dd, inv.issue_date>='2026-03-16'))\n# written off\nwo=inv[inv.status=='written_off']; print('written off', len(wo), wo.amt.sum()); print(wo.groupby([wo.payment_method, wo.issue_date.str[:4]]).amt.agg(['count','sum']))\nprint(wo[wo.paid_date!=''].head())\n# pay after write-off? payments against written off\nprint('payments to written_off invoices', (p.status=='written_off').sum())\n# unapplied\nun=pay[pay.invoice_id=='']\nfor _,u in un.iterrows():\n    print('\\nUNAPPLIED',u.payment_id,u.received_date,u.amt,u.method,u.payer_name,'|',u.memo)\n    key=u.payer_name.lower().split()[0].strip(',')\n    c=cus[cus.name.str.lower().str.contains(re.escape(key))]\n    print(c[['customer_id','name','payment_method','current_arr','billing_frequency']].to_string())\n    print(inv[inv.customer_id.isin(c.customer_id)&(inv.issue_date>='2026-01-01')][['invoice_id','customer_id','issue_date','due_date','amt','status','paid_date','payment_method']].to_string())\n"
}
```
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/explore.py\" \"$R/data\" 2>&1",
 "description": "Explore payment matching, AR agreement, unapplied receipts"
}
```

### Claude · 2026-11-20 17:16:23 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; cat docs/templates/collections.md | head -40; cat docs/board_update_2026_q3.md; cat docs/process_maps.md | sed -n 1,40p; grep -n -i \"dana\" docs/*.md | head",
 "description": "Read collections templates, board update, process maps"
}
```

### Tool · 2026-11-20 17:16:23 UTC
**Tool result:**
```
# Collections reminders

The templates Finance uses today, copied from the template library as they are.

## Courtesy reminder, 5 days before due

*Marisol (finance), Jan 2024, fine as is*

**Subject:** Ledgerline invoice {{invoice_number}} due {{due_date}}

Hi {{first_name}},

A quick heads-up that invoice {{invoice_number}} for {{amount}} is due on {{due_date}}.

If {{company}} pays by card on file, there's nothing you need to do. We'll charge it on the due date. If you pay by bank transfer, our remittance details are on the invoice and under Settings > Billing.

If anything looks off, like the seat count, plan or billing contact, just reply here before the due date and we'll fix it rather than have you pay the wrong amount.

Thanks,
Ledgerline Billing
billing@ledgerline.com

---

## First reminder, 7 days past due

*Copied from old AR tool defaults, 2021, never rewritten*

**Subject:** Overdue: invoice {{invoice_number}}

Dear {{first_name}},

Our records indicate that invoice {{invoice_number}} in the amount of {{amount}}, which was due on {{due_date}}, remains outstanding.

We kindly request that payment be remitted at your earliest convenience. Payment may be made by card or bank transfer via the link on the invoice.

Should payment have already been sent, please disregard this notice and accept our thanks. If there is a query regarding the invoice, please contact the Billing team at billing@ledgerline.com.

Regards,
Accounts Receivable
# Board update: third quarter 2026

Prepared by Alan Brandt and Maya Lindqvist. Figures are at 30 September 2026 unless stated.

## Summary

Growth stayed slow and the business stayed at break-even. ARR ended the quarter at $8,465,928. New business was $157,308 against churn of $129,504. Collections worsened again and are now the main risk to cash. Support response times are slipping as volume grows with a flat team.

## Numbers

| | Q3 2026 |
|---|---|
| ARR at quarter end | $8,465,928 |
| New ARR | $157,308 |
| Expansion ARR | $92,028 |
| Contraction and churn | $168,792 |
| New customers | 12 |
| Customers lost | 7 |
| Revenue | $2,127,257 |
| EBITDA | $113,351 |
| Cash | $2,979,195 |

## What we are worried about

1. **Cash collection.** Overdue receivables have risen for three quarters. Two people handle collections part-time, and one goes on leave in March.
2. **Small-firm churn.** We keep losing the smallest customers within a year or two of signing them.
3. **Speed to lead.** We still take most of a day to ans
… [result truncated, 4009 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; cat docs/templates/collections.md | head -40; cat docs/board_update_2026_q3.md; cat docs/process_maps.md | sed -n 1,40p; grep -n -i \"dana\" docs/*.md | head",
 "description": "Read collections templates, board update, process maps"
}
```

### Claude · 2026-11-20 17:16:24 UTC
Now the main facts script.

### Claude · 2026-11-20 17:17:11 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/facts.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD = sys.argv[1]; OUT = sys.argv[2]\nr = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv'); cus=r('customers/customers.csv')\ncon=r('customers/contacts.csv'); tk=r('support/tickets.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float)\nfor c in ['issue_date','due_date','paid_date']: inv[c+'_d']=pd.to_datetime(inv[c].replace('',None))\nfor c in ['received_date','applied_date']: pay[c+'_d']=pd.to_datetime(pay[c].replace('',None))\nASOF=pd.Timestamp('2026-10-31')\ncus['arr']=cus.current_arr.astype(float)\ntop50=set(cus.sort_values('arr',ascending=False).head(50).customer_id)\nprint('top50 ARR cutoff:', cus.sort_values('arr',ascending=False).arr.iloc[49], 'ties at cutoff:', (cus.arr==cus.sort_values('arr',ascending=False).arr.iloc[49]).sum())\nprint('cents amounts in invoices:', (inv.amt%1!=0).sum(), ' in payments:', (pay.amt%1!=0).sum())\n\n# ---------- quarter-end overdue reconstruction\np=pay[pay.invoice_id!=''][['invoice_id','received_date_d','applied_date_d']]\niv=inv.merge(p,on='invoice_id',how='left')\niv['wo_d']=np.where(iv.status=='written_off',iv.paid_date_d,pd.NaT); iv['wo_d']=pd.to_datetime(iv.wo_d)\niv['settle_ledger']=iv.applied_date_d.fillna(iv.wo_d)   # ledger closes when applied or written off\niv['settle_cash']=iv.received_date_d.fillna(iv.wo_d)\nqs=['2025-06-30','2025-09-30','2025-12-31','2026-03-31','2026-06-30','2026-09-30','2026-10-31']\nrows=[]\nfor q in qs:\n    Q=pd.Timestamp(q)\n    issued=iv.issue_date_d<=Q\n    for view,col in [('ledger','settle_ledger'),('cash','settle_cash')]:\n        unpaid=issued&(iv[col].isna()|(iv[col]>Q))\n        od=unpaid&(iv.due_date_d<Q)\n        rows.append(dict(quarter_end=q,view=view,open_ar_usd=iv[unpaid].amt.sum(),overdue_n=od.sum(),overdue_usd=iv[od].amt.sum(),\n             overdue_gt30_usd=iv[od&(iv.due_date_d<Q-pd.Timedelta(days=30))].amt.sum(),\n             overdue_pct_of_open=round(100*iv[od].amt.sum()/max(iv[unpaid].amt.sum(),1),1)))\nqt=pd.DataFrame(rows); print(qt.to_string()); qt.to_csv(os.path.join(OUT,'overdue_by_quarter.csv'),index=False)\n\n# ---------- historical \"chased for money we had\" (cash received but not applied at reminder date)\nh=iv[iv.received_date_d.notna()&iv.payment_method.isin(['ach','wire','check'])].copy()\nh['recv_late']=h.received_date_d>h.due_date_d\nh['ledger_late']=h.applied_date_d>h.due_date_d\nfor k in [7,21,45]:\n    R=h.due_date_d+pd.Timedelta(days=k)\n    h[f'chased_paid_{k}']=(h.received_date_d<=R)&(h.applied_date_d>R)\nprint('bank invoices paid:',len(h),'ontime cash but ledger late:',((~h.recv_late)&h.ledger_late).sum(), h[(~h.recv_late)&h.ledger_late].amt.sum())\nfor k in [7,21,45]:\n    s=h[h[f'chased_paid_{k}']]; print(f'reminder +{k}: would have chased already-received cash: n={len(s)} usd={s.amt.sum()}')\nanyc=h[h.chased_paid_7|h.chased_paid_21|h.chased_paid_45]\nprint('any reminder on received cash: n',len(anyc),'usd',anyc.amt.sum(), 'last 12m n', (anyc.due_date_d>=ASOF-pd.Timedelta(days=365)).sum(), anyc[anyc.due_date_d>=ASOF-pd.Timedelta(days=365)].amt.sum())\n# lag by year\nh['lag']=(h.applied_date_d-h.received_date_d).dt.days\nprint(h.groupby([h.received_date_d.dt.year,'payment_method']).lag.mean().unstack().round(1))\n\n# ---------- open AR detail with flags\nop=inv[inv.status.isin(['open','overdue','payment_failed'])].copy()\nop['dpd']=(ASOF-op.due_date_d).dt.days\nop['top50']=op.customer_id.isin(top50)\nop['arr']=op.customer_id.map(dict(zip(cus.customer_id,cus.arr)))\nop['account_manager']=op.customer_id.map(dict(zip(cus.customer_id,cus.account_manager)))\n# unapplied receipts matching\nun=pay[pay.invoice_id==''].copy()\ncusname=dict(zip(cus.customer_id,cus.name))\ndef norm(s): return re.sub(r'[^a-z0-9]','',s.lower())\ndef memo_inv(m): return ['INV-'+i for i in re.findall(r'(?:INV-?|inv|Invoice )\\s?(\\d{5})',m)]\nmrows=[]\nfor _,u in un.iterrows():\n    cands=cus[cus.name.map(norm)==norm(u.payer_name)].customer_id.tolist()\n    if not cands: cands=cus[cus.name.map(norm).str.startswith(norm(u.payer_name))].customer_id.tolist()\n    oi=op[op.customer_id.isin(cands)&(op.issue_date_d<=u.received_date_d)]\n    exact=oi[(oi.amt-u.amt).abs()<0.005]\n    mi=memo_inv(u.memo)\n    if mi and mi[0] in set(op.invoice_id): match=mi; how='memo invoice ref + amount + payer'\n    elif len(exact)==1: match=exact.invoice_id.tolist(); how='payer name + unique exact amount'\n    elif len(exact)>1: match=exact.sort_values('due_date').invoice_id.tolist(); how='payer name + exact amount, AMBIGUOUS (several open invoices same amount)'\n    else: match=[]; how='no match'\n    for m in match:\n        o=op[op.invoice_id==m].iloc[0]\n        mrows.append(dict(payment_id=u.payment_id,received_date=u.received_date,amount=u.amt,method=u.method,payer_name=u.payer_name,memo=u.memo,\n            candidate_invoice=m,customer_id=o.customer_id,customer_name=o.customer_name,inv_status=o.status,due_date=o.due_date,dpd=o.dpd,inv_amount=o.amt,top50=o.top50,how=how,n_candidates=len(match)))\num=pd.DataFrame(mrows); print(um.to_string()); um.to_csv(os.path.join(OUT,'unapplied_matches.csv'),index=False)\nop['unapplied_cash_pid']=op.invoice_id.map(um.groupby('candidate_invoice').payment_id.first())\n\n# ---------- tickets\ntk['created_d']=pd.to_datetime(tk.created_at)\ntk['open']=tk.status.isin(['open','pending'])\ntk['recent']=tk.created_d>=ASOF-pd.Timedelta(days=30)\ntxt=(tk.subject+' '+tk.body).str.lower()\ntk['kw_dispute']=txt.str.contains(r'disput|overcharg|wrong amount|incorrect|charged twice|double charg|refund|credit note|not right|doesn.t match|discrepan')\ntk['kw_rewrite']=txt.str.contains(r'
… [tool input truncated]
```

### Claude · 2026-11-20 17:17:14 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; mkdir -p \"$R/analysis/work\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/facts.py\" \"$R/data\" \"$R/analysis/work\" 2>&1",
 "description": "Compute evidence numbers"
}
```

### Tool · 2026-11-20 17:17:14 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/facts.py (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:17:16 UTC
**Tool result:**
```
/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/facts.py:85: UserWarning: This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.
  tk['kw_rewrite']=txt.str.contains(r'prorat|rounding|cent|credit note|new version|time zone|timezone|billing engine|since march|retr(y|ies)')
/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/facts.py:88: UserWarning: This pattern is interpreted as a regular expression, and has match groups. To actually get the groups, use str.extract.
  tk['kw_card']=txt.str.contains(r'card (was )?declin|card fail|failed payment|payment failed|expired card|update (our|the) card|new card')
top50 ARR cutoff: 43680.0 ties at cutoff: 2
cents amounts in invoices: 0  in payments: 0
   quarter_end    view  open_ar_usd  overdue_n  overdue_usd  overdue_gt30_usd  overdue_pct_of_open
0   2025-06-30  ledger     730943.0         36     148593.0           30292.0                 20.3
1   2025-06-30    cash     647375.0         31      85425.0           18868.0                 13.2
2   2025-09-30  ledger    1149477.0         48     487889.0          113766.0                 42.4
3   2025-09-30    cash    1085986.0         44     431213.0          109866.0                 39.7
4   2025-12-31  ledger     788365.0         40     220990.0           97313.0                 28.0
5   2025-12-31    cash     674908.0         35     147750.0           83449.0                 21.9
6   2026-03-31  ledger     992099.0         41     493659.0          263637.0                 49.8
7   2026-03-31    cash     759277.0         35     283577.0          126131.0                 37.3
8   2026-06-30  ledger     790726.0         38     209262.0           53118.0                 26.5
9   2026-06-30    cash     684130.0         32     133878.0           53118.0                 19.6
10  2026-09-30  ledger    1286085.0         47     599588.0          212466.0                 46.6
11  2026-09-30    cash    1131344.0         41     528670.0          185492.0                 46.7
12  2026-10-31  ledger    1430632.0         54     633245.0          317093.0                 44.3
13  2026-10-31    cash    1430632.0         54     633245.0         
… [result truncated, 20537 chars total]
```

### Claude ·  UTC
Now the main facts script.
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/facts.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD = sys.argv[1]; OUT = sys.argv[2]\nr = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv'); cus=r('customers/customers.csv')\ncon=r('customers/contacts.csv'); tk=r('support/tickets.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float)\nfor c in ['issue_date','due_date','paid_date']: inv[c+'_d']=pd.to_datetime(inv[c].replace('',None))\nfor c in ['received_date','applied_date']: pay[c+'_d']=pd.to_datetime(pay[c].replace('',None))\nASOF=pd.Timestamp('2026-10-31')\ncus['arr']=cus.current_arr.astype(float)\ntop50=set(cus.sort_values('arr',ascending=False).head(50).customer_id)\nprint('top50 ARR cutoff:', cus.sort_values('arr',ascending=False).arr.iloc[49], 'ties at cutoff:', (cus.arr==cus.sort_values('arr',ascending=False).arr.iloc[49]).sum())\nprint('cents amounts in invoices:', (inv.amt%1!=0).sum(), ' in payments:', (pay.amt%1!=0).sum())\n\n# ---------- quarter-end overdue reconstruction\np=pay[pay.invoice_id!=''][['invoice_id','received_date_d','applied_date_d']]\niv=inv.merge(p,on='invoice_id',how='left')\niv['wo_d']=np.where(iv.status=='written_off',iv.paid_date_d,pd.NaT); iv['wo_d']=pd.to_datetime(iv.wo_d)\niv['settle_ledger']=iv.applied_date_d.fillna(iv.wo_d)   # ledger closes when applied or written off\niv['settle_cash']=iv.received_date_d.fillna(iv.wo_d)\nqs=['2025-06-30','2025-09-30','2025-12-31','2026-03-31','2026-06-30','2026-09-30','2026-10-31']\nrows=[]\nfor q in qs:\n    Q=pd.Timestamp(q)\n    issued=iv.issue_date_d<=Q\n    for view,col in [('ledger','settle_ledger'),('cash','settle_cash')]:\n        unpaid=issued&(iv[col].isna()|(iv[col]>Q))\n        od=unpaid&(iv.due_date_d<Q)\n        rows.append(dict(quarter_end=q,view=view,open_ar_usd=iv[unpaid].amt.sum(),overdue_n=od.sum(),overdue_usd=iv[od].amt.sum(),\n             overdue_gt30_usd=iv[od&(iv.due_date_d<Q-pd.Timedelta(days=30))].amt.sum(),\n             overdue_pct_of_open=round(100*iv[od].amt.sum()/max(iv[unpaid].amt.sum(),1),1)))\nqt=pd.DataFrame(rows); print(qt.to_string()); qt.to_csv(os.path.join(OUT,'overdue_by_quarter.csv'),index=False)\n\n# ---------- historical \"chased for money we had\" (cash received but not applied at reminder date)\nh=iv[iv.received_date_d.notna()&iv.payment_method.isin(['ach','wire','check'])].copy()\nh['recv_late']=h.received_date_d>h.due_date_d\nh['ledger_late']=h.applied_date_d>h.due_date_d\nfor k in [7,21,45]:\n    R=h.due_date_d+pd.Timedelta(days=k)\n    h[f'chased_paid_{k}']=(h.received_date_d<=R)&(h.applied_date_d>R)\nprint('bank invoices paid:',len(h),'ontime cash but ledger late:',((~h.recv_late)&h.ledger_late).sum(), h[(~h.recv_late)&h.ledger_late].amt.sum())\nfor k in [7,21,45]:\n    s=h[h[f'chased_paid_{k}']]; print(f'reminder +{k}: would have chased already-received cash: n={len(s)} usd={s.amt.sum()}')\nanyc=h[h.chased_paid_7|h.chased_paid_21|h.chased_paid_45]\nprint('any reminder on received cash: n',len(anyc),'usd',anyc.amt.sum(), 'last 12m n', (anyc.due_date_d>=ASOF-pd.Timedelta(days=365)).sum(), anyc[anyc.due_date_d>=ASOF-pd.Timedelta(days=365)].amt.sum())\n# lag by year\nh['lag']=(h.applied_date_d-h.received_date_d).dt.days\nprint(h.groupby([h.received_date_d.dt.year,'payment_method']).lag.mean().unstack().round(1))\n\n# ---------- open AR detail with flags\nop=inv[inv.status.isin(['open','overdue','payment_failed'])].copy()\nop['dpd']=(ASOF-op.due_date_d).dt.days\nop['top50']=op.customer_id.isin(top50)\nop['arr']=op.customer_id.map(dict(zip(cus.customer_id,cus.arr)))\nop['account_manager']=op.customer_id.map(dict(zip(cus.customer_id,cus.account_manager)))\n# unapplied receipts matching\nun=pay[pay.invoice_id==''].copy()\ncusname=dict(zip(cus.customer_id,cus.name))\ndef norm(s): return re.sub(r'[^a-z0-9]','',s.lower())\ndef memo_inv(m): return ['INV-'+i for i in re.findall(r'(?:INV-?|inv|Invoice )\\s?(\\d{5})',m)]\nmrows=[]\nfor _,u in un.iterrows():\n    cands=cus[cus.name.map(norm)==norm(u.payer_name)].customer_id.tolist()\n    if not cands: cands=cus[cus.name.map(norm).str.startswith(norm(u.payer_name))].customer_id.tolist()\n    oi=op[op.customer_id.isin(cands)&(op.issue_date_d<=u.received_date_d)]\n    exact=oi[(oi.amt-u.amt).abs()<0.005]\n    mi=memo_inv(u.memo)\n    if mi and mi[0] in set(op.invoice_id): match=mi; how='memo invoice ref + amount + payer'\n    elif len(exact)==1: match=exact.invoice_id.tolist(); how='payer name + unique exact amount'\n    elif len(exact)>1: match=exact.sort_values('due_date').invoice_id.tolist(); how='payer name + exact amount, AMBIGUOUS (several open invoices same amount)'\n    else: match=[]; how='no match'\n    for m in match:\n        o=op[op.invoice_id==m].iloc[0]\n        mrows.append(dict(payment_id=u.payment_id,received_date=u.received_date,amount=u.amt,method=u.method,payer_name=u.payer_name,memo=u.memo,\n            candidate_invoice=m,customer_id=o.customer_id,customer_name=o.customer_name,inv_status=o.status,due_date=o.due_date,dpd=o.dpd,inv_amount=o.amt,top50=o.top50,how=how,n_candidates=len(match)))\num=pd.DataFrame(mrows); print(um.to_string()); um.to_csv(os.path.join(OUT,'unapplied_matches.csv'),index=False)\nop['unapplied_cash_pid']=op.invoice_id.map(um.groupby('candidate_invoice').payment_id.first())\n\n# ---------- tickets\ntk['created_d']=pd.to_datetime(tk.created_at)\ntk['open']=tk.status.isin(['open','pending'])\ntk['recent']=tk.created_d>=ASOF-pd.Timedelta(days=30)\ntxt=(tk.subject+' '+tk.body).str.lower()\ntk['kw_dispute']=txt.str.contains(r'disput|overcharg|wrong amount|incorrect|charged twice|double charg|refund|credit note|not right|doesn.t match|discrepan')\ntk['kw_rewrite']=txt.str.contains(r'
… [tool input truncated]
```
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; mkdir -p \"$R/analysis/work\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/facts.py\" \"$R/data\" \"$R/analysis/work\" 2>&1",
 "description": "Compute evidence numbers"
}
```

### Claude · 2026-11-20 17:17:36 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/scripts/tk_read.py\" <<'EOF'\nimport sys, pandas as pd\ntk=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False)\nids=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else None\nt=tk[tk.ticket_id.isin(ids)] if ids else tk\nfor _,x in t.iterrows():\n    print(f\"--- {x.ticket_id} {x.created_at} {x.customer_id} {x.customer_name} | cat={x.category} pri={x.priority} st={x.status} | {x.subject}\\n{x.body[:500]}\")\nEOF\n\"$R/.venv/bin/python\" -I \"$R/analysis/scripts/tk_read.py\" \"$R/data/support/tickets.csv\" T880829,T880886,T880180,T880739,T881011,T880816,T880831,T880949,T881016,T880453,T880856,T880946,T880643,T881021,T880849,T880989,T880184,T880813,T880944,T880871",
 "description": "Read tickets for overdue customers"
}
```

### Tool · 2026-11-20 17:17:38 UTC
**Tool result:**
```
--- T880180 2026-07-20 16:10 C1264 Westbrook Engineering Group | cat=Billing pri=high st=pending | need advice
Hi team,

We would like to raise a data integrity concern. During internal review we identified invoices where the aggregate of the itemised charges and the presented invoice total differ by the smallest currency unit. Kindly confirm whether this is a known issue and whether historical invoices are affected.
--- T880184 2026-07-20 20:13 C1469 Kingsway Engineering Group | cat= pri=normal st=pending | Can you check something for me
Hi there - The amount the client sees in the portal is 1,950.00 AUD but the PDF they downloaded says 1,949.99. Which one is right? They want to pay today.

Signe
--- T880453 2026-08-21 09:05 C1266 Thackeray Accounting | cat=How-to pri=normal st=pending | URGENT
Is there a 'remember this device' option so I don't have to put in a code every single time I log in from my office desktop?
--- T880643 2026-09-12 14:46 C1022 Studio Marsh | cat= pri=normal st=pending | Support
Morning,

my colleague noticed the invoice email says due the 14th, i definitely typed 15th. retyped it, saved, same thing in the email preview

Rhys
--- T880739 2026-09-22 16:25 C1264 Westbrook Engineering Group | cat=Billing pri=normal st=pending | Implementation fee was meant to be waived
Hi team,

Hi again, so on our call back in March your sales rep was really clear that the implementation fee would be waived since we were signing for two years. I even have it in my notes from that call! But INV-25730 has the full fee sitting right there as its own line. Our finance team has put the whole thing on hold until a corrected version comes through, so the sooner the better honestly.

Leo
--- T880813 2026-10-01 09:31 C1379 Ruiz & Whitfield CPAs | cat= pri=high st=solved | Feedback
Hi there - Can you update the trading name on our invoices only? Legal name stays the same, but clients know us by the shorter name and it's causing confusion in their AP systems.
--- T880816 2026-10-01 12:41 C1154 Okafor & Nakamura LLP | cat=Billing pri=high st=solved | Second office discount missing
Hi,

Your account manager offered us 50% off for three months if we moved our second office onto Ledgerline. We did that in good faith. There's no sign of it on INV-25765. We'll settle once the discount shows up.
--- T880829 2026-10-02 22:27 C1273 Jessop & Orwell Agency | cat=Account change pri=normal st=solved | ASAP please
Small request: our company name has an ampersand that shows u
… [result truncated, 6144 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/scripts/tk_read.py\" <<'EOF'\nimport sys, pandas as pd\ntk=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False)\nids=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else None\nt=tk[tk.ticket_id.isin(ids)] if ids else tk\nfor _,x in t.iterrows():\n    print(f\"--- {x.ticket_id} {x.created_at} {x.customer_id} {x.customer_name} | cat={x.category} pri={x.priority} st={x.status} | {x.subject}\\n{x.body[:500]}\")\nEOF\n\"$R/.venv/bin/python\" -I \"$R/analysis/scripts/tk_read.py\" \"$R/data/support/tickets.csv\" T880829,T880886,T880180,T880739,T881011,T880816,T880831,T880949,T881016,T880453,T880856,T880946,T880643,T881021,T880849,T880989,T880184,T880813,T880944,T880871",
 "description": "Read tickets for overdue customers"
}
```

### Claude · 2026-11-20 17:17:57 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/scripts/disputes.py\" <<'EOF'\nimport sys, os, re, pandas as pd\nD=sys.argv[1]; OUT=sys.argv[2]\ntk=pd.read_csv(os.path.join(D,'support/tickets.csv'),dtype=str,keep_default_na=False)\ninv=pd.read_csv(os.path.join(D,'finance/invoices.csv'),dtype=str,keep_default_na=False)\ntxt=(tk.subject+' '+tk.body)\ntk['inv_refs']=txt.str.findall(r'INV-\\d{5}').map(lambda l:','.join(sorted(set(l))))\nref=tk[tk.inv_refs!=''].assign(invoice_id=lambda d:d.inv_refs.str.split(',')).explode('invoice_id')\nref=ref.merge(inv[['invoice_id','customer_id','amount','status','due_date','payment_method']],on='invoice_id',how='left',suffixes=('','_inv'))\nprint('tickets referencing invoice ids:', (tk.inv_refs!='').sum(), 'refs', len(ref))\nprint('ref customer mismatch:', (ref.customer_id!=ref.customer_id_inv).sum(), 'unknown inv', ref.status.isna().sum())\nprint(ref.status.value_counts())\ncols=['ticket_id','created_at','customer_id','customer_name','category','priority','status','invoice_id','status_inv','amount','due_date','subject']\nref=ref.rename(columns={'status_inv':'x'}) if 'status_inv' in ref else ref\nref.columns=[c if c!='status' or i<list(ref.columns).index('invoice_id') else 'status_inv' for i,c in enumerate(ref.columns)]\nprint(ref[cols].sort_values('status_inv').to_string())\nref[cols+['body']].to_csv(os.path.join(OUT,'tickets_invoice_refs.csv'),index=False)\nlow=txt.str.lower()\nthemes={'rounding_cent':r'smallest currency|1,949|\\.99|rounding|rounded|a cent|one cent|penny|cents|off by',\n 'proration':r'prorat|partial month|mid-?cycle|days in',\n 'due_date_tz':r'due the|due date|time zone|timezone|says due|due on the',\n 'card_retry':r'retr(?:y|ies|ied)|declin|card fail|failed payment|payment failed',\n 'credit_note_version':r'credit note|new version|reissued|two versions|duplicate (?:invoice|charge)|charged twice|double',\n 'settings_moved':r'billing > preferences|preferences|settings > billing|can.t find the setting|moved'}\nfor k,v in themes.items(): tk[k]=low.str.contains(v)\ntk['month']=tk.created_at.str[:7]\nprint(tk.groupby('month')[list(themes)].sum())\nprint(pd.crosstab(tk.category,tk[list(themes)].any(axis=1)))\nfor k in themes:\n    s=tk[tk[k]]\n    print(f'\\n## {k} n={len(s)}')\n    for _,x in s.head(6).iterrows(): print(' ',x.ticket_id,x.customer_id,x.category,x.status,'|',x.body[:160].replace('\\n',' '))\ntk[['ticket_id','created_at','customer_id','customer_name','category','priority','status','inv_refs']+list(themes)].to_csv(os.path.join(OUT,'tickets_themes.csv'),index=False)\nEOF\n\"$R/.venv/bin/python\" -I \"$R/analysis/scripts/disputes.py\" \"$R/data\" \"$R/analysis/work\" 2>&1",
 "description": "Find disputes via ticket invoice references and rewrite themes"
}
```

### Tool · 2026-11-20 17:17:59 UTC
**Tool result:**
```
Exit code 1
tickets referencing invoice ids: 14 refs 14
ref customer mismatch: 0 unknown inv 0
status
solved     11
pending     3
Name: count, dtype: int64
Traceback (most recent call last):
  File "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/disputes.py", line 15, in <module>
    print(ref[cols].sort_values('status_inv').to_string())
  File "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/.venv/lib/python3.9/site-packages/pandas/core/frame.py", line 4119, in __getitem__
    indexer = self.columns._get_indexer_strict(key, "columns")[1]
  File "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/.venv/lib/python3.9/site-packages/pandas/core/indexes/base.py", line 6212, in _get_indexer_strict
    self._raise_if_missing(keyarr, indexer, axis_name)
  File "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/.venv/lib/python3.9/site-packages/pandas/core/indexes/base.py", line 6264, in _raise_if_missing
    raise KeyError(f"{not_found} not in index")
KeyError: "['status_inv'] not in index"
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/scripts/disputes.py\" <<'EOF'\nimport sys, os, re, pandas as pd\nD=sys.argv[1]; OUT=sys.argv[2]\ntk=pd.read_csv(os.path.join(D,'support/tickets.csv'),dtype=str,keep_default_na=False)\ninv=pd.read_csv(os.path.join(D,'finance/invoices.csv'),dtype=str,keep_default_na=False)\ntxt=(tk.subject+' '+tk.body)\ntk['inv_refs']=txt.str.findall(r'INV-\\d{5}').map(lambda l:','.join(sorted(set(l))))\nref=tk[tk.inv_refs!=''].assign(invoice_id=lambda d:d.inv_refs.str.split(',')).explode('invoice_id')\nref=ref.merge(inv[['invoice_id','customer_id','amount','status','due_date','payment_method']],on='invoice_id',how='left',suffixes=('','_inv'))\nprint('tickets referencing invoice ids:', (tk.inv_refs!='').sum(), 'refs', len(ref))\nprint('ref customer mismatch:', (ref.customer_id!=ref.customer_id_inv).sum(), 'unknown inv', ref.status.isna().sum())\nprint(ref.status.value_counts())\ncols=['ticket_id','created_at','customer_id','customer_name','category','priority','status','invoice_id','status_inv','amount','due_date','subject']\nref=ref.rename(columns={'status_inv':'x'}) if 'status_inv' in ref else ref\nref.columns=[c if c!='status' or i<list(ref.columns).index('invoice_id') else 'status_inv' for i,c in enumerate(ref.columns)]\nprint(ref[cols].sort_values('status_inv').to_string())\nref[cols+['body']].to_csv(os.path.join(OUT,'tickets_invoice_refs.csv'),index=False)\nlow=txt.str.lower()\nthemes={'rounding_cent':r'smallest currency|1,949|\\.99|rounding|rounded|a cent|one cent|penny|cents|off by',\n 'proration':r'prorat|partial month|mid-?cycle|days in',\n 'due_date_tz':r'due the|due date|time zone|timezone|says due|due on the',\n 'card_retry':r'retr(?:y|ies|ied)|declin|card fail|failed payment|payment failed',\n 'credit_note_version':r'credit note|new version|reissued|two versions|duplicate (?:invoice|charge)|charged twice|double',\n 'settings_moved':r'billing > preferences|preferences|settings > billing|can.t find the setting|moved'}\nfor k,v in themes.items(): tk[k]=low.str.contains(v)\ntk['month']=tk.created_at.str[:7]\nprint(tk.groupby('month')[list(themes)].sum())\nprint(pd.crosstab(tk.category,tk[list(themes)].any(axis=1)))\nfor k in themes:\n    s=tk[tk[k]]\n    print(f'\\n## {k} n={len(s)}')\n    for _,x in s.head(6).iterrows(): print(' ',x.ticket_id,x.customer_id,x.category,x.status,'|',x.body[:160].replace('\\n',' '))\ntk[['ticket_id','created_at','customer_id','customer_name','category','priority','status','inv_refs']+list(themes)].to_csv(os.path.join(OUT,'tickets_themes.csv'),index=False)\nEOF\n\"$R/.venv/bin/python\" -I \"$R/analysis/scripts/disputes.py\" \"$R/data\" \"$R/analysis/work\" 2>&1",
 "description": "Find disputes via ticket invoice references and rewrite themes"
}
```

### Claude · 2026-11-20 17:18:06 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; F=\"$R/analysis/scripts/disputes.py\"; \"$R/.venv/bin/python\" -I - \"$F\" <<'EOF'\nimport sys\np=sys.argv[1]; s=open(p).read()\ns=s.replace(\"ref=ref.merge(inv[['invoice_id','customer_id','amount','status','due_date','payment_method']],on='invoice_id',how='left',suffixes=('','_inv'))\",\n\"ref=ref.merge(inv[['invoice_id','customer_id','amount','status','due_date','payment_method']].rename(columns={'status':'status_inv','customer_id':'customer_id_inv'}),on='invoice_id',how='left')\")\ns=s.replace(\"print(ref.status.value_counts())\",\"print(ref.status_inv.value_counts())\")\ns=s.replace(\"ref=ref.rename(columns={'status_inv':'x'}) if 'status_inv' in ref else ref\\n\",\"\")\ns=s.replace(\"ref.columns=[c if c!='status' or i<list(ref.columns).index('invoice_id') else 'status_inv' for i,c in enumerate(ref.columns)]\\n\",\"\")\nopen(p,'w').write(s)\nEOF\n\"$R/.venv/bin/python\" -I \"$F\" \"$R/data\" \"$R/analysis/work\" 2>&1",
 "description": "Fix column naming and rerun dispute script"
}
```

### Tool · 2026-11-20 17:18:08 UTC
**Tool result:**
```
tickets referencing invoice ids: 14 refs 14
ref customer mismatch: 0 unknown inv 0
status_inv
overdue    14
Name: count, dtype: int64
   ticket_id        created_at customer_id                customer_name        category priority   status invoice_id status_inv    amount    due_date                                        subject
0    T880432  2026-08-19 09:34       C1439    Banerjee Petrov Engineers                   normal   solved  INV-25539    overdue   2652.00  2026-07-31             Client portal cancellation ignored
1    T880582  2026-09-07 15:42       C1254        Upton & Bell Advisory         Billing   normal   solved  INV-25662    overdue  44064.00  2026-08-26                   Late fee should not be there
2    T880648  2026-09-13 12:39       C1030        Mercer & Banerjee LLP         Billing   normal   solved  INV-25718    overdue   3876.00  2026-09-11          Still being charged for time tracking
3    T880667  2026-09-14 16:22       C1100    Oyelaran Devlin Engineers         Billing   normal   solved  INV-25711    overdue   2820.00  2026-09-09                                  Migration fee
4    T880738  2026-09-22 15:05       C1152            Ellery Consulting         Billing      low   solved  INV-25757    overdue  13056.00  2026-09-20                    Sales tax using old address
5    T880739  2026-09-22 16:25       C1264  Westbrook Engineering Group         Billing   normal  pending  INV-25730    overdue  47904.00  2026-09-13      Implementation fee was meant to be waived
6    T880757  2026-09-24 15:46       C1261       Wexler & Hume Advisory          How-to      low   solved  INV-25712    overdue   4080.00  2026-09-09                            Seat count is wrong
7    T880816  2026-10-01 12:41       C1154        Okafor & Nakamura LLP         Billing     high   solved  INV-25765    overdue  46848.00  2026-09-22                 Second office discount missing
8    T880849  2026-10-06 14:48       C1045          Castell Engineering         Billing   normal   solved  INV-25764    overdue   6324.00  2026-09-22                charged pro after we downgraded
9    T880856  2026-10-07 14:42       C1266         Thackeray Accounting         Billing   normal   solved  INV-25750    overdue   7896.00  2026-09-17                          VAT added incorrectly
10   T880886  2026-10-12 12:57       C1073           Riverside Partners         Billing   normal   solved  INV-25787    overdue  60576.00  2026-09-26     Users double counted after workspace merge
11
… [result truncated, 10171 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; F=\"$R/analysis/scripts/disputes.py\"; \"$R/.venv/bin/python\" -I - \"$F\" <<'EOF'\nimport sys\np=sys.argv[1]; s=open(p).read()\ns=s.replace(\"ref=ref.merge(inv[['invoice_id','customer_id','amount','status','due_date','payment_method']],on='invoice_id',how='left',suffixes=('','_inv'))\",\n\"ref=ref.merge(inv[['invoice_id','customer_id','amount','status','due_date','payment_method']].rename(columns={'status':'status_inv','customer_id':'customer_id_inv'}),on='invoice_id',how='left')\")\ns=s.replace(\"print(ref.status.value_counts())\",\"print(ref.status_inv.value_counts())\")\ns=s.replace(\"ref=ref.rename(columns={'status_inv':'x'}) if 'status_inv' in ref else ref\\n\",\"\")\ns=s.replace(\"ref.columns=[c if c!='status' or i<list(ref.columns).index('invoice_id') else 'status_inv' for i,c in enumerate(ref.columns)]\\n\",\"\")\nopen(p,'w').write(s)\nEOF\n\"$R/.venv/bin/python\" -I \"$F\" \"$R/data\" \"$R/analysis/work\" 2>&1",
 "description": "Fix column naming and rerun dispute script"
}
```

### Claude · 2026-11-20 17:18:21 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/tk_read.py\" \"$R/data/support/tickets.csv\" T880432,T880582,T880648,T880667,T880738,T880757,T880957,T881024,T881039 | cut -c1-400",
 "description": "Read remaining dispute tickets"
}
```

### Tool · 2026-11-20 17:18:23 UTC
**Tool result:**
```
--- T880432 2026-08-19 09:34 C1439 Banerjee Petrov Engineers | cat= pri=normal st=solved | Client portal cancellation ignored
We switched off the client portal in August because, frankly, our clients weren't logging into it. Your team confirmed the cancellation by email. INV-25539 not only still charges the monthly portal fee, it seems to have the setup line on it again?? Two partners signed off on dropping this module and neither of them is going to sign off on paying for it. Please correct and resend.
--- T880582 2026-09-07 15:42 C1254 Upton & Bell Advisory | cat=Billing pri=normal st=solved | Late fee should not be there
The card charge failed last month because of an outage on your payment side, not ours. Your support agent told us at the time the late fee would be waived. It's on INV-25662 anyway. I'm not authorising payment while that fee is included.

Noah
--- T880648 2026-09-13 12:39 C1030 Mercer & Banerjee LLP | cat=Billing pri=normal st=solved | Still being charged for time tracking
We cancelled the time tracking module at the end of last quarter. The cancellation confirmation is literally sitting in our admin settings. Yet here it is again on INV-25718. This is the second time I've had to chase something like this. Remove it. We are not paying for a module we switched off months ago.

Caleb
--- T880667 2026-09-14 16:22 C1100 Oyelaran Devlin Engineers | cat=Billing pri=normal st=solved | Migration fee
Data migration fee on INV-25711 was waived in writing. Remove it and resend.
--- T880738 2026-09-22 15:05 C1152 Ellery Consulting | cat=Billing pri=low st=solved | Sales tax using old address
Morning,

We moved offices in January and updated the billing address in the portal the same week. The sales tax on INV-25757 is still calculated for our old location, which is a higher rate. Payment is on hold until the tax is recalculated for the correct address.
--- T880757 2026-09-24 15:46 C1261 Wexler & Hume Advisory | cat=How-to pri=low st=solved | Seat count is wrong
INV-25712 bills us for 24 users. We have 17. Reissue it with the right number and we'll pay, not before.
--- T880957 2026-10-21 15:13 C1409 Wexler Media | cat=Account change pri=normal st=pending | Renewal discount not reflected
Hi there - As agreed at renewal, our annual plan includes a 15% multi-year discount. Invoice INV-25811 reflects list pricing with no reduction applied. Kindly issue a revised invoice. We are unable to process payment against the current document.
--- T881024 2026-10-
… [result truncated, 3245 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/tk_read.py\" \"$R/data/support/tickets.csv\" T880432,T880582,T880648,T880667,T880738,T880757,T880957,T881024,T881039 | cut -c1-400",
 "description": "Read remaining dispute tickets"
}
```

### Claude · 2026-11-20 17:19:04 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/testset.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD=sys.argv[1]; OUT=sys.argv[2]\nr=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); cus=r('customers/customers.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float)\nnorm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())\ncus['n']=cus.name.map(norm)\ndef cand_customers(payer):\n    n=norm(payer); ex=cus[cus.n==n].customer_id.tolist()\n    return ex if ex else cus[cus.n.str.startswith(n)].customer_id.tolist()\nmemo_inv=lambda m: ['INV-'+i for i in re.findall(r'(?:INV-?|inv|Invoice )\\s?(\\d{5})',m)]\n# settlement date of each invoice in ledger (applied date or write-off date)\nap=pay[pay.invoice_id!=''].set_index('invoice_id').applied_date\ninv['settle']=inv.invoice_id.map(ap)\ninv.loc[inv.status=='written_off','settle']=inv.paid_date\ninv['settle']=inv.settle.replace('', '9999-12-31').fillna('9999-12-31')\nbyc={c:g for c,g in inv.groupby('customer_id')}\nrows=[]\nfor _,p in pay.iterrows():\n    cc=cand_customers(p.payer_name)\n    openinv=pd.concat([byc[c] for c in cc]) if cc else inv.iloc[:0]\n    openinv=openinv[(openinv.issue_date<=p.received_date)&(openinv.settle>=p.received_date)]\n    same_amt=openinv[(openinv.amt-p.amt).abs()<0.005]\n    refs=memo_inv(p.memo)\n    exact_name=bool(cus.n.eq(norm(p.payer_name)).any())\n    reasons=[]\n    if p.method=='card': diff='trivial'; reasons.append('Stripe charge memo carries invoice id')\n    elif refs: diff='easy'; reasons.append('memo references invoice number')\n    else:\n        reasons.append('no invoice ref in memo')\n        if not exact_name: reasons.append(f'payer name drift ({len(cc)} candidate customers)')\n        if len(same_amt)==1 and len(cc)==1: diff='medium'; reasons.append('unique open invoice with exact amount')\n        elif len(same_amt)==1: diff='hard'; reasons.append('amount unique across candidate customers')\n        elif len(same_amt)>1: diff='hard'; reasons.append(f'{len(same_amt)} open invoices with same amount')\n        else: diff='hard'; reasons.append('no open invoice with exact amount at receipt (check data)')\n        if p.payer_name==p.payer_name.upper() and p.payer_name!=p.payer_name.title(): reasons.append('uppercase payer name')\n    rows.append(dict(payment_id=p.payment_id,received_date=p.received_date,amount=p.amount,method=p.method,payer_name=p.payer_name,memo=p.memo,\n        true_invoice_ids=p.invoice_id,n_candidate_customers=len(cc),n_open_same_amount=len(same_amt),difficulty=diff,difficulty_reason='; '.join(reasons)))\nt=pd.DataFrame(rows)\nprint(pd.crosstab(t.difficulty,t.method)); print(t[t.method!='card'].groupby('difficulty').n_open_same_amount.value_counts())\nhist=t[t.true_invoice_ids!=''].copy(); hist['label_source']='ledger_applied (payments.invoice_id, confirmed by staff)'\n# unapplied: inferred labels\ninferred={'PAY-65750':('INV-25784','inferred: payer name exact + unique exact amount among open invoices','medium'),\n 'PAY-65766':('INV-25806','inferred: uppercase payer name + unique exact amount; memo generic','medium'),\n 'PAY-65796':('INV-25951','inferred: uppercase payer + unique exact amount (implementation fee, not yet due); blank memo','medium'),\n 'PAY-65805':('INV-25469|INV-25852','inferred AMBIGUOUS: two overdue invoices of 5100.00; oldest-first convention says INV-25469; either is acceptable','hard'),\n 'PAY-65806':('INV-25845','inferred: memo invoice ref + exact amount + payer','easy'),\n 'PAY-65807':('INV-25937','inferred: memo \"Invoice 25937\" + exact amount + payer','easy'),\n 'PAY-65808':('INV-25867','inferred: memo \"inv25867\" + exact amount; note INV-26000 same amount also open','easy')}\nun=t[t.true_invoice_ids==''].copy()\nun['true_invoice_ids']=un.payment_id.map(lambda x:inferred[x][0]); un['label_source']=un.payment_id.map(lambda x:inferred[x][1]); un['difficulty']=un.payment_id.map(lambda x:inferred[x][2])\n# sample: all bank hard + stratified others\nrng=np.random.RandomState(7)\nbank=hist[hist.method!='card']\nhard=bank[bank.difficulty=='hard']\nmed=bank[bank.difficulty=='medium'].sample(min(80,(bank.difficulty=='medium').sum()),random_state=7)\neasy=bank[bank.difficulty=='easy'].sample(60,random_state=7)\ncard=hist[hist.method=='card'].sample(20,random_state=7)\nreal=pd.concat([un,hard,med,easy,card]); real['is_synthetic']=False\n# synthetic perturbations of real bank payments (for traps absent in the data)\nbase=bank[bank.received_date>='2026-03-16'].sample(40,random_state=11)\nsyn=[]\nfor i,(_,b) in enumerate(base.iterrows()):\n    kind=['bank_fee','cent_rounding','short_pay','combined'][i%4]\n    s=b.to_dict(); s['payment_id']=f'SYN-{i+1:03d}'; s['is_synthetic']=True; a=float(b.amount)\n    if kind=='bank_fee': fee=[15,25,35][i%3]; s['amount']=f'{a-fee:.2f}'; s['difficulty']='hard'; s['difficulty_reason']=f'synthetic: wire/intl bank fee ${fee} deducted from {b.amount}'\n    elif kind=='cent_rounding': d=[0.01,-0.01,0.02][i%3]; s['amount']=f'{a+d:.2f}'; s['difficulty']='medium'; s['difficulty_reason']=f'synthetic: per-line rounding diff {d:+.2f} (post-rewrite pattern)'\n    elif kind=='short_pay': s['amount']=f'{a*0.9:.2f}'; s['difficulty']='hard'; s['difficulty_reason']='synthetic: 10% short payment (disputed line withheld); should match but flag partial'\n    else:\n        other=inv[(inv.customer_id==inv.loc[inv.invoice_id==b.true_invoice_ids,'customer_id'].iloc[0])&(inv.invoice_id!=b.true_invoice_ids)&(inv.issue_date<=b.received_date)].sort_values('issue_date').tail(1)\n        if len(other)==0: continue\n        s['amount']=f'{a+other.amt.iloc[0]:.2f}'; s['true_invoice_ids']=b.true_invoice_ids+'|'+other.invoice_id.iloc[0]; s['difficulty']='hard'; s['difficulty_reason']='sy
… [tool input truncated]
```

### Claude · 2026-11-20 17:19:07 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/testset.py\" \"$R/data\" \"$R/analysis\" 2>&1 | tail -60",
 "description": "Build labelled cash-application test set"
}
```

### Tool · 2026-11-20 17:19:07 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/testset.py (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:19:11 UTC
**Tool result:**
```
method       ach  card  check  wire
difficulty                         
easy        1260     0    132   477
hard          71     0      0     9
medium       397     0     51   169
trivial        0  3242      0     0
difficulty  n_open_same_amount
easy        1                     1647
            2                      179
            3                       41
            4                        2
hard        2                       59
            1                       12
            3                        9
medium      1                      617
Name: count, dtype: int64
286
is_synthetic  False  True 
difficulty                
easy             63      0
hard             80     30
medium           83     10
trivial          20      0
label_source
ledger_applied            239
synthetic_perturbation     40
inferred:                   6
inferred                    1
Name: count, dtype: int64
difficulty_reason
no invoice ref in memo; 2 open invoices with same amount                                                                            48
no invoice ref in memo; 2 open invoices with same amount; uppercase payer name                                                       9
no invoice ref in memo; 3 open invoices with same amount                                                                             7
no invoice ref in memo; payer name drift (6 candidate customers); amount unique across candidate customers; uppercase payer name     3
no invoice ref in memo; payer name drift (4 candidate customers); amount unique across candidate customers; uppercase payer name     3
no invoice ref in memo; payer name drift (8 candidate customers); amount unique across candidate customers; uppercase payer name     2
no invoice ref in memo; payer name drift (7 candidate customers); amount unique across candidate customers; uppercase payer name     1
no invoice ref in memo; payer name drift (5 candidate customers); 2 open invoices with same amount; uppercase payer name             1
no invoice ref in memo; payer name drift (9 candidate customers); amount unique across candidate customers; uppercase payer name     1
no invoice ref in memo; payer name drift (5 candidate customers); amount unique across candidate customers; uppercase payer name     1
no invoice ref in memo; 3 open invoices with same amount; uppercase payer name                                                       1
no invoice ref in memo; payer name drift (5 candidate customers); 3 open invoices with 
… [result truncated, 2790 chars total]
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/testset.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD=sys.argv[1]; OUT=sys.argv[2]\nr=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); cus=r('customers/customers.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float)\nnorm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())\ncus['n']=cus.name.map(norm)\ndef cand_customers(payer):\n    n=norm(payer); ex=cus[cus.n==n].customer_id.tolist()\n    return ex if ex else cus[cus.n.str.startswith(n)].customer_id.tolist()\nmemo_inv=lambda m: ['INV-'+i for i in re.findall(r'(?:INV-?|inv|Invoice )\\s?(\\d{5})',m)]\n# settlement date of each invoice in ledger (applied date or write-off date)\nap=pay[pay.invoice_id!=''].set_index('invoice_id').applied_date\ninv['settle']=inv.invoice_id.map(ap)\ninv.loc[inv.status=='written_off','settle']=inv.paid_date\ninv['settle']=inv.settle.replace('', '9999-12-31').fillna('9999-12-31')\nbyc={c:g for c,g in inv.groupby('customer_id')}\nrows=[]\nfor _,p in pay.iterrows():\n    cc=cand_customers(p.payer_name)\n    openinv=pd.concat([byc[c] for c in cc]) if cc else inv.iloc[:0]\n    openinv=openinv[(openinv.issue_date<=p.received_date)&(openinv.settle>=p.received_date)]\n    same_amt=openinv[(openinv.amt-p.amt).abs()<0.005]\n    refs=memo_inv(p.memo)\n    exact_name=bool(cus.n.eq(norm(p.payer_name)).any())\n    reasons=[]\n    if p.method=='card': diff='trivial'; reasons.append('Stripe charge memo carries invoice id')\n    elif refs: diff='easy'; reasons.append('memo references invoice number')\n    else:\n        reasons.append('no invoice ref in memo')\n        if not exact_name: reasons.append(f'payer name drift ({len(cc)} candidate customers)')\n        if len(same_amt)==1 and len(cc)==1: diff='medium'; reasons.append('unique open invoice with exact amount')\n        elif len(same_amt)==1: diff='hard'; reasons.append('amount unique across candidate customers')\n        elif len(same_amt)>1: diff='hard'; reasons.append(f'{len(same_amt)} open invoices with same amount')\n        else: diff='hard'; reasons.append('no open invoice with exact amount at receipt (check data)')\n        if p.payer_name==p.payer_name.upper() and p.payer_name!=p.payer_name.title(): reasons.append('uppercase payer name')\n    rows.append(dict(payment_id=p.payment_id,received_date=p.received_date,amount=p.amount,method=p.method,payer_name=p.payer_name,memo=p.memo,\n        true_invoice_ids=p.invoice_id,n_candidate_customers=len(cc),n_open_same_amount=len(same_amt),difficulty=diff,difficulty_reason='; '.join(reasons)))\nt=pd.DataFrame(rows)\nprint(pd.crosstab(t.difficulty,t.method)); print(t[t.method!='card'].groupby('difficulty').n_open_same_amount.value_counts())\nhist=t[t.true_invoice_ids!=''].copy(); hist['label_source']='ledger_applied (payments.invoice_id, confirmed by staff)'\n# unapplied: inferred labels\ninferred={'PAY-65750':('INV-25784','inferred: payer name exact + unique exact amount among open invoices','medium'),\n 'PAY-65766':('INV-25806','inferred: uppercase payer name + unique exact amount; memo generic','medium'),\n 'PAY-65796':('INV-25951','inferred: uppercase payer + unique exact amount (implementation fee, not yet due); blank memo','medium'),\n 'PAY-65805':('INV-25469|INV-25852','inferred AMBIGUOUS: two overdue invoices of 5100.00; oldest-first convention says INV-25469; either is acceptable','hard'),\n 'PAY-65806':('INV-25845','inferred: memo invoice ref + exact amount + payer','easy'),\n 'PAY-65807':('INV-25937','inferred: memo \"Invoice 25937\" + exact amount + payer','easy'),\n 'PAY-65808':('INV-25867','inferred: memo \"inv25867\" + exact amount; note INV-26000 same amount also open','easy')}\nun=t[t.true_invoice_ids==''].copy()\nun['true_invoice_ids']=un.payment_id.map(lambda x:inferred[x][0]); un['label_source']=un.payment_id.map(lambda x:inferred[x][1]); un['difficulty']=un.payment_id.map(lambda x:inferred[x][2])\n# sample: all bank hard + stratified others\nrng=np.random.RandomState(7)\nbank=hist[hist.method!='card']\nhard=bank[bank.difficulty=='hard']\nmed=bank[bank.difficulty=='medium'].sample(min(80,(bank.difficulty=='medium').sum()),random_state=7)\neasy=bank[bank.difficulty=='easy'].sample(60,random_state=7)\ncard=hist[hist.method=='card'].sample(20,random_state=7)\nreal=pd.concat([un,hard,med,easy,card]); real['is_synthetic']=False\n# synthetic perturbations of real bank payments (for traps absent in the data)\nbase=bank[bank.received_date>='2026-03-16'].sample(40,random_state=11)\nsyn=[]\nfor i,(_,b) in enumerate(base.iterrows()):\n    kind=['bank_fee','cent_rounding','short_pay','combined'][i%4]\n    s=b.to_dict(); s['payment_id']=f'SYN-{i+1:03d}'; s['is_synthetic']=True; a=float(b.amount)\n    if kind=='bank_fee': fee=[15,25,35][i%3]; s['amount']=f'{a-fee:.2f}'; s['difficulty']='hard'; s['difficulty_reason']=f'synthetic: wire/intl bank fee ${fee} deducted from {b.amount}'\n    elif kind=='cent_rounding': d=[0.01,-0.01,0.02][i%3]; s['amount']=f'{a+d:.2f}'; s['difficulty']='medium'; s['difficulty_reason']=f'synthetic: per-line rounding diff {d:+.2f} (post-rewrite pattern)'\n    elif kind=='short_pay': s['amount']=f'{a*0.9:.2f}'; s['difficulty']='hard'; s['difficulty_reason']='synthetic: 10% short payment (disputed line withheld); should match but flag partial'\n    else:\n        other=inv[(inv.customer_id==inv.loc[inv.invoice_id==b.true_invoice_ids,'customer_id'].iloc[0])&(inv.invoice_id!=b.true_invoice_ids)&(inv.issue_date<=b.received_date)].sort_values('issue_date').tail(1)\n        if len(other)==0: continue\n        s['amount']=f'{a+other.amt.iloc[0]:.2f}'; s['true_invoice_ids']=b.true_invoice_ids+'|'+other.invoice_id.iloc[0]; s['difficulty']='hard'; s['difficulty_reason']='sy
… [tool input truncated]
```
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/testset.py\" \"$R/data\" \"$R/analysis\" 2>&1 | tail -60",
 "description": "Build labelled cash-application test set"
}
```

### Claude · 2026-11-20 17:19:28 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/scripts/extra.py\" <<'EOF'\nimport sys, os, pandas as pd, numpy as np\nA=sys.argv[1]; D=sys.argv[2]\nts=pd.read_csv(os.path.join(A,'testset_cash_app.csv'),dtype=str,keep_default_na=False)\ninv=pd.read_csv(os.path.join(D,'finance/invoices.csv'),dtype=str,keep_default_na=False); inv['amt']=inv.amount.astype(float)\npay=pd.read_csv(os.path.join(D,'finance/payments.csv'),dtype=str,keep_default_na=False)\nref=pd.read_csv(os.path.join(A,'work/tickets_invoice_refs.csv'),dtype=str)\nprint('disputed invoices', ref.invoice_id.nunique(), 'usd', ref.amount.astype(float).sum(), 'ticket status', ref.status.value_counts().to_dict(), 'category', ref.category.fillna('(blank)').value_counts().to_dict())\nop=pd.read_csv(os.path.join(A,'work/open_ar_flags.csv'),dtype=str,keep_default_na=False)\nd=op[op.invoice_id.isin(ref.invoice_id)]; print('disputed top50', d[d.top50=='True'][['invoice_id','customer_name','amount']].to_string())\n# ambiguous historical: did staff apply to oldest?\namb=ts[(ts.label_source.str.startswith('ledger'))&(ts.n_open_same_amount.astype(int)>1)]\niss=dict(zip(inv.invoice_id,inv.issue_date)); cust=dict(zip(inv.invoice_id,inv.customer_id))\nres=[]\nfor _,a in amb.iterrows():\n    c=cust[a.true_invoice_ids]; o=inv[(inv.customer_id==c)&(abs(inv.amt-float(a.amount))<.005)&(inv.issue_date<=a.received_date)]\n    pa=pay[pay.invoice_id.isin(o.invoice_id)].set_index('invoice_id').applied_date\n    o=o[o.invoice_id.map(pa).fillna('9999')>=a.received_date]\n    res.append(iss[a.true_invoice_ids]==o.issue_date.min())\nprint('ambiguous: applied to oldest open', sum(res),'of',len(res))\n# monthly overdue (ledger) for seasonality\np=pay[pay.invoice_id!=''].set_index('invoice_id').applied_date\ninv['settle']=inv.invoice_id.map(p); inv.loc[inv.status=='written_off','settle']=inv.paid_date; inv['settle']=inv.settle.fillna('9999')\nout=[]\nfor m in pd.date_range('2025-01-31','2026-10-31',freq='M'):\n    q=m.strftime('%Y-%m-%d'); od=inv[(inv.issue_date<=q)&(inv.due_date<q)&(inv.settle>q)]\n    out.append((q,len(od),od.amt.sum()))\nprint(pd.DataFrame(out,columns=['month_end','n','usd']).to_string())\n# what drives quarter-end spikes: annual invoices issued in quarter's last-60 days\nEOF\n\"$R/.venv/bin/python\" -I \"$R/analysis/scripts/extra.py\" \"$R/analysis\" \"$R/data\"",
 "description": "Compute dispute totals, oldest-first rate, monthly overdue"
}
```

### Tool · 2026-11-20 17:19:30 UTC
**Tool result:**
```
/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/extra.py:24: FutureWarning: 'M' is deprecated and will be removed in a future version, please use 'ME' instead.
  for m in pd.date_range('2025-01-31','2026-10-31',freq='M'):
disputed invoices 14 usd 309000.0 ticket status {'solved': 11, 'pending': 3} category {'Billing': 10, 'How-to': 2, '(blank)': 1, 'Account change': 1}
disputed top50    invoice_id                customer_name    amount
5   INV-25662        Upton & Bell Advisory  44064.00
11  INV-25730  Westbrook Engineering Group  47904.00
15  INV-25765        Okafor & Nakamura LLP  46848.00
18  INV-25787           Riverside Partners  60576.00
ambiguous: applied to oldest open 68 of 75
     month_end   n       usd
0   2025-01-31  37  258209.0
1   2025-02-28  53  384975.0
2   2025-03-31  51  423380.0
3   2025-04-30  43  225141.0
4   2025-05-31  38  196601.0
5   2025-06-30  36  148593.0
6   2025-07-31  37  261306.0
7   2025-08-31  43  401091.0
8   2025-09-30  48  487889.0
9   2025-10-31  57  597353.0
10  2025-11-30  49  364302.0
11  2025-12-31  40  220990.0
12  2026-01-31  43  295114.0
13  2026-02-28  54  472159.0
14  2026-03-31  41  493659.0
15  2026-04-30  49  315892.0
16  2026-05-31  51  253196.0
17  2026-06-30  38  209262.0
18  2026-07-31  44  435815.0
19  2026-08-31  61  613725.0
20  2026-09-30  47  599588.0
21  2026-10-31  54  633245.0
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/scripts/extra.py\" <<'EOF'\nimport sys, os, pandas as pd, numpy as np\nA=sys.argv[1]; D=sys.argv[2]\nts=pd.read_csv(os.path.join(A,'testset_cash_app.csv'),dtype=str,keep_default_na=False)\ninv=pd.read_csv(os.path.join(D,'finance/invoices.csv'),dtype=str,keep_default_na=False); inv['amt']=inv.amount.astype(float)\npay=pd.read_csv(os.path.join(D,'finance/payments.csv'),dtype=str,keep_default_na=False)\nref=pd.read_csv(os.path.join(A,'work/tickets_invoice_refs.csv'),dtype=str)\nprint('disputed invoices', ref.invoice_id.nunique(), 'usd', ref.amount.astype(float).sum(), 'ticket status', ref.status.value_counts().to_dict(), 'category', ref.category.fillna('(blank)').value_counts().to_dict())\nop=pd.read_csv(os.path.join(A,'work/open_ar_flags.csv'),dtype=str,keep_default_na=False)\nd=op[op.invoice_id.isin(ref.invoice_id)]; print('disputed top50', d[d.top50=='True'][['invoice_id','customer_name','amount']].to_string())\n# ambiguous historical: did staff apply to oldest?\namb=ts[(ts.label_source.str.startswith('ledger'))&(ts.n_open_same_amount.astype(int)>1)]\niss=dict(zip(inv.invoice_id,inv.issue_date)); cust=dict(zip(inv.invoice_id,inv.customer_id))\nres=[]\nfor _,a in amb.iterrows():\n    c=cust[a.true_invoice_ids]; o=inv[(inv.customer_id==c)&(abs(inv.amt-float(a.amount))<.005)&(inv.issue_date<=a.received_date)]\n    pa=pay[pay.invoice_id.isin(o.invoice_id)].set_index('invoice_id').applied_date\n    o=o[o.invoice_id.map(pa).fillna('9999')>=a.received_date]\n    res.append(iss[a.true_invoice_ids]==o.issue_date.min())\nprint('ambiguous: applied to oldest open', sum(res),'of',len(res))\n# monthly overdue (ledger) for seasonality\np=pay[pay.invoice_id!=''].set_index('invoice_id').applied_date\ninv['settle']=inv.invoice_id.map(p); inv.loc[inv.status=='written_off','settle']=inv.paid_date; inv['settle']=inv.settle.fillna('9999')\nout=[]\nfor m in pd.date_range('2025-01-31','2026-10-31',freq='M'):\n    q=m.strftime('%Y-%m-%d'); od=inv[(inv.issue_date<=q)&(inv.due_date<q)&(inv.settle>q)]\n    out.append((q,len(od),od.amt.sum()))\nprint(pd.DataFrame(out,columns=['month_end','n','usd']).to_string())\n# what drives quarter-end spikes: annual invoices issued in quarter's last-60 days\nEOF\n\"$R/.venv/bin/python\" -I \"$R/analysis/scripts/extra.py\" \"$R/analysis\" \"$R/data\"",
 "description": "Compute dispute totals, oldest-first rate, monthly overdue"
}
```

### Claude · 2026-11-20 17:20:12 UTC
Now writing SCHEMA.md.

### Claude · 2026-11-20 17:20:47 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/SCHEMA.md",
 "content": "# SCHEMA — Ledgerline O2C data room (as of 2026-10-31)\n\nGenerated by `analysis/scripts/schema.py` and `analysis/scripts/joins.py` (read as strings, `keep_default_na=False`; blanks = empty string).\nEvery row count matches the README listing exactly.\n\n| file | rows | README | grain / PK |\n|---|---|---|---|\n| finance/invoices.csv | 6,062 | 6,062 | invoice_id (unique) |\n| finance/payments.csv | 5,808 | 5,808 | payment_id (unique) |\n| finance/ar_aging.csv | 117 | 117 | invoice_id (unique) |\n| customers/customers.csv | 508 | 508 | customer_id (unique) |\n| customers/contacts.csv | 967 | 967 | contact_id (unique) |\n| customers/contracts.csv | 1,757 | 1,757 | customer_id + term_start |\n| support/tickets.csv | 1,041 | 1,041 | ticket_id (unique), 2026-07-01..2026-10-31 |\n| support/nps_responses.csv | 820 | 820 | response_id |\n| product/usage_monthly.csv | 6,955 | 6,955 | month + customer_id (2025-05..2026-10) |\n| sales/opportunities.csv | 2,176 | 2,176 | opportunity_id |\n\n## finance/invoices.csv\n`invoice_id str, customer_id str, customer_name str, type cat, issue_date date, due_date date, service_period_months int, amount float(2dp), currency str, status cat, paid_date date|blank, payment_method cat`\nExample: `INV-20001, C1194, Stanhope Engineering, subscription, 2022-01-03, 2022-02-02, 12, 5400.00, USD, paid, 2022-02-03, check`\n- type: subscription 5,938 / implementation 124\n- status: paid 5,801 / written_off 144 / open 63 / overdue 38 / payment_failed 16\n- payment_method: card 3,402 / ach 1,789 / wire 681 / check 190\n- service_period_months: 1 (3,784) / 3 (1,188) / 12 (1,090); currency all USD\n- Traps: `paid_date` is ALSO filled for `written_off` rows (it is the write-off date, always issue+150d). Card invoices have due_date = issue_date (3,384 of 3,402); bank methods are issue+30. All amounts are whole dollars (0 rows with cents). History starts 2022 (contract terms in force at 1 Jan 2023). `paid_date` = date cash was *applied* in the ledger, not received.\n\n## finance/payments.csv\n`payment_id str, received_date date, amount float, method cat, payer_name str, memo str|blank, applied_date date|blank, invoice_id str|blank`\nExample: `PAY-60001, 2022-01-12, 405.00, card, Corbin Design Partnership, Stripe charge INV-20013, 2022-01-12, INV-20013`\n- method: card 3,242 / ach 1,728 / wire 655 / check 183\n- invoice_id blank = unapplied: 7 rows (also applied_date blank). Each applied invoice_id appears once (no split/combined receipts).\n- memo templates: `Stripe charge INV-#####` 3,242 (all card) / `INV-#####` 999 / `Invoice #####` 571 / `Ledgerline subscription` 333 / blank 102 / `inv##### <Surname>` ~300 / `<Surname> payment` ~200\n- payer_name: 845 distinct; 80.0% exactly equal a customers.name.\n\n## finance/ar_aging.csv (QuickBooks export)\n`invoice_id, customer_id, customer_name, plan cat, issue_date, due_date, amount float, days_past_due int (floored at 0), bucket cat, status cat`\nExample: `INV-25433, C1029, Northgate Creative, Core, 2026-06-04, 2026-06-04, 799.00, 149, Over 90 days, payment_failed`\n- bucket: Not yet due 63 / 1-30 days 31 / 31-60 days 13 / 61-90 days 5 / Over 90 days 5\n- status: open 63 (= not yet due) / overdue 38 / payment_failed 16 (card, all past due)\n- Equals exactly the 117 invoices with status in {open, overdue, payment_failed}; customer, dates, amount, status all agree; bucket agrees with recomputed days past due.\n\n## customers/customers.csv\n`customer_id, name, website, industry cat, country cat, employees int, plan cat, status cat, signup_date, churn_date|blank, churn_reason cat|blank, billing_frequency cat, payment_method cat, current_seats int, current_arr int, renewal_date|blank, account_manager cat, acquisition_channel cat|blank, accounting_integration cat`\nExample: `C1002, Quill + Ingram Architects, quillingramarchitects.example, Architecture practice, United States, 75, Growth, active, 2019-01-09, , , annual, ach, 19, 15504, 2027-01-09, Maria Yardley, , none`\n- status: active 396 / churned 112; plan: Growth 285 / Core 162 / Enterprise 61\n- billing_frequency: annual 303 / monthly 104 / quarterly 101; payment_method: ach 223 / wire 129 / card 109 / check 47\n- country: US 392 / Canada 62 / UK 54; account_manager: Nadia Upton 130, Nadia Sinclair 130, Hannah Drummond 130, Maria Yardley 118\n- Top-50 by current_arr: cutoff $43,680 with 2 accounts tied at the cutoff (boundary is ambiguous).\n\n## customers/contacts.csv\n`contact_id, customer_id, first_name, last_name, email, role cat, status cat`\nExample: `P5001, C1001, Milan, Delacroix, milan.delacroix@lowellconsulting.example, Account admin and billing, active`\n- role: Billing contact 398 / Account admin 346 / Account admin and billing 162 / Executive sponsor 61\n- status: active 915 / `left the firm; still on invoice emails` 52\n- Every customer has >=1 billing-role contact and >=1 still active. Email domain = customers.website for 100% of contacts (no domain-mismatch trap here).\n\n## customers/contracts.csv\n`customer_id, term_start, term_end, plan, seats int, price_per_seat_per_month int, platform_fee int, arr int, change_type cat, prior_arr int|blank`\nExample: `C1001, 2023-01-01, 2023-12-31, Core, 18, 45, 0, 9720, in force at 1 Jan 2023, `\n- change_type: renewal 643 / expansion 526 / in force at 1 Jan 2023 322 / new 186 / contraction 80\n- price_per_seat: 45/47 (Core), 65/68 (Growth), 85/88 (Enterprise); platform_fee 0 or 12,000 (Enterprise)\n\n## support/tickets.csv (times US Central)\n`ticket_id, created_at datetime, customer_id, customer_name, requester_name, requester_email, channel cat, subject, body (long text), category cat|blank, priority cat, assignee, first_response_at, status cat, resolved_at|blank, csat_rating int|blank`\nExample: `T880001,
… [tool input truncated]
```

### Tool · 2026-11-20 17:20:47 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/SCHEMA.md (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
Now writing SCHEMA.md.
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/SCHEMA.md",
 "content": "# SCHEMA — Ledgerline O2C data room (as of 2026-10-31)\n\nGenerated by `analysis/scripts/schema.py` and `analysis/scripts/joins.py` (read as strings, `keep_default_na=False`; blanks = empty string).\nEvery row count matches the README listing exactly.\n\n| file | rows | README | grain / PK |\n|---|---|---|---|\n| finance/invoices.csv | 6,062 | 6,062 | invoice_id (unique) |\n| finance/payments.csv | 5,808 | 5,808 | payment_id (unique) |\n| finance/ar_aging.csv | 117 | 117 | invoice_id (unique) |\n| customers/customers.csv | 508 | 508 | customer_id (unique) |\n| customers/contacts.csv | 967 | 967 | contact_id (unique) |\n| customers/contracts.csv | 1,757 | 1,757 | customer_id + term_start |\n| support/tickets.csv | 1,041 | 1,041 | ticket_id (unique), 2026-07-01..2026-10-31 |\n| support/nps_responses.csv | 820 | 820 | response_id |\n| product/usage_monthly.csv | 6,955 | 6,955 | month + customer_id (2025-05..2026-10) |\n| sales/opportunities.csv | 2,176 | 2,176 | opportunity_id |\n\n## finance/invoices.csv\n`invoice_id str, customer_id str, customer_name str, type cat, issue_date date, due_date date, service_period_months int, amount float(2dp), currency str, status cat, paid_date date|blank, payment_method cat`\nExample: `INV-20001, C1194, Stanhope Engineering, subscription, 2022-01-03, 2022-02-02, 12, 5400.00, USD, paid, 2022-02-03, check`\n- type: subscription 5,938 / implementation 124\n- status: paid 5,801 / written_off 144 / open 63 / overdue 38 / payment_failed 16\n- payment_method: card 3,402 / ach 1,789 / wire 681 / check 190\n- service_period_months: 1 (3,784) / 3 (1,188) / 12 (1,090); currency all USD\n- Traps: `paid_date` is ALSO filled for `written_off` rows (it is the write-off date, always issue+150d). Card invoices have due_date = issue_date (3,384 of 3,402); bank methods are issue+30. All amounts are whole dollars (0 rows with cents). History starts 2022 (contract terms in force at 1 Jan 2023). `paid_date` = date cash was *applied* in the ledger, not received.\n\n## finance/payments.csv\n`payment_id str, received_date date, amount float, method cat, payer_name str, memo str|blank, applied_date date|blank, invoice_id str|blank`\nExample: `PAY-60001, 2022-01-12, 405.00, card, Corbin Design Partnership, Stripe charge INV-20013, 2022-01-12, INV-20013`\n- method: card 3,242 / ach 1,728 / wire 655 / check 183\n- invoice_id blank = unapplied: 7 rows (also applied_date blank). Each applied invoice_id appears once (no split/combined receipts).\n- memo templates: `Stripe charge INV-#####` 3,242 (all card) / `INV-#####` 999 / `Invoice #####` 571 / `Ledgerline subscription` 333 / blank 102 / `inv##### <Surname>` ~300 / `<Surname> payment` ~200\n- payer_name: 845 distinct; 80.0% exactly equal a customers.name.\n\n## finance/ar_aging.csv (QuickBooks export)\n`invoice_id, customer_id, customer_name, plan cat, issue_date, due_date, amount float, days_past_due int (floored at 0), bucket cat, status cat`\nExample: `INV-25433, C1029, Northgate Creative, Core, 2026-06-04, 2026-06-04, 799.00, 149, Over 90 days, payment_failed`\n- bucket: Not yet due 63 / 1-30 days 31 / 31-60 days 13 / 61-90 days 5 / Over 90 days 5\n- status: open 63 (= not yet due) / overdue 38 / payment_failed 16 (card, all past due)\n- Equals exactly the 117 invoices with status in {open, overdue, payment_failed}; customer, dates, amount, status all agree; bucket agrees with recomputed days past due.\n\n## customers/customers.csv\n`customer_id, name, website, industry cat, country cat, employees int, plan cat, status cat, signup_date, churn_date|blank, churn_reason cat|blank, billing_frequency cat, payment_method cat, current_seats int, current_arr int, renewal_date|blank, account_manager cat, acquisition_channel cat|blank, accounting_integration cat`\nExample: `C1002, Quill + Ingram Architects, quillingramarchitects.example, Architecture practice, United States, 75, Growth, active, 2019-01-09, , , annual, ach, 19, 15504, 2027-01-09, Maria Yardley, , none`\n- status: active 396 / churned 112; plan: Growth 285 / Core 162 / Enterprise 61\n- billing_frequency: annual 303 / monthly 104 / quarterly 101; payment_method: ach 223 / wire 129 / card 109 / check 47\n- country: US 392 / Canada 62 / UK 54; account_manager: Nadia Upton 130, Nadia Sinclair 130, Hannah Drummond 130, Maria Yardley 118\n- Top-50 by current_arr: cutoff $43,680 with 2 accounts tied at the cutoff (boundary is ambiguous).\n\n## customers/contacts.csv\n`contact_id, customer_id, first_name, last_name, email, role cat, status cat`\nExample: `P5001, C1001, Milan, Delacroix, milan.delacroix@lowellconsulting.example, Account admin and billing, active`\n- role: Billing contact 398 / Account admin 346 / Account admin and billing 162 / Executive sponsor 61\n- status: active 915 / `left the firm; still on invoice emails` 52\n- Every customer has >=1 billing-role contact and >=1 still active. Email domain = customers.website for 100% of contacts (no domain-mismatch trap here).\n\n## customers/contracts.csv\n`customer_id, term_start, term_end, plan, seats int, price_per_seat_per_month int, platform_fee int, arr int, change_type cat, prior_arr int|blank`\nExample: `C1001, 2023-01-01, 2023-12-31, Core, 18, 45, 0, 9720, in force at 1 Jan 2023, `\n- change_type: renewal 643 / expansion 526 / in force at 1 Jan 2023 322 / new 186 / contraction 80\n- price_per_seat: 45/47 (Core), 65/68 (Growth), 85/88 (Enterprise); platform_fee 0 or 12,000 (Enterprise)\n\n## support/tickets.csv (times US Central)\n`ticket_id, created_at datetime, customer_id, customer_name, requester_name, requester_email, channel cat, subject, body (long text), category cat|blank, priority cat, assignee, first_response_at, status cat, resolved_at|blank, csat_rating int|blank`\nExample: `T880001,
… [tool input truncated]
```

### Claude · 2026-11-20 17:20:57 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -i '' 's/ (no 2025 Dec gap; 7 waves)/ (7 waves)/' \"$R/analysis/SCHEMA.md\"; \"$R/.venv/bin/python\" -I - \"$R/data\" \"$R/analysis/work\" <<'EOF'\nimport sys,os,pandas as pd\nD,W=sys.argv[1:3]\ntk=pd.read_csv(os.path.join(D,'support/tickets.csv'),dtype=str,keep_default_na=False)\nop=pd.read_csv(os.path.join(W,'open_ar_flags.csv'),dtype=str,keep_default_na=False)\nod=op[op.dpd.astype(int)>0]\nesc=tk[tk.status.isin(['open','pending'])&tk.priority.isin(['high','urgent'])]\nx=od[od.customer_id.isin(esc.customer_id)]; print('overdue w/ open high/urgent ticket', len(x), x.amount.astype(float).sum(), x[['invoice_id','customer_name','amount']].to_string())\nprint(tk[tk.ticket_id.isin(['T880184','T880180','T880739','T880829'])][['ticket_id','created_at','first_response_at','status','resolved_at','priority']].to_string())\nprint('open/pending tickets total', tk.status.isin(['open','pending']).sum())\nEOF",
 "description": "Escalation proxy and key ticket timings"
}
```

### Tool · 2026-11-20 17:20:59 UTC
**Tool result:**
```
overdue w/ open high/urgent ticket 3 90130.0    invoice_id                customer_name    amount
11  INV-25730  Westbrook Engineering Group  47904.00
25  INV-25834       Delacroix, Jessop & Co  41568.00
41  INV-25897    Ambrose & Lowell Advisory    658.00
    ticket_id        created_at first_response_at   status       resolved_at priority
179   T880180  2026-07-20 16:10  2026-07-20 16:38  pending                       high
183   T880184  2026-07-20 20:13  2026-07-21 11:08  pending                     normal
738   T880739  2026-09-22 16:25  2026-09-22 17:49  pending                     normal
828   T880829  2026-10-02 22:27  2026-10-05 08:59   solved  2026-10-06 17:13   normal
open/pending tickets total 71
[This command modified 1 file you've previously read: ../analysis/SCHEMA.md. Call Read before editing.]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -i '' 's/ (no 2025 Dec gap; 7 waves)/ (7 waves)/' \"$R/analysis/SCHEMA.md\"; \"$R/.venv/bin/python\" -I - \"$R/data\" \"$R/analysis/work\" <<'EOF'\nimport sys,os,pandas as pd\nD,W=sys.argv[1:3]\ntk=pd.read_csv(os.path.join(D,'support/tickets.csv'),dtype=str,keep_default_na=False)\nop=pd.read_csv(os.path.join(W,'open_ar_flags.csv'),dtype=str,keep_default_na=False)\nod=op[op.dpd.astype(int)>0]\nesc=tk[tk.status.isin(['open','pending'])&tk.priority.isin(['high','urgent'])]\nx=od[od.customer_id.isin(esc.customer_id)]; print('overdue w/ open high/urgent ticket', len(x), x.amount.astype(float).sum(), x[['invoice_id','customer_name','amount']].to_string())\nprint(tk[tk.ticket_id.isin(['T880184','T880180','T880739','T880829'])][['ticket_id','created_at','first_response_at','status','resolved_at','priority']].to_string())\nprint('open/pending tickets total', tk.status.isin(['open','pending']).sum())\nEOF",
 "description": "Escalation proxy and key ticket timings"
}
```

### Claude · 2026-11-20 17:21:01 UTC
Now FACTS.md.

### Claude · 2026-11-20 17:22:08 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FACTS.md",
 "content": "# FACTS — O2C evidence numbers (as of 2026-10-31)\n\nScripts are in `analysis/scripts/` (facts.py, disputes.py, extra.py, testset.py). Working CSVs are in `analysis/work/`.\n**F** = fact computed straight from the data. **I** = inference or interpretation. \"Overdue\" = due_date < 2026-10-31 and still unpaid in the ledger.\n\n## 1. AR aging\n- **F** ar_aging.csv total: **117 invoices, $1,430,632**.\n  - Not yet due: 63 / $797,387\n  - 1-30 days: 31 / $316,152\n  - 31-60 days: 13 / $259,408\n  - 61-90 days: 5 / $48,100\n  - Over 90 days: 5 / $9,585\n  - **Overdue total: 54 invoices / $633,245** (38 `overdue` bank invoices $616,790 + 16 `payment_failed` card invoices $16,455).\n- **F** ar_aging.csv matches invoices.csv exactly. Both have the same 117 ids (status in open/overdue/payment_failed), with 0 disagreements on customer, dates, amount, status or bucket. The only difference is cosmetic: `days_past_due` is floored at 0 for not-yet-due rows.\n- **F** The real disagreement is with the bank. 7 receipts worth **$87,335** have arrived but are not applied (section 3), so the aging overstates receivables by that amount, and overstates overdue by $78,348.\n- **F** Over 90 days is only $9,585 (mostly small card failures). Bank-paid overdue is young: 1-60 days holds $575,560 (91% of overdue $).\n- **I** Process doc FIN-1 says \"60 to 110 overdue at any time\". The data shows 36 to 61 overdue invoices at each month end in 2025-26, so the doc likely overstates volume.\n\n## 2. Overdue trend: testing Dana's \"risen three quarters running\"\nMethod: rebuild the ledger at each date D. An invoice counts if issue_date <= D, due_date < D, and it is not settled by D. Settled means applied_date (ledger view) or received_date (cash view), or the write-off date for written_off rows. Output: `analysis/work/overdue_by_quarter.csv`.\n\n| quarter end | overdue $ (ledger) | # | overdue $ (cash already received removed) | overdue >30d $ (ledger) |\n|---|---|---|---|---|\n| 2025-06-30 | 148,593 | 36 | 85,425 | 30,292 |\n| 2025-09-30 | 487,889 | 48 | 431,213 | 113,766 |\n| 2025-12-31 | 220,990 | 40 | 147,750 | 97,313 |\n| 2026-03-31 | 493,659 | 41 | 283,577 | 263,637 |\n| 2026-06-30 | 209,262 | 38 | 133,878 | 53,118 |\n| 2026-09-30 | 599,588 | 47 | 528,670 | 212,466 |\n| 2026-10-31 (today) | 633,245 | 54 | 554,897* | 317,093 |\n\n*Today's cash view subtracts the 5 unapplied receipts that match overdue invoices ($78,348).\n\n- **F** Quarter on quarter, the claim is **false**. Overdue goes up, down, up, down, up: 221k → 494k → 209k → 600k. It is strongly seasonal. Month-end peaks fall in Feb-Mar and Aug-Oct, which are the annual-renewal billing waves.\n- **F** Year on year, the claim is **true** for three straight quarters:\n  - Q1: 423k → 494k (+17%)\n  - Q2: 149k → 209k (+41%)\n  - Q3: 488k → 600k (+23%)\n  - October: 597k → 633k (+6%)\n- **F** Part of reported \"overdue\" at each quarter end was cash already in the bank but not yet applied: $57k (Q3'25), $73k (Q4'25), **$210k (Q1'26, 43% of reported overdue)**, $75k (Q2'26) and $71k (Q3'26).\n- **I** The board's line \"overdue rose for three quarters\" is defensible only as a year-on-year statement. A sequential chart would show a sawtooth. Cash-application lag inflates the quarter-end number.\n\n## 3. Unapplied receipts (\"chased for money we already have\")\nMethod: payments with blank invoice_id. Payer is resolved to a customer by normalised exact name (letters and digits only, lower-cased). Candidates are that customer's open, overdue or failed invoices issued on or before received_date. A match needs an exact amount, or a memo invoice ref plus amount. Tolerance matching was not needed: every match is exact. Output: `analysis/work/unapplied_matches.csv`.\n\n- **F** **7 unapplied receipts, $87,335**: ACH 5 / $75,663, wire 2 / $11,672. All 7 were received 2026-10-17..10-31, and all 7 have a plausible open invoice.\n- **F** **5 match an invoice shown OVERDUE: $78,348 across 5 customers.** 2 match invoices not yet due ($8,987).\n\n| payment | received | $ | payer_name / memo | matches | status | dpd | how |\n|---|---|---|---|---|---|---|---|\n| PAY-65750 | 10-17 | 62,688 | Jessop & Orwell Agency / \"Jessop payment\" | INV-25784 (C1273, **top-50**) | overdue | 36 | exact name + unique amount; memo surname fits 8 customers |\n| PAY-65766 | 10-19 | 6,324 | BRANDT & LOWELL CPAS / \"Ledgerline subscription\" | INV-25806 (C1126) | overdue | 28 | uppercase name + unique amount |\n| PAY-65805 | 10-29 | 5,100 | Kingsway Engineering Group / (blank) | INV-25469 **or** INV-25852 (C1469) | overdue | 111 / 19 | AMBIGUOUS: two $5,100 overdue invoices |\n| PAY-65806 | 10-30 | 3,672 | Castellano, Crane & Co / \"INV-25845\" | INV-25845 (C1188) | overdue | 20 | memo ref |\n| PAY-65808 | 10-31 | 564 | YARDLEY & DUARTE ADVISORY / \"inv25867 Yardley\" | INV-25867 (C1346) | overdue | 16 | memo ref (INV-26000 also $564, open) |\n| PAY-65796 | 10-27 | 8,000 | ACHEBE + PEMBERTON ARCHITECTS / (blank) | INV-25951 (C1505, top-50) | open | -4 | uppercase name + unique amount (implementation fee) |\n| PAY-65807 | 10-30 | 987 | Studio Zeller / \"Invoice 25937\" | INV-25937 (C1223) | open | -2 | memo ref |\n\n- **F** Jessop & Orwell's $62,688 has gone unapplied for 14 calendar days (10 working days). Policy says 3 to 5 working days. The historical maximum ACH lag is 19 days.\n- **F, historical scale.** Application lag (applied_date - received_date, calendar days) is 0 for card. For ACH the mean is 4.7 (max 19), for wire 6.9 (max 21) and for check 8.1 (max 23). It has been flat since 2022.\n  - Of 2,559 bank-paid invoices, **434 ($4.95M) were paid on time in cash but recorded late in the ledger**.\n  - If reminders had run on the policy schedule (+7/+21/+45), **572 invoices ($
… [tool input truncated]
```

### Tool · 2026-11-20 17:22:08 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FACTS.md (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
Now FACTS.md.
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/FACTS.md",
 "content": "# FACTS — O2C evidence numbers (as of 2026-10-31)\n\nScripts are in `analysis/scripts/` (facts.py, disputes.py, extra.py, testset.py). Working CSVs are in `analysis/work/`.\n**F** = fact computed straight from the data. **I** = inference or interpretation. \"Overdue\" = due_date < 2026-10-31 and still unpaid in the ledger.\n\n## 1. AR aging\n- **F** ar_aging.csv total: **117 invoices, $1,430,632**.\n  - Not yet due: 63 / $797,387\n  - 1-30 days: 31 / $316,152\n  - 31-60 days: 13 / $259,408\n  - 61-90 days: 5 / $48,100\n  - Over 90 days: 5 / $9,585\n  - **Overdue total: 54 invoices / $633,245** (38 `overdue` bank invoices $616,790 + 16 `payment_failed` card invoices $16,455).\n- **F** ar_aging.csv matches invoices.csv exactly. Both have the same 117 ids (status in open/overdue/payment_failed), with 0 disagreements on customer, dates, amount, status or bucket. The only difference is cosmetic: `days_past_due` is floored at 0 for not-yet-due rows.\n- **F** The real disagreement is with the bank. 7 receipts worth **$87,335** have arrived but are not applied (section 3), so the aging overstates receivables by that amount, and overstates overdue by $78,348.\n- **F** Over 90 days is only $9,585 (mostly small card failures). Bank-paid overdue is young: 1-60 days holds $575,560 (91% of overdue $).\n- **I** Process doc FIN-1 says \"60 to 110 overdue at any time\". The data shows 36 to 61 overdue invoices at each month end in 2025-26, so the doc likely overstates volume.\n\n## 2. Overdue trend: testing Dana's \"risen three quarters running\"\nMethod: rebuild the ledger at each date D. An invoice counts if issue_date <= D, due_date < D, and it is not settled by D. Settled means applied_date (ledger view) or received_date (cash view), or the write-off date for written_off rows. Output: `analysis/work/overdue_by_quarter.csv`.\n\n| quarter end | overdue $ (ledger) | # | overdue $ (cash already received removed) | overdue >30d $ (ledger) |\n|---|---|---|---|---|\n| 2025-06-30 | 148,593 | 36 | 85,425 | 30,292 |\n| 2025-09-30 | 487,889 | 48 | 431,213 | 113,766 |\n| 2025-12-31 | 220,990 | 40 | 147,750 | 97,313 |\n| 2026-03-31 | 493,659 | 41 | 283,577 | 263,637 |\n| 2026-06-30 | 209,262 | 38 | 133,878 | 53,118 |\n| 2026-09-30 | 599,588 | 47 | 528,670 | 212,466 |\n| 2026-10-31 (today) | 633,245 | 54 | 554,897* | 317,093 |\n\n*Today's cash view subtracts the 5 unapplied receipts that match overdue invoices ($78,348).\n\n- **F** Quarter on quarter, the claim is **false**. Overdue goes up, down, up, down, up: 221k → 494k → 209k → 600k. It is strongly seasonal. Month-end peaks fall in Feb-Mar and Aug-Oct, which are the annual-renewal billing waves.\n- **F** Year on year, the claim is **true** for three straight quarters:\n  - Q1: 423k → 494k (+17%)\n  - Q2: 149k → 209k (+41%)\n  - Q3: 488k → 600k (+23%)\n  - October: 597k → 633k (+6%)\n- **F** Part of reported \"overdue\" at each quarter end was cash already in the bank but not yet applied: $57k (Q3'25), $73k (Q4'25), **$210k (Q1'26, 43% of reported overdue)**, $75k (Q2'26) and $71k (Q3'26).\n- **I** The board's line \"overdue rose for three quarters\" is defensible only as a year-on-year statement. A sequential chart would show a sawtooth. Cash-application lag inflates the quarter-end number.\n\n## 3. Unapplied receipts (\"chased for money we already have\")\nMethod: payments with blank invoice_id. Payer is resolved to a customer by normalised exact name (letters and digits only, lower-cased). Candidates are that customer's open, overdue or failed invoices issued on or before received_date. A match needs an exact amount, or a memo invoice ref plus amount. Tolerance matching was not needed: every match is exact. Output: `analysis/work/unapplied_matches.csv`.\n\n- **F** **7 unapplied receipts, $87,335**: ACH 5 / $75,663, wire 2 / $11,672. All 7 were received 2026-10-17..10-31, and all 7 have a plausible open invoice.\n- **F** **5 match an invoice shown OVERDUE: $78,348 across 5 customers.** 2 match invoices not yet due ($8,987).\n\n| payment | received | $ | payer_name / memo | matches | status | dpd | how |\n|---|---|---|---|---|---|---|---|\n| PAY-65750 | 10-17 | 62,688 | Jessop & Orwell Agency / \"Jessop payment\" | INV-25784 (C1273, **top-50**) | overdue | 36 | exact name + unique amount; memo surname fits 8 customers |\n| PAY-65766 | 10-19 | 6,324 | BRANDT & LOWELL CPAS / \"Ledgerline subscription\" | INV-25806 (C1126) | overdue | 28 | uppercase name + unique amount |\n| PAY-65805 | 10-29 | 5,100 | Kingsway Engineering Group / (blank) | INV-25469 **or** INV-25852 (C1469) | overdue | 111 / 19 | AMBIGUOUS: two $5,100 overdue invoices |\n| PAY-65806 | 10-30 | 3,672 | Castellano, Crane & Co / \"INV-25845\" | INV-25845 (C1188) | overdue | 20 | memo ref |\n| PAY-65808 | 10-31 | 564 | YARDLEY & DUARTE ADVISORY / \"inv25867 Yardley\" | INV-25867 (C1346) | overdue | 16 | memo ref (INV-26000 also $564, open) |\n| PAY-65796 | 10-27 | 8,000 | ACHEBE + PEMBERTON ARCHITECTS / (blank) | INV-25951 (C1505, top-50) | open | -4 | uppercase name + unique amount (implementation fee) |\n| PAY-65807 | 10-30 | 987 | Studio Zeller / \"Invoice 25937\" | INV-25937 (C1223) | open | -2 | memo ref |\n\n- **F** Jessop & Orwell's $62,688 has gone unapplied for 14 calendar days (10 working days). Policy says 3 to 5 working days. The historical maximum ACH lag is 19 days.\n- **F, historical scale.** Application lag (applied_date - received_date, calendar days) is 0 for card. For ACH the mean is 4.7 (max 19), for wire 6.9 (max 21) and for check 8.1 (max 23). It has been flat since 2022.\n  - Of 2,559 bank-paid invoices, **434 ($4.95M) were paid on time in cash but recorded late in the ledger**.\n  - If reminders had run on the policy schedule (+7/+21/+45), **572 invoices ($
… [tool input truncated]
```

### Claude · 2026-11-20 17:22:15 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -i '' 's/(16 customers, all active)/(15 customers, all active; Quill, Mott \\& Co has 2)/' \"$R/analysis/FACTS.md\"; grep -n \"15 customers\" \"$R/analysis/FACTS.md\"; ls \"$R/analysis\" \"$R/analysis/work\"; wc -l \"$R/analysis/testset_cash_app.csv\"",
 "description": "Fix customer count and list outputs"
}
```

### Tool · 2026-11-20 17:22:16 UTC
**Tool result:**
```
103:- **F** Currently **16 payment_failed / $16,455** (15 customers, all active; Quill, Mott & Co has 2). For **10 of them ($9,209)** the same customer's *later* card invoices were charged successfully, so the card on file works and the failed invoice was never re-run.
/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis:
FACTS.md
SCHEMA.md
scripts
testset_cash_app.csv
work

/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/work:
open_ar_flags.csv
overdue_by_quarter.csv
tickets_flags.csv
tickets_invoice_refs.csv
tickets_themes.csv
unapplied_matches.csv
     287 /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/testset_cash_app.csv
[This command modified 1 file you've previously read: ../analysis/FACTS.md. Call Read before editing.]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -i '' 's/(16 customers, all active)/(15 customers, all active; Quill, Mott \\& Co has 2)/' \"$R/analysis/FACTS.md\"; grep -n \"15 customers\" \"$R/analysis/FACTS.md\"; ls \"$R/analysis\" \"$R/analysis/work\"; wc -l \"$R/analysis/testset_cash_app.csv\"",
 "description": "Fix customer count and list outputs"
}
```

### Claude · 2026-11-20 17:22:31 UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "All three files are written: SCHEMA.md, FACTS.md and testset_cash_app.csv. Row counts match the README, every ID join is clean (0% failures), and `data/` is untouched. The only fuzzy joins are payer name/memo to customer/invoice, and ticket text to invoice for disputes.\n\n- **AR:** $1,430,632 open across 117 invoices. Overdue is 54 invoices, $633,245 (1-30d $316k, 31-60d $259k, 61-90d $48k, 90+ $9.6k). ar_aging.csv agrees with invoices.csv on every row. The real gap is with the bank: 7 receipts worth $87,335 have arrived but are not applied.\n- **Dana's claim:** false quarter on quarter. Overdue at quarter ends was $221k, $494k, $209k, $600k, a seasonal sawtooth. It is true year on year: Q1 +17%, Q2 +41%, Q3 +23%. At 31 Mar 2026, $210k (43%) of reported overdue was cash already received but not applied.\n- **Chased for money we have:** 5 unapplied receipts ($78,348) match invoices shown overdue. On history, if reminders had followed the policy schedule, 112 invoices ($1.63M) in the last 12 months would have been chased after the cash arrived. There is no reminder log, so this is exposure, not proof.\n- **Disputes:** these show up only as ticket text citing an invoice ID. 14 overdue invoices worth $309k (49% of overdue) are disputed. 11 of those tickets are marked solved but the invoice was never corrected, and 4 aren't tagged Billing. None of the 14 mention the March rewrite, so the link to it is weak.\n- **Top-50 accounts:** 6 overdue, $305,760. 4 are disputed and 1 is already paid.\n- **Failed cards:** 16 invoices, $16,455. For 10 of them the customer's later card charges succeeded, so nobody re-ran the failed charge. Historically 144 card invoices ($159k) were auto-written-off at 150 days, and 9 of them were over $2k, above the VP Finance's approval limit.\n- **Traps the brief expected but the data doesn't have:** no bank fees, short payments, combined payments or cent differences; every amount is whole dollars. The test set (286 rows) therefore includes 40 clearly flagged synthetic rows for those cases.\n\nMost demo-worthy examples:\n1. **Jessop & Orwell Agency (C1273, top-50):** INV-25784, $62,688, 36 days overdue. They paid it on 10-17 (PAY-65750, memo \"Jessop payment\", which fits 8 Jessop customers) and it has sat unapplied for 10 working days.\n2. **Kingsway Engineering Group (C1469):** INV-25469, $5,100, 111 days overdue, plus INV-25852, $5,100, 19 days overdue. Their $5,100 payment on 10-29 (PAY-65805) is unapplied and it's unclear which invoice it covers. A ticket from them (T880184, about a 1,950.00 vs 1,949.99 rounding question) has been pending since 07-20.\n3. **Westbrook Engineering Group (C1264, top-50):** INV-25730, $47,904, 48 days overdue. Disputed because an implementation fee was meant to be waived (T880739, pending), and they have a high-priority ticket on cent rounding (T880180) open since July. Policy says do not chase. Alternates: Riverside Partners INV-25787 ($60,576, seats double-counted, ticket marked solved but invoice unchanged), and Northgate Creative INV-25433 ($799, auto write-off on 11-01 although their card works).\n\nFiles are in /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/:\n- SCHEMA.md\n- FACTS.md\n- testset_cash_app.csv\n- work/ (supporting CSVs: open_ar_flags, unapplied_matches, overdue_by_quarter, tickets_invoice_refs, tickets_themes, tickets_flags)\n- scripts/"
}
```

### Tool · 2026-11-20 17:22:31 UTC
**Tool result:**
```
{"success":true,"message":"Report delivered to your caller."}
```

### Jacek · 2026-11-20 17:40:26 UTC
The coordinator sent a message while you were working:
Follow-up (target 20 min, write analysis/DISCREPANCIES.md + one CSV per check in analysis/work/, report ≤12 lines). The finance team needs a discrepancy review before we tell Maya it's ready for Priya on Monday:
1. Verify each of the 14 disputes against contracts.csv / pricing_and_packaging.md: is the customer right? (Riverside 62 vs 38 seats; Wexler & Hume 24 vs 17 users; Westbrook implementation fee waived?; Okafor & Nakamura 50% second-office discount; Castell downgrade proration; Brandt Ashby annual→monthly; Thackeray VAT; Ellery sales tax; Wexler Media 15% multi-year; Mercer & Banerjee module cancelled; Upton & Bell late fee; Oyelaran Devlin migration fee; Banerjee Petrov portal; Reyes $51,072 — the QA agent says that one may be a false positive). For each: verdict (customer right / we're right / can't tell from data), the $ we should credit, and evidence (contract row, invoice line). This turns "held" into "here is the fix".
2. AR tie-out: ar_aging total vs balance_sheet_monthly AR at 2026-10-31 vs invoices open; explain any gap (unapplied cash, credits).
3. Overpayments / duplicate payments / credits owed to customers; payments applied to a different customer than the invoice.
4. Write-offs vs policy: card auto write-offs >$2k (VP Finance limit) and any non-card write-offs; $ and list.
5. Contract vs invoice amount mismatches on currently open invoices (seat count × price + platform fee vs invoice amount), especially since the 16 Mar 2026 billing-engine rewrite (proration/rounding).
Facts vs inferences separated. Do not edit app/ or data/.

Address this before completing your current task.

### Claude ·  UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "All three files are written: SCHEMA.md, FACTS.md and testset_cash_app.csv. Row counts match the README, every ID join is clean (0% failures), and `data/` is untouched. The only fuzzy joins are payer name/memo to customer/invoice, and ticket text to invoice for disputes.\n\n- **AR:** $1,430,632 open across 117 invoices. Overdue is 54 invoices, $633,245 (1-30d $316k, 31-60d $259k, 61-90d $48k, 90+ $9.6k). ar_aging.csv agrees with invoices.csv on every row. The real gap is with the bank: 7 receipts worth $87,335 have arrived but are not applied.\n- **Dana's claim:** false quarter on quarter. Overdue at quarter ends was $221k, $494k, $209k, $600k, a seasonal sawtooth. It is true year on year: Q1 +17%, Q2 +41%, Q3 +23%. At 31 Mar 2026, $210k (43%) of reported overdue was cash already received but not applied.\n- **Chased for money we have:** 5 unapplied receipts ($78,348) match invoices shown overdue. On history, if reminders had followed the policy schedule, 112 invoices ($1.63M) in the last 12 months would have been chased after the cash arrived. There is no reminder log, so this is exposure, not proof.\n- **Disputes:** these show up only as ticket text citing an invoice ID. 14 overdue invoices worth $309k (49% of overdue) are disputed. 11 of those tickets are marked solved but the invoice was never corrected, and 4 aren't tagged Billing. None of the 14 mention the March rewrite, so the link to it is weak.\n- **Top-50 accounts:** 6 overdue, $305,760. 4 are disputed and 1 is already paid.\n- **Failed cards:** 16 invoices, $16,455. For 10 of them the customer's later card charges succeeded, so nobody re-ran the failed charge. Historically 144 card invoices ($159k) were auto-written-off at 150 days, and 9 of them were over $2k, above the VP Finance's approval limit.\n- **Traps the brief expected but the data doesn't have:** no bank fees, short payments, combined payments or cent differences; every amount is whole dollars. The test set (286 rows) therefore includes 40 clearly flagged synthetic rows for those cases.\n\nMost demo-worthy examples:\n1. **Jessop & Orwell Agency (C1273, top-50):** INV-25784, $62,688, 36 days overdue. They paid it on 10-17 (PAY-65750, memo \"Jessop payment\", which fits 8 Jessop customers) and it has sat unapplied for 10 working days.\n2. **Kingsway Engineering Group (C1469):** INV-25469, $5,100, 111 days overdue, plus INV-25852, $5,100, 19 days overdue. Their $5,100 payment on 10-29 (PAY-65805) is unapplied and it's unclear which invoice it covers. A ticket from them (T880184, about a 1,950.00 vs 1,949.99 rounding question) has been pending since 07-20.\n3. **Westbrook Engineering Group (C1264, top-50):** INV-25730, $47,904, 48 days overdue. Disputed because an implementation fee was meant to be waived (T880739, pending), and they have a high-priority ticket on cent rounding (T880180) open since July. Policy says do not chase. Alternates: Riverside Partners INV-25787 ($60,576, seats double-counted, ticket marked solved but invoice unchanged), and Northgate Creative INV-25433 ($799, auto write-off on 11-01 although their card works).\n\nFiles are in /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/:\n- SCHEMA.md\n- FACTS.md\n- testset_cash_app.csv\n- work/ (supporting CSVs: open_ar_flags, unapplied_matches, overdue_by_quarter, tickets_invoice_refs, tickets_themes, tickets_flags)\n- scripts/"
}
```

### Claude · 2026-11-20 17:40:33 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; cat docs/pricing_and_packaging.md; head -1 finance/balance_sheet_monthly.csv; tail -3 finance/balance_sheet_monthly.csv; grep -n \"51072\\|51,072\\|Reyes\" support/tickets.csv | cut -c1-300 | head; grep -n \"51072\" finance/invoices.csv customers/contracts.csv | head",
 "description": "Read pricing doc, balance sheet tail, find Reyes"
}
```

### Tool · 2026-11-20 17:40:33 UTC
**Tool result:**
```
# Pricing and packaging (internal price list)

This is the list sales quotes from. The public pricing page on the website still shows 2024 prices and has not been updated.

| Plan | Per seat per month, from 1 Jan 2025 | Before 2025 | Annual platform fee | Minimum seats |
|---|---|---|---|---|
| Core | $47 | $45 | none | 8 |
| Growth | $68 | $65 | none | 12 |
| Enterprise | $88 | $85 | $12,000 | 20 |

- All contracts are annual and renew on the anniversary of signing. Customers choose to be billed annually, quarterly or monthly.
- Seats can be added at renewal. Reductions are allowed at renewal only.
- Implementation fee for new customers: none on Core, $2,500 on Growth, $8,000 on Enterprise.
- Existing customers moved to the 2025 prices at their first renewal after 1 January 2025.

## What each plan includes

- **Core**: invoicing, payments, client portal, one accounting integration.
- **Growth**: everything in Core, plus retainers, milestone billing, approval rules and scheduled reports.
- **Enterprise**: everything in Growth, plus multi-entity, single sign-on, API access, a named account manager and a one-hour first response commitment.

## Discounting

Account executives may discount up to 10% on a first-year contract. Anything more needs the Head of Sales. Multi-year discounts are not offered. No discount is ever promised in writing before approval.
month,cash,accounts_receivable,other_assets,total_assets,deferred_revenue,unapplied_cash_receipts,accrued_liabilities,total_liabilities,equity,cash_collected_in_month,cash_paid_out_in_month
2026-08,2961153,1260557,185000,4406710,2920827,225876,240000,3386703,1020007,873658,662941
2026-09,2979195,1286085,185000,4450280,3013123,154741,240000,3407864,1042416,702205,684163
2026-10,2992481,1430632,185000,4608113,3174463,87335,240000,3501798,1106315,668963,655677
25:T880010,2026-07-01 19:40,C1132,Holloway Strategy,Anika Reyes,anika.reyes@hollowaystrategy.example,email,Something I noticed,"Hi team,
140:T880049,2026-07-06 17:14,C1193,Nakamura Consulting,Signe Reyes,signe.reyes@nakamuraconsulting.example,email,Query regarding our setup,"I'm confused about which date counts as the change date. I made the switch late in the evening our time, which would already have been the next day in UTC. Did t
220:T880077,2026-07-09 17:15,C1314,Reyes Wexler Law,Rhys Moreau,rhys.moreau@reyeswexlerlaw.example,web form,Is this possible?,"The tax line on our invoices just says Tax. Could it say VAT (20%) instead? Clients' accounts tea
… [result truncated, 4337 chars total]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/data\"; cat docs/pricing_and_packaging.md; head -1 finance/balance_sheet_monthly.csv; tail -3 finance/balance_sheet_monthly.csv; grep -n \"51072\\|51,072\\|Reyes\" support/tickets.csv | cut -c1-300 | head; grep -n \"51072\" finance/invoices.csv customers/contracts.csv | head",
 "description": "Read pricing doc, balance sheet tail, find Reyes"
}
```

### Claude · 2026-11-20 17:40:50 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/disp_verify.py",
 "content": "import sys, os, pandas as pd\nD=sys.argv[1]\nr=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)\ninv=r('finance/invoices.csv'); ctr=r('customers/contracts.csv'); cus=r('customers/customers.csv'); us=r('product/usage_monthly.csv'); tk=r('support/tickets.csv'); con=r('customers/contacts.csv')\nids=['INV-25539','INV-25662','INV-25718','INV-25711','INV-25757','INV-25730','INV-25712','INV-25765','INV-25764','INV-25750','INV-25787','INV-25811','INV-25822','INV-25834','INV-26009']\nfor i in ids:\n    v=inv[inv.invoice_id==i].iloc[0]; c=v.customer_id\n    print('\\n=====',i,c,v.customer_name,v.type,v.issue_date,'due',v.due_date,'period',v.service_period_months,'amt',v.amount,v.status,v.payment_method)\n    cu=cus[cus.customer_id==c].iloc[0]; print('  customer:',cu.plan,cu.status,cu.billing_frequency,cu.payment_method,'seats',cu.current_seats,'arr',cu.current_arr,'renew',cu.renewal_date,'signup',cu.signup_date,'country',cu.country,'AM',cu.account_manager)\n    print(ctr[ctr.customer_id==c].tail(4).to_string(index=False))\n    print(inv[(inv.customer_id==c)&(inv.issue_date>='2025-06-01')][['invoice_id','type','issue_date','service_period_months','amount','status','paid_date']].to_string(index=False))\n    u=us[us.customer_id==c].tail(4); print(u[['month','seats_licensed','active_users','uses_retainers','uses_milestones','uses_client_portal']].to_string(index=False))\n    for _,t in tk[tk.customer_id==c].iterrows():\n        print(f'  T {t.ticket_id} {t.created_at} {t.category}/{t.status} | {t.subject} | {t.body[:200]!r}')\n"
}
```

### Claude · 2026-11-20 17:40:53 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/disp_verify.py\" \"$R/data\" 2>&1 | cut -c1-330",
 "description": "Pull contract, invoice, usage, ticket evidence per dispute"
}
```

### Tool · 2026-11-20 17:40:53 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/disp_verify.py (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:40:55 UTC
**Tool result:**
```
<persisted-output>
Output too large (36.9KB). Full output saved to: /Users/jacekmaterna/.claude/projects/-Users-jacekmaterna-Library-Application-Support-Claude-scratch-workspaces-e69441d8-02c7-4ae1-82fa-e65f61df0516-362a2cee-265f-40fd-99ca-8b843a81ad27-scratch-2026-11-20-a3ea2a/603a7d18-df39-4b28-94b6-4623216101e2/tool-results/b2scul5ny.txt

Preview (first 2KB):
===== INV-25539 C1439 Banerjee Petrov Engineers subscription 2026-07-01 due 2026-07-31 period 3 amt 2652.00 overdue ach
  customer: Growth active quarterly ach seats 13 arr 10608 renew 2027-04-01 signup 2025-04-01 country United States AM Nadia Sinclair
customer_id term_start   term_end   plan seats price_per_seat_per_month platform_fee   arr change_type prior_arr
      C1439 2025-04-01 2026-03-31 Growth    13                       68            0 10608         new          
      C1439 2026-04-01 2027-03-31 Growth    13                       68            0 10608     renewal     10608
invoice_id         type issue_date service_period_months  amount  status  paid_date
 INV-24097 subscription 2025-07-01                     3 2652.00    paid 2025-10-12
 INV-24461 subscription 2025-10-01                     3 2652.00    paid 2026-02-06
 INV-24823 subscription 2026-01-01                     3 2652.00    paid 2026-04-27
 INV-25181 subscription 2026-04-01                     3 2652.00    paid 2026-06-21
 INV-25539 subscription 2026-07-01                     3 2652.00 overdue           
 INV-25927 subscription 2026-10-01                     3 2652.00    open           
  month seats_licensed active_users uses_retainers uses_milestones uses_client_portal
2026-07             13           12            yes             yes                yes
2026-08             13           13            yes             yes                yes
2026-09             13           12            yes             yes                yes
2026-10             13           13            yes             yes                yes
  T T880432 2026-08-19 09:34 /solved | Client portal cancellation ignored | "We switched off the client portal in August because, frankly, our clients weren't logging into it. Your team confirmed the cancellation by email. INV-25539 not only still charges the monthly portal fe"

...
</persisted-output>
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/disp_verify.py",
 "content": "import sys, os, pandas as pd\nD=sys.argv[1]\nr=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)\ninv=r('finance/invoices.csv'); ctr=r('customers/contracts.csv'); cus=r('customers/customers.csv'); us=r('product/usage_monthly.csv'); tk=r('support/tickets.csv'); con=r('customers/contacts.csv')\nids=['INV-25539','INV-25662','INV-25718','INV-25711','INV-25757','INV-25730','INV-25712','INV-25765','INV-25764','INV-25750','INV-25787','INV-25811','INV-25822','INV-25834','INV-26009']\nfor i in ids:\n    v=inv[inv.invoice_id==i].iloc[0]; c=v.customer_id\n    print('\\n=====',i,c,v.customer_name,v.type,v.issue_date,'due',v.due_date,'period',v.service_period_months,'amt',v.amount,v.status,v.payment_method)\n    cu=cus[cus.customer_id==c].iloc[0]; print('  customer:',cu.plan,cu.status,cu.billing_frequency,cu.payment_method,'seats',cu.current_seats,'arr',cu.current_arr,'renew',cu.renewal_date,'signup',cu.signup_date,'country',cu.country,'AM',cu.account_manager)\n    print(ctr[ctr.customer_id==c].tail(4).to_string(index=False))\n    print(inv[(inv.customer_id==c)&(inv.issue_date>='2025-06-01')][['invoice_id','type','issue_date','service_period_months','amount','status','paid_date']].to_string(index=False))\n    u=us[us.customer_id==c].tail(4); print(u[['month','seats_licensed','active_users','uses_retainers','uses_milestones','uses_client_portal']].to_string(index=False))\n    for _,t in tk[tk.customer_id==c].iterrows():\n        print(f'  T {t.ticket_id} {t.created_at} {t.category}/{t.status} | {t.subject} | {t.body[:200]!r}')\n"
}
```
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/disp_verify.py\" \"$R/data\" 2>&1 | cut -c1-330",
 "description": "Pull contract, invoice, usage, ticket evidence per dispute"
}
```

### Claude · 2026-11-20 17:40:59 UTC
**Tool call:** `Read`
```json
{
 "file_path": "/Users/jacekmaterna/.claude/projects/-Users-jacekmaterna-Library-Application-Support-Claude-scratch-workspaces-e69441d8-02c7-4ae1-82fa-e65f61df0516-362a2cee-265f-40fd-99ca-8b843a81ad27-scratch-2026-11-20-a3ea2a/603a7d18-df39-4b28-94b6-4623216101e2/tool-results/b2scul5ny.txt"
}
```

### Tool · 2026-11-20 17:40:59 UTC
**Tool result:**
```
1	
2	===== INV-25539 C1439 Banerjee Petrov Engineers subscription 2026-07-01 due 2026-07-31 period 3 amt 2652.00 overdue ach
3	  customer: Growth active quarterly ach seats 13 arr 10608 renew 2027-04-01 signup 2025-04-01 country United States AM Nadia Sinclair
4	customer_id term_start   term_end   plan seats price_per_seat_per_month platform_fee   arr change_type prior_arr
5	      C1439 2025-04-01 2026-03-31 Growth    13                       68            0 10608         new          
6	      C1439 2026-04-01 2027-03-31 Growth    13                       68            0 10608     renewal     10608
7	invoice_id         type issue_date service_period_months  amount  status  paid_date
8	 INV-24097 subscription 2025-07-01                     3 2652.00    paid 2025-10-12
9	 INV-24461 subscription 2025-10-01                     3 2652.00    paid 2026-02-06
10	 INV-24823 subscription 2026-01-01                     3 2652.00    paid 2026-04-27
11	 INV-25181 subscription 2026-04-01                     3 2652.00    paid 2026-06-21
12	 INV-25539 subscription 2026-07-01                     3 2652.00 overdue           
13	 INV-25927 subscription 2026-10-01                     3 2652.00    open           
14	  month seats_licensed active_users uses_retainers uses_milestones uses_client_portal
15	2026-07             13           12            yes             yes                yes
16	2026-08             13           13            yes             yes                yes
17	2026-09             13           12            yes             yes                yes
18	2026-10             13           13            yes             yes                yes
19	  T T880432 2026-08-19 09:34 /solved | Client portal cancellation ignored | "We switched off the client portal in August because, frankly, our clients weren't logging into it. Your team confirmed the cancellation by email. INV-25539 not only still charges the monthly portal fe"
20	
21	===== INV-25662 C1254 Upton & Bell Advisory subscription 2026-07-27 due 2026-08-26 period 12 amt 44064.00 overdue wire
22	  customer: Growth active annual wire seats 54 arr 44064 renew 2027-07-27 signup 2022-07-27 country United States AM Hannah Drummond
23	customer_id term_start   term_end   plan seats price_per_seat_per_month platform_fee   arr change_type prior_arr
24	      C1254 2023-07-27 2024-07-26 Growth    37                       65            0 28860   expansion     23400
25	      C1254 2024-07-27 2025-07-26 Growth    46                  
… [result truncated, 39003 chars total]
```

### Claude ·  UTC
**Tool call:** `Read`
```json
{
 "file_path": "/Users/jacekmaterna/.claude/projects/-Users-jacekmaterna-Library-Application-Support-Claude-scratch-workspaces-e69441d8-02c7-4ae1-82fa-e65f61df0516-362a2cee-265f-40fd-99ca-8b843a81ad27-scratch-2026-11-20-a3ea2a/603a7d18-df39-4b28-94b6-4623216101e2/tool-results/b2scul5ny.txt"
}
```

### Claude · 2026-11-20 17:42:18 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/discrepancies.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD=sys.argv[1]; W=sys.argv[2]\nr=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ctr=r('customers/contracts.csv'); cus=r('customers/customers.csv'); bs=r('finance/balance_sheet_monthly.csv'); ar=r('finance/ar_aging.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float); ar['amt']=ar.amount.astype(float)\nfor c in ['seats','price_per_seat_per_month','platform_fee','arr']: ctr[c]=ctr[c].astype(int)\n\n# ---- 5 / 1: contract vs invoice amount, all invoices\nctr_s=ctr.sort_values(['customer_id','term_start'])\ndef term_for(c,d):\n    t=ctr_s[(ctr_s.customer_id==c)&(ctr_s.term_start<=d)&(ctr_s.term_end>=d)]\n    return t.iloc[-1] if len(t) else None\nrows=[]\nfor _,v in inv.iterrows():\n    t=term_for(v.customer_id,v.issue_date)\n    if t is None: rows.append(dict(invoice_id=v.invoice_id,term_start='',expected=np.nan)); continue\n    calc_arr=t.seats*t.price_per_seat_per_month*12+t.platform_fee\n    if v.type=='subscription': exp=round(t.arr*int(v.service_period_months)/12,2)\n    else: exp={'Core':0,'Growth':2500,'Enterprise':8000}[t.plan]\n    rows.append(dict(invoice_id=v.invoice_id,term_start=t.term_start,plan=t.plan,seats=t.seats,price=t.price_per_seat_per_month,platform_fee=t.platform_fee,contract_arr=t.arr,arr_formula_ok=calc_arr==t.arr,expected=exp))\ncm=inv.merge(pd.DataFrame(rows),on='invoice_id',how='left')\ncm['diff']=(cm.amt-cm.expected).round(2)\ncm['post_rewrite']=cm.issue_date>='2026-03-16'\nprint('no covering contract term:', cm.expected.isna().sum()); print(cm[cm.expected.isna()][['invoice_id','customer_id','issue_date','type','amt','status']].head(10).to_string())\nprint('arr formula mismatches in contracts:', (~cm.arr_formula_ok.fillna(True).astype(bool)).sum(), ' contract rows w/ arr!=formula:', (ctr.seats*ctr.price_per_seat_per_month*12+ctr.platform_fee!=ctr.arr).sum())\nmm=cm[cm['diff'].fillna(0)!=0]\nprint('invoice != contract-derived amount:', len(mm), 'of', cm.expected.notna().sum()); print(pd.crosstab(mm.type,mm.post_rewrite))\nprint(mm[['invoice_id','customer_id','customer_name','type','issue_date','service_period_months','amt','expected','diff','status','plan','seats','price']].head(40).to_string())\nop=cm[cm.status.isin(['open','overdue','payment_failed'])]\nprint('OPEN invoices mismatching contract:', (op['diff'].fillna(0)!=0).sum(), 'of', len(op), ' no term:', op.expected.isna().sum())\ncm.drop(columns=[]).to_csv(os.path.join(W,'check5_contract_vs_invoice_all.csv'),index=False)\nop.to_csv(os.path.join(W,'check5_contract_vs_invoice_open.csv'),index=False)\n# price list check on terms post-2025\nlate=ctr[(ctr.term_start>='2025-01-01')]\npl={'Core':47,'Growth':68,'Enterprise':88}\nbad=late[late.price_per_seat_per_month!=late.plan.map(pl)]\nprint('2025+ contract terms not on 2025 price list:', len(bad), bad.change_type.value_counts().to_dict())\nmins={'Core':8,'Growth':12,'Enterprise':20}\nprint('terms below min seats:', (ctr.seats<ctr.plan.map(mins)).sum())\n# implementation invoices: for new customers only?\nimp=cm[cm.type=='implementation']\nprint('implementation invoices', len(imp), imp.amt.value_counts().to_dict(), 'diff!=0', (imp['diff']!=0).sum())\n\n# ---- 2: AR tie-out monthly\np=pay[pay.invoice_id!=''].set_index('invoice_id')\ninv['applied']=inv.invoice_id.map(p.applied_date); inv.loc[inv.status=='written_off','applied']=inv.paid_date; inv['applied']=inv.applied.fillna('9999')\nout=[]\nfor _,b in bs.iterrows():\n    me=(pd.Period(b.month)).end_time.strftime('%Y-%m-%d')\n    o=inv[(inv.issue_date<=me)&(inv.applied>me)].amt.sum()\n    un=pay[(pay.received_date<=me)&((pay.applied_date>me)|(pay.applied_date==''))].amt.sum()\n    out.append(dict(month=b.month,bs_ar=float(b.accounts_receivable),ledger_open_ar=o,ar_diff=float(b.accounts_receivable)-o,bs_unapplied=float(b.unapplied_cash_receipts),recon_unapplied=un,unapplied_diff=float(b.unapplied_cash_receipts)-un))\ntie=pd.DataFrame(out); print(tie.tail(8).to_string()); print('months with AR diff:', (tie.ar_diff.abs()>0.5).sum(), 'unapplied diff:', (tie.unapplied_diff.abs()>0.5).sum(), 'of', len(tie))\nprint(tie[(tie.ar_diff.abs()>0.5)|(tie.unapplied_diff.abs()>0.5)].to_string())\ntie.to_csv(os.path.join(W,'check2_ar_tieout.csv'),index=False)\nprint('asof: ar_aging', ar.amt.sum(), 'invoices open', inv[inv.status.isin(['open','overdue','payment_failed'])].amt.sum(), 'bs', bs.iloc[-1].accounts_receivable, 'unapplied', pay[pay.invoice_id==''].amt.sum())\n\n# ---- 3: overpay / duplicates / cross-customer\npm=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amt','issue_date']],on='invoice_id',suffixes=('','_inv'))\nprint('over/under payments:', (pm.amt!=pm.amt_inv).sum())\nprint('payment before invoice issue:', (pm.received_date<pm.issue_date).sum())\ndup=pay[pay.duplicated(['payer_name','amount','received_date'],keep=False)]\nprint('dup (payer,amount,date):', len(dup)); print(dup.head(10).to_string())\ndup2=pay[pay.duplicated(['payer_name','amount','memo'],keep=False)&(pay.memo.str.contains(r'\\d{5}'))]\nprint('dup (payer,amount,memo w/ inv ref):', len(dup2))\nnorm=lambda s: re.sub(r'[^a-z0-9]','',s.lower()); cn=dict(zip(cus.name.map(norm),cus.customer_id))\npm['payer_exact_cid']=pm.payer_name.map(lambda x: cn.get(norm(x),''))\ncross=pm[(pm.payer_exact_cid!='')&(pm.payer_exact_cid!=pm.customer_id)]\nprint('payer name exactly = a DIFFERENT customer than invoice:', len(cross)); print(cross[['payment_id','payer_name','payer_exact_cid','invoice_id','customer_id','customer_name','amt']].head(20).to_string())\npm['payer_prefix_ok']=[norm(c).startswith(norm(p_)) for p_,c in zip(pm.payer_name,pm.custom
… [tool input truncated]
```

### Claude · 2026-11-20 17:42:20 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/discrepancies.py\" \"$R/data\" \"$R/analysis/work\" 2>&1 | cut -c1-250",
 "description": "Run discrepancy checks 2-5"
}
```

### Tool · 2026-11-20 17:42:20 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/discrepancies.py (file state is current in your context — no need to Read it back)
```

### Tool · 2026-11-20 17:42:24 UTC
**Tool result:**
```
no covering contract term: 0
Empty DataFrame
Columns: [invoice_id, customer_id, issue_date, type, amt, status]
Index: []
arr formula mismatches in contracts: 0  contract rows w/ arr!=formula: 0
invoice != contract-derived amount: 0 of 6062
Empty DataFrame
Columns: []
Index: []
Empty DataFrame
Columns: [invoice_id, customer_id, customer_name, type, issue_date, service_period_months, amt, expected, diff, status, plan, seats, price]
Index: []
OPEN invoices mismatching contract: 0 of 117  no term: 0
2025+ contract terms not on 2025 price list: 0 {}
terms below min seats: 23
implementation invoices 124 {2500.0: 105, 8000.0: 19} diff!=0 0
      month      bs_ar  ledger_open_ar  ar_diff  bs_unapplied  recon_unapplied  unapplied_diff
38  2026-03   992099.0        992099.0      0.0      232822.0         232822.0             0.0
39  2026-04  1001467.0       1001467.0      0.0       29331.0          29331.0             0.0
40  2026-05   717783.0        717783.0      0.0      177204.0         177204.0             0.0
41  2026-06   790726.0        790726.0      0.0      106596.0         106596.0             0.0
42  2026-07  1181935.0       1181935.0      0.0       71196.0          71196.0             0.0
43  2026-08  1260557.0       1260557.0      0.0      225876.0         225876.0             0.0
44  2026-09  1286085.0       1286085.0      0.0      154741.0         154741.0             0.0
45  2026-10  1430632.0       1430632.0      0.0       87335.0          87335.0             0.0
months with AR diff: 0 unapplied diff: 0 of 46
Empty DataFrame
Columns: [month, bs_ar, ledger_open_ar, ar_diff, bs_unapplied, recon_unapplied, unapplied_diff]
Index: []
asof: ar_aging 1430632.0 invoices open 1430632.0 bs 1430632 unapplied 87335.0
over/under payments: 0
payment before invoice issue: 0
dup (payer,amount,date): 0
Empty DataFrame
Columns: [payment_id, received_date, amount, method, payer_name, memo, applied_date, invoice_id, amt]
Index: []
dup (payer,amount,memo w/ inv ref): 0
payer name exactly = a DIFFERENT customer than invoice: 0
Empty DataFrame
Columns: [payment_id, payer_name, payer_exact_cid, invoice_id, customer_id, customer_name, amt]
Index: []
payer not a prefix of invoice customer name: 0
invoices issued on/after churn date: 0 0.0 {}
invoices whose service period runs >1 month past churn: 0 0.0
open AR on churned customers: 0
write-offs by method: {'card': 144} days_to_wo [150]
     invoice_id customer_id             customer_name  issue_date   paid_date      amt se
… [result truncated, 3699 chars total]
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/scripts/discrepancies.py",
 "content": "import sys, os, re, pandas as pd, numpy as np\nD=sys.argv[1]; W=sys.argv[2]\nr=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)\ninv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ctr=r('customers/contracts.csv'); cus=r('customers/customers.csv'); bs=r('finance/balance_sheet_monthly.csv'); ar=r('finance/ar_aging.csv')\ninv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float); ar['amt']=ar.amount.astype(float)\nfor c in ['seats','price_per_seat_per_month','platform_fee','arr']: ctr[c]=ctr[c].astype(int)\n\n# ---- 5 / 1: contract vs invoice amount, all invoices\nctr_s=ctr.sort_values(['customer_id','term_start'])\ndef term_for(c,d):\n    t=ctr_s[(ctr_s.customer_id==c)&(ctr_s.term_start<=d)&(ctr_s.term_end>=d)]\n    return t.iloc[-1] if len(t) else None\nrows=[]\nfor _,v in inv.iterrows():\n    t=term_for(v.customer_id,v.issue_date)\n    if t is None: rows.append(dict(invoice_id=v.invoice_id,term_start='',expected=np.nan)); continue\n    calc_arr=t.seats*t.price_per_seat_per_month*12+t.platform_fee\n    if v.type=='subscription': exp=round(t.arr*int(v.service_period_months)/12,2)\n    else: exp={'Core':0,'Growth':2500,'Enterprise':8000}[t.plan]\n    rows.append(dict(invoice_id=v.invoice_id,term_start=t.term_start,plan=t.plan,seats=t.seats,price=t.price_per_seat_per_month,platform_fee=t.platform_fee,contract_arr=t.arr,arr_formula_ok=calc_arr==t.arr,expected=exp))\ncm=inv.merge(pd.DataFrame(rows),on='invoice_id',how='left')\ncm['diff']=(cm.amt-cm.expected).round(2)\ncm['post_rewrite']=cm.issue_date>='2026-03-16'\nprint('no covering contract term:', cm.expected.isna().sum()); print(cm[cm.expected.isna()][['invoice_id','customer_id','issue_date','type','amt','status']].head(10).to_string())\nprint('arr formula mismatches in contracts:', (~cm.arr_formula_ok.fillna(True).astype(bool)).sum(), ' contract rows w/ arr!=formula:', (ctr.seats*ctr.price_per_seat_per_month*12+ctr.platform_fee!=ctr.arr).sum())\nmm=cm[cm['diff'].fillna(0)!=0]\nprint('invoice != contract-derived amount:', len(mm), 'of', cm.expected.notna().sum()); print(pd.crosstab(mm.type,mm.post_rewrite))\nprint(mm[['invoice_id','customer_id','customer_name','type','issue_date','service_period_months','amt','expected','diff','status','plan','seats','price']].head(40).to_string())\nop=cm[cm.status.isin(['open','overdue','payment_failed'])]\nprint('OPEN invoices mismatching contract:', (op['diff'].fillna(0)!=0).sum(), 'of', len(op), ' no term:', op.expected.isna().sum())\ncm.drop(columns=[]).to_csv(os.path.join(W,'check5_contract_vs_invoice_all.csv'),index=False)\nop.to_csv(os.path.join(W,'check5_contract_vs_invoice_open.csv'),index=False)\n# price list check on terms post-2025\nlate=ctr[(ctr.term_start>='2025-01-01')]\npl={'Core':47,'Growth':68,'Enterprise':88}\nbad=late[late.price_per_seat_per_month!=late.plan.map(pl)]\nprint('2025+ contract terms not on 2025 price list:', len(bad), bad.change_type.value_counts().to_dict())\nmins={'Core':8,'Growth':12,'Enterprise':20}\nprint('terms below min seats:', (ctr.seats<ctr.plan.map(mins)).sum())\n# implementation invoices: for new customers only?\nimp=cm[cm.type=='implementation']\nprint('implementation invoices', len(imp), imp.amt.value_counts().to_dict(), 'diff!=0', (imp['diff']!=0).sum())\n\n# ---- 2: AR tie-out monthly\np=pay[pay.invoice_id!=''].set_index('invoice_id')\ninv['applied']=inv.invoice_id.map(p.applied_date); inv.loc[inv.status=='written_off','applied']=inv.paid_date; inv['applied']=inv.applied.fillna('9999')\nout=[]\nfor _,b in bs.iterrows():\n    me=(pd.Period(b.month)).end_time.strftime('%Y-%m-%d')\n    o=inv[(inv.issue_date<=me)&(inv.applied>me)].amt.sum()\n    un=pay[(pay.received_date<=me)&((pay.applied_date>me)|(pay.applied_date==''))].amt.sum()\n    out.append(dict(month=b.month,bs_ar=float(b.accounts_receivable),ledger_open_ar=o,ar_diff=float(b.accounts_receivable)-o,bs_unapplied=float(b.unapplied_cash_receipts),recon_unapplied=un,unapplied_diff=float(b.unapplied_cash_receipts)-un))\ntie=pd.DataFrame(out); print(tie.tail(8).to_string()); print('months with AR diff:', (tie.ar_diff.abs()>0.5).sum(), 'unapplied diff:', (tie.unapplied_diff.abs()>0.5).sum(), 'of', len(tie))\nprint(tie[(tie.ar_diff.abs()>0.5)|(tie.unapplied_diff.abs()>0.5)].to_string())\ntie.to_csv(os.path.join(W,'check2_ar_tieout.csv'),index=False)\nprint('asof: ar_aging', ar.amt.sum(), 'invoices open', inv[inv.status.isin(['open','overdue','payment_failed'])].amt.sum(), 'bs', bs.iloc[-1].accounts_receivable, 'unapplied', pay[pay.invoice_id==''].amt.sum())\n\n# ---- 3: overpay / duplicates / cross-customer\npm=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amt','issue_date']],on='invoice_id',suffixes=('','_inv'))\nprint('over/under payments:', (pm.amt!=pm.amt_inv).sum())\nprint('payment before invoice issue:', (pm.received_date<pm.issue_date).sum())\ndup=pay[pay.duplicated(['payer_name','amount','received_date'],keep=False)]\nprint('dup (payer,amount,date):', len(dup)); print(dup.head(10).to_string())\ndup2=pay[pay.duplicated(['payer_name','amount','memo'],keep=False)&(pay.memo.str.contains(r'\\d{5}'))]\nprint('dup (payer,amount,memo w/ inv ref):', len(dup2))\nnorm=lambda s: re.sub(r'[^a-z0-9]','',s.lower()); cn=dict(zip(cus.name.map(norm),cus.customer_id))\npm['payer_exact_cid']=pm.payer_name.map(lambda x: cn.get(norm(x),''))\ncross=pm[(pm.payer_exact_cid!='')&(pm.payer_exact_cid!=pm.customer_id)]\nprint('payer name exactly = a DIFFERENT customer than invoice:', len(cross)); print(cross[['payment_id','payer_name','payer_exact_cid','invoice_id','customer_id','customer_name','amt']].head(20).to_string())\npm['payer_prefix_ok']=[norm(c).startswith(norm(p_)) for p_,c in zip(pm.payer_name,pm.custom
… [tool input truncated]
```
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; \"$R/.venv/bin/python\" -I \"$R/analysis/scripts/discrepancies.py\" \"$R/data\" \"$R/analysis/work\" 2>&1 | cut -c1-250",
 "description": "Run discrepancy checks 2-5"
}
```

### Claude · 2026-11-20 17:42:36 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/analysis/work\"; \"$R/.venv/bin/python\" -I - \"$R/analysis/work/check4_writeoffs.csv\" \"$R/data/finance/invoices.csv\" \"$R/data/customers/customers.csv\" <<'EOF'\nimport sys,pandas as pd\nw=pd.read_csv(sys.argv[1],dtype=str); i=pd.read_csv(sys.argv[2],dtype=str); c=pd.read_csv(sys.argv[3],dtype=str)\nb=w[w.over_2k=='True']; print(b[['invoice_id','customer_name','type','amount','customer_status']].to_string())\nprint(c[c.customer_id.isin(['C1030','C1266','C1409','C1075','C1045'])][['customer_id','name','industry','country','status','renewal_date','billing_frequency']].to_string())\nprint(i[i.customer_id=='C1426'][['invoice_id','issue_date','amount','status','paid_date']].tail(6).to_string())\nEOF\ngrep -c \"\" \"$R/analysis/work/check3_cross_customer.csv\"",
 "description": "Detail write-offs and customer master checks"
}
```

### Tool · 2026-11-20 17:42:38 UTC
**Tool result:**
```
    invoice_id             customer_name            type    amount customer_status
3    INV-20304         Drummond Strategy    subscription   4485.00         churned
58   INV-22712         Greystone Digital    subscription   2535.00          active
82   INV-23444       Eastman Engineering    subscription   3264.00          active
94   INV-23907  Moreau & Glover Advisory    subscription   4095.00          active
104  INV-24229  Upton Stanhope Engineers    subscription   5712.00          active
114  INV-24416              Ellery Legal    subscription  17520.00          active
120  INV-24647         Haddad Thorne Law    subscription   2856.00          active
124  INV-24749          Kingsway Digital  implementation   2500.00          active
139  INV-25261           Studio Calloway    subscription   4284.00          active
    customer_id                   name                      industry         country  status renewal_date billing_frequency
29        C1030  Mercer & Banerjee LLP                      Law firm   United States  active   2026-11-12         quarterly
44        C1045    Castell Engineering       Engineering consultancy          Canada  active   2027-02-23         quarterly
74        C1075        Brandt Ashby IT              IT services firm  United Kingdom  active   2027-09-07            annual
265       C1266   Thackeray Accounting               Accounting firm   United States  active   2027-08-18            annual
408       C1409           Wexler Media  Marketing or creative agency  United Kingdom  active   2027-09-04           monthly
     invoice_id  issue_date   amount          status   paid_date
4133  INV-24134  2025-07-08  3264.00            paid  2025-07-08
4506  INV-24507  2025-10-08  3264.00            paid  2025-10-08
4861  INV-24862  2026-01-08  3264.00            paid  2026-01-08
5216  INV-25217  2026-04-08  3264.00            paid  2026-04-08
5576  INV-25577  2026-07-08  3264.00            paid  2026-07-08
5972  INV-25973  2026-10-08  3264.00  payment_failed         NaN
1
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cd \"$R/analysis/work\"; \"$R/.venv/bin/python\" -I - \"$R/analysis/work/check4_writeoffs.csv\" \"$R/data/finance/invoices.csv\" \"$R/data/customers/customers.csv\" <<'EOF'\nimport sys,pandas as pd\nw=pd.read_csv(sys.argv[1],dtype=str); i=pd.read_csv(sys.argv[2],dtype=str); c=pd.read_csv(sys.argv[3],dtype=str)\nb=w[w.over_2k=='True']; print(b[['invoice_id','customer_name','type','amount','customer_status']].to_string())\nprint(c[c.customer_id.isin(['C1030','C1266','C1409','C1075','C1045'])][['customer_id','name','industry','country','status','renewal_date','billing_frequency']].to_string())\nprint(i[i.customer_id=='C1426'][['invoice_id','issue_date','amount','status','paid_date']].tail(6).to_string())\nEOF\ngrep -c \"\" \"$R/analysis/work/check3_cross_customer.csv\"",
 "description": "Detail write-offs and customer master checks"
}
```

### Claude · 2026-11-20 17:43:09 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/work/check1_disputes_verdicts.csv\" <<'EOF'\ninvoice_id,customer_id,customer_name,ticket_id,ticket_status,invoice_amount,contract_term,contract_seats,price_per_seat,platform_fee,contract_arr,expected_invoice_amount,amount_matches_contract,customer_claim,verdict,credit_due_per_data,exposure_if_customer_proven_right,key_evidence\nINV-25787,C1073,Riverside Partners,T880886,solved,60576,2026-08-27..2027-08-26 expansion,46,88,12000,60576,60576,yes,62 seats billed vs 38 people (workspace merge),we're right on invoice (bills 46 not 62); can't tell if 39->46 expansion was merge artefact,0,7392 (39->46 seats x $88 x 12) up to 8448 (46->38),contract row C1073 2026-08-27 seats 46; usage seats_licensed 39 (Jul) ->46 (Aug); active_users 38 (Oct) 43 (Sep)\nINV-25712,C1261,Wexler & Hume Advisory,T880757,solved,4080,2026-08-10..2027-08-09 renewal,20,68,0,16320,4080,yes,billed for 24 users; have 17,we're right (invoice is 20 seats not 24; seats renewed at 20 on 08-10; reductions only at renewal),0,816 per quarter if cut to 17 (3x$68x3),contract C1261 2026-08-10 seats 20; usage active 10-13\nINV-25730,C1264,Westbrook Engineering Group,T880739,pending,47904,2026-08-14..2027-08-13 renewal,34,88,12000,47904,47904,yes,implementation fee should be waived,we're right (invoice = 34x88x12+12000 exactly; no implementation invoice exists; impl fee only for new customers; customer since 2022),0,0,no type=implementation invoice for C1264; pricing: impl fee new customers only; multi-year not offered\nINV-25765,C1154,Okafor & Nakamura LLP,T880816,solved,46848,2026-08-23..2027-08-22 renewal,33,88,12000,46848,46848,yes,AM promised 50% off 3 months for 2nd office,can't tell (no contract change for 2nd office; seats flat at 33; discount >10% needs Head of Sales; first-year only),0,5856 (50% x 3/12 x 46848) upper bound,contract seats 33 unchanged since 2023; usage active 12-13 of 33; pricing discount rules\nINV-25764,C1045,Castell Engineering,T880849,solved,6324,2026-02-23..2027-02-22 renewal,31,68,0,25296,6324,yes,downgraded 'pro'->'standard' on the 3rd; billed full month pro,we're right per contract (Growth 31 seats to 2027-02-22; plans named pro/standard don't exist; invoice is quarterly not monthly; downgrade on 10-03 postdates 08-23 invoice),0,~1070 (Growth->Core 31 seats x $21 x 50/365 x 12; would go on next invoice post-rewrite),contract C1045 Growth 31; customers.plan Growth; reductions at renewal only\nINV-25822,C1075,Brandt Ashby IT,T881024,pending,26112,2026-09-07..2027-09-06 renewal,32,68,0,26112,26112,yes,moved annual Enterprise -> monthly Team before renewal,we're right on amount (Growth not Enterprise; 'Team' plan doesn't exist; billing_frequency annual); can't verify confirmation screen,0,0 revenue; if switch to monthly billing proven: void and rebill 12 x 2176 (cash timing only),contract C1075 Growth 32 x 68; customers.billing_frequency annual; pricing: all contracts annual; frequency is billing choice\nINV-25750,C1266,Thackeray Accounting,T880856,solved,7896,2026-08-18..2027-08-17 renewal,14,47,0,7896,7896,yes,20% VAT added; should be reverse charge,can't tell (tax not in data: amounts exclude tax); base amount correct; customer master says United States (VAT reverse charge implausible),0 on base,tax line unknown (20% = 1579.20 if charged),customers.country United States; README amounts exclude sales tax\nINV-25757,C1152,Ellery Consulting,T880738,solved,13056,2026-08-21..2027-08-20 renewal,16,68,0,13056,13056,yes,sales tax calculated on old address,can't tell (tax not in data); base amount correct,0 on base,rate difference unknown,README amounts exclude sales tax; contract 16 x 68 x 12\nINV-25811,C1409,Wexler Media,T880957,pending,1224,2026-09-04..2027-09-03 renewal,18,68,0,14688,1224,yes,15% multi-year discount agreed at renewal,we're right (pricing: multi-year discounts not offered; renewal at list; customer is monthly not annual),0,183.60/month (15% of 1224) if AM overrode policy,contract C1409 renewal 18 x 68 list; pricing_and_packaging 'Multi-year discounts are not offered'\nINV-25718,C1030,Mercer & Banerjee LLP,T880648,solved,3876,2025-11-12..2026-11-11 expansion,19,68,0,15504,3876,yes,time-tracking module cancelled; still charged,we're right (no priced modules; invoice = 19x68x3); NB separate termination notice T880514 (eff. 30 Jun) not reflected; renewal 2026-11-12,0,0 on this invoice; renewal invoice 11-12 (15504/4) at risk,contract 19 x 68; pricing has no add-on modules; T880514 Billing/solved\nINV-25662,C1254,Upton & Bell Advisory,T880582,solved,44064,2026-07-27..2027-07-26 expansion,54,68,0,44064,44064,yes,late fee after card outage on our side,we're right (invoice = 54x68x12 exactly; no late fee in ledger; customer pays by wire not card),0,0,invoice amount = contract arr; customers.payment_method wire; no late-fee concept in policy\nINV-25711,C1100,Oyelaran Devlin Engineers,T880667,solved,2820,2026-02-10..2027-02-09 renewal,20,47,0,11280,2820,yes,data migration fee waived in writing,we're right (invoice = 20x47x3 exactly; no migration-fee item exists in data),0,0,contract 20 x 47; no implementation/migration invoice\nINV-25539,C1439,Banerjee Petrov Engineers,T880432,solved,2652,2026-04-01..2027-03-31 renewal,13,68,0,10608,2652,yes,client portal fee + setup line still charged,we're right (portal included in Core/Growth; invoice = 13x68x3; usage shows portal still in use Jul-Oct),0,0,pricing: client portal included in Core; usage uses_client_portal=yes 2026-07..10\nINV-25834,C1161,\"Delacroix, Jessop & Co\",T881039,solved,41568,2026-09-09..2027-09-08 renewal,28,88,12000,41568,41568,yes,3 seats for leavers,we're right per contract (renewed at 28 seats on 09-09; active users 23-27); can't tell if reduction was requested,0,3168 (3 x 88 x 12),contract C1161 2026-09-09 seats 28; usage act
… [tool input truncated]
```

### Tool · 2026-11-20 17:43:11 UTC
**Tool result:**
```
15 {'yes': 15}
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; cat > \"$R/analysis/work/check1_disputes_verdicts.csv\" <<'EOF'\ninvoice_id,customer_id,customer_name,ticket_id,ticket_status,invoice_amount,contract_term,contract_seats,price_per_seat,platform_fee,contract_arr,expected_invoice_amount,amount_matches_contract,customer_claim,verdict,credit_due_per_data,exposure_if_customer_proven_right,key_evidence\nINV-25787,C1073,Riverside Partners,T880886,solved,60576,2026-08-27..2027-08-26 expansion,46,88,12000,60576,60576,yes,62 seats billed vs 38 people (workspace merge),we're right on invoice (bills 46 not 62); can't tell if 39->46 expansion was merge artefact,0,7392 (39->46 seats x $88 x 12) up to 8448 (46->38),contract row C1073 2026-08-27 seats 46; usage seats_licensed 39 (Jul) ->46 (Aug); active_users 38 (Oct) 43 (Sep)\nINV-25712,C1261,Wexler & Hume Advisory,T880757,solved,4080,2026-08-10..2027-08-09 renewal,20,68,0,16320,4080,yes,billed for 24 users; have 17,we're right (invoice is 20 seats not 24; seats renewed at 20 on 08-10; reductions only at renewal),0,816 per quarter if cut to 17 (3x$68x3),contract C1261 2026-08-10 seats 20; usage active 10-13\nINV-25730,C1264,Westbrook Engineering Group,T880739,pending,47904,2026-08-14..2027-08-13 renewal,34,88,12000,47904,47904,yes,implementation fee should be waived,we're right (invoice = 34x88x12+12000 exactly; no implementation invoice exists; impl fee only for new customers; customer since 2022),0,0,no type=implementation invoice for C1264; pricing: impl fee new customers only; multi-year not offered\nINV-25765,C1154,Okafor & Nakamura LLP,T880816,solved,46848,2026-08-23..2027-08-22 renewal,33,88,12000,46848,46848,yes,AM promised 50% off 3 months for 2nd office,can't tell (no contract change for 2nd office; seats flat at 33; discount >10% needs Head of Sales; first-year only),0,5856 (50% x 3/12 x 46848) upper bound,contract seats 33 unchanged since 2023; usage active 12-13 of 33; pricing discount rules\nINV-25764,C1045,Castell Engineering,T880849,solved,6324,2026-02-23..2027-02-22 renewal,31,68,0,25296,6324,yes,downgraded 'pro'->'standard' on the 3rd; billed full month pro,we're right per contract (Growth 31 seats to 2027-02-22; plans named pro/standard don't exist; invoice is quarterly not monthly; downgrade on 10-03 postdates 08-23 invoice),0,~1070 (Growth->Core 31 seats x $21 x 50/365 x 12; would go on next invoice post-rewrite),contract C1045 Growth 31; customers.plan Growth; reductions at renewal only\nINV-25822,C1075,Brandt Ashby IT,T881024,pending,26112,2026-09-07..2027-09-06 renewal,32,68,0,26112,26112,yes,moved annual Enterprise -> monthly Team before renewal,we're right on amount (Growth not Enterprise; 'Team' plan doesn't exist; billing_frequency annual); can't verify confirmation screen,0,0 revenue; if switch to monthly billing proven: void and rebill 12 x 2176 (cash timing only),contract C1075 Growth 32 x 68; customers.billing_frequency annual; pricing: all contracts annual; frequency is billing choice\nINV-25750,C1266,Thackeray Accounting,T880856,solved,7896,2026-08-18..2027-08-17 renewal,14,47,0,7896,7896,yes,20% VAT added; should be reverse charge,can't tell (tax not in data: amounts exclude tax); base amount correct; customer master says United States (VAT reverse charge implausible),0 on base,tax line unknown (20% = 1579.20 if charged),customers.country United States; README amounts exclude sales tax\nINV-25757,C1152,Ellery Consulting,T880738,solved,13056,2026-08-21..2027-08-20 renewal,16,68,0,13056,13056,yes,sales tax calculated on old address,can't tell (tax not in data); base amount correct,0 on base,rate difference unknown,README amounts exclude sales tax; contract 16 x 68 x 12\nINV-25811,C1409,Wexler Media,T880957,pending,1224,2026-09-04..2027-09-03 renewal,18,68,0,14688,1224,yes,15% multi-year discount agreed at renewal,we're right (pricing: multi-year discounts not offered; renewal at list; customer is monthly not annual),0,183.60/month (15% of 1224) if AM overrode policy,contract C1409 renewal 18 x 68 list; pricing_and_packaging 'Multi-year discounts are not offered'\nINV-25718,C1030,Mercer & Banerjee LLP,T880648,solved,3876,2025-11-12..2026-11-11 expansion,19,68,0,15504,3876,yes,time-tracking module cancelled; still charged,we're right (no priced modules; invoice = 19x68x3); NB separate termination notice T880514 (eff. 30 Jun) not reflected; renewal 2026-11-12,0,0 on this invoice; renewal invoice 11-12 (15504/4) at risk,contract 19 x 68; pricing has no add-on modules; T880514 Billing/solved\nINV-25662,C1254,Upton & Bell Advisory,T880582,solved,44064,2026-07-27..2027-07-26 expansion,54,68,0,44064,44064,yes,late fee after card outage on our side,we're right (invoice = 54x68x12 exactly; no late fee in ledger; customer pays by wire not card),0,0,invoice amount = contract arr; customers.payment_method wire; no late-fee concept in policy\nINV-25711,C1100,Oyelaran Devlin Engineers,T880667,solved,2820,2026-02-10..2027-02-09 renewal,20,47,0,11280,2820,yes,data migration fee waived in writing,we're right (invoice = 20x47x3 exactly; no migration-fee item exists in data),0,0,contract 20 x 47; no implementation/migration invoice\nINV-25539,C1439,Banerjee Petrov Engineers,T880432,solved,2652,2026-04-01..2027-03-31 renewal,13,68,0,10608,2652,yes,client portal fee + setup line still charged,we're right (portal included in Core/Growth; invoice = 13x68x3; usage shows portal still in use Jul-Oct),0,0,pricing: client portal included in Core; usage uses_client_portal=yes 2026-07..10\nINV-25834,C1161,\"Delacroix, Jessop & Co\",T881039,solved,41568,2026-09-09..2027-09-08 renewal,28,88,12000,41568,41568,yes,3 seats for leavers,we're right per contract (renewed at 28 seats on 09-09; active users 23-27); can't tell if reduction was requested,0,3168 (3 x 88 x 12),contract C1161 2026-09-09 seats 28; usage act
… [tool input truncated]
```

### Claude · 2026-11-20 17:43:54 UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/DISCREPANCIES.md",
 "content": "# DISCREPANCIES — finance review before handover (as of 2026-10-31)\n\nScripts: `analysis/scripts/discrepancies.py`, `analysis/scripts/disp_verify.py`. Per-check CSVs are in `analysis/work/check1..5_*.csv`.\n**F** = fact computed from the data. **I** = inference. `data/` and `app/` were not touched.\n\n## Headline\nThe ledger is internally consistent. Every invoice in the data room (6,062 of 6,062) equals the amount derived from its contract term. AR ties to the balance sheet to the dollar in all 46 months.\n\nThe open question is not \"is our arithmetic wrong\" but **\"what did the customer see on the invoice document?\"** invoices.csv has one amount per invoice, with no line items, no tax and no discounts. None of the disputed extra lines (fees, VAT, late fee, module) exist in the ledger amount. So the evidence finance can send each customer is the contract row and the invoice amount, and an account manager confirms anything verbal.\n\n## 1. The 14 disputes (+ Reyes) — `work/check1_disputes_verdicts.csv`\nMethod (F): for each invoice I took the contract term covering issue_date. Expected amount = contract arr × service_period_months / 12, where arr = seats × price × 12 + platform fee (this formula holds on all 1,757 contract rows). I then checked customers.csv, usage_monthly.csv (seats, active users, modules) and pricing_and_packaging.md.\n\n**F: all 15 invoices equal their contract amount exactly.** Credit due according to the data: **$0 on every invoice.**\n\n| invoice | customer | $ | claim | verdict | exposure if customer proves it (I) |\n|---|---|---|---|---|---|\n| INV-25787 | Riverside Partners | 60,576 | 62 seats vs 38 people | **We're right on the invoice**: it bills 46 seats, not 62. **Can't tell** whether the 39→46 expansion at the 08-27 renewal came from the merge. Usage shows 38 active users in Oct, 43 in Sep. | $7,392 (7 seats) to $8,448 (down to 38) |\n| INV-25712 | Wexler & Hume | 4,080 | billed 24 users, have 17 | **We're right**: the invoice is for 20 seats, not 24. They renewed at 20 on 08-10, and seat reductions are allowed at renewal only. | $816/quarter if cut to 17 |\n| INV-25730 | Westbrook Eng. (top-50) | 47,904 | implementation fee should have been waived | **We're right**: 34×88×12 + 12,000 = 47,904 exactly. The customer has no implementation invoice, the fee applies to new customers only (they have been a customer since 2022), and multi-year deals are not offered. | $0 |\n| INV-25765 | Okafor & Nakamura (top-50) | 46,848 | 50% off 3 months for second office | **Can't tell.** There is no contract change for a second office (33 seats, flat since 2023). A discount over 10% needs the Head of Sales and is first-year only. | ≤ $5,856 |\n| INV-25764 | Castell Eng. | 6,324 | downgraded \"pro→standard\", billed a full month | **We're right per contract**: Growth, 31 seats, until 2027-02-22. No plans called pro or standard exist. The invoice is quarterly (08-23), and the downgrade date (10-03) is after it. After the rewrite, a plan change goes on the *next* invoice. | about $1,070 on the next invoice |\n| INV-25822 | Brandt Ashby IT | 26,112 | moved annual Enterprise→monthly \"Team\" | **We're right on the amount**: the plan is Growth, there is no \"Team\" plan, and the record says annual billing. **Can't verify** the confirmation screen they mention. | $0 revenue. If proven: void and rebill 12 × $2,176 (cash timing only) |\n| INV-25750 | Thackeray Accounting | 7,896 | 20% VAT added, should be reverse charge | **Can't tell**: tax is excluded from all amounts in the data. The base amount is correct. The customer record says **United States**, so a VAT reverse charge is implausible: either the master record or the tax engine is wrong. | tax line only (about $1,579 if 20% was charged) |\n| INV-25757 | Ellery Consulting | 13,056 | sales tax on old address | **Can't tell** (tax not in data). Base amount is correct. | rate difference only |\n| INV-25811 | Wexler Media | 1,224 | 15% multi-year discount | **We're right**: pricing says multi-year discounts are not offered, they renewed at list price, and they are billed monthly, not annually. | $183.60/month if an AM overrode policy |\n| INV-25718 | Mercer & Banerjee | 3,876 | time-tracking module cancelled | **We're right**: there are no priced modules, and 19×68×3 = 3,876. **Separate risk:** termination notice T880514 (\"discontinuing… effect from 30 June\", Billing, solved) is not reflected anywhere. Renewal is 2026-11-12. | the next renewal invoice ($3,876/quarter) is at risk |\n| INV-25662 | Upton & Bell (top-50) | 44,064 | late fee after a card outage on our side | **We're right**: 54×68×12 exactly, with no late fee in the ledger. The customer pays by **wire**, not card. | $0 |\n| INV-25711 | Oyelaran Devlin | 2,820 | migration fee should have been waived | **We're right**: 20×47×3 exactly. No migration-fee item exists. | $0 |\n| INV-25539 | Banerjee Petrov | 2,652 | portal fee + setup line | **We're right**: the portal is included in Core/Growth, and 13×68×3 = 2,652. Usage shows the portal still **in use** Jul–Oct. | $0 |\n| INV-25834 | Delacroix, Jessop & Co | 41,568 | 3 seats for leavers | **We're right per contract**: renewed at 28 seats on 09-09, with 23–27 active users. Can't tell whether they asked to reduce. | $3,168 |\n| INV-26009 | Reyes Consulting | 51,072 | — | **FALSE POSITIVE (QA agent is correct).** T880132 (07-15) is about Reyes's own client invoice and predates INV-26009 (issued 10-17). It has no INV reference. The invoice is open and due 11-16. | — |\n\n- Sum of exposure upper bounds if every claim were proven (I): about $28k plus unknown tax lines. That compares with **$309,000** of overdue invoices on hold over these disputes.\n- **I** \"Held → fix\": 9 of the 14 can be rel
… [tool input truncated]
```

### Tool · 2026-11-20 17:43:54 UTC
**Tool result:**
```
File created successfully at: /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/DISCREPANCIES.md (file state is current in your context — no need to Read it back)
```

### Claude ·  UTC
**Tool call:** `Write`
```json
{
 "file_path": "/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis/DISCREPANCIES.md",
 "content": "# DISCREPANCIES — finance review before handover (as of 2026-10-31)\n\nScripts: `analysis/scripts/discrepancies.py`, `analysis/scripts/disp_verify.py`. Per-check CSVs are in `analysis/work/check1..5_*.csv`.\n**F** = fact computed from the data. **I** = inference. `data/` and `app/` were not touched.\n\n## Headline\nThe ledger is internally consistent. Every invoice in the data room (6,062 of 6,062) equals the amount derived from its contract term. AR ties to the balance sheet to the dollar in all 46 months.\n\nThe open question is not \"is our arithmetic wrong\" but **\"what did the customer see on the invoice document?\"** invoices.csv has one amount per invoice, with no line items, no tax and no discounts. None of the disputed extra lines (fees, VAT, late fee, module) exist in the ledger amount. So the evidence finance can send each customer is the contract row and the invoice amount, and an account manager confirms anything verbal.\n\n## 1. The 14 disputes (+ Reyes) — `work/check1_disputes_verdicts.csv`\nMethod (F): for each invoice I took the contract term covering issue_date. Expected amount = contract arr × service_period_months / 12, where arr = seats × price × 12 + platform fee (this formula holds on all 1,757 contract rows). I then checked customers.csv, usage_monthly.csv (seats, active users, modules) and pricing_and_packaging.md.\n\n**F: all 15 invoices equal their contract amount exactly.** Credit due according to the data: **$0 on every invoice.**\n\n| invoice | customer | $ | claim | verdict | exposure if customer proves it (I) |\n|---|---|---|---|---|---|\n| INV-25787 | Riverside Partners | 60,576 | 62 seats vs 38 people | **We're right on the invoice**: it bills 46 seats, not 62. **Can't tell** whether the 39→46 expansion at the 08-27 renewal came from the merge. Usage shows 38 active users in Oct, 43 in Sep. | $7,392 (7 seats) to $8,448 (down to 38) |\n| INV-25712 | Wexler & Hume | 4,080 | billed 24 users, have 17 | **We're right**: the invoice is for 20 seats, not 24. They renewed at 20 on 08-10, and seat reductions are allowed at renewal only. | $816/quarter if cut to 17 |\n| INV-25730 | Westbrook Eng. (top-50) | 47,904 | implementation fee should have been waived | **We're right**: 34×88×12 + 12,000 = 47,904 exactly. The customer has no implementation invoice, the fee applies to new customers only (they have been a customer since 2022), and multi-year deals are not offered. | $0 |\n| INV-25765 | Okafor & Nakamura (top-50) | 46,848 | 50% off 3 months for second office | **Can't tell.** There is no contract change for a second office (33 seats, flat since 2023). A discount over 10% needs the Head of Sales and is first-year only. | ≤ $5,856 |\n| INV-25764 | Castell Eng. | 6,324 | downgraded \"pro→standard\", billed a full month | **We're right per contract**: Growth, 31 seats, until 2027-02-22. No plans called pro or standard exist. The invoice is quarterly (08-23), and the downgrade date (10-03) is after it. After the rewrite, a plan change goes on the *next* invoice. | about $1,070 on the next invoice |\n| INV-25822 | Brandt Ashby IT | 26,112 | moved annual Enterprise→monthly \"Team\" | **We're right on the amount**: the plan is Growth, there is no \"Team\" plan, and the record says annual billing. **Can't verify** the confirmation screen they mention. | $0 revenue. If proven: void and rebill 12 × $2,176 (cash timing only) |\n| INV-25750 | Thackeray Accounting | 7,896 | 20% VAT added, should be reverse charge | **Can't tell**: tax is excluded from all amounts in the data. The base amount is correct. The customer record says **United States**, so a VAT reverse charge is implausible: either the master record or the tax engine is wrong. | tax line only (about $1,579 if 20% was charged) |\n| INV-25757 | Ellery Consulting | 13,056 | sales tax on old address | **Can't tell** (tax not in data). Base amount is correct. | rate difference only |\n| INV-25811 | Wexler Media | 1,224 | 15% multi-year discount | **We're right**: pricing says multi-year discounts are not offered, they renewed at list price, and they are billed monthly, not annually. | $183.60/month if an AM overrode policy |\n| INV-25718 | Mercer & Banerjee | 3,876 | time-tracking module cancelled | **We're right**: there are no priced modules, and 19×68×3 = 3,876. **Separate risk:** termination notice T880514 (\"discontinuing… effect from 30 June\", Billing, solved) is not reflected anywhere. Renewal is 2026-11-12. | the next renewal invoice ($3,876/quarter) is at risk |\n| INV-25662 | Upton & Bell (top-50) | 44,064 | late fee after a card outage on our side | **We're right**: 54×68×12 exactly, with no late fee in the ledger. The customer pays by **wire**, not card. | $0 |\n| INV-25711 | Oyelaran Devlin | 2,820 | migration fee should have been waived | **We're right**: 20×47×3 exactly. No migration-fee item exists. | $0 |\n| INV-25539 | Banerjee Petrov | 2,652 | portal fee + setup line | **We're right**: the portal is included in Core/Growth, and 13×68×3 = 2,652. Usage shows the portal still **in use** Jul–Oct. | $0 |\n| INV-25834 | Delacroix, Jessop & Co | 41,568 | 3 seats for leavers | **We're right per contract**: renewed at 28 seats on 09-09, with 23–27 active users. Can't tell whether they asked to reduce. | $3,168 |\n| INV-26009 | Reyes Consulting | 51,072 | — | **FALSE POSITIVE (QA agent is correct).** T880132 (07-15) is about Reyes's own client invoice and predates INV-26009 (issued 10-17). It has no INV reference. The invoice is open and due 11-16. | — |\n\n- Sum of exposure upper bounds if every claim were proven (I): about $28k plus unknown tax lines. That compares with **$309,000** of overdue invoices on hold over these disputes.\n- **I** \"Held → fix\": 9 of the 14 can be rel
… [tool input truncated]
```

### Claude · 2026-11-20 17:44:01 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -i '' 's/about \\$28k plus unknown tax lines/about $25k, including a $1.6k VAT estimate but not Ellery'\"'\"'s unknown tax difference/' \"$R/analysis/DISCREPANCIES.md\"; grep -n \"about \\$25k\" \"$R/analysis/DISCREPANCIES.md\"; ls \"$R/analysis/work\"",
 "description": "Correct exposure total and list outputs"
}
```

### Tool · 2026-11-20 17:44:02 UTC
**Tool result:**
```
check1_disputes_verdicts.csv
check2_ar_tieout.csv
check3_cross_customer.csv
check3_post_churn_invoices.csv
check4_writeoffs.csv
check5_contract_vs_invoice_all.csv
check5_contract_vs_invoice_open.csv
eval_cash_app.log
eval_cash_app_results.csv
eval_controller.log
eval_guardrails.log
eval_guardrails_results.csv
eval_ticket_reads.csv
eval_ticket_sample_flagged.csv
eval_ticket_sample_notflagged.csv
open_ar_flags.csv
overdue_by_quarter.csv
tickets_flags.csv
tickets_invoice_refs.csv
tickets_themes.csv
unapplied_matches.csv
[This command modified 1 file you've previously read: analysis/DISCREPANCIES.md. Call Read before editing.]
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; sed -i '' 's/about \\$28k plus unknown tax lines/about $25k, including a $1.6k VAT estimate but not Ellery'\"'\"'s unknown tax difference/' \"$R/analysis/DISCREPANCIES.md\"; grep -n \"about \\$25k\" \"$R/analysis/DISCREPANCIES.md\"; ls \"$R/analysis/work\"",
 "description": "Correct exposure total and list outputs"
}
```

### Claude · 2026-11-20 17:44:07 UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; grep -n \"28k\\|25k\" \"$R/analysis/DISCREPANCIES.md\"",
 "description": "Check exposure line text"
}
```

### Tool · 2026-11-20 17:44:07 UTC
**Tool result:**
```
34:- Sum of exposure upper bounds if every claim were proven (I): about $25k, including a $1.6k VAT estimate but not Ellery's unknown tax difference. That compares with **$309,000** of overdue invoices on hold over these disputes.
```

### Claude ·  UTC
**Tool call:** `Bash`
```json
{
 "command": "R=\"/Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a\"; grep -n \"28k\\|25k\" \"$R/analysis/DISCREPANCIES.md\"",
 "description": "Check exposure line text"
}
```

### Claude · 2026-11-20 17:44:21 UTC
**Tool call:** `SubagentHandback`
```json
{
 "message": "The discrepancy review is written up in DISCREPANCIES.md, with one CSV per check. The ledger's arithmetic is clean. The real gap: invoices.csv holds only one total per invoice — no line items, tax, discounts, credit notes or refunds — so we can't see what the customer actually saw on the invoice.\n\n1. **Disputes:** all 14 invoices (plus Reyes) equal their contract amount (seats × price × 12 + platform fee, × period/12). Per the data, credit due is $0 on every one.\n   - **We're right (9):** Westbrook (customer since 2022, no implementation invoice exists), Upton & Bell (no late fee in the amount, and they pay by wire, not card), Wexler & Hume (billed for 20 seats, not the 24 they claim), Wexler Media (multi-year discounts aren't offered), Castell, Oyelaran, Banerjee Petrov, Mercer, Delacroix. These can be released with a contract-evidence reply.\n   - **Can't tell (5), each needs one account-manager or tax decision:** Riverside (invoice is for 46 seats, not 62; exposure $7.4–8.4k if the 39→46 renewal expansion came from the merge), Okafor & Nakamura (verbal discount, up to $5.9k), Thackeray (VAT; customer master says US), Ellery (sales tax), Brandt Ashby (billing frequency; cash timing only).\n   - **Reyes is a false positive:** the ticket is about their own client's invoice and predates INV-26009.\n   - Total exposure if every claim were proven is about $25k, against $309k of overdue invoices held over these disputes.\n   - Several claims contradict our own records (plan names that don't exist, wrong payment method, wrong country). Pull one invoice PDF (e.g. INV-25730) before Monday to check whether the PDFs and the data room agree.\n2. **AR tie-out:** ar_aging = open invoices = balance sheet AR = $1,430,632. The balance sheet carries $87,335 of unapplied cash separately as a liability, which equals the 7 unapplied payments. AR and unapplied cash both tie to the dollar in all 46 months; net receivable is $1,343,297.\n3. **Overpayments, duplicates, cross-customer:** none found, and no billing after churn. Three tickets mention refunds or double charges, but there are no refund records to check them against.\n4. **Write-offs:** 144 card write-offs ($159,192), all at exactly 150 days; no non-card write-offs. Nine were over the $2k VP Finance limit ($47,251), the largest Ellery Legal at $17,520; 8 of those customers are still active. Eastman Engineering's current $3,264 failed invoice is heading the same way.\n5. **Contract vs invoice:** 0 of the 117 open invoices mismatch, and 0 of all 6,062, before or after the rewrite (all whole dollars). The rewrite leaves no trace in our own invoices, so don't tell Priya it caused AR disputes. Minor exception: 23 contract terms are below the plan's minimum seats.\n\nOne item outside the brief: Mercer & Banerjee sent a termination notice (T880514) that isn't reflected anywhere, and their renewal is 2026-11-12.\n\nFiles are in /Users/jacekmaterna/Library/Application Support/Claude/scratch-workspaces/e69441d8-02c7-4ae1-82fa-e65f61df0516/362a2cee-265f-40fd-99ca-8b843a81ad27/scratch-2026-11-20-a3ea2a/analysis:\n- DISCREPANCIES.md\n- work/check1_disputes_verdicts.csv\n- work/check2_ar_tieout.csv\n- work/check3_cross_customer.csv\n- work/check3_post_churn_invoices.csv\n- work/check4_writeoffs.csv\n- work/check5_contract_vs_invoice_open.csv\n- work/check5_contract_vs_invoice_all.csv"
}
```

### Tool · 2026-11-20 17:44:21 UTC
**Tool result:**
```
{"success":true,"message":"Report delivered to your caller."}
```
