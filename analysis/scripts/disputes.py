import sys, os, re, pandas as pd
D=sys.argv[1]; OUT=sys.argv[2]
tk=pd.read_csv(os.path.join(D,'support/tickets.csv'),dtype=str,keep_default_na=False)
inv=pd.read_csv(os.path.join(D,'finance/invoices.csv'),dtype=str,keep_default_na=False)
txt=(tk.subject+' '+tk.body)
tk['inv_refs']=txt.str.findall(r'INV-\d{5}').map(lambda l:','.join(sorted(set(l))))
ref=tk[tk.inv_refs!=''].assign(invoice_id=lambda d:d.inv_refs.str.split(',')).explode('invoice_id')
ref=ref.merge(inv[['invoice_id','customer_id','amount','status','due_date','payment_method']].rename(columns={'status':'status_inv','customer_id':'customer_id_inv'}),on='invoice_id',how='left')
print('tickets referencing invoice ids:', (tk.inv_refs!='').sum(), 'refs', len(ref))
print('ref customer mismatch:', (ref.customer_id!=ref.customer_id_inv).sum(), 'unknown inv', ref.status.isna().sum())
print(ref.status_inv.value_counts())
cols=['ticket_id','created_at','customer_id','customer_name','category','priority','status','invoice_id','status_inv','amount','due_date','subject']
print(ref[cols].sort_values('status_inv').to_string())
ref[cols+['body']].to_csv(os.path.join(OUT,'tickets_invoice_refs.csv'),index=False)
low=txt.str.lower()
themes={'rounding_cent':r'smallest currency|1,949|\.99|rounding|rounded|a cent|one cent|penny|cents|off by',
 'proration':r'prorat|partial month|mid-?cycle|days in',
 'due_date_tz':r'due the|due date|time zone|timezone|says due|due on the',
 'card_retry':r'retr(?:y|ies|ied)|declin|card fail|failed payment|payment failed',
 'credit_note_version':r'credit note|new version|reissued|two versions|duplicate (?:invoice|charge)|charged twice|double',
 'settings_moved':r'billing > preferences|preferences|settings > billing|can.t find the setting|moved'}
for k,v in themes.items(): tk[k]=low.str.contains(v)
tk['month']=tk.created_at.str[:7]
print(tk.groupby('month')[list(themes)].sum())
print(pd.crosstab(tk.category,tk[list(themes)].any(axis=1)))
for k in themes:
    s=tk[tk[k]]
    print(f'\n## {k} n={len(s)}')
    for _,x in s.head(6).iterrows(): print(' ',x.ticket_id,x.customer_id,x.category,x.status,'|',x.body[:160].replace('\n',' '))
tk[['ticket_id','created_at','customer_id','customer_name','category','priority','status','inv_refs']+list(themes)].to_csv(os.path.join(OUT,'tickets_themes.csv'),index=False)
