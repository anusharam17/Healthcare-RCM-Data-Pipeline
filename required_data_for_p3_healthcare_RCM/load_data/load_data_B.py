import pandas as pd
import mysql.connector
import os

# --- Database config ---
db_name = 'hospital_b_db'
data_path = 'hospital_dbs/hospital-b'

# --- Connect to MySQL ---
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='anuram@2003', 
    database=db_name
)
cursor = conn.cursor()

# --- Table to CSV mapping ---
table_files = {
    'patients': 'patients.csv',
    'providers': 'providers.csv',
    'departments': 'departments.csv',
    'transactions': 'transactions.csv',
    'encounters': 'encounters.csv'
}

for table_name, filename in table_files.items():
    print(f"\n⏳ Loading data into: {table_name}")
    file_path = os.path.join(data_path, filename)

    df = pd.read_csv(file_path)

    # Optional: Uncomment to clear old data
    # cursor.execute(f"TRUNCATE TABLE {table_name}")

    for _, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.index)
        sql = f"INSERT IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))

    conn.commit()
    print(f"✅ Inserted {len(df)} rows into {table_name} (duplicates skipped)")

conn.close()
print("\n🎉 All data for hospital_a_db loaded successfully!")
