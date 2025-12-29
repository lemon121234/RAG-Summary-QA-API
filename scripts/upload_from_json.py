"""
從 JSON 文件上傳文檔
"""
import httpx
import asyncio
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


async def upload_from_json(json_file: str):
    """從 JSON 文件上傳文檔"""
    # 讀取 JSON 文件
    with open(json_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print("=" * 60)
    print(f"從 {json_file} 上傳 {len(articles)} 篇文檔")
    print("=" * 60)
    
    results = []
    async with httpx.AsyncClient(timeout=60.0) as client:
        for i, article in enumerate(articles, 1):
            title = article.get("title", "未命名文檔")
            content = article.get("content", "")
            
            if not content:
                print(f"\n[{i}/{len(articles)}] [SKIP] {title} - 內容為空")
                continue
            
            # 清理內容
            content = ' '.join(content.split())
            
            print(f"\n[{i}/{len(articles)}] 上傳: {title}")
            
            try:
                response = await client.post(
                    "http://localhost:8001/api/documents",
                    json={
                        "title": title,
                        "content": content
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  [OK] 文檔 ID: {result.get('document_id')}")
                    print(f"       片段數量: {result.get('chunks_count')}")
                    results.append(True)
                else:
                    print(f"  [ERROR] 上傳失敗: {response.status_code}")
                    print(f"          訊息: {response.text}")
                    results.append(False)
                    
            except Exception as e:
                print(f"  [ERROR] 請求失敗: {str(e)}")
                results.append(False)
            
            await asyncio.sleep(2)  # 等待嵌入向量生成
    
    # 總結
    print("\n" + "=" * 60)
    print("上傳結果")
    print("=" * 60)
    success_count = sum(results)
    print(f"成功: {success_count}/{len(articles)}")
    
    if success_count == len(articles):
        print("\n[SUCCESS] 所有文檔已成功上傳！")
    else:
        print("\n[WARNING] 部分文檔上傳失敗。")


if __name__ == "__main__":
    import sys
    
    json_file = sys.argv[1] if len(sys.argv) > 1 else "test_documents/articles.json"
    
    if not json_file.endswith('.json'):
        print("錯誤: 請提供 JSON 文件")
        sys.exit(1)
    
    asyncio.run(upload_from_json(json_file))



