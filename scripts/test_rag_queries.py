"""
測試 RAG 問答功能
"""
import httpx
import asyncio
import json


async def test_rag_query(question: str, language: str = "zh-TW"):
    """測試 RAG 問答"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        print(f"\n[Q] 問題: {question}")
        print("-" * 60)
        
        try:
            response = await client.post(
                "http://localhost:8001/api/rag/query",
                json={
                    "question": question,
                    "language": language
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"[A] 回答: {result.get('answer', 'N/A')}")
                print(f"[C] 信心程度: {result.get('confidence', 'N/A')}")
                
                sources = result.get('sources', [])
                if sources:
                    print(f"[S] 來源文檔 ({len(sources)} 個):")
                    for i, source in enumerate(sources[:3], 1):  # 只顯示前3個
                        print(f"     {i}. {source.get('title', 'N/A')} (相似度: {source.get('score', 0):.3f})")
                
                return result
            else:
                print(f"[ERROR] 錯誤: {response.status_code}")
                print(f"       訊息: {response.text}")
                return None
                
        except Exception as e:
            print(f"[ERROR] 請求失敗: {str(e)}")
            return None


async def main():
    """主函數"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 60)
    print("RAG 問答測試")
    print("=" * 60)
    
    # 測試問題列表
    questions = [
        # 文章 1：AI 醫療
        "AI 在醫療影像診斷方面有什麼優勢？",
        "AI 在個性化醫療方面如何發揮作用？",
        "AI 在醫療領域應用時面臨哪些挑戰？",
        
        # 文章 2：區塊鏈
        "區塊鏈的核心特點有哪些？",
        "智能合約是什麼？在哪些領域有應用？",
        "區塊鏈技術面臨哪些挑戰？",
        
        # 文章 3：雲端計算
        "雲端計算的主要優勢是什麼？",
        "雲端計算的三種服務模式是什麼？",
        "企業採用雲端計算時需要注意哪些風險？",
        
        # 跨文檔問題
        "人工智慧、區塊鏈和雲端計算這三種技術分別在哪些領域有應用？",
    ]
    
    print(f"\n將測試 {len(questions)} 個問題...\n")
    
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}]")
        result = await test_rag_query(question)
        results.append(result)
        await asyncio.sleep(2)  # 避免請求過快
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    success_count = sum(1 for r in results if r is not None)
    print(f"成功: {success_count}/{len(questions)}")
    
    if success_count > 0:
        print("\n[SUCCESS] 測試完成！可以查看上述回答評估 RAG 系統的效果。")


if __name__ == "__main__":
    asyncio.run(main())

