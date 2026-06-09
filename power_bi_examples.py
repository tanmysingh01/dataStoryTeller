"""
Power BI dashboard examples using semantic models.
Demonstrates how to create KPIs, bar charts, line graphs, and other visualizations.
"""

import logging
from power_bi_integration import (
    PowerBIDashboard, PowerBIDashboardBuilder, PowerBIDAXGenerator,
    PowerBIDataExporter, VisualizationType, PowerBIVisualization,
    PowerBIField
)
from semantic_model import (
    create_customer_churn_model,
    create_revenue_growth_model,
    create_supply_chain_risk_model,
    create_integrated_business_model
)

logger = logging.getLogger(__name__)


def example_customer_churn_dashboard():
    """Create dashboard for customer churn analysis.
    
    Includes:
    - Churn Rate KPI
    - Churn by Region bar chart
    - Churn Trend over time
    - At-Risk Customers table
    """
    logger.info("=" * 60)
    logger.info("EXAMPLE: Customer Churn Dashboard")
    logger.info("=" * 60)
    
    # Get semantic model
    model = create_customer_churn_model()
    
    # Create dashboard builder
    builder = PowerBIDashboardBuilder(model)
    dashboard = builder.create_dashboard(
        name="customer_churn",
        display_name="Customer Churn Analysis",
        description="Monitor customer retention and churn patterns"
    )
    
    # Add KPI Cards (Top row)
    logger.info("\n📊 Adding KPI Cards...")
    builder.add_kpi_card("churn_rate", "Churn Rate (%)", target=5.0)
    builder.add_kpi_card("total_customers", "Total Customers")
    builder.add_kpi_card("churned_count", "Churned Customers")
    builder.add_kpi_card("avg_tenure", "Avg Tenure (months)")
    
    # Add Bar Chart: Churn by Region
    logger.info("📊 Adding Bar Chart: Churn by Region...")
    builder.add_bar_chart(
        category="region",
        measure="churn_rate",
        title="Churn Rate by Region (%)",
        table_name="customers"
    )
    
    # Add Bar Chart: Churn by Subscription Type
    logger.info("📊 Adding Bar Chart: Churn by Subscription...")
    builder.add_bar_chart(
        category="subscription_type",
        measure="churn_rate",
        title="Churn Rate by Subscription Type (%)",
        table_name="customers"
    )
    
    # Add Line Chart: Churn Trend over Time
    logger.info("📊 Adding Line Chart: Churn Trend...")
    builder.add_line_chart(
        time_dimension="churn_date",
        measure="churn_rate",
        title="Churn Rate Trend Over Time"
    )
    
    # Add Table: At-Risk Customers
    logger.info("📊 Adding Table: High-Value At-Risk Customers...")
    builder.add_table(
        columns=["customer_name", "region", "monthly_charges", "tenure_months"],
        title="High-Value At-Risk Customers"
    )
    
    # Save dashboard
    dashboard_path = "dashboards/customer_churn_dashboard.json"
    dashboard.save_to_file(dashboard_path)
    
    logger.info(f"\n✅ Dashboard created with {len(dashboard.visualizations)} visualizations")
    logger.info(f"📁 Saved to: {dashboard_path}\n")
    
    return dashboard


