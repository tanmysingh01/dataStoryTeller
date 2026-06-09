"""
Main entry point for Fabric workspace initialization and management.
Demonstrates complete workflow for connecting and setting up semantic modeling.
"""

import logging
import sys
import json
from typing import Optional
from config import FabricConfig
from fabric_connection import FabricConnection, FabricSessionManager
from workspace_init import FabricWorkspaceInit, setup_fabric_workspace
from data_ingestion import (
    DataIngestionPipeline,
    SQLDataSource,
    create_ingestion_pipeline,
    create_sql_source
)
from semantic_model_examples import (
    example_customer_churn_model,
    example_revenue_growth_model,
    example_supply_chain_model,
    example_integrated_model,
    example_create_custom_model,
    example_extend_model,
    example_model_comparison,
    print_model_statistics
)
from power_bi_examples import (
    example_customer_churn_dashboard,
    example_revenue_growth_dashboard,
    example_supply_chain_dashboard,
    example_executive_summary_dashboard,
    example_dax_measures_guide,
    example_export_for_power_bi,
    example_power_bi_quick_start
)

# Configure logging
logging.basicConfig(
    level=FabricConfig.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_basic_connection():
    """Example: Basic connection to Fabric workspace."""
    logger.info("=" * 60)
    logger.info("Example 1: Basic Connection")
    logger.info("=" * 60)
    
    try:
        # Create connection
        connection = FabricConnection(auth_method="service_principal")
        
        # Connect to workspace
        if connection.connect():
            logger.info("Successfully connected to Fabric workspace")
            
            # Get client for API calls
            client = connection.get_client()
            logger.info(f"Fabric client ready: {client is not None}")
            
            # Close connection
            connection.close()
        else:
            logger.error("Failed to connect to Fabric workspace")
            
    except Exception as e:
        logger.error(f"Error in basic connection: {str(e)}")


def example_context_manager():
    """Example: Using context manager for automatic connection handling."""
    logger.info("=" * 60)
    logger.info("Example 2: Context Manager Usage")
    logger.info("=" * 60)
    
    try:
        # Use context manager for automatic connection/disconnection
        with FabricSessionManager(auth_method="service_principal") as connection:
            logger.info("Connected using context manager")
            
            # Connection is active here
            client = connection.get_client()
            logger.info(f"Client available in context: {client is not None}")
            
        # Connection automatically closed here
        logger.info("Connection automatically closed")
        
    except Exception as e:
        logger.error(f"Error in context manager: {str(e)}")


def example_workspace_initialization():
    """Example: Initialize workspace and prepare for semantic modeling."""
    logger.info("=" * 60)
    logger.info("Example 3: Workspace Initialization")
    logger.info("=" * 60)
    
    try:
        with FabricSessionManager() as connection:
            # Initialize workspace manager
            workspace_init = FabricWorkspaceInit(connection)
            
            # Initialize workspace
            workspace_name = FabricConfig.WORKSPACE_NAME or "MyFabricWorkspace"
            workspace_id = FabricConfig.WORKSPACE_ID or "default-workspace"
            
            if workspace_init.initialize_workspace(workspace_name, workspace_id):
                logger.info(f"Workspace initialized: {workspace_name}")
                
                # Prepare for semantic modeling
                setup_result = workspace_init.prepare_for_semantic_modeling()
                
                if setup_result:
                    logger.info(f"Setup status: {setup_result['status']}")
                    logger.info(f"Components created: {setup_result['components']}")
            else:
                logger.error("Failed to initialize workspace")
                
    except Exception as e:
        logger.error(f"Error in workspace initialization: {str(e)}")


def example_csv_ingestion():
    """Example: Ingest CSV file into Lakehouse."""
    logger.info("=" * 60)
    logger.info("Example 5: CSV Data Ingestion")
    logger.info("=" * 60)
    
    try:
        with FabricSessionManager() as connection:
            # Create ingestion pipeline
            pipeline = create_ingestion_pipeline(
                connection=connection,
                workspace_id=FabricConfig.WORKSPACE_ID or "workspace-001",
                workspace_name=FabricConfig.WORKSPACE_NAME or "MyWorkspace",
                lakehouse_name="data_lakehouse"
            )
            
            # Ingest CSV file
            result = pipeline.ingest_csv(
                file_path="data/sample_data.csv",
                table_name="sales_data",
                encoding="utf-8",
                mode="overwrite"
            )
            
            logger.info(f"Ingestion result: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        logger.error(f"Error in CSV ingestion: {str(e)}")


def example_sql_ingestion():
    """Example: Ingest data from SQL Server."""
    logger.info("=" * 60)
    logger.info("Example 6: SQL Data Ingestion")
    logger.info("=" * 60)
    
    try:
        with FabricSessionManager() as connection:
            # Create SQL data source
            sql_source = create_sql_source(
                server="localhost",
                database="SalesDB",
                username="sa",
                password="YourPassword123!"
            )
            
            # Create ingestion pipeline
            pipeline = create_ingestion_pipeline(
                connection=connection,
                workspace_id=FabricConfig.WORKSPACE_ID or "workspace-001",
                workspace_name=FabricConfig.WORKSPACE_NAME or "MyWorkspace",
                lakehouse_name="data_lakehouse"
            )
            
            # Ingest entire SQL table
            result = pipeline.ingest_sql_table(
                table_name="Customers",
                sql_source=sql_source,
                schema="dbo"
            )
            
            logger.info(f"Ingestion result: {json.dumps(result, indent=2)}")
            
            # Ingest with custom SQL query
            query_result = pipeline.ingest_sql_query(
                sql_query="SELECT * FROM dbo.Orders WHERE OrderDate > '2024-01-01'",
                table_name="recent_orders",
                sql_source=sql_source
            )
            
            logger.info(f"Query ingestion result: {json.dumps(query_result, indent=2)}")
            
            sql_source.disconnect()
            
    except Exception as e:
        logger.error(f"Error in SQL ingestion: {str(e)}")


def example_batch_ingestion():
    """Example: Ingest multiple data sources in batch."""
    logger.info("=" * 60)
    logger.info("Example 7: Batch Data Ingestion")
    logger.info("=" * 60)
    
    try:
        with FabricSessionManager() as connection:
            # Create SQL data source for SQL ingestions
            sql_source = create_sql_source(
                server="localhost",
                database="SalesDB",
                username="sa",
                password="YourPassword123!"
            )
            
            # Create ingestion pipeline
            pipeline = create_ingestion_pipeline(
                connection=connection,
                workspace_id=FabricConfig.WORKSPACE_ID or "workspace-001",
                workspace_name=FabricConfig.WORKSPACE_NAME or "MyWorkspace",
                lakehouse_name="data_lakehouse"
            )
            
            # Define batch ingestion configuration
            batch_config = [
                {
                    "type": "CSV",
                    "source": "data/customers.csv",
                    "table_name": "customers",
                    "encoding": "utf-8",
                    "mode": "overwrite"
                },
                {
                    "type": "CSV",
                    "source": "data/products.csv",
                    "table_name": "products",
                    "encoding": "utf-8",
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
            
            # Execute batch ingestion
            batch_results = pipeline.ingest_batch(batch_config, sql_source=sql_source)
            
            # Log summary
            successful = sum(1 for r in batch_results if r["status"] == "success")
            logger.info(f"✓ Batch completed: {successful}/{len(batch_results)} successful")
            
            for idx, result in enumerate(batch_results, 1):
                logger.info(f"  [{idx}] {result['table_name']}: {result['status']}")
            
            sql_source.disconnect()
            
    except Exception as e:
        logger.error(f"Error in batch ingestion: {str(e)}")


def example_ingestion_report():
    """Example: Generate ingestion report."""
    logger.info("=" * 60)
    logger.info("Example 8: Ingestion Report Generation")
    logger.info("=" * 60)
    
    try:
        with FabricSessionManager() as connection:
            # Create SQL data source
            sql_source = create_sql_source(
                server="localhost",
                database="SalesDB",
                username="sa",
                password="YourPassword123!"
            )
            
            # Create ingestion pipeline
            pipeline = create_ingestion_pipeline(
                connection=connection,
                workspace_id=FabricConfig.WORKSPACE_ID or "workspace-001",
                workspace_name=FabricConfig.WORKSPACE_NAME or "MyWorkspace",
                lakehouse_name="data_lakehouse"
            )
            
            # Perform some ingestions
            pipeline.ingest_csv(
                file_path="data/sales.csv",
                table_name="sales_data"
            )
            
            pipeline.ingest_sql_table(
                table_name="Customers",
                sql_source=sql_source
            )
            
            # Generate report
            report = pipeline.get_ingestion_report(
                save_path="ingestion_report.json"
            )
            
            logger.info(f"Report Summary:")
            logger.info(f"  Total Ingestions: {report['summary']['total_ingestions']}")
            logger.info(f"  Successful: {report['summary']['successful']}")
            logger.info(f"  Failed: {report['summary']['failed']}")
            logger.info(f"  Total Records: {report['summary']['total_records_ingested']}")
            logger.info(f"  Success Rate: {report['summary']['success_rate']}")
            
            sql_source.disconnect()
            
    except Exception as e:
        logger.error(f"Error in report generation: {str(e)}")


def example_semantic_customer_churn():
    """Example: Customer churn semantic model."""
    logger.info("=" * 60)
    logger.info("Example 9: Customer Churn Semantic Model")
    logger.info("=" * 60)
    
    try:
        example_customer_churn_model()
    except Exception as e:
        logger.error(f"Error in semantic model example: {str(e)}")


def example_semantic_revenue_growth():
    """Example: Revenue growth semantic model."""
    logger.info("=" * 60)
    logger.info("Example 10: Revenue Growth Semantic Model")
    logger.info("=" * 60)
    
    try:
        example_revenue_growth_model()
    except Exception as e:
        logger.error(f"Error in semantic model example: {str(e)}")


def example_semantic_supply_chain():
    """Example: Supply chain risk semantic model."""
    logger.info("=" * 60)
    logger.info("Example 11: Supply Chain Risk Semantic Model")
    logger.info("=" * 60)
    
    try:
        example_supply_chain_model()
    except Exception as e:
        logger.error(f"Error in semantic model example: {str(e)}")


def example_semantic_integrated():
    """Example: Integrated business semantic model."""
    logger.info("=" * 60)
    logger.info("Example 12: Integrated Business Semantic Model")
    logger.info("=" * 60)
    
    try:
        example_integrated_model()
    except Exception as e:
        logger.error(f"Error in semantic model example: {str(e)}")


def example_semantic_custom():
    """Example: Create custom semantic model."""
    logger.info("=" * 60)
    logger.info("Example 13: Create Custom Semantic Model")
    logger.info("=" * 60)
    
    try:
        model = example_create_custom_model()
        print_model_statistics(model)
    except Exception as e:
        logger.error(f"Error in custom model example: {str(e)}")


def example_semantic_extend():
    """Example: Extend semantic model."""
    logger.info("=" * 60)
    logger.info("Example 14: Extend Semantic Model")
    logger.info("=" * 60)
    
    try:
        example_extend_model()
    except Exception as e:
        logger.error(f"Error in model extension example: {str(e)}")


def example_semantic_comparison():
    """Example: Compare semantic models."""
    logger.info("=" * 60)
    logger.info("Example 15: Compare Semantic Models")
    logger.info("=" * 60)
    
    try:
        example_model_comparison()
    except Exception as e:
        logger.error(f"Error in model comparison: {str(e)}")


def example_power_bi_churn_dashboard():
    """Example: Customer churn dashboard for Power BI."""
    logger.info("=" * 60)
    logger.info("Example 16: Power BI - Customer Churn Dashboard")
    logger.info("=" * 60)
    
    try:
        example_customer_churn_dashboard()
    except Exception as e:
        logger.error(f"Error in Power BI dashboard: {str(e)}")


def example_power_bi_revenue_dashboard():
    """Example: Revenue growth dashboard for Power BI."""
    logger.info("=" * 60)
    logger.info("Example 17: Power BI - Revenue Growth Dashboard")
    logger.info("=" * 60)
    
    try:
        example_revenue_growth_dashboard()
    except Exception as e:
        logger.error(f"Error in Power BI dashboard: {str(e)}")


def example_power_bi_supply_chain_dashboard():
    """Example: Supply chain dashboard for Power BI."""
    logger.info("=" * 60)
    logger.info("Example 18: Power BI - Supply Chain Dashboard")
    logger.info("=" * 60)
    
    try:
        example_supply_chain_dashboard()
    except Exception as e:
        logger.error(f"Error in Power BI dashboard: {str(e)}")


def example_power_bi_executive_dashboard():
    """Example: Executive summary dashboard for Power BI."""
    logger.info("=" * 60)
    logger.info("Example 19: Power BI - Executive Summary Dashboard")
    logger.info("=" * 60)
    
    try:
        example_executive_summary_dashboard()
    except Exception as e:
        logger.error(f"Error in Power BI dashboard: {str(e)}")


def example_power_bi_dax_measures():
    """Example: DAX measures reference for Power BI."""
    logger.info("=" * 60)
    logger.info("Example 20: Power BI - DAX Measures Reference")
    logger.info("=" * 60)
    
    try:
        example_dax_measures_guide()
    except Exception as e:
        logger.error(f"Error in DAX guide: {str(e)}")


def example_power_bi_export():
    """Example: Export semantic models for Power BI."""
    logger.info("=" * 60)
    logger.info("Example 21: Power BI - Export Data & Templates")
    logger.info("=" * 60)
    
    try:
        example_export_for_power_bi()
    except Exception as e:
        logger.error(f"Error in Power BI export: {str(e)}")


def example_power_bi_quick_start_guide():
    """Example: Quick start guide for Power BI."""
    logger.info("=" * 60)
    logger.info("Example 22: Power BI - Quick Start Guide")
    logger.info("=" * 60)
    
    try:
        example_power_bi_quick_start()
    except Exception as e:
        logger.error(f"Error in quick start guide: {str(e)}")






    """Example: Create specific workspace items."""
    logger.info("=" * 60)
    logger.info("Example 4: Create Workspace Items")
    logger.info("=" * 60)
    
    try:
        with FabricSessionManager() as connection:
            workspace_init = FabricWorkspaceInit(connection)
            
            # Initialize workspace
            workspace_init.initialize_workspace("Analytics", "workspace-001")
            
            # Create lakehouse
            lakehouse = workspace_init.create_lakehouse(
                "sales_lakehouse",
                "Central data lake for sales analytics"
            )
            logger.info(f"Created: {lakehouse}")
            
            # Create semantic model
            model = workspace_init.create_semantic_model(
                "sales_model",
                "sales_dataset",
                "Semantic model for sales analysis"
            )
            logger.info(f"Created: {model}")
            
            # Create report
            report = workspace_init.create_report(
                "sales_report",
                "model-001",
                "Sales performance report"
            )
            logger.info(f"Created: {report}")
            
    except Exception as e:
        logger.error(f"Error creating workspace items: {str(e)}")


def main():
    """Main function - run examples."""
    logger.info("\n" + "=" * 60)
    logger.info("Microsoft Fabric Workspace Setup Examples")
    logger.info("=" * 60 + "\n")
    
    try:
        # Validate configuration
        FabricConfig.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        logger.info("\nPlease create a .env file with the following variables:")
        logger.info("  AZURE_TENANT_ID=your_tenant_id")
        logger.info("  AZURE_CLIENT_ID=your_client_id")
        logger.info("  AZURE_CLIENT_SECRET=your_client_secret")
        logger.info("  FABRIC_WORKSPACE_NAME=your_workspace_name")
        logger.info("  FABRIC_WORKSPACE_ID=your_workspace_id")
        logger.info("  AUTH_METHOD=service_principal")
        return
    
    # Run examples (comment out as needed)
    # WORKSPACE & CONNECTION EXAMPLES:
    # example_basic_connection()
    # example_context_manager()
    # example_workspace_initialization()
    # example_create_workspace_items()
    #
    # DATA INGESTION EXAMPLES:
    # example_csv_ingestion()
    # example_sql_ingestion()
    # example_batch_ingestion()
    # example_ingestion_report()
    #
    # SEMANTIC MODEL EXAMPLES:
    # example_semantic_customer_churn()
    # example_semantic_revenue_growth()
    # example_semantic_supply_chain()
    # example_semantic_integrated()
    # example_semantic_custom()
    # example_semantic_extend()
    # example_semantic_comparison()
    #
    # POWER BI DASHBOARD EXAMPLES:
    # example_power_bi_churn_dashboard()
    # example_power_bi_revenue_dashboard()
    # example_power_bi_supply_chain_dashboard()
    # example_power_bi_executive_dashboard()
    # example_power_bi_dax_measures()
    # example_power_bi_export()
    # example_power_bi_quick_start_guide()
    
    # Complete workspace setup
    logger.info("=" * 60)
    logger.info("Complete Workspace Setup")
    logger.info("=" * 60)
    
    workspace_name = FabricConfig.WORKSPACE_NAME or "MyFabricWorkspace"
    workspace_id = FabricConfig.WORKSPACE_ID or "default-workspace"
    
    result = setup_fabric_workspace(workspace_name, workspace_id)
    
    if result:
        logger.info(f"Setup completed with status: {result['status']}")
    else:
        logger.error("Workspace setup failed")


if __name__ == "__main__":
    main()
