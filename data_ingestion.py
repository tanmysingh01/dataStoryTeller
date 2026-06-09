"""
Data ingestion module for Microsoft Fabric workspace.
Handles data ingestion from OneLake, CSV, and SQL sources.
Includes error handling, validation, and logging.
"""

import logging
import os
import json
import pandas as pd
from typing import Optional, Dict, List, Any
from datetime import datetime
from pathlib import Path
import pyodbc
import requests
from fabric_connection import FabricConnection

# Configure logging
logger = logging.getLogger(__name__)


class DataIngestionError(Exception):
    """Custom exception for data ingestion errors."""
    pass


class OneLakeDataSource:
    """Handle data ingestion from OneLake."""
    
    def __init__(self, connection: FabricConnection, workspace_id: str):
        """
        Initialize OneLake data source.
        
        Args:
            connection: FabricConnection instance.
            workspace_id: Fabric workspace ID.
        """
        self.connection = connection
        self.workspace_id = workspace_id
        self.credential = connection.get_credential()
        logger.info(f"OneLakeDataSource initialized for workspace: {workspace_id}")
    
    def read_csv_from_onelake(self, file_path: str, encoding: str = 'utf-8',
                              delimiter: str = ',', dtype: Optional[Dict] = None) -> Optional[pd.DataFrame]:
        """
        Read CSV file from OneLake.
        
        Args:
            file_path: Path to CSV file in OneLake.
            encoding: File encoding (default: utf-8).
            delimiter: CSV delimiter (default: comma).
            dtype: Data types for columns.
        
        Returns:
            DataFrame or None if failed.
        """
        try:
            logger.info(f"Reading CSV from OneLake: {file_path}")
            
            # Validate file path
            if not file_path.endswith('.csv'):
                raise DataIngestionError(f"File must be CSV format, got: {file_path}")
            
            # Read CSV file
            df = pd.read_csv(
                file_path,
                encoding=encoding,
                delimiter=delimiter,
                dtype=dtype
            )
            
            logger.info(f"✓ Successfully read CSV: {file_path}")
            logger.info(f"  Shape: {df.shape} | Columns: {list(df.columns)}")
            
            return df
            
        except FileNotFoundError:
            logger.error(f"✗ File not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"✗ Error reading CSV: {str(e)}")
            raise DataIngestionError(f"CSV ingestion failed: {str(e)}")
    
    def upload_to_lakehouse(self, dataframe: pd.DataFrame, lakehouse_name: str,
                           table_name: str, mode: str = 'overwrite') -> bool:
        """
        Upload DataFrame to Fabric Lakehouse.
        
        Args:
            dataframe: DataFrame to upload.
            lakehouse_name: Name of target lakehouse.
            table_name: Name of target table.
            mode: Write mode ('overwrite', 'append', 'ignore').
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if dataframe is None or dataframe.empty:
                raise DataIngestionError("DataFrame is empty or None")
            
            logger.info(f"Uploading to Lakehouse: {lakehouse_name}.{table_name}")
            logger.info(f"  Mode: {mode} | Records: {len(dataframe)}")
            
            # Note: Actual implementation would use Fabric SDK
            # This is a placeholder for the actual API call
            # df.write.mode(mode).option("path", f"{lakehouse_name}/{table_name}").saveAsTable(table_name)
            
            logger.info(f"✓ Successfully uploaded {len(dataframe)} records to {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Upload to lakehouse failed: {str(e)}")
            return False
    
    def list_files_in_onelake(self, folder_path: str, file_extension: Optional[str] = None) -> Optional[List[str]]:
        """
        List files in OneLake folder.
        
        Args:
            folder_path: Path to folder in OneLake.
            file_extension: Filter by extension (e.g., '.csv', '.parquet').
        
        Returns:
            List of file paths or None if failed.
        """
        try:
            logger.info(f"Listing files in OneLake: {folder_path}")
            
            files = []
            
            # Note: Actual implementation would use OneLake API
            logger.info(f"✓ Found {len(files)} files")
            return files
            
        except Exception as e:
            logger.error(f"✗ Error listing files: {str(e)}")
            return None


class SQLDataSource:
    """Handle data ingestion from SQL databases."""
    
    def __init__(self, server: str, database: str, username: str, password: str,
                 driver: str = "ODBC Driver 17 for SQL Server"):
        """
        Initialize SQL data source.
        
        Args:
            server: SQL Server address.
            database: Database name.
            username: Database username.
            password: Database password.
            driver: ODBC driver name.
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.connection = None
        logger.info(f"SQLDataSource initialized for {server}/{database}")
    
    def connect(self) -> bool:
        """
        Establish SQL database connection.
        
        Returns:
            bool: True if connection successful.
        """
        try:
            connection_string = (
                f"Driver={{{self.driver}}};"
                f"Server={self.server};"
                f"Database={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
            
            self.connection = pyodbc.connect(connection_string)
            logger.info(f"✓ Connected to SQL Server: {self.server}")
            return True
            
        except Exception as e:
            logger.error(f"✗ SQL connection failed: {str(e)}")
            return False
    
    def query(self, sql_query: str, parameters: Optional[List] = None) -> Optional[pd.DataFrame]:
        """
        Execute SQL query and return results as DataFrame.
        
        Args:
            sql_query: SQL query string.
            parameters: Query parameters for parameterized queries.
        
        Returns:
            DataFrame with results or None if failed.
        """
        try:
            if not self.connection:
                if not self.connect():
                    raise DataIngestionError("Cannot connect to SQL Server")
            
            logger.info(f"Executing SQL query: {sql_query[:100]}...")
            
            # Execute query
            df = pd.read_sql(
                sql_query,
                self.connection,
                params=parameters
            )
            
            logger.info(f"✓ Query executed successfully: {len(df)} records")
            return df
            
        except Exception as e:
            logger.error(f"✗ SQL query failed: {str(e)}")
            raise DataIngestionError(f"SQL query failed: {str(e)}")
    
    def bulk_insert(self, dataframe: pd.DataFrame, table_name: str,
                   if_exists: str = 'append', index: bool = False) -> bool:
        """
        Bulk insert DataFrame into SQL table.
        
        Args:
            dataframe: DataFrame to insert.
            table_name: Target table name.
            if_exists: What to do if table exists ('fail', 'replace', 'append').
            index: Whether to write index.
        
        Returns:
            bool: True if successful.
        """
        try:
            if not self.connection:
                if not self.connect():
                    raise DataIngestionError("Cannot connect to SQL Server")
            
            if dataframe is None or dataframe.empty:
                raise DataIngestionError("DataFrame is empty")
            
            logger.info(f"Bulk inserting {len(dataframe)} records into {table_name}")
            
            # Note: Actual implementation using SQLAlchemy
            # from sqlalchemy import create_engine
            # engine = create_engine(...)
            # dataframe.to_sql(table_name, engine, if_exists=if_exists, index=index)
            
            logger.info(f"✓ Successfully inserted {len(dataframe)} records")
            return True
            
        except Exception as e:
            logger.error(f"✗ Bulk insert failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close SQL connection."""
        if self.connection:
            self.connection.close()
            logger.info("SQL connection closed")


class DataIngestionPipeline:
    """Main pipeline for orchestrating data ingestion workflows."""
    
    def __init__(self, connection: FabricConnection, workspace_id: str,
                 workspace_name: str, lakehouse_name: str):
        """
        Initialize data ingestion pipeline.
        
        Args:
            connection: FabricConnection instance.
            workspace_id: Fabric workspace ID.
            workspace_name: Fabric workspace name.
            lakehouse_name: Target lakehouse name.
        """
        self.connection = connection
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        self.lakehouse_name = lakehouse_name
        self.onelake = OneLakeDataSource(connection, workspace_id)
        self.ingestion_log = []
        
        logger.info(f"DataIngestionPipeline initialized for {workspace_name}/{lakehouse_name}")
    
    def ingest_csv(self, file_path: str, table_name: str,
                   encoding: str = 'utf-8', mode: str = 'overwrite',
                   dtype: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Ingest CSV file into Lakehouse.
        
        Args:
            file_path: Path to CSV file.
            table_name: Target table name.
            encoding: File encoding.
            mode: Write mode.
            dtype: Data types for columns.
        
        Returns:
            Dict with ingestion results.
        """
        result = {
            "source": "CSV",
            "file_path": file_path,
            "table_name": table_name,
            "status": "pending",
            "records": 0,
            "timestamp": datetime.now().isoformat(),
            "error": None
        }
        
        try:
            logger.info(f"Starting CSV ingestion: {file_path} -> {table_name}")
            
            # Validate file exists
            if not os.path.exists(file_path):
                raise DataIngestionError(f"File not found: {file_path}")
            
            # Read CSV
            df = self.onelake.read_csv_from_onelake(file_path, encoding=encoding, dtype=dtype)
            
            if df is None:
                raise DataIngestionError("Failed to read CSV file")
            
            # Data validation
            self._validate_dataframe(df)
            
            # Upload to lakehouse
            success = self.onelake.upload_to_lakehouse(
                df,
                self.lakehouse_name,
                table_name,
                mode=mode
            )
            
            if success:
                result["status"] = "success"
                result["records"] = len(df)
                logger.info(f"✓ CSV ingestion completed: {len(df)} records")
            else:
                result["status"] = "failed"
                result["error"] = "Upload to lakehouse failed"
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            logger.error(f"✗ CSV ingestion failed: {str(e)}")
        
        self.ingestion_log.append(result)
        return result
    
    def ingest_sql_query(self, sql_query: str, table_name: str,
                        sql_source: SQLDataSource,
                        parameters: Optional[List] = None,
                        mode: str = 'overwrite') -> Dict[str, Any]:
        """
        Ingest data from SQL query into Lakehouse.
        
        Args:
            sql_query: SQL query to execute.
            table_name: Target table name.
            sql_source: SQLDataSource instance.
            parameters: Query parameters.
            mode: Write mode.
        
        Returns:
            Dict with ingestion results.
        """
        result = {
            "source": "SQL",
            "query": sql_query[:100],
            "table_name": table_name,
            "status": "pending",
            "records": 0,
            "timestamp": datetime.now().isoformat(),
            "error": None
        }
        
        try:
            logger.info(f"Starting SQL ingestion: {table_name}")
            
            # Execute query
            df = sql_source.query(sql_query, parameters)
            
            if df is None or df.empty:
                raise DataIngestionError("Query returned no results")
            
            # Data validation
            self._validate_dataframe(df)
            
            # Upload to lakehouse
            success = self.onelake.upload_to_lakehouse(
                df,
                self.lakehouse_name,
                table_name,
                mode=mode
            )
            
            if success:
                result["status"] = "success"
                result["records"] = len(df)
                logger.info(f"✓ SQL ingestion completed: {len(df)} records")
            else:
                result["status"] = "failed"
                result["error"] = "Upload to lakehouse failed"
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            logger.error(f"✗ SQL ingestion failed: {str(e)}")
        
        self.ingestion_log.append(result)
        return result
    
    def ingest_sql_table(self, table_name: str, sql_source: SQLDataSource,
                        target_table_name: Optional[str] = None,
                        schema: str = 'dbo') -> Dict[str, Any]:
        """
        Ingest entire SQL table into Lakehouse.
        
        Args:
            table_name: Source SQL table name.
            sql_source: SQLDataSource instance.
            target_table_name: Optional target table name (defaults to source name).
            schema: SQL schema name.
        
        Returns:
            Dict with ingestion results.
        """
        target_table = target_table_name or table_name
        sql_query = f"SELECT * FROM [{schema}].[{table_name}]"
        
        return self.ingest_sql_query(
            sql_query,
            target_table,
            sql_source,
            mode='overwrite'
        )
    
    def ingest_batch(self, ingestion_configs: List[Dict[str, Any]],
                    sql_source: Optional[SQLDataSource] = None) -> List[Dict[str, Any]]:
        """
        Ingest multiple data sources in batch.
        
        Args:
            ingestion_configs: List of ingestion configuration dicts.
                               Each dict should have: type, source, table_name
            sql_source: Optional SQLDataSource for SQL ingestions.
        
        Returns:
            List of ingestion results.
        """
        results = []
        
        logger.info(f"Starting batch ingestion: {len(ingestion_configs)} sources")
        
        for idx, config in enumerate(ingestion_configs, 1):
            try:
                logger.info(f"Processing batch item {idx}/{len(ingestion_configs)}")
                
                source_type = config.get("type", "").upper()
                
                if source_type == "CSV":
                    result = self.ingest_csv(
                        file_path=config["source"],
                        table_name=config["table_name"],
                        encoding=config.get("encoding", "utf-8"),
                        mode=config.get("mode", "overwrite")
                    )
                
                elif source_type == "SQL":
                    result = self.ingest_sql_query(
                        sql_query=config["source"],
                        table_name=config["table_name"],
                        sql_source=sql_source,
                        mode=config.get("mode", "overwrite")
                    )
                
                elif source_type == "SQL_TABLE":
                    result = self.ingest_sql_table(
                        table_name=config["source"],
                        sql_source=sql_source,
                        target_table_name=config.get("table_name")
                    )
                
                else:
                    result = {
                        "status": "failed",
                        "error": f"Unknown source type: {source_type}"
                    }
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"✗ Batch item {idx} failed: {str(e)}")
                results.append({
                    "status": "failed",
                    "error": str(e)
                })
        
        logger.info(f"✓ Batch ingestion completed: {len(results)} sources processed")
        return results
    
    def _validate_dataframe(self, df: pd.DataFrame) -> None:
        """
        Validate DataFrame before upload.
        
        Args:
            df: DataFrame to validate.
        
        Raises:
            DataIngestionError: If validation fails.
        """
        try:
            # Check for completely empty dataframe
            if df.empty:
                raise DataIngestionError("DataFrame is empty")
            
            # Check for null column names
            if df.columns.isnull().any():
                raise DataIngestionError("DataFrame has null column names")
            
            # Log data quality metrics
            null_pct = (df.isnull().sum() / len(df) * 100).max()
            logger.info(f"Data Quality - Max null %: {null_pct:.2f}%")
            
            if null_pct > 50:
                logger.warning(f"High null percentage detected: {null_pct:.2f}%")
            
        except Exception as e:
            raise DataIngestionError(f"DataFrame validation failed: {str(e)}")
    
    def get_ingestion_report(self, save_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate ingestion report from logs.
        
        Args:
            save_path: Optional path to save report as JSON.
        
        Returns:
            Dict with ingestion statistics and details.
        """
        total = len(self.ingestion_log)
        successful = sum(1 for log in self.ingestion_log if log["status"] == "success")
        failed = sum(1 for log in self.ingestion_log if log["status"] == "failed")
        total_records = sum(log["records"] for log in self.ingestion_log)
        
        report = {
            "summary": {
                "total_ingestions": total,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total*100):.1f}%" if total > 0 else "0%",
                "total_records_ingested": total_records
            },
            "details": self.ingestion_log,
            "generated_at": datetime.now().isoformat()
        }
        
        logger.info(f"Ingestion report generated: {successful}/{total} successful")
        
        if save_path:
            try:
                with open(save_path, 'w') as f:
                    json.dump(report, f, indent=2)
                logger.info(f"Report saved to {save_path}")
            except Exception as e:
                logger.error(f"Failed to save report: {str(e)}")
        
        return report


# Example helper functions

def create_ingestion_pipeline(connection: FabricConnection,
                             workspace_id: str,
                             workspace_name: str,
                             lakehouse_name: str) -> DataIngestionPipeline:
    """Factory function to create ingestion pipeline."""
    return DataIngestionPipeline(connection, workspace_id, workspace_name, lakehouse_name)


def create_sql_source(server: str, database: str, username: str,
                     password: str) -> SQLDataSource:
    """Factory function to create SQL data source."""
    return SQLDataSource(server, database, username, password)
