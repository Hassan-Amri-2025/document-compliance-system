"""
Application configuration with open-source alternatives
No Azure dependencies required
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Document Compliance System"
    APP_VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Security
    SECRET_KEY: str = "your-very-secret-key-here-minimum-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    DB_USER: str = "docadmin"
    DB_PASSWORD: str = "change-this-password"
    DB_NAME: str = "document_compliance"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    
    # Constructed database URL
    DATABASE_URL: Optional[str] = None
    
    @validator("DATABASE_URL", pre=True)
    def construct_db_url(cls, v, values):
        if v:
            return v
        user = values.get("DB_USER")
        password = values.get("DB_PASSWORD")
        host = values.get("DB_HOST")
        port = values.get("DB_PORT")
        name = values.get("DB_NAME")
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None
    
    # File Storage Configuration (Local instead of Azure)
    STORAGE_TYPE: str = "local"  # Options: "local", "s3", "gcs"
    LOCAL_STORAGE_PATH: str = "./uploads"
    TEMPLATES_PATH: str = "./uploads/templates"
    DOCUMENTS_PATH: str = "./uploads/documents"
    CERTIFIED_PATH: str = "./uploads/certified"
    REPORTS_PATH: str = "./uploads/reports"
    VISUALIZATIONS_PATH: str = "./uploads/visualizations"
    TEMP_PATH: str = "./uploads/temp"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB in bytes
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "doc", "docx", "tex", "png", "jpg", "jpeg"]
    UPLOAD_PATH: str = "uploads"
    
    # Document Processing Configuration
    OCR_ENGINE: str = "tesseract"  # Options: "tesseract", "easyocr"
    OCR_LANGUAGES: List[str] = ["eng", "ara"]  # English and Arabic
    LAYOUT_MODEL: str = "lp://EfficientDete/PubLayNet"
    
    # Template Processing
    TEMPLATE_CACHE_TTL: int = 3600  # 1 hour
    MAX_CONCURRENT_VALIDATIONS: int = 10
    
    # Validation Settings
    DEFAULT_SIMILARITY_THRESHOLD: float = 0.85
    SSIM_WEIGHT: float = 0.4
    PERCEPTUAL_HASH_WEIGHT: float = 0.3
    LAYOUT_MATCH_WEIGHT: float = 0.3
    
    # Email Configuration (Optional)
    SMTP_HOST: Optional[str] = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Frontend URL (for QR codes and links)
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Performance Settings
    WORKER_CONNECTIONS: int = 4
    WORKER_TIMEOUT: int = 300
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def create_directories(self):
        """Create necessary directories for file storage"""
        directories = [
            self.LOCAL_STORAGE_PATH,
            self.TEMPLATES_PATH,
            self.DOCUMENTS_PATH,
            self.CERTIFIED_PATH,
            self.REPORTS_PATH,
            self.VISUALIZATIONS_PATH,
            self.TEMP_PATH
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Create settings instance
settings = Settings()

# Create directories on startup
settings.create_directories()