def example_revenue_growth_dashboard():
    """Create dashboard for revenue growth analysis.
    
    Includes:
    - Total Revenue KPI
    - Profit Margin KPI
    - Revenue by Product Category
    - Monthly Revenue Trend
    - Top Products by Revenue
    - Regional Revenue Heatmap
    """
    logger.info("=" * 60)
    logger.info("EXAMPLE: Revenue Growth Dashboard")
    logger.info("=" * 60)
    
    # Get semantic model
    model = create_revenue_growth_model()
    
    # Create dashboard builder
    builder = PowerBIDashboardBuilder(model)
    dashboard = builder.create_dashboard(
        name="revenue_growth",
        display_name="Revenue Growth Analysis",
        description="Track sales performance, profitability, and growth trends"
    )
    
    # Add KPI Cards
    logger.info("\n📊 Adding KPI Cards...")
    builder.add_kpi_card("total_sales", "Total Revenue ($)")
    builder.add_kpi_card("profit_margin", "Profit Margin (%)")
    builder.add_kpi_card("total_profit", "Total Profit ($)")
    builder.add_kpi_card("order_count", "Total Orders")
    
    # Add Bar Chart: Revenue by Product Category
    logger.info("📊 Adding Bar Chart: Revenue by Category...")
    builder.add_bar_chart(
        category="category",
        measure="total_sales",
        title="Revenue by Product Category",
        table_name="sales"
    )
    
    # Add Bar Chart: Top 10 Products by Revenue
    logger.info("📊 Adding Bar Chart: Top Products...")
    builder.add_bar_chart(
        category="product_name",
        measure="total_sales",
        title="Top 10 Products by Revenue",
        table_name="products"
    )
    
    # Add Line Chart: Monthly Revenue Trend
    logger.info("📊 Adding Line Chart: Revenue Trend...")
    builder.add_line_chart(
        time_dimension="order_date",
        measure="total_sales",
        title="Monthly Revenue Trend"
    )
    
    # Add Pie Chart: Revenue by Region
    logger.info("📊 Adding Pie Chart: Revenue Distribution...")
    builder.add_pie_chart(
        dimension="region",
        measure="total_sales",
        title="Revenue Distribution by Region"
    )
    
    # Add Matrix: Revenue Analysis
    logger.info("📊 Adding Matrix: Category vs Region Analysis...")
    builder.add_matrix(
        rows=["category"],
        columns=["region"],
        values=["total_sales", "profit_margin"],
        title="Revenue Analysis: Category vs Region"
    )
    
    # Save dashboard
    dashboard_path = "dashboards/revenue_growth_dashboard.json"
    dashboard.save_to_file(dashboard_path)
    
    logger.info(f"\n✅ Dashboard created with {len(dashboard.visualizations)} visualizations")
    logger.info(f"📁 Saved to: {dashboard_path}\n")
    
    return dashboard


def example_supply_chain_dashboard():
    """Create dashboard for supply chain monitoring.
    
    Includes:
    - Days of Supply KPI
    - Stockout Risk Items KPI
    - Overstock Items KPI
    - Inventory by Warehouse
    - Supplier Reliability Scorecard
    - At-Risk Items Table
    """
    logger.info("=" * 60)
    logger.info("EXAMPLE: Supply Chain Risk Dashboard")
    logger.info("=" * 60)
    
    # Get semantic model
    model = create_supply_chain_risk_model()
    
    # Create dashboard builder
    builder = PowerBIDashboardBuilder(model)
    dashboard = builder.create_dashboard(
        name="supply_chain_risk",
        display_name="Supply Chain Risk Monitoring",
        description="Monitor inventory levels, supplier reliability, and supply chain risks"
    )
    
    # Add KPI Cards
    logger.info("\n📊 Adding KPI Cards...")
    builder.add_kpi_card("avg_days_supply", "Avg Days of Supply (days)")
    builder.add_kpi_card("stockout_items", "Items at Stockout Risk")
    builder.add_kpi_card("overstock_items", "Items at Overstock Risk")
    builder.add_kpi_card("total_inventory_units", "Total Inventory Units")
    
    # Add Gauge Chart: Days of Supply
    logger.info("📊 Adding Gauge Chart: Days of Supply...")
    gauge_viz = PowerBIVisualization(
        name="gauge_days_supply",
        title="Days of Supply Status",
        visualization_type=VisualizationType.GAUGE,
        measures=[PowerBIField("avg_days_supply", "Days of Supply", "measure")]
    )
    dashboard.add_visualization(gauge_viz)
    
    # Add Bar Chart: Inventory by Warehouse
    logger.info("📊 Adding Bar Chart: Inventory by Warehouse...")
    builder.add_bar_chart(
        category="warehouse_location",
        measure="total_inventory_units",
        title="Inventory by Warehouse",
        table_name="inventory"
    )
    
    # Add Bar Chart: Supplier Reliability
    logger.info("📊 Adding Bar Chart: Supplier Performance...")
    builder.add_bar_chart(
        category="supplier_name",
        measure="avg_reliability",
        title="Supplier On-Time Delivery Rate",
        table_name="suppliers"
    )
    
    # Add Table: At-Risk Items
    logger.info("📊 Adding Table: At-Risk Items...")
    builder.add_table(
        columns=["product_id", "warehouse_location", "days_of_supply", "stockout_risk"],
        title="Items At Risk (Stockout or Overstock)"
    )
    
    # Add Matrix: Risk by Warehouse and Supplier
    logger.info("📊 Adding Matrix: Risk Analysis...")
    builder.add_matrix(
        rows=["warehouse_location"],
        columns=["supplier_id"],
        values=["stockout_items", "avg_days_supply"],
        title="Risk Assessment: Warehouse vs Supplier"
    )
    
    # Save dashboard
    dashboard_path = "dashboards/supply_chain_dashboard.json"
    dashboard.save_to_file(dashboard_path)
    
    logger.info(f"\n✅ Dashboard created with {len(dashboard.visualizations)} visualizations")
    logger.info(f"📁 Saved to: {dashboard_path}\n")
    
    return dashboard


