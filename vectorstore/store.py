"""
向量資料庫實現
提供文檔存儲、向量搜索等功能
"""
from typing import List, Dict
from datetime import datetime
import math


class VectorStore:
    """簡易向量資料庫"""
    
    def __init__(self):
        self.documents: Dict[str, dict] = {}  # 文檔元數據
        self.chunks: List[dict] = []  # 所有片段
        self.embeddings: List[List[float]] = []  # 對應的向量
    
    def add_document(self, doc_id: str, title: str, content: str, chunks: List[str], embeddings: List[List[float]]):
        """
        添加文檔到向量資料庫
        
        Args:
            doc_id: 文檔 ID
            title: 文檔標題
            content: 文檔內容
            chunks: 文本片段列表
            embeddings: 對應的嵌入向量列表
        """
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
    
    def delete_document(self, doc_id: str) -> bool:
        """
        刪除文檔
        
        Args:
            doc_id: 文檔 ID
        
        Returns:
            是否成功刪除
        """
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
        """
        向量相似度搜索
        
        Args:
            query_embedding: 查詢向量
            top_k: 返回最相關的 k 個結果
        
        Returns:
            相關片段列表，包含相似度分數
        """
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
        """
        計算餘弦相似度
        
        Args:
            a: 向量 A
            b: 向量 B
        
        Returns:
            相似度分數（0-1）
        """
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
        """返回片段總數"""
        return len(self.chunks)
    
    def count_documents(self) -> int:
        """返回文檔總數"""
        return len(self.documents)


# 全局向量存儲實例
vector_store = VectorStore()

