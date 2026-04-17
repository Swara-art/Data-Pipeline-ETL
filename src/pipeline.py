import pandas as pd
import sqlite3
import logging
import os
from datetime import datetime
from sqlalchemy import create_engine

# --- CONFIGURATION ---
RAW_DATA_PATH = 'data/raw_sales_data.csv'
DB_PATH = 'data/warehouse.sqlite'
LOG_FILE = 'logs/etl.log'

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self):
        self.raw_df = None
        self.processed_df = None

    def extract(self):
        """Extract data from CSV source."""
        logger.info("Starting Extraction Phase...")
        try:
            if not os.path.exists(RAW_DATA_PATH):
                raise FileNotFoundError(f"Source file not found: {RAW_DATA_PATH}")
            
            self.raw_df = pd.read_csv(RAW_DATA_PATH)
            logger.info(f"Successfully extracted {len(self.raw_df)} records.")
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            raise

    def transform(self):
        """Transform raw data into a clean, warehouse-ready format."""
        logger.info("Starting Transformation Phase...")
        try:
            df = self.raw_df.copy()

            # 1. Data Cleaning: Drop rows with missing critical numbers
            initial_count = len(df)
            df = df.dropna(subset=['Quantity', 'UnitPrice'])
            dropped_count = initial_count - len(df)
            logger.info(f"Dropped {dropped_count} rows with missing values.")

            # 2. Fill missing Notes
            df['Note'] = df['Note'].fillna('No Special Instructions')

            # 3. Type Conversion
            df['OrderDate'] = pd.to_datetime(df['OrderDate'])

            # 4. Feature Engineering: Calculate Revenue
            df['TotalRevenue'] = df['Quantity'] * df['UnitPrice']
            
            # 5. Add Metadata: Processed Timestamp
            df['ProcessedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 6. Business Logic: Filter out zero orders (if any)
            df = df[df['TotalRevenue'] > 0]

            self.processed_df = df
            logger.info(f"Transformation complete. Prepared {len(df)} cleaned records.")
        except Exception as e:
            logger.error(f"Transformation failed: {str(e)}")
            raise

    def load(self):
        """Load cleaned data into SQLite database."""
        logger.info("Starting Loading Phase...")
        try:
            # Create SQLAlchemy engine
            engine = create_engine(f'sqlite:///{DB_PATH}')
            
            # Write to SQL (Replace if exists, or append if desired)
            self.processed_df.to_sql('sales_analytics', con=engine, if_exists='replace', index=False)
            
            logger.info(f"Successfully loaded data into {DB_PATH} (Table: sales_analytics).")
        except Exception as e:
            logger.error(f"Loading failed: {str(e)}")
            raise

    def run(self):
        """Execute the full ETL process."""
        try:
            logger.info("--- ETL PIPELINE START ---")
            self.extract()
            self.transform()
            self.load()
            logger.info("--- ETL PIPELINE COMPLETED SUCCESSFULLY ---")
        except Exception as e:
            logger.critical(f"FATAL: Pipeline failed. Check logs for details. Error: {e}")

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run()
