import numpy as np
import random
import time
from collections import defaultdict

class GomokuBoard:
    """五子棋棋盘类"""
    def __init__(self, size=15):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)  # 0: 空, 1: 玩家(黑棋), 2: AI(白棋)
        self.current_player = 1  # 玩家先手
        self.last_move = None
        self.winner = None
        self.game_over = False
        
    def reset(self):
        """重置棋盘"""
        self.board.fill(0)
        self.current_player = 1
        self.last_move = None
        self.winner = None
        self.game_over = False
        
    def make_move(self, row, col):
        """在指定位置落子"""
        if self.game_over or self.board[row, col] != 0:
            return False
            
        self.board[row, col] = self.current_player
        self.last_move = (row, col)
        
        # 检查游戏是否结束
        if self.check_winner(row, col):
            self.winner = self.current_player
            self.game_over = True
        elif self.is_board_full():
            self.game_over = True
            self.winner = 0  # 平局
        else:
            self.current_player = 3 - self.current_player  # 切换玩家 (1->2, 2->1)
            
        return True
    
    def check_winner(self, row, col):
        """检查是否有玩家获胜"""
        player = self.board[row, col]
        if player == 0:
            return False
            
        # 检查四个方向: 水平、垂直、主对角线、副对角线
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1  # 当前位置
            
            # 正向检查
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r, c] == player:
                count += 1
                r += dr
                c += dc
                
            # 反向检查
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r, c] == player:
                count += 1
                r -= dr
                c -= dc
                
            if count >= 5:
                return True
                
        return False
    
    def is_board_full(self):
        """检查棋盘是否已满"""
        return np.all(self.board != 0)
    
    def get_valid_moves(self):
        """获取所有合法移动位置"""
        moves = []
        # 只考虑棋盘上有棋子周围的空位（加速搜索）
        if self.last_move:
            r, c = self.last_move
            # 检查周围3x3区域
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr, nc] == 0:
                        moves.append((nr, nc))
            # 如果没有找到，搜索整个棋盘
            if not moves:
                moves = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r, c] == 0]
        else:
            # 如果还没有落子，返回所有位置
            moves = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r, c] == 0]
            
        return moves
    
    def display(self):
        """显示棋盘"""
        print("   " + " ".join([f"{i:2}" for i in range(self.size)]))
        for r in range(self.size):
            row_str = f"{r:2} "
            for c in range(self.size):
                cell = self.board[r, c]
                if cell == 0:
                    row_str += " . "
                elif cell == 1:
                    row_str += " ● "  # 黑棋
                else:
                    row_str += " ○ "  # 白棋
            print(row_str)


class GomokuAI:
    """五子棋AI类"""
    def __init__(self, board, player=2, depth=3):
        self.board = board
        self.player = player  # AI的玩家编号
        self.depth = depth    # 搜索深度
        # 模式评分表
        self.pattern_scores = {
            "FIVE": 1000000,      # 五连
            "LIVE_FOUR": 10000,   # 活四
            "DEAD_FOUR": 1000,    # 死四
            "LIVE_THREE": 1000,   # 活三
            "DEAD_THREE": 100,    # 死三
            "LIVE_TWO": 100,      # 活二
            "DEAD_TWO": 10,       # 死二
            "LIVE_ONE": 10,       # 活一
            "DEAD_ONE": 1         # 死一
        }
        
    def evaluate_board(self):
        """评估当前棋盘局势"""
        if self.board.game_over:
            if self.board.winner == self.player:
                return 1000000
            elif self.board.winner == 3 - self.player:
                return -1000000
            else:
                return 0
                
        score = 0
        size = self.board.size
        
        # 检查所有可能的方向
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(size):
            for c in range(size):
                if self.board.board[r, c] == self.player:
                    score += self.evaluate_position(r, c, self.player)
                elif self.board.board[r, c] == 3 - self.player:
                    score -= self.evaluate_position(r, c, 3 - self.player) * 1.2  # 对手的威胁权重更高
                    
        return score
    
    def evaluate_position(self, row, col, player):
        """评估特定位置的局势"""
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            # 检查这个方向
            line = []
            for i in range(-4, 5):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < self.board.size and 0 <= c < self.board.size:
                    line.append(self.board.board[r, c])
                else:
                    line.append(-1)  # 边界
            
            # 分析棋型
            score += self.analyze_line(line, player)
            
        return score
    
    def analyze_line(self, line, player):
        """分析一条线上的棋型"""
        score = 0
        length = len(line)
        
        for i in range(length - 4):
            segment = line[i:i+5]
            score += self.analyze_segment(segment, player)
            
        return score
    
    def analyze_segment(self, segment, player):
        """分析5个连续位置的棋型"""
        # 统计玩家棋子和空位
        player_count = segment.count(player)
        empty_count = segment.count(0)
        opponent_count = 5 - player_count - empty_count
        
        if opponent_count > 0:
            return 0  # 有对手棋子，不是有效棋型
        
        # 根据玩家棋子和空位数量评分
        if player_count == 5:
            return self.pattern_scores["FIVE"]
        elif player_count == 4 and empty_count == 1:
            return self.pattern_scores["LIVE_FOUR"]
        elif player_count == 4:
            return self.pattern_scores["DEAD_FOUR"]
        elif player_count == 3 and empty_count == 2:
            return self.pattern_scores["LIVE_THREE"]
        elif player_count == 3:
            return self.pattern_scores["DEAD_THREE"]
        elif player_count == 2 and empty_count == 3:
            return self.pattern_scores["LIVE_TWO"]
        elif player_count == 2:
            return self.pattern_scores["DEAD_TWO"]
        elif player_count == 1 and empty_count == 4:
            return self.pattern_scores["LIVE_ONE"]
        elif player_count == 1:
            return self.pattern_scores["DEAD_ONE"]
            
        return 0
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        """极小化极大算法，带Alpha-Beta剪枝"""
        if depth == 0 or self.board.game_over:
            return self.evaluate_board(), None
            
        valid_moves = self.board.get_valid_moves()
        
        if not valid_moves:
            return self.evaluate_board(), None
            
        # 对移动进行排序以提高剪枝效率
        valid_moves = self.order_moves(valid_moves, maximizing_player)
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            
            for move in valid_moves:
                row, col = move
                # 模拟落子
                self.board.board[row, col] = self.player
                eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
                # 撤销落子
                self.board.board[row, col] = 0
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta剪枝
                    
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            
            for move in valid_moves:
                row, col = move
                # 模拟落子
                self.board.board[row, col] = 3 - self.player
                eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
                # 撤销落子
                self.board.board[row, col] = 0
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta剪枝
                    
            return min_eval, best_move
    
    def order_moves(self, moves, maximizing_player):
        """对可能的移动进行排序，提高剪枝效率"""
        scored_moves = []
        
        for move in moves:
            row, col = move
            # 中心优先
            center = self.board.size // 2
            distance_from_center = abs(row - center) + abs(col - center)
            score = -distance_from_center  # 距离中心越近，分数越高
            
            # 如果位置在已有棋子旁边，增加分数
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                        if self.board.board[nr, nc] != 0:
                            score += 10
            
            scored_moves.append((score, move))
        
        # 按分数降序排序
        scored_moves.sort(key=lambda x: x[0], reverse=True)
        
        return [move for _, move in scored_moves]
    
    def get_best_move(self):
        """获取最佳移动"""
        if self.board.game_over:
            return None
            
        # 如果棋盘为空，下在中心
        if np.all(self.board.board == 0):
            center = self.board.size // 2
            return (center, center)
        
        # 使用极小化极大算法计算最佳移动
        start_time = time.time()
        _, best_move = self.minimax(self.depth, float('-inf'), float('inf'), True)
        end_time = time.time()
        
        print(f"AI思考时间: {end_time - start_time:.2f}秒")
        
        # 如果没有找到最佳移动，随机选择一个合法移动
        if best_move is None:
            valid_moves = self.board.get_valid_moves()
            if valid_moves:
                best_move = random.choice(valid_moves)
                
        return best_move


