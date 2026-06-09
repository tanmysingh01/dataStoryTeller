"""
Power BI integration for Fabric semantic models.
Provides utilities to create Power BI dashboards from semantic model outputs.
"""

import logging
import json
import csv
import pandas as pd
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import requests
from pathlib import Path

logger = logging.getLogger(__name__)


class VisualizationType(Enum):
    """Power BI visualization types."""
    BAR_CHART = "clusteredBarChart"
    COLUMN_CHART = "clusteredColumnChart"
    LINE_CHART = "lineChart"
    AREA_CHART = "areaChart"
    PIE_CHART = "pieChart"
    DONUT_CHART = "donutChart"
    SCATTER_CHART = "scatterChart"
    TABLE = "table"
    MATRIX = "matrix"
    KPI = "kpi"
    GAUGE = "gauge"
    CARD = "card"


class DashboardTheme(Enum):
    """Power BI dashboard themes."""
    LIGHT = "light"
    DARK = "dark"
    CLASSIC = "classic"


@dataclass
class PowerBIField:
    """Represents a field in Power BI visualization."""
    name: str
    display_name: str
    type: str  # "measure", "dimension", "date"
    format_string: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "displayName": self.display_name,
            "type": self.type,
            "formatString": self.format_string
        }


@dataclass
class PowerBIVisualization:
    """Represents a Power BI visualization (chart, KPI, etc.)."""
    name: str
    title: str
    visualization_type: VisualizationType
    x_axis: Optional[PowerBIField] = None
    y_axis: Optional[PowerBIField] = None
    measures: List[PowerBIField] = None
    dimensions: List[PowerBIField] = None
    filters: Dict[str, Any] = None
    position: Dict[str, int] = None  # {"x": 0, "y": 0, "width": 4, "height": 3}
    data_source: str = "semantic_model"
    
    def __post_init__(self):
        if self.measures is None:
            self.measures = []
        if self.dimensions is None:
            self.dimensions = []
        if self.filters is None:
            self.filters = {}
        if self.position is None:
            self.position = {"x": 0, "y": 0, "width": 4, "height": 3}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON export."""
        return {
            "name": self.name,
            "title": self.title,
            "visualizationType": self.visualization_type.value,
            "xAxis": self.x_axis.to_dict() if self.x_axis else None,
            "yAxis": self.y_axis.to_dict() if self.y_axis else None,
            "measures": [m.to_dict() for m in self.measures],
            "dimensions": [d.to_dict() for d in self.dimensions],
            "filters": self.filters,
            "position": self.position,
            "dataSource": self.data_source
        }


@dataclass
class PowerBIDashboard:
    """Represents a complete Power BI dashboard definition."""
    name: str
    display_name: str
    description: str
    theme: DashboardTheme = DashboardTheme.LIGHT
    visualizations: List[PowerBIVisualization] = None
    filters: Dict[str, List[str]] = None  # Dashboard-level filters
    refresh_schedule: Optional[str] = None  # e.g., "daily", "hourly"
    
    def __post_init__(self):
        if self.visualizations is None:
            self.visualizations = []
        if self.filters is None:
            self.filters = {}
    
    def add_visualization(self, viz: PowerBIVisualization) -> None:
        """Add visualization to dashboard."""
        self.visualizations.append(viz)
        logger.info(f"Added visualization: {viz.name}")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "theme": self.theme.value,
            "visualizationCount": len(self.visualizations),
            "visualizations": [v.to_dict() for v in self.visualizations],
            "filters": self.filters,
            "refreshSchedule": self.refresh_schedule,
            "createdDate": datetime.now().isoformat()
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, file_path: str) -> None:
        """Save dashboard definition to JSON file."""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(self.to_json())
        logger.info(f"Dashboard definition saved: {file_path}")


class PowerBIDAXGenerator:
    """Generate DAX measures for Power BI."""
    
    @staticmethod
    def sum_measure(measure_name: str, column: str, table: str) -> str:
        """Generate DAX for SUM measure."""
        return f"{measure_name} := SUM({table}[{column}])"
    
    @staticmethod
    def average_measure(measure_name: str, column: str, table: str) -> str:
        """Generate DAX for AVERAGE measure."""
        return f"{measure_name} := AVERAGE({table}[{column}])"
    
    @staticmethod
    def count_measure(measure_name: str, column: str, table: str) -> str:
        """Generate DAX for COUNT measure."""
        return f"{measure_name} := COUNT({table}[{column}])"
    
    @staticmethod
    def distinct_count_measure(measure_name: str, column: str, table: str) -> str:
        """Generate DAX for DISTINCTCOUNT measure."""
        return f"{measure_name} := DISTINCTCOUNT({table}[{column}])"
    
    @staticmethod
    def percentage_measure(measure_name: str, numerator: str, denominator: str) -> str:
        """Generate DAX for percentage measure."""
        return f"{measure_name} := DIVIDE({numerator}, {denominator}, 0)"
    
    @staticmethod
    def year_to_date_measure(measure_name: str, column: str, table: str, date_column: str) -> str:
        """Generate DAX for Year-to-Date calculation."""
        return f"""{measure_name} := CALCULATE(
            SUM({table}[{column}]),
            DATESYTD({table}[{date_column}])
        )"""
    
    @staticmethod
    def month_over_month_growth(measure_name: str, current_value: str, prior_value: str) -> str:
        """Generate DAX for Month-over-Month growth."""
        return f"{measure_name} := DIVIDE({current_value} - {prior_value}, {prior_value}, 0)"
    
    @staticmethod
    def running_total(measure_name: str, column: str, table: str, date_column: str) -> str:
        """Generate DAX for running total."""
        return f"""{measure_name} := CALCULATE(
            SUM({table}[{column}]),
            FILTER(ALL({table}[{date_column}]), {table}[{date_column}] <= MAX({table}[{date_column}]))
        )"""


class PowerBIRESTClient:
    """Client for Power BI REST API."""
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """Initialize Power BI REST client.
        
        Args:
            tenant_id: Azure AD tenant ID
            client_id: App registration client ID
            client_secret: App registration client secret
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.base_url = "https://api.powerbi.com/v1.0/myorg"
        logger.info("Power BI REST client initialized")
    
    def authenticate(self) -> bool:
        """Authenticate to Power BI API."""
        try:
            auth_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "https://analysis.windows.net/.default"
            }
            
            response = requests.post(auth_url, data=payload)
            response.raise_for_status()
            
            self.token = response.json()["access_token"]
            logger.info("✓ Authentication successful")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Authentication failed: {str(e)}")
            return False
    
    def get_workspaces(self) -> Optional[List[Dict]]:
        """Get list of Power BI workspaces."""
        if not self.token:
            logger.error("Not authenticated. Call authenticate() first.")
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/groups", headers=headers)
            response.raise_for_status()
            
            workspaces = response.json()["value"]
            logger.info(f"✓ Retrieved {len(workspaces)} workspaces")
            return workspaces
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to get workspaces: {str(e)}")
            return None
    
    def get_datasets(self, workspace_id: str) -> Optional[List[Dict]]:
        """Get datasets in a workspace."""
        if not self.token:
            logger.error("Not authenticated")
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            url = f"{self.base_url}/groups/{workspace_id}/datasets"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            datasets = response.json()["value"]
            logger.info(f"✓ Retrieved {len(datasets)} datasets")
            return datasets
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to get datasets: {str(e)}")
            return None
    
    def create_dashboard(self, workspace_id: str, dashboard_name: str) -> Optional[str]:
        """Create new Power BI dashboard.
        
        Args:
            workspace_id: Target workspace ID
            dashboard_name: Name for new dashboard
            
        Returns:
            Dashboard ID if successful, None otherwise
        """
        if not self.token:
            logger.error("Not authenticated")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            url = f"{self.base_url}/groups/{workspace_id}/dashboards"
            payload = {"name": dashboard_name}
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            dashboard_id = response.json()["id"]
            logger.info(f"✓ Created dashboard: {dashboard_name}")
            return dashboard_id
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to create dashboard: {str(e)}")
            return None
    
    def add_tile_to_dashboard(self, workspace_id: str, dashboard_id: str, 
                             dataset_id: str, visualization_id: str,
                             title: str) -> bool:
        """Add visualization tile to dashboard."""
        if not self.token:
            logger.error("Not authenticated")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            url = f"{self.base_url}/groups/{workspace_id}/dashboards/{dashboard_id}/tiles"
            
            payload = {
                "title": title,
                "visualizationUrl": f"semanticmodels/{dataset_id}/visualizations/{visualization_id}"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            logger.info(f"✓ Added tile to dashboard: {title}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to add tile: {str(e)}")
            return False
    
    def refresh_dataset(self, workspace_id: str, dataset_id: str) -> bool:
        """Trigger dataset refresh."""
        if not self.token:
            logger.error("Not authenticated")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            url = f"{self.base_url}/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
            
            response = requests.post(url, json={}, headers=headers)
            response.raise_for_status()
            
            logger.info(f"✓ Dataset refresh triggered")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Failed to refresh dataset: {str(e)}")
            return False


class PowerBIDataExporter:
    """Export semantic model data in formats suitable for Power BI."""
    
    @staticmethod
    def export_semantic_model_to_csv(semantic_model, output_dir: str = "power_bi_exports") -> Dict[str, str]:
        """Export semantic model tables to CSV files.
        
        Args:
            semantic_model: SemanticModel instance
            output_dir: Directory to save CSV files
            
        Returns:
            Dictionary mapping table names to file paths
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        exported_files = {}
        
        for table_name, table in semantic_model.tables.items():
            # Create CSV with table metadata and columns
            csv_path = f"{output_dir}/{table_name}.csv"
            
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Header: Column name, Display name, Type, Description
                writer.writerow(["Column", "Display Name", "Data Type", "Description", "Measure?"])
                
                # Write columns
                for column in table.columns:
                    writer.writerow([
                        column.name,
                        column.display_name,
                        column.data_type.value,
                        column.description,
                        "No"
                    ])
                
                # Write measures
                for measure in table.measures:
                    writer.writerow([
                        measure.name,
                        measure.display_name,
                        "measure",
                        measure.description,
                        "Yes"
                    ])
            
            exported_files[table_name] = csv_path
            logger.info(f"Exported table to CSV: {csv_path}")
        
        return exported_files
    
    @staticmethod
    def export_to_power_bi_template(semantic_model, template_path: str = "power_bi_template.json") -> None:
        """Export semantic model as Power BI template.
        
        Creates a template that can be imported into Power BI Desktop.
        """
        template = {
            "name": semantic_model.name,
            "displayName": semantic_model.display_name,
            "version": "1.0",
            "createdDate": datetime.now().isoformat(),
            "tables": [],
            "measures": [],
            "relationships": []
        }
        
        # Add tables
        for table_name, table in semantic_model.tables.items():
            table_def = {
                "name": table_name,
                "displayName": table.display_name,
                "columns": [c.to_dict() for c in table.columns],
                "measures": [m.to_dict() for m in table.measures],
                "hierarchies": [h.to_dict() for h in table.hierarchies]
            }
            template["tables"].append(table_def)
        
        # Add relationships
        for rel in semantic_model.relationships:
            rel_def = {
                "fromTable": rel.from_table,
                "fromColumn": rel.from_column,
                "toTable": rel.to_table,
                "toColumn": rel.to_column,
                "cardinality": rel.cardinality
            }
            template["relationships"].append(rel_def)
        
        with open(template_path, 'w') as f:
            json.dump(template, f, indent=2)
        
        logger.info(f"Exported Power BI template: {template_path}")


class PowerBIDashboardBuilder:
    """Builder class for creating Power BI dashboards from semantic models."""
    
    def __init__(self, semantic_model):
        """Initialize dashboard builder.
        
        Args:
            semantic_model: SemanticModel instance
        """
        self.semantic_model = semantic_model
        self.dashboard = None
    
    def create_dashboard(self, name: str, display_name: str, description: str) -> PowerBIDashboard:
        """Create new dashboard."""
        self.dashboard = PowerBIDashboard(
            name=name,
            display_name=display_name,
            description=description
        )
        return self.dashboard
    
    def add_kpi_card(self, measure_name: str, measure_display: str, 
                     target: Optional[float] = None) -> PowerBIVisualization:
        """Add KPI card visualization."""
        viz = PowerBIVisualization(
            name=f"kpi_{measure_name}",
            title=measure_display,
            visualization_type=VisualizationType.KPI,
            measures=[PowerBIField(measure_name, measure_display, "measure")]
        )
        if self.dashboard:
            self.dashboard.add_visualization(viz)
        return viz
    
    def add_bar_chart(self, category: str, measure: str, title: str,
                     table_name: str) -> PowerBIVisualization:
        """Add bar chart visualization."""
        viz = PowerBIVisualization(
            name=f"bar_{measure}_{category}",
            title=title,
            visualization_type=VisualizationType.BAR_CHART,
            x_axis=PowerBIField(category, category, "dimension"),
            y_axis=PowerBIField(measure, measure, "measure"),
            measures=[PowerBIField(measure, measure, "measure")],
            dimensions=[PowerBIField(category, category, "dimension")]
        )
        if self.dashboard:
            self.dashboard.add_visualization(viz)
        return viz
    
    def add_line_chart(self, time_dimension: str, measure: str, title: str) -> PowerBIVisualization:
        """Add line chart visualization for time series."""
        viz = PowerBIVisualization(
            name=f"line_{measure}_{time_dimension}",
            title=title,
            visualization_type=VisualizationType.LINE_CHART,
            x_axis=PowerBIField(time_dimension, time_dimension, "date"),
            y_axis=PowerBIField(measure, measure, "measure"),
            measures=[PowerBIField(measure, measure, "measure")],
            dimensions=[PowerBIField(time_dimension, time_dimension, "date")]
        )
        if self.dashboard:
            self.dashboard.add_visualization(viz)
        return viz
    
    def add_pie_chart(self, dimension: str, measure: str, title: str) -> PowerBIVisualization:
        """Add pie chart visualization."""
        viz = PowerBIVisualization(
            name=f"pie_{measure}_{dimension}",
            title=title,
            visualization_type=VisualizationType.PIE_CHART,
            measures=[PowerBIField(measure, measure, "measure")],
            dimensions=[PowerBIField(dimension, dimension, "dimension")]
        )
        if self.dashboard:
            self.dashboard.add_visualization(viz)
        return viz
    
    def add_table(self, columns: List[str], title: str) -> PowerBIVisualization:
        """Add table visualization."""
        fields = [PowerBIField(col, col, "dimension") for col in columns]
        viz = PowerBIVisualization(
            name=f"table_{title.replace(' ', '_')}",
            title=title,
            visualization_type=VisualizationType.TABLE,
            dimensions=fields
        )
        if self.dashboard:
            self.dashboard.add_visualization(viz)
        return viz
    
    def add_matrix(self, rows: List[str], columns: List[str], 
                   values: List[str], title: str) -> PowerBIVisualization:
        """Add matrix visualization."""
        row_fields = [PowerBIField(r, r, "dimension") for r in rows]
        col_fields = [PowerBIField(c, c, "dimension") for c in columns]
        val_fields = [PowerBIField(v, v, "measure") for v in values]
        
        viz = PowerBIVisualization(
            name=f"matrix_{title.replace(' ', '_')}",
            title=title,
            visualization_type=VisualizationType.MATRIX,
            dimensions=row_fields + col_fields,
            measures=val_fields
        )
        if self.dashboard:
            self.dashboard.add_visualization(viz)
        return viz
    
    def build(self) -> PowerBIDashboard:
        """Return the built dashboard."""
        return self.dashboard
