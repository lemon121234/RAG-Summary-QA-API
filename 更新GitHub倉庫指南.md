# 更新 GitHub 倉庫指南

根據你的 GitHub 倉庫：https://github.com/lemon121234

你已經有三個倉庫：
1. **RAG-Summary-QA-API** - RAG 專案
2. **AI-prediction** - AI 預測模型
3. **2048** - 2048 遊戲

---

## 📋 更新步驟

### 方法 1：使用 Git 命令行（推薦）

#### 1. RAG-Summary-QA-API 倉庫

```bash
# 進入專案目錄
cd /path/to/Abstract

# 如果還沒有克隆，先克隆倉庫
git clone https://github.com/lemon121234/RAG-Summary-QA-API.git
cd RAG-Summary-QA-API

# 或者如果已經有本地倉庫，添加遠程
git remote add origin https://github.com/lemon121234/RAG-Summary-QA-API.git
```

**需要複製的文件：**
```bash
# 從 Abstract 目錄複製以下文件到 RAG-Summary-QA-API 目錄
# RAG 專案核心文件
- main.py
- config.py
- models.py
- requirements.txt (只包含 RAG 的依賴)
- README.md (RAG 專案的 README)
- README_穩定性與Debug.md

# 目錄
- ingest/
- vectorstore/
- retriever/
- llm/
- routes/
- services/
- tests/
- utils/
```

**更新步驟：**
```bash
# 複製文件後
git add .
git commit -m "Add stability tests and debug logging system"
git push origin main
```

---

#### 2. AI-prediction 倉庫

```bash
# 克隆或進入倉庫
git clone https://github.com/lemon121234/AI-prediction.git
cd AI-prediction

# 或添加遠程
git remote add origin https://github.com/lemon121234/AI-prediction.git
```

**需要複製的文件：**
```bash
# 從 Abstract 目錄複製以下文件到 AI-prediction 目錄
- ai_predict/ (整個目錄)
- main_ai_predict.py
- README_AI_Predict.md (重命名為 README.md)

# 創建新的 requirements.txt (只包含 AI 預測的依賴)
numpy>=1.20.0
scikit-learn>=1.0.0
```

**更新步驟：**
```bash
# 複製文件後
git add .
git commit -m "Add layered architecture: data preprocessing, feature extraction, model prediction"
git push origin main
```

---

#### 3. 2048 倉庫

```bash
# 克隆或進入倉庫
git clone https://github.com/lemon121234/2048.git
cd 2048

# 或添加遠程
git remote add origin https://github.com/lemon121234/2048.git
```

**需要複製的文件：**
```bash
# 從 Abstract 目錄複製以下文件到 2048 目錄
- game_2048/ (整個目錄)
- main_2048.py
- README_2048.md (重命名為 README.md)

# 創建新的 requirements.txt (只包含 2048 的依賴)
numpy>=1.20.0
```

**更新步驟：**
```bash
# 複製文件後
git add .
git commit -m "Add layered architecture: board, move handler, score calculator"
git push origin main
```

---

## 🔧 詳細操作步驟

### 步驟 1：準備文件

#### 為 RAG-Summary-QA-API 創建 requirements.txt

創建文件 `requirements_rag.txt`：
```
fastapi>=0.100.0
uvicorn>=0.20.0
python-dotenv>=1.0.0
pydantic>=2.0.0
httpx>=0.24.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

#### 為 AI-prediction 創建 requirements.txt

創建文件 `requirements_ai.txt`：
```
numpy>=1.20.0
scikit-learn>=1.0.0
```

#### 為 2048 創建 requirements.txt

創建文件 `requirements_2048.txt`：
```
numpy>=1.20.0
```

---

### 步驟 2：更新 RAG-Summary-QA-API

```bash
# 1. 進入 RAG 倉庫目錄
cd RAG-Summary-QA-API

# 2. 從 Abstract 目錄複製文件
# (在 Windows 上可以使用文件管理器複製，或使用以下命令)

