import pandas as pd
import logging
import os

# Setup logging
logging.basicConfig(
    filename='transform_patients.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def standardize_name(name):
    if pd.isnull(name):
        return ""
    return (
        str(name)
        .strip()
        .replace('.', '')
        .replace(',', '')
        .replace('_', ' ')
        .title()
    )

def transform_patients():
    input_file = "output/combined_patients.csv"
    output_file = "output/cleaned_patients.csv"

    try:
        # Load data
        df = pd.read_csv(input_file)
        logging.info("Loaded combined_patients.csv")

        # Drop exact duplicates
        before = df.shape[0]
        df.drop_duplicates(inplace=True)
        after = df.shape[0]
        logging.info(f"Removed {before - after} duplicate rows")

        # Standardize names
        name_columns = ['first_name', 'last_name', 'middle_name']
        for col in name_columns:
            if col in df.columns:
                df[col] = df[col].apply(standardize_name)
                logging.info(f"Standardized column: {col}")

        # Save cleaned file
        df.to_csv(output_file, index=False)
        logging.info(f"Cleaned file saved: {output_file}")
        print(f"✅ Cleaned file saved: {os.path.abspath(output_file)}")

    except Exception as e:
        logging.error(f"Error in transform_patients: {e}")
        print(f"[ERROR] Check logs: {e}")

if __name__ == "__main__":
    transform_patients()
