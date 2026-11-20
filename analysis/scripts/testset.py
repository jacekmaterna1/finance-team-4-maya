import sys, os, re, pandas as pd, numpy as np
D=sys.argv[1]; OUT=sys.argv[2]
r=lambda p: pd.read_csv(os.path.join(D,p),dtype=str,keep_default_na=False)
inv=r('finance/invoices.csv'); pay=r('finance/payments.csv'); cus=r('customers/customers.csv')
inv['amt']=inv.amount.astype(float); pay['amt']=pay.amount.astype(float)
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
cus['n']=cus.name.map(norm)
def cand_customers(payer):
    n=norm(payer); ex=cus[cus.n==n].customer_id.tolist()
    return ex if ex else cus[cus.n.str.startswith(n)].customer_id.tolist()
memo_inv=lambda m: ['INV-'+i for i in re.findall(r'(?:INV-?|inv|Invoice )\s?(\d{5})',m)]
# settlement date of each invoice in ledger (applied date or write-off date)
ap=pay[pay.invoice_id!=''].set_index('invoice_id').applied_date
inv['settle']=inv.invoice_id.map(ap)
inv.loc[inv.status=='written_off','settle']=inv.paid_date
inv['settle']=inv.settle.replace('', '9999-12-31').fillna('9999-12-31')
byc={c:g for c,g in inv.groupby('customer_id')}
rows=[]
for _,p in pay.iterrows():
    cc=cand_customers(p.payer_name)
    openinv=pd.concat([byc[c] for c in cc]) if cc else inv.iloc[:0]
    openinv=openinv[(openinv.issue_date<=p.received_date)&(openinv.settle>=p.received_date)]
    same_amt=openinv[(openinv.amt-p.amt).abs()<0.005]
    refs=memo_inv(p.memo)
    exact_name=bool(cus.n.eq(norm(p.payer_name)).any())
    reasons=[]
    if p.method=='card': diff='trivial'; reasons.append('Stripe charge memo carries invoice id')
    elif refs: diff='easy'; reasons.append('memo references invoice number')
    else:
        reasons.append('no invoice ref in memo')
        if not exact_name: reasons.append(f'payer name drift ({len(cc)} candidate customers)')
        if len(same_amt)==1 and len(cc)==1: diff='medium'; reasons.append('unique open invoice with exact amount')
        elif len(same_amt)==1: diff='hard'; reasons.append('amount unique across candidate customers')
        elif len(same_amt)>1: diff='hard'; reasons.append(f'{len(same_amt)} open invoices with same amount')
        else: diff='hard'; reasons.append('no open invoice with exact amount at receipt (check data)')
        if p.payer_name==p.payer_name.upper() and p.payer_name!=p.payer_name.title(): reasons.append('uppercase payer name')
    rows.append(dict(payment_id=p.payment_id,received_date=p.received_date,amount=p.amount,method=p.method,payer_name=p.payer_name,memo=p.memo,
        true_invoice_ids=p.invoice_id,n_candidate_customers=len(cc),n_open_same_amount=len(same_amt),difficulty=diff,difficulty_reason='; '.join(reasons)))
t=pd.DataFrame(rows)
print(pd.crosstab(t.difficulty,t.method)); print(t[t.method!='card'].groupby('difficulty').n_open_same_amount.value_counts())
hist=t[t.true_invoice_ids!=''].copy(); hist['label_source']='ledger_applied (payments.invoice_id, confirmed by staff)'
# unapplied: inferred labels
inferred={'PAY-65750':('INV-25784','inferred: payer name exact + unique exact amount among open invoices','medium'),
 'PAY-65766':('INV-25806','inferred: uppercase payer name + unique exact amount; memo generic','medium'),
 'PAY-65796':('INV-25951','inferred: uppercase payer + unique exact amount (implementation fee, not yet due); blank memo','medium'),
 'PAY-65805':('INV-25469|INV-25852','inferred AMBIGUOUS: two overdue invoices of 5100.00; oldest-first convention says INV-25469; either is acceptable','hard'),
 'PAY-65806':('INV-25845','inferred: memo invoice ref + exact amount + payer','easy'),
 'PAY-65807':('INV-25937','inferred: memo "Invoice 25937" + exact amount + payer','easy'),
 'PAY-65808':('INV-25867','inferred: memo "inv25867" + exact amount; note INV-26000 same amount also open','easy')}
