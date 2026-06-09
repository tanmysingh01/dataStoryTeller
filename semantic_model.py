"""
Semantic model definitions for Microsoft Fabric workspace.
Maps raw data columns to business concepts with metrics, relationships, and calculations.
"""

import logging
import json
from typing import Optional, Dict, List, Any, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class DataType(Enum):
    """Data types for semantic model columns."""
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    DATE = "date"
    BOOLEAN = "boolean"
    DECIMAL = "decimal"


class AggregationFunction(Enum):
    """Aggregation functions for measures."""
    SUM = "sum"
    AVG = "average"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    DISTINCT_COUNT = "distinct_count"
    LAST = "last"
    FIRST = "first"


@dataclass
class Column:
    """Defines a column in a semantic table."""
    name: str
    display_name: str
    data_type: DataType
    description: str = ""
    hidden: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "displayName": self.display_name,
            "dataType": self.data_type.value,
            "description": self.description,
            "hidden": self.hidden
        }


@dataclass
class Measure:
    """Defines a calculated measure in a semantic model."""
    name: str
    display_name: str
    description: str
    column: str  # Column to aggregate
    aggregation: AggregationFunction
    format_string: Optional[str] = None  # e.g., "0.00%" for percentages
    calculation: Optional[str] = None  # DAX/M query expression
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "column": self.column,
            "aggregation": self.aggregation.value,
            "formatString": self.format_string,
            "calculation": self.calculation
        }


@dataclass
class Hierarchy:
    """Defines a hierarchy for drill-down analysis."""
    name: str
    display_name: str
    description: str
    levels: List[str]  # Column names in order from top to bottom
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "levels": self.levels
        }


@dataclass
class Relationship:
    """Defines a relationship between tables in semantic model."""
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    cardinality: str = "many-to-one"  # one-to-one, one-to-many, many-to-one, many-to-many
    active: bool = True
    cross_filter_direction: str = "both"  # single, both
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "fromTable": self.from_table,
            "fromColumn": self.from_column,
            "toTable": self.to_table,
            "toColumn": self.to_column,
            "cardinality": self.cardinality,
            "active": self.active,
            "crossFilterDirection": self.cross_filter_direction
        }


