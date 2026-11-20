import sys, os, re, pandas as pd, numpy as np
D = sys.argv[1]; OUT = sys.argv[2]
r = lambda p: pd.read_csv(os.path.join(D,p), dtype=str, keep_default_na=False)
inv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ar=r('finance/ar_aging.csv'); cus=r('customers/customers.csv')
con=r('customers/contacts.csv'); tk=r('support/tickets.csv')
inv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float)
for c in ['issue_date','due_date','paid_date']: inv[c+'_d']=pd.to_datetime(inv[c].replace('',None))
for c in ['received_date','applied_date']: pay[c+'_d']=pd.to_datetime(pay[c].replace('',None))
ASOF=pd.Timestamp('2026-10-31')
cus['arr']=cus.current_arr.astype(float)
top50=set(cus.sort_values('arr',ascending=False).head(50).customer_id)
print('top50 ARR cutoff:', cus.sort_values('arr',ascending=False).arr.iloc[49], 'ties at cutoff:', (cus.arr==cus.sort_values('arr',ascending=False).arr.iloc[49]).sum())
print('cents amounts in invoices:', (inv.amt%1!=0).sum(), ' in payments:', (pay.amt%1!=0).sum())

# ---------- quarter-end overdue reconstruction
p=pay[pay.invoice_id!=''][['invoice_id','received_date_d','applied_date_d']]
iv=inv.merge(p,on='invoice_id',how='left')
iv['wo_d']=np.where(iv.status=='written_off',iv.paid_date_d,pd.NaT); iv['wo_d']=pd.to_datetime(iv.wo_d)
iv['settle_ledger']=iv.applied_date_d.fillna(iv.wo_d)   # ledger closes when applied or written off
iv['settle_cash']=iv.received_date_d.fillna(iv.wo_d)
qs=['2025-06-30','2025-09-30','2025-12-31','2026-03-31','2026-06-30','2026-09-30','2026-10-31']
rows=[]
for q in qs:
    Q=pd.Timestamp(q)
    issued=iv.issue_date_d<=Q
    for view,col in [('ledger','settle_ledger'),('cash','settle_cash')]:
        unpaid=issued&(iv[col].isna()|(iv[col]>Q))
        od=unpaid&(iv.due_date_d<Q)
        rows.append(dict(quarter_end=q,view=view,open_ar_usd=iv[unpaid].amt.sum(),overdue_n=od.sum(),overdue_usd=iv[od].amt.sum(),
             overdue_gt30_usd=iv[od&(iv.due_date_d<Q-pd.Timedelta(days=30))].amt.sum(),
             overdue_pct_of_open=round(100*iv[od].amt.sum()/max(iv[unpaid].amt.sum(),1),1)))
qt=pd.DataFrame(rows); print(qt.to_string()); qt.to_csv(os.path.join(OUT,'overdue_by_quarter.csv'),index=False)

# ---------- historical "chased for money we had" (cash received but not applied at reminder date)
h=iv[iv.received_date_d.notna()&iv.payment_method.isin(['ach','wire','check'])].copy()
h['recv_late']=h.received_date_d>h.due_date_d
h['ledger_late']=h.applied_date_d>h.due_date_d
for k in [7,21,45]:
    R=h.due_date_d+pd.Timedelta(days=k)
    h[f'chased_paid_{k}']=(h.received_date_d<=R)&(h.applied_date_d>R)
print('bank invoices paid:',len(h),'ontime cash but ledger late:',((~h.recv_late)&h.ledger_late).sum(), h[(~h.recv_late)&h.ledger_late].amt.sum())
for k in [7,21,45]:
    s=h[h[f'chased_paid_{k}']]; print(f'reminder +{k}: would have chased already-received cash: n={len(s)} usd={s.amt.sum()}')
anyc=h[h.chased_paid_7|h.chased_paid_21|h.chased_paid_45]
print('any reminder on received cash: n',len(anyc),'usd',anyc.amt.sum(), 'last 12m n', (anyc.due_date_d>=ASOF-pd.Timedelta(days=365)).sum(), anyc[anyc.due_date_d>=ASOF-pd.Timedelta(days=365)].amt.sum())
# lag by year
h['lag']=(h.applied_date_d-h.received_date_d).dt.days
print(h.groupby([h.received_date_d.dt.year,'payment_method']).lag.mean().unstack().round(1))

