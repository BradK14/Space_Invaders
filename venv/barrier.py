
import pygame
from pygame.sprite import Sprite
# from pillow import Image, ImageFilter

class Barrier(Sprite):
    def __init__(self, ai_settings, screen, x, y, type):
        super(Barrier, self).__init__()
        self.ai_settings = ai_settings
        self.type = type
        self.screen = screen

        self.health = 2

        self.rect = pygame.Rect(x, y, ai_settings.bar_width, ai_settings.bar_height)
        if type is '1':
            self.pic = pygame.image.load('images/Barrier1.png')
        elif type is 'TL':
            self.pic = pygame.image.load('images/BarrierTL1.png')
        elif type is 'TR':
            self.pic = pygame.image.load('images/BarrierTR1.png')
        elif type is 'BL':
            self.pic = pygame.image.load('images/BarrierBL1.png')
        elif type is 'BR':
            self.pic = pygame.image.load('images/BarrierBR1.png')

        self.image = pygame.transform.scale(self.pic, (ai_settings.bar_width, ai_settings.bar_height))

    def damage_barrier(self, barriers):
        if self.health == 2:
            if self.type is '1':
                self.pic = pygame.image.load('images/Barrier2.png')
            elif self.type is 'TL':
                self.pic = pygame.image.load('images/BarrierTL2.png')
            elif self.type is 'TR':
                self.pic = pygame.image.load('images/BarrierTR2.png')
            elif self.type is 'BL':
                self.pic = pygame.image.load('images/BarrierBL2.png')
            elif self.type is 'BR':
                self.pic = pygame.image.load('images/BarrierBR2.png')
            self.health = 1
            self.image = pygame.transform.scale(self.pic, (self.ai_settings.bar_width, self.ai_settings.bar_height))
        elif self.health == 1:
            barriers.remove(self)

    def blitme(self):
        self.screen.blit(self.image, self.rect)