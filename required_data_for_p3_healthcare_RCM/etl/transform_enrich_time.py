import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

try:
    input_path = "output/cleaned_patients_categorized.csv"
    output_path = "output/cleaned_patients_enriched.csv"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"{input_path} not found")

    df = pd.read_csv(input_path)

    # Convert ModifiedDate to datetime
    df['ModifiedDate'] = pd.to_datetime(df['ModifiedDate'], errors='coerce')

    # Add time features
    df['Modified_Year'] = df['ModifiedDate'].dt.year
    df['Modified_Month'] = df['ModifiedDate'].dt.month
    df['Modified_Day'] = df['ModifiedDate'].dt.day
    df['Modified_Quarter'] = df['ModifiedDate'].dt.quarter
    df['Modified_Weekday'] = df['ModifiedDate'].dt.day_name()

    # Save final enriched data
    df.to_csv(output_path, index=False)
    logging.info(f"✅ Time-enriched data saved to: {output_path}")

except Exception as e:
    logging.error(f"Check logs: {e}")
