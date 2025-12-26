"""
LLM 生成層
負責 prompt 構建和 LLM 調用
"""
from .qa import rag_qa
from .summarizer import generate_summary

__all__ = ["rag_qa", "generate_summary"]




