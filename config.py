"""
配置模組
存放所有系統配置
"""
import os

# Ollama 配置
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# 文本處理配置
CHUNK_SIZE = 500  # 每個文檔片段的字數
CHUNK_OVERLAP = 50  # 片段重疊字數
TOP_K = 5  # 檢索返回的片段數量

