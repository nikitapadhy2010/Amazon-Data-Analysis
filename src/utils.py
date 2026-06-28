import os
import sys
import time
import logging
import pandas as pd
import numpy as np
from pathlib import Path

# Create directories if they don't exist
Path("output/reports").mkdir(parents=True, exist_ok=True)
Path("output/cleaned_data").mkdir(parents=True, exist_ok=True)
Path("output/charts").mkdir(parents=True, exist_ok=True)

# Set up logging to both console and log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("output/reports/data_processing.log", mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

PRODUCT_TO_SUBCATEGORY = {
    'Drone Mini': 'Drones & Robotics',
    'Wireless Earbuds': 'Audio Accessories',
    'Bluetooth Speaker': 'Audio Accessories',
    'Noise Cancelling Headphones': 'Audio Accessories',
    'Microphone': 'Audio Accessories',
    'Car Charger': 'Power Accessories',
    'USB-C Charger': 'Power Accessories',
    'Wireless Charger': 'Power Accessories',
    'Power Bank 20000mAh': 'Power Accessories',
    'HDMI Cable 2m': 'Cables & Connectivity',
    'Smartwatch': 'Wearables',
    'Fitness Band': 'Wearables',
    'Air Fryer': 'Kitchen Appliances',
    'Electric Kettle': 'Kitchen Appliances',
    'Instant Pot': 'Kitchen Appliances',
    'Vacuum Cleaner': 'Home Appliances',
    'T-Shirt': 'Apparel',
    'Jeans': 'Apparel',
    'Winter Jacket': 'Apparel',
    'Dress Shirt': 'Apparel',
    'Running Shoes': 'Footwear',
    'Sunglasses': 'Fashion Accessories',
    'Backpack': 'Travel Bags',
    'Yoga Mat': 'Fitness Gear',
    'Water Bottle': 'Hydration',
    'Novel Bestseller': 'Fiction Literature',
    "Children's Book": "Children's Literature",
    'Kids Toy Car': 'Toys',
    'Board Game': 'Games',
    'Puzzle 1000pc': 'Games',
    'Desk Plant': 'Home Decor',
    'LED Desk Lamp': 'Home Lighting',
    'Smart Light Bulb': 'Home Lighting',
    'Office Chair': 'Office Furniture',
    'Desk Organizer': 'Office Accessories',
    '4K Monitor': 'Computer Displays',
    'Webcam Full HD': 'Computer Peripherals',
    'Mechanical Keyboard': 'Computer Input',
    'Gaming Mouse': 'Computer Input',
    'Portable SSD 1TB': 'Data Storage',
    'External HDD 2TB': 'Data Storage',
    'Memory Card 128GB': 'Data Storage',
    'Graphic Tablet': 'Creative Input',
    'Router': 'Networking Devices',
    'Smartphone Case': 'Mobile Accessories',
    'Phone Tripod': 'Mobile Accessories',
    'Laptop Sleeve': 'Computer Accessories',
    'Projector Mini': 'Home & Office Entertainment',
    'Cookware Set': 'Kitchenware',
    'Action Camera': 'Camera Accessories'
}

# Cost Margins per Category (used to compute Cost Price and Profit)
# Gross margin = 1 - CostMargin. e.g. Books has 30% margin, Electronics has 15% margin
CATEGORY_COST_MARGINS = {
    'Books': 0.70,          # 30% base margin
    'Electronics': 0.85,    # 15% base margin
    'Clothing': 0.60,       # 40% base margin
    'Toys & Games': 0.75,   # 25% base margin
    'Sports & Outdoors': 0.78, # 22% base margin
    'Home & Kitchen': 0.72   # 28% base margin
}

def load_data(file_path: str) -> pd.DataFrame:
    """
    Safely loads the Excel file into a pandas DataFrame.
    """
    start_time = time.time()
    logging.info(f"Attempting to load dataset from: {file_path}")
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")
        
        # Load the sheet 'Amazon'
        df = pd.read_excel(file_path, sheet_name='Amazon')
        elapsed = time.time() - start_time
        logging.info(f"Successfully loaded dataset of shape {df.shape} in {elapsed:.2f} seconds.")
        return df
    except Exception as e:
        logging.error(f"Error loading dataset: {str(e)}")
        raise

