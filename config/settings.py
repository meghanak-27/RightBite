# config/settings.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # General
    APP_NAME: str = "Agentic Food Ordering AI"
    DEBUG: bool = True
    ENV: str = "development"

    # LangGraph / LLM
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LLM_MODEL: str = "gemini-1.5-flash"  # Corrected for current Gemini naming
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000

    # Database
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017/foodbot")

    # Logging
    LOG_LEVEL: str = "INFO"

    # Pydantic v2 Configuration
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()