# 3. 確認文件已複製
ls -la  # Linux/Mac
dir     # Windows

# 4. 添加並提交
git add .
git status  # 檢查要提交的文件
git commit -m "Update: Add stability tests and debug logging system

- Add stability_test.py for embedding, chunking, retrieval consistency
- Add debug_logger.py for RAG session logging
- Update README with stability testing documentation
- Improve code organization and documentation"

# 5. 推送到 GitHub
git push origin main
```

---

### 步驟 3：更新 AI-prediction

```bash
# 1. 進入 AI-prediction 倉庫目錄
cd AI-prediction

# 2. 從 Abstract 目錄複製文件
# - ai_predict/ 目錄
# - main_ai_predict.py
# - README_AI_Predict.md (重命名為 README.md)

# 3. 創建 requirements.txt (使用 requirements_ai.txt 的內容)

# 4. 添加並提交
git add .
git commit -m "Update: Add layered architecture

- Add data preprocessing layer (DataPreprocessor)
- Add feature extraction layer (FeatureExtractor)
- Add model prediction layer (Predictor)
- Support multiple model types (linear, random_forest)
- Complete evaluation metrics (MSE, MAE, RMSE, R²)
- Feature importance analysis"

# 5. 推送到 GitHub
git push origin main
```

---

### 步驟 4：更新 2048

```bash
# 1. 進入 2048 倉庫目錄
cd 2048

# 2. 從 Abstract 目錄複製文件
# - game_2048/ 目錄
# - main_2048.py
# - README_2048.md (重命名為 README.md)

# 3. 創建 requirements.txt (使用 requirements_2048.txt 的內容)

# 4. 添加並提交
git add .
git commit -m "Update: Add layered architecture

- Add GameBoard layer (state management)
- Add MoveHandler layer (move logic with rotation technique)
- Add ScoreCalculator layer (score and statistics)
- Support random seed for reproducibility
- Improve code organization and documentation"

# 5. 推送到 GitHub
git push origin main
```

---

## 📝 文件對應表

### RAG-Summary-QA-API 倉庫

| Abstract 目錄 | RAG-Summary-QA-API 倉庫 |
|--------------|------------------------|
| `main.py` | `main.py` |
| `config.py` | `config.py` |
| `models.py` | `models.py` |
| `requirements.txt` (RAG部分) | `requirements.txt` |
| `README.md` | `README.md` |
| `README_穩定性與Debug.md` | `README_穩定性與Debug.md` |
| `ingest/` | `ingest/` |
| `vectorstore/` | `vectorstore/` |
| `retriever/` | `retriever/` |
| `llm/` | `llm/` |
| `routes/` | `routes/` |
| `services/` | `services/` |
| `tests/stability_test.py` | `tests/stability_test.py` |
| `utils/debug_logger.py` | `utils/debug_logger.py` |

### AI-prediction 倉庫

| Abstract 目錄 | AI-prediction 倉庫 |
|--------------|-------------------|
| `ai_predict/` | `ai_predict/` |
| `main_ai_predict.py` | `main_ai_predict.py` |
| `README_AI_Predict.md` | `README.md` |
| `requirements_ai.txt` | `requirements.txt` |

### 2048 倉庫

| Abstract 目錄 | 2048 倉庫 |
|--------------|----------|
| `game_2048/` | `game_2048/` |
| `main_2048.py` | `main_2048.py` |
| `README_2048.md` | `README.md` |
| `requirements_2048.txt` | `requirements.txt` |

---

## 🚀 快速更新腳本（Windows PowerShell）

創建 `update_repos.ps1`：

```powershell
# 設置路徑
$abstractPath = "C:\Users\samue\OneDrive\桌面\Abstract"
$ragRepo = "C:\path\to\RAG-Summary-QA-API"
$aiRepo = "C:\path\to\AI-prediction"
$game2048Repo = "C:\path\to\2048"

