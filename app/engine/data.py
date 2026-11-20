"""Load the Ledgerline data room into memory. Read-only; everything is as of 2026-10-31."""
import os
import re
from functools import lru_cache

import pandas as pd

AS_OF = pd.Timestamp("2026-10-31")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(ROOT, "data"))
DATA_ZIP = os.path.join(ROOT, "data_room", "ledgerline-data-room.zip")


def _ensure_data():
    """On Render the repo carries the original data-room zip; unpack it once at start-up."""
    global DATA_DIR
    if os.path.exists(os.path.join(DATA_DIR, "finance", "invoices.csv")):
        return
    if os.path.exists(DATA_ZIP):
        import zipfile

        target = os.environ.get("DATA_UNPACK_DIR", "/tmp/ledgerline-data")
        if not os.path.exists(os.path.join(target, "finance", "invoices.csv")):
            with zipfile.ZipFile(DATA_ZIP) as z:
                z.extractall(target)
        # the zip may contain a top-level folder
        for cand in (target, os.path.join(target, "ledgerline-data-room")):
            if os.path.exists(os.path.join(cand, "finance", "invoices.csv")):
                DATA_DIR = cand
                return
        for root, dirs, files in os.walk(target):
            if "invoices.csv" in files and root.endswith("finance"):
                DATA_DIR = os.path.dirname(root)
                return


_SUFFIXES = {"llp", "llc", "inc", "co", "ltd", "the", "and", "company", "partners", "group"}


def norm_name(s):
    """Normalise a company / payer name for matching: lower-case, & and + become 'and', punctuation removed."""
    if not isinstance(s, str):
        return ""
    s = s.lower().replace("&", " and ").replace("+", " and ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(s.split())


def core_tokens(s):
    return [t for t in norm_name(s).split() if t not in _SUFFIXES]


def domain_of(email_or_site):
    if not isinstance(email_or_site, str):
        return ""
    s = email_or_site.strip().lower()
    if "@" in s:
        s = s.split("@", 1)[1]
    s = re.sub(r"^https?://", "", s)
    s = s.split("/")[0]
    if s.startswith("www."):
        s = s[4:]
    return s


@lru_cache(maxsize=1)
def load():
    _ensure_data()

    def rd(p):
        return pd.read_csv(os.path.join(DATA_DIR, p))

    d = {
        "invoices": rd("finance/invoices.csv"),
        "payments": rd("finance/payments.csv"),
        "ar": rd("finance/ar_aging.csv"),
        "customers": rd("customers/customers.csv"),
        "contacts": rd("customers/contacts.csv"),
        "contracts": rd("customers/contracts.csv"),
        "tickets": rd("support/tickets.csv"),
        "nps": rd("support/nps_responses.csv"),
        "usage": rd("product/usage_monthly.csv"),
    }
    for k in ("invoices",):
        d[k]["issue_date"] = pd.to_datetime(d[k]["issue_date"])
        d[k]["due_date"] = pd.to_datetime(d[k]["due_date"])
    d["payments"]["received_date"] = pd.to_datetime(d["payments"]["received_date"])
    d["tickets"]["created_at"] = pd.to_datetime(d["tickets"]["created_at"])
    cus = d["customers"].copy()
    active = cus[cus["status"] == "active"].sort_values("current_arr", ascending=False)
    rank = {cid: i + 1 for i, cid in enumerate(active["customer_id"])}
    cus["rank"] = cus["customer_id"].map(rank)
    cus["norm"] = cus["name"].map(norm_name)
    cus["domain"] = cus["website"].map(domain_of)
    d["customers"] = cus
    return d


def read_doc(rel):
    _ensure_data()
    with open(os.path.join(DATA_DIR, rel), encoding="utf-8") as f:
        return f.read()
