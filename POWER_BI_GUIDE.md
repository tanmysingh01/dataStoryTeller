# Power BI Integration Guide

Complete guide to creating and deploying Power BI dashboards from Fabric IQ semantic models.

## Overview

The Power BI integration system provides three key capabilities:

1. **Dashboard Generation** - Create complete dashboard definitions from semantic models
2. **Data Export** - Export semantic model data in Power BI-compatible formats
3. **DAX Code Generation** - Generate DAX measures for common calculations

## Architecture

```
┌─────────────────────────────────────────┐
│   Semantic Models (semantic_model.py)   │
│  • Customer Churn                       │
│  • Revenue Growth                       │
│  • Supply Chain Risk                    │
│  • Integrated Business                  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│  Power BI Integration Layer             │
│  (power_bi_integration.py)              │
├─────────────────────────────────────────┤
│  • PowerBIDashboard - Dashboard builder │
│  • PowerBIVisualization - Chart/KPI def │
│  • PowerBIDAXGenerator - DAX measures   │
│  • PowerBIDataExporter - CSV/JSON export│
│  • PowerBIRESTClient - API integration  │
└──────────────────┬──────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
   ┌─────┐   ┌─────────┐   ┌─────────┐
   │JSON │   │CSV Files│   │DAX Expr │
   │Defs │   │  Export │   │Reference│
   └─────┘   └─────────┘   └─────────┘
      │            │            │
      └────────────┴────────────┘
             │
             ▼
   ┌──────────────────────┐
   │  Power BI Desktop    │
   │  or Power BI Service │
   └──────────────────────┘
             │
             ▼
   ┌──────────────────────┐
   │  Interactive Reports │
   │  & Dashboards        │
   └──────────────────────┘
```

## Module Reference

### power_bi_integration.py

#### Core Classes

**PowerBIVisualization**
```python
from power_bi_integration import PowerBIVisualization, VisualizationType

viz = PowerBIVisualization(
    name="bar_churn_by_region",
    title="Churn Rate by Region",
    visualization_type=VisualizationType.BAR_CHART,
    x_axis=PowerBIField("region", "Region", "dimension"),
    y_axis=PowerBIField("churn_rate", "Churn Rate (%)", "measure")
)
```

**PowerBIDashboard**
```python
from power_bi_integration import PowerBIDashboard

dashboard = PowerBIDashboard(
    name="customer_churn",
    display_name="Customer Churn Analysis",
    description="Monitor customer retention"
)
dashboard.add_visualization(viz)
dashboard.save_to_file("dashboards/churn.json")
```

**PowerBIDashboardBuilder**
```python
from power_bi_integration import PowerBIDashboardBuilder
from semantic_model import create_customer_churn_model

model = create_customer_churn_model()
builder = PowerBIDashboardBuilder(model)
dashboard = builder.create_dashboard("churn", "Churn", "Churn Analysis")

# Add visualizations
builder.add_kpi_card("churn_rate", "Churn Rate (%)")
builder.add_bar_chart("region", "churn_rate", "Churn by Region", "customers")
builder.add_line_chart("churn_date", "churn_rate", "Churn Trend")

# Build and save
dashboard = builder.build()
dashboard.save_to_file("dashboards/churn.json")
```

**PowerBIDAXGenerator**
```python
from power_bi_integration import PowerBIDAXGenerator

dax = PowerBIDAXGenerator()

# Generate common measures
sum_measure = dax.sum_measure("Total_Revenue", "sales_amount", "Sales")
avg_measure = dax.average_measure("Avg_Order_Value", "sales_amount", "Sales")
ytd_measure = dax.year_to_date_measure("YTD_Revenue", "sales_amount", "Sales", "order_date")

# Output: DAX expressions ready to copy into Power BI
# Total_Revenue := SUM(Sales[sales_amount])
# Avg_Order_Value := AVERAGE(Sales[sales_amount])
# YTD_Revenue := CALCULATE(SUM(Sales[sales_amount]), DATESYTD(Sales[order_date]))
```

**PowerBIDataExporter**
```python
from power_bi_integration import PowerBIDataExporter
from semantic_model import create_customer_churn_model

exporter = PowerBIDataExporter()
model = create_customer_churn_model()

# Export to CSV files for Power BI import
csv_files = exporter.export_semantic_model_to_csv(model, "power_bi_exports")

# Export as Power BI template (JSON)
exporter.export_to_power_bi_template(model, "dashboards/template.json")
```

