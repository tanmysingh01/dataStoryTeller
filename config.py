"""
Configuration module for Microsoft Fabric workspace connection.
Handles environment variables and configuration settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class FabricConfig:
    """Configuration class for Fabric workspace settings."""
    
    # Authentication Configuration
    TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
    CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
    USERNAME = os.getenv("FABRIC_USERNAME", "")
    PASSWORD = os.getenv("FABRIC_PASSWORD", "")
    
    # Fabric Configuration
    WORKSPACE_NAME = os.getenv("FABRIC_WORKSPACE_NAME", "")
    WORKSPACE_ID = os.getenv("FABRIC_WORKSPACE_ID", "")
    CAPACITY_ID = os.getenv("FABRIC_CAPACITY_ID", "")
    
    # API Configuration
    FABRIC_API_URL = os.getenv("FABRIC_API_URL", "https://api.fabric.microsoft.com")
    POWER_BI_API_URL = os.getenv("POWER_BI_API_URL", "https://api.powerbi.com/v1.0/myorg")
    
    # Authentication Method ('service_principal' or 'user')
    AUTH_METHOD = os.getenv("AUTH_METHOD", "service_principal")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Validate required configuration settings."""
        if cls.AUTH_METHOD == "service_principal":
            required_fields = ["TENANT_ID", "CLIENT_ID", "CLIENT_SECRET"]
        else:
            required_fields = ["USERNAME", "PASSWORD"]
        
        missing_fields = [field for field in required_fields if not getattr(cls, field)]
        if missing_fields:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing_fields)}. "
                f"Please set these in your .env file."
            )
