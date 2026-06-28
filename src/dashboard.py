import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set the style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

# Custom Amazon-inspired warm professional color palette
AMAZON_ORANGE = "#FF9900"
AMAZON_DARK = "#146EB4"
PALETTE_MUTED = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
COLOR_PRIMARY = "#1F4E79"
COLOR_SECONDARY = "#D9E1F2"

def plot_sales_by_state(df: pd.DataFrame, output_dir: str = "output/charts"):
    """
    Q15: Bar Chart - Top 10 States by Sales
    """
    os.makedirs(output_dir, exist_ok=True)
    state_sales = df.groupby('State')['TotalAmount'].sum().reset_index()
    state_sales = state_sales.sort_values(by='TotalAmount', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    # Use a clean blue gradient palette
    colors = sns.color_palette("Blues_r", n_colors=12)[:10]
    bars = plt.bar(state_sales['State'], state_sales['TotalAmount'] / 1e6, color=colors, edgecolor='grey', linewidth=0.5)
    
    # Value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'₹{height:.2f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')
                 
    plt.title("Top 10 States by Total Sales Volume", pad=20, fontweight='bold', color=COLOR_PRIMARY)
    plt.xlabel("State / Region", labelpad=10)
    plt.ylabel("Total Sales (INR in Millions)", labelpad=10)
    plt.tight_layout()
    
    file_path = os.path.join(output_dir, "q15_sales_by_state.png")
    plt.savefig(file_path, dpi=300)
    plt.close()
    print(f"Saved Q15 chart to: {file_path}")

def plot_sales_by_category(df: pd.DataFrame, output_dir: str = "output/charts"):
    """
    Q16: Pie Chart - Sales Share by Category
    """
    os.makedirs(output_dir, exist_ok=True)
    cat_sales = df.groupby('Category')['TotalAmount'].sum()
    
    plt.figure(figsize=(8, 8))
    # Clean warm custom colors
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a']
    
    # Plot pie chart with slight explode for emphasis
    explode = [0.03] * len(cat_sales)
    
    plt.pie(
        cat_sales, 
        labels=cat_sales.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors, 
        explode=explode,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )
    
    plt.title("Revenue Share Distribution by Product Category", pad=20, fontweight='bold', color=COLOR_PRIMARY)
    plt.tight_layout()
    
    file_path = os.path.join(output_dir, "q16_sales_by_category.png")
    plt.savefig(file_path, dpi=300)
    plt.close()
    print(f"Saved Q16 chart to: {file_path}")

def plot_monthly_trend(df: pd.DataFrame, output_dir: str = "output/charts"):
    """
    Q17: Line Chart - Monthly Sales and Profit Trend
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Resample to monthly sales and profit
    df_temp = df.copy()
    df_temp['YearMonth'] = df_temp['OrderDate'].dt.to_period('M')
    monthly_data = df_temp.groupby('YearMonth')[['TotalAmount', 'Profit']].sum().reset_index()
    monthly_data['YearMonth_Str'] = monthly_data['YearMonth'].astype(str)
    
    # Filter to last 24 months for readability or show overall trend (we have 2020-2024, i.e. 60 months)
    # Let's plot the overall trend but sample the x-axis ticks for clarity
    plt.figure(figsize=(12, 6))
    
    # Plot Sales on Primary Y Axis
    ax1 = plt.gca()
    color_sales = '#1F4E79'
    ax1.plot(monthly_data['YearMonth_Str'], monthly_data['TotalAmount'] / 1e6, 
             color=color_sales, marker='o', linewidth=2.5, label='Monthly Sales')
    ax1.set_xlabel('Timeline (Monthly)', labelpad=10)
    ax1.set_ylabel('Total Sales (INR in Millions)', color=color_sales, labelpad=10)
    ax1.tick_params(axis='y', labelcolor=color_sales)
    
    # Plot Profit on Secondary Y Axis
    ax2 = ax1.twinx()
    color_profit = '#2CA02C'
    ax2.plot(monthly_data['YearMonth_Str'], monthly_data['Profit'] / 1e6, 
             color=color_profit, marker='s', linestyle='--', linewidth=2, label='Monthly Profit')
    ax2.set_ylabel('Total Profit (INR in Millions)', color=color_profit, labelpad=10)
    ax2.tick_params(axis='y', labelcolor=color_profit)
    
    # Setting X-ticks frequency to avoid overlapping text
    ticks_to_use = monthly_data['YearMonth_Str'].values[::4]
    ax1.set_xticks(ticks_to_use)
    ax1.set_xticklabels(ticks_to_use, rotation=45, ha='right')
    
    # Align legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
    
    plt.title("Historical Monthly Sales & Profit Performance Trend (2020 - 2024)", pad=20, fontweight='bold', color=COLOR_PRIMARY)
    plt.tight_layout()
    
    file_path = os.path.join(output_dir, "q17_monthly_trend.png")
    plt.savefig(file_path, dpi=300)
    plt.close()
    print(f"Saved Q17 chart to: {file_path}")

def plot_sales_by_subcategory(df: pd.DataFrame, output_dir: str = "output/charts"):
    """
    Q18: Horizontal Bar Chart - Sales by Product Sub-Category
    """
    os.makedirs(output_dir, exist_ok=True)
    sub_sales = df.groupby('SubCategory')['TotalAmount'].sum().reset_index()
    sub_sales = sub_sales.sort_values(by='TotalAmount', ascending=True) # Ascending for bottom-up horizontal bar
    
    plt.figure(figsize=(12, 8))
    
    # Generate horizontal bar chart
    colors = sns.color_palette("viridis", n_colors=len(sub_sales))
    bars = plt.barh(sub_sales['SubCategory'], sub_sales['TotalAmount'] / 1e6, color=colors, edgecolor='grey', linewidth=0.5)
    
    # Add value labels inside/outside the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.05, bar.get_y() + bar.get_height()/2., 
                 f'₹{width:.2f}M', ha='left', va='center', fontsize=9, fontweight='bold')
                 
    plt.title("Revenue Contribution by Product Sub-Category", pad=20, fontweight='bold', color=COLOR_PRIMARY)
    plt.xlabel("Total Sales (INR in Millions)", labelpad=10)
    plt.ylabel("Product Sub-Category", labelpad=10)
    plt.xlim(0, sub_sales['TotalAmount'].max() / 1e6 * 1.15) # Leave space for labels
    plt.tight_layout()
    
    file_path = os.path.join(output_dir, "q18_sales_by_subcategory.png")
    plt.savefig(file_path, dpi=300)
    plt.close()
    print(f"Saved Q18 chart to: {file_path}")

if __name__ == "__main__":
    # Test script run
    try:
        df = pd.read_excel("output/cleaned_data/Amazon_Sales_Cleaned.xlsx")
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        plot_sales_by_state(df)
        plot_sales_by_category(df)
        plot_monthly_trend(df)
        plot_sales_by_subcategory(df)
        print("All test plots generated successfully.")
    except Exception as e:
        print("Failed to run test plots:", e)
