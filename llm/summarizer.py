"""
摘要生成模組
使用 LLM 生成文本摘要
"""
from llm.qa import call_ollama


async def generate_summary(text: str, max_length: int = 200, language: str = "zh-TW") -> str:
    """
    生成文本摘要
    
    Args:
        text: 要摘要的文本
        max_length: 摘要最大長度
        language: 輸出語言
    
    Returns:
        生成的摘要
    """
    language_map = {
        "zh-TW": "繁體中文",
        "zh-CN": "简体中文",
        "en": "English"
    }
    target_lang = language_map.get(language, "繁體中文")
    
    system_prompt = "你是一個專業的文本摘要助手。"
    
    prompt = f"""請為以下文本生成摘要。

要求：
1. 摘要不超過 {max_length} 字
2. 使用 {target_lang}
3. 保留關鍵信息

文本：
{text}

請直接輸出摘要。"""
    
    summary = await call_ollama(prompt, system_prompt)
    return summary

