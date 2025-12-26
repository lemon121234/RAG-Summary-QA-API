"""
2048 遊戲板模組
負責遊戲板的初始化和狀態管理
"""
import numpy as np
from typing import Tuple, List
import random


class GameBoard:
    """2048 遊戲板"""
    
    def __init__(self, size: int = 4, seed: int = None):
        """
        初始化遊戲板
        
        Args:
            size: 遊戲板大小（預設 4x4）
            seed: 隨機種子（用於可重現性）
        """
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.score = 0
        
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # 初始化時在兩個隨機位置放置 2
        self._add_random_tile()
        self._add_random_tile()
    
    def _add_random_tile(self) -> bool:
        """
        在隨機空位添加新方塊（2 或 4）
        
        Returns:
            是否成功添加
        """
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False
        
        # 90% 機率是 2，10% 機率是 4
        value = 2 if random.random() < 0.9 else 4
        row, col = random.choice(empty_cells)
        self.board[row, col] = value
        return True
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        獲取所有空格位置
        
        Returns:
            空格位置列表 [(row, col), ...]
        """
        return [(i, j) for i in range(self.size) 
                for j in range(self.size) 
                if self.board[i, j] == 0]
    
    def is_full(self) -> bool:
        """
        檢查遊戲板是否已滿
        
        Returns:
            是否已滿
        """
        return len(self.get_empty_cells()) == 0
    
    def can_move(self) -> bool:
        """
        檢查是否還能移動
        
        Returns:
            是否還能移動
        """
        if not self.is_full():
            return True
        
        # 檢查是否有相鄰的相同數字
        for i in range(self.size):
            for j in range(self.size):
                current = self.board[i, j]
                # 檢查右邊
                if j < self.size - 1 and self.board[i, j + 1] == current:
                    return True
                # 檢查下邊
                if i < self.size - 1 and self.board[i + 1, j] == current:
                    return True
        
        return False
    
    def get_max_tile(self) -> int:
        """
        獲取最大方塊值
        
        Returns:
            最大方塊值
        """
        return int(np.max(self.board))
    
    def copy(self) -> 'GameBoard':
        """
        複製遊戲板
        
        Returns:
            新的遊戲板實例
        """
        new_board = GameBoard(self.size)
        new_board.board = self.board.copy()
        new_board.score = self.score
        return new_board
    
    def __str__(self) -> str:
        """字符串表示"""
        return str(self.board)

