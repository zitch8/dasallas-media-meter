import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Application configuration."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

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