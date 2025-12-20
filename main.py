"""
RAG 摘要與QA API
使用 FastAPI + Ollama 實現檢索增強生成（RAG）
支援多文檔上傳、向量檢索、智能問答
（輕量版 - 不需要額外安裝 chromadb 和 sentence-transformers）
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import httpx
import os
import uuid
from datetime import datetime
import json
import math
import re

# ============ 配置 ============

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")  # Ollama 嵌入模型
CHUNK_SIZE = 500  # 每個文檔片段的字數
CHUNK_OVERLAP = 50  # 片段重疊字數
TOP_K = 5  # 檢索返回的片段數量

# ============ 初始化 ============

app = FastAPI(
    title="RAG 摘要與QA API",
    description="使用 RAG（檢索增強生成）技術的智能問答系統，支援多文檔上傳和向量檢索",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 內存向量資料庫 ============

class VectorStore:
    """簡易向量資料庫"""
    
    def __init__(self):
        self.documents: Dict[str, dict] = {}  # 文檔元數據
        self.chunks: List[dict] = []  # 所有片段
        self.embeddings: List[List[float]] = []  # 對應的向量
    
    def add_document(self, doc_id: str, title: str, content: str, chunks: List[str], embeddings: List[List[float]]):
        """添加文檔"""
        self.documents[doc_id] = {
            "id": doc_id,
            "title": title,
            "content": content,
            "content_length": len(content),
            "chunks_count": len(chunks),
            "created_at": datetime.now().isoformat()
        }
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            self.chunks.append({
                "id": f"{doc_id}_{i}",
                "document_id": doc_id,
                "title": title,
                "content": chunk,
                "chunk_index": i
            })
            self.embeddings.append(embedding)
    
    def delete_document(self, doc_id: str):
        """刪除文檔"""
        if doc_id not in self.documents:
            return False
        
        # 找出要刪除的片段索引
        indices_to_remove = [i for i, c in enumerate(self.chunks) if c["document_id"] == doc_id]
        
        # 從後往前刪除
        for i in reversed(indices_to_remove):
            del self.chunks[i]
            del self.embeddings[i]
        
        del self.documents[doc_id]
        return True
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[dict]:
        """向量相似度搜索"""
        if not self.embeddings:
            return []
        
        # 計算餘弦相似度
        scores = []
        for i, emb in enumerate(self.embeddings):
            score = self._cosine_similarity(query_embedding, emb)
            scores.append((i, score))
        
        # 排序並返回 top_k
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for i, score in scores[:top_k]:
            chunk = self.chunks[i].copy()
            chunk["score"] = score
            results.append(chunk)
        
        return results
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """計算餘弦相似度"""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)
    
    def clear(self):
        """清空所有數據"""
        self.documents.clear()
        self.chunks.clear()
        self.embeddings.clear()
    
    def count_chunks(self) -> int:
        return len(self.chunks)
    
    def count_documents(self) -> int:
        return len(self.documents)


# 初始化向量存儲
vector_store = VectorStore()


# ============ 工具函數 ============

def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """將文本分割成小塊"""
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += ("\n\n" + para if current_chunk else para)
        else:
            if current_chunk:
                chunks.append(current_chunk)
            
            if len(para) > chunk_size:
                sentences = re.split(r'(?<=[。！？.!?])\s*', para)
                current_chunk = ""
                for sent in sentences:
                    if len(current_chunk) + len(sent) <= chunk_size:
                        current_chunk += sent
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = sent
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # 如果沒有分割成功，至少返回原文
    if not chunks and text.strip():
        chunks = [text.strip()]
    
    return chunks


async def get_embedding(text: str) -> List[float]:
    """使用 Ollama 獲取文本嵌入向量"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                json={
                    "model": EMBEDDING_MODEL,
                    "prompt": text
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"嵌入生成失敗: {response.text}"
                )
            
            result = response.json()
            return result.get("embedding", [])
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"無法連接到 Ollama。請確認已啟動並下載嵌入模型: ollama pull {EMBEDDING_MODEL}"
        )


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """批量獲取嵌入向量"""
    embeddings = []
    for text in texts:
        emb = await get_embedding(text)
        embeddings.append(emb)
    return embeddings


async def call_ollama(prompt: str, system_prompt: str = "") -> str:
    """調用 Ollama LLM"""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Ollama 請求失敗: {response.text}")
            
            result = response.json()
            return result.get("response", "").strip()
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="無法連接到 Ollama。請執行 'ollama serve'"
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama 回應超時")


# ============ 請求/回應模型 ============

class DocumentUploadRequest(BaseModel):
    content: str = Field(..., description="文檔內容", min_length=10)
    title: str = Field(default="未命名文檔", description="文檔標題")


