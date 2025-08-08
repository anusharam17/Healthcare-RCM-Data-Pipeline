import pandas as pd
import os
import logging

# Set up logging
log_path = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output/combine_patients.log"
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def combine_patients():
    try:
        base_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM"
        output_dir = os.path.join(base_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        hospital_a_path = os.path.join(output_dir, "a_patients.csv")
        hospital_b_path = os.path.join(output_dir, "b_patients.csv")
        combined_path = os.path.join(output_dir, "combined_patients.csv")

        df_a = pd.read_csv(hospital_a_path)
        df_b = pd.read_csv(hospital_b_path)
        logging.info(f"Loaded: {hospital_a_path} ({len(df_a)} rows)")
        logging.info(f"Loaded: {hospital_b_path} ({len(df_b)} rows)")

        df_a = df_a[[
            'PatientID', 'FirstName', 'LastName', 'MiddleName', 'SSN',
            'PhoneNumber', 'Gender', 'DOB', 'Address', 'ModifiedDate', 'HospitalName'
        ]].copy().dropna().drop_duplicates().head(5000)

        df_b = df_b.rename(columns={
            'ID': 'PatientID',
            'F_Name': 'FirstName',
            'L_Name': 'LastName',
            'M_Name': 'MiddleName'
        })[[
            'PatientID', 'FirstName', 'LastName', 'MiddleName', 'SSN',
            'PhoneNumber', 'Gender', 'DOB', 'Address', 'ModifiedDate', 'HospitalName'
        ]].copy().dropna().drop_duplicates().head(5000)

        df_a['PatientID'] = df_a['PatientID'].apply(lambda x: f"HOSP_A_{x}")
        df_b['PatientID'] = df_b['PatientID'].apply(lambda x: f"HOSP_B_{x}")

        logging.info(f"Cleaned Hospital A rows: {len(df_a)}")
        logging.info(f"Cleaned Hospital B rows: {len(df_b)}")

        combined_df = pd.concat([df_a, df_b], ignore_index=True)

        if combined_df.shape[0] != 10000:
            msg = f"Expected 10,000 rows but got {combined_df.shape[0]}"
            logging.warning(msg)
            print(f"[ERROR] Check logs: {msg}")
        else:
            logging.info("Combined patient data has 10,000 rows")

        combined_df.to_csv(combined_path, index=False)
        logging.info(f"Saved combined patient file: {combined_path}")
        print(f"✅ Combined file saved: {combined_path}")

    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        print(f"[CRITICAL ERROR] {str(e)} — Check logs!")

def check_claims():
    output_path = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output/combined_claims.csv"
    if os.path.exists(output_path):
        df = pd.read_csv(output_path)
        print(f"📊 Combined claims has {len(df)} rows.")
    else:
        print("[❌] Combined claims file not found.")


def combine_claims():
    try:
        base_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM"
        claims_dir = os.path.join(base_dir, "claims")
        output_path = os.path.join(base_dir, "output", "combined_claims.csv")

        claim_a_path = os.path.join(claims_dir, "hospital1_claim_data.csv")
        claim_b_path = os.path.join(claims_dir, "hospital2_claim_data.csv")

        df_a = pd.read_csv(claim_a_path)
        df_b = pd.read_csv(claim_b_path)

        logging.info(f"Loaded claims: {claim_a_path} ({len(df_a)} rows)")
        logging.info(f"Loaded claims: {claim_b_path} ({len(df_b)} rows)")

        df_a['Source'] = 'HospitalA'
        df_b['Source'] = 'HospitalB'

        # Optional: standardize column names or formats here
        combined_claims = pd.concat([df_a, df_b], ignore_index=True)
        logging.info(f"Combined claims total rows: {len(combined_claims)}")

        combined_claims.to_csv(output_path, index=False)
        logging.info(f"Saved combined claims: {output_path}")
        print(f"✅ Combined claims saved: {output_path}")

    except Exception as e:
        logging.error(f"Failed to combine claims: {str(e)}")
        print(f"[CRITICAL ERROR] Claims combining failed — see logs.")


if __name__ == "__main__":
    combine_patients()
    check_claims()
    combine_claims()
