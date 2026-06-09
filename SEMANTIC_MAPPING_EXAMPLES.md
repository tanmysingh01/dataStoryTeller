# Semantic Model Mapping: From Raw Data to Business Concepts

Detailed reference showing how raw data columns map to business-meaningful concepts for Customer Churn, Revenue Growth, and Supply Chain Risk.

## 1. CUSTOMER CHURN ANALYSIS

### Problem: Understand why customers leave

**Raw Data Challenge:**
```
Data is scattered across tables:
- customers table: IDs, names, tenure, subscription type
- charges table: monthly fees, total charges
- events table: churn flags, churn dates
- geography table: regions
```

**Business Questions:**
- Which customers are most likely to churn?
- What's our overall churn rate?
- How does tenure affect churn?
- Which regions have highest churn?
- What's the revenue impact of churn?

### Semantic Mapping

```
┌─────────────────────────────────────────┐
│          RAW COLUMNS (SQL)              │
├─────────────────────────────────────────┤
│ customer_id       (VARCHAR)             │
│ customer_name     (VARCHAR)             │
│ tenure_months     (INT)                 │
│ monthly_charges   (DECIMAL)             │
│ total_charges     (DECIMAL)             │
│ is_churned        (BIT)                 │
│ churn_date        (DATE)                │
│ subscription_type (VARCHAR)             │
│ region            (VARCHAR)             │
└─────────────────────────────────────────┘
                    ↓
            [SEMANTIC MODEL]
                    ↓
┌──────────────────────────────────────────┐
│      BUSINESS CONCEPTS (Semantic)        │
├──────────────────────────────────────────┤
│ Dimensions:                              │
│  - Customer (Name, Subscription Type)    │
│  - Tenure Segment (0-6m, 6-12m, 12m+)  │
│  - Region (North, South, East, West)    │
│  - Status (Active, Churned)              │
│                                          │
│ Measures:                                │
│  - Total Customers (Count distinct)      │
│  - Churned Customers (Count churn=true)  │
│  - Churn Rate (% of total)               │
│  - Average Tenure (months)               │
│  - Average Monthly Charges (ARPU)        │
│  - Total Revenue at Risk (value)         │
│                                          │
│ Hierarchies:                             │
│  - Region → Subscription → Customer      │
│  - Tenure Band → Region → Status         │
└──────────────────────────────────────────┘
```

### Code Example: Customer Churn Mapping

```python
from semantic_model import (
    SemanticModel, SemanticTable, Column, Measure,
    Hierarchy, DataType, AggregationFunction
)

# Create model
model = SemanticModel("customer_churn", "Customer Churn Analysis")

# Create Customers table
customers = SemanticTable("customers", "Customers")

# MAP RAW COLUMNS TO BUSINESS ATTRIBUTES
customers.add_column(Column("customer_id", "Customer ID", DataType.STRING))
customers.add_column(Column("customer_name", "Customer Name", DataType.STRING))
customers.add_column(Column("tenure_months", "Tenure (Months)", DataType.INT,
    "How long customer has been with us"))
customers.add_column(Column("monthly_charges", "Monthly Charges", DataType.DECIMAL,
    "Average Revenue Per User (ARPU)"))
customers.add_column(Column("total_charges", "Lifetime Value", DataType.DECIMAL,
    "Total revenue from customer"))
customers.add_column(Column("is_churned", "Churned Status", DataType.BOOLEAN,
    "Whether customer has cancelled"))
customers.add_column(Column("churn_date", "Churn Date", DataType.DATE))
customers.add_column(Column("subscription_type", "Subscription", DataType.STRING,
    "Premium, Standard, Basic"))
customers.add_column(Column("region", "Region", DataType.STRING))

# CREATE BUSINESS METRICS
customers.add_measure(Measure(
    name="total_customers",
    display_name="Total Customers",
    description="Count of all active and churned customers",
    column="customer_id",
    aggregation=AggregationFunction.DISTINCT_COUNT
))

customers.add_measure(Measure(
    name="churned_count",
    display_name="Churned Customers",
    description="Number of customers who left",
    column="customer_id",
    aggregation=AggregationFunction.COUNT,
    calculation="CALCULATE(COUNT(customers[customer_id]), customers[is_churned]=TRUE())"
))

customers.add_measure(Measure(
    name="churn_rate",
    display_name="Churn Rate",
    description="% of customers lost",
    column="is_churned",
    aggregation=AggregationFunction.AVG,
    format_string="0.00%"
))

customers.add_measure(Measure(
    name="avg_tenure",
    display_name="Avg Customer Tenure",
    description="Average months customers stay",
    column="tenure_months",
    aggregation=AggregationFunction.AVG,
    format_string="0 months"
))

customers.add_measure(Measure(
    name="arpu",
    display_name="Average Revenue Per User",
    description="Avg monthly charges per customer",
    column="monthly_charges",
    aggregation=AggregationFunction.AVG,
    format_string="$#,##0.00"
))

customers.add_measure(Measure(
    name="total_revenue",
    display_name="Total Lifetime Revenue",
    description="Sum of all customer lifetime values",
    column="total_charges",
    aggregation=AggregationFunction.SUM,
    format_string="$#,##0.00"
))

# CREATE DRILL-DOWN HIERARCHIES
customers.add_hierarchy(Hierarchy(
    name="churn_analysis",
    display_name="Churn Analysis",
    levels=["region", "subscription_type", "customer_name"]
))

# Hide technical columns
customers.hide_column("customer_id")

model.add_table(customers)

# RESULT: Business users now see meaningful concepts
# Instead of raw SQL, they ask:
# - "What's our churn rate?"                    → Churn Rate measure
# - "Which regions have highest churn?"         → Region hierarchy + Churn Rate
# - "Who are our high-value at-risk customers?" → Filter by subscription + tenure + ARPU
# - "Show me churned vs active customers"       → Segment by Is_Churned status
```