def example_executive_summary_dashboard():
    """Create executive summary dashboard with KPIs from all models.
    
    High-level view of business health:
    - Customer Health (Churn Rate, Customer Count)
    - Sales Health (Revenue, Profit Margin)
    - Supply Chain Health (Days of Supply, Supplier Reliability)
    """
    logger.info("=" * 60)
    logger.info("EXAMPLE: Executive Summary Dashboard")
    logger.info("=" * 60)
    
    # Get integrated model
    model = create_integrated_business_model()
    
    # Create dashboard
    builder = PowerBIDashboardBuilder(model)
    dashboard = builder.create_dashboard(
        name="executive_summary",
        display_name="Executive Summary",
        description="High-level business metrics and KPIs"
    )
    
    logger.info("\n📊 Adding Executive KPI Cards...")
    
    # Customer metrics
    builder.add_kpi_card("churn_rate", "Customer Churn Rate (%)")
    builder.add_kpi_card("total_customers", "Total Active Customers")
    
    # Revenue metrics
    builder.add_kpi_card("total_sales", "Total Revenue ($)")
    builder.add_kpi_card("profit_margin", "Profit Margin (%)")
    builder.add_kpi_card("order_count", "Total Orders")
    
    # Supply chain metrics
    builder.add_kpi_card("avg_days_supply", "Avg Days Supply (days)")
    builder.add_kpi_card("stockout_items", "At-Risk Items")
    
    # Add key trend charts
    logger.info("📊 Adding Trend Charts...")
    builder.add_line_chart(
        time_dimension="order_date",
        measure="total_sales",
        title="Revenue Trend (Last 12 Months)"
    )
    
    builder.add_pie_chart(
        dimension="region",
        measure="total_sales",
        title="Revenue by Region"
    )
    
    builder.add_bar_chart(
        category="category",
        measure="profit_margin",
        title="Profit Margin by Product Category",
        table_name="products"
    )
    
    # Save dashboard
    dashboard_path = "dashboards/executive_summary_dashboard.json"
    dashboard.save_to_file(dashboard_path)
    
    logger.info(f"\n✅ Executive dashboard created with {len(dashboard.visualizations)} visualizations")
    logger.info(f"📁 Saved to: {dashboard_path}\n")
    
    return dashboard


