import pygame

class Dialog:
    def __init__(self, game_stats, msg):
        self.screen = game_stats.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_stats.settings
        self.text_color = self.settings.text_color
        self.rect_color = self.settings.rect_color

        self.rect = pygame.Rect(0, 0, self.settings.width,
            self.settings.height)
        self.rect.center = self.screen_rect.center
        self.font = self.settings.font

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True,
            self.text_color, self.rect_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.settings.rect_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
