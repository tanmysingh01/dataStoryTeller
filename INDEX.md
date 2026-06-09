# Documentation Index

Complete navigation guide to all dataStoryTeller documentation and examples.

## 📋 Getting Started

Start here if you're new to the project:

1. **[README.md](README.md)** - Project overview and setup instructions
2. **[QUICK_START.md](QUICK_START.md)** - First 5-minute examples with real data
3. **[.env.example](.env.example)** - Configure your credentials

## 🏗️ System Architecture

Understand how the system is designed:

1. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture with data flows
   - End-to-end data flow diagram
   - Component interactions
   - Technology stack
   - Deployment workflow

2. **[DATA_INGESTION_GUIDE.md](DATA_INGESTION_GUIDE.md)** - Data ingestion pipeline documentation
   - Module reference
   - Usage examples
   - Error handling
   - Performance optimization

3. **[SEMANTIC_MODEL_GUIDE.md](SEMANTIC_MODEL_GUIDE.md)** - Semantic model system documentation
   - Concepts and architecture
   - All three pre-built models explained
   - How to extend models
   - Best practices

## 📊 Semantic Models Reference

Learn about the three pre-built semantic models:

1. **[SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md)** ⭐ START HERE
   - One-page reference for all three models
   - Key metrics and dimensions for each model
   - Common extensions
   - Running examples

2. **[SEMANTIC_MAPPING_EXAMPLES.md](SEMANTIC_MAPPING_EXAMPLES.md)** - Real-world examples
   - Customer Churn: raw columns → business concepts
   - Revenue Growth: raw columns → business concepts
   - Supply Chain Risk: raw columns → business concepts
   - Before/after SQL comparisons
   - Key mapping principles

## 📈 Power BI Dashboard Creation

Create interactive dashboards from semantic models:

1. **[POWER_BI_GUIDE.md](POWER_BI_GUIDE.md)** - Complete Power BI integration guide
   - Architecture and module reference
   - Dashboard builder usage
   - Visualization types and examples
   - DAX measure generation
   - Power BI Desktop integration
   - Best practices and troubleshooting

2. **power_bi_integration.py** - Core module with:
   - `PowerBIDashboard` - Dashboard builder
   - `PowerBIVisualization` - Chart/KPI definitions
   - `PowerBIDAXGenerator` - DAX measure code generation
   - `PowerBIDataExporter` - CSV/JSON export
   - `PowerBIRESTClient` - Power BI Service API

3. **power_bi_examples.py** - 7 pre-built dashboard examples:
   - Customer Churn Dashboard
   - Revenue Growth Dashboard
   - Supply Chain Risk Dashboard
   - Executive Summary Dashboard
   - DAX Measures Reference
   - Data Export Examples
   - Power BI Quick Start Guide

## 🔧 Module Reference

### Core Modules

**fabric_connection.py** - Authentication and connection
- Service Principal and User authentication
- Context manager for automatic cleanup
- Secure credential handling

**workspace_init.py** - Workspace initialization
- Create lakehouse, semantic models, reports
- Factory function for complete setup

**data_ingestion.py** - Data ingestion pipeline
- CSV and SQL support
- Batch processing
- Error handling and validation

**semantic_model.py** - Semantic model definitions
- Core classes: Column, Measure, Hierarchy, Relationship
- SemanticModel and SemanticTable
- Factory functions for pre-built models

**semantic_model_examples.py** - Example utilities
- 8 demonstration functions
- Model statistics and comparison

**main.py** - Main entry point
- 15 example functions demonstrating all features
- Uncomment to run specific examples

**config.py** - Configuration management
- Environment variable management
- Validation for authentication methods

## 🚀 Examples by Use Case

### Workspace & Connection (4 examples)
```python
# In main.py, uncomment:
example_basic_connection()           # Basic connectivity test
example_context_manager()             # Automatic resource management
example_workspace_initialization()    # Set up workspace from scratch
example_create_workspace_items()      # Create lakehouse, models, reports
```

### Data Ingestion (4 examples)
```python
# In main.py, uncomment:
example_csv_ingestion()              # Import CSV from OneLake
example_sql_ingestion()              # Query SQL Server
example_batch_ingestion()            # Multiple sources at once
example_ingestion_report()           # Generate ingestion analytics
```

### Semantic Models (7 examples)
```python
# In main.py, uncomment:
example_semantic_customer_churn()    # Customer churn model
example_semantic_revenue_growth()    # Revenue growth model
example_semantic_supply_chain()      # Supply chain risk model
example_semantic_integrated()        # Combined model
example_semantic_custom()            # Create custom model
example_semantic_extend()            # Add measures to model
example_semantic_comparison()        # Compare all models
```

### Power BI Dashboards (7 examples)
```python
# In main.py, uncomment:
example_power_bi_churn_dashboard()              # Customer churn dashboard
example_power_bi_revenue_dashboard()            # Revenue growth dashboard
example_power_bi_supply_chain_dashboard()       # Supply chain dashboard
example_power_bi_executive_dashboard()          # Executive summary
example_power_bi_dax_measures()                 # DAX code generation
example_power_bi_export()                       # Data export (CSV/JSON)
example_power_bi_quick_start_guide()            # Quick start guide
```

