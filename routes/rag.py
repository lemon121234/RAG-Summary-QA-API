"""
RAG 問答路由
處理檢索增強生成的問答功能
"""
from fastapi import APIRouter, HTTPException

from models import RAGQueryRequest, RAGQueryResponse
from vectorstore import vector_store
from retriever import search_similar_chunks
from llm import rag_qa
from utils.debug_logger import rag_debug_logger

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
    
    # 搜索相關片段（增加 top_k 以確保檢索到更多相關內容）
    search_top_k = max(request.top_k * 2, 10)  # 檢索更多片段，然後過濾
    results = await search_similar_chunks(request.question, search_top_k)
    
    # 記錄檢索過程（Debug）
    rag_debug_logger.log_retrieval(
        query=request.question,
        retrieved_chunks=results,
        top_k=request.top_k
    )
    
    # 準備來源信息（優先顯示包含關鍵詞的結果）
    sources = []
    seen_docs = {}  # 記錄每個文檔已顯示的片段數
    
    # 提取查詢關鍵詞（中文和英文）
    import re
    query_text = request.question
    # 提取中文詞（2個字符以上）
    chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', query_text)
    # 提取英文詞
    english_words = re.findall(r'[a-zA-Z]{3,}', query_text)
    all_keywords = chinese_words + [w.lower() for w in english_words]
    
    # 分兩輪：第一輪優先選擇包含關鍵詞的，第二輪填充剩餘
    keyword_results = []
    other_results = []
    
    for r in results:
        content = r["content"]
        content_lower = content.lower()
        
        # 檢查是否包含關鍵詞
        has_keyword = any(kw in content or kw.lower() in content_lower for kw in all_keywords if len(kw) > 1)
        
        item = {
            "document_title": r["title"],
            "content": content[:200] + "..." if len(content) > 200 else content,
            "relevance_score": round(r["score"], 3),
            "has_keyword": has_keyword,
            "score": r["score"]
        }
        
        if has_keyword:
            keyword_results.append(item)
        else:
            other_results.append(item)
    
    # 先添加包含關鍵詞的結果，再添加其他結果
    final_results = sorted(keyword_results, key=lambda x: x["score"], reverse=True) + \
                   sorted(other_results, key=lambda x: x["score"], reverse=True)
    
    # 限制每個文檔最多顯示 2 個片段
    for item in final_results:
        doc_title = item["document_title"]
        doc_count = seen_docs.get(doc_title, 0)
        
        if doc_count < 2 and len(sources) < request.top_k:
            sources.append({
                "document_title": item["document_title"],
                "content": item["content"],
                "relevance_score": item["relevance_score"]
            })
            seen_docs[doc_title] = doc_count + 1
    
    # 執行 RAG 問答
    answer, confidence = await rag_qa(request.question, results, request.language)
    
    # 記錄完整的 RAG 會話（Debug）
    rag_debug_logger.log_full_rag_session(
        question=request.question,
        retrieved_chunks=results,
        answer=answer,
        confidence=confidence,
        top_k=request.top_k
    )
    
    return RAGQueryResponse(
        question=request.question,
        answer=answer,
        sources=sources,
        confidence=confidence
    )

