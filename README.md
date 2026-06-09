# Microsoft Fabric Workspace Setup

Complete boilerplate code for connecting to Microsoft Fabric workspace using Python SDK, with authentication setup and semantic modeling initialization.

⭐ **NEW? Start here:** [GETTING_STARTED.md](GETTING_STARTED.md) - Step-by-step setup guide

## Features

- ✅ Service Principal and User authentication methods
- ✅ Secure credential management with `.env` file support
- ✅ Fabric workspace connection and initialization
- ✅ Lakehouse creation
- ✅ Semantic model setup
- ✅ Report generation
- ✅ Context manager for automatic connection handling
- ✅ Comprehensive logging and error handling

## Project Structure

```
dataStoryTeller/
├── config.py                      # Configuration and environment variables
├── fabric_connection.py           # Authentication and connection management
├── workspace_init.py              # Workspace initialization and semantic modeling
├── data_ingestion.py              # Data ingestion pipeline (CSV, SQL sources)
├── semantic_model.py              # Semantic model definitions and builders
├── semantic_model_examples.py     # Semantic model examples and utilities
├── main.py                        # Main entry point and examples
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment configuration
├── batch_ingestion_config.json    # Example batch ingestion configuration
├── README.md                      # Main project documentation
├── QUICK_START.md                 # Quick start guide for data ingestion
├── DATA_INGESTION_GUIDE.md        # Comprehensive data ingestion documentation
├── SEMANTIC_MODEL_GUIDE.md        # Semantic model concepts and usage guide
├── SEMANTIC_MAPPING_EXAMPLES.md   # Real-world mapping examples
├── SEMANTIC_MODELS_QUICK_REF.md   # One-page reference for all models
├── ARCHITECTURE.md                # Complete system architecture
├── data/                          # Sample data files
│   └── sample_data.csv           # Example CSV for testing
└── models/                        # Generated semantic model JSON files
    ├── customer_churn_model.json
    ├── revenue_growth_model.json
    ├── supply_chain_model.json
    └── integrated_business_model.json
```

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `fabric` - Microsoft Fabric SDK
- `azure-identity` - Azure authentication
- `python-dotenv` - Environment variable management
- `requests` - HTTP library
- `pandas` - Data manipulation and analysis
- `pyodbc` - SQL Server connection
- `sqlalchemy` - SQL toolkit and ORM

### 2. Configure Authentication

Create a `.env` file in the project root directory based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and fill in your Azure/Fabric credentials:

```env
# Service Principal Authentication
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# Workspace Configuration
FABRIC_WORKSPACE_NAME=MyFabricWorkspace
FABRIC_WORKSPACE_ID=your_workspace_id
```

### 3. Configure Data Sources (Optional)

For SQL data ingestion, you can add SQL connection details:

```env
# SQL Server Configuration (optional)
SQL_SERVER=your-sql-server.database.windows.net
SQL_DATABASE=SalesDB
SQL_USERNAME=admin@company
SQL_PASSWORD=SecurePassword123
```

Note: For security, never commit credentials to source control. Use `.env` files and `.gitignore`.

## Usage

### Basic Connection

```python
from fabric_connection import FabricConnection

# Create connection
connection = FabricConnection(auth_method="service_principal")

# Connect to workspace
if connection.connect():
    client = connection.get_client()
    # Use client for API calls
    connection.close()
```

### Using Context Manager (Recommended)

```python
from fabric_connection import FabricSessionManager

# Automatic connection and disconnection
with FabricSessionManager() as connection:
    client = connection.get_client()
    # Connection is automatically closed after this block
```

### Initialize Workspace

```python
from fabric_connection import FabricSessionManager
from workspace_init import FabricWorkspaceInit

with FabricSessionManager() as connection:
    workspace_init = FabricWorkspaceInit(connection)
    
    # Initialize workspace
    workspace_init.initialize_workspace("MyWorkspace", "workspace-id")
    
    # Prepare for semantic modeling
    setup_result = workspace_init.prepare_for_semantic_modeling()
```

### Create Workspace Items

```python
# Create a Lakehouse
lakehouse = workspace_init.create_lakehouse(
    "sales_lakehouse",
    "Central data lake for sales"
)

# Create a Semantic Model
model = workspace_init.create_semantic_model(
    "sales_model",
    "sales_dataset",
    "Semantic model for sales"
)

# Create a Report
report = workspace_init.create_report(
    "sales_report",
    model["modelId"],
    "Sales performance report"
)
```

### Complete Setup

```python
from workspace_init import setup_fabric_workspace

result = setup_fabric_workspace(
    workspace_name="MyWorkspace",
    workspace_id="workspace-id",
    auth_method="service_principal"
)

if result:
    print(f"Setup status: {result['status']}")
    print(f"Components: {result['components']}")
```

