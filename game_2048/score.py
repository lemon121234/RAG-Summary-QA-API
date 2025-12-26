"""
2048 得分計算模組
負責得分計算和統計
"""
from game_2048.board import GameBoard
from typing import Dict


class ScoreCalculator:
    """得分計算器"""
    
    @staticmethod
    def calculate_score(board: GameBoard) -> int:
        """
        計算當前得分
        
        Args:
            board: 遊戲板
        
        Returns:
            當前得分
        """
        return board.score
    
    @staticmethod
    def get_statistics(board: GameBoard) -> Dict:
        """
        獲取遊戲統計信息
        
        Args:
            board: 遊戲板
        
        Returns:
            統計信息字典
        """
        return {
            "score": board.score,
            "max_tile": board.get_max_tile(),
            "empty_cells": len(board.get_empty_cells()),
            "total_cells": board.size * board.size,
            "fill_rate": 1 - (len(board.get_empty_cells()) / (board.size * board.size))
        }
    
    @staticmethod
    def estimate_potential_score(board: GameBoard) -> int:
        """
        估算潛在得分（用於AI策略）
        
        Args:
            board: 遊戲板
        
        Returns:
            估算的潛在得分
        """
        # 簡單啟發式：最大方塊值 * 空格數量
        max_tile = board.get_max_tile()
        empty_count = len(board.get_empty_cells())
        return max_tile * empty_count * 10