un=t[t.true_invoice_ids==''].copy()
un['true_invoice_ids']=un.payment_id.map(lambda x:inferred[x][0]); un['label_source']=un.payment_id.map(lambda x:inferred[x][1]); un['difficulty']=un.payment_id.map(lambda x:inferred[x][2])
# sample: all bank hard + stratified others
rng=np.random.RandomState(7)
bank=hist[hist.method!='card']
hard=bank[bank.difficulty=='hard']
med=bank[bank.difficulty=='medium'].sample(min(80,(bank.difficulty=='medium').sum()),random_state=7)
easy=bank[bank.difficulty=='easy'].sample(60,random_state=7)
card=hist[hist.method=='card'].sample(20,random_state=7)
real=pd.concat([un,hard,med,easy,card]); real['is_synthetic']=False
# synthetic perturbations of real bank payments (for traps absent in the data)
base=bank[bank.received_date>='2026-03-16'].sample(40,random_state=11)
syn=[]
for i,(_,b) in enumerate(base.iterrows()):
    kind=['bank_fee','cent_rounding','short_pay','combined'][i%4]
    s=b.to_dict(); s['payment_id']=f'SYN-{i+1:03d}'; s['is_synthetic']=True; a=float(b.amount)
    if kind=='bank_fee': fee=[15,25,35][i%3]; s['amount']=f'{a-fee:.2f}'; s['difficulty']='hard'; s['difficulty_reason']=f'synthetic: wire/intl bank fee ${fee} deducted from {b.amount}'
    elif kind=='cent_rounding': d=[0.01,-0.01,0.02][i%3]; s['amount']=f'{a+d:.2f}'; s['difficulty']='medium'; s['difficulty_reason']=f'synthetic: per-line rounding diff {d:+.2f} (post-rewrite pattern)'
    elif kind=='short_pay': s['amount']=f'{a*0.9:.2f}'; s['difficulty']='hard'; s['difficulty_reason']='synthetic: 10% short payment (disputed line withheld); should match but flag partial'
    else:
        other=inv[(inv.customer_id==inv.loc[inv.invoice_id==b.true_invoice_ids,'customer_id'].iloc[0])&(inv.invoice_id!=b.true_invoice_ids)&(inv.issue_date<=b.received_date)].sort_values('issue_date').tail(1)
        if len(other)==0: continue
        s['amount']=f'{a+other.amt.iloc[0]:.2f}'; s['true_invoice_ids']=b.true_invoice_ids+'|'+other.invoice_id.iloc[0]; s['difficulty']='hard'; s['difficulty_reason']='synthetic: one receipt covering two invoices'
        s['memo']=re.sub(r'(INV-?|inv|Invoice )\s?\d{5}','',s['memo']).strip() or 'Ledgerline'
    s['label_source']='synthetic_perturbation of '+b.payment_id+' (true label from ledger)'
    syn.append(s)
ts=pd.concat([real,pd.DataFrame(syn)],ignore_index=True)
cols=['payment_id','received_date','amount','method','payer_name','memo','true_invoice_ids','label_source','difficulty','difficulty_reason','n_candidate_customers','n_open_same_amount','is_synthetic']
ts[cols].to_csv(os.path.join(OUT,'testset_cash_app.csv'),index=False)
print(len(ts)); print(pd.crosstab(ts.difficulty,[ts.is_synthetic])); print(ts.label_source.str.split(' ').str[0].value_counts())
print(hard.difficulty_reason.value_counts().head(15))
# historical stats for FACTS
print('bank payments w/o memo invoice ref:', (bank.difficulty!='easy').sum(), 'of', len(bank))
print('payer drift among bank no-ref:', bank[bank.difficulty!='easy'].difficulty_reason.str.contains('drift').sum())
