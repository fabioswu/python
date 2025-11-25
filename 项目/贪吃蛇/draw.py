import pygame

class Draw:
    def __init__(self, snake_game):
        self.screen = snake_game.screen
        self.settings = snake_game.settings
        self.board = snake_game.board
        self.head_color = self.settings.head_color
        self.body_color = self.settings.body_color
        self.food_color = self.settings.food_color
        self.head_pos = self.board.head_pos

        self.rect = pygame.Rect(0, 0, self.settings.square_side,
                                     self.settings.square_side)

    def get_bodies(self):
        self.bodies = []
        for i in range(self.settings.board_height):
            for j in range(self.settings.board_width):
                if self.board.board[i][j] in [1, 2, 3, 4, -1] and \
                   [i, j] != self.board.head_pos:
                    self.bodies.append([j, i])

    def draw_things(self):
        self.get_bodies()
        for i in self.bodies:
            self.rect.topleft = tuple(map(
                lambda x: x*self.settings.square_side, i))
            pygame.draw.rect(self.screen, self.body_color, self.rect)


        self.rect.topleft = tuple(map(lambda x: x*self.settings.square_side,
                                      reversed(self.board.food_pos)))
        pygame.draw.rect(self.screen, self.food_color, self.rect)

        self.rect.topleft = tuple(map(lambda x: x*self.settings.square_side,
                                      reversed(self.board.head_pos)))
        pygame.draw.rect(self.screen, self.head_color, self.rect)
