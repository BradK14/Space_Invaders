import pygame
from pygame.sprite import Sprite

class UFO(Sprite):
    """A class to represent a UFO that moves across the top of the screen at random intervals"""
    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super(UFO, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Create UFO just off screen
        self.rect = pygame.Rect((self.ai_settings.UFO_width * -1),0 , self.ai_settings.UFO_width, self.ai_settings.UFO_height)
        self.pic = pygame.image.load('images/UFO.png')
        self.image = pygame.transform.scale(self.pic, (self.ai_settings.UFO_width, self.ai_settings.UFO_height))

    def update_pos(self):
        self.rect.x += self.ai_settings.UFO_speed

    def blit_me(self):
        self.screen.blit(self.image, self.rect)