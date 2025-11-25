import pygame
from dialog import Dialog

class GameStats:
    def __init__(self, snake_game, fail_msg, start_msg, pause_msg):
        self.screen = snake_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = snake_game.settings

        self.game_active = False

        self.fail = Dialog(self, fail_msg)
        self.start = Dialog(self, start_msg)
        self.pause = Dialog(self, pause_msg)

        self.score = 0