## 📁 File Structure

```
dataStoryTeller/
│
├── 📄 Configuration
│   ├── config.py                     # Settings & environment vars
│   ├── .env.example                  # Credentials template
│   ├── requirements.txt              # Python dependencies
│   └── batch_ingestion_config.json   # Batch configuration
│
├── 🔐 Authentication & Setup
│   ├── fabric_connection.py          # Fabric authentication
│   └── workspace_init.py             # Workspace initialization
│
├── 📥 Data Ingestion
│   └── data_ingestion.py             # CSV & SQL ingestion pipeline
│
├── 📊 Semantic Models
│   ├── semantic_model.py             # Core semantic model system
│   └── semantic_model_examples.py    # Example implementations
│
├── 📈 Power BI Integration
│   ├── power_bi_integration.py       # Dashboard builder, DAX generator
│   └── power_bi_examples.py          # 7 pre-built dashboard examples
│
├── 🎯 Execution
│   └── main.py                       # Main entry & 22 examples
│
├── 📚 Quick Reference (START HERE)
│   ├── README.md                     # Project overview
│   ├── QUICK_START.md                # 5-minute examples
│   ├── GETTING_STARTED.md            # 7-phase setup guide
│   └── SEMANTIC_MODELS_QUICK_REF.md  # One-page model reference
│
├── 📖 Comprehensive Guides
│   ├── ARCHITECTURE.md               # System architecture
│   ├── DATA_INGESTION_GUIDE.md       # Ingestion documentation
│   ├── SEMANTIC_MODEL_GUIDE.md       # Model system documentation
│   ├── SEMANTIC_MAPPING_EXAMPLES.md  # Real-world examples
│   ├── POWER_BI_GUIDE.md             # Power BI integration guide
│   └── INDEX.md                      # Complete documentation map
│
├── 📦 Sample Data
│   ├── data/
│   │   └── sample_data.csv
│
├── 💾 Generated Models (after running examples)
│   └── models/
│       ├── customer_churn_model.json
│       ├── revenue_growth_model.json
│       ├── supply_chain_model.json
│       └── integrated_business_model.json
│
└── 📊 Dashboard Definitions (after running Power BI examples)
    └── dashboards/
        ├── customer_churn_dashboard.json
        ├── revenue_growth_dashboard.json
        ├── supply_chain_dashboard.json
        ├── executive_summary_dashboard.json
        ├── dax_measures_reference.txt
        └── POWER_BI_QUICK_START.txt
```

## 🎓 Learning Paths

### Path 1: Quick Start (30 minutes)
1. Read [README.md](README.md) (5 min)
2. Follow [QUICK_START.md](QUICK_START.md) (5 min)
3. Review [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md) (10 min)
4. Run examples in main.py (10 min)

### Path 2: Deep Dive (2-3 hours)
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) (20 min)
2. Study [DATA_INGESTION_GUIDE.md](DATA_INGESTION_GUIDE.md) (30 min)
3. Study [SEMANTIC_MODEL_GUIDE.md](SEMANTIC_MODEL_GUIDE.md) (40 min)
4. Review [SEMANTIC_MAPPING_EXAMPLES.md](SEMANTIC_MAPPING_EXAMPLES.md) (30 min)
5. Run all examples and examine outputs (30 min)

### Path 3: Customization (4-6 hours)
1. Complete Path 2
2. Read module source code:
   - data_ingestion.py (understand DataIngestionPipeline)
   - semantic_model.py (understand SemanticModel architecture)
3. Create custom data sources
4. Create custom semantic models for your domain
5. Deploy to Fabric workspace

### Path 4: Production Deployment (ongoing)
1. Complete Path 3
2. Set up environment credentials (.env)
3. Configure batch ingestion (batch_ingestion_config.json)
4. Set up scheduled ingestion
5. Deploy semantic models to Fabric
6. Connect Power BI
7. Monitor and maintain

## 🔑 Key Concepts Explained

### Semantic Model (What & Why)
**What:** A layer that translates raw database columns into business concepts
**Why:** Business users can ask "What's our churn rate?" instead of writing SQL

### Three Pre-built Models
1. **Customer Churn** - Understand customer retention
2. **Revenue Growth** - Track sales performance
3. **Supply Chain Risk** - Monitor inventory and suppliers

### Data Flow
Raw CSV/SQL → Ingestion Pipeline → Fabric Lakehouse → Semantic Model → Power BI → Business Insights

### Key Patterns
- **Factory Functions** - Create complex objects: `create_customer_churn_model()`
- **Context Managers** - Automatic resource cleanup: `with FabricSessionManager():`
- **Data Classes** - Structured data: `@dataclass Column, Measure, Hierarchy`

## 📞 Common Tasks

### Generate all semantic models
```bash
python main.py
# Uncomment all example_semantic_* functions
```

