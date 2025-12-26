"""
2048 遊戲主入口
展示分層架構設計
"""
from game_2048 import GameBoard, MoveHandler, ScoreCalculator


def main():
    """主函數 - 簡單的遊戲循環示例"""
    print("=" * 60)
    print("🎮 2048 遊戲 - 分層架構示例")
    print("=" * 60)
    
    # 初始化遊戲板（使用固定種子確保可重現性）
    board = GameBoard(size=4, seed=42)
    print(f"\n初始遊戲板：\n{board}")
    print(f"初始得分：{ScoreCalculator.calculate_score(board)}")
    
    # 執行幾次移動
    moves = ['left', 'down', 'right', 'up']
    
    for move_name in moves:
        print(f"\n執行移動：{move_name}")
        
        # 根據方向調用對應的移動方法
        if move_name == 'left':
            new_board, score_delta, moved = MoveHandler.move_left(board)
        elif move_name == 'right':
            new_board, score_delta, moved = MoveHandler.move_right(board)
        elif move_name == 'up':
            new_board, score_delta, moved = MoveHandler.move_up(board)
        else:  # down
            new_board, score_delta, moved = MoveHandler.move_down(board)
        
        if moved:
            board = new_board
            # 移動成功後添加新方塊
            board._add_random_tile()
            print(f"移動成功！得分增加：{score_delta}")
            print(f"當前得分：{ScoreCalculator.calculate_score(board)}")
            print(f"遊戲板：\n{board}")
        else:
            print("無法移動（該方向沒有可合併的方塊）")
        
        # 顯示統計信息
        stats = ScoreCalculator.get_statistics(board)
        print(f"統計：最大方塊={stats['max_tile']}, 空格={stats['empty_cells']}")
        
        # 檢查遊戲是否結束
        if not board.can_move():
            print("\n遊戲結束！無法繼續移動")
            break
    
    print(f"\n最終得分：{ScoreCalculator.calculate_score(board)}")
    print(f"最大方塊：{ScoreCalculator.get_statistics(board)['max_tile']}")


if __name__ == "__main__":
    main()

