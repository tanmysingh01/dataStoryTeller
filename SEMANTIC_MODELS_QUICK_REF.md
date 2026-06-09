# Semantic Models Quick Reference

One-page reference for the three pre-built semantic models and how to use them.

## Customer Churn Model

**Purpose:** Identify and analyze customer churn patterns

**Key Metric:** Churn Rate (% of customers lost)

| Raw Column | Business Concept | Type | Format |
|---|---|---|---|
| customer_id | Customer ID | Dimension | (hidden) |
| customer_name | Customer Name | Attribute | Text |
| tenure_months | Tenure (Months) | Metric | 0 months |
| monthly_charges | Monthly Charges | Metric | $#,##0.00 |
| total_charges | Lifetime Value | Metric | $#,##0.00 |
| is_churned | Churned Status | Dimension | T/F |
| churn_date | Churn Date | Time | Date |
| subscription_type | Subscription | Dimension | Text |
| region | Region | Dimension | Text |

**Measures (Pre-built):**
- Total Customers (DISTINCT COUNT)
- Churned Customers (COUNT WHERE is_churned=TRUE)
- Churn Rate (AVG is_churned) → Format: 0.00%
- Avg Customer Tenure (AVG tenure_months) → Format: 0 months
- Avg Revenue Per User (AVG monthly_charges) → Format: $#,##0.00
- Total Lifetime Revenue (SUM total_charges) → Format: $#,##0.00

**Hierarchies:**
1. Churn Analysis: Region > Subscription Type > Customer
2. Tenure Analysis: Region > Tenure Months

**Typical Questions Answered:**
- "What's our overall churn rate?"
- "Which regions have the highest churn?"
- "Which subscription types are most at-risk?"
- "What's the revenue impact of churn?"
- "Who are our high-value at-risk customers?"

**Python Usage:**
```python
from semantic_model import create_customer_churn_model
model = create_customer_churn_model()
customers = model.get_table("customers")
# Add custom measures, hierarchies, or save
model.save_to_file("models/customer_churn_model.json")
```

---

## Revenue Growth Model

**Purpose:** Track sales performance and growth across products and regions

**Key Metric:** Total Revenue & Profit Margin

| Raw Column | Business Concept | Type | Format |
|---|---|---|---|
| sales_id | Sales ID | Dimension | (hidden) |
| order_date | Order Date | Time | Date |
| product_id | Product ID | Dimension | (hidden) |
| product_name | Product Name | Attribute | Text |
| category | Category | Dimension | Text |
| subcategory | Subcategory | Dimension | Text |
| quantity | Quantity Sold | Metric | #,##0 units |
| unit_price | Unit Price | Attribute | $#,##0.00 |
| sales_amount | Sales Revenue | Metric | $#,##0.00 |
| cost_amount | Cost of Goods | Metric | $#,##0.00 |
| profit_amount | Gross Profit | Metric | $#,##0.00 |
| region | Region | Dimension | Text |

**Measures (Pre-built):**
- Total Revenue (SUM sales_amount) → Format: $#,##0.00
- Total Cost (SUM cost_amount) → Format: $#,##0.00
- Total Profit (SUM profit_amount) → Format: $#,##0.00
- Profit Margin (AVG profit/sales) → Format: 0.00%
- Order Count (DISTINCT sales_id)
- Average Order Value (AVG sales_amount) → Format: $#,##0.00
- Units Sold (SUM quantity) → Format: #,##0

**Hierarchies:**
1. Regional Analysis: Region > Category > Product
2. Time Analysis: Order Date (drill to Year/Quarter/Month)
3. Product Hierarchy: Category > Subcategory > Product

**Relationships:**
- Sales.product_id → Products.product_id (many-to-one)

**Typical Questions Answered:**
- "What's our total revenue?"
- "Which products drive the most profit?"
- "How does revenue differ by region?"
- "What's our profit margin trending?"
- "Which categories are growing fastest?"
- "Show me Q1 vs Q2 performance"

