"""Run SQL-based business analytics against the cleaned SQLite data."""
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, inspect

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "business.db"

if not DATABASE_PATH.exists():
    raise SystemExit(
        "business.db was not found. Run 'python etl_pipeline.py' first."
    )

engine = create_engine(f"sqlite:///{DATABASE_PATH.as_posix()}")
if not inspect(engine).has_table("cleaned_orders"):
    engine.dispose()
    raise SystemExit(
        "The cleaned_orders table was not found. Run 'python etl_pipeline.py' first."
    )

queries = {
    "Running cumulative revenue by date (CTE + SUM OVER)": """
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
    """,
    "Product revenue ranking (CTE + RANK)": """
        WITH product_totals AS (
            SELECT product, SUM(quantity * price) AS total_revenue
            FROM cleaned_orders
            GROUP BY product
        )
        SELECT
            product,
            total_revenue,
            RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
        FROM product_totals
        ORDER BY revenue_rank, product;
    """,
    "Highest-value order per product (ROW_NUMBER)": """
        WITH ranked_orders AS (
            SELECT
                order_id,
                customer_name,
                product,
                order_date,
                quantity * price AS order_total,
                ROW_NUMBER() OVER (
                    PARTITION BY product
                    ORDER BY quantity * price DESC, order_id
                ) AS product_order_number
            FROM cleaned_orders
        )
        SELECT *
        FROM ranked_orders
        WHERE product_order_number = 1
        ORDER BY product;
    """,
    "High-value orders (order total greater than $100)": """
        SELECT
            order_id,
            customer_name,
            product,
            order_date,
            quantity,
            price,
            quantity * price AS order_total
        FROM cleaned_orders
        WHERE quantity * price > 100
        ORDER BY order_total DESC;
    """,
}

try:
    for title, query in queries.items():
        print(f"\n=== {title} ===")
        result = pd.read_sql_query(query, con=engine)
        if result.empty:
            print("No rows matched this query.")
        else:
            print(result.to_string(index=False))
finally:
    engine.dispose()
