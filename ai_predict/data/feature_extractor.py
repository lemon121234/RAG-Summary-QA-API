"""
特徵提取模組
負責從原始數據中提取特徵
"""
import numpy as np
from typing import List, Optional


class FeatureExtractor:
    """特徵提取器"""
    
    @staticmethod
    def extract_basic_features(data: np.ndarray) -> np.ndarray:
        """
        提取基本統計特徵
        
        Args:
            data: 原始數據
        
        Returns:
            特徵向量
        """
        features = []
        
        if data.ndim == 1:
            # 一維數據
            features.extend([
                np.mean(data),
                np.std(data),
                np.min(data),
                np.max(data),
                np.median(data)
            ])
        else:
            # 多維數據 - 對每列提取特徵
            for col in range(data.shape[1]):
                col_data = data[:, col]
                features.extend([
                    np.mean(col_data),
                    np.std(col_data),
                    np.min(col_data),
                    np.max(col_data),
                    np.median(col_data)
                ])
        
        return np.array(features)
    
    @staticmethod
    def extract_temporal_features(
        data: np.ndarray,
        window_size: int = 3
    ) -> np.ndarray:
        """
        提取時間序列特徵（移動平均、變化率等）
        
        Args:
            data: 時間序列數據
            window_size: 窗口大小
        
        Returns:
            特徵向量
        """
        if data.ndim > 1:
            data = data.flatten()
        
        features = []
        
        # 移動平均
        if len(data) >= window_size:
            moving_avg = np.convolve(
                data,
                np.ones(window_size) / window_size,
                mode='valid'
            )
            features.extend([
                np.mean(moving_avg),
                np.std(moving_avg)
            ])
        
        # 變化率
        if len(data) > 1:
            diff = np.diff(data)
            features.extend([
                np.mean(diff),
                np.std(diff),
                np.sum(diff > 0) / len(diff)  # 上升比例
            ])
        
        return np.array(features) if features else np.array([0.0])
    
    @staticmethod
    def extract_interaction_features(
        data: np.ndarray,
        max_interactions: int = 5
    ) -> np.ndarray:
        """
        提取交互特徵（特徵之間的乘積、比值等）
        
        Args:
            data: 原始數據
            max_interactions: 最大交互特徵數量
        
        Returns:
            交互特徵向量
        """
        if data.ndim == 1:
            return np.array([])
        
        features = []
        n_features = min(data.shape[1], max_interactions)
        
        # 特徵乘積
        for i in range(n_features):
            for j in range(i + 1, min(n_features, data.shape[1])):
                interaction = data[:, i] * data[:, j]
                features.append(np.mean(interaction))
        
        return np.array(features) if features else np.array([0.0])
    
    @staticmethod
    def combine_features(
        basic: np.ndarray,
        temporal: Optional[np.ndarray] = None,
        interaction: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        組合多種特徵
        
        Args:
            basic: 基本特徵
            temporal: 時間序列特徵（可選）
            interaction: 交互特徵（可選）
        
        Returns:
            組合後的特徵向量
        """
        features = [basic]
        
        if temporal is not None:
            features.append(temporal)
        
        if interaction is not None:
            features.append(interaction)
        
        return np.concatenate(features)

