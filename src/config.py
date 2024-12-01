import os
from dataclasses import dataclass

@dataclass
class Config:
    # Default configuration
    HOST: str = "0.0.0.0"  # Listen on all interfaces
    PORT: int = 5000
    BASE_URL: str = None  # Will be set based on environment
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-this"
    DB_PATH: str = "pytiny.db"

    @classmethod
    def load(cls):
        """Load configuration from environment variables."""
        config = cls()
        
        # Override with environment variables if set
        if os.getenv("PYTINY_HOST"):
            config.HOST = os.getenv("PYTINY_HOST")
        
        if os.getenv("PYTINY_PORT"):
            config.PORT = int(os.getenv("PYTINY_PORT"))
            
        if os.getenv("PYTINY_BASE_URL"):
            config.BASE_URL = os.getenv("PYTINY_BASE_URL")
            
        if os.getenv("PYTINY_DEBUG"):
            config.DEBUG = os.getenv("PYTINY_DEBUG").lower() == "true"
            
        if os.getenv("PYTINY_SECRET_KEY"):
            config.SECRET_KEY = os.getenv("PYTINY_SECRET_KEY")
            
        if os.getenv("PYTINY_DB_PATH"):
            config.DB_PATH = os.getenv("PYTINY_DB_PATH")
            
        return config
