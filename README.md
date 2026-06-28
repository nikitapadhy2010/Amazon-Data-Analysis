# Amazon India Data Analytics & BI Project

An industry-level, end-to-end Data Analytics and Business Intelligence solution for Amazon India to evaluate transactional performance, optimize category profit margins, assess customer loyalty, and minimize delivery risk. 

---

## 1. Project Overview

This project analyzes a transactional dataset of **100,000 sales orders** spanning from **01-Jan-2020** to **29-Dec-2024**. The dataset represents sales transactions containing customer details, geographical locations, product names, categories, pricing, discounts, shipping fees, tax, and order fulfillment statuses.

To support executive-level decision making, this project delivers:
1. **Cleaned & Enriched Dataset**: Standardized schemas with derived metrics like **Profit** and **Sub-Category**.
2. **Modular Python Pipeline (`src/`)**: Python scripts implementing strict data validation, cleaning, and aggregation to answer core business questions.
3. **Interactive Jupyter Notebook (`notebook/`)**: A presentation-ready notebook documenting the analysis step-by-step.
4. **High-Resolution Visualizations (`output/charts/`)**: High-quality 300 DPI PNG charts representing sales by state, category distribution, temporal trends, and sub-category performance.
5. **Interactive Excel Dashboard Guide & Formulas**: Reusable Excel formulas and layout blueprints to construct an interactive BI dashboard in Excel.

---

## 2. Business Problem & Insights

### Key Financial Performance (KPIs)
* **Total Sales (GMV)**: ₹91,825,647.92 (INR)
* **Total Net Profit**: ₹16,210,439.18 (INR)
* **Total Transactions**: 100,000 orders
* **Corporate Gross Margin**: 17.65%
* **Average Order Value (AOV)**: ₹918.26
* **Average Profit per Order**: ₹162.10

### Category Profitability Paradox
While **Electronics** drives the largest portion of raw revenue (₹15.58M), it contributes the lowest profit margin (**6.90%**) due to high baseline costs. Conversely, **Clothing** (₹15.25M in sales) generates ₹4.60M in net profit at a **30.16%** margin. Marketing investments should shift from top-line revenue metrics to bottom-line profit drivers (Clothing and Books).

### Operations and Return Mitigation
Across all payment methods, approximately **18.4%** of orders are Cancelled or Returned (with COD orders presenting the highest doorstep rejection rates). This reverse logistics leakage significantly dilutes profit margins and demands structural interventions.

---

## 3. Directory Structure

```
Amazon_Data_Analytics_Project/
├── .venv/                      # Python Virtual Environment
├── data/
│   └── Amazon_Sales.xlsx       # Raw source dataset (100,000 rows)
├── notebook/
│   └── Amazon_Data_Analysis.ipynb  # Executed Jupyter Notebook with outputs
├── src/
│   ├── utils.py                # Data loading, validation, and cleaning logic
│   ├── analysis.py             # Main analytical script answering Q1-Q18
│   ├── dashboard.py            # Code generating 300 DPI matplotlib charts
│   └── create_notebook.py      # Notebook creation and execution script
├── output/
│   ├── charts/                 # High-resolution PNG plots (Q15-Q18)
│   │   ├── q15_sales_by_state.png
│   │   ├── q16_sales_by_category.png
│   │   ├── q17_monthly_trend.png
│   │   └── q18_sales_by_subcategory.png
│   ├── reports/                # Markdown business reports
│   │   ├── business_analysis_report.md
│   │   └── excel_dashboard_guide.md
│   └── cleaned_data/           # Cleaned and enriched dataset
│       └── Amazon_Sales_Cleaned.xlsx
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore file
```

---

## 4. Environment Setup

To run the analysis locally, set up the virtual environment as described below.

