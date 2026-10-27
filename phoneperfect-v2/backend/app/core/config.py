from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "PhonePerfect 2.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "phoneperfect-v2-dev-secret-key-change-in-production-2026"
    
    # Database - Default to SQLite for seamless zero-setup testing, with PostgreSQL production support
    DATABASE_URL: str = "sqlite:///./phoneperfect_v2.db"
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_PASSWORD: Optional[str] = "postgres"
    POSTGRES_SERVER: Optional[str] = "localhost"
    POSTGRES_PORT: Optional[str] = "5432"
    POSTGRES_DB: Optional[str] = "phoneperfect_v2"

    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173", "*"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
