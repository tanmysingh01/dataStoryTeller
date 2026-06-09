# Architecture Overview

Complete architecture showing how raw data flows through ingestion to semantic models to business insights.

## End-to-End Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  • CSV Files (OneLake)           • SQL Server Tables                        │
│  • SQL Queries                   • Web APIs                                 │
└──────────────────────┬──────────────────────────────┬──────────────────────┘
                       │                              │
                       ▼                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                                     │
│                 (data_ingestion.py)                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐                       │
│  │  OneLakeDataSource   │  │   SQLDataSource      │                       │
│  │                      │  │                      │                       │
│  │ • read_csv()         │  │ • connect()          │                       │
│  │ • upload_to_lake()   │  │ • query()            │                       │
│  │ • list_files()       │  │ • bulk_insert()      │                       │
│  └──────────────────────┘  └──────────────────────┘                       │
│           │                         │                                      │
│           └─────────┬───────────────┘                                      │
│                     │                                                       │
│            ┌────────▼─────────┐                                            │
│            │ DataIngestion    │                                            │
│            │ Pipeline         │                                            │
│            │                  │                                            │
│            │ • ingest_csv()   │                                            │
│            │ • ingest_sql()   │                                            │
│            │ • ingest_batch() │                                            │
│            │ • validation     │                                            │
│            │ • error handling │                                            │
│            │ • logging        │                                            │
│            └────────┬─────────┘                                            │
│                     │                                                       │
└─────────────────────┼───────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FABRIC LAKEHOUSE                                         │
│                 (Physical Tables)                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  customers  │  sales  │  products  │  suppliers  │  inventory              │
│  ──────────────────────────────────────────────────────────────             │
│  Raw Data Rows (CSV imported, SQL synced)                                   │
│  No business logic, no aggregations, just tables                            │
│                                                                             │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SEMANTIC MODEL LAYER                                      │
│             (semantic_model.py, SEMANTIC_MODEL_GUIDE.md)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║  CUSTOMER CHURN MODEL                                                ║  │
│  ║  ─────────────────────────────────────────────────────────────────  ║  │
│  ║  Tables:                                                            ║  │
│  ║  ├─ Customers                                                       ║  │
│  ║  │  ├─ Columns: Name, Tenure, Subscription, Region                 ║  │
│  ║  │  ├─ Measures: Churn Rate, Avg Tenure, Total Revenue            ║  │
│  ║  │  └─ Hierarchies: Region > Subscription > Customer              ║  │
│  ║  │                                                                  ║  │
│  ║  ║  Relationships: None                                             ║  │
│  ║  │                                                                  ║  │
│  ║  Raw Mapping:                                                       ║  │
│  ║    customer_id             → Customer ID (hidden)                   ║  │
│  ║    tenure_months           → Tenure (Months)                        ║  │
│  ║    monthly_charges         → Monthly Charges (ARPU)                ║  │
│  ║    is_churned + churn_date → Churn Rate, Status                   ║  │
│  ║    region                  → Region (Dimension)                     ║  │
│  ║    subscription_type       → Subscription Type (Dimension)          ║  │
│  ║  ╔════════════════════════════════════════════════════════════╗    ║  │
│  ║  ║ Business Questions → Semantic Concepts:                  ║    ║  │
│  ║  ║ "What's our churn rate?" → Churn Rate measure             ║    ║  │
│  ║  ║ "Which regions have highest churn?" → Region hierarchy    ║    ║  │
│  ║  ║ "Who are high-value at-risk?" → Filter by Charges + Tenure║   ║  │
│  ║  ║ "Show me churned vs active" → Filter Churn Status         ║    ║  │
│  ║  ╚════════════════════════════════════════════════════════════╝    ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║  REVENUE GROWTH MODEL                                                ║  │
│  ║  ─────────────────────────────────────────────────────────────────  ║  │
│  ║  Tables:                                                            ║  │
│  ║  ├─ Products                                                         ║  │
│  ║  │  ├─ Columns: Name, Category, Price                               ║  │
│  ║  │  └─ Hierarchies: Category > Subcategory > Product                ║  │
│  ║  │                                                                  ║  │
│  ║  ├─ Sales                                                            ║  │
│  ║  │  ├─ Columns: Date, Quantity, Price, Region                      ║  │
│  ║  │  ├─ Measures: Total Sales, Profit Margin, Order Count           ║  │
│  ║  │  └─ Hierarchies: Region > Category > Product > Date             ║  │
│  ║  │                                                                  ║  │
│  ║  Relationships:                                                      ║  │
│  ║    Sales.product_id → Products.product_id (many-to-one)            ║  │
│  ║  ╔════════════════════════════════════════════════════════════╗    ║  │
│  ║  ║ Business Questions → Semantic Concepts:                  ║    ║  │
│  ║  ║ "Revenue by region?" → Sales × Region hierarchy           ║    ║  │
│  ║  ║ "Most profitable products?" → Sort by Profit Margin       ║    ║  │
│  ║  ║ "Sales trends over time?" → Time Analysis hierarchy       ║    ║  │
│  ║  ║ "Q1 vs Q2 performance?" → Slice by Order Date             ║    ║  │
│  ║  ╚════════════════════════════════════════════════════════════╝    ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║  SUPPLY CHAIN RISK MODEL                                             ║  │
│  ║  ─────────────────────────────────────────────────────────────────  ║  │
│  ║  Tables:                                                            ║  │
│  ║  ├─ Suppliers                                                        ║  │
│  ║  │  ├─ Columns: Name, Country, Reliability Score, Lead Time        ║  │
│  ║  │  └─ Measures: Avg Reliability, Avg Lead Time                    ║  │
│  ║  │                                                                  ║  │
│  ║  ├─ Inventory                                                        ║  │
│  ║  │  ├─ Columns: Location, Stock Level, Days of Supply, Risk Flags  ║  │
│  ║  │  ├─ Measures: Total Inventory, Avg Days Supply, Risk Count      ║  │
│  ║  │  └─ Hierarchies: Warehouse > Product > Risk Level               ║  │
│  ║  │                                                                  ║  │
│  ║  Relationships:                                                      ║  │
│  ║    Inventory.supplier_id → Suppliers.supplier_id (many-to-one)    ║  │
│  ║  ╔════════════════════════════════════════════════════════════╗    ║  │
│  ║  ║ Business Questions → Semantic Concepts:                  ║    ║  │
│  ║  ║ "Which items are at stockout risk?" → Stockout Risk Count ║    ║  │
│  ║  ║ "Which suppliers are unreliable?" → Reliability Score     ║    ║  │
│  ║  ║ "Where's inventory concentrated?" → Warehouse hierarchy   ║    ║  │
│  ║  ║ "Supply chain visibility?" → Days of Supply measure       ║    ║  │
│  ║  ╚════════════════════════════════════════════════════════════╝    ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                             │
│  Models are defined in:                                                     │
│    • semantic_model.py (classes & logic)                                   │
│    • semantic_model_examples.py (factory functions)                        │
│    • main.py (example_semantic_* functions)                                │
│                                                                             │
│  Models are exported as:                                                    │
│    • models/customer_churn_model.json                                       │
│    • models/revenue_growth_model.json                                       │
│    • models/supply_chain_model.json                                         │
│    • models/integrated_business_model.json                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 BUSINESS INTELLIGENCE LAYER                                 │
│              (Power BI, Excel, Analytics)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Consumers see:                                                             │
│  ✓ Intuitive business concepts (not technical details)                     │
│  ✓ Pre-calculated measures (Churn Rate, Profit Margin, etc.)              │
│  ✓ Clear hierarchies for drill-down analysis                              │
│  ✓ Relationships between tables for cross-dimensional analysis            │
│  ✓ Consistent formatting (%, $, units)                                    │
│  ✓ Hidden technical keys (customer_id, product_id)                        │
│                                                                             │
│  Examples:                                                                  │
│  • "Show churn rate by region and subscription type"                       │
│  • "Which product category had highest profit margin?"                     │
│  • "Alert: 47 items at risk of stockout"                                   │
│  • "Supplier reliability scorecard"                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          MAIN.PY                                         │
│              (Main entry point and orchestrator)                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Workspace & Connection Examples:                                       │
│  • example_basic_connection()                                           │
│  • example_context_manager()                                            │
│  • example_workspace_initialization()                                   │
│  • example_create_workspace_items()                                     │
│      ↓                                                                   │
│    Calls fabric_connection.py, workspace_init.py                        │
│                                                                          │
│  Data Ingestion Examples:                                               │
│  • example_csv_ingestion()                                              │
│  • example_sql_ingestion()                                              │
│  • example_batch_ingestion()                                            │
│  • example_ingestion_report()                                           │
│      ↓                                                                   │
│    Calls data_ingestion.py                                              │
│                                                                          │
│  Semantic Model Examples:                                               │
│  • example_semantic_customer_churn()                                    │
│  • example_semantic_revenue_growth()                                    │
│  • example_semantic_supply_chain()                                      │
│  • example_semantic_integrated()                                        │
│  • example_semantic_custom()                                            │
│  • example_semantic_extend()                                            │
│  • example_semantic_comparison()                                        │
│      ↓                                                                   │
│    Calls semantic_model.py, semantic_model_examples.py                  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Data Flow by Use Case