## 2. REVENUE GROWTH ANALYSIS

### Problem: Understand sales performance and growth

**Raw Data Challenge:**
```
Sales data scattered across:
- sales transactions table: IDs, amounts, dates
- products table: names, categories, prices
- customers table: regions, segments
- costs table: COGS, shipping, overhead
```

**Business Questions:**
- What's our total revenue?
- Which products drive growth?
- How does revenue differ by region?
- What's our profit margin?
- How are sales trending over time?
- Which product categories are growing fastest?

### Semantic Mapping

```
┌──────────────────────────────────────────┐
│        RAW COLUMNS (Multiple Tables)     │
├──────────────────────────────────────────┤
│ SALES:           PRODUCTS:               │
│ sales_id         product_id              │
│ order_date       product_name            │
│ product_id       category                │
│ quantity         subcategory             │
│ unit_price       base_price              │
│ sales_amount     ← (calculated qty×price)│
│ cost_amount      CUSTOMERS:              │
│ profit_amount    region                  │
│ region           customer_segment        │
└──────────────────────────────────────────┘
                    ↓
            [SEMANTIC MODEL]
                    ↓
┌──────────────────────────────────────────┐
│      BUSINESS CONCEPTS (Semantic)        │
├──────────────────────────────────────────┤
│ Dimensions:                              │
│  - Product (Category, Subcategory)       │
│  - Region (Geographic Market)            │
│  - Time (Year, Quarter, Month, Date)     │
│  - Segment (Premium, Standard, etc.)     │
│                                          │
│ Measures:                                │
│  - Total Sales Revenue (SUM)             │
│  - Order Count (DISTINCT)                │
│  - Average Order Value (AVG)             │
│  - Total Cost (SUM)                      │
│  - Total Profit (SUM)                    │
│  - Profit Margin (Profit/Sales %)        │
│  - YoY Growth (% change)                 │
│  - Units Sold (SUM Qty)                  │
│                                          │
│ Hierarchies:                             │
│  - Region → Category → Product           │
│  - Year → Quarter → Month → Date         │
│  - Segment → Product → Region            │
└──────────────────────────────────────────┘
```

### Code Example: Revenue Growth Mapping