def validate_data(df: pd.DataFrame) -> dict:
    """
    Validates dataset for missing values, duplicates, out-of-range numeric fields, etc.
    """
    logging.info("Starting data validation...")
    validation_report = {}
    
    # 1. Basic counts
    validation_report['total_rows'] = int(df.shape[0])
    validation_report['total_columns'] = int(df.shape[1])
    
    # 2. Missing values
    null_counts = df.isnull().sum().to_dict()
    validation_report['missing_values'] = {k: int(v) for k, v in null_counts.items() if v > 0}
    logging.info(f"Missing values found: {validation_report['missing_values']}")
    
    # 3. Duplicate rows
    dup_count = int(df.duplicated().sum())
    validation_report['duplicate_rows'] = dup_count
    logging.info(f"Duplicate rows count: {dup_count}")
    
    # 4. Out-of-range numeric checks (negatives)
    numeric_cols = ['Quantity', 'UnitPrice', 'Discount', 'Tax', 'ShippingCost', 'TotalAmount']
    negatives = {}
    for col in numeric_cols:
        if col in df.columns:
            neg_count = int((df[col] < 0).sum())
            if neg_count > 0:
                negatives[col] = neg_count
    validation_report['negative_values'] = negatives
    logging.info(f"Negative values found: {negatives}")
    
    # 5. Outliers check (using Z-score > 3 on TotalAmount)
    if 'TotalAmount' in df.columns:
        mean_val = df['TotalAmount'].mean()
        std_val = df['TotalAmount'].std()
        outlier_count = int((((df['TotalAmount'] - mean_val) / std_val).abs() > 3).sum())
        validation_report['total_amount_outliers_z3'] = outlier_count
        logging.info(f"Outliers in TotalAmount (Z > 3): {outlier_count}")
        
    return validation_report

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw dataset, trims whitespace, formats types, 
    maps sub-categories, and computes derived profit.
    """
    logging.info("Starting data cleaning and enrichment...")
    cleaned_df = df.copy()
    
    # 1. Trim whitespace in string columns
    str_cols = cleaned_df.select_dtypes(include=['object', 'string']).columns
    for col in str_cols:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        
    # 2. Handle duplicates (none exist based on diagnostics, but standard safeguard)
    cleaned_df = cleaned_df.drop_duplicates()
    
    # 3. Ensure proper data types
    cleaned_df['OrderDate'] = pd.to_datetime(cleaned_df['OrderDate'])
    
    # Numeric column enforcement
    numeric_cols = ['Quantity', 'UnitPrice', 'Discount', 'Tax', 'ShippingCost', 'TotalAmount']
    for col in numeric_cols:
        cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0.0)
        
    # 4. Map Sub-Category
    logging.info("Mapping Sub-Categories based on product list...")
    cleaned_df['SubCategory'] = cleaned_df['ProductName'].map(PRODUCT_TO_SUBCATEGORY)
    # Default unmapped products to 'Other Accessories'
    cleaned_df['SubCategory'] = cleaned_df['SubCategory'].fillna('Other Accessories')
    
    # 5. Calculate Profit based on category cost margins and OrderStatus
    logging.info("Calculating derived Profit column...")
    
    # Create margins vector based on Category
    margins = cleaned_df['Category'].map(CATEGORY_COST_MARGINS).fillna(0.75) # Default 25% margin if unmapped
    
    # Base revenue and cost calculations
    # Revenue = (Quantity * UnitPrice) * (1 - Discount)
    # Cost = (Quantity * UnitPrice) * CostMargin
    # Base Profit = Revenue - Cost
    base_revenue = (cleaned_df['Quantity'] * cleaned_df['UnitPrice']) * (1 - cleaned_df['Discount'])
    base_cost = (cleaned_df['Quantity'] * cleaned_df['UnitPrice']) * margins
    base_profit = base_revenue - base_cost
    
    # Apply OrderStatus rules:
    # Delivered, Shipped, Pending: Normal BaseProfit
    # Returned: Loss equal to shipping cost + 5% product cost (processing fee and depreciation)
    # Cancelled: 0 profit (never transacted, no cost incurred)
    conditions = [
        cleaned_df['OrderStatus'].isin(['Delivered', 'Shipped', 'Pending']),
        cleaned_df['OrderStatus'] == 'Returned',
        cleaned_df['OrderStatus'] == 'Cancelled'
    ]
    
    choices = [
        base_profit,
        -cleaned_df['ShippingCost'] - (0.05 * cleaned_df['Quantity'] * cleaned_df['UnitPrice']),
        0.0
    ]
    
    cleaned_df['Profit'] = np.select(conditions, choices, default=base_profit)
    
    # Round columns to 2 decimal places for clean representation
    cleaned_df['Profit'] = cleaned_df['Profit'].round(2)
    cleaned_df['TotalAmount'] = cleaned_df['TotalAmount'].round(2)
    
    logging.info("Data cleaning and enrichment complete.")
    return cleaned_df

def save_cleaned_data(df: pd.DataFrame, output_path: str):
    """
    Saves the cleaned DataFrame to Excel.
    """
    start_time = time.time()
    logging.info(f"Saving cleaned dataset to {output_path}...")
    try:
        # Use xlsxwriter for high performance and formatting support
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Amazon_Cleaned', index=False)
        elapsed = time.time() - start_time
        logging.info(f"Cleaned dataset saved successfully in {elapsed:.2f} seconds.")
    except Exception as e:
        logging.error(f"Error saving cleaned data: {str(e)}")
        raise

if __name__ == "__main__":
    # Test script execution
    try:
        raw_df = load_data("data/Amazon_Sales.xlsx")
        report = validate_data(raw_df)
        print("Validation report:", report)
        cleaned_df = clean_data(raw_df)
        save_cleaned_data(cleaned_df, "output/cleaned_data/Amazon_Sales_Cleaned.xlsx")
        print("Cleaned data sample:\n", cleaned_df.head(2))
    except Exception as ex:
        print("Execution failed:", ex)
