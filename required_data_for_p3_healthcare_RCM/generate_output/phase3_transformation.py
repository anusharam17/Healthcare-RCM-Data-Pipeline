import pandas as pd
import os
from datetime import datetime
import numpy as np

# Paths
data_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output"

def calculate_age(dob):
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def clean_phone(phone):
    phone = str(phone)
    digits = ''.join(filter(str.isdigit, phone))
    return digits if len(digits) >= 10 else None

def standardize_name(name):
    return str(name).strip().title() if pd.notna(name) else None

# Save helper
def save_cleaned(df, filename):
    out_path = os.path.join(data_dir, filename)
    df.to_csv(out_path, index=False)
    print(f"💾 Saved: {out_path}")

# 1. Patients
df_pat = pd.read_csv(os.path.join(data_dir, "combined_patients.csv"))
df_pat["FirstName"] = df_pat["FirstName"].apply(standardize_name)
df_pat["LastName"] = df_pat["LastName"].apply(standardize_name)
df_pat["PhoneNumber"] = df_pat["PhoneNumber"].apply(clean_phone)
df_pat["DOB"] = pd.to_datetime(df_pat["DOB"], errors="coerce")
df_pat["Age"] = df_pat["DOB"].apply(lambda x: calculate_age(x) if pd.notnull(x) else None)
df_pat.drop_duplicates(subset="PatientID", inplace=True)
print(f"✅ Patients cleaned: {len(df_pat)} rows")
save_cleaned(df_pat, "cleaned_patients.csv")

# 2. Providers
df_prov = pd.read_csv(os.path.join(data_dir, "combined_providers.csv"))
if "ProviderName" in df_prov.columns:
    df_prov["ProviderName"] = df_prov["ProviderName"].apply(standardize_name)
df_prov.drop_duplicates(subset="ProviderID", inplace=True)
print(f"✅ Providers cleaned: {len(df_prov)} rows")
save_cleaned(df_prov, "cleaned_providers.csv")

# 3. Transactions
df_trans = pd.read_csv(os.path.join(data_dir, "combined_transactions.csv"))
if "TransactionDate" in df_trans.columns:
    df_trans["TransactionDate"] = pd.to_datetime(df_trans["TransactionDate"], errors="coerce")
if "AmountPaid" in df_trans.columns and "TotalAmount" in df_trans.columns:
    df_trans["PaymentStatus"] = np.where(df_trans["AmountPaid"] >= df_trans["TotalAmount"], "Paid", "Pending")
df_trans.drop_duplicates(subset="TransactionID", inplace=True)
print(f"✅ Transactions cleaned: {len(df_trans)} rows")
save_cleaned(df_trans, "cleaned_transactions.csv")

# 4. Encounters
df_enc = pd.read_csv(os.path.join(data_dir, "combined_encounters.csv"))
if "EncounterDate" in df_enc.columns:
    df_enc["EncounterDate"] = pd.to_datetime(df_enc["EncounterDate"], errors="coerce")
df_enc.drop_duplicates(subset="EncounterID", inplace=True)
print(f"✅ Encounters cleaned: {len(df_enc)} rows")
save_cleaned(df_enc, "cleaned_encounters.csv")

# 5. Claims
df_claims = pd.read_csv(os.path.join(data_dir, "combined_claims.csv"))
if "ClaimDate" in df_claims.columns:
    df_claims["ClaimDate"] = pd.to_datetime(df_claims["ClaimDate"], errors="coerce")

# Find claim ID column dynamically
claim_id_col = None
for col in df_claims.columns:
    if col.lower() in ["claim_id", "claimid", "id"]:
        claim_id_col = col
        break

if claim_id_col:
    df_claims.drop_duplicates(subset=claim_id_col, inplace=True)
else:
    df_claims.drop_duplicates(inplace=True)

print(f"✅ Claims cleaned: {len(df_claims)} rows")
save_cleaned(df_claims, "cleaned_claims.csv")

