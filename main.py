"""
RAG 摘要與QA API
使用 FastAPI + Ollama 實現檢索增強生成（RAG）
支援多文檔上傳、向量檢索、智能問答
（輕量版 - 不需要額外安裝 chromadb 和 sentence-transformers）
"""
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import OLLAMA_BASE_URL, OLLAMA_MODEL, EMBEDDING_MODEL
from vectorstore import vector_store
from routes import documents_router, rag_router, summary_router, url_router

# ============ 初始化 FastAPI ============

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

# ============ 註冊路由 ============

app.include_router(documents_router)
app.include_router(rag_router)
app.include_router(summary_router)
app.include_router(url_router)

# ============ 根端點 ============

@app.get("/")
async def root():
    """API 根端點"""
    return {
        "message": "Welcome to RAG Summary & QA API",
        "version": "2.2.0",
        "features": [
            "RAG - Retrieval Augmented Generation",
            "Multi-document Knowledge Base",
            "Vector Semantic Search",
            "Smart Summarization",
            "URL Content Summarization",
            "URL Question Answering"
        ],
        "stats": {
            "documents": vector_store.count_documents(),
            "total_chunks": vector_store.count_chunks(),
            "embedding_model": EMBEDDING_MODEL,
            "llm_model": OLLAMA_MODEL
        },
        "endpoints": {
            "documents": "POST /api/documents",
            "rag_query": "POST /api/rag/query",
            "summary": "POST /api/summary",
            "url_summary": "POST /api/url/summary",
            "url_qa": "POST /api/url/qa",
            "docs": "/docs"
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


# ============ 啟動 ============

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("RAG Summary & QA API v2.2")
    print("=" * 60)
    print(f"LLM Model: {OLLAMA_MODEL}")
    print(f"Embedding Model: {EMBEDDING_MODEL}")
    print("=" * 60)
    print("Please ensure:")
    print(f"  1. Ollama is running: ollama serve")
    print(f"  2. LLM downloaded: ollama pull {OLLAMA_MODEL}")
    print(f"  3. Embedding model: ollama pull {EMBEDDING_MODEL}")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
