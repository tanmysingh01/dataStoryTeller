# Data Ingestion Quick Start Guide

Get started with data ingestion in Microsoft Fabric within minutes.

## Prerequisites

- [x] Python environment configured (see [README.md](README.md))
- [x] Dependencies installed: `pip install -r requirements.txt`
- [x] `.env` file configured with Fabric credentials
- [x] CSV files or SQL Server access

## Quick Examples

### 1. Ingest a CSV File (5 minutes)

```python
from fabric_connection import FabricSessionManager
from data_ingestion import create_ingestion_pipeline

# Setup connection
with FabricSessionManager() as connection:
    # Create pipeline
    pipeline = create_ingestion_pipeline(
        connection=connection,
        workspace_id="workspace-001",
        workspace_name="MyWorkspace",
        lakehouse_name="my_lakehouse"
    )
    
    # Ingest CSV
    result = pipeline.ingest_csv(
        file_path="data/sample_data.csv",
        table_name="sales",
        mode="overwrite"
    )
    
    # Check result
    print(f"Status: {result['status']}")
    print(f"Records: {result['records']}")
```

### 2. Ingest Data from SQL Server (10 minutes)

```python
from data_ingestion import create_sql_source

# Create SQL connection
sql_source = create_sql_source(
    server="your-server.database.windows.net",
    database="SalesDB",
    username="admin@company",
    password="YourPassword123"
)

# Ingest a table
result = pipeline.ingest_sql_table(
    table_name="Customers",
    sql_source=sql_source,
    schema="dbo"
)

print(f"Ingested {result['records']} customer records")

# Cleanup
sql_source.disconnect()
```

### 3. Ingest from SQL Query (10 minutes)

```python
# Filter data with SQL query
result = pipeline.ingest_sql_query(
    sql_query="SELECT * FROM dbo.Orders WHERE OrderDate > '2024-01-01' AND Status='Completed'",
    table_name="recent_orders",
    sql_source=sql_source
)

print(f"Ingested {result['records']} recent orders")
```

### 4. Ingest Multiple Sources (15 minutes)

```python
# Define batch configuration
sources = [
    {
        "type": "CSV",
        "source": "data/customers.csv",
        "table_name": "customers"
    },
    {
        "type": "CSV",
        "source": "data/products.csv",
        "table_name": "products"
    },
    {
        "type": "SQL_TABLE",
        "source": "Orders",
        "table_name": "orders"
    }
]

# Process all sources
results = pipeline.ingest_batch(sources, sql_source=sql_source)

# Check results
for result in results:
    print(f"{result['table_name']}: {result['status']}")
```

### 5. Generate Ingestion Report (5 minutes)

```python
# Generate comprehensive report
report = pipeline.get_ingestion_report(
    save_path="ingestion_report.json"
)

# Display summary
print(f"Total Ingestions: {report['summary']['total_ingestions']}")
print(f"Successful: {report['summary']['successful']}")
print(f"Failed: {report['summary']['failed']}")
print(f"Success Rate: {report['summary']['success_rate']}")
print(f"Total Records: {report['summary']['total_records_ingested']}")
```

## Common Scenarios

### Scenario 1: Daily CSV Import

**Task:** Load daily sales data from CSV every morning

```python
import os
from datetime import datetime

# Daily CSV location
csv_file = f"data/sales_{datetime.now().strftime('%Y%m%d')}.csv"

if os.path.exists(csv_file):
    result = pipeline.ingest_csv(
        file_path=csv_file,
        table_name="daily_sales",
        mode="append"  # Append, don't overwrite
    )
    
    if result['status'] == 'success':
        print(f"✓ Loaded {result['records']} records")
    else:
        print(f"✗ Error: {result['error']}")
else:
    print(f"File not found: {csv_file}")
```

### Scenario 2: Incremental SQL Sync

**Task:** Sync only new/modified records from SQL Server

```python
# Query only recent changes
query = """
    SELECT * FROM dbo.Orders 
    WHERE ModifiedDate > DATEADD(DAY, -1, CAST(GETDATE() AS DATE))
"""

result = pipeline.ingest_sql_query(
    sql_query=query,
    table_name="orders_incremental",
    sql_source=sql_source,
    mode="append"
)
```

### Scenario 3: Multi-Source ETL Pipeline

**Task:** Extract from multiple sources, load to one lakehouse

```python
# Configuration for entire ETL
etl_config = [
    # From CSV files
    {"type": "CSV", "source": "source1/data.csv", "table_name": "source1_data"},
    {"type": "CSV", "source": "source2/data.csv", "table_name": "source2_data"},
    
    # From SQL queries
    {"type": "SQL", "source": "SELECT * FROM SourceDB.dbo.Table1", "table_name": "table1"},
    {"type": "SQL", "source": "SELECT * FROM SourceDB.dbo.Table2", "table_name": "table2"},
    
    # Complete SQL tables
    {"type": "SQL_TABLE", "source": "Table3", "table_name": "table3"}
]

# Execute pipeline
results = pipeline.ingest_batch(etl_config, sql_source=sql_source)

# Log summary
successful = sum(1 for r in results if r['status'] == 'success')
print(f"✓ {successful} of {len(results)} sources loaded successfully")
```

