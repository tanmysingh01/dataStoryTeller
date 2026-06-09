"""
Microsoft Fabric workspace connection and authentication module.
Handles authentication and connection setup using Python SDK.
"""

import logging
from typing import Optional
from azure.identity import ClientSecretCredential, UsernamePasswordCredential
from fabric import FabricClient
from config import FabricConfig

# Configure logging
logging.basicConfig(level=FabricConfig.LOG_LEVEL)
logger = logging.getLogger(__name__)


class FabricConnection:
    """
    Manages connection to Microsoft Fabric workspace.
    Supports Service Principal and User authentication methods.
    """
    
    def __init__(self, auth_method: Optional[str] = None):
        """
        Initialize Fabric connection.
        
        Args:
            auth_method: Authentication method ('service_principal' or 'user').
                        If None, uses config setting.
        """
        FabricConfig.validate()
        self.auth_method = auth_method or FabricConfig.AUTH_METHOD
        self.credential = None
        self.client = None
        self.access_token = None
        
        logger.info(f"Initializing Fabric connection with {self.auth_method} authentication")
    
    def authenticate_service_principal(self) -> bool:
        """
        Authenticate using Service Principal (Azure AD).
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        try:
            self.credential = ClientSecretCredential(
                tenant_id=FabricConfig.TENANT_ID,
                client_id=FabricConfig.CLIENT_ID,
                client_secret=FabricConfig.CLIENT_SECRET
            )
            
            # Get access token for verification
            scope = ["https://api.fabric.microsoft.com/.default"]
            self.access_token = self.credential.get_token(*scope)
            
            logger.info("✓ Service Principal authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"✗ Service Principal authentication failed: {str(e)}")
            return False
    
    def authenticate_user(self) -> bool:
        """
        Authenticate using username and password.
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        try:
            self.credential = UsernamePasswordCredential(
                client_id=FabricConfig.CLIENT_ID or "04b07795-8ddb-461a-bbee-02f36b87f4b6",  # Default Power BI CLI client ID
                username=FabricConfig.USERNAME,
                password=FabricConfig.PASSWORD
            )
            
            # Get access token for verification
            scope = ["https://api.powerbi.com/.default"]
            self.access_token = self.credential.get_token(*scope)
            
            logger.info("✓ User authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"✗ User authentication failed: {str(e)}")
            return False
    
    def connect(self) -> bool:
        """
        Establish connection to Fabric workspace.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            # Perform authentication based on method
            if self.auth_method == "service_principal":
                if not self.authenticate_service_principal():
                    return False
            elif self.auth_method == "user":
                if not self.authenticate_user():
                    return False
            else:
                logger.error(f"Unknown authentication method: {self.auth_method}")
                return False
            
            # Initialize Fabric client
            self.client = FabricClient(
                credential=self.credential,
                workspace_id=FabricConfig.WORKSPACE_ID
            )
            
            logger.info("✓ Fabric workspace connection established")
            return True
            
        except Exception as e:
            logger.error(f"✗ Connection to Fabric workspace failed: {str(e)}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connection is established."""
        return self.client is not None
    
    def get_client(self) -> Optional[FabricClient]:
        """
        Get the Fabric client instance.
        
        Returns:
            FabricClient: The Fabric client if connected, None otherwise.
        """
        if not self.is_connected():
            logger.warning("Not connected to Fabric workspace")
            return None
        return self.client
    
    def get_credential(self):
        """Get the credential object for API calls."""
        return self.credential
    
    def close(self):
        """Close the connection."""
        self.client = None
        self.credential = None
        logger.info("Fabric connection closed")


class FabricSessionManager:
    """Context manager for Fabric connections."""
    
    def __init__(self, auth_method: Optional[str] = None):
        """Initialize session manager."""
        self.connection = FabricConnection(auth_method)
    
    def __enter__(self):
        """Enter context manager."""
        if self.connection.connect():
            return self.connection
        else:
            raise ConnectionError("Failed to establish Fabric connection")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.connection.close()
        return False
