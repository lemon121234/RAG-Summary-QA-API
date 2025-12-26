"""
嵌入向量生成模組
使用 Ollama 生成文本的嵌入向量
"""
import httpx
from typing import List
from fastapi import HTTPException

from config import OLLAMA_BASE_URL, EMBEDDING_MODEL


async def get_embedding(text: str) -> List[float]:
    """
    使用 Ollama 獲取文本嵌入向量
    
    Args:
        text: 要嵌入的文本
    
    Returns:
        嵌入向量（浮點數列表）
    
    Raises:
        HTTPException: 當 Ollama 連接失敗或模型不存在時
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                json={
                    "model": EMBEDDING_MODEL,
                    "prompt": text
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"嵌入生成失敗: {response.text}"
                )
            
            result = response.json()
            return result.get("embedding", [])
            
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"無法連接到 Ollama。請確認已啟動並下載嵌入模型: ollama pull {EMBEDDING_MODEL}"
        )


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    批量獲取嵌入向量
    
    Args:
        texts: 文本列表
    
    Returns:
        嵌入向量列表
    """
    embeddings = []
    for text in texts:
        emb = await get_embedding(text)
        embeddings.append(emb)
    return embeddings




