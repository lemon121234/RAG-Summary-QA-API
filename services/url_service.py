"""
URL 服務模組
處理網頁內容抓取
"""
import httpx
import re
from typing import Dict
from fastapi import HTTPException
from bs4 import BeautifulSoup
from urllib.parse import urlparse


async def fetch_webpage_content(url: str) -> Dict[str, str]:
    """
    抓取網頁內容並提取文字
    
    Args:
        url: 網頁 URL
    
    Returns:
        包含標題和內容的字典
    
    Raises:
        HTTPException: 當網頁抓取失敗時
    """
    try:
        # 驗證 URL
        parsed = urlparse(url)
        if not parsed.scheme:
            url = "https://" + url
        
        # 設置請求頭，模擬瀏覽器
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            # 解析 HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 移除 script 和 style 標籤
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()
            
            # 提取標題
            title = ""
            if soup.title:
                title = soup.title.get_text().strip()
            elif soup.find("h1"):
                title = soup.find("h1").get_text().strip()
            
            # 提取主要內容
            # 優先查找 article, main, 或包含大量文字的 div
            content = ""
            article = soup.find("article") or soup.find("main") or soup.find("div", class_=re.compile("content|article|post|entry"))
            
            if article:
                content = article.get_text(separator="\n", strip=True)
            else:
                # 如果沒有找到特定標籤，提取所有段落
                paragraphs = soup.find_all("p")
                content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            # 如果內容太短，嘗試提取 body
            if len(content) < 100:
                body = soup.find("body")
                if body:
                    content = body.get_text(separator="\n", strip=True)
            
            # 清理內容：移除多餘空白
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = content.strip()
            
            return {
                "title": title,
                "content": content,
                "url": url
            }
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="網頁載入超時，請稍後再試")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"無法訪問網頁: HTTP {e.response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"抓取網頁失敗: {str(e)}")

