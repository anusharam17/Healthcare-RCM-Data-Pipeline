import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

try:
    input_path = "output/cleaned_patients_with_age.csv"
    output_path = "output/cleaned_patients_standardized.csv"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"{input_path} not found")

    # Read input file
    df = pd.read_csv(input_path)

    # Standardize names
    for col in ['FirstName', 'LastName', 'MiddleName']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()

    # Standardize phone numbers
    def clean_phone(phone):
        phone = ''.join(filter(str.isdigit, str(phone)))
        return phone[-10:] if len(phone) >= 10 else phone

    df['PhoneNumber'] = df['PhoneNumber'].apply(clean_phone)

    # Standardize address
    if 'Address' in df.columns:
        df['Address'] = df['Address'].astype(str).str.title()

    # Save to new CSV
    df.to_csv(output_path, index=False)
    logging.info(f"✅ Standardized data saved to: {output_path}")

except Exception as e:
    logging.error(f"Check logs: {e}")
