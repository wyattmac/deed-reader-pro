#!/usr/bin/env python3
"""
Deed Reader Pro - FastAPI Backend
---------------------------------
Async REST API with Anthropic Claude integration for deed document processing.

Migration from Flask to FastAPI for better async support and performance.
"""

import os
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Import routers
from routers.documents import router as documents_router
from routers.analysis import router as analysis_router
# from routers.chat import router as chat_router
# from routers.plotting import router as plotting_router

# Import services
from services.claude_service import ClaudeService


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings for validation."""
    
    # Basic settings
    app_name: str = "Deed Reader Pro API"
    app_version: str = "2.0.0"
    environment: str = "development"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 5000
    
    # Security
    secret_key: str = os.getenv('SECRET_KEY', os.urandom(32).hex())
    allowed_hosts: list = ["*"]
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # File upload
    max_content_length: int = 50 * 1024 * 1024  # 50MB
    upload_folder: str = "uploads"
    allowed_extensions: set = {"txt", "pdf", "png", "jpg", "jpeg", "tiff", "bmp"}
    
    # AI Services
    anthropic_api_key: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    openai_api_key: Optional[str] = os.getenv('OPENAI_API_KEY')
    openai_model: str = "gpt-3.5-turbo"
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Database (for future PostgreSQL migration)
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Initialize settings
settings = Settings()

# Configure logging
def setup_logging():
    """Configure application logging."""
    handlers = [logging.StreamHandler()]
    
    if settings.log_file:
        handlers.append(logging.FileHandler(settings.log_file))
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=handlers
    )
    
    # Reduce noise from external libraries
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)


# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown tasks.
    """
    # Startup
    logger.info("=" * 50)
    logger.info("Starting Deed Reader Pro FastAPI Backend")
    logger.info("=" * 50)
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Ensure upload directory exists
    os.makedirs(settings.upload_folder, exist_ok=True)
    logger.info(f"Upload directory: {settings.upload_folder}")
    
    # Initialize Claude service
    if settings.anthropic_api_key:
        if ClaudeService.initialize(settings.anthropic_api_key):
            app.state.claude_enabled = True
            logger.info("Claude service initialized successfully")
        else:
            app.state.claude_enabled = False
            logger.warning("Claude service initialization failed")
    else:
        app.state.claude_enabled = False
        logger.warning("No Anthropic API key provided")
    
    logger.info("=" * 50)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Deed Reader Pro Backend")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered deed parsing and visualization API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts
    )


# Custom middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url} - IP: {request.client.host}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(
        f"Response: {response.status_code} - {process_time:.3f}s"
    )
    
    # Add custom headers
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-API-Version"] = settings.app_version
    
    return response


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Cache control for API responses
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    
    return response


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - redirects to API documentation."""
    return {
        "message": "Welcome to Deed Reader Pro API",
        "documentation": "/api/docs",
        "health": "/api/health",
        "version": settings.app_version
    }


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Comprehensive health check endpoint."""
    start_time = time.time()
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": settings.app_version,
        "environment": settings.environment,
        "services": {
            "api": "healthy",
            "claude": "healthy" if app.state.claude_enabled else "disabled",
            "storage": "healthy" if os.path.exists(settings.upload_folder) else "error"
        },
        "system": {
            "upload_folder_exists": os.path.exists(settings.upload_folder),
            "upload_folder_writable": os.access(settings.upload_folder, os.W_OK),
            "python_version": os.sys.version.split()[0],
            "max_content_length_mb": settings.max_content_length // (1024 * 1024)
        }
    }
    
    # Check overall health
    all_services_healthy = all(
        status in ["healthy", "disabled"] 
        for status in health_data["services"].values()
    )
    
    if not all_services_healthy:
        health_data["status"] = "degraded"
        raise HTTPException(status_code=503, detail=health_data)
    
    # Add response time
    health_data["response_time_ms"] = round((time.time() - start_time) * 1000, 2)
    
    return health_data


# API info endpoint
@app.get("/api/info")
async def api_info():
    """API information and available endpoints."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "REST API for deed document processing and analysis",
        "endpoints": {
            "health": "/api/health",
            "documents": "/api/documents",
            "analysis": "/api/analysis",
            "chat": "/api/chat",
            "plotting": "/api/plotting"
        },
        "features": {
            "file_upload": True,
            "ai_analysis": app.state.claude_enabled,
            "interactive_chat": app.state.claude_enabled,
            "coordinate_extraction": app.state.claude_enabled,
            "plotting": True,
            "ocr_vision": app.state.claude_enabled
        },
        "limits": {
            "max_file_size_mb": settings.max_content_length // (1024 * 1024),
            "allowed_file_types": list(settings.allowed_extensions)
        }
    }


# Include routers
app.include_router(documents_router, prefix="/api/documents", tags=["documents"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["analysis"])
# app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
# app.include_router(plotting_router, prefix="/api/plotting", tags=["plotting"])


# Exception handlers
@app.exception_handler(400)
async def bad_request_handler(request: Request, exc: HTTPException):
    """Handle bad request errors."""
    return JSONResponse(
        status_code=400,
        content={
            "error": "Bad Request",
            "message": str(exc.detail) if hasattr(exc, 'detail') else "The request was invalid or malformed",
            "status_code": 400,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle not found errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested resource {request.url.path} was not found",
            "status_code": 404,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "available_endpoints": ["/api/health", "/api/info", "/api/docs"]
        }
    )


@app.exception_handler(413)
async def request_entity_too_large_handler(request: Request, exc: HTTPException):
    """Handle payload too large errors."""
    max_size_mb = settings.max_content_length // (1024 * 1024)
    return JSONResponse(
        status_code=413,
        content={
            "error": "Payload Too Large",
            "message": f"File size exceeds the maximum allowed size of {max_size_mb}MB",
            "status_code": 413,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    """Handle internal server errors."""
    error_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    logger.error(f"Internal server error [{error_id}]: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": f"An unexpected error occurred. Error ID: {error_id}",
            "error_id": error_id,
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


if __name__ == "__main__":
    """Run the application using uvicorn."""
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 