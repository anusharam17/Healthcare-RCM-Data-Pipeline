from etl.extractor import DataExtractorCleaner

# Paths for data and claims
output_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output"
claims_dir = "/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/claims"

# Initialize extractor
extractor = DataExtractorCleaner(data_dir=output_dir, claims_dir=claims_dir)

# Entities and their unique ID columns
entities = {
    'patients': 'PatientID',
    'providers': 'ProviderID',
    'transactions': 'TransactionID',
    'encounters': 'EncounterID'
}

# Process each entity and print row count
for entity, id_col in entities.items():
    print(f"Processing {entity}...")
    df = extractor.extract_and_clean_entity(entity, subset_col=id_col)
    print(f"✅ {entity}: {len(df)} rows after cleaning")

# Process claims
print("Processing claims...")
df_claims = extractor.extract_and_clean_claims()
print(f"✅ claims: {len(df_claims)} rows after cleaning")

print("✅ All files combined and cleaned successfully.")
