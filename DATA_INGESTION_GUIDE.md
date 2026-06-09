# Data Ingestion Module Documentation

Complete guide for ingesting data into Microsoft Fabric from CSV and SQL sources with comprehensive error handling and logging.

## Overview

The data ingestion module provides a robust pipeline for:
- ✅ CSV file ingestion from OneLake
- ✅ SQL Server table and query ingestion
- ✅ Batch processing of multiple sources
- ✅ Data validation and quality checks
- ✅ Comprehensive error handling and logging
- ✅ Ingestion reporting and monitoring

## Module Components

### 1. OneLakeDataSource

Handles reading and uploading data from/to OneLake.

```python
from fabric_connection import FabricSessionManager
from data_ingestion import OneLakeDataSource

with FabricSessionManager() as connection:
    onelake = OneLakeDataSource(connection, workspace_id="workspace-001")
    
    # Read CSV from OneLake
    df = onelake.read_csv_from_onelake(
        file_path="data/sales.csv",
        encoding="utf-8",
        delimiter=","
    )
    
    # Upload DataFrame to Lakehouse
    success = onelake.upload_to_lakehouse(
        dataframe=df,
        lakehouse_name="my_lakehouse",
        table_name="sales_data",
        mode="overwrite"
    )
```

### 2. SQLDataSource

Manages connections to SQL Server databases and data retrieval.

```python
from data_ingestion import SQLDataSource

# Create SQL connection
sql_source = SQLDataSource(
    server="localhost",
    database="SalesDB",
    username="sa",
    password="YourPassword"
)

# Connect
if sql_source.connect():
    # Execute query
    df = sql_source.query(
        "SELECT * FROM dbo.Customers WHERE Status = 'Active'"
    )
    
    # Bulk insert data
    sql_source.bulk_insert(
        dataframe=df,
        table_name="new_customers",
        if_exists="replace"
    )
    
    sql_source.disconnect()
```

### 3. DataIngestionPipeline

Main orchestrator for complete data ingestion workflows.

```python
from fabric_connection import FabricSessionManager
from data_ingestion import create_ingestion_pipeline, create_sql_source

with FabricSessionManager() as connection:
    # Create pipeline
    pipeline = create_ingestion_pipeline(
        connection=connection,
        workspace_id="workspace-001",
        workspace_name="MyWorkspace",
        lakehouse_name="data_lakehouse"
    )
    
    # Ingest CSV
    csv_result = pipeline.ingest_csv(
        file_path="data/products.csv",
        table_name="products"
    )
    
    # Ingest SQL table
    sql_source = create_sql_source(
        server="localhost",
        database="SalesDB",
        username="sa",
        password="YourPassword"
    )
    
    sql_result = pipeline.ingest_sql_table(
        table_name="Customers",
        sql_source=sql_source
    )
    
    sql_source.disconnect()
```

## Usage Examples

### CSV Ingestion

```python
pipeline.ingest_csv(
    file_path="data/sales_data.csv",
    table_name="sales",
    encoding="utf-8",
    mode="overwrite",
    dtype={"amount": float, "quantity": int}
)
```

**Parameters:**
- `file_path`: Path to CSV file (required)
- `table_name`: Target table name (required)
- `encoding`: File encoding (default: 'utf-8')
- `mode`: Write mode - 'overwrite', 'append', 'ignore' (default: 'overwrite')
- `dtype`: Column data types (optional)

### SQL Table Ingestion

```python
sql_source = create_sql_source(
    server="your-server.database.windows.net",
    database="SalesDB",
    username="admin@company",
    password="SecurePassword123"
)

pipeline.ingest_sql_table(
    table_name="Orders",
    sql_source=sql_source,
    target_table_name="orders_fact",  # Optional: rename target
    schema="dbo"
)
```

### SQL Query Ingestion

```python
pipeline.ingest_sql_query(
    sql_query="SELECT * FROM dbo.Customers WHERE CreatedDate > '2024-01-01'",
    table_name="new_customers",
    sql_source=sql_source,
    parameters=None,  # For parameterized queries
    mode="append"
)
```

### Batch Ingestion

