import pandas as pd

try:
    # Load the combined encounters file
    df = pd.read_csv("../output/combined_encounters.csv")
    print("[DEBUG] Columns:", df.columns.tolist())

    # Drop duplicate rows
    df = df.drop_duplicates()
    print(f"[INFO] Remaining records after dropping duplicates: {len(df)}")

    # Convert date columns to datetime
    date_cols = ['EncounterDate', 'InsertDate', 'ModifiedDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Standardize EncounterType and EncounterReason if they exist
    if 'EncounterType' in df.columns:
        df['EncounterType'] = df['EncounterType'].astype(str).str.strip().str.title()
    if 'EncounterReason' in df.columns:
        df['EncounterReason'] = df['EncounterReason'].astype(str).str.strip().str.title()

    # Handle missing values in numerical columns if any
    num_cols = ['DeptID']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Save cleaned version
    df.to_csv("../output/cleaned_encounters.csv", index=False)
    print("[SUCCESS] Cleaned encounters saved to ../output/cleaned_encounters.csv")

except Exception as e:
    print(f"[ERROR] {e}")
