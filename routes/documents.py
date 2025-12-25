"""
文檔管理路由
處理文檔的上傳、查詢、刪除等操作
"""
from fastapi import APIRouter, HTTPException
import uuid

from models import DocumentUploadRequest, DocumentResponse
from vectorstore import vector_store
from ingest import split_text, get_embeddings

router = APIRouter(prefix="/api/documents", tags=["文檔管理"])


@router.post("", response_model=DocumentResponse)
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


@router.get("")
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


@router.get("/{document_id}")
async def get_document(document_id: str):
    """📄 獲取特定文檔"""
    if document_id not in vector_store.documents:
        raise HTTPException(status_code=404, detail=f"找不到文檔 ID: {document_id}")
    
    return vector_store.documents[document_id]


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """🗑️ 刪除文檔"""
    if not vector_store.delete_document(document_id):
        raise HTTPException(status_code=404, detail=f"找不到文檔 ID: {document_id}")
    
    return {"message": f"已成功刪除文檔 {document_id}"}


@router.delete("")
async def clear_all_documents():
    """🗑️ 清空所有文檔"""
    vector_store.clear()
    return {"message": "已清空所有文檔"}

