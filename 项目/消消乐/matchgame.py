import pygame, sys, time

from settings import Settings
from board import Board
from draw import Draw

class MatchGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.board = Board(self)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('消消乐')

        self.draw = Draw(self)
        self.clock = pygame.time.Clock()

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
            if not self.board.selected:
                self.board.selected = mouse_pos
            else:
                x1, y1 = self.board.selected
                x2, y2 = mouse_pos
                if abs(x1-x2) + abs(y1-y2) == 1:
                    (self.board.board[x1][y1],
                     self.board.board[x2][y2]) = \
                    (self.board.board[x2][y2],
                     self.board.board[x1][y1])
                    self.board.selected = None
                    self._update_screen()
                    
                    start_time = time.time()
                    while time.time() - start_time < self.settings.sleep_time:
                        self.clock.tick(60)
                        self._check_events()

                    if not self.board._check_eliminate():
                        (self.board.board[x1][y1],
                         self.board.board[x2][y2]) = \
                        (self.board.board[x2][y2],
                         self.board.board[x1][y1])
                        self._update_screen()
                else:
                    self.board.selected = mouse_pos
        else:
            self.board.selected = None

    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw.draw_score_board()
        self.draw.draw_board()
        pygame.display.flip()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

if __name__ == '__main__':
    match_game = MatchGame()
    match_game.run_game()
