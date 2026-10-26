# 📈 Enterprise Business Insights & Automated ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Data Governance](https://img.shields.io/badge/MIS-Audit%20Logging-green)

A production-grade, end-to-end data engineering and business intelligence application built to automate data ingestion, enforce strict MIS data governance, execute advanced SQL analytics, and serve real-time management reports.

---

## 🚀 Key Architectural Features

### 1. 🛡️ Automated ETL Pipeline & MIS Audit Governance (`etl_pipeline.py`)
* Programmatically ingests raw operational CSV data.
* Handles data cleansing: detects and drops duplicates, imputes missing values, and standardizes mixed date formats.
* **MIS Governance Logging:** Automatically writes pipeline health metadata (initial row counts, duplicates removed, missing values imputed, and final clean rows) to an `etl_audit_log` table.

### 2. ⚡ Advanced SQL Analytics Layer (`sql_analytics.py`)
* Queries relational SQLite tables using advanced database features:
  * **Common Table Expressions (CTEs):** Modularized subquery blocks for clean financial aggregation.
  * **Window Functions (`SUM() OVER`, `RANK()`):** Computes running cumulative revenues over time and product revenue tiers.

### 3. 📊 Interactive Management Web App (`app.py`)
* Built with **Streamlit** for real-time interactive business reporting.
* Features dynamic sidebar product filters and order value sliders.
* Includes a **One-Click Management Export Button (`st.download_button`)** enabling stakeholders to instantly download filtered datasets as clean CSV reports.

---

## 🛠️ Tech Stack
* **Languages & Libraries:** Python, Pandas, SQLAlchemy, Streamlit
* **Database & Storage:** SQLite, Relational Tables
* **DevOps & Version Control:** Git, GitHub

---

## ⚙️ Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/rishibhor326-lgt/Automated-Business-Insights-SQL-Python-ETL-Pipeline.git](https://github.com/rishibhor326-lgt/Automated-Business-Insights-SQL-Python-ETL-Pipeline.git)
   cd Automated-Business-Insights-SQL-Python-ETL-Pipeline
