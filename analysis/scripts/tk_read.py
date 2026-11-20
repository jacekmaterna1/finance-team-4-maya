import sys, pandas as pd
tk=pd.read_csv(sys.argv[1],dtype=str,keep_default_na=False)
ids=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else None
t=tk[tk.ticket_id.isin(ids)] if ids else tk
for _,x in t.iterrows():
    print(f"--- {x.ticket_id} {x.created_at} {x.customer_id} {x.customer_name} | cat={x.category} pri={x.priority} st={x.status} | {x.subject}\n{x.body[:500]}")
