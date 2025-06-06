﻿#  Airbnb NYC Data Engineering Project

This is a complete data engineering pipeline built to clean, transform, enrich, and prepare the Airbnb NYC dataset for analysis, machine learning, and visualization.

---

## What This Project Includes

This project walks through the following steps:

1. **Ingest raw CSV** into the project
2. **Clean and repair data** (handling missing, incorrect, or duplicate values)
3. **Engineer useful features** using NumPy and Pandas
4. **Normalize and scale numeric features** using MinMaxScaler
5. **Label listings** based on demand logic
6. **Save the final dataset** for future use in SQL or Power BI

---

##  Folder Structure
airbnb_project/
├── scripts/ # All Python scripts
│ ├── ingest_data.py # Loads raw file into /data/raw/
│ ├── clean_data.py # Cleans and filters the data
│ ├── metrics_summary.py # Feature engineering, normalization, labeling
│ └── load_to_sql.py # (To be created) Load final data to SQL DB
│
├── data/
│ ├── raw/ # Contains original Airbnb_Open_Data.csv
│ └── cleaned/ # Contains cleaned and final datasets
│ ├── airbnb_cleaned.csv
│ └── airbnb_with_features.csv
│
├── config/
│ └── db_config.yaml # Database config (for future SQL load)
│
├── notebooks/ # (Optional) Jupyter notebooks for exploration
│ └── airbnb_exploration.ipynb
│
└── README.md # This file


---

##  Features We Created

| Feature Name              | Description |
|--------------------------|-------------|
| `log_total_cost`         | Log-transformed total cost to reduce skew |
| `price_bucket`           | Categorized prices into groups: Very Low → Luxury |
| `price_per_min_stay`     | Price divided by minimum nights |
| `price_rank_within_area` | Rank of listing within its neighborhood |
| `*_scaled` columns       | Normalized features (0–1) using MinMaxScaler |
| `is_high_demand_listing` | Labeled listings as high demand based on reviews, availability, and pricing |

---

##  Tools Used

- Python 3.11
- Pandas, NumPy
- Scikit-learn (MinMaxScaler)
- GitHub for version control
- PowerShell for script execution

---
## 🔍 SQL Analysis
Saved all medium-to-advanced queries in `analysis/airbnb_sql_queries.sql`, including:
- Price-based insights
- Room type trends
- Host activity and review metrics
- Anomaly detection


##  Author

**Keerthana Take**  
Data Engineer 
