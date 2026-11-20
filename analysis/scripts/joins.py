import sys, os, re, pandas as pd
D = sys.argv[1]
r = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)
inv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv')
cus=r('customers/customers.csv'); con=r('customers/contacts.csv'); ctr=r('customers/contracts.csv')
tk=r('support/tickets.csv'); nps=r('support/nps_responses.csv'); us=r('product/usage_monthly.csv'); opp=r('sales/opportunities.csv')
cid=set(cus.customer_id); name=dict(zip(cus.customer_id,cus.name))
def rate(lbl, s, ref):
    s=s[s!='']; miss=(~s.isin(ref)).sum(); print(f"{lbl}: n={len(s)} missing={miss} ({miss/len(s):.2%})")
def namedrift(lbl, df, idc, nc):
    m=df[df[idc].isin(cid)]; d=m[m[nc]!=m[idc].map(name)]
    print(f"{lbl} name!=customers.name: {len(d)}/{len(m)} rows, {d[idc].nunique()} customers")
    print(d[[idc,nc]].drop_duplicates().assign(master=lambda x:x[idc].map(name)).head(8).to_string())
rate('invoices.customer_id->customers', inv.customer_id, cid); namedrift('invoices',inv,'customer_id','customer_name')
rate('ar_aging.invoice_id->invoices', ar.invoice_id, set(inv.invoice_id)); rate('ar_aging.customer_id->customers', ar.customer_id, cid); namedrift('ar_aging',ar,'customer_id','customer_name')
rate('payments.invoice_id->invoices', pay.invoice_id, set(inv.invoice_id))
print('payments invoice_id dup:', pay[pay.invoice_id!=''].invoice_id.duplicated().sum())
# payer name vs invoice customer
p=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amount','status','payment_method']],on='invoice_id',how='left',suffixes=('','_inv'))
pm=p[p.payer_name!=p.customer_name]
print(f"payer_name != invoice customer_name: {len(pm)}/{len(p)} ({len(pm)/len(p):.1%})")
print(pm[['payer_name','customer_name','method']].sample(15,random_state=1).to_string())
print('payer_name exact match to any customers.name:', pay.payer_name.isin(set(cus.name)).mean())
rate('contacts.customer_id', con.customer_id, cid); rate('contracts.customer_id', ctr.customer_id, cid)
rate('tickets.customer_id', tk.customer_id, cid); namedrift('tickets',tk,'customer_id','customer_name')
rate('nps.customer_id', nps.customer_id, cid); rate('usage.customer_id', us.customer_id, cid)
rate('opps.customer_id', opp.customer_id, cid); namedrift('opps',opp,'customer_id','account_name')
# email domain vs website
dom=lambda e: e.split('@')[-1].lower()
web=dict(zip(cus.customer_id,cus.website.str.lower()))
con['dom_ok']=[dom(e)==web.get(c) for e,c in zip(con.email,con.customer_id)]
print('contacts domain != website:', (~con.dom_ok).sum(), con[~con.dom_ok][['customer_id','email','role','status']].head(10).to_string())
tk['dom_ok']=[dom(e)==web.get(c) for e,c in zip(tk.requester_email,tk.customer_id)]
print('tickets requester domain != website:', (~tk.dom_ok).sum(), tk[~tk.dom_ok][['customer_id','requester_email']].head(5).to_string())
# billing contacts per customer
bill=con[con.role.str.contains('billing',case=False)]
print('customers with no billing contact:', len(cid-set(bill.customer_id)))
print('customers whose all billing contacts left:', (bill.groupby('customer_id').status.apply(lambda s:(s!='active').all())).sum())
# memo patterns
print(pay.memo.str.replace(r'\d','#',regex=True).value_counts().head(40).to_string())
print(pay[pay.invoice_id==''].to_string())
