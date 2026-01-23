import pygame, sys

from settings import Settings
from board import Board
from draw import Draw
from scoreboard import ScoreBoard

class MatchGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('消消乐')

        self.sb = ScoreBoard(self)
        self.board = Board(self)
        self.draw = Draw(self)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = list(pygame.mouse.get_pos())
                self._check_selected(mouse_pos)

    def _check_selected(self, mouse_pos):
        mouse_pos[0] -= 1
        mouse_pos[1] -= 40
        mouse_pos.reverse()
        mouse_pos = list(map(lambda x: x //
            (self.settings.square_side+1), mouse_pos))
        if mouse_pos[1] < 0:
            mouse_pos[1] = 0
        if self.board.selected != mouse_pos and mouse_pos[0] >= 0:
            x1, y1 = mouse_pos
            if self.board.board[x1][y1] == 0:
                self.board.selected = None
                return
            if not self.board.selected:
                self.board.selected = mouse_pos
            else:
                x2, y2 = self.board.selected
                if (abs(x1-x2) + abs(y1-y2) == 1):
                    (self.board.board[x1][y1],
                     self.board.board[x2][y2]) = \
                    (self.board.board[x2][y2],
                     self.board.board[x1][y1])
                    self.board.selected = None
                    if not self.board.update():
                        (self.board.board[x1][y1],
                         self.board.board[x2][y2]) = \
                        (self.board.board[x2][y2],
                         self.board.board[x1][y1])
                else:
                    self.board.selected = mouse_pos
        else:
            self.board.selected = None
        #print(self.board.selected)

    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw.draw_score_board()
        self.draw.draw_board()
        self.sb.show_score()

        pygame.display.flip()

    def run_game(self):
        self.board.update()
        while True:
            self._check_events()
            self._update_screen()

if __name__ == '__main__':
    match_game = MatchGame()
    match_game.run_game()
