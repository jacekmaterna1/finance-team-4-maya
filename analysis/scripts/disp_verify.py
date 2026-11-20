import sys, os, pandas as pd
D=sys.argv[1]
r=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)
inv=r('finance/invoices.csv'); ctr=r('customers/contracts.csv'); cus=r('customers/customers.csv'); us=r('product/usage_monthly.csv'); tk=r('support/tickets.csv'); con=r('customers/contacts.csv')
ids=['INV-25539','INV-25662','INV-25718','INV-25711','INV-25757','INV-25730','INV-25712','INV-25765','INV-25764','INV-25750','INV-25787','INV-25811','INV-25822','INV-25834','INV-26009']
for i in ids:
    v=inv[inv.invoice_id==i].iloc[0]; c=v.customer_id
    print('\n=====',i,c,v.customer_name,v.type,v.issue_date,'due',v.due_date,'period',v.service_period_months,'amt',v.amount,v.status,v.payment_method)
    cu=cus[cus.customer_id==c].iloc[0]; print('  customer:',cu.plan,cu.status,cu.billing_frequency,cu.payment_method,'seats',cu.current_seats,'arr',cu.current_arr,'renew',cu.renewal_date,'signup',cu.signup_date,'country',cu.country,'AM',cu.account_manager)
    print(ctr[ctr.customer_id==c].tail(4).to_string(index=False))
    print(inv[(inv.customer_id==c)&(inv.issue_date>='2025-06-01')][['invoice_id','type','issue_date','service_period_months','amount','status','paid_date']].to_string(index=False))
    u=us[us.customer_id==c].tail(4); print(u[['month','seats_licensed','active_users','uses_retainers','uses_milestones','uses_client_portal']].to_string(index=False))
    for _,t in tk[tk.customer_id==c].iterrows():
        print(f'  T {t.ticket_id} {t.created_at} {t.category}/{t.status} | {t.subject} | {t.body[:200]!r}')
