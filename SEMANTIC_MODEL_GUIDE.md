# Semantic Models in Microsoft Fabric

Comprehensive guide to defining, implementing, and extending semantic models that map raw data to business concepts.

## Overview

A semantic model transforms raw data columns into meaningful business metrics and relationships. Instead of exposing technical details, business users see intuitive concepts like "Customer Churn", "Revenue Growth", and "Supply Chain Risk".

### Key Components

- **Tables** - Data entities (Customers, Sales, Inventory)
- **Columns** - Data attributes (Customer ID, Sales Amount, Stock Level)
- **Measures** - Business metrics (Total Revenue, Churn Rate, Days of Supply)
- **Hierarchies** - Drill-down paths (Region > Customer > Transaction)
- **Relationships** - Table connections (Sales → Products → Suppliers)

## Architecture

```
Raw Data (CSV, SQL Server)
    ↓
Data Ingestion Pipeline
    ↓
Lakehouse (Physical Tables)
    ↓
Semantic Model (Business Layer)
    ↓
Business Users (Reports, Dashboards, Analysis)
```

## Semantic Models Included

### 1. Customer Churn Model

**Purpose:** Identify and analyze customer churn patterns

**Raw Columns Mapped:**
```
customer_id           → Customer identifier
tenure_months         → Tenure metric
monthly_charges       → Revenue metric
is_churned            → Churn status
churn_date            → Historical tracking
region                → Geographic dimension
subscription_type     → Service offering
```

**Business Concepts Created:**
- Total Customers (distinct count of customers)
- Churned Customers (count of customers with is_churned=true)
- Churn Rate (% of customers who churned)
- Average Tenure (customer retention metric)
- Average Monthly Charges (ARPU)
- Total Revenue (lifetime customer value)

**Hierarchies for Analysis:**
- Region > Subscription Type > Customer
- Tenure Bands > Region > Customer

### 2. Revenue Growth Model

**Purpose:** Track sales performance across products, regions, and time

**Raw Columns Mapped:**
```
sales_id              → Transaction identifier
order_date            → Time dimension
product_id            → Product identifier
region                → Geographic dimension
quantity              → Sales volume
unit_price            → Pricing data
sales_amount          → Revenue (quantity × price)
cost_amount           → Cost of goods sold
profit_amount         → Gross profit
```

**Business Concepts Created:**
- Total Sales (sum of all sales amounts)
- Total Cost (sum of all costs)
- Total Profit (sum of all profits)
- Profit Margin (profit % of sales)
- Order Count (transaction count)
- Average Order Value (sales per transaction)

**Hierarchies for Analysis:**
- Region > Product Category > Product > Order Date
- Category > Subcategory > Product

**Relationships:**
- Sales → Products (many-to-one on product_id)

### 3. Supply Chain Risk Model

**Purpose:** Monitor inventory levels and supplier reliability

**Raw Columns Mapped:**
```
supplier_id           → Supplier identifier
reliability_score     → On-time delivery %
avg_lead_time_days    → Lead time metric
quality_score         → Quality rating

current_stock_level   → Inventory quantity
safety_stock_level    → Minimum threshold
reorder_point         → Reorder trigger
days_of_supply        → Inventory coverage
stockout_risk         → Risk indicator
overstock_risk        → Risk indicator
```

**Business Concepts Created:**
- Supplier Count (total suppliers)
- Average Reliability (on-time delivery rate)
- Average Lead Time (supplier performance)
- Total Inventory Units (total stock)
- Average Days of Supply (inventory coverage)
- Stockout Risk Count (at-risk products)
- Overstock Risk Count (excess inventory)

**Hierarchies for Analysis:**
- Warehouse Location > Stockout Risk > Product
- Supplier Country > Reliability Score

**Relationships:**
- Inventory → Suppliers (many-to-one on supplier_id)

## How Semantic Models Work

### Step 1: Map Raw Data

```python
from semantic_model import Column, DataType

# Raw columns become meaningful business attributes
customers_table.add_column(Column(
    name="tenure_months",           # Raw column name
    display_name="Tenure (Months)", # Business user label
    data_type=DataType.INT,
    description="Months as customer"
))
```

### Step 2: Define Business Metrics

