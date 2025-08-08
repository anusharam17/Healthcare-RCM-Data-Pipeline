import pandas as pd
from datetime import datetime
from google.cloud import bigquery
import os

class SCD2Handler:
    def __init__(self, historical_file, new_file, output_file,
                 gcp_project, dataset_id, table_id, service_account_path):
        self.historical_file = historical_file
        self.new_file = new_file
        self.output_file = output_file
        self.gcp_project = gcp_project
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.service_account_path = service_account_path

    def load_data(self):
        self.historical_df = pd.read_csv(self.historical_file)
        self.new_df = pd.read_csv(self.new_file)

        # Clean column names
        self.historical_df.columns = self.historical_df.columns.str.strip()
        self.new_df.columns = self.new_df.columns.str.strip()

        # Rename columns for consistency
        if 'HospitalName' in self.new_df.columns:
            self.new_df.rename(columns={'HospitalName': 'hospital'}, inplace=True)

        # Ensure date columns are DATE type
        if 'StartDate' in self.historical_df.columns:
            self.historical_df['StartDate'] = pd.to_datetime(
                self.historical_df['StartDate'], errors='coerce'
            ).dt.date
        if 'EndDate' in self.historical_df.columns:
            self.historical_df['EndDate'] = pd.to_datetime(
                self.historical_df['EndDate'], errors='coerce'
            ).dt.date

        # Ensure 'IsCurrent' exists and is boolean
        if 'IsCurrent' in self.historical_df.columns:
            self.historical_df['IsCurrent'] = self.historical_df['IsCurrent'].astype(bool)
        else:
            self.historical_df['IsCurrent'] = True

        print("✅ Data Loaded Successfully")
        print("📋 Historical Columns:", self.historical_df.columns.tolist())
        print("📋 New Data Columns:", self.new_df.columns.tolist())

    def process(self):
        current_df = self.historical_df[self.historical_df['IsCurrent'] == True]

        merged = pd.merge(
            current_df,
            self.new_df,
            on='PatientID',
            how='outer',
            suffixes=('_hist', '_new'),
            indicator=True
        )

        compare_columns = ['FirstName', 'MiddleName', 'LastName', 'Gender', 'DOB', 'Age', 'hospital']

        updated_records = []
        unchanged_records = []
        new_records = []

        today = datetime.today().date()  # Proper DATE object

        for _, row in merged.iterrows():
            if row['_merge'] == 'right_only':
                # New patient
                new_records.append({
                    'PatientID': row['PatientID'],
                    'FirstName': row['FirstName'],
                    'MiddleName': row['MiddleName'],
                    'LastName': row['LastName'],
                    'Gender': row['Gender'],
                    'DOB': row['DOB'],
                    'Age': row['Age'],
                    'hospital': row['hospital'],
                    'StartDate': today,
                    'EndDate': None,
                    'IsCurrent': True,
                    'Version': 1
                })

            elif row['_merge'] == 'both':
                changes = False
                for col in compare_columns:
                    col_hist = col + '_hist'
                    col_new = col + '_new'
                    if col_hist in row and col_new in row:
                        if pd.isna(row[col_hist]) and pd.isna(row[col_new]):
                            continue
                        elif row[col_hist] != row[col_new]:
                            changes = True
                            break

                if changes:
                    idx = self.historical_df[
                        (self.historical_df['PatientID'] == row['PatientID']) &
                        (self.historical_df['IsCurrent'] == True)
                    ].index
                    self.historical_df.loc[idx, 'IsCurrent'] = False
                    self.historical_df.loc[idx, 'EndDate'] = today

                    version = self.historical_df.loc[idx[0], 'Version'] + 1 if not idx.empty else 1

                    updated_records.append({
                        'PatientID': row['PatientID'],
                        'FirstName': row['FirstName_new'],
                        'MiddleName': row['MiddleName_new'],
                        'LastName': row['LastName_new'],
                        'Gender': row['Gender_new'],
                        'DOB': row['DOB_new'],
                        'Age': row['Age_new'],
                        'hospital': row['hospital_new'],
                        'StartDate': today,
                        'EndDate': None,
                        'IsCurrent': True,
                        'Version': version
                    })
                else:
                    unchanged_records.append(row['PatientID'])

        print(f"➕ New Records: {len(new_records)}")
        print(f"🔁 Updated Records: {len(updated_records)}")
        print(f"✅ Unchanged Records: {len(unchanged_records)}")

        final_df = pd.concat(
            [self.historical_df, pd.DataFrame(new_records + updated_records)],
            ignore_index=True
        )
        final_df.sort_values(by=['PatientID', 'Version'], inplace=True)

        # Save backup CSV as strings for readability
        final_df_csv = final_df.copy()
        final_df_csv['StartDate'] = final_df_csv['StartDate'].astype(str)
        final_df_csv['EndDate'] = final_df_csv['EndDate'].astype(str)
        final_df_csv.to_csv(self.output_file, index=False)
        print(f"📦 Final SCD2 file written to: {self.output_file}")

        # Load to BigQuery
        self.load_to_bigquery(final_df)

    def load_to_bigquery(self, df):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.service_account_path
        client = bigquery.Client(project=self.gcp_project)

        table_ref = f"{self.gcp_project}.{self.dataset_id}.{self.table_id}"

        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        # Partition by StartDate (DATE type)
        job_config.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="StartDate"
        )
        # Cluster by PatientID
        job_config.clustering_fields = ["PatientID"]

        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()

        print(f"✅ Data loaded to BigQuery table: {table_ref}")


if __name__ == "__main__":
    scd2 = SCD2Handler(
        historical_file="/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/dim_tables/dim_patient.csv",
        new_file="/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output/cleaned_patients.csv",
        output_file="/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output/dim_patient_history.csv",
        gcp_project="healthcare-rcm-467805",
        dataset_id="healthcare_rcm",
        table_id="dim_patient",
        service_account_path="/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/credentials/healthcare-rcm-467805-f5f313cc10f7.json"
    )
    scd2.load_data()
    scd2.process()
