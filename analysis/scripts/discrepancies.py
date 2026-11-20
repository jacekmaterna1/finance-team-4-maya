import sys, os, re, pandas as pd, numpy as np
D=sys.argv[1]; W=sys.argv[2]
r=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)
inv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); ctr=r('customers/contracts.csv'); cus=r('customers/customers.csv'); bs=r('finance/balance_sheet_monthly.csv'); ar=r('finance/ar_aging.csv')
inv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float); ar['amt']=ar.amount.astype(float)
for c in ['seats','price_per_seat_per_month','platform_fee','arr']: ctr[c]=ctr[c].astype(int)

# ---- 5 / 1: contract vs invoice amount, all invoices
ctr_s=ctr.sort_values(['customer_id','term_start'])
def term_for(c,d):
    t=ctr_s[(ctr_s.customer_id==c)&(ctr_s.term_start<=d)&(ctr_s.term_end>=d)]
    return t.iloc[-1] if len(t) else None
rows=[]
for _,v in inv.iterrows():
    t=term_for(v.customer_id,v.issue_date)
    if t is None: rows.append(dict(invoice_id=v.invoice_id,term_start='',expected=np.nan)); continue
    calc_arr=t.seats*t.price_per_seat_per_month*12+t.platform_fee
    if v.type=='subscription': exp=round(t.arr*int(v.service_period_months)/12,2)
    else: exp={'Core':0,'Growth':2500,'Enterprise':8000}[t.plan]
    rows.append(dict(invoice_id=v.invoice_id,term_start=t.term_start,plan=t.plan,seats=t.seats,price=t.price_per_seat_per_month,platform_fee=t.platform_fee,contract_arr=t.arr,arr_formula_ok=calc_arr==t.arr,expected=exp))
cm=inv.merge(pd.DataFrame(rows),on='invoice_id',how='left')
cm['diff']=(cm.amt-cm.expected).round(2)
cm['post_rewrite']=cm.issue_date>='2026-03-16'
print('no covering contract term:', cm.expected.isna().sum()); print(cm[cm.expected.isna()][['invoice_id','customer_id','issue_date','type','amt','status']].head(10).to_string())
print('arr formula mismatches in contracts:', (~cm.arr_formula_ok.fillna(True).astype(bool)).sum(), ' contract rows w/ arr!=formula:', (ctr.seats*ctr.price_per_seat_per_month*12+ctr.platform_fee!=ctr.arr).sum())
mm=cm[cm['diff'].fillna(0)!=0]
print('invoice != contract-derived amount:', len(mm), 'of', cm.expected.notna().sum()); print(pd.crosstab(mm.type,mm.post_rewrite))
print(mm[['invoice_id','customer_id','customer_name','type','issue_date','service_period_months','amt','expected','diff','status','plan','seats','price']].head(40).to_string())
op=cm[cm.status.isin(['open','overdue','payment_failed'])]
print('OPEN invoices mismatching contract:', (op['diff'].fillna(0)!=0).sum(), 'of', len(op), ' no term:', op.expected.isna().sum())
cm.drop(columns=[]).to_csv(os.path.join(W,'check5_contract_vs_invoice_all.csv'),index=False)
op.to_csv(os.path.join(W,'check5_contract_vs_invoice_open.csv'),index=False)
# price list check on terms post-2025
late=ctr[(ctr.term_start>='2025-01-01')]
pl={'Core':47,'Growth':68,'Enterprise':88}
bad=late[late.price_per_seat_per_month!=late.plan.map(pl)]
print('2025+ contract terms not on 2025 price list:', len(bad), bad.change_type.value_counts().to_dict())
mins={'Core':8,'Growth':12,'Enterprise':20}
print('terms below min seats:', (ctr.seats<ctr.plan.map(mins)).sum())
# implementation invoices: for new customers only?
imp=cm[cm.type=='implementation']
print('implementation invoices', len(imp), imp.amt.value_counts().to_dict(), 'diff!=0', (imp['diff']!=0).sum())

# ---- 2: AR tie-out monthly
p=pay[pay.invoice_id!=''].set_index('invoice_id')
inv['applied']=inv.invoice_id.map(p.applied_date); inv.loc[inv.status=='written_off','applied']=inv.paid_date; inv['applied']=inv.applied.fillna('9999')
out=[]
for _,b in bs.iterrows():
    me=(pd.Period(b.month)).end_time.strftime('%Y-%m-%d')
    o=inv[(inv.issue_date<=me)&(inv.applied>me)].amt.sum()
    un=pay[(pay.received_date<=me)&((pay.applied_date>me)|(pay.applied_date==''))].amt.sum()
    out.append(dict(month=b.month,bs_ar=float(b.accounts_receivable),ledger_open_ar=o,ar_diff=float(b.accounts_receivable)-o,bs_unapplied=float(b.unapplied_cash_receipts),recon_unapplied=un,unapplied_diff=float(b.unapplied_cash_receipts)-un))
