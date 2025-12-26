# RAG 專案 - PPT 代碼片段

## 📋 目錄

1. [架構圖代碼](#架構圖代碼)
2. [核心代碼片段](#核心代碼片段)
3. [穩定性測試代碼](#穩定性測試代碼)
4. [Debug Logging 代碼](#debug-logging-代碼)

---

## 🏗️ 架構圖代碼

### 分層架構示意

```python
# 分層架構：職責分離
ingest/              # 資料攝取層
  ├── splitter.py   # 文本切割
  └── embedder.py   # 向量嵌入

vectorstore/         # 向量存儲層
  └── store.py      # 向量資料庫

retriever/           # 檢索層
  └── search.py     # 相似度搜尋

llm/                 # 生成層
  ├── qa.py         # RAG 問答
  └── summarizer.py # 摘要生成

routes/              # API 路由層
  ├── documents.py   # 文檔管理
  └── rag.py        # RAG 問答
```

---

## 💻 核心代碼片段

### 1. 主入口（簡潔清晰）

```python
# main.py - 只有 125 行
from fastapi import FastAPI
from routes import documents_router, rag_router

app = FastAPI(title="RAG 摘要與QA API")

# 註冊路由
app.include_router(documents_router)
app.include_router(rag_router)
```

**說明**：從 800+ 行重構為分層架構，主文件只有 125 行

---

### 2. 文本切割（可配置）

```python
# ingest/splitter.py
def split_text(
    text: str, 
    chunk_size: int = CHUNK_SIZE,  # 可配置
    overlap: int = CHUNK_OVERLAP   # 可配置
) -> List[str]:
    """
    將文本分割成小塊
    支持動態調整 chunk size 和 overlap
    """
    # 按段落分割
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += para
        else:
            chunks.append(current_chunk)
            # 處理 overlap
            current_chunk = para[-overlap:] + para
    
    return chunks
```

**說明**：可配置的 chunking strategy，支持調整參數

---

### 3. Cosine Similarity（語意相似度）

```python
# vectorstore/store.py
def _cosine_similarity(
    self, 
    a: List[float], 
    b: List[float]
) -> float:
    """
    計算餘弦相似度
    比歐氏距離更適合高維向量
    """
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)
```

**說明**：使用 cosine similarity 計算語意相似度

---

### 4. Top-K Retrieval（檢索最相關內容）

```python
# vectorstore/store.py
def search(
    self, 
    query_embedding: List[float], 
    top_k: int = 5
) -> List[dict]:
    """
    向量相似度搜索
    返回最相關的 k 個結果
    """
    # 計算餘弦相似度
    scores = []
    for i, emb in enumerate(self.embeddings):
        score = self._cosine_similarity(query_embedding, emb)
        scores.append((i, score))
    
    # 排序並返回 top_k
    scores.sort(key=lambda x: x[1], reverse=True)
    
    results = []
    for i, score in scores[:top_k]:
        chunk = self.chunks[i].copy()
        chunk["score"] = score  # 附帶相似度分數
        results.append(chunk)
    
    return results
```

**說明**：Top-k retrieval 確保只返回最相關的內容

---

### 5. RAG 問答（完整流程）

```python
# llm/qa.py
async def rag_qa(
    question: str, 
    context_chunks: List[Dict], 
    language: str = "zh-TW"
) -> tuple[str, str]:
    """
    RAG 問答流程：
    1. 組合上下文
    2. 構建 prompt
    3. 調用 LLM
    4. 計算信心程度
    """
    # 組合上下文
    context = "\n\n---\n\n".join([
        f"[來源: {chunk['title']}]\n{chunk['content']}"
        for chunk in context_chunks
    ])
    
    # 構建 prompt
    prompt = f"""請根據以下參考資料回答問題。

## 參考資料
{context}

## 問題
{question}"""
    
    # 調用 LLM
    answer = await call_ollama(prompt, system_prompt)
    
    # 計算信心程度（基於相似度分數）
    avg_score = sum(chunk.get("score", 0) for chunk in context_chunks) / len(context_chunks)
    if avg_score > 0.7:
        confidence = "high"
    elif avg_score > 0.5:
        confidence = "medium"
    else:
        confidence = "low"
    
    return answer, confidence
```

**說明**：完整的 RAG 流程，包含信心程度計算

---

## 🧪 穩定性測試代碼

### Embedding 一致性測試

```python
# tests/stability_test.py
async def test_embedding_consistency(
    self, 
    text: str, 
    iterations: int = 5
) -> Dict:
    """
    測試 embedding 一致性
    驗證同一文本多次生成 embedding 是否相同
    """
    embeddings = []
    for i in range(iterations):
        emb = await get_embedding(text)
        embeddings.append(emb)
    
    # 檢查一致性
    first_emb = embeddings[0]
    all_same = all(
        abs(a - b) < 1e-6 
        for a, b in zip(emb, first_emb)
        for emb in embeddings[1:]
    )
    
    return {
        "status": "✅ PASS" if all_same else "❌ FAIL",
        "all_embeddings_same": all_same
    }
```

**說明**：驗證 embedding 的 deterministic 特性

---

### Retrieval 一致性測試

```python
# tests/stability_test.py
async def test_retrieval_consistency(
    self,
    query: str,
    iterations: int = 5,
    top_k: int = 5
) -> Dict:
    """
    測試檢索一致性
    驗證同一 query 多次檢索結果是否相同
    """
    all_results = []
    for i in range(iterations):
        results = await search_similar_chunks(query, top_k)
        all_results.append(results)
    
    # 檢查一致性
    first_results = all_results[0]
    consistent = all(
        len(results) == len(first_results) and
        all(
            r.get("id") == first.get("id") and
            abs(r.get("score", 0) - first.get("score", 0)) < 1e-6
            for r, first in zip(results, first_results)
        )
        for results in all_results[1:]
    )
    
    return {
        "status": "✅ PASS" if consistent else "❌ FAIL",
        "is_consistent": consistent
    }
```

**說明**：驗證檢索過程的 deterministic 特性

---

## 🔍 Debug Logging 代碼

### 檢索過程記錄

```python
# utils/debug_logger.py
def log_retrieval(
    self,
    query: str,
    retrieved_chunks: List[Dict],
    top_k: int = 5
):
    """
    記錄檢索過程
    包含：查詢、檢索結果、相似度分數
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "retrieval",
        "query": query,
        "top_k": top_k,
        "retrieved_count": len(retrieved_chunks),
        "chunks": [
            {
                "rank": i + 1,
                "document_title": chunk.get("title"),
                "similarity_score": round(chunk.get("score", 0), 4),
                "content_preview": chunk.get("content", "")[:100]
            }
            for i, chunk in enumerate(retrieved_chunks)
        ]
    }
    
    # 計算統計信息
    if retrieved_chunks:
        scores = [chunk.get("score", 0) for chunk in retrieved_chunks]
        log_entry["statistics"] = {
            "avg_score": sum(scores) / len(scores),
            "max_score": max(scores),
            "min_score": min(scores)
        }
    
    self.session_logs.append(log_entry)
```

**說明**：記錄每次檢索的詳細信息，方便 debug

---

### 完整 RAG 會話記錄

```python
# utils/debug_logger.py
def log_full_rag_session(
    self,
    question: str,
    retrieved_chunks: List[Dict],
    answer: str,
    confidence: str,
    top_k: int = 5
):
    """
    記錄完整的 RAG 會話
    包含：問題、檢索結果、答案、信心程度
    """
    session = {
        "timestamp": datetime.now().isoformat(),
        "type": "full_rag_session",
        "question": question,
        "top_k": top_k,
        "retrieved_chunks": [
            {
                "document_title": chunk.get("title"),
                "similarity_score": round(chunk.get("score", 0), 4),
                "content_preview": chunk.get("content", "")[:200]
            }
            for chunk in retrieved_chunks
        ],
        "answer": answer,
        "confidence": confidence,
        "answer_quality_indicators": {
            "avg_similarity": round(
                sum(chunk.get("score", 0) for chunk in retrieved_chunks) / len(retrieved_chunks),
                4
            ),
            "has_high_confidence_chunks": any(
                chunk.get("score", 0) > 0.7 for chunk in retrieved_chunks
            )
        }
    }
    
    # 保存到文件
    session_file = DEBUG_DIR / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=2)
```

**說明**：記錄完整的 RAG 會話，方便事後分析

---

## 📊 PPT 使用建議

### 1. 架構圖
- 使用第一部分的架構示意代碼
- 可以配合流程圖說明數據流向

### 2. 核心功能
- 選擇 2-3 個核心代碼片段
- 重點說明設計決策（如為什麼用 cosine similarity）

### 3. 穩定性與 Debug
- 展示穩定性測試代碼
- 說明如何通過 logging 快速定位問題

### 4. 代碼展示技巧
- 只展示關鍵部分，不要全部代碼
- 用註釋說明重點
- 可以配合流程圖或架構圖

---

## 🎯 重點強調

1. **分層架構**：從 800+ 行重構為清晰的五層架構
2. **可配置性**：chunk size 和 overlap 可調整
3. **穩定性**：實作穩定性測試確保 deterministic
4. **Debug 能力**：完整的 logging 系統方便問題定位
5. **技術選型**：cosine similarity + top-k retrieval

