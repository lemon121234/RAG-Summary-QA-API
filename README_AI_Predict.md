# AI 預測模型

一個使用 Python 實現的 AI 預測模型框架，採用分層架構設計，支持完整的機器學習流程：數據預處理、特徵提取、模型訓練和評估。

## 🎯 專案特點

- 🏗️ **分層架構**：數據預處理層、特徵提取層、模型層
- 🔧 **數據處理**：支持標準化、異常值處理、缺失值處理
- 🎯 **特徵工程**：多種特徵提取方法（基本統計、時間序列、交互特徵）
- 📊 **模型評估**：完整的評估指標（MSE、MAE、RMSE、R²）
- 🔍 **特徵重要性**：支持特徵重要性分析

## 📁 專案結構

```
ai_predict/
├── __init__.py
├── data/
│   ├── __init__.py
│   ├── preprocessor.py      # 數據預處理層
│   └── feature_extractor.py # 特徵提取層
└── model/
    ├── __init__.py
    └── predictor.py         # 模型層

main_ai_predict.py          # 主入口
```

## 🚀 快速開始

### 安裝依賴

```bash
pip install numpy scikit-learn
```

### 運行示例

```bash
python main_ai_predict.py
```

## 🏗️ 架構設計

### 1. DataPreprocessor（數據預處理層）

負責數據清洗和標準化：
- 數據標準化（Z-score）
- 異常值處理（Z-score 方法）
- 缺失值處理（均值、中位數、零值填充）

**關鍵特性：**
- 採用 fit/transform 模式，確保訓練集和測試集使用相同的標準化參數
- 避免數據洩漏（data leakage）
- 支持多種缺失值處理策略

### 2. FeatureExtractor（特徵提取層）

負責特徵工程：
- 基本統計特徵（均值、標準差、最大值、最小值、中位數）
- 時間序列特徵（移動平均、變化率）
- 交互特徵（特徵乘積、比值）

**關鍵特性：**
- 支持一維和多維數據
- 可以靈活組合多種特徵類型
- 靜態方法設計，易於測試

### 3. Predictor（模型層）

負責模型訓練、預測和評估：
- 支持多種模型類型（線性回歸、隨機森林等）
- 完整的評估指標
- 特徵重要性分析

**關鍵特性：**
- 使用策略模式，易於擴展新模型
- 提供完整的評估指標（MSE、MAE、RMSE、R²）
- 支持特徵重要性分析

## 💡 設計亮點

### Fit/Transform 模式

確保訓練集和測試集使用相同的標準化參數：

```python
# 訓練階段
preprocessor = DataPreprocessor(normalize=True)
X_train_processed = preprocessor.fit_transform(X_train)

# 測試階段（使用相同的標準化參數）
X_test_processed = preprocessor.transform(X_test)  # 不重新 fit
```

這避免了數據洩漏，確保模型評估的準確性。

### 多種特徵提取方法

可以根據數據類型靈活組合特徵：

```python
feature_extractor = FeatureExtractor()

# 基本特徵
basic_features = feature_extractor.extract_basic_features(X)

# 時間序列特徵
temporal_features = feature_extractor.extract_temporal_features(X, window_size=3)

# 組合特徵
combined_features = feature_extractor.combine_features(
    basic_features, temporal_features
)
```

### 完整的模型評估

提供多種評估指標：

```python
metrics = predictor.evaluate(X_test, y_test)
# 返回: {'mse': ..., 'mae': ..., 'rmse': ..., 'r2': ...}
```

## 📊 使用範例

```python
from ai_predict import Predictor, DataPreprocessor, FeatureExtractor
import numpy as np

# 1. 數據預處理
preprocessor = DataPreprocessor(normalize=True)
X_processed = preprocessor.fit_transform(X_raw)

# 2. 特徵提取
feature_extractor = FeatureExtractor()
features = feature_extractor.extract_basic_features(X_processed)

# 3. 分割數據
X_train, X_test = X_processed[:80], X_processed[80:]
y_train, y_test = y[:80], y[80:]

# 4. 訓練模型
predictor = Predictor(model_type='random_forest')
train_metrics = predictor.train(X_train, y_train)

# 5. 評估模型
test_metrics = predictor.evaluate(X_test, y_test)
print(f"MSE: {test_metrics['mse']:.2f}")
print(f"R²: {test_metrics['r2']:.3f}")

# 6. 進行預測
predictions = predictor.predict(X_test)
```

## 🎯 面試重點

### 分層架構
> 「我將 AI 預測模型設計為三層：數據預處理層負責數據清洗和標準化，特徵提取層負責特徵工程，模型層負責訓練和預測。每個層都可以獨立測試和替換，符合開閉原則（OCP）。」

### 數據處理
> 「`DataPreprocessor` 採用 fit/transform 模式，確保訓練和測試數據使用相同的標準化參數，避免數據洩漏。同時提供異常值處理功能，使用 Z-score 方法識別和移除異常值。」

### 特徵工程
> 「`FeatureExtractor` 提供多種特徵提取方法：基本統計特徵、時間序列特徵、交互特徵。可以根據數據類型靈活組合，支持一維和多維數據。這體現了特徵工程的重要性，好的特徵往往比複雜的模型更重要。」

### 模型評估
> 「`Predictor` 使用策略模式，支持多種模型類型（線性回歸、隨機森林等），易於擴展。提供完整的評估指標（MSE、MAE、RMSE、R²），並且支持特徵重要性分析，幫助理解模型行為。」

## 📄 授權

MIT License

