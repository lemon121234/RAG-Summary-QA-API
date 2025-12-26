"""
數據模型模組
定義所有 API 的請求/回應模型
"""
from pydantic import BaseModel, Field
from typing import List, Dict

# ============ 文檔管理 ============

class DocumentUploadRequest(BaseModel):
    content: str = Field(..., description="文檔內容", min_length=10)
    title: str = Field(default="未命名文檔", description="文檔標題")


class DocumentResponse(BaseModel):
    document_id: str
    title: str
    content_length: int
    chunks_count: int
    created_at: str


# ============ RAG 問答 ============

class RAGQueryRequest(BaseModel):
    question: str = Field(..., description="要回答的問題", min_length=3)
    top_k: int = Field(default=5, description="檢索片段數量", ge=1, le=20)
    language: str = Field(default="zh-TW", description="輸出語言")


class RAGQueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict]
    confidence: str


# ============ 摘要 ============

class SummaryRequest(BaseModel):
    document_id: str = Field(..., description="文檔 ID")
    max_length: int = Field(default=200, description="摘要最大長度", ge=10, le=1000)
    language: str = Field(default="zh-TW", description="輸出語言")


# ============ URL 摘要 ============

class URLSummaryRequest(BaseModel):
    url: List[str] = Field(..., description="要摘要的網址（可傳多個）", min_length=1)
    max_length: int = Field(default=200, description="摘要最大長度", ge=10, le=1000)
    language: str = Field(default="zh-TW", description="輸出語言")


# ============ URL 問答 ============

class URLQARequest(BaseModel):
    url: str = Field(..., description="要問答的網址", min_length=5)
    question: str = Field(..., description="要回答的問題", min_length=3)
    language: str = Field(default="zh-TW", description="輸出語言")


class URLQAResponse(BaseModel):
    url: str
    question: str
    answer: str
    title: str