class RAGQueryRequest(BaseModel):
    question: str = Field(..., description="要回答的問題", min_length=3)
    top_k: int = Field(default=5, description="檢索片段數量", ge=1, le=20)
    language: str = Field(default="zh-TW", description="輸出語言")


class SummaryRequest(BaseModel):
    document_id: str = Field(..., description="文檔 ID")
    max_length: int = Field(default=200, description="摘要最大長度", ge=10, le=1000)
    language: str = Field(default="zh-TW", description="輸出語言")


class DocumentResponse(BaseModel):
    document_id: str
    title: str
    content_length: int
    chunks_count: int
    created_at: str


class RAGQueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[dict]
    confidence: str


# ============ API 端點 ============

@app.get("/")
async def root():
    """API 根端點"""
    return {
        "message": "🚀 歡迎使用 RAG 摘要與QA API",
        "version": "2.0.0",
        "features": [
            "📚 RAG 檢索增強生成",
            "🔍 多文檔知識庫",
            "🎯 向量語義搜索",
            "📝 智能摘要生成"
        ],
        "stats": {
            "documents": vector_store.count_documents(),
            "total_chunks": vector_store.count_chunks(),
            "embedding_model": EMBEDDING_MODEL,
            "llm_model": OLLAMA_MODEL
        },
        "endpoints": {
            "上傳文檔": "POST /api/documents",
            "列出文檔": "GET /api/documents",
            "RAG 問答": "POST /api/rag/query",
            "語義搜索": "POST /api/rag/search",
            "生成摘要": "POST /api/summary",
            "API 文檔": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """健康檢查"""
    ollama_status = "unknown"
    embedding_status = "unknown"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # 檢查 Ollama
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if response.status_code == 200:
                ollama_status = "healthy"
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                
                # 檢查嵌入模型是否存在
                if any(EMBEDDING_MODEL in name for name in model_names):
                    embedding_status = "ready"
                else:
                    embedding_status = f"missing - 請執行: ollama pull {EMBEDDING_MODEL}"
            else:
                ollama_status = "error"
    except Exception:
        ollama_status = "unreachable"
    
    return {
        "status": "healthy",
        "ollama_status": ollama_status,
        "embedding_status": embedding_status,
        "llm_model": OLLAMA_MODEL,
        "embedding_model": EMBEDDING_MODEL,
        "documents_count": vector_store.count_documents(),
        "chunks_count": vector_store.count_chunks()
    }


# ============ 文檔管理 ============

@app.post("/api/documents", response_model=DocumentResponse)
async def upload_document(request: DocumentUploadRequest):
    """
    📤 上傳文檔到知識庫
    
    文檔會被自動分割並建立向量索引，用於後續的 RAG 問答。
    """
    document_id = str(uuid.uuid4())[:8]
    
    # 分割文檔
    chunks = split_text(request.content)
    
    if not chunks:
        raise HTTPException(status_code=400, detail="文檔內容太短")
    
    # 生成嵌入向量
    print(f"正在為 {len(chunks)} 個片段生成嵌入向量...")
    embeddings = await get_embeddings(chunks)
    
    # 存入向量資料庫
    vector_store.add_document(
        doc_id=document_id,
        title=request.title,
        content=request.content,
        chunks=chunks,
        embeddings=embeddings
    )
    
    doc = vector_store.documents[document_id]
    
    return DocumentResponse(
        document_id=document_id,
        title=request.title,
        content_length=doc["content_length"],
        chunks_count=doc["chunks_count"],
        created_at=doc["created_at"]
    )


@app.get("/api/documents")
async def list_documents():
    """📋 列出所有文檔"""
    documents = []
    for doc_id, doc in vector_store.documents.items():
        documents.append({
            "document_id": doc_id,
            "title": doc["title"],
            "content_length": doc["content_length"],
            "chunks_count": doc["chunks_count"],
            "created_at": doc["created_at"],
            "preview": doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"]
        })
    
    return {
        "total": len(documents),
        "total_chunks": vector_store.count_chunks(),
        "documents": documents
    }


@app.get("/api/documents/{document_id}")
async def get_document(document_id: str):
    """📄 獲取特定文檔"""
    if document_id not in vector_store.documents:
        raise HTTPException(status_code=404, detail=f"找不到文檔 ID: {document_id}")
    
    return vector_store.documents[document_id]


@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    """🗑️ 刪除文檔"""
    if not vector_store.delete_document(document_id):
        raise HTTPException(status_code=404, detail=f"找不到文檔 ID: {document_id}")
    
    return {"message": f"已成功刪除文檔 {document_id}"}


@app.delete("/api/documents")
async def clear_all_documents():
    """🗑️ 清空所有文檔"""
    vector_store.clear()
    return {"message": "已清空所有文檔"}


# ============ RAG 功能 ============

@app.post("/api/rag/search")
async def semantic_search(request: RAGQueryRequest):
    """
    🔍 語義搜索
    
    在知識庫中搜索與問題最相關的文檔片段。
    """
    if vector_store.count_chunks() == 0:
        raise HTTPException(status_code=400, detail="知識庫為空，請先上傳文檔")
    
    # 獲取問題的嵌入向量
    query_embedding = await get_embedding(request.question)
    
    # 搜索
    results = vector_store.search(query_embedding, request.top_k)
    
    return {
        "question": request.question,
        "results_count": len(results),
        "sources": [
            {
                "document_title": r["title"],
                "content": r["content"],
                "relevance_score": round(r["score"], 3)
            }
            for r in results
        ]
    }


@app.post("/api/rag/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    """
    🤖 RAG 問答
    
    使用檢索增強生成（RAG）技術回答問題：
    1. 在知識庫中搜索相關片段
    2. 將片段作為上下文傳給 LLM
    3. LLM 根據上下文生成答案
    """
    if vector_store.count_chunks() == 0:
        raise HTTPException(status_code=400, detail="知識庫為空，請先上傳文檔")
    
    # 獲取問題嵌入
    query_embedding = await get_embedding(request.question)
    
    # 搜索相關片段
    results = vector_store.search(query_embedding, request.top_k)
    
    # 組合上下文
    context_parts = []
    sources = []
    for r in results:
        context_parts.append(f"[來源: {r['title']}]\n{r['content']}")
        sources.append({
            "document_title": r["title"],
            "content": r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"],
            "relevance_score": round(r["score"], 3)
        })
    
    context = "\n\n---\n\n".join(context_parts)
    
    # 語言設定
    language_map = {
        "zh-TW": "繁體中文",
        "zh-CN": "简体中文",
        "en": "English"
    }
    target_lang = language_map.get(request.language, "繁體中文")
    
    # 構建提示詞
    system_prompt = """你是一個專業的問答助手。請根據提供的參考資料回答問題。
規則：
1. 只根據參考資料中的信息回答
2. 如果資料中沒有相關信息，請明確說明
3. 回答要準確、有條理
4. 適當引用來源"""
    
    prompt = f"""請根據以下參考資料回答問題。

## 參考資料
{context}

## 問題
{request.question}

請用{target_lang}回答。"""
    
    # 調用 LLM
    answer = await call_ollama(prompt, system_prompt)
    
    # 計算信心程度
    if results:
        avg_score = sum(r["score"] for r in results) / len(results)
        if avg_score > 0.7:
            confidence = "high"
        elif avg_score > 0.5:
            confidence = "medium"
        else:
            confidence = "low"
    else:
        confidence = "low"
    
    return RAGQueryResponse(
        question=request.question,
        answer=answer,
        sources=sources,
        confidence=confidence
    )


# ============ 摘要功能 ============

@app.post("/api/summary")
async def create_summary(request: SummaryRequest):
    """
    📝 生成文檔摘要
    """
    if request.document_id not in vector_store.documents:
        raise HTTPException(status_code=404, detail=f"找不到文檔 ID: {request.document_id}")
    
    doc = vector_store.documents[request.document_id]
    text = doc["content"]
    
    language_map = {
        "zh-TW": "繁體中文",
        "zh-CN": "简体中文",
        "en": "English"
    }
    target_lang = language_map.get(request.language, "繁體中文")
    
    system_prompt = "你是一個專業的文本摘要助手。"
    
    prompt = f"""請為以下文本生成摘要。

要求：
1. 摘要不超過 {request.max_length} 字
2. 使用 {target_lang}
3. 保留關鍵信息

文本：
{text}

請直接輸出摘要。"""
    
    summary = await call_ollama(prompt, system_prompt)
    
    return {
        "document_id": request.document_id,
        "title": doc["title"],
        "original_length": len(text),
        "summary": summary,
        "summary_length": len(summary)
    }


# ============ 啟動 ============

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("RAG Summary & QA API v2.0")
    print("=" * 60)
    print(f"LLM Model: {OLLAMA_MODEL}")
    print(f"Embedding Model: {EMBEDDING_MODEL}")
    print(f"Chunk Size: {CHUNK_SIZE}")
    print(f"Top K: {TOP_K}")
    print("=" * 60)
    print("Please ensure:")
    print(f"  1. Ollama is running: ollama serve")
    print(f"  2. LLM downloaded: ollama pull {OLLAMA_MODEL}")
    print(f"  3. Embedding model: ollama pull {EMBEDDING_MODEL}")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
