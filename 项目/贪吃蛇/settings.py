import pygame

class Settings:
    def __init__(self):
        self.board_width = 16
        self.board_height = 16
        self.square_side = 30
        self.screen_width = self.board_width*self.square_side
        self.screen_height = self.board_height*self.square_side

        self.bg_color = (50, 0, 0)
        self.head_color = (200, 0, 0)
        self.body_color = (150, 0, 0)

        self.time = 0.2

        self.width = 250
        self.height = 50
        self.rect_color = (0, 255, 0)
        self.text_color = (255, 255, 255)

        self.score_color = (255, 255, 255)

        self.food_color = (0, 255, 255)

        self.font = pygame.font.SysFont(None, 45)