```python
from semantic_model import Measure, AggregationFunction

# Create metrics from raw columns
customers_table.add_measure(Measure(
    name="churn_rate",
    display_name="Churn Rate",
    description="Percentage of customers who churned",
    column="is_churned",
    aggregation=AggregationFunction.AVG,
    format_string="0.00%"  # Display as percentage
))
```

### Step 3: Create Relationships

```python
from semantic_model import Relationship

# Connect tables for cross-dimensional analysis
model.add_relationship(Relationship(
    from_table="sales",
    from_column="product_id",
    to_table="products",
    to_column="product_id",
    cardinality="many-to-one"
))
```

### Step 4: Define Hierarchies

```python
from semantic_model import Hierarchy

# Enable drill-down analysis
products_table.add_hierarchy(Hierarchy(
    name="product_hierarchy",
    display_name="Product Hierarchy",
    description="Product category drill-down",
    levels=["category", "subcategory", "product_name"]
))
```

## Usage Examples

### Create a Semantic Model

```python
from semantic_model import (
    SemanticModel, SemanticTable, Column, Measure,
    DataType, AggregationFunction
)

# 1. Create model
model = SemanticModel(
    name="sales_analysis",
    display_name="Sales Analysis Model",
    description="Analyze sales performance"
)

# 2. Create table
sales = SemanticTable("sales", "Sales", "Sales transactions")

# 3. Add columns
sales.add_column(Column("sales_id", "Sales ID", DataType.STRING))
sales.add_column(Column("amount", "Amount", DataType.DECIMAL))

# 4. Add measures
sales.add_measure(Measure(
    "total_sales",
    "Total Sales",
    "Sum of all sales",
    "amount",
    AggregationFunction.SUM,
    format_string="$#,##0.00"
))

# 5. Add to model
model.add_table(sales)

# 6. Validate and save
validation = model.validate()
model.save_to_file("sales_model.json")
```

### Use Pre-built Models

```python
from semantic_model import create_customer_churn_model

# Get ready-to-use model
model = create_customer_churn_model()

# Customize
customers = model.get_table("customers")
customers.add_measure(Measure(
    "high_value_churn",
    "High Value Churns",
    "Churn of customers with monthly charges > $100",
    "customer_id",
    AggregationFunction.COUNT,
    calculation="CALCULATE(COUNT(...), FILTER(...))"
))

# Save
model.save_to_file("churn_model_extended.json")
```

### Validate Models

```python
# Check model integrity
validation = model.validate()

print(f"Valid: {validation['valid']}")
print(f"Tables: {validation['table_count']}")
print(f"Relationships: {validation['relationship_count']}")

if validation['issues']:
    for issue in validation['issues']:
        print(f"ERROR: {issue}")

if validation['warnings']:
    for warning in validation['warnings']:
        print(f"WARNING: {warning}")
```

## Extending Semantic Models

### Add New Measures

```python
# Extend existing table with new metric
customers = model.get_table("customers")

customers.add_measure(Measure(
    "at_risk_customers",
    "At-Risk Customers",
    "High-value customers with short tenure (< 12 months)",
    "customer_id",
    AggregationFunction.COUNT,
    calculation="CALCULATE(COUNT(...), FILTER(...))"
))
```

### Add New Hierarchies

```python
# Enable new drill-down paths
customers.add_hierarchy(Hierarchy(
    "value_segment",
    "Value Segmentation",
    "Segment by subscription type and charges",
    ["subscription_type", "monthly_charges"]
))
```

### Add New Tables

```python
# Extend model with related data
support_tickets = SemanticTable(
    "support_tickets",
    "Support Tickets",
    "Customer support interactions"
)

support_tickets.add_column(Column("ticket_id", "Ticket ID", DataType.STRING))
support_tickets.add_column(Column("customer_id", "Customer ID", DataType.STRING))
support_tickets.add_column(Column("resolution_time_hours", "Resolution Time", DataType.INT))

model.add_table(support_tickets)

# Connect to customers
model.add_relationship(Relationship(
    from_table="support_tickets",
    from_column="customer_id",
    to_table="customers",
    to_column="customer_id",
    cardinality="many-to-one"
))
```

### Create Composite Models

