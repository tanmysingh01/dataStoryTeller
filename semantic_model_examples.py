"""
Examples and utilities for working with semantic models in Fabric.
"""

import logging
from semantic_model import (
    Column, Measure, Hierarchy, Relationship, SemanticTable, SemanticModel,
    DataType, AggregationFunction,
    create_customer_churn_model,
    create_revenue_growth_model,
    create_supply_chain_risk_model,
    create_integrated_business_model
)

logger = logging.getLogger(__name__)


def example_customer_churn_model():
    """Example: Customer churn semantic model."""
    logger.info("=" * 60)
    logger.info("Example: Customer Churn Semantic Model")
    logger.info("=" * 60)
    
    # Create the model
    model = create_customer_churn_model()
    
    # Validate model
    validation = model.validate()
    logger.info(f"Model validation: {validation['valid']}")
    logger.info(f"  Tables: {validation['table_count']}")
    logger.info(f"  Relationships: {validation['relationship_count']}")
    
    if validation['issues']:
        logger.warning(f"Issues: {validation['issues']}")
    
    # Print summary
    logger.info(model.get_summary())
    
    # Get customers table details
    customers = model.get_table("customers")
    logger.info(f"\nCustomers Table:")
    logger.info(f"  Columns: {len(customers.columns)}")
    for col in customers.columns.values():
        logger.info(f"    - {col.display_name} ({col.data_type.value})")
    
    logger.info(f"  Measures: {len(customers.measures)}")
    for measure in customers.measures.values():
        logger.info(f"    - {measure.display_name}: {measure.aggregation.value}({measure.column})")
    
    # Save model
    model.save_to_file("models/customer_churn_model.json")


def example_revenue_growth_model():
    """Example: Revenue growth semantic model."""
    logger.info("=" * 60)
    logger.info("Example: Revenue Growth Semantic Model")
    logger.info("=" * 60)
    
    model = create_revenue_growth_model()
    
    # Show relationships
    logger.info("Model Relationships:")
    for rel in model.relationships:
        logger.info(f"  {rel.from_table}.{rel.from_column} -> {rel.to_table}.{rel.to_column}")
    
    # Show sales measures
    sales = model.get_table("sales")
    logger.info(f"\nSales Measures:")
    for measure in sales.measures.values():
        logger.info(f"  - {measure.display_name}: {measure.description}")
    
    # Show hierarchies
    logger.info(f"\nHierarchies for drill-down:")
    for hierarchy in sales.hierarchies.values():
        logger.info(f"  - {hierarchy.display_name}: {' > '.join(hierarchy.levels)}")
    
    model.save_to_file("models/revenue_growth_model.json")


def example_supply_chain_model():
    """Example: Supply chain risk semantic model."""
    logger.info("=" * 60)
    logger.info("Example: Supply Chain Risk Semantic Model")
    logger.info("=" * 60)
    
    model = create_supply_chain_risk_model()
    
    # Show tables
    logger.info("Tables in model:")
    for table in model.tables.values():
        logger.info(f"  - {table.display_name}: {len(table.measures)} measures")
    
    # Show risk measures
    inventory = model.get_table("inventory")
    logger.info(f"\nInventory Risk Measures:")
    for measure in inventory.measures.values():
        if "risk" in measure.name.lower():
            logger.info(f"  - {measure.display_name}: {measure.description}")
    
    model.save_to_file("models/supply_chain_model.json")


def example_integrated_model():
    """Example: Integrated business semantic model."""
    logger.info("=" * 60)
    logger.info("Example: Integrated Business Semantic Model")
    logger.info("=" * 60)
    
    model = create_integrated_business_model()
    
    # Show overview
    logger.info(f"Model: {model.display_name}")
    logger.info(f"Tables: {len(model.tables)}")
    logger.info(f"Relationships: {len(model.relationships)}")
    
    # List all tables
    logger.info(f"\nAvailable Tables:")
    for table in model.tables.values():
        logger.info(f"  - {table.display_name}")
    
    # Validate integrated model
    validation = model.validate()
    logger.info(f"\nValidation Results:")
    logger.info(f"  Valid: {validation['valid']}")
    if validation['warnings']:
        logger.warning(f"  Warnings: {validation['warnings']}")
    
    model.save_to_file("models/integrated_business_model.json")


