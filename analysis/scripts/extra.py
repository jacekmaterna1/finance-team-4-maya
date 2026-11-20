import sys, os, pandas as pd, numpy as np
A=sys.argv[1]; D=sys.argv[2]
ts=pd.read_csv(os.path.join(A,'testset_cash_app.csv'),dtype=str,keep_default_na=False)
inv=pd.read_csv(os.path.join(D,'finance/invoices.csv'),dtype=str,keep_default_na=False); inv['amt']=inv.amount.astype(float)
pay=pd.read_csv(os.path.join(D,'finance/payments.csv'),dtype=str,keep_default_na=False)
ref=pd.read_csv(os.path.join(A,'work/tickets_invoice_refs.csv'),dtype=str)
print('disputed invoices', ref.invoice_id.nunique(), 'usd', ref.amount.astype(float).sum(), 'ticket status', ref.status.value_counts().to_dict(), 'category', ref.category.fillna('(blank)').value_counts().to_dict())
op=pd.read_csv(os.path.join(A,'work/open_ar_flags.csv'),dtype=str,keep_default_na=False)
d=op[op.invoice_id.isin(ref.invoice_id)]; print('disputed top50', d[d.top50=='True'][['invoice_id','customer_name','amount']].to_string())
# ambiguous historical: did staff apply to oldest?
amb=ts[(ts.label_source.str.startswith('ledger'))&(ts.n_open_same_amount.astype(int)>1)]
iss=dict(zip(inv.invoice_id,inv.issue_date)); cust=dict(zip(inv.invoice_id,inv.customer_id))
res=[]
for _,a in amb.iterrows():
    c=cust[a.true_invoice_ids]; o=inv[(inv.customer_id==c)&(abs(inv.amt-float(a.amount))<.005)&(inv.issue_date<=a.received_date)]
    pa=pay[pay.invoice_id.isin(o.invoice_id)].set_index('invoice_id').applied_date
    o=o[o.invoice_id.map(pa).fillna('9999')>=a.received_date]
    res.append(iss[a.true_invoice_ids]==o.issue_date.min())
print('ambiguous: applied to oldest open', sum(res),'of',len(res))
# monthly overdue (ledger) for seasonality
p=pay[pay.invoice_id!=''].set_index('invoice_id').applied_date
inv['settle']=inv.invoice_id.map(p); inv.loc[inv.status=='written_off','settle']=inv.paid_date; inv['settle']=inv.settle.fillna('9999')
out=[]
for m in pd.date_range('2025-01-31','2026-10-31',freq='M'):
    q=m.strftime('%Y-%m-%d'); od=inv[(inv.issue_date<=q)&(inv.due_date<q)&(inv.settle>q)]
    out.append((q,len(od),od.amt.sum()))
print(pd.DataFrame(out,columns=['month_end','n','usd']).to_string())
# what drives quarter-end spikes: annual invoices issued in quarter's last-60 days
