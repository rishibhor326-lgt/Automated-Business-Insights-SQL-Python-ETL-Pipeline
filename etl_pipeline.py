import pandas as pd
from sqlalchemy import create_engine

print("1. Reading raw data...")
df = pd.read_csv('raw_data.csv')
initial_count = len(df)

print("\n--- BEFORE CLEANING ---")
print(df)

# 2. Data Cleaning & Governance Steps
# A. Track and remove duplicate rows
duplicates_count = df.duplicated().sum()
df = df.drop_duplicates()

# B. Track and fill missing values
missing_names_count = df['customer_name'].isna().sum()
df['customer_name'] = df['customer_name'].fillna('Unknown')

# C. Standardize text format
df['customer_name'] = df['customer_name'].str.title()

# D. Standardize date format using mixed format support
df['order_date'] = pd.to_datetime(
    df['order_date'], format='mixed', errors='coerce'
).dt.strftime('%Y-%m-%d')

final_count = len(df)

print("\n--- AFTER CLEANING ---")
print(df)

# Create MIS Audit Metadata Table
audit_df = pd.DataFrame([{
    'initial_rows': initial_count,
    'duplicates_removed': duplicates_count,
    'missing_values_imputed': missing_names_count,
    'final_clean_rows': final_count,
    'etl_status': 'SUCCESS',
}])

# 3. Load Phase: Save cleaned data and audit log into SQLite database
print(
    '\n3. Loading cleaned data and MIS audit logs into the database...'
)
engine = create_engine('sqlite:///business.db')
df.to_sql('cleaned_orders', con=engine, if_exists='replace', index=False)
audit_df.to_sql('etl_audit_log', con=engine, if_exists='replace', index=False)
print('ETL Pipeline executed successfully with full data governance logging!')

