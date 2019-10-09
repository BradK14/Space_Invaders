import pygame
from time import sleep

class High_Scores:
    def __init__(self,ai_settings, screen):
        self.ai_settings = ai_settings
        self.screen = screen

        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
    def display(self, new_high_score):
        textobj = self.font.render(str(new_high_score), 1, self.text_color)
        textrect = textobj.get_rect()
        textrect.topleft = 400, 400
        self.screen.blit(textobj, textrect)
        # sleep(5)