**Python Usage:**
```python
from semantic_model import create_revenue_growth_model
model = create_revenue_growth_model()
sales = model.get_table("sales")
# Sales and products are already linked
# Add hierarchies or custom measures
model.save_to_file("models/revenue_growth_model.json")
```

---

## Supply Chain Risk Model

**Purpose:** Monitor inventory and supplier risks

**Key Metric:** Days of Supply & Stockout Risk Count

| Raw Column | Business Concept | Type | Format |
|---|---|---|---|
| supplier_id | Supplier ID | Dimension | (hidden) |
| supplier_name | Supplier Name | Attribute | Text |
| country | Country | Dimension | Text |
| reliability_score | On-Time Delivery % | Metric | 0.00% |
| avg_lead_time_days | Avg Lead Time | Metric | 0 days |
| quality_score | Quality Rating | Metric | 0-100 |
| warehouse_location | Warehouse | Dimension | Text |
| current_stock_level | Current Stock | Metric | #,##0 units |
| safety_stock_level | Safety Stock | Metric | #,##0 units |
| reorder_point | Reorder Point | Metric | #,##0 units |
| days_of_supply | Days of Supply | Metric | 0.0 days |
| stockout_risk | Stockout Risk | Dimension | T/F |
| overstock_risk | Overstock Risk | Dimension | T/F |

**Measures (Pre-built):**
- Total Inventory Units (SUM current_stock_level) → Format: #,##0 units
- Avg Days of Supply (AVG days_of_supply) → Format: 0.0 days
- Stockout Risk Items (COUNT WHERE stockout_risk=TRUE)
- Overstock Risk Items (COUNT WHERE overstock_risk=TRUE)
- Avg Supplier Reliability (AVG reliability_score) → Format: 0.00%
- Avg Lead Time (AVG avg_lead_time_days) → Format: 0 days
- Avg Quality Score (AVG quality_score) → Format: 0-100

**Hierarchies:**
1. Inventory Risk: Warehouse > Stockout Risk > Product
2. Supplier Analysis: Supplier > Lead Time > Product
3. Supply Chain: Warehouse > Supplier Reliability

**Relationships:**
- Inventory.supplier_id → Suppliers.supplier_id (many-to-one)

**Typical Questions Answered:**
- "Which items are at risk of stockout?"
- "Which items are overstocked?"
- "Which suppliers are unreliable?"
- "What's our average days of supply?"
- "Where are supply chain bottlenecks?"
- "Which products have long lead times?"
- "Alert: How many items need immediate reorder?"

**Python Usage:**
```python
from semantic_model import create_supply_chain_risk_model
model = create_supply_chain_risk_model()
inventory = model.get_table("inventory")
suppliers = model.get_table("suppliers")
# Inventory and suppliers are already linked
model.save_to_file("models/supply_chain_model.json")
```

---

## Integrated Business Model

**Purpose:** Analyze customer, revenue, and supply chain together

**Combines:** All tables and measures from above three models

```python
from semantic_model import create_integrated_business_model
model = create_integrated_business_model()
# 9 total tables, 27+ measures, multiple relationships
model.save_to_file("models/integrated_business_model.json")
```

**Example Cross-Model Analysis:**
- "High-value customers with stockout risk products"
- "Revenue impact from supplier reliability"
- "Customer churn in low-supply regions"

---

## Common Extensions

### Add Custom Measure to Any Model

```python
model = create_customer_churn_model()
customers = model.get_table("customers")

# Add new measure
customers.add_measure(Measure(
    "high_value_churn",
    "High Value Churn",
    "Churned customers with monthly charges > $100",
    "customer_id",
    AggregationFunction.COUNT,
    calculation="CALCULATE(COUNT(...), FILTER(customers, monthly_charges > 100 AND is_churned = TRUE()))"
))

model.save_to_file("models/customer_churn_extended.json")
```

