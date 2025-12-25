"""
URL 相關路由
處理網址摘要和問答功能
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime

from models import URLSummaryRequest, URLQARequest, URLQAResponse
from services import fetch_webpage_content
from llm.qa import call_ollama
from llm import generate_summary

router = APIRouter(prefix="/api/url", tags=["URL 功能"])


@router.post("/summary")
async def url_summary(request: URLSummaryRequest):
    """
    🌐 網址摘要（支援多個網址）
    
    輸入一個或多個網址，系統會自動抓取網頁內容並生成摘要。
    可以同時處理多個網址，返回每個網址的摘要。
    """
    results = []
    errors = []
    
    # 處理每個網址
    for url in request.url:
        try:
            # 抓取網頁內容
            webpage = await fetch_webpage_content(url)
            
            if not webpage["content"] or len(webpage["content"]) < 50:
                errors.append({
                    "url": url,
                    "error": "無法從網頁中提取足夠的文字內容，可能是網頁結構特殊或需要登入"
                })
                continue
            
            # 如果內容太長，先截取前 5000 字
            content = webpage["content"]
            if len(content) > 5000:
                content = content[:5000] + "..."
            
            # 使用摘要生成模組
            summary = await generate_summary(content, request.max_length, request.language)
            
            results.append({
                "url": url,
                "title": webpage["title"],
                "original_length": len(webpage["content"]),
                "summary": summary,
                "summary_length": len(summary),
                "status": "success"
            })
            
        except HTTPException as e:
            errors.append({
                "url": url,
                "error": e.detail
            })
        except Exception as e:
            errors.append({
                "url": url,
                "error": f"處理失敗: {str(e)}"
            })
    
    # 如果所有網址都失敗
    if len(results) == 0 and len(errors) > 0:
        raise HTTPException(
            status_code=400,
            detail=f"所有網址處理失敗: {errors[0]['error']}"
        )
    
    return {
        "total_urls": len(request.url),
        "success_count": len(results),
        "error_count": len(errors),
        "results": results,
        "errors": errors if errors else None,
        "created_at": datetime.now().isoformat()
    }


@router.post("/qa", response_model=URLQAResponse)
async def url_qa(request: URLQARequest):
    """
    ❓ 網址問答
    
    輸入網址和問題，系統會自動抓取網頁內容並根據內容回答問題。
    """
    # 抓取網頁內容
    webpage = await fetch_webpage_content(request.url)
    
    if not webpage["content"] or len(webpage["content"]) < 50:
        raise HTTPException(
            status_code=400,
            detail="無法從網頁中提取足夠的文字內容，可能是網頁結構特殊或需要登入"
        )
    
    # 語言設定
    language_map = {
        "zh-TW": "繁體中文",
        "zh-CN": "简体中文",
        "en": "English"
    }
    target_lang = language_map.get(request.language, "繁體中文")
    
    # 如果內容太長，先截取前 8000 字（問答需要更多上下文）
    content = webpage["content"]
    if len(content) > 8000:
        content = content[:8000] + "..."
    
    system_prompt = """你是一個專業的問答助手。請根據提供的網頁內容回答問題。
規則：
1. 只根據網頁內容中的信息回答
2. 如果內容中沒有相關信息，請明確說明
3. 回答要準確、有條理
4. 可以適當引用網頁中的內容"""
    
    prompt = f"""請根據以下網頁內容回答問題。

網頁標題：{webpage["title"]}

網頁內容：
{content}

問題：{request.question}

請用{target_lang}回答。如果網頁內容中沒有相關信息，請明確說明。"""
    
    answer = await call_ollama(prompt, system_prompt)
    
    return URLQAResponse(
        url=request.url,
        question=request.question,
        answer=answer,
        title=webpage["title"]
    )