```python
# Create Products table
products = SemanticTable("products", "Products")
products.add_column(Column("product_id", "Product ID", DataType.STRING))
products.add_column(Column("product_name", "Product Name", DataType.STRING))
products.add_column(Column("category", "Category", DataType.STRING,
    "Major product category"))
products.add_column(Column("subcategory", "Subcategory", DataType.STRING))
products.add_column(Column("unit_price", "Unit Price", DataType.DECIMAL))

products.add_hierarchy(Hierarchy(
    "product_hierarchy",
    "Product Hierarchy",
    levels=["category", "subcategory", "product_name"]
))

model.add_table(products)

# Create Sales table
sales = SemanticTable("sales", "Sales")
sales.add_column(Column("sales_id", "Sales ID", DataType.STRING))
sales.add_column(Column("order_date", "Order Date", DataType.DATE))
sales.add_column(Column("product_id", "Product ID", DataType.STRING))
sales.add_column(Column("region", "Region", DataType.STRING))
sales.add_column(Column("quantity", "Quantity Sold", DataType.INT))
sales.add_column(Column("unit_price", "Unit Price", DataType.DECIMAL))
sales.add_column(Column("sales_amount", "Sales Revenue", DataType.DECIMAL))
sales.add_column(Column("cost_amount", "Cost of Goods", DataType.DECIMAL))
sales.add_column(Column("profit_amount", "Gross Profit", DataType.DECIMAL))

# BUSINESS METRICS
sales.add_measure(Measure(
    "total_sales",
    "Total Revenue",
    "Sum of all sales transactions",
    "sales_amount",
    AggregationFunction.SUM,
    format_string="$#,##0.00"
))

sales.add_measure(Measure(
    "order_count",
    "Orders",
    "Number of transactions",
    "sales_id",
    AggregationFunction.DISTINCT_COUNT
))

sales.add_measure(Measure(
    "avg_order_value",
    "Average Order Value",
    "Avg revenue per transaction",
    "sales_amount",
    AggregationFunction.AVG,
    format_string="$#,##0.00"
))

sales.add_measure(Measure(
    "total_profit",
    "Total Profit",
    "Sum of all profits",
    "profit_amount",
    AggregationFunction.SUM,
    format_string="$#,##0.00"
))

sales.add_measure(Measure(
    "profit_margin",
    "Profit Margin %",
    "Profit as % of revenue",
    "profit_amount",
    AggregationFunction.AVG,
    format_string="0.00%"
))

sales.add_measure(Measure(
    "units_sold",
    "Units Sold",
    "Total quantity sold",
    "quantity",
    AggregationFunction.SUM,
    format_string="#,##0"
))

# DRILL-DOWN PATHS
sales.add_hierarchy(Hierarchy(
    "regional_analysis",
    "Regional Sales",
    levels=["region", "category", "product_name"]
))

sales.add_hierarchy(Hierarchy(
    "time_analysis",
    "Time Series",
    levels=["order_date"]  # Can drill to Year/Quarter/Month in BI tool
))

# RELATIONSHIPS
model.add_relationship(Relationship(
    from_table="sales",
    from_column="product_id",
    to_table="products",
    to_column="product_id",
    cardinality="many-to-one"
))

# RESULT: Business users can now:
# - "Revenue by region and product"          → Use hierarchy drill-down
# - "Which products are most profitable?"    → Sort by Profit Margin measure
# - "Track sales trends over time"           → Use Time Analysis hierarchy
# - "Compare Q1 vs Q2 performance"           → Slice by order_date
```

## 3. SUPPLY CHAIN RISK ANALYSIS

### Problem: Identify inventory and supplier risks

**Raw Data Challenge:**
```
Risk data scattered across:
- suppliers table: reliability, lead times, quality
- inventory table: stock levels, reorder points, dates
- warehouse table: locations
- demand forecast table: predicted needs
```

**Business Questions:**
- Which items are at risk of stockout?
- Which items are overstocked?
- Which suppliers are unreliable?
- What's our average days of inventory supply?
- Where are supply chain bottlenecks?
- Which products have long lead times?

### Semantic Mapping

