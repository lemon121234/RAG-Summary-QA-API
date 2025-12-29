"""
穩定性測試腳本
驗證 RAG 系統的檢索結果是否穩定（deterministic）
"""
import asyncio
import json
from pathlib import Path
from typing import List, Dict
import sys
import os

# 添加項目根目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vectorstore import vector_store
from retriever import search_similar_chunks
from ingest import split_text, get_embedding
from utils.debug_logger import rag_debug_logger, DEBUG_DIR


class StabilityTester:
    """穩定性測試器"""
    
    def __init__(self):
        self.test_results: List[Dict] = []
    
    async def test_embedding_consistency(self, text: str, iterations: int = 5) -> Dict:
        """
        測試 embedding 一致性
        
        Args:
            text: 測試文本
            iterations: 測試次數
        
        Returns:
            測試結果
        """
        print(f"\n🔍 測試 Embedding 一致性...")
        print(f"   文本: {text[:50]}...")
        print(f"   測試次數: {iterations}")
        
        embeddings = []
        for i in range(iterations):
            emb = await get_embedding(text)
            embeddings.append(emb)
            print(f"   第 {i+1} 次: embedding 維度 = {len(emb)}")
        
        # 檢查一致性
        first_emb = embeddings[0]
        all_same = all(
            len(emb) == len(first_emb) and
            all(abs(a - b) < 1e-6 for a, b in zip(emb, first_emb))
            for emb in embeddings[1:]
        )
        
        result = {
            "test_name": "embedding_consistency",
            "text": text,
            "iterations": iterations,
            "all_embeddings_same": all_same,
            "embedding_dim": len(first_emb),
            "status": "✅ PASS" if all_same else "❌ FAIL"
        }
        
        print(f"   結果: {result['status']}")
        return result
    
    async def test_retrieval_consistency(
        self,
        query: str,
        iterations: int = 5,
        top_k: int = 5
    ) -> Dict:
        """
        測試檢索一致性
        
        Args:
            query: 查詢文本
            iterations: 測試次數
            top_k: top-k 參數
        
        Returns:
            測試結果
        """
        print(f"\n🔍 測試 Retrieval 一致性...")
        print(f"   查詢: {query}")
        print(f"   測試次數: {iterations}, top_k: {top_k}")
        
        all_results = []
        for i in range(iterations):
            results = await search_similar_chunks(query, top_k)
            all_results.append(results)
            
            # 記錄每次檢索
            rag_debug_logger.log_retrieval(query, retrieved_chunks=results, top_k=top_k)
            
            print(f"   第 {i+1} 次: 檢索到 {len(results)} 個片段")
            if results:
                scores = [r.get("score", 0) for r in results]
                print(f"           相似度分數: {[round(s, 3) for s in scores]}")
        
        # 檢查一致性
        first_results = all_results[0]
        consistent = True
        differences = []
        
        for i, results in enumerate(all_results[1:], 1):
            if len(results) != len(first_results):
                consistent = False
                differences.append(f"第 {i+1} 次結果數量不同: {len(results)} vs {len(first_results)}")
                continue
            
            # 檢查每個位置的 chunk ID 和分數
            for j, (first, current) in enumerate(zip(first_results, results)):
                if first.get("id") != current.get("id"):
                    consistent = False
                    differences.append(
                        f"第 {i+1} 次 rank {j+1} chunk ID 不同: "
                        f"{first.get('id')} vs {current.get('id')}"
                    )
                
                score_diff = abs(first.get("score", 0) - current.get("score", 0))
                if score_diff > 1e-6:
                    consistent = False
                    differences.append(
                        f"第 {i+1} 次 rank {j+1} 分數不同: "
                        f"{first.get('score', 0):.6f} vs {current.get('score', 0):.6f}"
                    )
        
        result = {
            "test_name": "retrieval_consistency",
            "query": query,
            "iterations": iterations,
            "top_k": top_k,
            "is_consistent": consistent,
            "differences": differences,
            "status": "✅ PASS" if consistent else "❌ FAIL"
        }
        
        print(f"   結果: {result['status']}")
        if differences:
            print(f"   差異: {differences[:3]}...")  # 只顯示前3個
        
        return result
    
    async def test_chunking_consistency(self, text: str, iterations: int = 5) -> Dict:
        """
        測試 chunking 一致性
        
        Args:
            text: 測試文本
            iterations: 測試次數
        
        Returns:
            測試結果
        """
        print(f"\n🔍 測試 Chunking 一致性...")
        print(f"   文本長度: {len(text)} 字")
        print(f"   測試次數: {iterations}")
        
        all_chunks = []
        for i in range(iterations):
            chunks = split_text(text)
            all_chunks.append(chunks)
            print(f"   第 {i+1} 次: 產生 {len(chunks)} 個 chunks")
        
        # 檢查一致性
        first_chunks = all_chunks[0]
        consistent = True
        differences = []
        
        for i, chunks in enumerate(all_chunks[1:], 1):
            if len(chunks) != len(first_chunks):
                consistent = False
                differences.append(f"第 {i+1} 次 chunk 數量不同: {len(chunks)} vs {len(first_chunks)}")
                continue
            
            for j, (first, current) in enumerate(zip(first_chunks, chunks)):
                if first != current:
                    consistent = False
                    differences.append(f"第 {i+1} 次 chunk {j+1} 內容不同")
                    break
        
        result = {
            "test_name": "chunking_consistency",
            "text_length": len(text),
            "iterations": iterations,
            "chunks_count": len(first_chunks),
            "is_consistent": consistent,
            "differences": differences,
            "status": "✅ PASS" if consistent else "❌ FAIL"
        }
        
        print(f"   結果: {result['status']}")
        return result
    
    async def run_all_tests(
        self,
        test_text: str,
        test_query: str,
        iterations: int = 5
    ):
        """
        執行所有穩定性測試
        
        Args:
            test_text: 測試文本
            test_query: 測試查詢
            iterations: 每個測試的迭代次數
        """
        print("=" * 60)
        print("🚀 RAG 系統穩定性測試")
        print("=" * 60)
        
        # 確保有文檔在向量資料庫中
        if vector_store.count_chunks() == 0:
            print("\n⚠️  向量資料庫為空，先添加測試文檔...")
            chunks = split_text(test_text)
            embeddings = []
            for chunk in chunks:
                emb = await get_embedding(chunk)
                embeddings.append(emb)
            
            vector_store.add_document(
                doc_id="test_doc_001",
                title="穩定性測試文檔",
                content=test_text,
                chunks=chunks,
                embeddings=embeddings
            )
            print(f"✅ 已添加測試文檔: {len(chunks)} 個 chunks")
        
        # 執行測試
        results = []
        
        # 1. Embedding 一致性
        results.append(await self.test_embedding_consistency(test_text, iterations))
        
        # 2. Chunking 一致性
        results.append(await self.test_chunking_consistency(test_text, iterations))
        
        # 3. Retrieval 一致性
        results.append(await self.test_retrieval_consistency(test_query, iterations))
        
        # 保存結果
        self.test_results = results
        self.save_results()
        
        # 顯示摘要
        print("\n" + "=" * 60)
        print("📊 測試摘要")
        print("=" * 60)
        for result in results:
            print(f"{result['status']} {result['test_name']}")
        
        all_passed = all(r['status'] == '✅ PASS' for r in results)
        print(f"\n{'✅ 所有測試通過' if all_passed else '❌ 部分測試失敗'}")
        
        return results
    
    def save_results(self):
        """保存測試結果"""
        results_file = DEBUG_DIR / f"stability_test_{Path(__file__).stem}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                "test_results": self.test_results,
                "summary": {
                    "total_tests": len(self.test_results),
                    "passed": sum(1 for r in self.test_results if r['status'] == '✅ PASS'),
                    "failed": sum(1 for r in self.test_results if r['status'] == '❌ FAIL')
                }
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 測試結果已保存: {results_file}")


async def main():
    """主函數"""
    tester = StabilityTester()
    
    # 測試數據
    test_text = """
    人工智能（AI）是計算機科學的一個分支，致力於創建能夠執行通常需要人類智能的任務的系統。
    AI 系統可以學習、推理、感知環境並做出決策。機器學習是 AI 的一個子領域，它使計算機能夠從數據中學習，而無需明確編程。
    深度學習是機器學習的一個子集，使用神經網絡來模擬人腦的工作方式。
    RAG（檢索增強生成）是一種結合檢索和生成的技術，用於提高語言模型的準確性和相關性。
    """
    
    test_query = "什麼是 RAG？"
    
    await tester.run_all_tests(test_text, test_query, iterations=5)


if __name__ == "__main__":
    asyncio.run(main())





