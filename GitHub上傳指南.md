# GitHub 上傳指南

## 📋 準備工作

### 1. 檢查 .gitignore

已更新 `.gitignore` 排除以下私人文件：
- 履歷相關的 .md 文件
- Debug logs 目錄
- 日誌文件

### 2. 確認要上傳的文件

**RAG 專案：**
- ✅ 所有 Python 代碼文件
- ✅ `README.md`（已更新包含穩定性測試）
- ✅ `README_穩定性與Debug.md`
- ✅ `requirements.txt`
- ✅ `tests/stability_test.py`
- ✅ `utils/debug_logger.py`

**2048 遊戲：**
- ✅ `game_2048/` 目錄
- ✅ `main_2048.py`
- ✅ `README_2048.md`

**AI 預測模型：**
- ✅ `ai_predict/` 目錄
- ✅ `main_ai_predict.py`
- ✅ `README_AI_Predict.md`

**不會上傳：**
- ❌ `venv/` 目錄
- ❌ `__pycache__/` 目錄
- ❌ 私人文件（履歷相關的 .md）
- ❌ Debug logs

---

## 🚀 上傳步驟

### 方法 1：使用 Git 命令行

#### 1. 初始化 Git 倉庫（如果還沒有）

```bash
# 在專案根目錄執行
git init
```

#### 2. 添加遠程倉庫

```bash
# 替換為你的 GitHub 倉庫 URL
git remote add origin https://github.com/你的用戶名/你的倉庫名.git
```

#### 3. 添加文件

```bash
# 添加所有文件（.gitignore 會自動排除不需要的文件）
git add .

# 檢查要提交的文件
git status
```

#### 4. 提交

```bash
git commit -m "Initial commit: RAG, 2048, AI Predict projects with stability tests"
```

#### 5. 推送到 GitHub

```bash
# 如果是第一次推送
git push -u origin main

# 或如果默認分支是 master
git push -u origin master
```

---

### 方法 2：使用 GitHub Desktop

1. 打開 GitHub Desktop
2. 選擇 "Add" → "Add Existing Repository"
3. 選擇專案目錄
4. 確認要提交的文件（確保排除私人文件）
5. 填寫 commit message
6. 點擊 "Commit to main"
7. 點擊 "Push origin" 推送到 GitHub

---

### 方法 3：分別上傳到不同倉庫

如果你想將三個專案分別上傳到不同的倉庫：

#### RAG 專案倉庫

```bash
# 創建 RAG 專案目錄
mkdir rag-project
cd rag-project

# 複製 RAG 相關文件
# （只複製 RAG 相關的文件，不包括 game_2048 和 ai_predict）

# 初始化並上傳
git init
git add .
git commit -m "RAG project with stability tests"
git remote add origin https://github.com/你的用戶名/rag-project.git
git push -u origin main
```

#### 2048 遊戲倉庫

```bash
# 創建 2048 專案目錄
mkdir 2048-game
cd 2048-game

# 複製 2048 相關文件
# （只複製 game_2048/ 和 main_2048.py）

# 初始化並上傳
git init
git add .
git commit -m "2048 game with layered architecture"
git remote add origin https://github.com/你的用戶名/2048-game.git
git push -u origin main
```

#### AI 預測模型倉庫

```bash
# 創建 AI 預測專案目錄
mkdir ai-predict
cd ai-predict

# 複製 AI 預測相關文件
# （只複製 ai_predict/ 和 main_ai_predict.py）

# 初始化並上傳
git init
git add .
git commit -m "AI prediction model with layered architecture"
git remote add origin https://github.com/你的用戶名/ai-predict.git
git push -u origin main
```

---

## 📝 建議的倉庫結構

### 選項 1：單一倉庫（推薦）

```
your-repo/
├── README.md                    # 主 README（介紹三個專案）
├── README_穩定性與Debug.md      # RAG 穩定性測試說明
├── README_2048.md               # 2048 遊戲說明
├── README_AI_Predict.md         # AI 預測模型說明
├── requirements.txt             # 依賴（RAG 專案）
│
├── main.py                      # RAG 主入口
├── config.py
├── models.py
├── ingest/                      # RAG 專案
├── vectorstore/
├── retriever/
├── llm/
├── routes/
├── services/
├── tests/                       # RAG 穩定性測試
├── utils/                       # RAG debug logger
│
├── game_2048/                   # 2048 遊戲
├── main_2048.py
│
└── ai_predict/                 # AI 預測模型
    └── main_ai_predict.py
```

**優點：**
- 所有專案在一個地方，方便管理
- 可以展示多個專案的架構設計能力

### 選項 2：三個獨立倉庫

- `rag-project` - RAG 專案
- `2048-game` - 2048 遊戲
- `ai-predict` - AI 預測模型

**優點：**
- 每個專案獨立，更專業
- 可以分別設置不同的 README 和說明

---

## ✅ 上傳前檢查清單

- [ ] 確認 `.gitignore` 已更新
- [ ] 確認所有私人文件已排除
- [ ] 確認 `venv/` 和 `__pycache__/` 不會上傳
- [ ] 確認所有 README 文件已創建
- [ ] 確認代碼沒有硬編碼的敏感信息
- [ ] 測試代碼可以正常運行（至少語法正確）

---

## 📚 README 文件說明

### 主 README.md
- 介紹 RAG 專案
- 包含穩定性測試說明

### README_2048.md
- 介紹 2048 遊戲
- 說明架構設計和設計亮點

### README_AI_Predict.md
- 介紹 AI 預測模型
- 說明數據處理和特徵工程

### README_穩定性與Debug.md
- RAG 專案的穩定性測試說明
- Debug logging 使用指南

---

## 🎯 上傳後的建議

1. **添加 Topics**：在 GitHub 倉庫設置中添加 topics，如：
   - `rag`
   - `fastapi`
   - `machine-learning`
   - `python`
   - `nlp`

2. **添加描述**：在倉庫描述中簡要說明專案

3. **添加 License**：如果需要的話，添加 MIT License

4. **添加 Badges**：可以添加一些 badges 顯示專案狀態

---

## 🔧 常見問題

### Q: 如何確認哪些文件會被上傳？

```bash
# 檢查 git status
git status

# 查看會被忽略的文件
git status --ignored
```

### Q: 如何更新已上傳的倉庫？

```bash
# 修改文件後
git add .
git commit -m "Update: 描述你的更改"
git push
```

### Q: 如何從 GitHub 刪除已上傳的私人文件？

```bash
# 從 Git 歷史中刪除文件（但保留本地文件）
git rm --cached 文件名

# 提交更改
git commit -m "Remove private files"

# 推送到 GitHub
git push
```

---

## 📞 需要幫助？

如果遇到問題，可以：
1. 檢查 Git 錯誤信息
2. 確認 GitHub 倉庫權限設置
3. 確認網絡連接正常