### Add Custom Hierarchy

```python
customers.add_hierarchy(Hierarchy(
    "value_segment",
    "Value Segmentation",
    "Drill down by value and risk",
    ["subscription_type", "monthly_charges", "tenure_months"]
))
```

### Create Brand New Model

```python
from semantic_model import SemanticModel, SemanticTable, Column, Measure, DataType, AggregationFunction

model = SemanticModel("marketing", "Marketing Campaigns")
campaigns = SemanticTable("campaigns", "Campaigns")

campaigns.add_column(Column("campaign_id", "Campaign ID", DataType.STRING))
campaigns.add_column(Column("spend", "Spend", DataType.DECIMAL))
campaigns.add_column(Column("revenue", "Revenue", DataType.DECIMAL))

campaigns.add_measure(Measure(
    "roi",
    "ROI",
    "Return on Investment",
    "revenue",
    AggregationFunction.SUM,
    format_string="0.0%",
    calculation="(SUM(revenue) - SUM(spend)) / SUM(spend)"
))

model.add_table(campaigns)
model.save_to_file("models/marketing_model.json")
```

---

## Running Examples

```bash
# Generate JSON files for all models
python main.py

# Uncomment example functions in main.py:
# example_semantic_customer_churn()          # Generates customer_churn_model.json
# example_semantic_revenue_growth()          # Generates revenue_growth_model.json
# example_semantic_supply_chain()            # Generates supply_chain_model.json
# example_semantic_integrated()              # Generates integrated_business_model.json
# example_semantic_custom()                  # Generates custom_marketing_model.json
# example_semantic_extend()                  # Generates customer_churn_extended.json
# example_semantic_comparison()              # Prints comparison table
```

**Output:** Models are saved to `models/` directory as JSON files ready for Fabric deployment

---

## Best Practices Checklist

✅ **Naming**
- [ ] Use clear display names ("Churn Rate", not "churn")
- [ ] Hide technical IDs (customer_id, product_id)
- [ ] Document each measure with description

✅ **Formatting**
- [ ] Use format strings for currency ($#,##0.00)
- [ ] Use format strings for percentages (0.00%)
- [ ] Use format strings for counts (#,##0)

✅ **Structure**
- [ ] Define all key relationships
- [ ] Create hierarchies for common drill paths
- [ ] Hide columns users shouldn't see

✅ **Quality**
- [ ] Validate model before saving (model.validate())
- [ ] Test common queries work
- [ ] Document any custom calculations

✅ **Extensibility**
- [ ] Use clear naming for future additions
- [ ] Document column purposes
- [ ] Keep measures focused on single concepts

---

## File Structure After Examples

```
models/
├── customer_churn_model.json           (example_semantic_customer_churn)
├── revenue_growth_model.json           (example_semantic_revenue_growth)
├── supply_chain_model.json             (example_semantic_supply_chain)
├── integrated_business_model.json      (example_semantic_integrated)
├── custom_marketing_model.json         (example_semantic_custom)
└── customer_churn_extended.json        (example_semantic_extend)
```

Each JSON file can be deployed directly to Fabric workspace.

---

## Support & Resources

- **Comprehensive Guide:** [SEMANTIC_MODEL_GUIDE.md](SEMANTIC_MODEL_GUIDE.md)
- **Real-World Examples:** [SEMANTIC_MAPPING_EXAMPLES.md](SEMANTIC_MAPPING_EXAMPLES.md)
- **System Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Main Documentation:** [README.md](README.md)
- **Data Ingestion:** [DATA_INGESTION_GUIDE.md](DATA_INGESTION_GUIDE.md)

## Next Steps

1. Run examples to generate JSON model files
2. Review generated models in `models/` directory
3. Customize models for your business
4. Deploy to Fabric workspace
5. Connect Power BI and create dashboards
6. Monitor usage and refine hierarchies
