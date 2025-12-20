# 摘要與QA API

一個使用 FastAPI 和 OpenAI 構建的文本摘要與智能問答 API。

## 功能特點

- 📝 **文本摘要**: 將長文本自動生成簡潔摘要
- 💬 **智能問答**: 根據提供的上下文回答問題
- 🌐 **多語言支持**: 支持繁體中文、簡體中文、英文
- 📚 **自動文檔**: 內建 Swagger UI 互動式文檔

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 為 `.env` 並填入您的 OpenAI API Key：

```bash
cp .env.example .env
```

編輯 `.env` 文件：
```
OPENAI_API_KEY=your_actual_api_key_here
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

## API 端點

### 基本端點

| 方法 | 端點 | 說明 |
|------|------|------|
| GET | `/` | API 歡迎頁面 |
| GET | `/health` | 健康檢查 |
| GET | `/docs` | Swagger UI 文檔 |

### 核心功能

#### 文本摘要 - POST `/api/summary`

**請求範例：**
```json
{
  "text": "人工智能（AI）是計算機科學的一個分支，致力於創建能夠執行通常需要人類智能的任務的系統。這些任務包括學習、推理、問題解決、感知和語言理解。AI 技術已經在醫療、金融、交通等多個領域得到廣泛應用。",
  "max_length": 100,
  "language": "zh-TW"
}
```

**回應範例：**
```json
{
  "original_length": 120,
  "summary": "人工智能是計算機科學分支，旨在創建執行學習、推理等人類智能任務的系統，已廣泛應用於醫療、金融、交通等領域。",
  "summary_length": 52
}
```

#### 智能問答 - POST `/api/qa`

**請求範例：**
```json
{
  "context": "台北101大樓位於台灣台北市信義區，樓高509.2公尺，地上101層，地下5層。於2004年完工，曾是世界最高建築。",
  "question": "台北101有多高？",
  "language": "zh-TW"
}
```

**回應範例：**
```json
{
  "question": "台北101有多高？",
  "answer": "台北101樓高509.2公尺。",
  "confidence": "high"
}
```

## 參數說明

### 摘要 API 參數

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| text | string | ✅ | - | 需要摘要的文本（最少10字） |
| max_length | int | ❌ | 200 | 摘要最大長度（50-1000字） |
| language | string | ❌ | zh-TW | 輸出語言 |

### 問答 API 參數

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| context | string | ✅ | - | 上下文/文檔內容（最少10字） |
| question | string | ✅ | - | 要回答的問題（最少3字） |
| language | string | ❌ | zh-TW | 輸出語言 |

### 支持的語言

- `zh-TW` - 繁體中文
- `zh-CN` - 簡體中文
- `en` - 英文

## 使用 cURL 測試

### 摘要測試
```bash
curl -X POST "http://localhost:8000/api/summary" \
  -H "Content-Type: application/json" \
  -d '{"text": "這是一段很長的測試文本...", "max_length": 100}'
```

### 問答測試
```bash
curl -X POST "http://localhost:8000/api/qa" \
  -H "Content-Type: application/json" \
  -d '{"context": "台北101樓高509.2公尺。", "question": "台北101有多高？"}'
```

## 技術棧

- **FastAPI** - 高性能 Python Web 框架
- **OpenAI GPT-3.5** - AI 語言模型
- **Pydantic** - 數據驗證
- **Uvicorn** - ASGI 伺服器

## 授權

MIT License

