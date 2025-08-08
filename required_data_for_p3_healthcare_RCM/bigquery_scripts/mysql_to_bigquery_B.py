import pandas as pd
import mysql.connector
from google.cloud import bigquery
from google.oauth2 import service_account

# MySQL config for Hospital B
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "anuram@2003",
    "database": "hospital_b_db"
}

# Connect to MySQL
conn = mysql.connector.connect(**mysql_config)
print("✅ Connected to MySQL.")

# Example table name from MySQL
table_name = "patients"  # change this if you're loading another table

# Extract data from MySQL
query = f"SELECT * FROM {table_name};"
df = pd.read_sql(query, conn)
print(f"✅ Extracted {len(df)} rows from MySQL.")

# Add hospital_id column to identify source
df['hospital_id'] = 'B'

# Reorder columns: move hospital_id to front (optional)
cols = ['hospital_id'] + [col for col in df.columns if col != 'hospital_id']
df = df[cols]

# Drop problematic columns (optional, based on error)
if 'ID' in df.columns:
    df = df.drop(columns=['ID'])

# Connect to BigQuery
key_path = 'credentials/healthcare-rcm-467805-f5f313cc10f7.json'
credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)
print("✅ Connected to BigQuery.")

# Upload to BigQuery
destination_table = f"healthcare_rcm.{table_name}"  # same table name
df.to_gbq(
    destination_table=destination_table,
    project_id=credentials.project_id,
    credentials=credentials,
    if_exists="append"  # append to avoid schema overwrite
)
print(f"✅ Uploaded data to BigQuery table {destination_table}")
