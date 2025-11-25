import pygame

class Settings:
    def __init__(self):
        self.board_width = 8
        self.board_height = 8
        self.square_side = 30
        self.screen_width = self.board_width*(self.square_side+1)+1
        self.screen_height = self.board_height*(self.square_side+1)+40

        self.bg_color = (130, 130, 130)
        self.color_1 = (196, 30, 30)
        self.color_2 = (30, 196, 30)
        self.color_3 = (30, 30, 196)
        self.color_4 = (196, 196, 30)
        self.color_5 = (30, 196, 196)
        self.color_empty = (200, 200, 200)

        self.sleep_time = 0.3
