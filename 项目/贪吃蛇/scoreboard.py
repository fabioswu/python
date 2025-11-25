import pygame

class Scoreboard:
    def __init__(self, snake_game):
        self.screen = snake_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = snake_game.settings
        self.stats = snake_game.stats

    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.settings.font.render(score_str, True,
            self.settings.score_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.midtop = self.screen_rect.midtop

    def show_score(self):
        self.prep_score()
        self.screen.blit(self.score_image, self.score_rect)