## Running Examples

Run the main script to execute example workflows:

```bash
python main.py
```

Uncomment specific examples in `main.py` to run them:

**Workspace & Connection:**
- `example_basic_connection()` - Basic connection demonstration
- `example_context_manager()` - Context manager usage
- `example_workspace_initialization()` - Workspace setup
- `example_create_workspace_items()` - Item creation

**Data Ingestion:**
- `example_csv_ingestion()` - CSV data ingestion
- `example_sql_ingestion()` - SQL table and query ingestion
- `example_batch_ingestion()` - Batch processing of multiple sources
- `example_ingestion_report()` - Generate ingestion reports

**Semantic Models:**
- `example_semantic_customer_churn()` - Customer churn model
- `example_semantic_revenue_growth()` - Revenue growth model
- `example_semantic_supply_chain()` - Supply chain risk model
- `example_semantic_integrated()` - Integrated business model
- `example_semantic_custom()` - Create custom model
- `example_semantic_extend()` - Extend existing model
- `example_semantic_comparison()` - Compare models

## Authentication Methods

### Service Principal (Recommended for Production)

1. Create Azure AD Service Principal
2. Grant it access to Fabric workspace
3. Set credentials in `.env`:
   ```env
   AUTH_METHOD=service_principal
   AZURE_TENANT_ID=your_tenant_id
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   ```

### User Authentication

Set credentials in `.env`:
```env
AUTH_METHOD=user
FABRIC_USERNAME=your_email@company.com
FABRIC_PASSWORD=your_password
```

## Module Reference

### `config.py`

Configuration management with environment variable loading.

- `FabricConfig.validate()` - Validate required settings

### `fabric_connection.py`

Authentication and connection management.

- `FabricConnection` - Main connection class
- `FabricSessionManager` - Context manager for connections

**Key Methods:**
- `connect()` - Establish connection
- `authenticate_service_principal()` - Service Principal auth
- `authenticate_user()` - User auth
- `get_client()` - Get Fabric client
- `is_connected()` - Check connection status

### `workspace_init.py`

Workspace initialization and semantic modeling setup.

- `FabricWorkspaceInit` - Workspace manager class
- `setup_fabric_workspace()` - Complete setup function

**Key Methods:**
- `initialize_workspace()` - Initialize workspace
- `create_lakehouse()` - Create lakehouse
- `create_semantic_model()` - Create semantic model
- `create_report()` - Create report
- `prepare_for_semantic_modeling()` - Full setup

### `data_ingestion.py`

Comprehensive data ingestion pipeline for CSV and SQL sources.

- `OneLakeDataSource` - Read/write OneLake data
- `SQLDataSource` - SQL Server connections and queries
- `DataIngestionPipeline` - Main orchestration engine

**Key Methods:**
- `ingest_csv()` - Ingest CSV files
- `ingest_sql_query()` - Execute SQL queries
- `ingest_sql_table()` - Ingest complete SQL tables
- `ingest_batch()` - Process multiple sources
- `get_ingestion_report()` - Generate ingestion reports

### `semantic_model.py`

Semantic model definitions for mapping raw data to business concepts.

- `SemanticModel` - Main model container
- `SemanticTable` - Individual tables with columns and measures
- `Column` - Data attributes with business names
- `Measure` - Calculated metrics (Count, Sum, Average, etc.)
- `Hierarchy` - Drill-down paths for analysis
- `Relationship` - Table connections and cardinality

**Factory Functions:**
- `create_customer_churn_model()` - Pre-built churn model
- `create_revenue_growth_model()` - Pre-built revenue model
- `create_supply_chain_risk_model()` - Pre-built supply chain model
- `create_integrated_business_model()` - Combined model

**Key Methods:**
- `add_table()` - Add semantic table
- `add_relationship()` - Connect tables
- `validate()` - Check model integrity
- `save_to_file()` - Export to JSON
- `to_json()` - Serialize model

### `semantic_model_examples.py`

Examples and utilities for working with semantic models.

- `example_customer_churn_model()` - Churn model demonstration
- `example_revenue_growth_model()` - Revenue model demonstration
- `example_supply_chain_model()` - Supply chain model demonstration
- `example_integrated_model()` - Integrated model demonstration
- `example_create_custom_model()` - Create marketing model
- `example_extend_model()` - Add measures to existing model
- `print_model_statistics()` - Display model details

The module supports comprehensive data ingestion with error handling and logging.

### CSV Ingestion

