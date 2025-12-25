"""
摘要路由
處理文檔摘要功能
"""
from fastapi import APIRouter, HTTPException

from models import SummaryRequest
from vectorstore import vector_store
from llm import generate_summary

router = APIRouter(prefix="/api/summary", tags=["摘要"])


@router.post("")
async def create_summary(request: SummaryRequest):
    """
    📝 生成文檔摘要
    """
    if request.document_id not in vector_store.documents:
        raise HTTPException(status_code=404, detail=f"找不到文檔 ID: {request.document_id}")
    
    doc = vector_store.documents[request.document_id]
    text = doc["content"]
    
    summary = await generate_summary(text, request.max_length, request.language)
    
    return {
        "document_id": request.document_id,
        "title": doc["title"],
        "original_length": len(text),
        "summary": summary,
        "summary_length": len(summary)
    }

