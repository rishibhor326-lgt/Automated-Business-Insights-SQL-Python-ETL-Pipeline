# Automated Business Insights & SQL/Python ETL Pipeline

An end-to-end data analytics project that cleans transactional data, stores structured records in SQLite, runs advanced SQL analysis, and presents business metrics through an interactive Streamlit dashboard.

## Live Demo

**Status:** The public dashboard has not been deployed yet.

To publish the app, open the [Streamlit Community Cloud deployment page](https://share.streamlit.io/deploy?repository=rishibhor326-lgt%2FAutomated-Business-Insights-SQL-Python-ETL-Pipeline&branch=main&mainModule=app.py), connect the repository, select `main` and `app.py`, and deploy. Add the generated public URL here after deployment succeeds.

## Overview

The project demonstrates a practical analytics workflow using Python, Pandas, SQL, SQLite, SQLAlchemy, and Streamlit.

### Key Features

- **Automated ETL:** Reads raw CSV data, removes exact duplicates, standardizes customer names, parses mixed date formats, validates numeric fields, and records data-quality checks.
- **Relational data storage:** Loads processed data and ETL audit metrics into SQLite using SQLAlchemy.
- **Advanced SQL analytics:** Uses CTEs, `SUM() OVER`, `RANK()`, and `ROW_NUMBER()` to analyze cumulative revenue, product rankings, and high-value orders.
- **Interactive dashboard:** Displays filtered revenue, order count, average order value, product revenue charts, and cumulative revenue trends.
- **Report export:** Lets users filter orders and download the results as a CSV file.
- **First-run setup:** Initializes the local database from the included sample CSV when the expected tables are not available.

## Dashboard

The dashboard provides data-quality metrics, KPI cards, product-level revenue analysis, cumulative revenue results, a filtered order table, and CSV export.

## Workflow

```text
raw_data.csv
    ↓
Python + Pandas ETL
    ├── Duplicate removal and data standardization
    ├── Date and numeric validation
    └── ETL audit metrics
    ↓
SQLite database (SQLAlchemy)
    ↓
Advanced SQL analytics
    ↓
Streamlit MIS dashboard
    ↓
Filtered CSV report
```

## Technology Stack

| Area | Technologies |
|---|---|
| Programming and data processing | Python, Pandas |
| Database | SQLite, SQLAlchemy |
| Analytics | SQL, CTEs, window functions, aggregations |
| Dashboard | Streamlit |
| Data export | CSV |
| Version control | Git, GitHub |

## Repository Structure

| File | Purpose |
|---|---|
| `raw_data.csv` | Sample transactional dataset |
| `etl_pipeline.py` | Cleans and loads data and records ETL audit metrics |
| `sql_analytics.py` | Executes SQL analytics queries |
| `app.py` | Runs the interactive dashboard |
| `requirements.txt` | Lists Python dependencies |
| `.gitignore` | Excludes local databases and environment files |

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/rishibhor326-lgt/Automated-Business-Insights-SQL-Python-ETL-Pipeline.git
cd Automated-Business-Insights-SQL-Python-ETL-Pipeline
```

### 2. Create a virtual environment

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

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the ETL pipeline

```bash
python etl_pipeline.py
```

The script creates `business.db` and writes the `cleaned_orders` and `etl_audit_log` tables.

### 5. Run the SQL analytics

```bash
python sql_analytics.py
```

### 6. Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Sample Data Notes

The included dataset contains six raw rows. The ETL pipeline removes one exact duplicate, fills one missing customer name, and loads five cleaned rows. The sample dashboard displays **$1,836.00** in total order value across those five rows using the current sample data.

These values describe the bundled demonstration dataset only; they are not real business performance results.

## Limitations

- The project uses a small sample dataset to demonstrate the workflow.
- SQLite is used for local and demo purposes; production use may require a managed database, access controls, monitoring, and operational safeguards.
- Dashboard currency labels use dollars in the current example. Confirm currency and metric definitions before adapting the project to another dataset.
- Invalid dates and non-numeric quantity or price values are recorded during ETL and should be reviewed before relying on date-based analysis.

## Author

**Rishi Bhor**

[GitHub](https://github.com/rishibhor326-lgt/) · [LinkedIn](https://www.linkedin.com/in/rishi-bhor-02a23b289/)
