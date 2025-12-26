# GitHub 倉庫更新腳本
# 用於更新三個 GitHub 倉庫

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub 倉庫更新腳本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 設置路徑
$abstractPath = "C:\Users\samue\OneDrive\桌面\Abstract"
$baseReposPath = "C:\Users\samue"  # 根據你的實際倉庫位置調整

# 倉庫路徑（請根據實際位置修改）
$ragRepo = Join-Path $baseReposPath "RAG-Summary-QA-API"
$aiRepo = Join-Path $baseReposPath "AI-prediction"
$game2048Repo = Join-Path $baseReposPath "2048"

# 檢查倉庫是否存在
function Test-RepoExists {
    param($repoPath, $repoName)
    
    if (-not (Test-Path $repoPath)) {
        Write-Host "❌ $repoName 倉庫不存在: $repoPath" -ForegroundColor Red
        Write-Host "   請先克隆倉庫或修改路徑" -ForegroundColor Yellow
        return $false
    }
    
    if (-not (Test-Path (Join-Path $repoPath ".git"))) {
        Write-Host "❌ $repoPath 不是 Git 倉庫" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# 更新 RAG 倉庫
function Update-RAGRepo {
    Write-Host ""
    Write-Host "📦 更新 RAG-Summary-QA-API..." -ForegroundColor Green
    
    if (-not (Test-RepoExists $ragRepo "RAG-Summary-QA-API")) {
        return
    }
    
    Set-Location $ragRepo
    
    # 複製文件
    Write-Host "   複製文件..." -ForegroundColor Yellow
    
    # 核心文件
    Copy-Item "$abstractPath\main.py" -Destination "." -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\config.py" -Destination "." -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\models.py" -Destination "." -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\README.md" -Destination "." -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\README_穩定性與Debug.md" -Destination "." -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\requirements_rag.txt" -Destination "requirements.txt" -Force -ErrorAction SilentlyContinue
    
    # 目錄
    $dirs = @("ingest", "vectorstore", "retriever", "llm", "routes", "services", "tests", "utils")
    foreach ($dir in $dirs) {
        if (Test-Path "$abstractPath\$dir") {
            if (Test-Path "$ragRepo\$dir") {
                Remove-Item "$ragRepo\$dir" -Recurse -Force -ErrorAction SilentlyContinue
            }
            Copy-Item "$abstractPath\$dir" -Destination "$ragRepo" -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "   ✓ 複製 $dir/" -ForegroundColor Gray
        }
    }
    
    # Git 操作
    Write-Host "   Git 操作..." -ForegroundColor Yellow
    git add . 2>&1 | Out-Null
    $status = git status --short
    if ($status) {
        git commit -m "Update: Add stability tests and debug logging system

- Add stability_test.py for embedding, chunking, retrieval consistency
- Add debug_logger.py for RAG session logging
- Update README with stability testing documentation
- Improve code organization and documentation" 2>&1 | Out-Null
        
        Write-Host "   ✓ 已提交更改" -ForegroundColor Green
        Write-Host "   ⚠️  請手動執行: git push origin main" -ForegroundColor Yellow
    } else {
        Write-Host "   ℹ️  沒有更改需要提交" -ForegroundColor Gray
    }
}

# 更新 AI-prediction 倉庫
function Update-AIRepo {
    Write-Host ""
    Write-Host "📦 更新 AI-prediction..." -ForegroundColor Green
    
    if (-not (Test-RepoExists $aiRepo "AI-prediction")) {
        return
    }
    
    Set-Location $aiRepo
    
    # 複製文件
    Write-Host "   複製文件..." -ForegroundColor Yellow
    
    if (Test-Path "$abstractPath\ai_predict") {
        if (Test-Path "$aiRepo\ai_predict") {
            Remove-Item "$aiRepo\ai_predict" -Recurse -Force -ErrorAction SilentlyContinue
        }
        Copy-Item "$abstractPath\ai_predict" -Destination "$aiRepo" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "   ✓ 複製 ai_predict/" -ForegroundColor Gray
    }
    
    Copy-Item "$abstractPath\main_ai_predict.py" -Destination "." -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\README_AI_Predict.md" -Destination "README.md" -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\requirements_ai.txt" -Destination "requirements.txt" -Force -ErrorAction SilentlyContinue
    
    # Git 操作
    Write-Host "   Git 操作..." -ForegroundColor Yellow
    git add . 2>&1 | Out-Null
    $status = git status --short
    if ($status) {
        git commit -m "Update: Add layered architecture for AI prediction model

- Add data preprocessing layer (DataPreprocessor)
- Add feature extraction layer (FeatureExtractor)
- Add model prediction layer (Predictor)
- Support multiple model types (linear, random_forest)
- Complete evaluation metrics (MSE, MAE, RMSE, R²)
- Feature importance analysis" 2>&1 | Out-Null
        
        Write-Host "   ✓ 已提交更改" -ForegroundColor Green
        Write-Host "   ⚠️  請手動執行: git push origin main" -ForegroundColor Yellow
    } else {
        Write-Host "   ℹ️  沒有更改需要提交" -ForegroundColor Gray
    }
}

# 更新 2048 倉庫
function Update-2048Repo {
    Write-Host ""
    Write-Host "📦 更新 2048..." -ForegroundColor Green
    
    if (-not (Test-RepoExists $game2048Repo "2048")) {
        return
    }
    
    Set-Location $game2048Repo
    
    # 複製文件
    Write-Host "   複製文件..." -ForegroundColor Yellow
    
    if (Test-Path "$abstractPath\game_2048") {
        if (Test-Path "$game2048Repo\game_2048") {
            Remove-Item "$game2048Repo\game_2048" -Recurse -Force -ErrorAction SilentlyContinue
        }
        Copy-Item "$abstractPath\game_2048" -Destination "$game2048Repo" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "   ✓ 複製 game_2048/" -ForegroundColor Gray
    }
    
    Copy-Item "$abstractPath\main_2048.py" -Destination "." -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\README_2048.md" -Destination "README.md" -Force -ErrorAction SilentlyContinue
    Copy-Item "$abstractPath\requirements_2048.txt" -Destination "requirements.txt" -Force -ErrorAction SilentlyContinue
    
    # Git 操作
    Write-Host "   Git 操作..." -ForegroundColor Yellow
    git add . 2>&1 | Out-Null
    $status = git status --short
    if ($status) {
        git commit -m "Update: Add layered architecture for 2048 game

- Add GameBoard layer (state management)
- Add MoveHandler layer (move logic with rotation technique)
- Add ScoreCalculator layer (score and statistics)
- Support random seed for reproducibility
- Improve code organization and documentation" 2>&1 | Out-Null
        
        Write-Host "   ✓ 已提交更改" -ForegroundColor Green
        Write-Host "   ⚠️  請手動執行: git push origin main" -ForegroundColor Yellow
    } else {
        Write-Host "   ℹ️  沒有更改需要提交" -ForegroundColor Gray
    }
}

# 主程序
Write-Host "請確認倉庫路徑是否正確：" -ForegroundColor Yellow
Write-Host "  RAG: $ragRepo" -ForegroundColor Gray
Write-Host "  AI: $aiRepo" -ForegroundColor Gray
Write-Host "  2048: $game2048Repo" -ForegroundColor Gray
Write-Host ""
$confirm = Read-Host "是否繼續？(Y/N)"

if ($confirm -eq "Y" -or $confirm -eq "y") {
    Update-RAGRepo
    Update-AIRepo
    Update-2048Repo
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "✅ 更新完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  重要：請手動執行以下命令推送更改：" -ForegroundColor Yellow
    Write-Host "  cd $ragRepo" -ForegroundColor Gray
    Write-Host "  git push origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  cd $aiRepo" -ForegroundColor Gray
    Write-Host "  git push origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  cd $game2048Repo" -ForegroundColor Gray
    Write-Host "  git push origin main" -ForegroundColor Gray
} else {
    Write-Host "已取消" -ForegroundColor Yellow
}

