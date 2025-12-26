"""
AI 預測模型模組
負責模型預測和評估
"""
import numpy as np
from typing import Optional, Dict, Tuple
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class Predictor:
    """預測器"""
    
    def __init__(self, model_type: str = 'linear'):
        """
        初始化預測器
        
        Args:
            model_type: 模型類型 ('linear', 'random_forest')
        """
        self.model_type = model_type
        self.model = None
        self.is_trained = False
        
        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"未知的模型類型: {model_type}")
    
    def train(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> Dict[str, float]:
        """
        訓練模型
        
        Args:
            X: 特徵數據
            y: 目標值
        
        Returns:
            訓練指標（如訓練集上的 MSE）
        """
        self.model.fit(X, y)
        self.is_trained = True
        
        # 計算訓練指標
        y_pred = self.model.predict(X)
        metrics = {
            'train_mse': mean_squared_error(y, y_pred),
            'train_mae': mean_absolute_error(y, y_pred),
            'train_r2': r2_score(y, y_pred)
        }
        
        return metrics
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        進行預測
        
        Args:
            X: 特徵數據
        
        Returns:
            預測結果
        """
        if not self.is_trained:
            raise ValueError("模型尚未訓練，請先調用 train()")
        
        return self.model.predict(X)
    
    def evaluate(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> Dict[str, float]:
        """
        評估模型
        
        Args:
            X: 測試特徵數據
            y: 測試目標值
        
        Returns:
            評估指標
        """
        if not self.is_trained:
            raise ValueError("模型尚未訓練，請先調用 train()")
        
        y_pred = self.predict(X)
        
        metrics = {
            'mse': mean_squared_error(y, y_pred),
            'mae': mean_absolute_error(y, y_pred),
            'rmse': np.sqrt(mean_squared_error(y, y_pred)),
            'r2': r2_score(y, y_pred)
        }
        
        return metrics
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """
        獲取特徵重要性（僅適用於某些模型）
        
        Returns:
            特徵重要性數組（如果模型支持）
        """
        if not self.is_trained:
            return None
        
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            return np.abs(self.model.coef_)
        else:
            return None