```
┌──────────────────────────────────────────┐
│        RAW COLUMNS (Multiple Tables)     │
├──────────────────────────────────────────┤
│ SUPPLIERS:       INVENTORY:              │
│ supplier_id      inventory_id            │
│ supplier_name    product_id              │
│ country          warehouse_location      │
│ reliability_score current_stock_level    │
│ avg_lead_time    safety_stock_level      │
│ quality_score    reorder_point           │
│                  inventory_date          │
│ PRODUCTS:        days_of_supply          │
│ product_id       stockout_risk (flag)    │
│ product_name     overstock_risk (flag)   │
│ unit_cost        supplier_id             │
└──────────────────────────────────────────┘
                    ↓
            [SEMANTIC MODEL]
                    ↓
┌──────────────────────────────────────────┐
│      BUSINESS CONCEPTS (Semantic)        │
├──────────────────────────────────────────┤
│ Dimensions:                              │
│  - Supplier (Country, Reliability)       │
│  - Product (Name, Category)              │
│  - Warehouse (Location)                  │
│  - Risk Level (Critical, High, Medium)   │
│                                          │
│ Measures:                                │
│  - Total Inventory Units (SUM)           │
│  - Days of Supply (AVG) - KEY METRIC     │
│  - Stockout Risk Items (COUNT)           │
│  - Overstock Risk Items (COUNT)          │
│  - Avg Supplier Reliability (AVG %)      │
│  - Avg Lead Time (AVG days)              │
│  - Avg Quality Score (AVG)               │
│  - Items at Risk (%)                     │
│                                          │
│ Hierarchies:                             │
│  - Warehouse → Product → Risk Level      │
│  - Supplier Country → Reliability        │
│  - Product → Supplier → Lead Time        │
└──────────────────────────────────────────┘
```

### Code Example: Supply Chain Risk Mapping

```python
# Create Suppliers table
suppliers = SemanticTable("suppliers", "Suppliers")
suppliers.add_column(Column("supplier_id", "Supplier ID", DataType.STRING))
suppliers.add_column(Column("supplier_name", "Supplier Name", DataType.STRING))
suppliers.add_column(Column("country", "Country", DataType.STRING))
suppliers.add_column(Column("reliability_score", "On-Time Delivery %", DataType.DECIMAL,
    "% of orders delivered on time"))
suppliers.add_column(Column("avg_lead_time_days", "Avg Lead Time", DataType.INT,
    "Average days from order to delivery"))
suppliers.add_column(Column("quality_score", "Quality Rating", DataType.DECIMAL,
    "0-100 quality score"))

suppliers.add_measure(Measure(
    "avg_reliability",
    "Average Reliability",
    "% orders on time across suppliers",
    "reliability_score",
    AggregationFunction.AVG,
    format_string="0.00%"
))

suppliers.add_measure(Measure(
    "avg_lead_time",
    "Average Lead Time",
    "Typical supplier lead time",
    "avg_lead_time_days",
    AggregationFunction.AVG,
    format_string="0 days"
))

# Create Inventory table
inventory = SemanticTable("inventory", "Inventory")
inventory.add_column(Column("inventory_id", "Inventory ID", DataType.STRING))
inventory.add_column(Column("product_id", "Product ID", DataType.STRING))
inventory.add_column(Column("warehouse_location", "Warehouse", DataType.STRING))
inventory.add_column(Column("current_stock_level", "Current Stock", DataType.INT,
    "Units on hand"))
inventory.add_column(Column("safety_stock_level", "Safety Stock", DataType.INT,
    "Minimum required level"))
inventory.add_column(Column("reorder_point", "Reorder Point", DataType.INT,
    "Trigger level for new order"))
inventory.add_column(Column("inventory_date", "Inventory Date", DataType.DATE))
inventory.add_column(Column("days_of_supply", "Days of Supply", DataType.INT,
    "Estimated days supply available"))
inventory.add_column(Column("stockout_risk", "Stockout Risk", DataType.BOOLEAN,
    "TRUE if at risk of running out"))
inventory.add_column(Column("overstock_risk", "Overstock Risk", DataType.BOOLEAN,
    "TRUE if excess inventory"))
inventory.add_column(Column("supplier_id", "Supplier ID", DataType.STRING))

# KEY SUPPLY CHAIN METRICS
inventory.add_measure(Measure(
    "total_inventory_units",
    "Total Inventory",
    "Sum of all inventory on hand",
    "current_stock_level",
    AggregationFunction.SUM,
    format_string="#,##0 units"
))

inventory.add_measure(Measure(
    "avg_days_supply",
    "Avg Days of Supply",
    "Average days supply available",
    "days_of_supply",
    AggregationFunction.AVG,
    format_string="0.0 days"
))

inventory.add_measure(Measure(
    "stockout_items",
    "Stockout Risk Items",
    "Items at risk of running out",
    "inventory_id",
    AggregationFunction.COUNT,
    calculation="CALCULATE(COUNT(...), stockout_risk=TRUE())"
))

inventory.add_measure(Measure(
    "overstock_items",
    "Overstock Items",
    "Items with excess inventory",
    "inventory_id",
    AggregationFunction.COUNT,
    calculation="CALCULATE(COUNT(...), overstock_risk=TRUE())"
))

inventory.add_measure(Measure(
    "at_risk_percentage",
    "% at Risk",
    "Percentage of items at risk",
    "inventory_id",
    AggregationFunction.COUNT,
    format_string="0.0%"
))

# DRILL-DOWN PATHS
inventory.add_hierarchy(Hierarchy(
    "risk_analysis",
    "Risk Analysis",
    levels=["warehouse_location", "stockout_risk", "product_id"]
))

inventory.add_hierarchy(Hierarchy(
    "supplier_analysis",
    "Supplier Analysis",
    levels=["supplier_id", "product_id", "days_of_supply"]
))

# RELATIONSHIPS
model.add_relationship(Relationship(
    from_table="inventory",
    from_column="supplier_id",
    to_table="suppliers",
    to_column="supplier_id",
    cardinality="many-to-one"
))

# RESULT: Supply chain managers can now:
# - "Show me all stockout risks"              → Filter stockout_risk=TRUE
# - "Which suppliers are unreliable?"         → Sort by Reliability Score
# - "Where's our inventory concentrated?"     → Group by warehouse_location
# - "What's our average supply visibility?"   → Avg Days of Supply measure
# - "Which products have long lead times?"    → Sort suppliers by lead time
```