**PowerBIRESTClient** (For Power BI Service Integration)
```python
from power_bi_integration import PowerBIRESTClient

# Authenticate to Power BI Service
client = PowerBIRESTClient(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

if client.authenticate():
    # Get workspaces
    workspaces = client.get_workspaces()
    
    # Create dashboard
    dashboard_id = client.create_dashboard("workspace-id", "My Dashboard")
    
    # Add tile
    client.add_tile_to_dashboard(
        workspace_id="workspace-id",
        dashboard_id=dashboard_id,
        dataset_id="dataset-id",
        visualization_id="viz-id",
        title="Sales Chart"
    )
```

## Visualization Types

Supported visualization types:

| Type | Class | Use Case |
|------|-------|----------|
| Bar Chart | `VisualizationType.BAR_CHART` | Compare categories |
| Column Chart | `VisualizationType.COLUMN_CHART` | Compare categories (vertical) |
| Line Chart | `VisualizationType.LINE_CHART` | Show trends over time |
| Area Chart | `VisualizationType.AREA_CHART` | Show trends with stacked area |
| Pie Chart | `VisualizationType.PIE_CHART` | Show distribution/parts of whole |
| Donut Chart | `VisualizationType.DONUT_CHART` | Show distribution with center info |
| Scatter Chart | `VisualizationType.SCATTER_CHART` | Show correlation |
| Table | `VisualizationType.TABLE` | Show detailed data |
| Matrix | `VisualizationType.MATRIX` | Show cross-tabulation |
| KPI | `VisualizationType.KPI` | Highlight key metric |
| Gauge | `VisualizationType.GAUGE` | Show metric against target |
| Card | `VisualizationType.CARD` | Single metric display |

## Usage Examples

### Example 1: Create Customer Churn Dashboard

```python
from power_bi_integration import PowerBIDashboardBuilder
from semantic_model import create_customer_churn_model

# Get semantic model
model = create_customer_churn_model()

# Create builder
builder = PowerBIDashboardBuilder(model)
dashboard = builder.create_dashboard(
    "customer_churn",
    "Customer Churn Analysis",
    "Monitor customer retention metrics"
)

# Add KPI cards
builder.add_kpi_card("churn_rate", "Churn Rate (%)", target=5.0)
builder.add_kpi_card("total_customers", "Total Customers")
builder.add_kpi_card("churned_count", "Churned Customers")
builder.add_kpi_card("avg_tenure", "Avg Tenure (months)")

# Add charts
builder.add_bar_chart("region", "churn_rate", "Churn by Region", "customers")
builder.add_bar_chart("subscription_type", "churn_rate", "Churn by Subscription", "customers")
builder.add_line_chart("churn_date", "churn_rate", "Churn Trend Over Time")
builder.add_table(["customer_name", "region", "tenure_months", "is_churned"], "At-Risk Customers")

# Save dashboard
dashboard = builder.build()
dashboard.save_to_file("dashboards/customer_churn_dashboard.json")
```

Output: `dashboards/customer_churn_dashboard.json`

### Example 2: Create Revenue Dashboard

```python
from power_bi_integration import PowerBIDashboardBuilder
from semantic_model import create_revenue_growth_model

model = create_revenue_growth_model()
builder = PowerBIDashboardBuilder(model)
dashboard = builder.create_dashboard(
    "revenue_growth",
    "Revenue Analysis",
    "Track sales performance"
)

# KPIs
builder.add_kpi_card("total_sales", "Total Revenue")
builder.add_kpi_card("profit_margin", "Profit Margin (%)")
builder.add_kpi_card("total_profit", "Total Profit")
builder.add_kpi_card("order_count", "Orders")

# Visualizations
builder.add_bar_chart("category", "total_sales", "Revenue by Category", "sales")
builder.add_line_chart("order_date", "total_sales", "Revenue Trend")
builder.add_pie_chart("region", "total_sales", "Revenue by Region")
builder.add_matrix(["category"], ["region"], ["total_sales", "profit_margin"], "Analysis")

dashboard.save_to_file("dashboards/revenue_dashboard.json")
```

