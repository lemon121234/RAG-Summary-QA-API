# 測試腳本說明

這個目錄包含 RAG 專案的測試和工具腳本。

## 📋 腳本列表

### 測試腳本

1. **test_rag_queries.py** - 測試 RAG 問答功能
   ```bash
   python scripts/test_rag_queries.py
   ```

2. **test_retrieval.py** - 測試檢索功能
   ```bash
   python scripts/test_retrieval.py
   ```

3. **test_upload_single.py** - 測試單個文檔上傳
   ```bash
   python scripts/test_upload_single.py
   ```

### 工具腳本

4. **upload_test_documents.py** - 批量上傳測試文檔
   ```bash
   python scripts/upload_test_documents.py
   ```

5. **upload_from_json.py** - 從 JSON 文件批量上傳文檔
   ```bash
   python scripts/upload_from_json.py
   ```

### 測試資料

6. **test_questions.md** - RAG 測試問題集
   - 包含測試問題和預期答案
   - 可用於驗證系統功能

## 🚀 使用前準備

1. 確保 API 服務器正在運行：
   ```bash
   python main.py
   ```

2. 確保已上傳測試文檔到知識庫

3. 根據需要修改腳本中的 API 地址（預設為 `http://localhost:8001`）

## 📝 注意事項

- 這些腳本主要用於開發和測試
- 在運行測試前，請確保 Ollama 服務正常運行
- 某些腳本可能需要先上傳測試文檔

