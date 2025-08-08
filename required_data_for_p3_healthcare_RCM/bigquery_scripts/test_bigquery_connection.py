from google.cloud import bigquery
import os

# ✅ Correct path to service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/credentials/healthcare-rcm-467805-f5f313cc10f7.json"

# Initialize BigQuery client
client = bigquery.Client(project="healthcare-rcm-467805")

# Check connection
datasets = list(client.list_datasets())
print("Datasets in project:")
for dataset in datasets:
    print(f"- {dataset.dataset_id}")
