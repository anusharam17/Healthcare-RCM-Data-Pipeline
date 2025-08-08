import pandas as pd
import os

# Paths
data_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output"

def save_and_log(df, filename, label):
    path = os.path.join(data_dir, filename)
    df.to_csv(path, index=False)
    print(f"✅ {label}: {len(df)} rows — saved to {filename}")

# 1. DIM_PATIENT
df_pat = pd.read_csv(os.path.join(data_dir, "cleaned_patients.csv"))
dim_patient = df_pat[[col for col in ["PatientID", "FirstName", "LastName", "Gender", "DOB", "Age", "HospitalName"] if col in df_pat.columns]]
save_and_log(dim_patient, "dim_patient.csv", "dim_patient")

# 2. DIM_PROVIDER
df_prov = pd.read_csv(os.path.join(data_dir, "cleaned_providers.csv"))
save_and_log(df_prov, "dim_provider.csv", "dim_provider")

# 3. DIM_DATE
date_cols = []
for file, col in [
    ("cleaned_transactions.csv", "TransactionDate"),
    ("cleaned_encounters.csv", "EncounterDate"),
    ("cleaned_claims.csv", "ClaimDate")
]:
    path = os.path.join(data_dir, file)
    if os.path.exists(path):
        df = pd.read_csv(path)
        if col in df.columns:
            date_cols.extend(pd.to_datetime(df[col], errors="coerce").dropna().dt.date.unique())

dim_date = pd.DataFrame(sorted(set(date_cols)), columns=["Date"])
dim_date["Year"] = pd.to_datetime(dim_date["Date"]).dt.year
dim_date["Month"] = pd.to_datetime(dim_date["Date"]).dt.month
dim_date["Day"] = pd.to_datetime(dim_date["Date"]).dt.day
save_and_log(dim_date, "dim_date.csv", "dim_date")

# 4. DIM_PROCEDURE (with placeholder descriptions if missing)
df_enc = pd.read_csv(os.path.join(data_dir, "cleaned_encounters.csv"))
if "ProcedureCode" in df_enc.columns:
    if "ProcedureDescription" not in df_enc.columns:
        df_enc["ProcedureDescription"] = "Description for " + df_enc["ProcedureCode"].astype(str)
    dim_procedure = df_enc[["ProcedureCode", "ProcedureDescription"]].drop_duplicates()
else:
    dim_procedure = pd.DataFrame(columns=["ProcedureCode", "ProcedureDescription"])
save_and_log(dim_procedure, "dim_procedure.csv", "dim_procedure")

# 5. FACT_TRANSACTIONS
df_trans = pd.read_csv(os.path.join(data_dir, "cleaned_transactions.csv"))
cols_needed = [col for col in ["TransactionID", "PatientID", "ProviderID", "TransactionDate", "TotalAmount", "AmountPaid", "PaymentStatus"] if col in df_trans.columns]
fact_transactions = df_trans[cols_needed]
save_and_log(fact_transactions, "fact_transactions.csv", "fact_transactions")

# 6. FACT_CLAIMS
df_claims = pd.read_csv(os.path.join(data_dir, "cleaned_claims.csv"))
fact_claims = df_claims.copy() if not df_claims.empty else pd.DataFrame(columns=["ClaimID"])
save_and_log(fact_claims, "fact_claims.csv", "fact_claims")
