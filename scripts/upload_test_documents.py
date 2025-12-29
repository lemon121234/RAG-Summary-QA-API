"""
上傳測試文檔到 RAG 系統
"""
import httpx
import asyncio
from pathlib import Path


async def upload_document(file_path: str, title: str = None):
    """上傳單個文檔（從文件讀取 title 和 content）"""
    import json
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 讀取文件內容
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"[ERROR] 讀取文件失敗: {file_path}")
            print(f"        錯誤: {str(e)}")
            return False
        
        # 解析文件：第一行是 title，第二行開始是 content
        if len(lines) < 2:
            print(f"[ERROR] 文件格式錯誤: {file_path}")
            print(f"        需要至少兩行：第一行是標題，第二行是內容")
            return False
        
        # 第一行是 title（如果沒有提供 title 參數）
        if title is None:
            title = lines[0].strip()
        
        # 第二行開始是 content（合併所有剩餘行）
        content = ''.join(lines[1:]).strip()
        
        # 確保內容不為空
        if not content:
            print(f"[ERROR] 文件內容為空: {file_path}")
            return False
        
        # 清理內容：移除多餘的換行和空格（但保留單個空格）
        content = ' '.join(content.split())  # 將所有空白字符替換為單個空格
        
        # 構建請求數據
        request_data = {
            "title": title,
            "content": content
        }
        
        # 驗證 JSON 序列化
        try:
            json_str = json.dumps(request_data, ensure_ascii=False)
            # 驗證可以正確解析
            json.loads(json_str)
        except Exception as e:
            print(f"[ERROR] JSON 序列化失敗: {str(e)}")
            return False
        
        # 發送請求
        try:
            response = await client.post(
                "http://localhost:8001/api/documents",
                json=request_data,
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        except httpx.RequestError as e:
            print(f"[ERROR] 網絡請求失敗: {str(e)}")
            return False
        except Exception as e:
            print(f"[ERROR] 請求異常: {str(e)}")
            return False
        
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] 已上傳: {title}")
            print(f"     文檔 ID: {result.get('document_id', 'N/A')}")
            print(f"     片段數量: {result.get('chunks_count', 'N/A')}")
            return True
        else:
            print(f"[ERROR] 上傳失敗: {title}")
            print(f"        錯誤: {response.text}")
            return False


async def main():
    """主函數"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 60)
    print("上傳測試文檔到 RAG 系統")
    print("=" * 60)
    
    # 測試文檔列表（現在只需要文件路徑，title 會從文件第一行讀取）
    documents = [
        "test_documents/article1_ai.txt",
        "test_documents/article2_blockchain.txt",
        "test_documents/article3_cloud_computing.txt"
    ]
    
    # 檢查文件是否存在
    for file_path in documents:
        if not Path(file_path).exists():
            print(f"[ERROR] 文件不存在: {file_path}")
            return
    
    # 上傳文檔
    print("\n開始上傳文檔...\n")
    results = []
    
    for file_path in documents:
        success = await upload_document(file_path)
        results.append(success)
        await asyncio.sleep(1)  # 避免請求過快
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 上傳結果")
    print("=" * 60)
    success_count = sum(results)
    print(f"成功: {success_count}/{len(documents)}")
    
    if success_count == len(documents):
        print("\n[SUCCESS] 所有文檔已成功上傳！")
        print("\n現在可以測試 RAG 問答功能：")
        print("  - 訪問 http://localhost:8001/docs")
        print("  - 使用 POST /api/rag/query 進行問答")
    else:
        print("\n[WARNING] 部分文檔上傳失敗，請檢查錯誤信息")


if __name__ == "__main__":
    asyncio.run(main())

