"""
資料攝取層
負責文檔載入、文本切割、向量嵌入
"""
from .splitter import split_text
from .embedder import get_embedding, get_embeddings

__all__ = ["split_text", "get_embedding", "get_embeddings"]