```python
from semantic_model import create_integrated_business_model

# Combine multiple models
integrated = create_integrated_business_model()

# Now can analyze:
# - Customer churn AND revenue impact
# - Supply chain risk AND sales performance
# - Inventory levels AND customer satisfaction
```

## Column Mapping Examples

### Customer Churn: Raw → Business

```
Raw Data (SQL/CSV)          Semantic Model (Business)
─────────────────────────── ──────────────────────────
cust_id                  →  Customer ID (hidden)
cust_name               →  Customer Name
tenure_mo               →  Tenure (Months)
subs_type               →  Subscription Type
monthly_fee             →  Monthly Charges
total_fee               →  Total Charges
is_churn                →  Is Churned
churn_dt                →  Churn Date
geo_region              →  Region

Calculated Measures:
                        →  Churn Rate (AVG(is_churn))
                        →  Average Tenure (AVG(tenure_mo))
                        →  Total Revenue (SUM(total_fee))
```

### Revenue Growth: Raw → Business

```
Raw Data                    Semantic Model
─────────────────────────── ──────────────────────────
sales_no                →  Sales ID (hidden)
order_dt                →  Order Date
prod_no                 →  Product ID (hidden)
prd_name                →  Product Name
category                →  Category
qty_sold                →  Quantity
unit_price              →  Unit Price
region                  →  Region
sales_val               →  Sales Amount

Calculated Measures:
                        →  Total Sales (SUM(sales_val))
                        →  Order Count (DISTINCT sales_no)
                        →  Average Order Value (AVG(sales_val))
```

### Supply Chain: Raw → Business

```
Raw Data                    Semantic Model
─────────────────────────── ──────────────────────────
supplier_no             →  Supplier ID (hidden)
supplier_name           →  Supplier Name
on_time_pct             →  Reliability Score
lead_days               →  Avg Lead Time (Days)

warehouse_loc           →  Warehouse Location
prod_qty                →  Current Stock Level
safety_qty              →  Safety Stock Level
days_inv                →  Days of Supply
is_stockout_risk        →  Stockout Risk

Calculated Measures:
                        →  Total Inventory (SUM(prod_qty))
                        →  Avg Days Supply (AVG(days_inv))
                        →  At-Risk Items (COUNT WHERE risk=true)
```

## Data Type Support

Semantic models support various data types:

| Type | Example | Use Cases |
|------|---------|-----------|
| INT | 100, 500, 1000 | Counts, quantities, days |
| FLOAT | 3.14, 99.99 | Ratings, percentages, decimals |
| STRING | "Northeast", "Premium" | Names, categories, descriptions |
| DATE | 2024-06-09 | Dates, time dimensions |
| BOOLEAN | true, false | Flags, binary indicators |
| DECIMAL | $1,234.56 | Currency, precise decimals |

## Aggregation Functions

Each measure uses an aggregation function:

| Function | Purpose | Example |
|----------|---------|---------|
| SUM | Total | Total Revenue, Total Inventory |
| AVG | Average | Average Tenure, Average Order Value |
| COUNT | Count | Order Count, Customer Count |
| MIN | Minimum | Min Lead Time, Min Stock Level |
| MAX | Maximum | Max Price, Max Tenure |
| DISTINCT_COUNT | Unique | Unique Customers, Unique Products |
| LAST | Last Value | Last Status, Latest Date |
| FIRST | First Value | First Order Date, Initial Status |

## Format Strings

Format strings control measure display:

```
"0.00"          → 1234.57
"$#,##0.00"     → $1,234.57
"0.00%"         → 85.42%
"#,##0"         → 1,235 (no decimals)
"0 days"        → 14 days
"0.0x"          → 1.5x (multiple)
```

## Relationships & Cardinality

Relationships define how tables connect:

| Cardinality | From | To | Example |
|-------------|------|-----|---------|
| many-to-one | Sales (many) | Products (one) | Many sales per product |
| one-to-many | Customers (one) | Orders (many) | One customer many orders |
| one-to-one | Employee | EmployeeDetails | One employee one record |
| many-to-many | Authors | Books | Many authors per book, many books per author |

## Best Practices

### 1. Clear Naming Conventions

```python
✓ GOOD
Column("monthly_charges", "Monthly Charges")
Measure("churn_rate", "Churn Rate")

✗ BAD
Column("mc", "MC")
Measure("churn", "Churn")
```