tie=pd.DataFrame(out); print(tie.tail(8).to_string()); print('months with AR diff:', (tie.ar_diff.abs()>0.5).sum(), 'unapplied diff:', (tie.unapplied_diff.abs()>0.5).sum(), 'of', len(tie))
print(tie[(tie.ar_diff.abs()>0.5)|(tie.unapplied_diff.abs()>0.5)].to_string())
tie.to_csv(os.path.join(W,'check2_ar_tieout.csv'),index=False)
print('asof: ar_aging', ar.amt.sum(), 'invoices open', inv[inv.status.isin(['open','overdue','payment_failed'])].amt.sum(), 'bs', bs.iloc[-1].accounts_receivable, 'unapplied', pay[pay.invoice_id==''].amt.sum())

# ---- 3: overpay / duplicates / cross-customer
pm=pay[pay.invoice_id!=''].merge(inv[['invoice_id','customer_id','customer_name','amt','issue_date']],on='invoice_id',suffixes=('','_inv'))
print('over/under payments:', (pm.amt!=pm.amt_inv).sum())
print('payment before invoice issue:', (pm.received_date<pm.issue_date).sum())
dup=pay[pay.duplicated(['payer_name','amount','received_date'],keep=False)]
print('dup (payer,amount,date):', len(dup)); print(dup.head(10).to_string())
dup2=pay[pay.duplicated(['payer_name','amount','memo'],keep=False)&(pay.memo.str.contains(r'\d{5}'))]
print('dup (payer,amount,memo w/ inv ref):', len(dup2))
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower()); cn=dict(zip(cus.name.map(norm),cus.customer_id))
pm['payer_exact_cid']=pm.payer_name.map(lambda x: cn.get(norm(x),''))
cross=pm[(pm.payer_exact_cid!='')&(pm.payer_exact_cid!=pm.customer_id)]
print('payer name exactly = a DIFFERENT customer than invoice:', len(cross)); print(cross[['payment_id','payer_name','payer_exact_cid','invoice_id','customer_id','customer_name','amt']].head(20).to_string())
pm['payer_prefix_ok']=[norm(c).startswith(norm(p_)) for p_,c in zip(pm.payer_name,pm.customer_name)]
print('payer not a prefix of invoice customer name:', (~pm.payer_prefix_ok).sum())
# truncated payer that equals a different customer's full name
pd.concat([cross.assign(issue='payer_is_other_customer'), pm[~pm.payer_prefix_ok].assign(issue='payer_not_prefix')]).to_csv(os.path.join(W,'check3_cross_customer.csv'),index=False)
# post-churn billing
cus_ch=cus[cus.churn_date!=''].set_index('customer_id').churn_date
ic=inv[inv.customer_id.isin(cus_ch.index)].copy(); ic['churn']=ic.customer_id.map(cus_ch)
pc=ic[ic.issue_date>=ic.churn]; print('invoices issued on/after churn date:', len(pc), pc.amt.sum(), pc.status.value_counts().to_dict())
# service period extends past churn (credit owed?)
ic['end']=(pd.to_datetime(ic.issue_date)+pd.to_timedelta(ic.service_period_months.astype(int)*30.4,unit='D'))
ov=ic[(ic.issue_date<ic.churn)&(ic.end>pd.to_datetime(ic.churn)+pd.Timedelta(days=31))]
print('invoices whose service period runs >1 month past churn:', len(ov), ov.amt.sum())
pc.to_csv(os.path.join(W,'check3_post_churn_invoices.csv'),index=False)
# active customers with open invoices but churned
print('open AR on churned customers:', inv[inv.status.isin(['open','overdue','payment_failed'])&inv.customer_id.isin(cus_ch.index)].shape[0])

# ---- 4: write-offs
wo=inv[inv.status=='written_off'].copy(); wo['days_to_wo']=(pd.to_datetime(wo.paid_date)-pd.to_datetime(wo.issue_date)).dt.days
print('write-offs by method:', wo.payment_method.value_counts().to_dict(), 'days_to_wo', wo.days_to_wo.unique())
big=wo[wo.amt>2000].sort_values('paid_date'); print(big[['invoice_id','customer_id','customer_name','issue_date','paid_date','amt','service_period_months']].to_string())
cs=dict(zip(cus.customer_id,cus.status)); big=big.assign(customer_status=big.customer_id.map(cs))
print('big wo customer status:', big.customer_status.value_counts().to_dict())
wo.assign(over_2k=wo.amt>2000,customer_status=wo.customer_id.map(cs)).to_csv(os.path.join(W,'check4_writeoffs.csv'),index=False)
print('wo by year >2k:', big.groupby(big.paid_date.str[:4]).amt.agg(['count','sum']).to_dict())