```python
batch_config = [
    {
        "type": "CSV",
        "source": "data/customers.csv",
        "table_name": "customers",
        "mode": "overwrite"
    },
    {
        "type": "CSV",
        "source": "data/products.csv",
        "table_name": "products",
        "mode": "overwrite"
    },
    {
        "type": "SQL_TABLE",
        "source": "Orders",
        "table_name": "orders",
        "schema": "dbo"
    },
    {
        "type": "SQL",
        "source": "SELECT * FROM dbo.Payments WHERE Status = 'Completed'",
        "table_name": "completed_payments",
        "mode": "overwrite"
    }
]

results = pipeline.ingest_batch(batch_config, sql_source=sql_source)
```

## Error Handling

The module includes comprehensive error handling with custom exceptions:

```python
from data_ingestion import DataIngestionError

try:
    result = pipeline.ingest_csv("data/sales.csv", "sales")
except DataIngestionError as e:
    logger.error(f"Ingestion error: {str(e)}")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
```

**Common Error Scenarios:**
- File not found
- Invalid CSV format
- SQL connection failure
- Empty DataFrame
- Null column names
- Data type mismatches

All errors are logged with detailed context for troubleshooting.

## Logging

Ingestion operations are logged at multiple levels:

```python
import logging

# Set logging level in .env
LOG_LEVEL=DEBUG  # For detailed output
LOG_LEVEL=INFO   # For normal operation
LOG_LEVEL=WARNING # For warnings and errors only
```

**Log Output Example:**
```
2024-06-09 10:15:23 - data_ingestion - INFO - Starting CSV ingestion: data/sales.csv -> sales
2024-06-09 10:15:24 - data_ingestion - INFO - ✓ Successfully read CSV: data/sales.csv
2024-06-09 10:15:24 - data_ingestion - INFO -   Shape: (1000, 5) | Columns: ['date', 'product', 'quantity', 'amount', 'region']
2024-06-09 10:15:24 - data_ingestion - INFO - Data Quality - Max null %: 2.5%
2024-06-09 10:15:25 - data_ingestion - INFO - ✓ Successfully uploaded 1000 records to sales
```

## Data Validation

DataFrame validation occurs automatically before upload:

```python
# Checks performed:
- Empty DataFrame detection
- Null column names
- Null percentage analysis
- Data type consistency
```

High null percentages trigger warnings:
```
WARNING - High null percentage detected: 65.50%
```

## Ingestion Reports

Generate comprehensive ingestion reports:

```python
report = pipeline.get_ingestion_report(
    save_path="reports/ingestion_report.json"
)

# Access report data
print(report['summary']['success_rate'])
print(report['summary']['total_records_ingested'])
print(report['details'])  # Detailed per-ingestion info
```

**Report Format:**
```json
{
  "summary": {
    "total_ingestions": 4,
    "successful": 3,
    "failed": 1,
    "success_rate": "75.0%",
    "total_records_ingested": 5250
  },
  "details": [
    {
      "source": "CSV",
      "file_path": "data/customers.csv",
      "table_name": "customers",
      "status": "success",
      "records": 1200,
      "timestamp": "2024-06-09T10:15:23.123456"
    },
    ...
  ],
  "generated_at": "2024-06-09T10:20:15.987654"
}
```

## Advanced Features

### Parameterized SQL Queries

```python
# Safe from SQL injection
query = "SELECT * FROM dbo.Orders WHERE CustomerID = ? AND OrderDate > ?"
results = sql_source.query(
    sql_query=query,
    parameters=[12345, "2024-01-01"]
)
```

### Custom Data Types

```python
dtypes = {
    'customer_id': int,
    'amount': float,
    'purchase_date': str,
    'is_active': bool
}

pipeline.ingest_csv(
    file_path="data/orders.csv",
    table_name="orders",
    dtype=dtypes
)
```

### Append Mode for Incremental Loads

```python
# Append new records without replacing
pipeline.ingest_csv(
    file_path="data/daily_transactions.csv",
    table_name="transactions",
    mode="append"
)
```

## Performance Considerations

### Optimize CSV Ingestion

