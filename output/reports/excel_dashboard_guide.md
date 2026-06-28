# Amazon India Sales Performance - Excel Dashboard Construction Guide

This guide provides step-by-step, industry-level instructions and exact formulas to construct a professional, interactive Excel Dashboard based on the cleaned Amazon Sales dataset (`Amazon_Sales_Cleaned.xlsx`).

---

## Part 1: Dataset Enrichment & Cleaning Formulas (Excel-Side)

If you are starting from the raw workbook, follow these steps to enrich and clean your data directly in Excel. If you are importing our pre-cleaned dataset (`Amazon_Sales_Cleaned.xlsx`), these steps have been automated, but we provide the matching Excel formulas below for compliance and verification.

### 1. Data Cleaning
* **Trim Whitespace**: Ensure all text cells are free of leading/trailing spaces.
  * *Formula*: `=TRIM(D2)` (Applied to `CustomerName`, `ProductName`, `Category`, `Brand`, `City`, `State`, `Country`, `PaymentMethod`, `OrderStatus`).
* **Format OrderDate**:
  * Ensure the `OrderDate` column is formatted as a Short Date (`YYYY-MM-DD`).
* **Data Types**:
  * Select columns `Quantity` to `TotalAmount`, right-click -> **Format Cells** -> **Number** (2 decimal places for currency, 0 decimal places for Quantity).

### 2. Monthly Grouping (For Monthly Trend Analysis)
Create a new helper column named `YearMonth` to easily group dates chronologically.
* *Formula*: `=TEXT(B2, "yyyy-mm")`
* *Explanation*: This extracts the Year and Month from the `OrderDate` in column `B` as a sortable string (e.g. `2023-01`).

### 3. Profit Column (Conditional Logic)
Since the raw sheet does not contain a profit metric, calculate it in column `V` (`Profit`) based on product costs and transaction statuses:
* Create a **Margin Reference Table** (placed in a sheet named `Margins` or columns `X:Y` on the same sheet):
  | Category (Col X) | Cost Margin (Col Y) |
  | :--- | :--- |
  | Books | 0.70 |
  | Electronics | 0.85 |
  | Clothing | 0.60 |
  | Toys & Games | 0.75 |
  | Sports & Outdoors | 0.78 |
  | Home & Kitchen | 0.72 |

* **Profit Calculation Formula**:
  ```excel
  =IF(P2="Cancelled", 0, IF(P2="Returned", -M2 - (0.05 * I2 * J2), (I2 * J2) * (1 - K2) - (I2 * J2 * VLOOKUP(G2, Margins!$A$2:$B$7, 2, FALSE))))
  ```
* *Formula Breakdown*:
  1. `IF(P2="Cancelled", 0, ...)`: Cancelled orders yield zero profit.
  2. `IF(P2="Returned", -M2 - (0.05 * I2 * J2), ...)`: Returned orders yield a loss equal to the shipping cost (`-M2` where column M is `ShippingCost`) plus a 5% restocking/processing loss based on subtotal (`0.05 * Quantity * UnitPrice`).
  3. Otherwise (Normal transaction): Profit = Net Revenue (`Quantity * UnitPrice * (1 - Discount)`) minus Cost (`Quantity * UnitPrice * CostMargin`).

---

## Part 2: KPI Metrics & Summary Formulas

Create a dedicated sheet named `Dashboard` and set up the KPI Cards. Write the following formulas referencing the `Amazon_Cleaned` sheet.

### 1. Total Sales (GMV)
* **Formula**: `=SUM(Amazon_Cleaned!N:N)` (where column N is `TotalAmount`)
* **Formatting**: Format as Currency (₹, English India, 2 decimal places).
* **Explanation**: Aggregates total revenue across all sales.

### 2. Total Profit
* **Formula**: `=SUM(Amazon_Cleaned!V:V)` (where column V is `Profit`)
* **Formatting**: Format as Currency (₹).
* **Explanation**: Aggregates final profit after subtracting product cost and returns.

### 3. Total Orders
* **Formula**: `=COUNTA(Amazon_Cleaned!A:A) - 1` (where column A is `OrderID`)
* **Explanation**: Counts all transactions (excluding the header row).

### 4. Average Sales per Transaction
* **Formula**: `=AVERAGE(Amazon_Cleaned!N:N)`
* **Explanation**: Returns the average transaction value.

### 5. Average Profit per Transaction
* **Formula**: `=AVERAGE(Amazon_Cleaned!V:V)`
* **Explanation**: Shows average profit contribution per transaction.

