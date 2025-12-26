"""
2048 遊戲模組
分層架構設計，職責清晰
"""
from game_2048.board import GameBoard
from game_2048.move import MoveHandler
from game_2048.score import ScoreCalculator

__all__ = ['GameBoard', 'MoveHandler', 'ScoreCalculator']

