# backend/app/core/config.py
"""Configuration settings for the backend."""
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings, loaded from environment variables."""
    # LLM API Keys
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Pinecone Vector DB
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = "gcp-starter"
    PINECONE_INDEX_NAME: Optional[str] = "research-index"
    
    # Optional Redis
    REDIS_URL: Optional[str] = None
    
    # App config
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
