"""Clean raw business orders, log data-quality metrics, and load SQLite tables."""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = BASE_DIR / "raw_data.csv"
DATABASE_PATH = BASE_DIR / "business.db"

REQUIRED_COLUMNS = {
    "order_id",
    "customer_name",
    "order_date",
    "product",
    "quantity",
    "price",
}


def run_etl() -> None:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Required input file was not found: {RAW_DATA_PATH.name}"
        )

    print(f"Reading raw data from {RAW_DATA_PATH.name}...")
    df = pd.read_csv(RAW_DATA_PATH)

    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input CSV is missing required columns: {columns}")

    initial_count = len(df)
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Treat null and whitespace-only customer names as missing.
    customer_names = df["customer_name"].astype("string").str.strip()
    customer_names = customer_names.mask(customer_names.eq(""), pd.NA)
    missing_names_count = int(customer_names.isna().sum())
    df["customer_name"] = customer_names.fillna("Unknown").str.title()

    # Accept mixed source date formats and standardize valid dates to ISO format.
    parsed_dates = pd.to_datetime(
        df["order_date"], format="mixed", errors="coerce"
    )
    invalid_dates_count = int(parsed_dates.isna().sum())
    df["order_date"] = parsed_dates.dt.strftime("%Y-%m-%d")

    # Ensure fields used in sales calculations are numeric.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    invalid_sales_rows = int(df[["quantity", "price"]].isna().any(axis=1).sum())

    final_count = len(df)
    audit_df = pd.DataFrame(
        [
            {
                "initial_rows": initial_count,
                "duplicates_removed": duplicate_count,
                "missing_values_imputed": missing_names_count,
                "invalid_dates": invalid_dates_count,
                "invalid_sales_rows": invalid_sales_rows,
                "final_clean_rows": final_count,
                "etl_status": "SUCCESS",
                "processed_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        ]
    )

    database_url = f"sqlite:///{DATABASE_PATH.as_posix()}"
    engine = create_engine(database_url)
    try:
        with engine.begin() as connection:
            df.to_sql(
                "cleaned_orders",
                con=connection,
                if_exists="replace",
                index=False,
            )
            audit_df.to_sql(
                "etl_audit_log",
                con=connection,
                if_exists="replace",
                index=False,
            )
    finally:
        engine.dispose()

    print("\nETL completed successfully.")
    print(f"Rows read: {initial_count}")
    print(f"Duplicate rows removed: {duplicate_count}")
    print(f"Missing customer names filled: {missing_names_count}")
    print(f"Invalid dates coerced to missing: {invalid_dates_count}")
    print(f"Rows with invalid quantity/price: {invalid_sales_rows}")
    print(f"Cleaned rows loaded: {final_count}")
    print(f"SQLite database: {DATABASE_PATH.name}")
    print("Tables created: cleaned_orders, etl_audit_log")


if __name__ == "__main__":
    run_etl()
