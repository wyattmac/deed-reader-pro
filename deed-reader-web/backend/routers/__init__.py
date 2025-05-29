"""
FastAPI Routers for Deed Reader Pro
"""

from .documents import router as documents_router
from .analysis import router as analysis_router

__all__ = ['documents_router', 'analysis_router'] 