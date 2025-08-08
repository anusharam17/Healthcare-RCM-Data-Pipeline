import pandas as pd

# Generate date range
date_range = pd.date_range(start="2000-01-01", end="2030-12-31")

# Create dataframe with clean column names
df = pd.DataFrame({
    'date_key': date_range,
    'day': date_range.day,
    'month': date_range.month,
    'year': date_range.year,
    'quarter': date_range.quarter,
    'day_name': date_range.day_name(),
    'month_name': date_range.month_name(),
    'is_weekend': date_range.weekday >= 5
})

# Save to CSV
df.to_csv('/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/output/dim_date.csv', index=False)
print("✅ Clean dim_date.csv generated!")
