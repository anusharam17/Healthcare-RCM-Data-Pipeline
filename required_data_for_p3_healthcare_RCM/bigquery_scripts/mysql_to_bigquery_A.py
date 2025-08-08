import os
import pandas as pd
import mysql.connector
from google.cloud import bigquery
from google.oauth2 import service_account

# === 1. Set environment variable for authentication ===
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/credentials/healthcare-rcm-467805-f5f313cc10f7.json"

# === 2. MySQL Configuration ===
mysql_config = {
    'user': 'root',
    'password': 'anuram@2003',  # <-- Replace with your MySQL password
    'host': 'localhost',
    'database': 'hospital_a_db'  # Change to hospital_b_db if needed
}

# === 3. Connect to MySQL and load data from a table ===
try:
    conn = mysql.connector.connect(**mysql_config)
    print("✅ Connected to MySQL.")

    query = "SELECT * FROM patients;"  # Change table as needed
    df = pd.read_sql(query, conn)
    print(f"✅ Extracted {len(df)} rows from MySQL.")

except Exception as e:
    print("❌ MySQL Error:", e)
    exit()

# === 4. BigQuery Configuration ===
project_id = "healthcare-rcm-467805"
dataset_id = "healthcare_rcm"
table_id = "patient"  # BigQuery table name (can be same as MySQL table)

try:
    # Initialize BigQuery client
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    bq_client = bigquery.Client(credentials=credentials, project=project_id)
    print("✅ Connected to BigQuery.")

    # Define destination table
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Load data to BigQuery
    job = bq_client.load_table_from_dataframe(df, table_ref)
    job.result()  # Wait for job to finish
    print(f"✅ Uploaded data to BigQuery table: {table_ref}")

except Exception as e:
    print("❌ BigQuery Error:", e)
