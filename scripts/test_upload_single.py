"""
單個文檔上傳測試腳本（用於調試 JSON 錯誤）
"""
import httpx
import json
import asyncio
from pathlib import Path


async def test_upload_single(file_path: str, title: str = None):
    """測試上傳單個文檔"""
    if not Path(file_path).exists():
        print(f"[ERROR] 文件不存在: {file_path}")
        return
    
    # 讀取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # 清理內容
    content = ' '.join(content.split())
    
    if not title:
        title = Path(file_path).stem
    
    # 構建請求數據
    request_data = {
        "title": title,
        "content": content
    }
    
    # 驗證 JSON
    print("=" * 60)
    print("JSON 驗證測試")
    print("=" * 60)
    try:
        json_str = json.dumps(request_data, ensure_ascii=False)
        print(f"[OK] JSON 序列化成功")
        print(f"     JSON 長度: {len(json_str)} 字符")
        print(f"     內容長度: {len(content)} 字符")
        
        # 檢查第 777 個字符附近
        if len(json_str) > 777:
            print(f"\n第 777 個字符附近:")
            start = max(0, 777 - 20)
            end = min(len(json_str), 777 + 20)
            print(f"    {json_str[start:end]}")
            print(f"    {' ' * (777 - start)}^")
        
        # 驗證可以解析
        parsed = json.loads(json_str)
        print(f"[OK] JSON 解析成功")
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 解析失敗:")
        print(f"    位置: {e.pos}")
        print(f"    錯誤: {e.msg}")
        print(f"    附近內容: {json_str[max(0, e.pos-20):e.pos+20]}")
        return
    except Exception as e:
        print(f"[ERROR] JSON 處理失敗: {str(e)}")
        return
    
    # 發送請求
    print("\n" + "=" * 60)
    print("發送 HTTP 請求")
    print("=" * 60)
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:8001/api/documents",
                json=request_data
            )
            
            print(f"狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"[SUCCESS] 上傳成功!")
                print(f"    文檔 ID: {result.get('document_id')}")
                print(f"    片段數量: {result.get('chunks_count')}")
            else:
                print(f"[ERROR] 上傳失敗:")
                print(f"    響應: {response.text}")
                
    except Exception as e:
        print(f"[ERROR] 請求失敗: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python test_upload_single.py <文件路徑> [標題]")
        print("\n示例:")
        print("  python test_upload_single.py test_documents/article1_ai.txt")
        print("  python test_upload_single.py test_documents/article1_ai.txt 'AI醫療應用'")
        sys.exit(1)
    
    file_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    
    asyncio.run(test_upload_single(file_path, title))

