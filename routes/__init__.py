"""
路由模組
"""
from .documents import router as documents_router
from .rag import router as rag_router
from .summary import router as summary_router
from .url import router as url_router

__all__ = ["documents_router", "rag_router", "summary_router", "url_router"]




