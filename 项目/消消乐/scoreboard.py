import pygame

class ScoreBoard:
	def __init__(self, game):
		self.score = 0
		self.screen = game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = game.settings

	def prep_score(self):
		score_str = str(self.score)
		self.score_image = self.settings.font.render(score_str, True,
			self.settings.score_color, self.settings.bg_color)

		self.score_rect = self.score_image.get_rect()
		self.score_rect.topleft = self.screen_rect.topleft

	def show_score(self):
		self.prep_score()
		self.screen.blit(self.score_image, self.score_rect)