### Use Case 1: Daily Sales Data Import

```
1. CSV File (daily_sales.csv)
   ↓
2. Data Ingestion Pipeline
   └─ OneLakeDataSource.read_csv()
   └─ Validation & error handling
   ↓
3. Fabric Lakehouse
   └─ sales table (raw data)
   ↓
4. Semantic Model (Revenue Growth)
   └─ Maps to Sales measures
   └─ Connects to Products table
   ↓
5. Power BI Dashboard
   └─ "Revenue by Product > Region > Date"
   └─ Drill down to daily level
   └─ View Profit Margin, Order Count, etc.
```

### Use Case 2: Customer Churn Analysis

```
1. SQL Server (Customers, Events)
   ↓
2. Data Ingestion Pipeline
   └─ SQLDataSource.query() or bulk ingest
   └─ Data quality checks
   └─ Logging & reporting
   ↓
3. Fabric Lakehouse
   └─ customers table
   └─ events table (churn_date, is_churned)
   ↓
4. Semantic Model (Customer Churn)
   └─ Churn Rate measure = AVG(is_churned)
   └─ Hierarchies: Region > Subscription > Customer
   ↓
5. Analytics
   └─ "Which regions have highest churn?"
   └─ "Profile high-value churned customers"
   └─ "Alert on sudden churn spike"
```

