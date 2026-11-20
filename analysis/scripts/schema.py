import sys, os, pandas as pd
D = sys.argv[1]
files = {
 'invoices':'finance/invoices.csv','payments':'finance/payments.csv','ar_aging':'finance/ar_aging.csv',
 'customers':'customers/customers.csv','contacts':'customers/contacts.csv','contracts':'customers/contracts.csv',
 'tickets':'support/tickets.csv','nps_responses':'support/nps_responses.csv','usage_monthly':'product/usage_monthly.csv',
 'opportunities':'sales/opportunities.csv'}
expected = {'invoices':6062,'payments':5808,'ar_aging':117,'customers':508,'contacts':967,'contracts':1757,
 'tickets':1041,'nps_responses':820,'usage_monthly':6955,'opportunities':2176}
df = {k: pd.read_csv(os.path.join(D,v), dtype=str, keep_default_na=False) for k,v in files.items()}
for k,d in df.items():
    print(f"\n### {k} ({files[k]}) rows={len(d)} expected={expected[k]}")
    print("cols:", list(d.columns))
    print("example:", d.iloc[0].to_dict() if k!='tickets' else {c:(d.iloc[0][c][:80]) for c in d.columns})
    for c in d.columns:
        n = d[c].nunique()
        blank = (d[c]=='').sum()
        if n <= 15:
            print(f"  {c}: blanks={blank} values={d[c].value_counts().to_dict()}")
        else:
            print(f"  {c}: nunique={n} blanks={blank}")
