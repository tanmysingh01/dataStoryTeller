# Getting Started: Step-by-Step Setup

Your complete guide to set up and deploy dataStoryTeller to Microsoft Fabric.

## Phase 1: Local Setup (15 minutes)

### Step 1: Verify Python Installation
```bash
python --version
# Should be Python 3.8+
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output shows successful installation of:
- fabric
- azure-identity
- pandas
- pyodbc
- sqlalchemy
- requests
- python-dotenv

### Step 3: Configure Environment Variables
```bash
# Copy template
copy .env.example .env

# Edit .env with your values
# Open in VS Code or text editor and fill in:
TENANT_ID=your_azure_tenant_id
CLIENT_ID=your_app_registration_client_id
CLIENT_SECRET=your_app_secret
WORKSPACE_NAME=my_fabric_workspace
WORKSPACE_ID=your_workspace_id
```

**Don't have these values?** See [README.md - Configuration](README.md#configuration) for setup instructions.

### Step 4: Run First Example
```bash
# Open main.py
# Uncomment the first example:
# example_basic_connection()

python main.py
```

If you see no errors, you're connected! ✅

---

## Phase 2: Understand the System (20 minutes)

### Read These in Order:
1. **[ARCHITECTURE.md](ARCHITECTURE.md)** - See data flow and components
2. **[SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md)** - Understand the three models
3. **[INDEX.md](INDEX.md)** - Navigate all documentation

### Key Insights:
- Raw data (CSV, SQL) → Ingestion pipeline → Lakehouse → Semantic model → Power BI
- Three pre-built models: Customer Churn, Revenue Growth, Supply Chain Risk
- Each model maps technical columns to business concepts

---

## Phase 3: Run All Examples (20 minutes)

### Step 1: Generate Semantic Models
```python
# In main.py, uncomment these:
example_semantic_customer_churn()
example_semantic_revenue_growth()
example_semantic_supply_chain()
example_semantic_integrated()

python main.py
```

This creates JSON files in `models/` directory.

### Step 2: Verify Generated Files
```bash
# Check models directory was created
dir models/
# Should contain:
# - customer_churn_model.json
# - revenue_growth_model.json
# - supply_chain_model.json
# - integrated_business_model.json
```

### Step 3: Review Generated Models
```bash
# Open any JSON file to see model structure
# Look for:
# - tables (array)
# - columns (with descriptions)
# - measures (with aggregations)
# - hierarchies (drill-down paths)
# - relationships (connections)
```

---

## Phase 4: Customize for Your Business (30 minutes)

### Scenario: Create Marketing Model
```python
from semantic_model import (
    SemanticModel, SemanticTable, Column, Measure,
    Hierarchy, DataType, AggregationFunction
)

# Create model
model = SemanticModel("marketing", "Marketing Campaigns")

# Create table
campaigns = SemanticTable("campaigns", "Campaigns")

# Add columns
campaigns.add_column(Column("campaign_id", "Campaign ID", DataType.STRING))
campaigns.add_column(Column("campaign_name", "Campaign Name", DataType.STRING))
campaigns.add_column(Column("channel", "Channel", DataType.STRING, "Email, Social, Paid"))
campaigns.add_column(Column("spend", "Spend", DataType.DECIMAL, "Campaign cost"))
campaigns.add_column(Column("revenue", "Revenue", DataType.DECIMAL, "Generated revenue"))
campaigns.add_column(Column("leads", "Leads", DataType.INT, "Leads generated"))
campaigns.add_column(Column("conversions", "Conversions", DataType.INT, "Sales made"))

# Add measures
campaigns.add_measure(Measure(
    "total_spend",
    "Total Spend",
    "Total campaign investment",
    "spend",
    AggregationFunction.SUM,
    format_string="$#,##0.00"
))

campaigns.add_measure(Measure(
    "total_revenue",
    "Total Revenue",
    "Revenue generated",
    "revenue",
    AggregationFunction.SUM,
    format_string="$#,##0.00"
))

campaigns.add_measure(Measure(
    "roi",
    "ROI %",
    "Return on investment",
    "revenue",
    AggregationFunction.AVG,
    format_string="0.0%"
))

campaigns.add_measure(Measure(
    "conversion_rate",
    "Conversion Rate",
    "% of leads that convert",
    "conversions",
    AggregationFunction.AVG,
    format_string="0.0%"
))

campaigns.add_measure(Measure(
    "cost_per_lead",
    "Cost Per Lead",
    "Average spend per lead",
    "leads",
    AggregationFunction.AVG,
    format_string="$#,##0.00"
))

# Add hierarchy
campaigns.add_hierarchy(Hierarchy(
    "channel_analysis",
    "Channel Analysis",
    levels=["channel", "campaign_name"]
))

# Add to model
model.add_table(campaigns)

# Validate
validation = model.validate()
print(f"Valid: {validation['valid']}")
print(f"Tables: {validation['table_count']}")

# Save
model.save_to_file("models/marketing_model.json")
print("✅ Marketing model created!")
```

**Result:** `models/marketing_model.json` ready for Fabric

---

## Phase 5: Ingest Data (20 minutes)

### Scenario: Import Sales CSV

**Prerequisite:** Have a CSV file ready (or use data/sample_data.csv)

```python
from fabric_connection import FabricConnection, FabricSessionManager
from data_ingestion import create_ingestion_pipeline

