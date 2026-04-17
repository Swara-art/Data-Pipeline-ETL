# Mini ETL Data Pipeline

A lightweight ETL (Extract, Transform, Load) pipeline built with Python to process sales data and load it into a structured database.

## Project Goal
Demonstrate a modular approach to data engineering by extracting raw sales data, performing cleaning and enrichment, and storing the results in a SQLite data warehouse for analytical use.

## Features
- **Extraction**: Reads raw data from CSV files using Pandas.
- **Transformation**:
  - Handles missing values (removes invalid data).
  - Normalizes text fields.
  - Formats date strings to DateTime objects.
  - Performs feature engineering (Calculates `TotalRevenue`).
  - Adds processing metadata (`ProcessedAt` timestamp).
- **Loading**: Persists the cleaned data to a SQLite database (`warehouse.sqlite`) using SQLAlchemy.
- **Logging**: Detailed logging of every stage into `logs/etl.log`.

## Directory Structure
```text
ETL Data Pipeline/
├── data/               # Raw and processed data storage
├── logs/               # Application log files
├── src/
│   ├── generator.py    # Generates sample sales data CSV
│   └── pipeline.py     # Main ETL logic script
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Sample Data**:
   ```bash
   python src/generator.py
   ```

3. **Run the ETL Pipeline**:
   ```bash
   python src/pipeline.py
   ```

## Deliverables
- **Python ETL Script**: Located at `src/pipeline.py`.
- **Sample Dataset**: Generated at `data/raw_sales_data.csv`.
- **DB Output**: Created at `data/warehouse.sqlite`.
- **Documentation**: This README.