### Example 3: Export Data for Power BI Desktop

```python
from power_bi_integration import PowerBIDataExporter
from semantic_model import create_customer_churn_model

exporter = PowerBIDataExporter()
model = create_customer_churn_model()

# Export to CSV files
csv_files = exporter.export_semantic_model_to_csv(model, "power_bi_exports/churn")
# Creates: customers.csv with all columns and measures

# Export as Power BI template
exporter.export_to_power_bi_template(model, "dashboards/churn_template.json")
```

### Example 4: Generate DAX Measures

```python
from power_bi_integration import PowerBIDAXGenerator

dax = PowerBIDAXGenerator()

measures = {
    "Total Sales": dax.sum_measure("Total_Sales", "sales_amount", "Sales"),
    "Profit Margin": dax.percentage_measure("Profit_Margin", "[Total_Profit]", "[Total_Sales]"),
    "YTD Sales": dax.year_to_date_measure("YTD_Sales", "sales_amount", "Sales", "order_date"),
    "MoM Growth": dax.month_over_month_growth("MoM_Growth", "[Current_Month]", "[Prior_Month]"),
}

# Copy these DAX expressions into Power BI:
for name, dax_expr in measures.items():
    print(f"{name}:")
    print(f"  {dax_expr}\n")
```

Output:
```
Total Sales:
  Total_Sales := SUM(Sales[sales_amount])

Profit Margin:
  Profit_Margin := DIVIDE([Total_Profit], [Total_Sales], 0)

YTD Sales:
  YTD_Sales := CALCULATE(
        SUM(Sales[sales_amount]),
        DATESYTD(Sales[order_date])
    )

MoM Growth:
  MoM_Growth := DIVIDE([Current_Month] - [Prior_Month], [Prior_Month], 0)
```

## Integration with Power BI Desktop

### Step 1: Generate Dashboard Definition

```python
from power_bi_examples import example_customer_churn_dashboard

# Generates: dashboards/customer_churn_dashboard.json
example_customer_churn_dashboard()
```

### Step 2: Import Data into Power BI Desktop

**Option A: From Fabric Semantic Model**
1. Power BI Desktop > Get Data > Power BI Datasets
2. Connect to your Fabric workspace
3. Select semantic model (e.g., customer_churn)

**Option B: From Exported CSV**
1. Power BI Desktop > Get Data > Folder
2. Select `power_bi_exports` folder
3. Load and transform data

### Step 3: Create Visualizations

Using the dashboard JSON definition as guide:

1. **Create KPI Cards**
   - Visualization: Card
   - Value: Drag measure (e.g., Churn Rate)
   - Configure formatting

2. **Create Bar Chart**
   - Visualization: Clustered Bar Chart
   - X-Axis: Drag category dimension (e.g., Region)
   - Y-Axis: Drag measure (e.g., Churn Rate)

3. **Create Line Chart**
   - Visualization: Line Chart
   - X-Axis: Drag date (Order Date)
   - Y-Axis: Drag measure (e.g., Total Revenue)

4. **Create Matrix**
   - Visualization: Matrix
   - Rows: Drag dimension (e.g., Category)
   - Columns: Drag dimension (e.g., Region)
   - Values: Drag measures (e.g., Total Sales)

### Step 4: Add DAX Measures

Copy DAX from `dashboards/dax_measures_reference.txt`:

1. Home > New Measure
2. Paste DAX expression
3. Click OK
4. Use measure in visualizations

### Step 5: Build Dashboard

1. Create new blank page named "Dashboard"
2. Pin visualizations to dashboard
3. Arrange for visual hierarchy:
   - KPIs at top
   - Charts in middle
   - Details at bottom
4. Add slicers for interactivity

### Step 6: Publish to Fabric

1. File > Publish
2. Select workspace
3. Report available in Power BI Service

## Dashboard Templates

Pre-built dashboard templates are available in `power_bi_examples.py`:

### Customer Churn Dashboard
- **KPIs**: Churn Rate, Total Customers, Churned Count, Avg Tenure
- **Charts**: Churn by Region (Bar), Churn by Subscription (Bar), Churn Trend (Line)
- **Tables**: At-Risk Customers