# Connect to Fabric
with FabricSessionManager(connection_class=FabricConnection) as session:
    connection = session.connection
    
    # Create pipeline
    pipeline = create_ingestion_pipeline(
        connection=connection,
        workspace_id="your_workspace_id",
        workspace_name="my_fabric_workspace",
        lakehouse_name="my_lakehouse"
    )
    
    # Ingest CSV
    result = pipeline.ingest_csv(
        file_path="data/sample_data.csv",
        encoding="utf-8",
        delimiter=","
    )
    
    print(f"✅ Ingested {result['row_count']} rows")
    print(f"📊 Columns: {', '.join(result['columns'])}")
```

**Result:** Data now in Fabric Lakehouse

---

## Phase 6: Connect to Fabric Workspace (30 minutes)

### Prerequisites:
- Fabric workspace created
- Service Principal with workspace access (for production)
- Credentials in .env file

### Step 1: Test Connection
```bash
# In main.py, uncomment:
example_basic_connection()

python main.py
```

### Step 2: Create Workspace Items
```bash
# In main.py, uncomment:
example_create_workspace_items()

python main.py
```

### Step 3: Deploy Semantic Models
Models are stored as JSON. Deploy to Fabric using:
```python
# Upload models/customer_churn_model.json to Fabric
# Via Fabric UI: Semantic Models > New > From .json
```

---

## Phase 7: Connect Power BI (15 minutes)

### In Power BI Desktop:
1. **Get Data** → **Power BI Datasets** → Select your workspace
2. Choose semantic model (e.g., Customer Churn)
3. Build visualizations using:
   - **Churn Rate** measure
   - **Region** dimension
   - **Subscription** dimension
   - Hierarchies for drill-down

### Example: Churn Analysis Dashboard
```
┌─────────────────────────────────────────┐
│     Churn Analysis by Region (%)        │
├─────────────────────────────────────────┤
│  East: 8.3%    │  South: 5.2%          │
│  West: 6.1%    │  North: 4.7%          │
└─────────────────────────────────────────┘
         ↓ (Click Region)
┌─────────────────────────────────────────┐
│  East Region - Churn by Subscription    │
├─────────────────────────────────────────┤
│  Premium: 6.8%                          │
│  Standard: 8.9%                         │
│  Basic: 10.2%                           │
└─────────────────────────────────────────┘
         ↓ (Click Subscription)
┌─────────────────────────────────────────┐
│  Premium Customers in East (At Risk)    │
├─────────────────────────────────────────┤
│  Customer ID  │ Tenure │ Monthly Charges│
│  CUST_001     │ 4m     │ $85            │
│  CUST_002     │ 6m     │ $95            │
│  ...          │ ...    │ ...            │
└─────────────────────────────────────────┘
```

---

## Troubleshooting

### Issue: "Module not found: fabric"
```bash
# Solution: Install requirements
pip install -r requirements.txt

# Or individually:
pip install fabric azure-identity
```

### Issue: "Authentication failed"
1. Check .env file has correct values
2. Verify credentials are active in Azure
3. Check workspace access permissions

### Issue: "No models in models/ directory"
1. Run semantic examples: `example_semantic_customer_churn()`
2. Verify script completed without errors
3. Check models directory path

### Issue: "CSV import fails"
1. Check file path is correct and accessible
2. Verify CSV format (comma-separated)
3. Review error message in logs

**Need more help?** See [INDEX.md - Troubleshooting](INDEX.md#troubleshooting)

---

## What You Now Have

✅ **Local Environment:**
- Python with all dependencies
- Configuration file (.env)
- Example code ready to run

✅ **Semantic Models:**
- Customer Churn model (JSON)
- Revenue Growth model (JSON)
- Supply Chain Risk model (JSON)
- Custom models you've created

✅ **Data Pipeline:**
- CSV ingestion
- SQL query support
- Batch processing capability
- Error handling

✅ **Documentation:**
- Architecture guide
- Example walkthroughs
- Model reference
- Troubleshooting guide

---

## Next Steps

### Immediate (Today):
1. ✅ Run examples: `python main.py`
2. ✅ Review generated models in `models/` directory
3. ✅ Read [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md)

### Short-term (This Week):
1. Create custom semantic models for your business domain
2. Test data ingestion with your own CSV/SQL sources
3. Deploy to Fabric workspace
4. Connect Power BI

### Long-term (This Month):
1. Set up automated data ingestion
2. Create production dashboards
3. Monitor data quality
4. Refine models based on feedback

---

## Documentation Map

| Need | Read |
|------|------|
| Quick overview | [README.md](README.md) |
| 5-minute examples | [QUICK_START.md](QUICK_START.md) |
| Model reference | [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md) |
| System architecture | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Data ingestion | [DATA_INGESTION_GUIDE.md](DATA_INGESTION_GUIDE.md) |
| Semantic models | [SEMANTIC_MODEL_GUIDE.md](SEMANTIC_MODEL_GUIDE.md) |
| Real examples | [SEMANTIC_MAPPING_EXAMPLES.md](SEMANTIC_MAPPING_EXAMPLES.md) |
| All docs | [INDEX.md](INDEX.md) |

---

## Success Checklist

- [ ] Python installed and requirements installed
- [ ] .env file configured with Fabric credentials
- [ ] First example runs successfully: `example_basic_connection()`
- [ ] All semantic models generated in `models/` directory
- [ ] Reviewed [SEMANTIC_MODELS_QUICK_REF.md](SEMANTIC_MODELS_QUICK_REF.md)
- [ ] Understood data flow from [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Created custom semantic model for your business
- [ ] Successfully ingested sample data
- [ ] Connected to Fabric workspace
- [ ] Connected Power BI to semantic model
- [ ] Created first dashboard

When all items are checked, you're production-ready! 🚀

---

**Congratulations!** You now have a complete, production-ready data analytics solution built on Microsoft Fabric.

**Questions?** Start with [INDEX.md](INDEX.md) - it has links to all documentation.
