# etl/clean_providers.py
import pandas as pd

try:
    df = pd.read_csv("../output/combined_providers.csv")
    print("[DEBUG] Columns:", df.columns.tolist())

    # Drop duplicates
    df = df.drop_duplicates()
    print(f"[INFO] Remaining records after dropping duplicates: {len(df)}")

    # Create full name
    df['ProviderName'] = df['FirstName'].str.strip().str.title() + " " + df['LastName'].str.strip().str.title()

    # Standardize NPI (preserve leading 0s)
    df['NPI'] = df['NPI'].astype(str).str.zfill(10)

    # Rename Specialization to Specialty for consistency
    if 'Specialization' in df.columns:
        df.rename(columns={'Specialization': 'Specialty'}, inplace=True)

    # Fill missing specialty
    df['Specialty'] = df['Specialty'].fillna('Unknown').str.title()

    # Save cleaned version
    df.to_csv("../output/cleaned_providers.csv", index=False)
    print("[SUCCESS] Cleaned providers saved to ../output/cleaned_providers.csv")

except Exception as e:
    print(f"[ERROR] {e}")