### Revenue Growth Dashboard
- **KPIs**: Total Revenue, Profit Margin, Total Profit, Order Count
- **Charts**: Revenue by Category (Bar), Revenue Trend (Line), Revenue Distribution (Pie)
- **Matrix**: Category vs Region Analysis

### Supply Chain Risk Dashboard
- **KPIs**: Days of Supply, Stockout Items, Overstock Items, Total Inventory
- **Gauge**: Days of Supply Status
- **Charts**: Inventory by Warehouse (Bar), Supplier Performance (Bar)
- **Tables**: At-Risk Items

### Executive Summary Dashboard
- **KPIs**: All key metrics from all models
- **Charts**: Top trends and key metrics
- **Summary**: Business health snapshot

## Running Examples

To generate all dashboard definitions:

```bash
# In main.py, uncomment:
# example_power_bi_churn_dashboard()
# example_power_bi_revenue_dashboard()
# example_power_bi_supply_chain_dashboard()
# example_power_bi_executive_dashboard()
# example_power_bi_dax_measures()
# example_power_bi_export()
# example_power_bi_quick_start_guide()

python main.py
```

Outputs:
- `dashboards/customer_churn_dashboard.json`
- `dashboards/revenue_growth_dashboard.json`
- `dashboards/supply_chain_dashboard.json`
- `dashboards/executive_summary_dashboard.json`
- `dashboards/dax_measures_reference.txt`
- `dashboards/POWER_BI_QUICK_START.txt`
- `power_bi_exports/` (CSV files)

## Best Practices

### Dashboard Design
- **KPIs First**: Start with key metrics at top
- **Hierarchy**: Drill-down from overview to details
- **Consistent Colors**: Use business color scheme
- **Clear Titles**: Each visualization needs clear title
- **Filters**: Add date, region, category slicers

### Measure Naming
- Use PascalCase: `Total_Revenue`, not `totalrevenue`
- Descriptive: `Profit_Margin_Percent`, not `pm`
- Include unit in format string: "$#,##0.00", not just number

### Performance
- Aggregate before Power BI when possible
- Avoid complex DAX calculations
- Limit visual interactions
- Use aggregated tables for large datasets

### Security
- Row-level security (RLS) for sensitive data
- Restrict access to workspaces
- Audit report usage
- Refresh sensitive data in off-hours

## Troubleshooting

### Dashboard Won't Import

**Issue**: JSON file is invalid
```bash
# Validate JSON
python -c "import json; json.load(open('dashboards/churn.json'))"
```

**Solution**: Check semantic model validation before save
```python
validation = model.validate()
if validation['valid']:
    dashboard.save_to_file("dashboards/churn.json")
else:
    print(validation['issues'])
```

### Measures Not Showing

**Issue**: Columns not visible in Power BI
- Check column `hidden` attribute
- Verify measure references correct column name
- Validate data types match

**Solution**: Review semantic model
```python
model = create_customer_churn_model()
print(model.to_json())  # Check column and measure definitions
```

### Data Not Refreshing

**Issue**: Dashboard shows stale data
- Set refresh schedule in Power BI Service
- Check data source connectivity
- Verify lakehouse data is current

## API Integration (Advanced)

For production dashboards programmatically created in Power BI Service:

```python
from power_bi_integration import PowerBIRESTClient

# Authenticate
client = PowerBIRESTClient(
    tenant_id=os.getenv("TENANT_ID"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

if client.authenticate():
    # Get workspaces
    workspaces = client.get_workspaces()
    workspace_id = workspaces[0]['id']
    
    # Create dashboard
    dashboard_id = client.create_dashboard(workspace_id, "Analytics")
    
    # Refresh data
    client.refresh_dataset(workspace_id, "dataset-id")
```

## Next Steps

1. **Generate Dashboards**: Run `example_power_bi_*_dashboard()` functions
2. **Export Data**: Run `example_export_for_power_bi()`
3. **Review Templates**: Open `dashboards/POWER_BI_QUICK_START.txt`
4. **Import to Power BI**: Use CSV files or Fabric semantic models
5. **Create Visualizations**: Follow dashboard templates
6. **Deploy**: Publish to Power BI Service
7. **Monitor**: Set up refresh schedules and alerts

See [POWER_BI_QUICK_START.txt](dashboards/POWER_BI_QUICK_START.txt) for step-by-step instructions.