```python
from fabric_connection import FabricSessionManager
from data_ingestion import create_ingestion_pipeline

with FabricSessionManager() as connection:
    pipeline = create_ingestion_pipeline(
        connection=connection,
        workspace_id="workspace-001",
        workspace_name="MyWorkspace",
        lakehouse_name="data_lakehouse"
    )
    
    result = pipeline.ingest_csv(
        file_path="data/sales.csv",
        table_name="sales_data",
        encoding="utf-8",
        mode="overwrite"
    )
```

### SQL Ingestion

```python
from data_ingestion import create_sql_source

sql_source = create_sql_source(
    server="localhost",
    database="SalesDB",
    username="sa",
    password="password"
)

# Ingest entire table
result = pipeline.ingest_sql_table(
    table_name="Customers",
    sql_source=sql_source
)

# Or execute custom query
result = pipeline.ingest_sql_query(
    sql_query="SELECT * FROM dbo.Orders WHERE OrderDate > '2024-01-01'",
    table_name="recent_orders",
    sql_source=sql_source
)
```

### Batch Ingestion

Process multiple data sources efficiently:

```python
batch_config = [
    {"type": "CSV", "source": "data/customers.csv", "table_name": "customers"},
    {"type": "CSV", "source": "data/products.csv", "table_name": "products"},
    {"type": "SQL_TABLE", "source": "Orders", "table_name": "orders"},
    {"type": "SQL", "source": "SELECT * FROM dbo.Payments WHERE Status='Completed'", "table_name": "payments"}
]

results = pipeline.ingest_batch(batch_config, sql_source=sql_source)
```

### Generate Ingestion Reports

```python
report = pipeline.get_ingestion_report(save_path="ingestion_report.json")

print(f"Success Rate: {report['summary']['success_rate']}")
print(f"Total Records: {report['summary']['total_records_ingested']}")
```

See [DATA_INGESTION_GUIDE.md](DATA_INGESTION_GUIDE.md) for complete documentation.

## Semantic Modeling

The semantic model layer transforms raw data into business concepts, enabling intuitive analysis without SQL knowledge.

### Pre-built Models

Three semantic models map raw columns to business concepts:

1. **Customer Churn Model** - Identify at-risk customers
   - Raw columns: customer_id, tenure_months, monthly_charges, is_churned
   - Business concepts: Churn Rate, Average Tenure, Customer Value
   - Hierarchies: Region > Subscription > Customer

2. **Revenue Growth Model** - Track sales performance
   - Raw columns: sales_id, product_id, sales_amount, cost_amount, profit_amount
   - Business concepts: Total Revenue, Profit Margin, Average Order Value
   - Hierarchies: Region > Category > Product > Date

3. **Supply Chain Risk Model** - Monitor inventory and suppliers
   - Raw columns: current_stock_level, days_of_supply, stockout_risk
   - Business concepts: Days of Supply, Stockout Risk, Supplier Reliability
   - Hierarchies: Warehouse > Product > Risk Level

### Using Semantic Models

```python
from semantic_model import (
    create_customer_churn_model,
    create_revenue_growth_model,
    create_supply_chain_risk_model
)

# Load pre-built model
model = create_customer_churn_model()

# Add custom measures
customers = model.get_table("customers")
customers.add_measure(Measure(
    "high_value_at_risk",
    "High Value At-Risk",
    "Customers with charges > $100 and tenure < 12 months",
    "customer_id",
    AggregationFunction.COUNT
))

# Validate and save
validation = model.validate()
model.save_to_file("models/churn_model_custom.json")
```

### Extending Models

```python
from semantic_model import SemanticModel, SemanticTable, Column, Measure, DataType

# Create custom model
model = SemanticModel("custom", "Custom Model")

# Add tables, columns, measures
table = SemanticTable("my_table", "My Table")
table.add_column(Column("value", "Value", DataType.DECIMAL))
table.add_measure(Measure("total", "Total", "Sum of values", "value", AggregationFunction.SUM))

# Deploy to Fabric
model.add_table(table)
model.save_to_file("models/custom_model.json")
```

See [SEMANTIC_MODEL_GUIDE.md](SEMANTIC_MODEL_GUIDE.md) and [SEMANTIC_MAPPING_EXAMPLES.md](SEMANTIC_MAPPING_EXAMPLES.md) for complete documentation.

**Quick Reference:** [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md) - One-page reference for all three models

## Power BI Integration

Generate Power BI dashboards from semantic models with KPIs, bar charts, line graphs, and more.

- **Module:** `power_bi_integration.py` - Dashboard builder, DAX generator, data exporter, REST API client
- **Examples:** `power_bi_examples.py` - 7 example dashboards for all models
- **Guide:** [POWER_BI_GUIDE.md](POWER_BI_GUIDE.md) - Complete Power BI integration documentation

