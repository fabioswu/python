import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# 初始化Pygame
pygame.init()
screen = pygame.display.set_mode((670, 670))
pygame.display.set_caption('五子棋')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_COLOR = (238, 154, 73)
RED = (255, 0, 0)
GREEN = (0, 128, 0)

# 棋盘参数
BOARD_SIZE = 15
CELL_SIZE = 44
MARGIN = 27

# 棋子状态
EMPTY = 0
BLACK_CHESS = 1
WHITE_CHESS = 2

class GomokuGame:
    def __init__(self):
        """初始化五子棋游戏"""
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK_CHESS
        self.game_over = False
        self.winner = None
        self.font = pygame.font.SysFont('SimHei', 48)
        self.small_font = pygame.font.SysFont('SimHei', 24)

    def draw_board(self):
        """绘制棋盘"""
        screen.fill(BOARD_COLOR)

        # 绘制网格线
        for i in range(BOARD_SIZE):
            # 垂直线
            pygame.draw.line(
                screen, BLACK,
                (MARGIN + i * CELL_SIZE, MARGIN),
                (MARGIN + i * CELL_SIZE, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE),
                2
            )
            # 水平线
            pygame.draw.line(
                screen, BLACK,
                (MARGIN, MARGIN + i * CELL_SIZE),
                (MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE),
                2
            )

        # 绘制天元和星位
        center = MARGIN + 7 * CELL_SIZE
        pygame.draw.circle(screen, BLACK, (center, center), 8)

        # 绘制星位点
        star_points = [3, 7, 11]
        for i in star_points:
            for j in star_points:
                if i == 7 and j == 7:  # 天元已经绘制
                    continue
                x = MARGIN + i * CELL_SIZE
                y = MARGIN + j * CELL_SIZE
                pygame.draw.circle(screen, BLACK, (x, y), 4)

        # 绘制棋子
        self.draw_chess_pieces()

        # 绘制游戏结束提示
        if self.game_over and self.winner:
            self.draw_winner_prompt()

    def draw_chess_pieces(self):
        """绘制所有棋子"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != EMPTY:
                    x = MARGIN + col * CELL_SIZE
                    y = MARGIN + row * CELL_SIZE
                    color = BLACK if self.board[row][col] == BLACK_CHESS else WHITE
                    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 2 - 2)

    def draw_winner_prompt(self):
        """绘制胜方提示"""
        winner_text = "黑棋获胜!" if self.winner == BLACK_CHESS else "白棋获胜!"
        text_color = BLACK if self.winner == BLACK_CHESS else WHITE

        # 创建半透明覆盖层
        overlay = pygame.Surface((670, 670), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 半透明黑色
        screen.blit(overlay, (0, 0))

        # 绘制获胜文本
        winner_surface = self.font.render(winner_text, True, text_color)
        text_rect = winner_surface.get_rect(center=(335, 300))
        screen.blit(winner_surface, text_rect)

        # 绘制重新开始提示
        restart_surface = self.small_font.render("按空格键重新开始", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(335, 360))
        screen.blit(restart_surface, restart_rect)

    def get_board_position(self, mouse_x, mouse_y):
        """
        将鼠标坐标转换为棋盘坐标

        Args:
            mouse_x (int): 鼠标x坐标
            mouse_y (int): 鼠标y坐标

        Returns:
            tuple: 棋盘坐标(row, col)，如果不在棋盘范围内则返回(None, None)
        """
        # 计算最近的网格交点
        col = round((mouse_x - MARGIN) / CELL_SIZE)
        row = round((mouse_y - MARGIN) / CELL_SIZE)

        # 检查是否在有效范围内
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None, None

    def place_chess(self, row, col):
        """
        在指定位置放置棋子

        Args:
            row (int): 行坐标
            col (int): 列坐标

        Returns:
            bool: 是否成功放置棋子
        """
        if self.game_over or self.board[row][col] != EMPTY:
            return False

        self.board[row][col] = self.current_player
        if self.check_winner(row, col):
            self.game_over = True
            self.winner = self.current_player
        else:
            # 切换玩家
            self.current_player = WHITE_CHESS if self.current_player == BLACK_CHESS else BLACK_CHESS
        return True

    def check_winner(self, row, col):
        """
        检查是否有玩家获胜

        Args:
            row (int): 最后一步的行坐标
            col (int): 最后一步的列坐标

        Returns:
            bool: 是否有玩家获胜
        """
        player = self.board[row][col]
        directions = [
            (0, 1),   # 水平
            (1, 0),   # 垂直
            (1, 1),   # 主对角线
            (1, -1)   # 副对角线
        ]

        for dx, dy in directions:
            count = 1  # 包含当前棋子

            # 向一个方向检查
            r, c = row + dx, col + dy
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dx
                c += dy

            # 向相反方向检查
            r, c = row - dx, col - dy
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dx
                c -= dy

            # 如果连成五子则获胜
            if count >= 5:
                return True
        return False

    def reset_game(self):
        """重置游戏"""
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK_CHESS
        self.game_over = False
        self.winner = None

def main():
    """主函数"""
    game = GomokuGame()
    game.draw_board()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not game.game_over:
                x, y = event.pos
                row, col = game.get_board_position(x, y)
                if row is not None and col is not None:
                    if game.place_chess(row, col):
                        game.draw_board()
                        pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                # 按空格键重新开始游戏
                if event.key == pygame.K_SPACE:
                    game.reset_game()
                    game.draw_board()
                    pygame.display.update()

        # 显示当前玩家提示（仅在游戏未结束时）
        if not game.game_over:
            player_name = "黑棋" if game.current_player == BLACK_CHESS else "白棋"
            pygame.display.set_caption(f'五子棋 - 当前玩家: {player_name}')
        else:
            pygame.display.set_caption('五子棋 - 游戏结束')

        pygame.display.update()

if __name__ == '__main__':
    main()

