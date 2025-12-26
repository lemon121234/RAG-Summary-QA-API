"""
Debug 和 Logging 工具
用於記錄 RAG 系統的檢索和生成過程，方便 debug 和穩定性驗證
"""
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_debug.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Debug 記錄目錄
DEBUG_DIR = Path("debug_logs")
DEBUG_DIR.mkdir(exist_ok=True)


class RAGDebugLogger:
    """RAG 系統的 Debug Logger"""
    
    def __init__(self):
        self.session_logs: List[Dict] = []
    
    def log_retrieval(
        self,
        query: str,
        query_embedding: Optional[List[float]] = None,
        retrieved_chunks: List[Dict] = None,
        top_k: int = 5
    ):
        """
        記錄檢索過程
        
        Args:
            query: 查詢文本
            query_embedding: 查詢向量（可選，因為可能很長）
            retrieved_chunks: 檢索到的片段
            top_k: 返回的 top-k 數量
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "retrieval",
            "query": query,
            "query_embedding_dim": len(query_embedding) if query_embedding else None,
            "top_k": top_k,
            "retrieved_count": len(retrieved_chunks) if retrieved_chunks else 0,
            "chunks": []
        }
        
        if retrieved_chunks:
            for i, chunk in enumerate(retrieved_chunks):
                chunk_log = {
                    "rank": i + 1,
                    "document_id": chunk.get("document_id"),
                    "document_title": chunk.get("title"),
                    "chunk_index": chunk.get("chunk_index"),
                    "similarity_score": round(chunk.get("score", 0), 4),
                    "content_preview": chunk.get("content", "")[:100] + "..." if len(chunk.get("content", "")) > 100 else chunk.get("content", "")
                }
                log_entry["chunks"].append(chunk_log)
        
        self.session_logs.append(log_entry)
        logger.info(f"Retrieval: query='{query[:50]}...', retrieved={len(retrieved_chunks) if retrieved_chunks else 0} chunks")
        
        # 計算統計信息
        if retrieved_chunks:
            scores = [chunk.get("score", 0) for chunk in retrieved_chunks]
            avg_score = sum(scores) / len(scores) if scores else 0
            max_score = max(scores) if scores else 0
            min_score = min(scores) if scores else 0
            
            logger.info(f"  Score stats: avg={avg_score:.3f}, max={max_score:.3f}, min={min_score:.3f}")
    
    def log_qa(
        self,
        question: str,
        answer: str,
        confidence: str,
        context_chunks: List[Dict] = None
    ):
        """
        記錄問答過程
        
        Args:
            question: 問題
            answer: 答案
            confidence: 信心程度
            context_chunks: 使用的上下文片段
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "qa",
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "context_chunks_count": len(context_chunks) if context_chunks else 0
        }
        
        self.session_logs.append(log_entry)
        logger.info(f"QA: question='{question[:50]}...', confidence={confidence}, answer_length={len(answer)}")
    
    def log_full_rag_session(
        self,
        question: str,
        retrieved_chunks: List[Dict],
        answer: str,
        confidence: str,
        top_k: int = 5
    ):
        """
        記錄完整的 RAG 會話（檢索 + 生成）
        
        Args:
            question: 問題
            retrieved_chunks: 檢索到的片段
            answer: 生成的答案
            confidence: 信心程度
            top_k: top-k 參數
        """
        session = {
            "timestamp": datetime.now().isoformat(),
            "type": "full_rag_session",
            "question": question,
            "top_k": top_k,
            "retrieved_chunks": [
                {
                    "document_title": chunk.get("title"),
                    "similarity_score": round(chunk.get("score", 0), 4),
                    "content_preview": chunk.get("content", "")[:200]
                }
                for chunk in retrieved_chunks
            ],
            "answer": answer,
            "confidence": confidence,
            "answer_quality_indicators": {
                "avg_similarity": round(
                    sum(chunk.get("score", 0) for chunk in retrieved_chunks) / len(retrieved_chunks)
                    if retrieved_chunks else 0, 4
                ),
                "has_high_confidence_chunks": any(
                    chunk.get("score", 0) > 0.7 for chunk in retrieved_chunks
                ) if retrieved_chunks else False
            }
        }
        
        self.session_logs.append(session)
        
        # 保存到文件
        session_file = DEBUG_DIR / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Full RAG session logged: {session_file}")
    
    def save_session_summary(self, filename: Optional[str] = None):
        """
        保存會話摘要
        
        Args:
            filename: 文件名（可選）
        """
        if not filename:
            filename = DEBUG_DIR / f"session_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            "total_sessions": len([log for log in self.session_logs if log.get("type") == "full_rag_session"]),
            "total_retrievals": len([log for log in self.session_logs if log.get("type") == "retrieval"]),
            "sessions": self.session_logs
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Session summary saved: {filename}")
        return filename


# 全局 logger 實例
rag_debug_logger = RAGDebugLogger()


