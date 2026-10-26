import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///business.db')

print('=== ENTERPRISE ADVANCED SQL ANALYTICS REPORT ===')

# 1. Advanced Query using CTE & Window Functions (Running Cumulative Revenue)
print('\n1. Running Cumulative Revenue Over Time (CTE + Window Function):')
query_window = """
    WITH daily_sales AS (
        SELECT order_date, 
               SUM(quantity * price) AS daily_revenue
        FROM cleaned_orders
        GROUP BY order_date
    )
    SELECT order_date,
           daily_revenue,
           SUM(daily_revenue) OVER (ORDER BY order_date) AS running_total_revenue
    FROM daily_sales
    ORDER BY order_date;
"""
df_window = pd.read_sql(query_window, con=engine)
print(df_window)

# 2. Product Revenue Ranking using Window Function RANK()
print('\n2. Product Revenue Ranking (Window Function RANK()):')
query_rank = """
    WITH product_totals AS (
        SELECT product,
               SUM(quantity * price) AS total_revenue
        FROM cleaned_orders
        GROUP BY product
    )
    SELECT product,
           total_revenue,
           RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
    FROM product_totals;
"""
df_rank = pd.read_sql(query_rank, con=engine)
print(df_rank)