# ---------- open AR detail with flags
op=inv[inv.status.isin(['open','overdue','payment_failed'])].copy()
op['dpd']=(ASOF-op.due_date_d).dt.days
op['top50']=op.customer_id.isin(top50)
op['arr']=op.customer_id.map(dict(zip(cus.customer_id,cus.arr)))
op['account_manager']=op.customer_id.map(dict(zip(cus.customer_id,cus.account_manager)))
# unapplied receipts matching
un=pay[pay.invoice_id==''].copy()
cusname=dict(zip(cus.customer_id,cus.name))
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
def memo_inv(m): return ['INV-'+i for i in re.findall(r'(?:INV-?|inv|Invoice )\s?(\d{5})',m)]
mrows=[]
for _,u in un.iterrows():
    cands=cus[cus.name.map(norm)==norm(u.payer_name)].customer_id.tolist()
    if not cands: cands=cus[cus.name.map(norm).str.startswith(norm(u.payer_name))].customer_id.tolist()
    oi=op[op.customer_id.isin(cands)&(op.issue_date_d<=u.received_date_d)]
    exact=oi[(oi.amt-u.amt).abs()<0.005]
    mi=memo_inv(u.memo)
    if mi and mi[0] in set(op.invoice_id): match=mi; how='memo invoice ref + amount + payer'
    elif len(exact)==1: match=exact.invoice_id.tolist(); how='payer name + unique exact amount'
    elif len(exact)>1: match=exact.sort_values('due_date').invoice_id.tolist(); how='payer name + exact amount, AMBIGUOUS (several open invoices same amount)'
    else: match=[]; how='no match'
    for m in match:
        o=op[op.invoice_id==m].iloc[0]
        mrows.append(dict(payment_id=u.payment_id,received_date=u.received_date,amount=u.amt,method=u.method,payer_name=u.payer_name,memo=u.memo,
            candidate_invoice=m,customer_id=o.customer_id,customer_name=o.customer_name,inv_status=o.status,due_date=o.due_date,dpd=o.dpd,inv_amount=o.amt,top50=o.top50,how=how,n_candidates=len(match)))
um=pd.DataFrame(mrows); print(um.to_string()); um.to_csv(os.path.join(OUT,'unapplied_matches.csv'),index=False)
op['unapplied_cash_pid']=op.invoice_id.map(um.groupby('candidate_invoice').payment_id.first())

# ---------- tickets
tk['created_d']=pd.to_datetime(tk.created_at)
tk['open']=tk.status.isin(['open','pending'])
tk['recent']=tk.created_d>=ASOF-pd.Timedelta(days=30)
txt=(tk.subject+' '+tk.body).str.lower()
tk['kw_dispute']=txt.str.contains(r'disput|overcharg|wrong amount|incorrect|charged twice|double charg|refund|credit note|not right|doesn.t match|discrepan')
tk['kw_rewrite']=txt.str.contains(r'prorat|rounding|cent|credit note|new version|time zone|timezone|billing engine|since march|retr(y|ies)')
tk['kw_escal']=txt.str.contains(r'escalat|cancel|lawyer|legal|unacceptable|ceo|manager|complain')
tk['kw_paid']=txt.str.contains(r'already paid|we paid|have paid|paid this|paid it|sent the payment|remittance|wire|reminder|chased|chasing|overdue|collections')
tk['kw_card']=txt.str.contains(r'card (was )?declin|card fail|failed payment|payment failed|expired card|update (our|the) card|new card')
print('ticket flags:', tk[['open','recent','kw_dispute','kw_rewrite','kw_escal','kw_paid','kw_card']].sum().to_dict())
print(pd.crosstab(tk.category,tk.kw_dispute))
tk.to_pickle(os.path.join(OUT,'..','analysis_tk.pkl')) if False else None
rel=tk[tk.open|tk.recent]
g=rel.groupby('customer_id').agg(t_n=('ticket_id','count'),t_open=('open','sum'),t_billing=('category',lambda s:(s=='Billing').sum()),
    t_urgent=('priority',lambda s:s.isin(['urgent','high']).sum()),t_dispute=('kw_dispute','sum'),t_paid=('kw_paid','sum'),t_escal=('kw_escal','sum'),
    t_ids=('ticket_id',lambda s:','.join(s)))