### Use Case 3: Supply Chain Monitoring

```
1. Multiple Sources
   ├─ SQL: Supplier data, reliability scores
   ├─ CSV: Inventory snapshots
   └─ API: Real-time stock levels
   ↓
2. Batch Data Ingestion
   └─ Process all sources in sequence
   └─ Unified ingestion report
   └─ Error handling & retry logic
   ↓
3. Fabric Lakehouse
   ├─ suppliers table
   ├─ inventory table
   └─ relationships defined
   ↓
4. Semantic Model (Supply Chain Risk)
   ├─ Days of Supply metric
   ├─ Stockout Risk Count
   ├─ Supplier Reliability hierarchies
   └─ Cross-table analysis
   ↓
5. Decision Support
   └─ "Alert: 12 items at risk of stockout"
   └─ "Supplier performance scorecard"
   └─ "Inventory optimization recommendations"
```

## Technology Stack

```
┌──────────────────────────────────────────────────────────┐
│ Data Sources                                             │
│ • CSV (OneLake)  • SQL Server  • APIs  • Web Data       │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│ Python Libraries (requirements.txt)                      │
│ • fabric             - Microsoft Fabric SDK              │
│ • azure-identity     - Azure authentication              │
│ • pandas             - Data manipulation                 │
│ • pyodbc             - SQL Server connection             │
│ • sqlalchemy         - SQL toolkit                       │
│ • python-dotenv      - Environment variable management   │
│ • requests           - HTTP client                       │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│ Application Layer (Python Modules)                       │
├──────────────────────────────────────────────────────────┤
│ • config.py                  - Configuration mgmt         │
│ • fabric_connection.py       - Auth & connection          │
│ • workspace_init.py          - Workspace setup            │
│ • data_ingestion.py          - CSV/SQL ingestion         │
│ • semantic_model.py          - Semantic definitions       │
│ • semantic_model_examples.py - Model factories            │
│ • main.py                    - Orchestration              │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│ Microsoft Fabric                                         │
├──────────────────────────────────────────────────────────┤
│ • Fabric Workspace (OneLake)                             │
│ • Lakehouse (raw data tables)                            │
│ • Semantic Models (business layer)                       │
│ • Power BI Integration                                   │
└──────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│ Business Intelligence & Analytics                        │
│ • Power BI Dashboards                                    │
│ • Excel Analysis                                         │
│ • Business Insights                                      │
└──────────────────────────────────────────────────────────┘
```

## Key Design Principles

### 1. Layered Architecture
- **Data Layer:** Raw tables in Lakehouse
- **Semantic Layer:** Business concepts with measures
- **Presentation Layer:** BI tools and dashboards

### 2. Separation of Concerns
- Ingestion handles data quality and validation
- Semantic models define business logic
- BI tools focus on visualization

### 3. Error Handling & Logging
- Every operation is logged (INFO, WARNING, ERROR)
- Graceful error recovery
- Detailed ingestion reports

### 4. Scalability
- Batch processing for large datasets
- Relationship definitions for dimensional analysis
- Hierarchy support for drill-down exploration

### 5. Security
- Environment variables for credentials
- No hardcoded secrets
- Role-based access through Fabric

## Extensibility Points

### Add New Data Sources
```python
# In data_ingestion.py
class MyDataSource:
    def read(self):
        # Custom logic
        pass

# In pipeline
pipeline.add_source(MyDataSource())
```

### Add New Business Metrics
```python
# In semantic_model.py
table.add_measure(Measure(
    "my_metric",
    "My Metric",
    "My business metric",
    "column",
    AggregationFunction.CUSTOM
))
```

### Add New Analysis Dimensions
```python
# Add hierarchy
table.add_hierarchy(Hierarchy(
    "my_hierarchy",
    "My Analysis",
    levels=["level1", "level2", "level3"]
))
```

## Deployment Workflow

```
1. Development
   ├─ Update Python code
   ├─ Test locally with examples
   └─ Generate model JSON files

2. Configuration
   ├─ Update .env with Fabric credentials
   ├─ Verify data sources
   └─ Validate semantic models

3. Deployment
   ├─ Create/update Fabric workspace
   ├─ Ingest data to lakehouse
   ├─ Deploy semantic models
   └─ Grant permissions

4. Validation
   ├─ Check data quality
   ├─ Verify model relationships
   ├─ Test BI connections
   └─ Monitor ingestion logs

5. Monitoring
   ├─ Track ingestion success rate
   ├─ Monitor data freshness
   ├─ Alert on failures
   └─ Collect usage analytics
```

This architecture provides a complete, production-ready solution for enterprise data analytics in Microsoft Fabric.