def example_dax_measures_guide():
    """Generate useful DAX measures for Power BI.
    
    Shows common DAX expressions that can be used in Power BI measures.
    """
    logger.info("=" * 60)
    logger.info("EXAMPLE: DAX Measures Guide")
    logger.info("=" * 60)
    
    dax_generator = PowerBIDAXGenerator()
    
    measures = {
        "Sum Measures": [
            dax_generator.sum_measure("Total_Revenue", "sales_amount", "Sales"),
            dax_generator.sum_measure("Total_Cost", "cost_amount", "Sales"),
        ],
        "Average Measures": [
            dax_generator.average_measure("Avg_Order_Value", "sales_amount", "Sales"),
            dax_generator.average_measure("Avg_Tenure", "tenure_months", "Customers"),
        ],
        "Count Measures": [
            dax_generator.distinct_count_measure("Customer_Count", "customer_id", "Customers"),
            dax_generator.count_measure("Transaction_Count", "sales_id", "Sales"),
        ],
        "Calculated Measures": [
            dax_generator.percentage_measure("Profit_Margin", "[Total_Profit]", "[Total_Revenue]"),
            dax_generator.month_over_month_growth("MoM_Growth", "[Current_Month_Revenue]", "[Prior_Month_Revenue]"),
        ],
        "Time Intelligence": [
            dax_generator.year_to_date_measure("YTD_Revenue", "sales_amount", "Sales", "order_date"),
            dax_generator.running_total("Running_Total_Revenue", "sales_amount", "Sales", "order_date"),
        ]
    }
    
    logger.info("\n📝 Common DAX Measures for Power BI:\n")
    
    for category, dax_list in measures.items():
        logger.info(f"• {category}:")
        for dax_expr in dax_list:
            logger.info(f"  {dax_expr}")
        logger.info("")
    
    # Save to file
    with open("dashboards/dax_measures_reference.txt", "w") as f:
        f.write("DAX Measures Reference for Power BI\n")
        f.write("=" * 60 + "\n\n")
        
        for category, dax_list in measures.items():
            f.write(f"{category}:\n")
            for dax_expr in dax_list:
                f.write(f"{dax_expr}\n")
            f.write("\n")
    
    logger.info("✅ DAX reference saved to: dashboards/dax_measures_reference.txt")


def example_export_for_power_bi():
    """Export semantic models in Power BI-friendly formats.
    
    Creates CSV files and Power BI templates that can be used in Power BI Desktop.
    """
    logger.info("=" * 60)
    logger.info("EXAMPLE: Export for Power BI")
    logger.info("=" * 60)
    
    exporter = PowerBIDataExporter()
    
    # Export each model
    models = {
        "Customer Churn": create_customer_churn_model(),
        "Revenue Growth": create_revenue_growth_model(),
        "Supply Chain Risk": create_supply_chain_risk_model(),
    }
    
    for model_name, model in models.items():
        logger.info(f"\n📊 Exporting {model_name} model...")
        
        # Export to CSV
        csv_files = exporter.export_semantic_model_to_csv(model, f"power_bi_exports/{model_name.lower().replace(' ', '_')}")
        logger.info(f"✓ CSV files created: {len(csv_files)} tables")
        
        # Export to Power BI template
        template_path = f"dashboards/{model_name.lower().replace(' ', '_')}_template.json"
        exporter.export_to_power_bi_template(model, template_path)
        logger.info(f"✓ Power BI template: {template_path}")
    
    logger.info("\n✅ All exports complete!")
    logger.info("💡 Use these files in Power BI Desktop:")
    logger.info("   1. Open Power BI Desktop")
    logger.info("   2. Get Data > More > Folder")
    logger.info("   3. Select the power_bi_exports folder")
    logger.info("   4. Build visualizations from the data")


