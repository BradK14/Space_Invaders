import pygame
from pygame.sprite import Sprite

class Aliens(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, ai_settings, screen, alien_number, type):
        """Initialize the alien, and set its starting position."""
        super(Aliens, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.type = type

        # Load the alien image, and set its rect attribute.
        self.rect = pygame.Rect(35, 35, 35, 35)

        if type is 1:
            self.default_pic = pygame.image.load('images/Alien1a1.png')
            self.secondary_pic = pygame.image.load('images/Alien1a2.png')
            if alien_number % 2 is 0:
                self.pic = self.default_pic
            else:
                self.pic = self.secondary_pic
        elif type is 2:
            self.default_pic = pygame.image.load('images/Alien2a1.png')
            self.secondary_pic = pygame.image.load('images/Alien2a2.png')
            if alien_number % 2 is 0:
                self.pic = self.default_pic
            else:
                self.pic = self.secondary_pic
        elif type is 3:
            self.default_pic = pygame.image.load('images/Alien3a1.png')
            self.secondary_pic = pygame.image.load('images/Alien3a2.png')
            if alien_number % 2 is 0:
                self.pic = self.default_pic
            else:
                self.pic = self.secondary_pic
        self.image = pygame.transform.scale(self.pic, (35, 35))
        self.default_image = pygame.transform.scale(self.default_pic, (35, 35))
        self.secondary_image = pygame.transform.scale(self.secondary_pic, (35, 35))
        if alien_number % 2 is 0:
            self.step = 1
        else:
            self.step = 2

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += self.Move_Alien()
        self.rect.x = self.x

    def Move_Alien(self):
        if self.step == 1:
            self.image = self.secondary_image
            self.step = 2
        else:
            self.image = self.default_image
            self.step = 1
        return (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)