# etl/clean_claims.py
import pandas as pd

try:
    df = pd.read_csv("../output/combined_claims.csv")
    print("[DEBUG] Columns:", df.columns.tolist())

    df = df.drop_duplicates()
    print(f"[INFO] Remaining records after dropping duplicates: {len(df)}")

    # Convert dates
    df['ServiceDate'] = pd.to_datetime(df['ServiceDate'], errors='coerce')
    df['ClaimDate'] = pd.to_datetime(df['ClaimDate'], errors='coerce')
    df['InsertDate'] = pd.to_datetime(df['InsertDate'], errors='coerce')
    df['ModifiedDate'] = pd.to_datetime(df['ModifiedDate'], errors='coerce')

    # Clean ClaimStatus
    df['ClaimStatus'] = df['ClaimStatus'].str.strip().str.title()

    # Clean PayorType
    df['PayorType'] = df['PayorType'].str.strip().str.title()

    # If ProcedureCode exists, clean it
    if 'ProcedureCode' in df.columns:
        df['ProcedureCode'] = df['ProcedureCode'].astype(str).str.upper().str.strip()
    else:
        print("[WARNING] 'ProcedureCode' column not found. Skipping ProcedureCode cleaning.")

    # Fill NA in numerical fields
    for col in ['ClaimAmount', 'PaidAmount', 'Deductible', 'Coinsurance', 'Copay']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # Save cleaned version
    df.to_csv("../output/cleaned_claims.csv", index=False)
    print("[SUCCESS] Cleaned claims saved to ../output/cleaned_claims.csv")

except Exception as e:
    print(f"[ERROR] {e}")
