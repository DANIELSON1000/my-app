# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:03:39 2025

@author: ELINA
"""

# database.py
import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

TENANTS = DATA_DIR / "tenants.csv"
PAYMENTS = DATA_DIR / "payments.csv"
MESSAGES = DATA_DIR / "messages.csv"

def read_table(path, cols=None):
    if not path.exists():
        if cols:
            df = pd.DataFrame(columns=cols)
            df.to_csv(path, index=False)
            return df
        return pd.DataFrame()
    return pd.read_csv(path, dtype=str)

def write_table(path, df):
    df.to_csv(path, index=False)

def load_tenants():
    cols = ["tenant_id","fullname","id_number","phone","sex","people","house_status","start_date","rent","username","password","agreement_file","created_at"]
    return read_table(TENANTS, cols)

def save_tenants(df):
    write_table(TENANTS, df)

def load_payments():
    cols = ["payment_id","tenant_id","month","status","paid_date"]
    return read_table(PAYMENTS, cols)

def save_payments(df):
    write_table(PAYMENTS, df)

def load_messages():
    cols = ["message_id","tenant_id","message","reply","date_sent","date_reply","status"]
    return read_table(MESSAGES, cols)

def save_messages(df):
    write_table(MESSAGES, df)

def next_id(df, id_col):
    if df.empty:
        return "1"
    return str(int(df[id_col].astype(int).max()) + 1)

def timestamp_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
