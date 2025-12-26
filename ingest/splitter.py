"""
文本切割模組
將長文本分割成適合處理的小塊
"""
import re
from typing import List

from config import CHUNK_SIZE, CHUNK_OVERLAP


def split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    將文本分割成小塊
    
    Args:
        text: 要分割的文本
        chunk_size: 每個片段的最大字數
        overlap: 片段之間的重疊字數
    
    Returns:
        文本片段列表
    """
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += ("\n\n" + para if current_chunk else para)
        else:
            if current_chunk:
                chunks.append(current_chunk)
            
            if len(para) > chunk_size:
                sentences = re.split(r'(?<=[。！？.!?])\s*', para)
                current_chunk = ""
                for sent in sentences:
                    if len(current_chunk) + len(sent) <= chunk_size:
                        current_chunk += sent
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = sent
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # 如果沒有分割成功，至少返回原文
    if not chunks and text.strip():
        chunks = [text.strip()]
    
    return chunks




