# Automated Business Insights & SQL/Python ETL Pipeline

An end-to-end MIS and business intelligence project that transforms raw order data into validated records, performs SQL-based revenue analysis, and presents management-ready metrics through an interactive Streamlit dashboard.

## Dashboard Preview

<p align="center">
  <img src="assets/screenshots/01_dashboard_overview.png" alt="Enterprise MIS dashboard overview with ETL audit metrics and KPI cards" width="100%">
</p>

<p align="center"><strong>Executive overview — data-quality checks, revenue KPIs, and product-level performance</strong></p>

<p align="center">
  <img src="assets/screenshots/02_revenue_analytics.png" alt="Revenue contribution by product and cumulative revenue analysis using a SQL window function" width="49%">
  <img src="assets/screenshots/03_filtered_orders_export.png" alt="Filtered orders management table and CSV export control" width="49%">
</p>

<p align="center"><strong>Revenue analysis, cumulative totals, filtered order details, and report export</strong></p>

## Project Overview

The pipeline demonstrates a practical reporting workflow: ingest transactional data, clean and validate it, store the results in SQLite, query business metrics with SQL, and expose the results through a dashboard.

### Key Capabilities

- **ETL and data quality:** removes duplicate records, standardizes missing customer names, validates fields, and records pipeline audit metrics.
- **SQL analytics:** uses common table expressions (CTEs), aggregations, and window functions to calculate cumulative revenue and analyze product performance.
- **Management KPIs:** presents filtered revenue, total orders, and average order value.
- **Interactive reporting:** displays product revenue contributions and a filtered order-level table.
- **CSV export:** allows users to download the currently filtered order report for further analysis.
- **Local reproducibility:** includes sample data and scripts to run the pipeline and dashboard on a local machine.

## Results on the Included Sample Dataset

| Data-quality / reporting measure | Demonstration result |
|---|---:|
| Initial raw rows | 6 |
| Duplicate rows removed | 1 |
| Missing customer names filled | 1 |
| Final cleaned rows | 5 |
| Total order value shown | $1,836.00 |
| Orders in the cleaned sample | 5 |
| Average order value shown | $367.20 |

These are outputs from the bundled demonstration data, not real company performance results.

## Workflow

```text
raw_data.csv
    ↓
Python + Pandas ETL
    ├── Duplicate removal and standardization
    ├── Date and numeric validation
    └── Data-quality audit metrics
    ↓
SQLite database (SQLAlchemy)
    ↓
SQL analysis (CTEs, aggregations, window functions)
    ↓
Streamlit MIS dashboard
    ↓
Filtered CSV management report
```

## Technology Stack

| Area | Tools |
|---|---|
| Programming and data processing | Python, Pandas |
| Database | SQLite, SQLAlchemy |
| Querying and analytics | SQL, CTEs, window functions, aggregations |
| Dashboard | Streamlit |
| Data exchange | CSV |
| Version control | Git, GitHub |

## Repository Structure

| File | Purpose |
|---|---|
| `raw_data.csv` | Sample transactional data |
| `etl_pipeline.py` | Cleans and loads records and writes ETL audit metrics |
| `sql_analytics.py` | Runs SQL-based business analysis |
| `app.py` | Interactive MIS dashboard and filtered report export |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes local and environment files |

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/rishibhor326-lgt/Automated-Business-Insights-SQL-Python-ETL-Pipeline.git
cd Automated-Business-Insights-SQL-Python-ETL-Pipeline
```

### 2. Create and activate a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

### 3. Install dependencies and run the pipeline

```bash
python -m pip install -r requirements.txt
python etl_pipeline.py
python sql_analytics.py
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Notes and Limitations

- The included dataset is intentionally small and is meant to demonstrate the workflow.
- The SQLite database is suitable for a local demonstration; production deployments may require a managed database, access controls, and monitoring.
- The sample dashboard displays dollar-denominated values. Confirm currency and metric definitions before using the project with other data.
- Review ETL validation logs and source-data quality before relying on results for operational decisions.

## Author

**Rishi Bhor**

[GitHub](https://github.com/rishibhor326-lgt/) · [LinkedIn](https://www.linkedin.com/in/rishi-bhor-02a23b289/)