## Comparison: Raw vs. Semantic

### BEFORE Semantic Model:
```
User Query: "How much revenue did Product X generate in the Northeast region?"

Steps Required:
1. Find the sales table
2. Find the products table  
3. Find the regions table
4. Write JOIN statements
5. Filter WHERE product = 'X' AND region = 'Northeast'
6. SUM the sales_amount column
7. Convert to currency format
8. Verify column names (sales_value? sales_amt? amount?)
```

### AFTER Semantic Model:
```
User Query: "Total Revenue for Product X in Northeast"

Steps Required:
1. Click on "Total Revenue" measure
2. Drag "Product Name" to filter/slice
3. Set filter: Product Name = "Product X"
4. Drag "Region" to filter/slice
5. Set filter: Region = "Northeast"
6. Result automatically formatted and calculated!
```

## Key Mapping Principles

1. **Hide Technical Details** - Hide customer_id, product_id, sales_id
2. **Expose Business Concepts** - Show "Churn Rate", "Profit Margin", "Days of Supply"
3. **Format for Business** - Use "0.00%", "$#,##0.00", "0 days"
4. **Create Drill Paths** - Enable Region > Category > Product analysis
5. **Define Relationships** - Connect sales to products to suppliers
6. **Calculate Metrics** - Pre-build common metrics as measures
7. **Document Everything** - Clear descriptions for all columns and measures

## File Outputs

When you create semantic models, JSON files are generated:

```json
{
  "name": "customer_churn",
  "displayName": "Customer Churn Analysis",
  "version": "1.0",
  "tables": [
    {
      "name": "customers",
      "displayName": "Customers",
      "columns": [
        {
          "name": "churn_rate",
          "displayName": "Churn Rate",
          "dataType": "float"
        }
      ],
      "measures": [
        {
          "name": "total_customers",
          "displayName": "Total Customers",
          "aggregation": "distinct_count"
        }
      ]
    }
  ],
  "relationships": [
    {
      "fromTable": "sales",
      "fromColumn": "product_id",
      "toTable": "products",
      "toColumn": "product_id"
    }
  ]
}
```

These JSON files represent your semantic model and can be deployed to Fabric.
