from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.api.v1.api import api_router
from app.db.session import init_db
from app.core.exceptions import setup_exception_handlers
from app.utils.logger import setup_logging


# Setup logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info("Starting Document Compliance System...")
    
    # Initialize database
    await init_db()
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_PATH, exist_ok=True)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Document Compliance System...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.ENVIRONMENT == "development" else settings.BACKEND_CORS_ORIGINS
)

# Setup exception handlers
setup_exception_handlers(app)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files for uploads
if settings.ENVIRONMENT == "development":
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_PATH), name="uploads")

# Setup Prometheus metrics
if settings.ENVIRONMENT == "production":
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
