"""
RAG 問答模組
構建 prompt 並調用 LLM 生成答案
"""
from typing import List, Dict
import httpx
from fastapi import HTTPException

from config import OLLAMA_BASE_URL, OLLAMA_MODEL


async def call_ollama(prompt: str, system_prompt: str = "") -> str:
    """
    調用 Ollama LLM
    
    Args:
        prompt: 用戶提示詞
        system_prompt: 系統提示詞
    
    Returns:
        LLM 生成的回應
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Ollama 請求失敗: {response.text}")
            
            result = response.json()
            return result.get("response", "").strip()
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="無法連接到 Ollama。請執行 'ollama serve'"
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama 回應超時")


async def rag_qa(question: str, context_chunks: List[Dict], language: str = "zh-TW") -> tuple[str, str]:
    """
    執行 RAG 問答
    
    Args:
        question: 問題
        context_chunks: 相關的文本片段
        language: 輸出語言
    
    Returns:
        (答案, 信心程度)
    """
    # 組合上下文
    context_parts = []
    for chunk in context_chunks:
        context_parts.append(f"[來源: {chunk['title']}]\n{chunk['content']}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    # 語言設定
    language_map = {
        "zh-TW": "繁體中文",
        "zh-CN": "简体中文",
        "en": "English"
    }
    target_lang = language_map.get(language, "繁體中文")
    
    # 構建提示詞
    system_prompt = """你是一個專業的問答助手。請根據提供的參考資料回答問題。
規則：
1. 只根據參考資料中的信息回答
2. 如果資料中沒有相關信息，請明確說明
3. 回答要準確、有條理
4. 適當引用來源"""
    
    prompt = f"""請根據以下參考資料回答問題。

## 參考資料
{context}

## 問題
{question}

請用{target_lang}回答。"""
    
    # 調用 LLM
    answer = await call_ollama(prompt, system_prompt)
    
    # 計算信心程度
    if context_chunks:
        avg_score = sum(chunk.get("score", 0) for chunk in context_chunks) / len(context_chunks)
        if avg_score > 0.7:
            confidence = "high"
        elif avg_score > 0.5:
            confidence = "medium"
        else:
            confidence = "low"
    else:
        confidence = "low"
    
    return answer, confidence