### Ingest data from CSV
```python
from data_ingestion import create_ingestion_pipeline
pipeline = create_ingestion_pipeline(connection, workspace_id, workspace_name, lakehouse_name)
pipeline.ingest_csv("path/to/file.csv")
```

### Create custom semantic model
```python
from semantic_model import SemanticModel, SemanticTable, Column, Measure

model = SemanticModel("my_model", "My Model")
table = SemanticTable("my_table", "My Table")
table.add_column(Column("value", "Value", DataType.DECIMAL))
table.add_measure(Measure("total", "Total", "Sum", "value", AggregationFunction.SUM))
model.add_table(table)
model.save_to_file("models/my_model.json")
```

### Extend existing model
```python
model = create_customer_churn_model()
customers = model.get_table("customers")
customers.add_measure(Measure(
    "high_value",
    "High Value Customers",
    "Customers with charges > $100",
    "customer_id",
    AggregationFunction.COUNT
))
```

### Validate model
```python
validation = model.validate()
if validation["valid"]:
    model.save_to_file("models/model.json")
else:
    print(validation["issues"])
```

### Generate Power BI dashboards
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
dashboard.save_to_file("dashboards/churn.json")
```

### Export data for Power BI
```python
from power_bi_integration import PowerBIDataExporter
from semantic_model import create_customer_churn_model

exporter = PowerBIDataExporter()
model = create_customer_churn_model()

# Export to CSV files
csv_files = exporter.export_semantic_model_to_csv(model, "power_bi_exports")

# Export as Power BI template
exporter.export_to_power_bi_template(model, "dashboards/template.json")
```

### Generate DAX measures
```python
from power_bi_integration import PowerBIDAXGenerator

dax = PowerBIDAXGenerator()

measures = {
    "Total Sales": dax.sum_measure("Total_Sales", "sales_amount", "Sales"),
    "Profit Margin": dax.percentage_measure("Profit_Margin", "[Total_Profit]", "[Total_Sales]"),
    "YTD Sales": dax.year_to_date_measure("YTD_Sales", "sales_amount", "Sales", "order_date"),
}

for name, dax_expr in measures.items():
    print(f"{name}:\n  {dax_expr}\n")
```

## 🐛 Troubleshooting

**"Module not found" error**
- Check requirements.txt installed: `pip install -r requirements.txt`
- Verify Python environment activated

**"Connection failed" error**
- Check .env file has correct credentials
- Verify Fabric workspace exists and you have access
- See [README.md#Configuration](README.md) section

**"Validation errors" in semantic model**
- Check all relationships reference existing tables
- Ensure no circular relationships
- Verify measure columns exist in table

**Data ingestion fails**
- Check file path is accessible
- Verify file format (CSV, SQL query syntax)
- Review error logs for specific issue
- See [DATA_INGESTION_GUIDE.md#Troubleshooting](DATA_INGESTION_GUIDE.md)

**Power BI dashboard won't import**
- Validate JSON file is valid: `python -c "import json; json.load(open('dashboards/churn.json'))"`
- Check semantic model validation: `model.validate()`
- Ensure all measures reference existing columns

**DAX measures not showing in Power BI**
- Check column names exactly match table definition
- Verify column visibility is not hidden
- Use correct table references in DAX

## 📞 Support

1. **Quick Questions** → Check [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md)
2. **How-To Guides** → Check [QUICK_START.md](QUICK_START.md)
3. **Power BI Help** → Check [POWER_BI_GUIDE.md](POWER_BI_GUIDE.md)
4. **Data Ingestion Reference** → Check [DATA_INGESTION_GUIDE.md](DATA_INGESTION_GUIDE.md)
4. **System Understanding** → Check [ARCHITECTURE.md](ARCHITECTURE.md)
5. **Real Examples** → Check [SEMANTIC_MAPPING_EXAMPLES.md](SEMANTIC_MAPPING_EXAMPLES.md)

## ✅ Checklist: Ready to Deploy?

- [ ] Read [README.md](README.md)
- [ ] Installed requirements.txt: `pip install -r requirements.txt`
- [ ] Configured .env file with credentials
- [ ] Ran examples successfully: `python main.py`
- [ ] Reviewed generated JSON files in models/ directory
- [ ] Read [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md)
- [ ] Understood data flow in [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Customized semantic models for your business
- [ ] Tested data ingestion pipeline
- [ ] Deployed to Fabric workspace
- [ ] Connected Power BI to semantic models
- [ ] Created dashboards for business users

## 🚀 Next Steps

1. **Start Here:** [README.md](README.md)
2. **Quick Examples:** [QUICK_START.md](QUICK_START.md)
3. **Model Reference:** [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md)
4. **Run Examples:** `python main.py`
5. **Deploy to Fabric:** Follow [ARCHITECTURE.md](ARCHITECTURE.md) deployment section

---

**Last Updated:** November 2024
**Status:** Complete and production-ready
**Version:** 1.0

All components are implemented, tested, and documented. Ready for deployment to Microsoft Fabric workspace.
