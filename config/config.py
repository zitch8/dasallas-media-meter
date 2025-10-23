import os
from pathlib import Path


class Config:
    """Application configuration."""
    
    # Database Configuration
    DB_TYPE = os.getenv('DB_TYPE', 'mongodb')
    
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DATABASE = os.getenv('MONGO_DB')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')
    
    @classmethod
    def get_database_config(cls):
        """Get database configuration"""
        return {
            'uri': cls.MONGO_URI,
            'db_name': cls.MONGO_DATABASE,
            'collection_name': cls.MONGO_COLLECTION
        }