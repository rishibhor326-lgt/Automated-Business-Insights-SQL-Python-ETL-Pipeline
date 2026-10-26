"""Streamlit dashboard for ETL quality metrics and business reporting."""
from pathlib import Path
import subprocess
import sys

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, inspect

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "business.db"
ETL_SCRIPT = BASE_DIR / "etl_pipeline.py"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

st.set_page_config(
    page_title="Automated Business Insights",
    page_icon="📈",
    layout="wide",
)


def database_is_ready() -> bool:
    """Return True when the local database contains both expected tables."""
    if not DATABASE_PATH.exists():
        return False

    engine = create_engine(DATABASE_URL)
    try:
        tables = set(inspect(engine).get_table_names())
        return {"cleaned_orders", "etl_audit_log"}.issubset(tables)
    except Exception:
        return False
    finally:
        engine.dispose()


def ensure_database() -> None:
    """Create the SQLite database automatically on first launch."""
    if database_is_ready():
        return

    with st.spinner("Preparing the sample data and SQLite database..."):
        result = subprocess.run(
            [sys.executable, str(ETL_SCRIPT)],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

    if result.returncode != 0:
        st.error("The data pipeline could not initialise the dashboard.")
        details = (result.stdout or "") + "\n" + (result.stderr or "")
        with st.expander("ETL diagnostic output"):
            st.code(details.strip() or "No diagnostic output was returned.")
        st.stop()


ensure_database()

engine = create_engine(DATABASE_URL)
try:
    df_orders = pd.read_sql_query("SELECT * FROM cleaned_orders", con=engine)
    df_audit = pd.read_sql_query("SELECT * FROM etl_audit_log", con=engine)
    running_query = """
        WITH daily_sales AS (
            SELECT order_date, SUM(quantity * price) AS daily_revenue
            FROM cleaned_orders
            WHERE order_date IS NOT NULL
            GROUP BY order_date
        )
        SELECT
            order_date,
            daily_revenue,
            SUM(daily_revenue) OVER (
                ORDER BY order_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS running_total_revenue
        FROM daily_sales
        ORDER BY order_date;
    """
    df_running = pd.read_sql_query(running_query, con=engine)
finally:
    engine.dispose()

if df_orders.empty:
    st.warning("The cleaned dataset is empty. Check raw_data.csv and rerun the ETL pipeline.")
    st.stop()

df_orders["quantity"] = pd.to_numeric(df_orders["quantity"], errors="coerce")
df_orders["price"] = pd.to_numeric(df_orders["price"], errors="coerce")
df_orders["order_total"] = df_orders["quantity"] * df_orders["price"]
df_orders = df_orders.dropna(subset=["order_total"]).copy()

if df_orders.empty:
    st.warning("No valid order totals are available in the cleaned dataset.")
    st.stop()

st.title("📈 Automated Business Insights")
st.caption(
    "A portfolio demonstration combining a Python/Pandas ETL pipeline, "
    "SQLite analytics, SQL window functions, and interactive MIS reporting."
)

# Data-quality and ETL audit metrics.
with st.expander("🛡️ Data Governance & ETL Audit", expanded=True):
    audit = df_audit.iloc[0]
    audit_cols = st.columns(4)
    audit_cols[0].metric("Initial Raw Rows", f"{int(audit['initial_rows']):,}")
    audit_cols[1].metric("Duplicates Removed", f"{int(audit['duplicates_removed']):,}")
    audit_cols[2].metric("Missing Values Imputed", f"{int(audit['missing_values_imputed']):,}")
    audit_cols[3].metric("Final Clean Rows", f"{int(audit['final_clean_rows']):,}")
    if "invalid_dates" in df_audit.columns or "invalid_sales_rows" in df_audit.columns:
        invalid_dates = int(audit.get("invalid_dates", 0))
        invalid_sales_rows = int(audit.get("invalid_sales_rows", 0))
        st.caption(
            f"Additional checks — invalid dates: {invalid_dates:,}; "
            f"rows with invalid quantity/price: {invalid_sales_rows:,}."
        )

st.sidebar.header("🔍 Interactive Filters")
available_products = sorted(
    df_orders["product"].dropna().astype(str).unique().tolist()
)
selected_products = st.sidebar.multiselect(
    "Products",
    options=available_products,
    default=available_products,
)
min_total = float(df_orders["order_total"].min())
max_total = float(df_orders["order_total"].max())

if min_total < max_total:
    minimum_order_total = st.sidebar.slider(
        "Minimum order total ($)",
        min_value=min_total,
        max_value=max_total,
        value=min_total,
        step=1.0,
    )
else:
    minimum_order_total = min_total
    st.sidebar.caption("All valid orders have the same total.")

filtered_df = df_orders[
    df_orders["product"].astype(str).isin(selected_products)
    & (df_orders["order_total"] >= minimum_order_total)
].copy()

total_revenue = float(filtered_df["order_total"].sum())
order_count = int(len(filtered_df))
average_order_value = total_revenue / order_count if order_count else 0.0

st.subheader("📊 Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Filtered Revenue", f"${total_revenue:,.2f}")
kpi2.metric("Orders", f"{order_count:,}")
kpi3.metric("Average Order Value", f"${average_order_value:,.2f}")

st.divider()
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Revenue by Product")
    if filtered_df.empty:
        st.info("No rows match the current filters.")
    else:
        product_revenue = (
            filtered_df.groupby("product", dropna=False)["order_total"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(product_revenue)

with right_col:
    st.subheader("Cumulative Revenue by Date")
    if df_running.empty:
        st.info("No valid order dates are available for the running-total chart.")
    else:
        chart_data = df_running.set_index("order_date")["running_total_revenue"]
        st.line_chart(chart_data)
        with st.expander("View SQL window-function results"):
            st.dataframe(df_running, use_container_width=True, hide_index=True)

st.divider()
st.subheader("📋 Filtered Orders & Report Export")
display_columns = [
    column for column in
    ["order_id", "customer_name", "order_date", "product", "quantity", "price", "order_total"]
    if column in filtered_df.columns
]
st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
)
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download filtered report (CSV)",
    data=csv_data,
    file_name="business_filtered_report.csv",
    mime="text/csv",
    disabled=filtered_df.empty,
)

st.caption(
    "Sample transactional data is included for demonstration. "
    "Validate data definitions and currency before using this pattern with business data."
)
