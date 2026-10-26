import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(
    page_title='Enterprise MIS & Business Intelligence Dashboard',
    page_icon='📈',
    layout='wide',
)

engine = create_engine('sqlite:///business.db')

st.title('📈 Enterprise MIS & Business Intelligence Dashboard')
st.markdown(
    'Automated ETL Pipeline, Advanced SQL Analytics (CTEs & Window Functions)'
    '[cite: 3], and Interactive Management Reporting.'
)

# Load data & audit logs from database
df_orders = pd.read_sql('SELECT * FROM cleaned_orders', con=engine)
df_orders['order_total'] = df_orders['quantity'] * df_orders['price']
df_audit = pd.read_sql('SELECT * FROM etl_audit_log', con=engine)

# --- MIS DATA QUALITY AUDIT LOG SECTION ---
with st.expander('🛡️ MIS Data Governance & ETL Audit Log', expanded=True):
  st.markdown(
      'Pipeline hygiene metrics tracked automatically during ingestion and'
      ' transformation.'
  )
  cols = st.columns(4)
  cols[0].metric('Initial Raw Rows', int(df_audit['initial_rows'].iloc[0]))
  cols[1].metric('Duplicates Dropped', int(df_audit['duplicates_removed'].iloc[0]))
  cols[2].metric(
      'Missing Values Imputed', int(df_audit['missing_values_imputed'].iloc[0])
  )
  cols[3].metric('Final Clean Rows', int(df_audit['final_clean_rows'].iloc[0]))

st.markdown('---')

# --- SIDEBAR CONTROLS ---
st.sidebar.header('🔍 Interactive Controls')
products = df_orders['product'].unique().tolist()
selected_products = st.sidebar.multiselect(
    'Filter Products:', products, default=products
)

min_val, max_val = float(df_orders['order_total'].min()), float(
    df_orders['order_total'].max()
)
min_filter = st.sidebar.slider(
    'Minimum Order Total ($):',
    min_value=min_val,
    max_value=max_val,
    value=min_val,
)

filtered_df = df_orders[
    (df_orders['product'].isin(selected_products))
    & (df_orders['order_total'] >= min_filter)
]

# --- KPI METRIC CARDS ---
st.subheader('📊 Key Performance Indicators (KPIs)')
total_rev = filtered_df['order_total'].sum()
total_orders = len(filtered_df)
avg_order = filtered_df['order_total'].mean() if total_orders > 0 else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric('Filtered Revenue', f'${total_rev:,.2f}')
kpi2.metric('Total Orders', f'{total_orders}')
kpi3.metric('Average Order Value', f'${avg_order:,.2f}')

st.markdown('---')

# --- VISUALS & WINDOW FUNCTION ANALYTICS ---
col_left, col_right = st.columns(2)

with col_left:
  st.subheader('📊 Revenue Contribution by Product')
  if not filtered_df.empty:
    chart_data = filtered_df.groupby('product')['order_total'].sum()
    st.bar_chart(chart_data)
  else:
    st.info('No data available for selected filters.')

with col_right:
  st.subheader('📈 Running Cumulative Revenue (Window Function)')
  query_running = """
        WITH daily_sales AS (
            SELECT order_date, SUM(quantity * price) AS daily_revenue
            FROM cleaned_orders
            GROUP BY order_date
        )
        SELECT order_date,
               SUM(daily_revenue) OVER (ORDER BY order_date) AS running_total_revenue
        FROM daily_sales
        ORDER BY order_date;
    """
  df_running = pd.read_sql(query_running, con=engine)
  st.dataframe(df_running, use_container_width=True)

st.markdown('---')

# --- CLEANED DATA TABLE & EXPORT ---
st.subheader('📋 Filtered Orders & Management Export')
st.dataframe(filtered_df, use_container_width=True)

# One-Click MIS Export Button
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label='📥 Download Filtered Report as CSV (MIS Management Export)',
    data=csv_data,
    file_name='business_filtered_report.csv',
    mime='text/csv',
)
