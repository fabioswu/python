import pygame

class Draw:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.board = game.board

    def draw_score_board(self):
        rect = pygame.Rect(0, 0, self.settings.screen_width, 39)
        pygame.draw.rect(self.screen, self.settings.bg_color, rect)

    def draw_board(self):
        if self.board.selected:
            rect = pygame.Rect(0, 0, self.settings.square_side+2,
                self.settings.square_side+2)
            y, x = self.board.selected
            rect.x = x*(self.settings.square_side+1)
            rect.y = y*(self.settings.square_side+1) + 39
            pygame.draw.rect(self.screen, (255, 255, 255), rect)
        rect = pygame.Rect(0, 0, self.settings.square_side,
            self.settings.square_side)
        for x in range(self.settings.board_height):
            for y in range(self.settings.board_width):
                item = self.board.board[x][y]
                rect.x = y*(self.settings.square_side+1)+1
                rect.y = x*(self.settings.square_side+1)+40
                if item == 1:
                    color = self.settings.color_1
                elif item == 2:
                    color = self.settings.color_2
                elif item == 3:
                    color = self.settings.color_3
                elif item == 4:
                    color = self.settings.color_4
                elif item == 5:
                    color = self.settings.color_5
                elif item == 0:
                    color = self.settings.color_empty
                pygame.draw.rect(self.screen, color, rect)