class GomokuGame:
    """五子棋游戏主类"""
    def __init__(self, size=15, ai_depth=3):
        self.board = GomokuBoard(size)
        self.ai = GomokuAI(self.board, player=2, depth=ai_depth)
        self.human_player = 1
        self.ai_player = 2
        
    def play(self):
        """开始游戏"""
        print("=" * 50)
        print("欢迎来到五子棋游戏!")
        print("黑棋(●)先手，白棋(○)后手")
        print("输入坐标格式: 行 列 (例如: 7 7 表示第7行第7列)")
        print("输入 'q' 退出游戏")
        print("=" * 50)
        
        self.board.display()
        
        while not self.board.game_over:
            if self.board.current_player == self.human_player:
                self.human_move()
            else:
                self.ai_move()
                
        self.show_game_result()
        
    def human_move(self):
        """处理人类玩家移动"""
        while True:
            try:
                move_input = input(f"玩家{self.board.current_player}({'●' if self.board.current_player == 1 else '○'})的回合，请输入落子位置: ")
                
                if move_input.lower() == 'q':
                    print("游戏结束!")
                    self.board.game_over = True
                    return
                    
                parts = move_input.split()
                if len(parts) != 2:
                    print("请输入两个数字，用空格分隔!")
                    continue
                    
                row, col = int(parts[0]), int(parts[1])
                
                if row < 0 or row >= self.board.size or col < 0 or col >= self.board.size:
                    print(f"位置超出范围! 请输入0到{self.board.size-1}之间的数字!")
                    continue
                    
                if self.board.make_move(row, col):
                    self.board.display()
                    break
                else:
                    print("该位置已有棋子，请重新选择!")
                    
            except ValueError:
                print("请输入有效的数字!")
            except KeyboardInterrupt:
                print("\n游戏结束!")
                self.board.game_over = True
                return
                
    def ai_move(self):
        """处理AI移动"""
        print(f"AI(○)正在思考...")
        row, col = self.ai.get_best_move()
        
        if row is not None and col is not None:
            self.board.make_move(row, col)
            print(f"AI在位置 ({row}, {col}) 落子")
            self.board.display()
        else:
            print("AI无法找到合法移动!")
            
    def show_game_result(self):
        """显示游戏结果"""
        print("=" * 50)
        if self.board.winner == self.human_player:
            print("恭喜! 你赢了!")
        elif self.board.winner == self.ai_player:
            print("AI赢了!")
        else:
            print("平局!")
        print("=" * 50)


def main():
    """主函数"""
    # 设置棋盘大小和AI搜索深度
    board_size = 15
    ai_depth = 3  # 搜索深度，增加会提高AI强度但会减慢速度
    
    while True:
        game = GomokuGame(board_size, ai_depth)
        game.play()
        
        play_again = input("是否再玩一局? (y/n): ")
        if play_again.lower() != 'y':
            print("感谢游戏，再见!")
            break


if __name__ == "__main__":
    main()
