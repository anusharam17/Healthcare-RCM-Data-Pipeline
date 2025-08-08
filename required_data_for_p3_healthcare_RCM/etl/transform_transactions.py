import pandas as pd
import numpy as np
from datetime import datetime

# Load transactions
file_path = '../output/combined_transactions.csv'
df = pd.read_csv(file_path)
print("[DEBUG] Columns in the file:", list(df.columns))

# Trim whitespace and standardize title casing for specific columns
columns_to_clean = ['PaymentStatus', 'AmountType', 'LineOfBusiness', 'VisitType']

for col in columns_to_clean:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()
    else:
        print(f"[INFO] '{col}' column not found. Skipping transformation for it.")

# Convert date columns to datetime format
date_columns = ['VisitDate', 'ServiceDate', 'PaidDate', 'InsertDate', 'ModifiedDate']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Remove duplicates
df = df.drop_duplicates()
print(f"[INFO] Remaining records after dropping duplicates: {len(df)}")

# Add surrogate keys (temporary until proper key generation in star schema)
df['TransactionSK'] = range(1, len(df) + 1)

# Derive new columns
df['TransactionMonth'] = df['VisitDate'].dt.month
df['TransactionYear'] = df['VisitDate'].dt.year

# Categorize payment status
def categorize_status(status):
    if pd.isnull(status):
        return 'Unknown'
    status = status.lower()
    if 'paid' in status:
        return 'Paid'
    elif 'denied' in status:
        return 'Denied'
    elif 'pending' in status:
        return 'Pending'
    else:
        return 'Other'

df['PaymentCategory'] = df['PaymentStatus'].apply(categorize_status)

# Save cleaned data
output_path = '../output/cleaned_transactions.csv'
df.to_csv(output_path, index=False)
print(f"[SUCCESS] Cleaned transactions saved to {output_path}")
