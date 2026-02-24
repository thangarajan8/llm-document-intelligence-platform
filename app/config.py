"""
Configuration module for the application.
"""

from typing import Dict, Any
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # LLM Settings
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    
    # Embedding Settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))
    
    # Chunking Settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval Settings
    TOP_K = int(os.getenv("TOP_K", "5"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # Vector Store Settings
    VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "chroma")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./data/vector_store")
    
    # Paths
    DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
    LOGS_DIR = Path(os.getenv("LOGS_DIR", "./logs"))
    SAMPLE_DOCS_DIR = DATA_DIR / "sample_docs"
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """
        Convert config to dictionary.
        
        Returns:
            Configuration as dictionary
        """
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith("_") and key.isupper()
        }
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration.
        
        Returns:
            True if configuration is valid
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        # Create directories if they don't exist
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.SAMPLE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
        
        return True

