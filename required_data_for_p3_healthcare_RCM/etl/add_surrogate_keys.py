import pandas as pd
import os

# ✅ Correct relative paths (you are running from root of the project)
input_path = "output/cleaned_patients_categorized.csv"
output_path = "dim_tables/dim_patients.csv"

# Load data
df = pd.read_csv(input_path)

# Add surrogate key
df.insert(0, 'PatientKey', range(1, len(df) + 1))

# Save dimension table
df.to_csv(output_path, index=False)

print(f"[✅ SUCCESS] Surrogate key added and saved to: {output_path}")
