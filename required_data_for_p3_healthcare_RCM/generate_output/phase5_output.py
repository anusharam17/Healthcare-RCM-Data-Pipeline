# phase5_load_to_bigquery.py
import os
from google.cloud import bigquery

# -------- CONFIG --------
# Path to your service account JSON key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/credentials/healthcare-rcm-467805-f5f313cc10f7.json"

# BigQuery project and dataset
PROJECT_ID = "healthcare-rcm-467805"
DATASET_ID = "helathcare_rcm"

# Local CSV output folder from Phase 4
OUTPUT_DIR = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output"

# List of CSVs to upload
TABLES = [
    "dim_patient.csv",
    "dim_provider.csv",
    "dim_date.csv",
    "dim_procedure.csv",
    "fact_transactions.csv",
    "fact_claims.csv"
]

# -------- LOAD TO BIGQUERY --------
client = bigquery.Client(project=PROJECT_ID)

def load_csv_to_bq(csv_filename):
    table_name = os.path.splitext(csv_filename)[0]
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    with open(os.path.join(OUTPUT_DIR, csv_filename), "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    
    job.result()  # Wait for the load to complete
    table = client.get_table(table_id)
    print(f"✅ {table_name}: {table.num_rows} rows loaded into {table_id}")

if __name__ == "__main__":
    print("\n--- Phase 5: Loading Phase 4 CSVs into BigQuery ---\n")
    for csv_file in TABLES:
        load_csv_to_bq(csv_file)
    print("\n✅ All tables loaded successfully into BigQuery.")
