"""
相似度搜尋模組
在向量資料庫中搜索相關內容
"""
from typing import List
from vectorstore import vector_store
from ingest import get_embedding


async def search_similar_chunks(query: str, top_k: int = 5) -> List[dict]:
    """
    搜索與查詢相關的文本片段
    
    Args:
        query: 查詢文本
        top_k: 返回最相關的 k 個結果
    
    Returns:
        相關片段列表，包含相似度分數
    """
    # 獲取查詢向量
    query_embedding = await get_embedding(query)
    
    # 在向量資料庫中搜索
    results = vector_store.search(query_embedding, top_k)
    
    return results