### 2. Hide Technical Keys

```python
table.hide_column("customer_id")
table.hide_column("sales_id")
# Business users see only meaningful data
```

### 3. Use Format Strings

```python
Measure(..., format_string="$#,##0.00")  # Currency
Measure(..., format_string="0.00%")      # Percentage
Measure(..., format_string="#,##0")      # Count
```

### 4. Document Everything

```python
Column("tenure_months", "Tenure (Months)", 
    description="Number of complete months customer has been active")

Measure("churn_rate", "Churn Rate",
    description="Percentage of customers who cancelled subscription within period")
```

### 5. Design for Analysis

```python
# Create hierarchies that support drill-down
Hierarchy("sales_drill", "Sales Analysis",
    levels=["region", "category", "product", "date"])

# This enables: Region > Category > Product > Date analysis
```

### 6. Validate Before Deployment

```python
validation = model.validate()
if not validation['valid']:
    for issue in validation['issues']:
        print(f"FIX BEFORE DEPLOY: {issue}")
```

## Performance Considerations

### 1. Limit Calculated Measures

```python
# Use calculated measures sparingly - they impact query performance
# Pre-calculate in ETL when possible
```

### 2. Index Key Columns

```python
# Ensure fact table keys are indexed in source database
CREATE INDEX idx_sales_product ON sales(product_id)
CREATE INDEX idx_sales_date ON sales(order_date)
```

### 3. Aggregate Properly

```python
# Design aggregations for query efficiency
# Use SUM/COUNT for detailed facts
# Pre-aggregate for historical data
```

## Deployment Checklist

- [ ] All tables defined with display names
- [ ] All key relationships created
- [ ] Hidden technical columns marked
- [ ] Format strings applied to measures
- [ ] Hierarchies defined for drill-down
- [ ] Model validates with no issues
- [ ] Documentation complete
- [ ] Sample queries tested
- [ ] Performance tested with data
- [ ] Model file saved and versioned

## Advanced: Custom Calculations

For complex business logic, use DAX/M expressions:

```python
Measure(
    name="at_risk_customers",
    display_name="At-Risk Customers",
    description="High-value customers with short tenure",
    column="customer_id",
    aggregation=AggregationFunction.COUNT,
    calculation="""
        CALCULATE(
            COUNT(customers[customer_id]),
            FILTER(
                customers,
                customers[monthly_charges] > 100
                AND customers[tenure_months] < 12
            )
        )
    """
)
```

## Troubleshooting

### Issue: Relationship References Invalid Column

```
ERROR: Relationship references non-existent column: sales.xyz
```

**Solution:** Verify column name matches exactly (case-sensitive)

### Issue: Circular Relationships

```
WARNING: Model contains potential circular relationships
```

**Solution:** Review relationships - ensure they form a tree structure

### Issue: High Null Percentages

```
WARNING: High null percentage detected: 65.50%
```

**Solution:** Check data quality - investigate missing data in source

## Examples in Code

Run examples:

```bash
# Customer churn model
python main.py example_semantic_customer_churn

# Revenue growth model
python main.py example_semantic_revenue_growth

# Supply chain model
python main.py example_semantic_supply_chain

# Create custom model
python main.py example_semantic_custom

# Extend existing model
python main.py example_semantic_extend

# Compare models
python main.py example_semantic_comparison
```

## Files Generated

When you run semantic model examples:

```
models/
├── customer_churn_model.json
├── revenue_growth_model.json
├── supply_chain_model.json
├── integrated_business_model.json
├── custom_marketing_model.json
└── customer_churn_extended.json
```

## Resources

- [Module: semantic_model.py](semantic_model.py)
- [Examples: semantic_model_examples.py](semantic_model_examples.py)
- [Microsoft Fabric Docs](https://learn.microsoft.com/fabric/)
- [Semantic Model Best Practices](https://learn.microsoft.com/power-bi/guidance/star-schema)

## Next Steps

1. **Review** the three pre-built models (Churn, Revenue, Supply Chain)
2. **Run** example code to generate model JSON files
3. **Customize** models to match your business definitions
4. **Deploy** to Fabric workspace
5. **Connect** to Power BI for visualization
6. **Monitor** usage and refine hierarchies based on user queries
