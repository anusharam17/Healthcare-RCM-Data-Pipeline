import pandas as pd
import os
import logging

class DataExtractorCleaner:
    def __init__(self, data_dir="../output", claims_dir="../claims"):
        self.data_dir = data_dir
        self.claims_dir = claims_dir
        self.setup_logging()

    def setup_logging(self):
        logs_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(logs_dir, exist_ok=True)

        logging.basicConfig(
            filename=os.path.join(logs_dir, "data_extraction_cleaning.log"),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def read_and_combine(self, path1, path2, subset_col=None):
        try:
            df1 = pd.read_csv(path1)
            df2 = pd.read_csv(path2)

            combined_df = pd.concat([df1, df2], ignore_index=True)

            # Strip column names and remove spaces
            combined_df.columns = combined_df.columns.str.strip()

            # Drop rows with any null values
            combined_df.dropna(inplace=True)

            # Drop duplicates (use specific column subset if provided)
            if subset_col:
                combined_df.drop_duplicates(subset=subset_col, inplace=True)
            else:
                combined_df.drop_duplicates(inplace=True)

            return combined_df

        except Exception as e:
            logging.error(f"❌ Error reading or combining files: {path1}, {path2} -> {e}")
            return pd.DataFrame()

    def extract_and_clean_entity(self, entity, subset_col=None):
        path_a = os.path.join(self.data_dir, f'a_{entity}.csv')
        path_b = os.path.join(self.data_dir, f'b_{entity}.csv')
        combined_df = self.read_and_combine(path_a, path_b, subset_col=subset_col)

        if not combined_df.empty:
            output_path = os.path.join(self.data_dir, f'combined_{entity}.csv')
            combined_df.to_csv(output_path, index=False)
            logging.info(f"✅ Combined and cleaned {entity}: {combined_df.shape[0]} rows")
        else:
            logging.warning(f"⚠️ No data extracted for {entity}")
        return combined_df

    def extract_and_clean_claims(self):
        path1 = os.path.join(self.claims_dir, "hospital1_claim_data.csv")
        path2 = os.path.join(self.claims_dir, "hospital2_claim_data.csv")
        combined_df = self.read_and_combine(path1, path2, subset_col="claim_id")

        if not combined_df.empty:
            output_path = os.path.join(self.data_dir, 'combined_claims.csv')
            combined_df.to_csv(output_path, index=False)
            logging.info(f"✅ Combined and cleaned claims: {combined_df.shape[0]} rows")
        else:
            logging.warning("⚠️ No claims data extracted.")
        return combined_df

if __name__ == "__main__":
    extractor = DataExtractorCleaner()
    entities = {
        'patients': 'patient_id',
        'providers': 'provider_id',
        'transactions': 'transaction_id',
        'encounters': 'encounter_id'
    }

    for entity, id_col in entities.items():
        print(f"Processing {entity}...")
        extractor.extract_and_clean_entity(entity, subset_col=id_col)

    print("Processing claims...")
    extractor.extract_and_clean_claims()
    print("✅ All files combined and cleaned successfully.")
