"""
2048 移動處理模組
負責處理遊戲的移動邏輯（上下左右）
"""
import numpy as np
from typing import Tuple
from game_2048.board import GameBoard


class MoveHandler:
    """移動處理器"""
    
    @staticmethod
    def move_left(board: GameBoard) -> Tuple[GameBoard, int, bool]:
        """
        向左移動
        
        Args:
            board: 遊戲板
        
        Returns:
            (新遊戲板, 得分增量, 是否移動成功)
        """
        return MoveHandler._move(board, 'left')
    
    @staticmethod
    def move_right(board: GameBoard) -> Tuple[GameBoard, int, bool]:
        """
        向右移動
        
        Args:
            board: 遊戲板
        
        Returns:
            (新遊戲板, 得分增量, 是否移動成功)
        """
        return MoveHandler._move(board, 'right')
    
    @staticmethod
    def move_up(board: GameBoard) -> Tuple[GameBoard, int, bool]:
        """
        向上移動
        
        Args:
            board: 遊戲板
        
        Returns:
            (新遊戲板, 得分增量, 是否移動成功)
        """
        return MoveHandler._move(board, 'up')
    
    @staticmethod
    def move_down(board: GameBoard) -> Tuple[GameBoard, int, bool]:
        """
        向下移動
        
        Args:
            board: 遊戲板
        
        Returns:
            (新遊戲板, 得分增量, 是否移動成功)
        """
        return MoveHandler._move(board, 'down')
    
    @staticmethod
    def _move(board: GameBoard, direction: str) -> Tuple[GameBoard, int, bool]:
        """
        執行移動操作
        
        Args:
            board: 遊戲板
            direction: 移動方向 ('left', 'right', 'up', 'down')
        
        Returns:
            (新遊戲板, 得分增量, 是否移動成功)
        """
        new_board = board.copy()
        new_board.board = board.board.copy()
        
        # 根據方向旋轉遊戲板，統一處理為向左移動
        if direction == 'right':
            new_board.board = np.fliplr(new_board.board)
        elif direction == 'up':
            new_board.board = np.rot90(new_board.board, k=-1)
        elif direction == 'down':
            new_board.board = np.rot90(new_board.board, k=1)
        
        # 執行向左移動
        score_delta = 0
        moved = False
        
        for i in range(new_board.size):
            row = new_board.board[i, :].copy()
            new_row, row_score, row_moved = MoveHandler._merge_row(row)
            
            new_board.board[i, :] = new_row
            score_delta += row_score
            if row_moved:
                moved = True
        
        # 還原旋轉
        if direction == 'right':
            new_board.board = np.fliplr(new_board.board)
        elif direction == 'up':
            new_board.board = np.rot90(new_board.board, k=1)
        elif direction == 'down':
            new_board.board = np.rot90(new_board.board, k=-1)
        
        # 更新得分
        new_board.score = board.score + score_delta
        
        return new_board, score_delta, moved
    
    @staticmethod
    def _merge_row(row: np.ndarray) -> Tuple[np.ndarray, int, bool]:
        """
        合併一行（向左）
        
        Args:
            row: 一行數據
        
        Returns:
            (新行, 得分增量, 是否移動)
        """
        # 移除零
        non_zeros = row[row != 0]
        
        # 合併相同數字
        merged = []
        score = 0
        i = 0
        moved = len(non_zeros) < len(row) or not np.array_equal(row[:len(non_zeros)], non_zeros)
        
        while i < len(non_zeros):
            if i < len(non_zeros) - 1 and non_zeros[i] == non_zeros[i + 1]:
                # 合併
                merged_value = non_zeros[i] * 2
                merged.append(merged_value)
                score += merged_value
                i += 2
                moved = True
            else:
                merged.append(non_zeros[i])
                i += 1
        
        # 填充到原始長度
        new_row = np.zeros_like(row)
        new_row[:len(merged)] = merged
        
        return new_row, score, moved