op=op.merge(g,left_on='customer_id',right_index=True,how='left')
for c in ['t_n','t_open','t_billing','t_urgent','t_dispute','t_paid','t_escal']: op[c]=op[c].fillna(0).astype(int)
# all-time billing/dispute tickets per customer (window Jul-Oct)
g2=tk.groupby('customer_id').agg(all_billing=('category',lambda s:(s=='Billing').sum()),all_dispute=('kw_dispute','sum'))
op=op.merge(g2,left_on='customer_id',right_index=True,how='left').fillna({'all_billing':0,'all_dispute':0})
# contacts
bill=con[con.role.str.contains('billing',case=False)]
stale=bill[bill.status!='active']
op['stale_billing_contact']=op.customer_id.isin(set(stale.customer_id))
op['active_billing_contacts']=op.customer_id.map(bill[bill.status=='active'].groupby('customer_id').size()).fillna(0).astype(int)
op.drop(columns=[c for c in op.columns if c.endswith('_d')]).to_csv(os.path.join(OUT,'open_ar_flags.csv'),index=False)
od=op[op.dpd>0]
print('\nOVERDUE (dpd>0) n',len(od),'usd',od.amt.sum())
def s(mask,l): x=od[mask]; print(f'{l}: n={len(x)} usd={x.amt.sum():,.0f} customers={x.customer_id.nunique()}')
s(od.t_n>0,'overdue w/ open-or-recent ticket'); s(od.t_open>0,'overdue w/ open ticket'); s(od.t_billing>0,'overdue w/ open/recent Billing ticket')
s(od.t_urgent>0,'overdue w/ open/recent high/urgent ticket'); s(od.t_dispute>0,'overdue w/ open/recent dispute-language ticket'); s(od.t_paid>0,'overdue w/ open/recent ticket mentioning paid/reminder')
s(od.t_escal>0,'overdue w/ escalation language'); s(od.top50,'overdue top50'); s(od.stale_billing_contact,'overdue stale billing contact')
s(od.unapplied_cash_pid.notna(),'overdue with unapplied cash candidate')
s(od.all_billing>0,'overdue w/ any Billing ticket Jul-Oct')
print(od.groupby('status').amt.agg(['count','sum']))
print(od[od.t_n>0][['invoice_id','customer_id','customer_name','status','amt','dpd','top50','t_ids','t_billing','t_dispute','t_paid','t_escal','stale_billing_contact','unapplied_cash_pid']].sort_values('amt',ascending=False).to_string())
print(od[od.top50][['invoice_id','customer_name','amt','dpd','arr','status','t_n']].to_string())
print(od[od.stale_billing_contact][['invoice_id','customer_id','customer_name','amt','dpd','active_billing_contacts']].to_string())
print(stale.merge(od[['customer_id','invoice_id','amt']],on='customer_id')[['customer_id','first_name','last_name','email','role','invoice_id','amt']].to_string())

# ---------- card failures
card=inv[inv.payment_method=='card'].copy()
card['delay']=(card.paid_date_d-card.issue_date_d).dt.days
card['post']=card.issue_date_d>=pd.Timestamp('2026-03-16')
card['outcome']=np.select([card.status=='payment_failed',card.status=='written_off',(card.status=='paid')&(card.delay>0)],['still_failed','written_off','recovered_late'],'paid_on_day')
print(pd.crosstab([card.issue_date_d.dt.year,card.post],card.outcome))
print('recovered delay by post-rewrite:'); print(card[card.outcome=='recovered_late'].groupby('post').delay.describe())
print('write-off delay:', card[card.outcome=='written_off'].delay.describe().to_dict())
pf=card[card.status=='payment_failed'].copy()
pf['days_since']=(ASOF-pf.issue_date_d).dt.days
pf['auto_writeoff_on']=(pf.issue_date_d+pd.Timedelta(days=150)).dt.date
# later card invoices paid on same customer = card works now
later=card[card.status=='paid'].groupby('customer_id').issue_date_d.max()
pf['later_card_invoice_paid']=pf.customer_id.map(later)>pf.issue_date_d
pf['cust_status']=pf.customer_id.map(dict(zip(cus.customer_id,cus.status)))
pf=pf.merge(g,left_on='customer_id',right_index=True,how='left')
print(pf[['invoice_id','customer_id','customer_name','issue_date','amt','days_since','auto_writeoff_on','later_card_invoice_paid','cust_status','t_n','t_ids']].to_string())
print('payment_failed n',len(pf),'usd',pf.amt.sum(),'later paid',pf.later_card_invoice_paid.sum(), pf[pf.later_card_invoice_paid].amt.sum())
wo=card[card.status=='written_off']; later_wo=wo.customer_id.map(later)>wo.issue_date_d
print('written_off card n',len(wo),'usd',wo.amt.sum(),'where customer later paid by card:',later_wo.sum(),wo[later_wo].amt.sum())
print('written off last 12m:', (wo.paid_date_d>=ASOF-pd.Timedelta(days=365)).sum(), wo[wo.paid_date_d>=ASOF-pd.Timedelta(days=365)].amt.sum())
print('non-card written off:', (inv[(inv.status=='written_off')&(inv.payment_method!='card')]).shape[0])
print('written off > 2000:', (wo.amt>2000).sum(), wo[wo.amt>2000].amt.sum())
# card tickets
print(tk[tk.kw_card][['ticket_id','created_at','customer_id','customer_name','category','status','subject']].to_string())
tk.drop(columns=['created_d']).to_csv(os.path.join(OUT,'tickets_flags.csv'),index=False)