class SemanticTable:
    """Represents a table in a semantic model."""
    
    def __init__(self, name: str, display_name: str, description: str = ""):
        """
        Initialize semantic table.
        
        Args:
            name: Table name (must match source table).
            display_name: Display name for business users.
            description: Table description.
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.columns: Dict[str, Column] = {}
        self.measures: Dict[str, Measure] = {}
        self.hierarchies: Dict[str, Hierarchy] = {}
        
        logger.info(f"Created semantic table: {name}")
    
    def add_column(self, column: Column) -> "SemanticTable":
        """Add a column to the table."""
        self.columns[column.name] = column
        logger.debug(f"Added column {column.name} to {self.name}")
        return self
    
    def add_measure(self, measure: Measure) -> "SemanticTable":
        """Add a measure to the table."""
        self.measures[measure.name] = measure
        logger.debug(f"Added measure {measure.name} to {self.name}")
        return self
    
    def add_hierarchy(self, hierarchy: Hierarchy) -> "SemanticTable":
        """Add a hierarchy to the table."""
        self.hierarchies[hierarchy.name] = hierarchy
        logger.debug(f"Added hierarchy {hierarchy.name} to {self.name}")
        return self
    
    def hide_column(self, column_name: str) -> "SemanticTable":
        """Hide a column from business users."""
        if column_name in self.columns:
            self.columns[column_name].hidden = True
            logger.debug(f"Hidden column {column_name}")
        return self
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "columns": [col.to_dict() for col in self.columns.values()],
            "measures": [m.to_dict() for m in self.measures.values()],
            "hierarchies": [h.to_dict() for h in self.hierarchies.values()]
        }


class SemanticModel:
    """Main semantic model that combines tables and relationships."""
    
    def __init__(self, name: str, display_name: str, description: str = "", version: str = "1.0"):
        """
        Initialize semantic model.
        
        Args:
            name: Model name.
            display_name: Display name for business users.
            description: Model description.
            version: Model version.
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.version = version
        self.tables: Dict[str, SemanticTable] = {}
        self.relationships: List[Relationship] = []
        self.created_at = datetime.now().isoformat()
        
        logger.info(f"Created semantic model: {name} v{version}")
    
    def add_table(self, table: SemanticTable) -> "SemanticModel":
        """Add a table to the model."""
        self.tables[table.name] = table
        logger.info(f"Added table {table.name} to model {self.name}")
        return self
    
    def add_relationship(self, relationship: Relationship) -> "SemanticModel":
        """Add a relationship between tables."""
        self.relationships.append(relationship)
        logger.info(f"Added relationship: {relationship.from_table}.{relationship.from_column} -> {relationship.to_table}.{relationship.to_column}")
        return self
    
    def get_table(self, table_name: str) -> Optional[SemanticTable]:
        """Retrieve a table by name."""
        return self.tables.get(table_name)
    
    def get_relationships_for_table(self, table_name: str) -> List[Relationship]:
        """Get all relationships involving a table."""
        return [
            r for r in self.relationships
            if r.from_table == table_name or r.to_table == table_name
        ]
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate semantic model integrity.
        
        Returns:
            Dict with validation results.
        """
        issues = []
        warnings = []
        
        # Check for tables
        if not self.tables:
            issues.append("Model has no tables")
        
        # Check relationships reference existing tables
        for rel in self.relationships:
            if rel.from_table not in self.tables:
                issues.append(f"Relationship references non-existent table: {rel.from_table}")
            if rel.to_table not in self.tables:
                issues.append(f"Relationship references non-existent table: {rel.to_table}")
            
            # Check columns exist
            from_table = self.tables.get(rel.from_table)
            if from_table and rel.from_column not in from_table.columns:
                issues.append(f"Relationship references non-existent column: {rel.from_table}.{rel.from_column}")
        
        # Check measures reference existing columns
        for table in self.tables.values():
            for measure in table.measures.values():
                if measure.column not in table.columns:
                    warnings.append(f"Measure {measure.name} references non-existent column: {measure.column}")
        
        # Check for circular relationships
        if self._has_circular_relationships():
            warnings.append("Model contains potential circular relationships")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "table_count": len(self.tables),
            "relationship_count": len(self.relationships)
        }
    
    def _has_circular_relationships(self) -> bool:
        """Check for circular relationships using DFS."""
        visited = set()
        rec_stack = set()
        
        def has_cycle(table_name: str) -> bool:
            visited.add(table_name)
            rec_stack.add(table_name)
            
            for rel in self.relationships:
                if rel.from_table == table_name:
                    neighbor = rel.to_table
                    if neighbor not in visited:
                        if has_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True
            
            rec_stack.remove(table_name)
            return False
        
        for table_name in self.tables:
            if table_name not in visited:
                if has_cycle(table_name):
                    return True
        
        return False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "version": self.version,
            "createdAt": self.created_at,
            "tables": [t.to_dict() for t in self.tables.values()],
            "relationships": [r.to_dict() for r in self.relationships]
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, file_path: str) -> bool:
        """Save model definition to JSON file."""
        try:
            with open(file_path, 'w') as f:
                f.write(self.to_json())
            logger.info(f"Saved semantic model to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model: {str(e)}")
            return False
    
    def get_summary(self) -> str:
        """Get a text summary of the model."""
        summary = f"""
        ===== Semantic Model: {self.display_name} =====
        Name: {self.name}
        Version: {self.version}
        
        Tables ({len(self.tables)}):
        """
        for table in self.tables.values():
            summary += f"\n  - {table.display_name} ({len(table.columns)} columns, {len(table.measures)} measures)"
        
        summary += f"\n\nRelationships ({len(self.relationships)}):\n"
        for rel in self.relationships:
            summary += f"  - {rel.from_table} -> {rel.to_table}\n"
        
        return summary


# Factory functions for common semantic models

def create_customer_churn_model() -> SemanticModel:
    """
    Create a semantic model for customer churn analysis.
    
    Maps raw columns to business concepts:
    - customer_id, tenure -> Customer dimension
    - churn_rate, monthly_charges -> Churn metrics
    - subscription_type -> Service offering
    """
    model = SemanticModel(
        name="customer_churn",
        display_name="Customer Churn Analysis",
        description="Semantic model for analyzing customer churn patterns and identifying at-risk customers"
    )
    
    # Customers table
    customers = SemanticTable("customers", "Customers", "Customer dimension table")
    customers.add_column(Column("customer_id", "Customer ID", DataType.STRING, "Unique customer identifier"))
    customers.add_column(Column("customer_name", "Customer Name", DataType.STRING, "Full name of customer"))
    customers.add_column(Column("tenure_months", "Tenure (Months)", DataType.INT, "Months as customer"))
    customers.add_column(Column("subscription_type", "Subscription Type", DataType.STRING, "Type of subscription"))
    customers.add_column(Column("monthly_charges", "Monthly Charges", DataType.DECIMAL, "Monthly subscription fee"))
    customers.add_column(Column("total_charges", "Total Charges", DataType.DECIMAL, "Lifetime charges"))
    customers.add_column(Column("is_churned", "Is Churned", DataType.BOOLEAN, "Whether customer has churned"))
    customers.add_column(Column("churn_date", "Churn Date", DataType.DATE, "Date of churn (if applicable)"))
    customers.add_column(Column("region", "Region", DataType.STRING, "Geographic region"))
    
    # Add measures for churn metrics
    customers.add_measure(Measure(
        "customer_count",
        "Total Customers",
        "Count of unique customers",
        "customer_id",
        AggregationFunction.DISTINCT_COUNT
    ))
    
    customers.add_measure(Measure(
        "churned_customers",
        "Churned Customers",
        "Count of customers who churned",
        "customer_id",
        AggregationFunction.COUNT,
        calculation="CALCULATE(COUNT(customers[customer_id]), FILTER(customers, customers[is_churned]=TRUE()))"
    ))
    
    customers.add_measure(Measure(
        "churn_rate",
        "Churn Rate",
        "Percentage of customers who churned",
        "is_churned",
        AggregationFunction.AVG,
        format_string="0.00%"
    ))
    
    customers.add_measure(Measure(
        "avg_tenure",
        "Average Tenure",
        "Average months as customer",
        "tenure_months",
        AggregationFunction.AVG,
        format_string="0.0"
    ))
    
    customers.add_measure(Measure(
        "avg_monthly_charges",
        "Average Monthly Charges",
        "Average monthly subscription fee",
        "monthly_charges",
        AggregationFunction.AVG,
        format_string="$#,##0.00"
    ))
    
    customers.add_measure(Measure(
        "total_revenue",
        "Total Revenue",
        "Sum of all charges",
        "total_charges",
        AggregationFunction.SUM,
        format_string="$#,##0.00"
    ))
    
    # Add hierarchies for drill-down
    customers.add_hierarchy(Hierarchy(
        "churn_analysis",
        "Churn Analysis",
        "Drill down by region and subscription type",
        ["region", "subscription_type", "customer_id"]
    ))
    
    customers.add_hierarchy(Hierarchy(
        "tenure_analysis",
        "Tenure Analysis",
        "Analyze by tenure bands",
        ["region", "tenure_months"]
    ))
    
    # Hide internal IDs
    customers.hide_column("customer_id")
    
    model.add_table(customers)
    
    logger.info("Created customer churn semantic model")
    return model


def create_revenue_growth_model() -> SemanticModel:
    """
    Create a semantic model for revenue growth analysis.
    
    Maps raw columns to business concepts:
    - sales, order_date -> Revenue dimension
    - product_category, region -> Sales segments
    - quantity, unit_price -> Revenue components
    """
    model = SemanticModel(
        name="revenue_growth",
        display_name="Revenue Growth Analysis",
        description="Semantic model for tracking revenue growth across products, regions, and time periods"
    )
    
    # Products table
    products = SemanticTable("products", "Products", "Product dimension")
    products.add_column(Column("product_id", "Product ID", DataType.STRING, "Unique product identifier"))
    products.add_column(Column("product_name", "Product Name", DataType.STRING, "Product name"))
    products.add_column(Column("category", "Category", DataType.STRING, "Product category"))
    products.add_column(Column("subcategory", "Subcategory", DataType.STRING, "Product subcategory"))
    products.add_column(Column("unit_price", "Unit Price", DataType.DECIMAL, "Base product price"))
    
    products.add_measure(Measure(
        "product_count",
        "Product Count",
        "Total number of products",
        "product_id",
        AggregationFunction.DISTINCT_COUNT
    ))
    
    products.add_hierarchy(Hierarchy(
        "product_hierarchy",
        "Product Hierarchy",
        "Product category drill-down",
        ["category", "subcategory", "product_name"]
    ))
    
    products.hide_column("product_id")
    model.add_table(products)
    
    # Sales table
    sales = SemanticTable("sales", "Sales", "Sales transaction facts")
    sales.add_column(Column("sales_id", "Sales ID", DataType.STRING, "Unique sales transaction ID"))
    sales.add_column(Column("order_date", "Order Date", DataType.DATE, "Date of sale"))
    sales.add_column(Column("product_id", "Product ID", DataType.STRING, "Reference to product"))
    sales.add_column(Column("region", "Region", DataType.STRING, "Geographic region"))
    sales.add_column(Column("quantity", "Quantity", DataType.INT, "Units sold"))
    sales.add_column(Column("unit_price", "Unit Price", DataType.DECIMAL, "Price per unit"))
    sales.add_column(Column("sales_amount", "Sales Amount", DataType.DECIMAL, "Total sales value"))
    sales.add_column(Column("cost_amount", "Cost Amount", DataType.DECIMAL, "Cost of goods sold"))
    sales.add_column(Column("profit_amount", "Profit Amount", DataType.DECIMAL, "Gross profit"))
    
    sales.add_measure(Measure(
        "total_sales",
        "Total Sales",
        "Sum of all sales",
        "sales_amount",
        AggregationFunction.SUM,
        format_string="$#,##0.00"
    ))
    
    sales.add_measure(Measure(
        "total_cost",
        "Total Cost",
        "Sum of all costs",
        "cost_amount",
        AggregationFunction.SUM,
        format_string="$#,##0.00"
    ))
    
    sales.add_measure(Measure(
        "total_profit",
        "Total Profit",
        "Total gross profit",
        "profit_amount",
        AggregationFunction.SUM,
        format_string="$#,##0.00"
    ))
    
    sales.add_measure(Measure(
        "profit_margin",
        "Profit Margin",
        "Profit as percentage of sales",
        "profit_amount",
        AggregationFunction.AVG,
        format_string="0.00%"
    ))
    
    sales.add_measure(Measure(
        "order_count",
        "Order Count",
        "Number of sales transactions",
        "sales_id",
        AggregationFunction.DISTINCT_COUNT
    ))
    
    sales.add_measure(Measure(
        "avg_order_value",
        "Average Order Value",
        "Average sales per transaction",
        "sales_amount",
        AggregationFunction.AVG,
        format_string="$#,##0.00"
    ))
    
    sales.add_hierarchy(Hierarchy(
        "sales_hierarchy",
        "Sales Hierarchy",
        "Drill down by region, product category, and date",
        ["region", "category", "product_name", "order_date"]
    ))
    
    sales.hide_column("sales_id")
    model.add_table(sales)
    
    # Add relationship: Sales -> Products
    model.add_relationship(Relationship(
        from_table="sales",
        from_column="product_id",
        to_table="products",
        to_column="product_id",
        cardinality="many-to-one"
    ))
    
    logger.info("Created revenue growth semantic model")
    return model


def create_supply_chain_risk_model() -> SemanticModel:
    """
    Create a semantic model for supply chain risk analysis.
    
    Maps raw columns to business concepts:
    - inventory_level, lead_time -> Supply chain metrics
    - supplier_reliability -> Supplier risk
    - demand_forecast -> Demand planning
    """
    model = SemanticModel(
        name="supply_chain_risk",
        display_name="Supply Chain Risk Analysis",
        description="Semantic model for identifying supply chain risks and inventory optimization"
    )
    
    # Suppliers table
    suppliers = SemanticTable("suppliers", "Suppliers", "Supplier dimension")
    suppliers.add_column(Column("supplier_id", "Supplier ID", DataType.STRING, "Unique supplier ID"))
    suppliers.add_column(Column("supplier_name", "Supplier Name", DataType.STRING, "Supplier name"))
    suppliers.add_column(Column("country", "Country", DataType.STRING, "Supplier country"))
    suppliers.add_column(Column("reliability_score", "Reliability Score", DataType.DECIMAL, "On-time delivery %"))
    suppliers.add_column(Column("avg_lead_time_days", "Avg Lead Time (Days)", DataType.INT, "Average lead time"))
    suppliers.add_column(Column("quality_score", "Quality Score", DataType.DECIMAL, "Quality rating 0-100"))
    
    suppliers.add_measure(Measure(
        "supplier_count",
        "Supplier Count",
        "Total number of suppliers",
        "supplier_id",
        AggregationFunction.DISTINCT_COUNT
    ))
    
    suppliers.add_measure(Measure(
        "avg_reliability",
        "Average Reliability",
        "Average on-time delivery rate",
        "reliability_score",
        AggregationFunction.AVG,
        format_string="0.00%"
    ))
    
    suppliers.add_measure(Measure(
        "avg_lead_time",
        "Average Lead Time",
        "Average supplier lead time",
        "avg_lead_time_days",
        AggregationFunction.AVG,
        format_string="0 days"
    ))
    
    suppliers.hide_column("supplier_id")
    model.add_table(suppliers)
    
    # Inventory table
    inventory = SemanticTable("inventory", "Inventory", "Inventory facts")
    inventory.add_column(Column("inventory_id", "Inventory ID", DataType.STRING, "Unique inventory record"))
    inventory.add_column(Column("product_id", "Product ID", DataType.STRING, "Product reference"))
    inventory.add_column(Column("warehouse_location", "Warehouse Location", DataType.STRING, "Storage location"))
    inventory.add_column(Column("current_stock_level", "Current Stock Level", DataType.INT, "Units in stock"))
    inventory.add_column(Column("safety_stock_level", "Safety Stock Level", DataType.INT, "Minimum safe level"))
    inventory.add_column(Column("reorder_point", "Reorder Point", DataType.INT, "Trigger for reorder"))
    inventory.add_column(Column("inventory_date", "Inventory Date", DataType.DATE, "Inventory snapshot date"))
    inventory.add_column(Column("days_of_supply", "Days of Supply", DataType.INT, "Estimated days supply"))
    inventory.add_column(Column("stockout_risk", "Stockout Risk", DataType.BOOLEAN, "Risk of stockout"))
    inventory.add_column(Column("overstock_risk", "Overstock Risk", DataType.BOOLEAN, "Risk of overstock"))
    inventory.add_column(Column("supplier_id", "Supplier ID", DataType.STRING, "Supplier reference"))
    
    inventory.add_measure(Measure(
        "total_inventory_units",
        "Total Inventory Units",
        "Sum of all inventory",
        "current_stock_level",
        AggregationFunction.SUM,
        format_string="#,##0"
    ))
    
    inventory.add_measure(Measure(
        "avg_days_supply",
        "Average Days of Supply",
        "Average inventory coverage",
        "days_of_supply",
        AggregationFunction.AVG,
        format_string="0.0 days"
    ))
    
    inventory.add_measure(Measure(
        "stockout_risk_count",
        "Stockout Risk Count",
        "Products at risk of stockout",
        "inventory_id",
        AggregationFunction.COUNT,
        calculation="CALCULATE(COUNT(inventory[inventory_id]), FILTER(inventory, inventory[stockout_risk]=TRUE()))"
    ))
    
    inventory.add_measure(Measure(
        "overstock_risk_count",
        "Overstock Risk Count",
        "Products at risk of overstock",
        "inventory_id",
        AggregationFunction.COUNT,
        calculation="CALCULATE(COUNT(inventory[inventory_id]), FILTER(inventory, inventory[overstock_risk]=TRUE()))"
    ))
    
    inventory.add_hierarchy(Hierarchy(
        "inventory_risk",
        "Inventory Risk",
        "Analyze inventory by risk and location",
        ["warehouse_location", "stockout_risk", "product_id"]
    ))
    
    inventory.hide_column("inventory_id")
    model.add_table(inventory)
    
    # Add relationship: Inventory -> Suppliers
    model.add_relationship(Relationship(
        from_table="inventory",
        from_column="supplier_id",
        to_table="suppliers",
        to_column="supplier_id",
        cardinality="many-to-one"
    ))
    
    logger.info("Created supply chain risk semantic model")
    return model


# Composite model combining all business concepts

def create_integrated_business_model() -> SemanticModel:
    """
    Create an integrated semantic model combining customer, revenue, and supply chain insights.
    """
    model = SemanticModel(
        name="integrated_business",
        display_name="Integrated Business Analytics",
        description="Comprehensive semantic model combining customer, revenue, and supply chain insights",
        version="2.0"
    )
    
    # Add all tables from individual models
    customer_model = create_customer_churn_model()
    revenue_model = create_revenue_growth_model()
    supply_model = create_supply_chain_risk_model()
    
    for table in customer_model.tables.values():
        model.add_table(table)
    
    for table in revenue_model.tables.values():
        model.add_table(table)
    
    for table in supply_model.tables.values():
        model.add_table(table)
    
    # Add relationships
    for rel in revenue_model.relationships:
        model.add_relationship(rel)
    
    for rel in supply_model.relationships:
        model.add_relationship(rel)
    
    logger.info("Created integrated business semantic model")
    return model
