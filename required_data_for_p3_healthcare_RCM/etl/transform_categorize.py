import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

try:
    input_path = "output/cleaned_patients_standardized.csv"
    output_path = "output/cleaned_patients_categorized.csv"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"{input_path} not found")

    df = pd.read_csv(input_path)

    # Add AgeGroup
    def categorize_age(age):
        if age < 0:
            return "Invalid"
        elif age <= 17:
            return "Child"
        elif age <= 35:
            return "Young Adult"
        elif age <= 60:
            return "Adult"
        else:
            return "Senior"

    df['age_group'] = df['age'].apply(categorize_age)

    # Add GenderCategory
    def categorize_gender(g):
        g = str(g).upper().strip()
        if g in ['M', 'MALE']:
            return "Male"
        elif g in ['F', 'FEMALE']:
            return "Female"
        else:
            return "Other"

    df['GenderCategory'] = df['Gender'].apply(categorize_gender)

    # Save
    df.to_csv(output_path, index=False)
    logging.info(f"✅ Categorized data saved to: {output_path}")

except Exception as e:
    logging.error(f"Check logs: {e}")
