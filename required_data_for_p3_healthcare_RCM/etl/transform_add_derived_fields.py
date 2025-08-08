import pandas as pd
from datetime import datetime
import os
import logging

# Setup logging
logging.basicConfig(filename='etl/transform_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_age(dob):
    try:
        birth_date = pd.to_datetime(dob, errors='coerce')
        today = pd.to_datetime('today')
        return (today.year - birth_date.year) - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        return None

def assign_age_group(age):
    if pd.isnull(age):
        return 'Unknown'
    elif age < 18:
        return 'Child'
    elif age < 60:
        return 'Adult'
    else:
        return 'Senior'

def main():
    try:
        input_file = 'output/cleaned_patients.csv'
        output_file = 'output/cleaned_patients_with_age.csv'

        # Load data
        df = pd.read_csv(input_file)

        # Calculate Age
        df['age'] = df['DOB'].apply(calculate_age)

        # Add Age Group
        df['age_group'] = df['age'].apply(assign_age_group)

        # Flag minors
        df['is_minor'] = df['age'] < 18

        # Save transformed file
        df.to_csv(output_file, index=False)
        logging.info("Derived fields added successfully.")
        print(f"✅ Derived fields added. File saved to: {output_file}")

    except Exception as e:
        logging.error(f"Failed to add derived fields: {e}")
        print(f"[ERROR] Check logs: {e}")

if __name__ == "__main__":
    main()
