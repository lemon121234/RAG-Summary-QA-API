# RAG 摘要與QA API

一個使用 FastAPI 和 Ollama 構建的 RAG（檢索增強生成）系統，支援多文檔上傳、向量檢索、智能問答、URL 摘要等功能。

## 🎯 功能特點

- 🤖 **RAG 問答**: 使用檢索增強生成技術，根據知識庫回答問題
- 📚 **多文檔管理**: 上傳、查詢、刪除文檔，自動建立向量索引
- 🔍 **向量語義搜索**: 使用嵌入向量進行相似度搜索
- 📝 **智能摘要**: 文檔摘要和 URL 內容摘要
- 🌐 **URL 問答**: 直接對網頁內容進行問答
- 🌍 **多語言支持**: 支持繁體中文、簡體中文、英文

## 📁 專案結構

本專案採用**分層架構**，按照 RAG 流程組織代碼：

```
rag_app/
├── main.py              # FastAPI 初始化和路由註冊
├── config.py            # 配置模組
├── models.py            # 數據模型（Pydantic）
│
├── ingest/              # 資料攝取層
│   ├── splitter.py      # 文本切割
│   └── embedder.py      # 嵌入向量生成
│
├── vectorstore/         # 向量存儲層
│   └── store.py         # 向量資料庫操作
│
├── retriever/           # 檢索層
│   └── search.py        # 相似度搜尋
│
├── llm/                 # 生成層
│   ├── qa.py           # RAG 問答
│   └── summarizer.py   # 摘要生成
│
├── services/            # 業務邏輯層
│   └── url_service.py  # URL 處理
│
└── routes/              # API 路由層
    ├── documents.py    # 文檔管理
    ├── rag.py          # RAG 問答
    ├── summary.py      # 摘要
    └── url.py          # URL 功能
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 安裝並啟動 Ollama

下載並安裝 [Ollama](https://ollama.ai/)

啟動 Ollama 服務：
```bash
ollama serve
```

下載所需的模型：
```bash
ollama pull llama3.2          # LLM 模型
ollama pull nomic-embed-text   # 嵌入模型
```

### 3. 啟動伺服器

```bash
python main.py
```

或使用 uvicorn：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

伺服器將在 `http://localhost:8000` 啟動。

## 📚 API 端點

### 基本端點

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/` | API 歡迎頁面 |
| GET | `/health` | 健康檢查 |
| GET | `/docs` | Swagger UI 文檔 |

### 文檔管理

#### 上傳文檔 - POST `/api/documents`

**請求範例：**
```json
{
  "title": "AI 介紹",
  "content": "人工智能（AI）是計算機科學的一個分支..."
}
```

#### 列出文檔 - GET `/api/documents`

#### 獲取文檔 - GET `/api/documents/{document_id}`

#### 刪除文檔 - DELETE `/api/documents/{document_id}`

### RAG 問答

#### RAG 問答 - POST `/api/rag/query`

**請求範例：**
```json
{
  "question": "AI 是什麼？",
  "top_k": 5,
  "language": "zh-TW"
}
```

**回應範例：**
```json
{
  "question": "AI 是什麼？",
  "answer": "根據資料，AI 是...",
  "sources": [
    {
      "document_title": "AI 介紹",
      "content": "...",
      "relevance_score": 0.85
    }
  ],
  "confidence": "high"
}
```

### 摘要功能

#### 文檔摘要 - POST `/api/summary`

**請求範例：**
```json
{
  "document_id": "abc12345",
  "max_length": 200,
  "language": "zh-TW"
}
```

#### URL 摘要 - POST `/api/url/summary`

**請求範例：**
```json
{
  "url": ["https://example.com/article1", "https://example.com/article2"],
  "max_length": 200,
  "language": "zh-TW"
}
```

### URL 問答

#### URL 問答 - POST `/api/url/qa`

**請求範例：**
```json
{
  "url": "https://example.com/article",
  "question": "這篇文章的主要觀點是什麼？",
  "language": "zh-TW"
}
```

## 🔧 配置

可以在 `config.py` 中修改配置，或使用環境變數：

- `OLLAMA_BASE_URL`: Ollama 服務地址（預設: `http://localhost:11434`）
- `OLLAMA_MODEL`: LLM 模型名稱（預設: `llama3.2`）
- `EMBEDDING_MODEL`: 嵌入模型名稱（預設: `nomic-embed-text`）
- `CHUNK_SIZE`: 文本片段大小（預設: 500）
- `CHUNK_OVERLAP`: 片段重疊大小（預設: 50）
- `TOP_K`: 檢索返回的片段數量（預設: 5）

## 🎓 RAG 架構說明

本專案採用**分層架構**，按照 RAG 流程組織：

1. **ingest 層**: 資料攝取（文本切割、向量嵌入）
2. **vectorstore 層**: 向量存儲（文檔和向量管理）
3. **retriever 層**: 檢索（相似度搜索）
4. **llm 層**: 生成（prompt 構建、LLM 調用）
5. **routes 層**: API 路由（HTTP 端點）

這種架構的優點：
- ✅ 職責分離，每個層只負責一個功能
- ✅ 易於擴展，例如想換向量資料庫只需修改 `vectorstore/` 層
- ✅ 易於測試，每個層可以獨立測試
- ✅ 符合業界標準，這是生產環境常見的 RAG 架構

## 📊 技術棧

- **FastAPI** - 高性能 Python Web 框架
- **Ollama** - 本地 LLM 和嵌入模型
- **Pydantic** - 數據驗證
- **Uvicorn** - ASGI 伺服器
- **BeautifulSoup** - 網頁內容提取
- **httpx** - 異步 HTTP 客戶端

## 📝 使用範例

### 完整工作流程

1. **上傳文檔**
```bash
curl -X POST "http://localhost:8000/api/documents" \
  -H "Content-Type: application/json" \
  -d '{"title": "測試文檔", "content": "這是一段很長的測試文本..."}'
```

2. **RAG 問答**
```bash
curl -X POST "http://localhost:8000/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "測試文檔的主要內容是什麼？"}'
```

3. **生成摘要**
```bash
curl -X POST "http://localhost:8000/api/summary" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "abc12345", "max_length": 100}'
```

## 🔍 健康檢查

訪問 `/health` 端點可以檢查系統狀態：

```bash
curl http://localhost:8000/health
```

回應包含：
- Ollama 連接狀態
- 嵌入模型狀態
- 文檔和片段數量

## 🧪 穩定性測試與 Debug

本專案包含完整的穩定性測試和 debug logging 系統。

### 穩定性測試

執行穩定性測試：
```bash
python tests/stability_test.py
```

測試內容：
- **Embedding 一致性測試**：驗證同一文本多次生成 embedding 是否相同
- **Chunking 一致性測試**：驗證同一文本多次切割是否產生相同的 chunks
- **Retrieval 一致性測試**：驗證同一 query 多次檢索結果是否相同

詳細說明請參考 [README_穩定性與Debug.md](README_穩定性與Debug.md)

### Debug Logging

每次 RAG 查詢都會自動記錄到：
- 控制台輸出
- `rag_debug.log` 文本日誌
- `debug_logs/session_*.json` 結構化記錄

詳細說明請參考 [README_穩定性與Debug.md](README_穩定性與Debug.md)

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！
