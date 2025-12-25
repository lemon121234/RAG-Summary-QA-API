"""
RAG 問答路由
處理檢索增強生成的問答功能
"""
from fastapi import APIRouter, HTTPException

from models import RAGQueryRequest, RAGQueryResponse
from vectorstore import vector_store
from retriever import search_similar_chunks
from llm import rag_qa

router = APIRouter(prefix="/api/rag", tags=["RAG 問答"])


@router.post("/query", response_model=RAGQueryResponse)
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
    
    # 搜索相關片段
    results = await search_similar_chunks(request.question, request.top_k)
    
    # 準備來源信息
    sources = []
    for r in results:
        sources.append({
            "document_title": r["title"],
            "content": r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"],
            "relevance_score": round(r["score"], 3)
        })
    
    # 執行 RAG 問答
    answer, confidence = await rag_qa(request.question, results, request.language)
    
    return RAGQueryResponse(
        question=request.question,
        answer=answer,
        sources=sources,
        confidence=confidence
    )

