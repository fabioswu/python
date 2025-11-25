import pygame, sys, time

from settings import Settings
from board import Board
from draw import Draw
from game_stats import GameStats
from scoreboard import Scoreboard

class Snake:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Snake')

        self.stats = GameStats(self, 'Game over', 'Play', 'Paused')
        self.sb = Scoreboard(self)
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

                if self.stats.game_active:

                    if event.key in [pygame.K_RIGHT, pygame.K_d]:
                        if self.board.direction not in [2, 4]:
                            self.board.direction = 2
                            break

                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        if self.board.direction not in [2, 4]:
                            self.board.direction = 4
                            break

                    if event.key in [pygame.K_UP, pygame.K_w]:
                        if self.board.direction not in [1, 3]:
                            self.board.direction = 1
                            break

                    if event.key in [pygame.K_DOWN, pygame.K_s]:
                        if self.board.direction not in [1, 3]:
                            self.board.direction = 3
                            break

                if event.key in [pygame.K_SPACE, pygame.K_RETURN] and \
                   self.started:
                    self.stats.game_active = not self.stats.game_active

            elif event.type == pygame.MOUSEBUTTONDOWN and \
                 not self.stats.game_active:
                mouse_pos = pygame.mouse.get_pos()
                self._check_start_button(mouse_pos)

    def _check_start_button(self, mouse_pos):
        if self.stats.start.rect.collidepoint(mouse_pos) and not self.started:
            self.stats.game_active = True
            self.board.give_food()

    def _check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.draw.draw_things()
        self.sb.show_score()

        if not self.stats.game_active:
            pygame.mouse.set_visible(True)
            if not self.started:
                self.stats.start.draw()
            else:
                self.stats.pause.draw()
        else:
            pygame.mouse.set_visible(False)

        pygame.display.flip()

    def game_over(self):
        self.stats.fail.draw()
        pygame.mouse.set_visible(True)
        pygame.display.flip()
        while True:
            self._check_quit()

    def run_game(self):
        self.started = False
        while True:
            self._check_events()
            self._update_screen()
            if self.stats.game_active:
                self.started = True
                if self.board.update_snake():
                    pygame.display.flip()
                    self.game_over()

                time.sleep(self.settings.time)


if __name__ == '__main__':
    snake = Snake()
    snake.run_game()
