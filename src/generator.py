import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_sample_data(output_path='data/raw_sales_data.csv'):
    # Create directory if not exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Configuration
    num_records = 100
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB-C Cable', 'Webcam', 'Headset']
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    # Generate random data
    data = {
        'OrderID': range(1001, 1001 + num_records),
        'Product': np.random.choice(products, num_records),
        'Quantity': np.random.randint(1, 10, num_records),
        'UnitPrice': np.round(np.random.uniform(10.0, 1500.0, num_records), 2),
        'OrderDate': [(datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d') for _ in range(num_records)],
        'Region': np.random.choice(regions, num_records),
        'Note': [np.random.choice([None, 'Urgent', 'Standard', 'Gift wrap'], p=[0.4, 0.2, 0.3, 0.1]) for _ in range(num_records)]
    }
    
    df = pd.DataFrame(data)
    
    # Add some null values for transformation demonstration
    df.loc[df.sample(frac=0.05).index, 'Quantity'] = np.nan
    df.loc[df.sample(frac=0.05).index, 'UnitPrice'] = np.nan
    
    df.to_csv(output_path, index=False)
    print(f"Sample data generated at: {output_path}")

if __name__ == "__main__":
    generate_sample_data()
