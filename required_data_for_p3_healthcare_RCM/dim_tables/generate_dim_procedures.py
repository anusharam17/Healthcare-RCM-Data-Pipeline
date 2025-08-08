import pandas as pd
import hashlib

# Load encounters data
df = pd.read_csv('../output/cleaned_encounters.csv')

# Check required column
if 'ProcedureCode' not in df.columns:
    print("❌ 'ProcedureCode' column not found.")
    exit()

# Drop null or empty ProcedureCodes
df = df[df['ProcedureCode'].notna()]
df = df[df['ProcedureCode'].astype(str).str.strip() != '']

# Drop duplicates
df_unique = df[['ProcedureCode']].drop_duplicates().reset_index(drop=True)

# Add ProcedureKey as surrogate key
df_unique.insert(0, 'ProcedureKey', range(1, len(df_unique) + 1))

# Optional: Add placeholder descriptions
df_unique['ProcedureDescription'] = 'Description for ' + df_unique['ProcedureCode'].astype(str)

# Reorder columns
df_unique = df_unique[['ProcedureKey', 'ProcedureCode', 'ProcedureDescription']]

# Save to CSV
df_unique.to_csv('../output/dim_procedure.csv', index=False)

print(f"[✅] dim_procedure.csv created with {len(df_unique)} unique procedures.")
