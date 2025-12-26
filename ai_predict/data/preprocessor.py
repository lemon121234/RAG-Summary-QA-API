"""
數據預處理模組
負責數據清洗、標準化等操作
"""
import numpy as np
from typing import List, Tuple, Optional


class DataPreprocessor:
    """數據預處理器"""
    
    def __init__(self, normalize: bool = True):
        """
        初始化預處理器
        
        Args:
            normalize: 是否進行標準化
        """
        self.normalize = normalize
        self.mean: Optional[np.ndarray] = None
        self.std: Optional[np.ndarray] = None
        self.fitted = False
    
    def fit(self, data: np.ndarray):
        """
        擬合預處理器（計算均值和標準差）
        
        Args:
            data: 訓練數據
        """
        if self.normalize:
            self.mean = np.mean(data, axis=0)
            self.std = np.std(data, axis=0)
            # 避免除零
            self.std = np.where(self.std == 0, 1, self.std)
        self.fitted = True
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        """
        轉換數據
        
        Args:
            data: 原始數據
        
        Returns:
            處理後的數據
        """
        if not self.fitted:
            raise ValueError("預處理器尚未擬合，請先調用 fit()")
        
        processed = data.copy()
        
        # 標準化
        if self.normalize and self.mean is not None and self.std is not None:
            processed = (processed - self.mean) / self.std
        
        return processed
    
    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        """
        擬合並轉換數據
        
        Args:
            data: 原始數據
        
        Returns:
            處理後的數據
        """
        self.fit(data)
        return self.transform(data)
    
    def remove_outliers(
        self,
        data: np.ndarray,
        threshold: float = 3.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        移除異常值（使用 Z-score 方法）
        
        Args:
            data: 原始數據
            threshold: Z-score 閾值
        
        Returns:
            (清理後的數據, 異常值索引)
        """
        if data.ndim == 1:
            z_scores = np.abs((data - np.mean(data)) / np.std(data))
        else:
            z_scores = np.abs((data - np.mean(data, axis=0)) / np.std(data, axis=0))
            z_scores = np.max(z_scores, axis=1)
        
        outlier_mask = z_scores < threshold
        outliers = np.where(~outlier_mask)[0]
        
        return data[outlier_mask], outliers
    
    def handle_missing_values(
        self,
        data: np.ndarray,
        strategy: str = 'mean'
    ) -> np.ndarray:
        """
        處理缺失值
        
        Args:
            data: 包含缺失值的數據
            strategy: 處理策略 ('mean', 'median', 'zero')
        
        Returns:
            處理後的數據
        """
        processed = data.copy()
        
        if strategy == 'mean':
            fill_value = np.nanmean(processed, axis=0)
        elif strategy == 'median':
            fill_value = np.nanmedian(processed, axis=0)
        elif strategy == 'zero':
            fill_value = 0
        else:
            raise ValueError(f"未知的策略: {strategy}")
        
        # 填充缺失值
        if processed.ndim == 1:
            processed = np.where(np.isnan(processed), fill_value, processed)
        else:
            for i in range(processed.shape[1]):
                processed[:, i] = np.where(
                    np.isnan(processed[:, i]),
                    fill_value[i] if isinstance(fill_value, np.ndarray) else fill_value,
                    processed[:, i]
                )
        
        return processed