### Scenario 4: Error Handling and Retry Logic

**Task:** Handle errors gracefully and retry failed sources

```python
from data_ingestion import DataIngestionError

def ingest_with_retry(pipeline, config, max_retries=3):
    """Ingest with automatic retry on failure."""
    for attempt in range(max_retries):
        try:
            if config['type'] == 'CSV':
                result = pipeline.ingest_csv(
                    file_path=config['source'],
                    table_name=config['table_name']
                )
            else:
                result = pipeline.ingest_sql_query(
                    sql_query=config['source'],
                    table_name=config['table_name'],
                    sql_source=sql_source
                )
            
            if result['status'] == 'success':
                return result
        
        except DataIngestionError as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying... ({max_retries - attempt - 1} attempts left)")
                continue
            else:
                return {"status": "failed", "error": str(e)}
    
    return {"status": "failed", "error": "Max retries exceeded"}

# Use it
result = ingest_with_retry(pipeline, {"type": "CSV", "source": "data/file.csv", "table_name": "data"})
```

### Scenario 5: Data Quality Checks

**Task:** Validate data before and after ingestion

```python
import pandas as pd

# Read CSV
df = pd.read_csv("data/sales.csv")

# Validate data quality
print(f"Total rows: {len(df)}")
print(f"Missing values:\n{df.isnull().sum()}")
print(f"Data types:\n{df.dtypes}")

# Check for specific requirements
if df['amount'].min() < 0:
    print("WARNING: Negative amounts detected")

if df['date'].isnull().any():
    print("ERROR: Null dates found - cleaning...")
    df = df[df['date'].notna()]

# Ingest cleaned data
result = pipeline.ingest_csv(
    file_path="data/sales_cleaned.csv",
    table_name="sales"
)
```

## Troubleshooting Tips

### Check if File Exists
```python
import os
file_path = "data/sales.csv"
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    print(f"File found: {os.path.getsize(file_path)} bytes")
```

### Test SQL Connection
```python
if sql_source.connect():
    print("✓ SQL connection successful")
    
    # Test query
    test_result = sql_source.query("SELECT TOP 1 * FROM dbo.Customers")
    print(f"✓ Query returned {len(test_result)} rows")
else:
    print("✗ SQL connection failed")
```

### View Detailed Logs
```python
import logging

# Set log level to DEBUG for detailed output
logging.getLogger("data_ingestion").setLevel(logging.DEBUG)
logging.getLogger("fabric_connection").setLevel(logging.DEBUG)

# Now run ingestion - more details will be logged
result = pipeline.ingest_csv("data/sales.csv", "sales")
```

### Check Ingestion Report
```python
# Generate report to see what succeeded/failed
report = pipeline.get_ingestion_report()

print("\nFailed Ingestions:")
for item in report['details']:
    if item['status'] == 'failed':
        print(f"  - {item['table_name']}: {item['error']}")
```

## Performance Tips

### For Large CSV Files
```python
# Process in chunks for large files
import pandas as pd

chunksize = 100000
for i, chunk in enumerate(pd.read_csv("large_file.csv", chunksize=chunksize)):
    # Process each chunk
    temp_file = f"temp_chunk_{i}.csv"
    chunk.to_csv(temp_file, index=False)
    
    # Ingest chunk
    result = pipeline.ingest_csv(temp_file, f"sales_chunk_{i}")
    print(f"Chunk {i}: {result['records']} records")
```

### For SQL Queries
```python
# Use indexes and WHERE clauses to reduce data
query = """
    SELECT * FROM dbo.LargeTable 
    WHERE year(CreatedDate) = 2024 
    AND Status IN ('Active', 'Completed')
"""

result = pipeline.ingest_sql_query(query, "filtered_data", sql_source)
```

### Optimize Batch Processing
```python
# Process similar types together
csv_configs = [c for c in batch_config if c['type'] == 'CSV']
sql_configs = [c for c in batch_config if c['type'] != 'CSV']

# Process CSVs first (no connection overhead)
csv_results = pipeline.ingest_batch(csv_configs)

# Then SQL (reuse connection)
sql_results = pipeline.ingest_batch(sql_configs, sql_source)
```

## Next Steps

1. **Explore the Sample Data:** Run examples with `data/sample_data.csv`
2. **Configure SQL Connection:** Update `.env` with SQL Server details
3. **Create Your First Pipeline:** Adapt examples to your data sources
4. **Set Up Scheduling:** Use Windows Task Scheduler or CI/CD for automation
5. **Monitor:** Check logs and ingestion reports regularly

## Resources

- [Complete Data Ingestion Guide](DATA_INGESTION_GUIDE.md)
- [Main README](README.md)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PyODBC Guide](https://github.com/mkleehammer/pyodbc/wiki)

## Support

For issues:
1. Check the [DATA_INGESTION_GUIDE.md](DATA_INGESTION_GUIDE.md) Troubleshooting section
2. Enable `LOG_LEVEL=DEBUG` in `.env`
3. Review error messages in the ingestion report
4. Check file paths and permissions
