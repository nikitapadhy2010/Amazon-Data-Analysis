import os
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

def create_and_execute_notebook():
    nb = nbf.v4.new_notebook()
    
    # Define the cells
    cells = [
        # Cell 1: Markdown Title
        nbf.v4.new_markdown_cell("""# Amazon India Sales Data Analytics Notebook
This notebook presents an interactive, step-by-step data analysis pipeline for Amazon India's transactional sales data. It walks through data loading, comprehensive data validation, cleaning/enrichment, key performance indicator (KPI) calculations, category-level performance assessments, temporal trends, and correlation tables.

## Project Structure Check
Ensure that the `src` directory is on the path to import our modular cleaning utilities.
"""),
        
        # Cell 2: Setup imports
        nbf.v4.new_code_cell("""import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add src directory to system path
sys.path.append(os.path.abspath('../src'))
from utils import load_data, validate_data, clean_data
from dashboard import (
    plot_sales_by_state, 
    plot_sales_by_category, 
    plot_monthly_trend, 
    plot_sales_by_subcategory
)

# Notebook styling
sns.set_theme(style="whitegrid")
%matplotlib inline
"""),

        # Cell 3: Markdown Q1 & Q2
        nbf.v4.new_markdown_cell("""### Q1 & Q2: Dataset Loading and Validation
We load the raw dataset, run standard validation checks (checking for missing values, duplicates, and negative numbers), and clean/enrich the dataset with:
1. **Sub-Category**: A mapped categorisation derived from the 50 unique product names.
2. **Profit**: Dynamic margin calculation reflecting discounts, manufacturing costs, and order statuses (penalising returns with negative profit).
"""),

        # Cell 4: Code Q1 & Q2
        nbf.v4.new_code_cell("""raw_path = "../data/Amazon_Sales.xlsx"
df_raw = load_data(raw_path)

print("\\n--- Validation Report ---")
report = validate_data(df_raw)
for key, val in report.items():
    print(f"{key}: {val}")

print("\\n--- Cleaning Data ---")
df_clean = clean_data(df_raw)
print("Cleaned Data Shape:", df_clean.shape)
df_clean.head(2)
"""),

        # Cell 5: Markdown Q3
        nbf.v4.new_markdown_cell("""### Q3: Key Performance Indicators (KPIs)
Here, we compute the primary corporate health metrics:
* **Total Sales (GMV)**
* **Total Profit**
* **Total Transactions**
* **Average Order Value (AOV)**
* **Gross Profit Margin (%)**
"""),

        # Cell 6: Code Q3
        nbf.v4.new_code_cell("""total_sales = df_clean['TotalAmount'].sum()
total_profit = df_clean['Profit'].sum()
total_orders = df_clean['OrderID'].nunique()
avg_sales = df_clean['TotalAmount'].mean()
avg_profit = df_clean['Profit'].mean()
aov = total_sales / total_orders
gross_margin = (total_profit / total_sales) * 100

print(f"Total Sales (GMV): ₹{total_sales:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Sales per Order: ₹{avg_sales:,.2f}")
print(f"Average Profit per Order: ₹{avg_profit:,.2f}")
print(f"Average Order Value (AOV): ₹{aov:,.2f}")
print(f"Gross Profit Margin: {gross_margin:.2f}%")
"""),

        # Cell 7: Markdown Q4
        nbf.v4.new_markdown_cell("""### Q4: Sales by State
Analysis of geographic performance. Let's see the top 10 states by sales.
"""),

        # Cell 8: Code Q4
        nbf.v4.new_code_cell("""state_sales = df_clean.groupby('State').agg(
    Total_Sales=('TotalAmount', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Order_Count=('OrderID', 'count')
).sort_values(by='Total_Sales', ascending=False).head(10)
state_sales
"""),

        # Cell 9: Markdown Q5
        nbf.v4.new_markdown_cell("""### Q5: Sales by Category
We evaluate the performance of primary categories to see which ones are top drivers and which ones have the healthiest profit margins.
"""),

        # Cell 10: Code Q5
        nbf.v4.new_code_cell("""cat_sales = df_clean.groupby('Category').agg(
    Total_Sales=('TotalAmount', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Order_Count=('OrderID', 'count')
).sort_values(by='Total_Sales', ascending=False)
cat_sales['Margin_%'] = (cat_sales['Total_Profit'] / cat_sales['Total_Sales']) * 100
cat_sales
"""),

        # Cell 11: Markdown Q7
        nbf.v4.new_markdown_cell("""### Q7: Sales by Sub-Category
We drill down into the 15 product sub-categories to isolate sales drivers.
"""),

        # Cell 12: Code Q7
        nbf.v4.new_code_cell("""subcat_sales = df_clean.groupby('SubCategory').agg(
    Total_Sales=('TotalAmount', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Order_Count=('OrderID', 'count')
).sort_values(by='Total_Sales', ascending=False)
subcat_sales['Margin_%'] = (subcat_sales['Total_Profit'] / subcat_sales['Total_Sales']) * 100
subcat_sales
"""),

        # Cell 13: Markdown Q9
        nbf.v4.new_markdown_cell("""### Q9: Top Customers
We identify the top 10 high-value customers by their lifetime purchases and check their loyalty and transactional count.
"""),

        # Cell 14: Code Q9
        nbf.v4.new_code_cell("""top_customers = df_clean.groupby(['CustomerID', 'CustomerName']).agg(
    Total_Spent=('TotalAmount', 'sum'),
    Total_Profit_Gen=('Profit', 'sum'),
    Order_Count=('OrderID', 'count'),
    Avg_Order_Value=('TotalAmount', 'mean')
).sort_values(by='Total_Spent', ascending=False).head(10)
top_customers
"""),

        # Cell 15: Markdown Q10
        nbf.v4.new_markdown_cell("""### Q10: Product Quantity
Isolation of the top 10 products sold by units/quantity.
"""),

        # Cell 16: Code Q10
        nbf.v4.new_code_cell("""top_products = df_clean.groupby(['ProductID', 'ProductName']).agg(
    Total_Qty_Sold=('Quantity', 'sum'),
    Total_Revenue=('TotalAmount', 'sum'),
    Avg_Unit_Price=('UnitPrice', 'mean')
).sort_values(by='Total_Qty_Sold', ascending=False).head(10)
top_products
"""),

        # Cell 17: Markdown Q11
        nbf.v4.new_markdown_cell("""### Q11: Payment Method Preferences
Analysis of checkout payment choices and their correlation to average transaction amounts.
"""),

        # Cell 18: Code Q11
        nbf.v4.new_code_cell("""pay_methods = df_clean.groupby('PaymentMethod').agg(
    Total_Sales=('TotalAmount', 'sum'),
    Order_Count=('OrderID', 'count'),
    Avg_Sales=('TotalAmount', 'mean')
).sort_values(by='Total_Sales', ascending=False)
pay_methods['Sales_Share_%'] = (pay_methods['Total_Sales'] / total_sales) * 100
pay_methods['Order_Share_%'] = (pay_methods['Order_Count'] / total_orders) * 100
pay_methods
"""),

        # Cell 19: Markdown Q12
        nbf.v4.new_markdown_cell("""### Q12: Monthly Sales and Profit Trend
Aggregating transactions monthly to understand trends, seasonality, and overall performance trajectories.
"""),

        # Cell 20: Code Q12
        nbf.v4.new_code_cell("""df_clean['YearMonth'] = df_clean['OrderDate'].dt.to_period('M')
monthly_data = df_clean.groupby('YearMonth').agg(
    Monthly_Sales=('TotalAmount', 'sum'),
    Monthly_Profit=('Profit', 'sum'),
    Order_Count=('OrderID', 'count')
).reset_index()
monthly_data['YearMonth_Str'] = monthly_data['YearMonth'].astype(str)

print("First Year Monthly Preview:")
display(monthly_data.head(12))
"""),

        # Cell 21: Markdown Q13
        nbf.v4.new_markdown_cell("""### Q13: Multi-Level Analysis (Cross-tabulations)
We evaluate structural combinations like:
1. Category by Country sales.
2. Payment Method by Order Status counts (revealing reverse logistics leakages for different modes).
"""),

        # Cell 22: Code Q13
        nbf.v4.new_code_cell("""print("--- Category by Country Sales ---")
display(pd.crosstab(df_clean['Category'], df_clean['Country'], values=df_clean['TotalAmount'], aggfunc='sum'))

print("\\n--- Payment Method by Order Status Counts ---")
display(pd.crosstab(df_clean['PaymentMethod'], df_clean['OrderStatus']))

print("\\n--- Status Distribution Rates (%) by Payment Method ---")
display(pd.crosstab(df_clean['PaymentMethod'], df_clean['OrderStatus'], normalize='index') * 100)
"""),

        # Cell 23: Markdown Visuals
        nbf.v4.new_markdown_cell("""### Q15 - Q18: Visualizations
We generate and display the analytical charts within the notebook cells.
"""),

        # Cell 24: Code Q15 (Bar chart)
        nbf.v4.new_code_cell("""# Q15: Top States by Sales
state_plot_data = df_clean.groupby('State')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False).head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x='State', y='TotalAmount', data=state_plot_data, palette='viridis', hue='State', legend=False)
plt.title("Top 10 States by Sales (Jupyter Inline)")
plt.ylabel("Sales (INR)")
plt.show()
"""),

        # Cell 25: Code Q16 (Pie chart)
        nbf.v4.new_code_cell("""# Q16: Sales share by Category
cat_plot_data = df_clean.groupby('Category')['TotalAmount'].sum()
plt.figure(figsize=(7, 7))
plt.pie(cat_plot_data, labels=cat_plot_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("muted"))
plt.title("Revenue Share Distribution (Jupyter Inline)")
plt.show()
"""),

        # Cell 26: Code Q17 (Line chart)
        nbf.v4.new_code_cell("""# Q17: Monthly Trend
plt.figure(figsize=(12, 5))
plt.plot(monthly_data['YearMonth_Str'], monthly_data['Monthly_Sales'], label='Sales', color='blue', marker='o')
plt.plot(monthly_data['YearMonth_Str'], monthly_data['Monthly_Profit'], label='Profit', color='green', marker='s', linestyle='--')
plt.xticks(monthly_data['YearMonth_Str'].values[::4], rotation=45)
plt.title("Monthly Performance Trends (Jupyter Inline)")
plt.ylabel("INR")
plt.legend()
plt.show()
"""),

        # Cell 27: Code Q18 (Horizontal Bar chart)
        nbf.v4.new_code_cell("""# Q18: Sales by Sub-Category
sub_plot_data = df_clean.groupby('SubCategory')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(y='SubCategory', x='TotalAmount', data=sub_plot_data, palette='coolwarm', hue='SubCategory', legend=False)
plt.title("Revenue by Sub-Category (Jupyter Inline)")
plt.xlabel("Sales (INR)")
plt.show()
""")
    ]
    
    nb.cells.extend(cells)
    
    # Save unexecuted notebook first
    nb_dir = "notebook"
    os.makedirs(nb_dir, exist_ok=True)
    nb_path = os.path.join(nb_dir, "Amazon_Data_Analysis.ipynb")
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
        
    print(f"Jupyter Notebook template written to: {nb_path}")
    
    # Execute the notebook to pre-compute outputs
    print("Executing Jupyter Notebook cells...")
    try:
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        # Execute in project root or notebook folder?
        # Running it with resources path so relative paths work correctly
        ep.preprocess(nb, {'metadata': {'path': nb_dir}})
        
        # Write executed notebook back
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Jupyter Notebook executed and saved successfully with outputs.")
    except Exception as e:
        print("Failed to execute notebook cells:", e)
        # Save the unexecuted notebook as backup if execution fails
        raise

if __name__ == "__main__":
    create_and_execute_notebook()