# 更新 RAG 倉庫
Write-Host "Updating RAG-Summary-QA-API..."
Set-Location $ragRepo
Copy-Item "$abstractPath\main.py" -Force
Copy-Item "$abstractPath\config.py" -Force
Copy-Item "$abstractPath\models.py" -Force
Copy-Item "$abstractPath\README.md" -Force
Copy-Item "$abstractPath\README_穩定性與Debug.md" -Force
# ... 複製其他文件
git add .
git commit -m "Update: Add stability tests and debug logging"
git push origin main

# 更新 AI-prediction 倉庫
Write-Host "Updating AI-prediction..."
Set-Location $aiRepo
Copy-Item "$abstractPath\ai_predict" -Recurse -Force
Copy-Item "$abstractPath\main_ai_predict.py" -Force
Copy-Item "$abstractPath\README_AI_Predict.md" -Destination "README.md" -Force
git add .
git commit -m "Update: Add layered architecture"
git push origin main

# 更新 2048 倉庫
Write-Host "Updating 2048..."
Set-Location $game2048Repo
Copy-Item "$abstractPath\game_2048" -Recurse -Force
Copy-Item "$abstractPath\main_2048.py" -Force
Copy-Item "$abstractPath\README_2048.md" -Destination "README.md" -Force
git add .
git commit -m "Update: Add layered architecture"
git push origin main

Write-Host "All repositories updated!"
```

---

## ✅ 更新後檢查

### 檢查 RAG-Summary-QA-API

訪問：https://github.com/lemon121234/RAG-Summary-QA-API

確認：
- [ ] `tests/stability_test.py` 存在
- [ ] `utils/debug_logger.py` 存在
- [ ] `README_穩定性與Debug.md` 存在
- [ ] README.md 包含穩定性測試說明

### 檢查 AI-prediction

訪問：https://github.com/lemon121234/AI-prediction

確認：
- [ ] `ai_predict/` 目錄存在
- [ ] `main_ai_predict.py` 存在
- [ ] README.md 說明分層架構

### 檢查 2048

訪問：https://github.com/lemon121234/2048

確認：
- [ ] `game_2048/` 目錄存在
- [ ] `main_2048.py` 存在
- [ ] README.md 說明分層架構

---

## 🎯 提交信息建議

### RAG-Summary-QA-API

```
Update: Add stability tests and debug logging system

- Add stability_test.py for embedding, chunking, retrieval consistency
- Add debug_logger.py for RAG session logging
- Update README with stability testing documentation
- Improve code organization and documentation
```

### AI-prediction

```
Update: Add layered architecture for AI prediction model

- Add data preprocessing layer (DataPreprocessor)
- Add feature extraction layer (FeatureExtractor)
- Add model prediction layer (Predictor)
- Support multiple model types (linear, random_forest)
- Complete evaluation metrics (MSE, MAE, RMSE, R²)
- Feature importance analysis
```

### 2048

```
Update: Add layered architecture for 2048 game

- Add GameBoard layer (state management)
- Add MoveHandler layer (move logic with rotation technique)
- Add ScoreCalculator layer (score and statistics)
- Support random seed for reproducibility
- Improve code organization and documentation
```

---

## 📞 遇到問題？

### 問題 1：遠程倉庫已存在

```bash
# 檢查現有遠程
git remote -v

# 如果已存在，更新 URL
git remote set-url origin https://github.com/lemon121234/倉庫名.git
```

### 問題 2：分支名稱不同

```bash
# 檢查當前分支
git branch

# 如果主分支是 master 而不是 main
git push origin master
```

### 問題 3：需要強制推送

```bash
# 謹慎使用！只在確定時使用
git push -f origin main
```

---

## 🎉 完成後

更新完成後，你的三個 GitHub 倉庫將包含：
- ✅ 完整的模組化代碼
- ✅ 清晰的 README 說明
- ✅ 穩定性測試（RAG）
- ✅ 分層架構設計（所有專案）

這樣面試官就可以看到你的代碼組織能力和工程思維了！

