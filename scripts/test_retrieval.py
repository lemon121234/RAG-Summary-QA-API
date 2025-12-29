"""
測試檢索功能
"""
import httpx
import asyncio


async def test_retrieval():
    """測試檢索功能"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 測試問題
        test_queries = [
            "智能合約是什麼？",
            "區塊鏈的核心特點",
            "AI 在醫療影像診斷",
            "雲端計算的服務模式"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"查詢: {query}")
            print('='*60)
            
            try:
                # 先測試檢索（通過 RAG 查詢）
                response = await client.post(
                    "http://localhost:8001/api/rag/query",
                    json={
                        "question": query,
                        "top_k": 5,
                        "language": "zh-TW"
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"\n回答: {result['answer'][:200]}...")
                    print(f"\n檢索到的文檔:")
                    for i, source in enumerate(result['sources'][:3], 1):
                        print(f"  {i}. {source['document_title']} (相似度: {source['relevance_score']})")
                        print(f"     內容: {source['content'][:100]}...")
                else:
                    print(f"錯誤: {response.status_code}")
                    print(f"訊息: {response.text}")
                    
            except Exception as e:
                print(f"請求失敗: {str(e)}")
            
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(test_retrieval())