def example_power_bi_quick_start():
    """Show quick start guide for creating Power BI dashboards.
    
    Provides step-by-step instructions for using generated files.
    """
    logger.info("=" * 60)
    logger.info("Power BI Quick Start Guide")
    logger.info("=" * 60)
    
    guide = """
📊 CREATING POWER BI DASHBOARDS FROM SEMANTIC MODELS

Step 1: Generate Semantic Models and Dashboards
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run examples in main.py to generate:
  • Dashboard definitions (JSON files)
  • DAX measures reference
  • Exported data files

Step 2: Open Power BI Desktop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Download Power BI Desktop (free from Microsoft)
2. Create new project
3. Connect to your Fabric workspace or import data

Step 3: Import Data
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Option A: From Fabric Semantic Models
  1. File > Get Data > Power BI Datasets
  2. Select your Fabric workspace
  3. Choose customer churn, revenue growth, or supply chain model

Option B: From Exported CSV Files
  1. Get Data > Folder
  2. Select power_bi_exports folder
  3. Load and Transform data

Step 4: Create Visualizations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Use Dashboard Templates (dashboards/*.json):
  1. Churn Dashboard (KPIs + Churn by Region + Trend)
  2. Revenue Dashboard (Revenue by Category + Trend + Margin)
  3. Supply Chain Dashboard (Days of Supply + Risk Items)
  4. Executive Summary (All KPIs + Key Trends)

Common Visualizations:
  • KPI Card: Single metric (e.g., Total Revenue)
  • Bar Chart: Compare categories (e.g., Revenue by Region)
  • Line Chart: Trends over time (e.g., Revenue Trend)
  • Pie Chart: Distribution (e.g., Revenue by Region %)
  • Table: Detailed data (e.g., Top Customers)
  • Matrix: Cross-tabulation (e.g., Revenue by Category vs Region)

Step 5: Add Measures Using DAX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reference file: dashboards/dax_measures_reference.txt

Common DAX:
  Churn Rate: AVERAGE(Customers[is_churned])
  Profit Margin: DIVIDE(SUM(Sales[profit]), SUM(Sales[revenue]))
  YoY Growth: DIVIDE(CALCULATE(..., YEAR=2026), CALCULATE(..., YEAR=2025))

Step 6: Create Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Create new blank page for dashboard
2. Add visualizations (pin multiple charts)
3. Add slicers for interactivity (Region, Date Range, etc.)
4. Add KPI cards at top for key metrics
5. Arrange for visual hierarchy

Step 7: Publish to Fabric
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. File > Publish
2. Select your Fabric workspace
3. Report is now available in Power BI Service

Step 8: Set Up Refresh Schedule
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Power BI Service > Dataset Settings
2. Scheduled Refresh > Add schedule
3. Set frequency (e.g., Daily at 2 AM)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DASHBOARD LAYOUT RECOMMENDATIONS

Customer Churn Dashboard:
┌─────────────────────────────────────────────┐
│ Churn Rate: 6.5% │ Total Customers: 5,234  │
│ Churned: 340     │ Avg Tenure: 24 months   │
├─────────────────────────────────────────────┤
│ Churn by Region (Bar)  │ Churn Trend (Line) │
│                        │                     │
├─────────────────────────────────────────────┤
│ Churn by Subscription (Bar)                 │
├─────────────────────────────────────────────┤
│ At-Risk Customers Table                     │
└─────────────────────────────────────────────┘

Revenue Growth Dashboard:
┌─────────────────────────────────────────────┐
│ Revenue: $2.5M    │ Profit Margin: 22%      │
│ Profit: $550K     │ Orders: 12,450          │
├─────────────────────────────────────────────┤
│ Revenue Trend (Line)  │ Profit by Region(Pie)│
├─────────────────────────────────────────────┤
│ Revenue by Category (Bar)                   │
│                                             │
├─────────────────────────────────────────────┤
│ Category vs Region Matrix                   │
└─────────────────────────────────────────────┘

Supply Chain Dashboard:
┌─────────────────────────────────────────────┐
│ Days Supply: 15   │ Stockout Items: 12      │
│ Overstock: 8      │ Total Inventory: 45,230 │
├─────────────────────────────────────────────┤
│ Days Supply (Gauge) │ Inventory by Warehouse│
├─────────────────────────────────────────────┤
│ Supplier Reliability (Bar)                  │
├─────────────────────────────────────────────┤
│ At-Risk Items Table                         │
└─────────────────────────────────────────────┘
"""
    
    logger.info(guide)
    
    # Save to file
    with open("dashboards/POWER_BI_QUICK_START.txt", "w") as f:
        f.write(guide)
    
    logger.info("\n✅ Quick start guide saved to: dashboards/POWER_BI_QUICK_START.txt")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Run examples
    example_customer_churn_dashboard()
    example_revenue_growth_dashboard()
    example_supply_chain_dashboard()
    example_executive_summary_dashboard()
    example_dax_measures_guide()
    example_export_for_power_bi()
    example_power_bi_quick_start()