**Quick Start:**
```python
from power_bi_integration import PowerBIDashboardBuilder
from semantic_model import create_customer_churn_model

model = create_customer_churn_model()
builder = PowerBIDashboardBuilder(model)
dashboard = builder.create_dashboard("churn", "Churn Analysis", "Monitor retention")

# Add visualizations
builder.add_kpi_card("churn_rate", "Churn Rate (%)")
builder.add_bar_chart("region", "churn_rate", "Churn by Region", "customers")
builder.add_line_chart("churn_date", "churn_rate", "Churn Trend")

# Save for Power BI
dashboard.save_to_file("dashboards/churn_dashboard.json")
```

**Dashboard Types Supported:**
- ✅ KPI Cards - Highlight key metrics
- ✅ Bar Charts - Compare categories
- ✅ Line Charts - Show trends over time
- ✅ Pie Charts - Show distribution
- ✅ Gauges - Metric against target
- ✅ Tables - Detailed data
- ✅ Matrices - Cross-tabulation

**Pre-built Dashboards:**
1. Customer Churn - Churn rate, regional analysis, at-risk customers
2. Revenue Growth - Sales, profit margin, trends by category
3. Supply Chain Risk - Days of supply, stockout alerts, supplier reliability
4. Executive Summary - All KPIs, key trends, business health

See [POWER_BI_GUIDE.md](POWER_BI_GUIDE.md) for complete documentation, usage examples, and integration steps.

## System Architecture

The system follows a layered architecture with three main components:

1. **Data Layer** - Raw ingestion from CSV/SQL to Lakehouse
2. **Semantic Layer** - Business concepts and metrics
3. **Presentation Layer** - BI tools and dashboards

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete architecture overview with data flows and component interactions.

## Error Handling

All modules include comprehensive error handling and logging:

```python
import logging

# Logs are output with timestamp and level
logger = logging.getLogger(__name__)

# Set log level in .env:
LOG_LEVEL=DEBUG  # For detailed debugging
```

### Data Ingestion Error Handling

The data ingestion pipeline includes specialized error handling:

```python
from data_ingestion import DataIngestionError

try:
    result = pipeline.ingest_csv("data/sales.csv", "sales_table")
except DataIngestionError as e:
    logger.error(f"Ingestion error: {str(e)}")
    # Handle gracefully - log and continue
except FileNotFoundError:
    logger.error("CSV file not found")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
```

**Errors Handled:**
- File not found or inaccessible
- Invalid CSV format or encoding
- SQL connection failures
- Empty or null DataFrames
- Data type mismatches
- High data quality issues (warnings)

### Logging in Ingestion Pipeline

```
2024-06-09 10:15:23 - data_ingestion - INFO - Starting CSV ingestion: data/sales.csv -> sales
2024-06-09 10:15:24 - data_ingestion - INFO - ✓ Successfully read CSV: data/sales.csv
2024-06-09 10:15:24 - data_ingestion - INFO -   Shape: (1000, 5) | Columns: ['date', 'product', 'quantity', 'amount', 'region']
2024-06-09 10:15:24 - data_ingestion - INFO - Data Quality - Max null %: 2.5%
2024-06-09 10:15:25 - data_ingestion - INFO - ✓ Successfully uploaded 1000 records to sales
```

## Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`:
   ```
   .env
   *.pyc
   __pycache__/
   ```

2. **Use Service Principal for production** - More secure than storing passwords

3. **Rotate credentials regularly** - Update Azure AD credentials periodically

4. **Limit permissions** - Give Service Principal only necessary Fabric workspace access

5. **Use environment variables** - Never hardcode credentials

## Troubleshooting

### "Missing required configuration" Error

Ensure `.env` file is created and contains required fields:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Authentication Failed

1. Verify tenant ID, client ID, and secret are correct
2. Ensure Service Principal has access to Fabric workspace
3. Check if credentials are expired
4. Verify network connectivity to Azure endpoints

### Connection Timeout

1. Check internet connection
2. Verify Fabric API URL is accessible
3. Check firewall rules
4. Try with `LOG_LEVEL=DEBUG` for more details

## Next Steps

1. **Implement data ingestion** - Load data into lakehouse
2. **Create data models** - Define dimensions and measures
3. **Build reports** - Create Power BI reports on semantic models
4. **Set up refresh** - Configure automatic data refresh schedules
5. **Add security** - Implement row-level security (RLS)

## Resources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/en-us/fabric/)
- [Python SDK for Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-python-api)
- [Azure Identity Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)
- [Power BI Embeddings API](https://learn.microsoft.com/en-us/rest/api/power-bi/)

## License

This boilerplate code is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs with `LOG_LEVEL=DEBUG`
3. Consult Microsoft Fabric documentation
4. Contact Microsoft support for account-specific issues