def example_create_custom_model():
    """Example: Create a custom semantic model."""
    logger.info("=" * 60)
    logger.info("Example: Create Custom Semantic Model")
    logger.info("=" * 60)
    
    # Create model
    model = SemanticModel(
        name="marketing_campaigns",
        display_name="Marketing Campaign Performance",
        description="Track marketing campaign effectiveness and ROI"
    )
    
    # Create campaigns table
    campaigns = SemanticTable("campaigns", "Campaigns", "Marketing campaigns")
    campaigns.add_column(Column("campaign_id", "Campaign ID", DataType.STRING))
    campaigns.add_column(Column("campaign_name", "Campaign Name", DataType.STRING))
    campaigns.add_column(Column("channel", "Channel", DataType.STRING, "Marketing channel: email, social, paid"))
    campaigns.add_column(Column("start_date", "Start Date", DataType.DATE))
    campaigns.add_column(Column("end_date", "End Date", DataType.DATE))
    campaigns.add_column(Column("budget", "Budget", DataType.DECIMAL))
    campaigns.add_column(Column("spend", "Spend", DataType.DECIMAL))
    campaigns.add_column(Column("impressions", "Impressions", DataType.INT))
    campaigns.add_column(Column("clicks", "Clicks", DataType.INT))
    campaigns.add_column(Column("conversions", "Conversions", DataType.INT))
    campaigns.add_column(Column("revenue", "Revenue", DataType.DECIMAL))
    
    # Add measures
    campaigns.add_measure(Measure(
        "campaign_count",
        "Campaign Count",
        "Total campaigns",
        "campaign_id",
        AggregationFunction.DISTINCT_COUNT
    ))
    
    campaigns.add_measure(Measure(
        "total_budget",
        "Total Budget",
        "Sum of campaign budgets",
        "budget",
        AggregationFunction.SUM,
        format_string="$#,##0.00"
    ))
    
    campaigns.add_measure(Measure(
        "ctr",
        "Click-Through Rate",
        "Clicks / Impressions",
        "clicks",
        AggregationFunction.SUM,
        format_string="0.00%",
        calculation="SUM(campaigns[clicks]) / SUM(campaigns[impressions])"
    ))
    
    campaigns.add_measure(Measure(
        "conversion_rate",
        "Conversion Rate",
        "Conversions / Clicks",
        "conversions",
        AggregationFunction.SUM,
        format_string="0.00%",
        calculation="SUM(campaigns[conversions]) / SUM(campaigns[clicks])"
    ))
    
    campaigns.add_measure(Measure(
        "roi",
        "ROI",
        "Return on Investment",
        "revenue",
        AggregationFunction.SUM,
        format_string="0.00%",
        calculation="(SUM(campaigns[revenue]) - SUM(campaigns[spend])) / SUM(campaigns[spend])"
    ))
    
    campaigns.add_hierarchy(Hierarchy(
        "campaign_hierarchy",
        "Campaign Hierarchy",
        "Channel > Campaign performance",
        ["channel", "campaign_name"]
    ))
    
    campaigns.hide_column("campaign_id")
    
    model.add_table(campaigns)
    
    logger.info("Created custom marketing model")
    logger.info(model.get_summary())
    
    model.save_to_file("models/custom_marketing_model.json")
    
    return model


def example_extend_model():
    """Example: Extend existing model with new measures."""
    logger.info("=" * 60)
    logger.info("Example: Extend Semantic Model")
    logger.info("=" * 60)
    
    model = create_customer_churn_model()
    customers = model.get_table("customers")
    
    # Add new measures to existing table
    customers.add_measure(Measure(
        "high_value_customers",
        "High Value Customers",
        "Customers with monthly charges > $100",
        "customer_id",
        AggregationFunction.COUNT,
        calculation="CALCULATE(COUNT(customers[customer_id]), FILTER(customers, customers[monthly_charges] > 100))"
    ))
    
    customers.add_measure(Measure(
        "at_risk_customers",
        "At-Risk Customers",
        "High-value customers with short tenure",
        "customer_id",
        AggregationFunction.COUNT,
        calculation="CALCULATE(COUNT(customers[customer_id]), FILTER(customers, customers[monthly_charges] > 100 AND customers[tenure_months] < 12))"
    ))
    
    # Add new hierarchy
    customers.add_hierarchy(Hierarchy(
        "value_segment",
        "Value Segmentation",
        "Segment by subscription type and charges",
        ["subscription_type", "monthly_charges"]
    ))
    
    logger.info("Extended model with new measures and hierarchies")
    logger.info(f"Measures now: {len(customers.measures)}")
    
    model.save_to_file("models/customer_churn_extended.json")


def example_model_comparison():
    """Example: Compare multiple semantic models."""
    logger.info("=" * 60)
    logger.info("Example: Compare Semantic Models")
    logger.info("=" * 60)
    
    models = {
        "Churn": create_customer_churn_model(),
        "Revenue": create_revenue_growth_model(),
        "Supply Chain": create_supply_chain_risk_model()
    }
    
    logger.info("Model Comparison:\n")
    logger.info(f"{'Model':<20} {'Tables':<10} {'Relationships':<15} {'Measures':<10}")
    logger.info("-" * 55)
    
    for name, model in models.items():
        total_measures = sum(len(t.measures) for t in model.tables.values())
        logger.info(f"{name:<20} {len(model.tables):<10} {len(model.relationships):<15} {total_measures:<10}")


# Display semantic model statistics

def print_model_statistics(model: SemanticModel):
    """Print detailed statistics about a semantic model."""
    logger.info(f"\n{'='*60}")
    logger.info(f"Semantic Model Statistics: {model.display_name}")
    logger.info(f"{'='*60}")
    
    # Table statistics
    logger.info(f"\nTables ({len(model.tables)}):")
    for table in model.tables.values():
        logger.info(f"  {table.display_name}:")
        logger.info(f"    - Columns: {len(table.columns)}")
        logger.info(f"    - Measures: {len(table.measures)}")
        logger.info(f"    - Hierarchies: {len(table.hierarchies)}")
    
    # Measure types
    logger.info(f"\nMeasure Types:")
    measure_types = {}
    for table in model.tables.values():
        for measure in table.measures.values():
            agg = measure.aggregation.value
            measure_types[agg] = measure_types.get(agg, 0) + 1
    
    for agg_type, count in measure_types.items():
        logger.info(f"  - {agg_type}: {count}")
    
    # Relationship statistics
    logger.info(f"\nRelationships ({len(model.relationships)}):")
    for rel in model.relationships:
        logger.info(f"  - {rel.from_table} [{rel.from_column}] -> {rel.to_table} [{rel.to_column}]")
        logger.info(f"    Cardinality: {rel.cardinality} | Active: {rel.active}")
    
    # Validation
    validation = model.validate()
    logger.info(f"\nValidation: {'✓ VALID' if validation['valid'] else '✗ INVALID'}")
    if validation['issues']:
        logger.warning(f"  Issues: {validation['issues']}")
    if validation['warnings']:
        logger.warning(f"  Warnings: {validation['warnings']}")
