import sys, os, re, pandas as pd, numpy as np
D = sys.argv[1]
r = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)
inv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv'); cus=r('customers/customers.csv')
inv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float); ar['amt']=ar.amount.astype(float)
# payer name drift classes
p=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amt','issue_date','due_date','status','paid_date','payment_method']],on='invoice_id',suffixes=('','_inv'))
def cls(a,b):
    if a==b: return 'exact'
    if a==b.upper(): return 'uppercase'
    if b.lower().startswith(a.lower()): return 'truncated'
    if a.lower() in b.lower(): return 'substring'
    return 'other'
p['ncls']=[cls(a,b) for a,b in zip(p.payer_name,p.customer_name)]
print(p.ncls.value_counts()); print(p[p.ncls=='other'][['payer_name','customer_name']].drop_duplicates().head(30).to_string())
print(pd.crosstab(p.ncls,p.method))
# amount diffs
p['diff']=(p.amt-p.amt_inv).round(2)
print('amount diff distribution:'); print(p['diff'].value_counts().head(25))
print(p[p['diff']!=0][['payment_id','received_date','amt','amt_inv','diff','method','memo','invoice_id']].head(40).to_string())
# method mismatch
print('method mismatch:', (p.method!=p.payment_method).sum())
# memo referencing invoice id vs applied
def memo_inv(m):
    x=re.findall(r'(?:INV-?|inv|Invoice )\s?(\d{5})',m); return ['INV-'+i for i in x]
p['memo_inv']=p.memo.map(memo_inv)
p['memo_n']=p.memo_inv.map(len)
p['memo_ok']=[ (i in l) if l else None for i,l in zip(p.invoice_id,p.memo_inv)]
print('memo refs count:', p.memo_n.value_counts().to_dict()); print('memo ref equals applied:', p.memo_ok.value_counts(dropna=False).to_dict())
print(p[p.memo_ok==False][['payment_id','received_date','amt','amt_inv','memo','invoice_id','customer_name','payer_name']].head(30).to_string())
# lag
p['lag']=(pd.to_datetime(p.applied_date)-pd.to_datetime(p.received_date)).dt.days
print('apply lag by method:'); print(p.groupby('method').lag.describe())
p['pd_vs_applied']=(p.paid_date==p.applied_date)
print('invoice paid_date == applied_date:', p.pd_vs_applied.mean(), ' paid_date==received:', (p.paid_date==p.received_date).mean())
# statuses of invoices that have payments
print(p.status.value_counts())
# recent applied after as-of?
print('applied after 2026-10-31:', (p.applied_date>'2026-10-31').sum(), 'received after:', (pay.received_date>'2026-10-31').sum())
print('max dates', pay.received_date.max(), pay.applied_date.max(), inv.issue_date.max())
# open invoices
op=inv[inv.status.isin(['open','overdue','payment_failed'])]
print(op.groupby(['status','payment_method']).amt.agg(['count','sum']))
m=ar.merge(inv,on='invoice_id',suffixes=('_ar','_inv'))
for c in ['customer_id','issue_date','due_date','status']:
    print(c,'disagree', (m[c+'_ar']!=m[c+'_inv']).sum())
print('amount disagree', (m.amt_ar!=m.amt_inv).sum())
print('open in invoices not in ar:', len(set(op.invoice_id)-set(ar.invoice_id)), 'ar not open in invoices:', len(set(ar.invoice_id)-set(op.invoice_id)))
# days past due recompute
asof=pd.Timestamp('2026-10-31')
m['dpd_calc']=(asof-pd.to_datetime(m.due_date_inv)).dt.days
print('dpd disagree', (m.dpd_calc!=m.days_past_due.astype(int)).sum()); print(m[m.dpd_calc!=m.days_past_due.astype(int)][['invoice_id','due_date_inv','days_past_due','dpd_calc','bucket']].head(20).to_string())
def bk(d): return 'Not yet due' if d<=0 else '1-30 days' if d<=30 else '31-60 days' if d<=60 else '61-90 days' if d<=90 else 'Over 90 days'
m['bk_calc']=m.dpd_calc.map(bk); print('bucket disagree', (m.bk_calc!=m.bucket).sum()); print(m[m.bk_calc!=m.bucket][['invoice_id','due_date_inv','days_past_due','dpd_calc','bucket','bk_calc','status_ar']].to_string())
# status vs due
print(pd.crosstab(m.status_ar,m.bk_calc))
print(ar.groupby('bucket').amt.agg(['count','sum'])); print('total', ar.amt.sum())
# due date = issue +30 check
inv['dd']=(pd.to_datetime(inv.due_date)-pd.to_datetime(inv.issue_date)).dt.days
print(pd.crosstab(inv.dd, inv.payment_method))
print(pd.crosstab(inv.dd, inv.issue_date>='2026-03-16'))
# written off
wo=inv[inv.status=='written_off']; print('written off', len(wo), wo.amt.sum()); print(wo.groupby([wo.payment_method, wo.issue_date.str[:4]]).amt.agg(['count','sum']))
print(wo[wo.paid_date!=''].head())
# pay after write-off? payments against written off
print('payments to written_off invoices', (p.status=='written_off').sum())
# unapplied
un=pay[pay.invoice_id=='']
for _,u in un.iterrows():
    print('\nUNAPPLIED',u.payment_id,u.received_date,u.amt,u.method,u.payer_name,'|',u.memo)
    key=u.payer_name.lower().split()[0].strip(',')
    c=cus[cus.name.str.lower().str.contains(re.escape(key))]
    print(c[['customer_id','name','payment_method','current_arr','billing_frequency']].to_string())
    print(inv[inv.customer_id.isin(c.customer_id)&(inv.issue_date>='2026-01-01')][['invoice_id','customer_id','issue_date','due_date','amt','status','paid_date','payment_method']].to_string())