### 6. Average Order Value (AOV)
* **Formula**: `=TotalSales / TotalOrders` (pointing to the KPI cell addresses)
* **Explanation**: Measures average ticket size.

### 7. Corporate Gross Profit Margin (%)
* **Formula**: `=TotalProfit / TotalSales`
* **Formatting**: Format as Percentage (`0.0%`).
* **Explanation**: Computes profitability ratio.

---

## Part 3: Pivot Table & Pivot Chart Construction

Create a separate worksheet named `Pivot_Tables`. Insert the following Pivot Tables sourcing from the range `Amazon_Cleaned!A:V`.

### 1. Sales by State (Pivot Table 1)
* **Rows**: `State`
* **Values**: `TotalAmount` (Sum, renamed to "Sales (INR)")
* **Sorting**: Sort by "Sales (INR)" in descending order.
* **Pivot Chart**: Insert a **Clustered Bar Chart** (Horizontal) or **Clustered Column Chart** (Vertical). Filter to show Top 10 states.

### 2. Profit by Category (Pivot Table 2)
* **Rows**: `Category`
* **Values**: `Profit` (Sum, renamed to "Profit (INR)")
* **Sorting**: Sort by "Profit (INR)" descending.
* **Pivot Chart**: Insert a **Clustered Column Chart**.

### 3. Revenue Share by Category (Pivot Table 3)
* **Rows**: `Category`
* **Values**: `TotalAmount` (Sum, shown as **% of Column Total**)
* **Pivot Chart**: Insert a **Pie Chart** or **Doughnut Chart** to show percentage share.

### 4. Monthly Sales Trend (Pivot Table 4)
* **Rows**: `YearMonth` (drag `OrderDate` into Rows; Excel will auto-group by Year/Month, or use our helper `YearMonth` column)
* **Values**: `TotalAmount` (Sum) and `Profit` (Sum)
* **Pivot Chart**: Insert a **Line Chart** with dual-axes. Plot Sales as a Line on the primary axis, and Profit as a Line/Area on the secondary axis.

---

## Part 4: Interactive Dashboard Layout & Aesthetics

A premium executive dashboard should be visually stunning and clean. Follow these layout guidelines:

### 1. Canvas Setup
* Hide gridlines: Go to **View** -> Uncheck **Gridlines**.
* Background Color: Fill background with a very light neutral gray (e.g. Hex `#F2F4F7` or `#F8F9FA`) to make KPI cards and charts pop.

### 2. KPI Cards Layout
* Place KPI cards at the top of the dashboard.
* Each card should be a rounded rectangle shape filled with white, with a subtle border and shadow.
* Inside each card:
  * Top text: Gray, small font (e.g. Segoe UI, size 9, bold) representing label (e.g., "TOTAL GMV").
  * Bottom value: Dark color (e.g. Hex `#1F4E79`), large font (Segoe UI, size 18, bold) linked to the formula cell.

### 3. Chart Customization
* Remove default chart borders and match background fills to the white KPI card style.
* Use a cohesive color scheme:
  * **Sales**: Navy Blue (`#1F4E79`)
  * **Profit**: Forest Green (`#2CA02C`)
  * **Highlights/Alerts**: Muted Orange (`#FF9900`)
* Remove chart titles inside the chart block and place text labels in cells above the charts.
* Add data labels to major charts where readable.

### 4. Interactive Slicers
* Select any Pivot Chart -> **PivotChart Analyze** -> **Insert Slicer**.
* Select: `State`, `Category`, `PaymentMethod`.
* Format Slicers:
  * Match style to the navy blue or light gray corporate theme.
  * Arrange in a vertical column on the left side of the dashboard as a navigation panel.
* **CRITICAL STEP**: Right-click each Slicer -> **Report Connections** -> Check all Pivot Tables on the `Pivot_Tables` sheet. This ensures that clicking a slicer updates all KPIs and charts simultaneously.

### 5. Conditional Formatting Rules
* Apply conditional formatting on the `Amazon_Cleaned` sheet:
  * **High Returns Indicator**: Highlight cells in the `OrderStatus` column where value is "Returned" with Light Red Fill (`#FFC7CE`) and Dark Red Text (`#9C0006`).
  * **High Value Orders**: Apply a Soft Green data bar to the `TotalAmount` column for amounts above ₹2,000.
  * **Negative Profit Alert**: Set conditional formatting on the `Profit` column to highlight any negative cell values in light red to quickly spot unprofitable transactions.
