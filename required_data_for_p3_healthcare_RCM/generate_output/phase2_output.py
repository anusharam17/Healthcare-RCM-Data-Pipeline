import pandas as pd
import os

# Paths
data_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output"
claims_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/claims"

def preview_df(df, name):
    print(f"✅ {name}: {len(df)} rows before cleaning")

    print(df.head(3))
    print("-" * 100)

def combine_patients():
    df_a = pd.read_csv(os.path.join(data_dir, "a_patients.csv"))
    df_b = pd.read_csv(os.path.join(data_dir, "b_patients.csv"))

    # Rename B columns to match A
    rename_map = {
        "ID": "PatientID",
        "F_Name": "FirstName",
        "L_Name": "LastName",
        "M_Name": "MiddleName"
    }
    df_b.rename(columns=rename_map, inplace=True)

    combined = pd.concat([df_a, df_b], ignore_index=True)
    preview_df(combined, "patients")
    return combined

def combine_providers():
    df_a = pd.read_csv(os.path.join(data_dir, "a_providers.csv"))
    df_b = pd.read_csv(os.path.join(data_dir, "b_providers.csv"))
    combined = pd.concat([df_a, df_b], ignore_index=True)
    preview_df(combined, "providers")
    return combined

def combine_transactions():
    df_a = pd.read_csv(os.path.join(data_dir, "a_transactions.csv"))
    df_b = pd.read_csv(os.path.join(data_dir, "b_transactions.csv"))
    combined = pd.concat([df_a, df_b], ignore_index=True)
    preview_df(combined, "transactions")
    return combined

def combine_encounters():
    df_a = pd.read_csv(os.path.join(data_dir, "a_encounters.csv"))
    df_b = pd.read_csv(os.path.join(data_dir, "b_encounters.csv"))
    combined = pd.concat([df_a, df_b], ignore_index=True)
    preview_df(combined, "encounters")
    return combined

def combine_claims():
    df_a = pd.read_csv(os.path.join(claims_dir, "hospital1_claim_data.csv"))
    df_b = pd.read_csv(os.path.join(claims_dir, "hospital2_claim_data.csv"))
    combined = pd.concat([df_a, df_b], ignore_index=True)
    preview_df(combined, "claims")
    return combined

if __name__ == "__main__":
    print("\n--- Phase 2: Data Extraction & Combination (Raw Counts + Preview) ---\n")
    combine_patients()
    combine_providers()
    combine_transactions()
    combine_encounters()
    combine_claims()
