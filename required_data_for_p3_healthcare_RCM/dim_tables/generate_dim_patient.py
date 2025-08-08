import pandas as pd
from datetime import datetime

# File paths
input_path = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output/cleaned_patients.csv"
output_path = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/dim_tables/dim_patient.csv"

# Read the cleaned patient CSV
df = pd.read_csv(input_path)

# Convert dates
df['DOB'] = pd.to_datetime(df['DOB'], errors='coerce')
df['Updated_Date'] = pd.to_datetime(df.get('Updated_Date', pd.NaT), errors='coerce')

# Drop invalid DOBs
df = df.dropna(subset=['DOB'])

# Calculate Age
today = datetime.today()
df['Age'] = df['DOB'].apply(lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))

# Add SCD2 fields
df['StartDate'] = today.strftime('%Y-%m-%d')
df['EndDate'] = pd.NaT
df['IsCurrent'] = True
df['Version'] = 1  # Initial version is always 1

# Rename for consistency
df.rename(columns={
    'M_Name': 'MiddleName',
    'Updated_Date': 'ModifiedDate'
}, inplace=True)

# Add missing hospital column if needed
if 'hospital' not in df.columns:
    df['hospital'] = 'HOSP_UNKNOWN'

# Reorder columns for dimension table
dim_patient = df[[
    'PatientID',        # 1
    'FirstName',        # 2
    'MiddleName',       # 3
    'LastName',         # 4
    'Gender',           # 5
    'DOB',              # 6
    'Age',              # 7
    'hospital',         # 8
    'StartDate',        # 9
    'EndDate',          # 10
    'IsCurrent',        # 11
    'Version'           # 12
]]

# Save to CSV
dim_patient.to_csv(output_path, index=False)
print("✅ dim_patient.csv (with Version) created successfully at:")
print(output_path)
