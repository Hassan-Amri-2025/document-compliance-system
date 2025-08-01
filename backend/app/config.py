from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Optional, List
import os
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Document Compliance System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    DEBUG: bool = Field(True, env="DEBUG")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DB_ECHO: bool = Field(False, env="DB_ECHO")
    
    # Redis
    REDIS_URL: str = Field("redis://localhost:6379", env="REDIS_URL")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Azure Document Intelligence
    AZURE_DOCUMENT_INTELLIGENCE_KEY: str = Field(..., env="AZURE_DOCUMENT_INTELLIGENCE_KEY")
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: str = Field(..., env="AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    
    # Azure Storage
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = Field(None, env="AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_CONTAINER: str = Field("templates", env="AZURE_STORAGE_CONTAINER")
    
    # File Upload
    MAX_UPLOAD_SIZE: int = Field(52428800, env="MAX_UPLOAD_SIZE")  # 50MB
    ALLOWED_EXTENSIONS: List[str] = Field(
        ["pdf", "doc", "docx", "tex", "png", "jpg", "jpeg"],
        env="ALLOWED_EXTENSIONS"
    )
    UPLOAD_PATH: str = Field("uploads", env="UPLOAD_PATH")
    
    # Template Processing
    TEMPLATE_CACHE_TTL: int = Field(3600, env="TEMPLATE_CACHE_TTL")
    MAX_CONCURRENT_VALIDATIONS: int = Field(10, env="MAX_CONCURRENT_VALIDATIONS")
    
    # Validation Settings
    DEFAULT_SIMILARITY_THRESHOLD: float = Field(0.85, env="DEFAULT_SIMILARITY_THRESHOLD")
    SSIM_WEIGHT: float = Field(0.4, env="SSIM_WEIGHT")
    PERCEPTUAL_HASH_WEIGHT: float = Field(0.3, env="PERCEPTUAL_HASH_WEIGHT")
    LAYOUT_MATCH_WEIGHT: float = Field(0.3, env="LAYOUT_MATCH_WEIGHT")
    
    # Email
    SMTP_HOST: Optional[str] = Field(None, env="SMTP_HOST")
    SMTP_PORT: Optional[int] = Field(None, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(None, env="SMTP_PASSWORD")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(
        ["http://localhost:3000", "http://localhost:8000"],
        env="BACKEND_CORS_ORIGINS"
    )
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def parse_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip().lower() for ext in v.split(",")]
        return v
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
