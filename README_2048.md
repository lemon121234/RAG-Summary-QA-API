# 2048 遊戲

一個使用 Python 實現的 2048 遊戲，採用分層架構設計，職責清晰，易於理解和擴展。

## 🎯 專案特點

- 🏗️ **分層架構**：遊戲板層、移動邏輯層、得分計算層
- 🔄 **統一移動處理**：通過旋轉技巧將四方向移動統一為一個實現
- 🎲 **可重現性**：支持隨機種子，確保遊戲狀態可重現
- 📊 **統計分析**：提供豐富的遊戲統計信息

## 📁 專案結構

```
game_2048/
├── __init__.py          # 模組導出
├── board.py             # 遊戲板層（狀態管理）
├── move.py              # 移動邏輯層（操作處理）
└── score.py             # 得分計算層（統計分析）

main_2048.py             # 主入口
```

## 🚀 快速開始

### 安裝依賴

```bash
pip install numpy
```

### 運行遊戲

```bash
python main_2048.py
```

## 🏗️ 架構設計

### 1. GameBoard（遊戲板層）

負責遊戲板的初始化和狀態管理：
- 遊戲板初始化
- 隨機方塊生成
- 遊戲狀態檢查（是否可移動、是否已滿）

**關鍵特性：**
- 支持隨機種子，確保可重現性
- 提供 `can_move()` 方法檢查遊戲是否結束
- 支持遊戲板複製

### 2. MoveHandler（移動邏輯層）

負責處理遊戲的移動邏輯：
- 四方向移動（上下左右）
- 方塊合併邏輯
- 得分計算

**關鍵特性：**
- 通過旋轉技巧統一處理四方向移動
- 返回移動是否成功，避免無效移動
- 計算每次移動的得分增量

### 3. ScoreCalculator（得分計算層）

負責得分計算和統計：
- 當前得分計算
- 遊戲統計信息
- 潛在得分估算（用於 AI 策略）

**關鍵特性：**
- 使用靜態方法，不依賴實例狀態
- 提供豐富的統計信息（最大方塊、空格數量、填充率等）

## 💡 設計亮點

### 統一移動處理

通過旋轉遊戲板，將四個方向的移動統一轉換為向左移動：

```python
# 根據方向旋轉遊戲板，統一處理為向左移動
if direction == 'right':
    new_board.board = np.fliplr(new_board.board)
elif direction == 'up':
    new_board.board = np.rot90(new_board.board, k=-1)
elif direction == 'down':
    new_board.board = np.rot90(new_board.board, k=1)

# 執行向左移動邏輯
# ...

# 還原旋轉
```

這樣只需要實現一次合併邏輯，大大減少了代碼重複，符合 DRY（Don't Repeat Yourself）原則。

### 可重現性

支持隨機種子參數，確保遊戲狀態可重現：

```python
board = GameBoard(size=4, seed=42)  # 固定種子
```

這對於測試和調試非常重要。

## 📊 使用範例

```python
from game_2048 import GameBoard, MoveHandler, ScoreCalculator

# 初始化遊戲板
board = GameBoard(size=4, seed=42)

# 執行移動
new_board, score_delta, moved = MoveHandler.move_left(board)

if moved:
    board = new_board
    board._add_random_tile()  # 移動成功後添加新方塊
    print(f"得分增加：{score_delta}")

# 獲取統計信息
stats = ScoreCalculator.get_statistics(board)
print(f"最大方塊：{stats['max_tile']}")
print(f"空格數量：{stats['empty_cells']}")
```

## 🎯 面試重點

### 分層架構
> 「我將 2048 遊戲設計為三層架構：`GameBoard` 負責遊戲板狀態管理，`MoveHandler` 負責移動邏輯處理，`ScoreCalculator` 負責得分計算和統計。每個模組職責單一，符合單一職責原則（SRP）。」

### 設計模式
> 「我使用旋轉技巧將四方向移動統一為一個實現，減少代碼重複。這體現了 DRY 原則和代碼復用。」

### 可重現性
> 「`GameBoard` 支持隨機種子參數，確保遊戲狀態可重現，這對於測試和調試非常重要。」

## 📄 授權

MIT License