```python
# Use chunking for large files
# Read in batches to reduce memory usage
import pandas as pd

chunksize = 100000
for chunk in pd.read_csv("large_file.csv", chunksize=chunksize):
    # Process chunk
    df = chunk
    # Ingest chunk
```

### Optimize SQL Queries

```python
# Use WHERE clause to filter data
# Avoid SELECT *
query = """
    SELECT customer_id, order_id, amount
    FROM dbo.Orders
    WHERE order_date >= '2024-01-01'
    AND status = 'Completed'
"""
```

### Batch Processing Efficiency

```python
# Process multiple sources in sequence
# Connection is reused across ingestions
batch_results = pipeline.ingest_batch(configs)

# All sources processed in single session
# Reduced connection overhead
```

## Security Best Practices

1. **Never hardcode credentials:**
   ```python
   # ✓ Good - Use environment variables
   sql_source = create_sql_source(
       server=os.getenv("SQL_SERVER"),
       database=os.getenv("SQL_DATABASE"),
       username=os.getenv("SQL_USERNAME"),
       password=os.getenv("SQL_PASSWORD")
   )
   
   # ✗ Bad - Hardcoded credentials
   sql_source = create_sql_source(
       server="localhost",
       database="SalesDB",
       username="sa",
       password="Password123"  # Never do this!
   )
   ```

2. **Use parameterized queries:**
   ```python
   # ✓ Good
   query = "SELECT * FROM dbo.Users WHERE id = ?"
   results = sql_source.query(query, parameters=[user_id])
   
   # ✗ Bad - SQL injection risk
   query = f"SELECT * FROM dbo.Users WHERE id = {user_id}"
   ```

3. **Validate file paths:**
   ```python
   import os
   from pathlib import Path
   
   file_path = "data/sales.csv"
   if not Path(file_path).exists():
       raise DataIngestionError(f"File not found: {file_path}")
   ```

## Troubleshooting

### CSV Not Found

```
✗ File not found: data/sales.csv
```

**Solution:**
- Verify file path is correct (relative or absolute)
- Check working directory
- Ensure file permissions are correct

### SQL Connection Failed

```
✗ SQL connection failed: Connection refused
```

**Solution:**
- Verify server address and port
- Check network connectivity
- Verify credentials are correct
- Ensure SQL Server is running

### DataFrame Empty

```
✗ DataFrame is empty or None
```

**Solution:**
- Check file content is not empty
- Verify SQL query returns results
- Check encoding setting matches file

### High Null Percentage

```
WARNING - High null percentage detected: 65.50%
```

**Solution:**
- Review data quality
- Check column mappings
- Consider data preprocessing

## Example: Complete Workflow

```python
from fabric_connection import FabricSessionManager
from data_ingestion import create_ingestion_pipeline, create_sql_source
import json

# Initialize
with FabricSessionManager() as connection:
    pipeline = create_ingestion_pipeline(
        connection=connection,
        workspace_id="workspace-001",
        workspace_name="Analytics",
        lakehouse_name="data_lake"
    )
    
    # Create SQL source
    sql = create_sql_source(
        server="sql-server.database.windows.net",
        database="ProductDB",
        username="admin",
        password="SecurePass123"
    )
    
    # Ingest multiple sources
    configs = [
        {"type": "CSV", "source": "data/customers.csv", "table_name": "customers"},
        {"type": "SQL_TABLE", "source": "Products", "table_name": "products"},
        {"type": "SQL", "source": "SELECT * FROM Orders WHERE Year(OrderDate)=2024", "table_name": "orders_2024"}
    ]
    
    results = pipeline.ingest_batch(configs, sql_source=sql)
    
    # Generate report
    report = pipeline.get_ingestion_report("ingestion_summary.json")
    
    print(f"Success Rate: {report['summary']['success_rate']}")
    print(f"Records Ingested: {report['summary']['total_records_ingested']}")
    
    sql.disconnect()
```

## Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PyODBC Documentation](https://github.com/mkleehammer/pyodbc)
- [Microsoft Fabric Python API](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-python-api)
- [SQL Server Best Practices](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-log-architecture-and-management-guide)

## License

This module is provided as-is for educational and development purposes.