### Windows CMD
```cmd
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate.bat

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Windows PowerShell
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Linux & macOS
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

---

## 5. Execution Instructions

Ensure your virtual environment is active before running these commands:

1. **Run Full Analysis & Report Generation**:
   ```bash
   python src/analysis.py
   ```
   This runs the data validation, cleaning, calculations for Q1-Q13, generates 300 DPI charts in `output/charts/`, and exports `output/reports/business_analysis_report.md`.

2. **Re-build & Execute Jupyter Notebook**:
   ```bash
   python src/create_notebook.py
   ```
   This rebuilds the Jupyter template and pre-computes the code cell outputs.

---

## 6. Interactive Excel Dashboard Design

The dashboard is structured around a **Clean Canvas layout** (gridlines hidden, neutral `#F8F9FA` gray background) to maximize legibility.

### Core Excel Formulas

#### Derived Columns (Applied in Cleaning Sheet):
* **YearMonth Helper**: `=TEXT(B2, "yyyy-mm")` (Used for monthly grouping on Line Charts)
* **Profit Logic**:
  ```excel
  =IF(P2="Cancelled", 0, IF(P2="Returned", -M2 - (0.05 * I2 * J2), (I2 * J2) * (1 - K2) - (I2 * J2 * VLOOKUP(G2, Margins!$A$2:$B$7, 2, FALSE))))
  ```
  *(Reference table sheet `Margins` holds category cost margins: Books=0.70, Electronics=0.85, Clothing=0.60, Toys=0.75, Sports=0.78, Kitchen=0.72)*

#### KPI Card Summaries:
* **Total Sales (GMV)**: `=SUM(Amazon_Cleaned!N:N)`
* **Total Profit**: `=SUM(Amazon_Cleaned!V:V)`
* **Total Transactions**: `=COUNTA(Amazon_Cleaned!A:A) - 1`
* **Average Order Value (AOV)**: `=[TotalSalesCell]/[TotalOrdersCell]`
* **Gross Profit Margin (%)**: `=[TotalProfitCell]/[TotalSalesCell]`

### Charts & Layout Plan:
* **Top 10 States by Sales**: Clustered horizontal bar chart sorted descending.
* **Profitability by Category**: Clustered vertical column chart.
* **Revenue Share by Category**: Doughnut chart showing % contribution.
* **Monthly Trends**: Dual-axis line chart (Sales on primary axis in blue, Profit on secondary axis in green).
* **Interactivity**: Add **Slicers** for `State`, `Category`, and `PaymentMethod`. Right-click each -> **Report Connections** and select all Pivot Tables to bind the entire canvas.

---

## 7. Business Recommendations

1. **Strategic Marketing Re-allocation (Priority: High)**:
   * **Problem**: Electronics accounts for 17% of GMV but only 6.6% of profits due to narrow margins (15% base margin minus discount dilution).
   * **Action**: Dynamically allocate 40% of the Electronics ad budget to Clothing and Books (which carry 30.1% and 20.8% profit margins respectively) to capture high-margin bottom-line growth.

2. **COD Doorstep Rejection Mitigation (Priority: High)**:
   * **Problem**: Cash on Delivery (COD) orders demonstrate high delivery cancellation and return rates.
   * **Action**: Implement "OTP Verification at Delivery" for COD transactions and restrict COD checkout for customers with a historical return rate exceeding 15%. Incentivize conversion to UPI/Amazon Pay at checkout with a 2% instant discount coupon.

3. **VIP Bulk Purchaser Program (Priority: Medium)**:
   * **Problem**: 0.51% of users represent transaction outliers contributing a massive share of GMV (ordering bulk quantities of premium items).
   * **Action**: Auto-enroll customers who spend more than ₹3,000 per order into the 'Amazon India VIP/Business Club', giving them dedicated GST invoices, bulk discounts, and prioritized delivery support to secure customer lifetime value (LTV).

---

## 8. Authors & License

* **Author**: Senior Business Intelligence Engineer & Data Analytics Specialist, Amazon India
* **License**: Commercial / Private Proprietary
