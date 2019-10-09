'''
import pygame
# from pillow import Image, ImageFilter

class Barrier:
    def __init__(self, ai_settings, screen, type):
        self.ai_settings = ai_settings
        self.type = type
        self.screen = screen
        
        self.rect = pygame.Rect(35, 35, 35, 35)
        if type is '1':
            self.pic = pygame.image.load('images/Barrier1')
        elif type is 'TL':
            self.pic = pygame.image.load('images/BarrierTL1')
        elif type is 'TR':
            self.pic = pygame.image.load('images/BarrierTR1')
        elif type is 'BL':
            self.pic = pygame.image.load('images/BarrierBL1')
        elif type is 'BR':
            self.pic = pygame.image.load('images/BarrierBR1')
'''        

'''
class Barrier:
    def __init__(self, ai_settings, screen):
        super(Barrier, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen


    def (self):

'''