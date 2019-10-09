import pygame, random
from pygame.sprite import Sprite

class Alien_Laser(Sprite):
    """A class to manage lasers shot from the aliens"""
    def __init__(self, ai_settings, screen, aliens):
        """Create a laser at a random aliens position"""
        super(Alien_Laser, self).__init__()
        self.screen = screen

        # Create laser rect at (0, 0), then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)

        # Set laser position at a random alien
        choice = random.randint(1, len(aliens))
        iteration = 1
        for alien in aliens:
            if choice == iteration:
                self.rect.centerx = alien.rect.centerx
                self.rect.bottom = alien.rect.bottom
            iteration += 1

        # Store a decimal value for the bullet's position.
        self.y = float(self.rect.y)
        self.color = ai_settings.alien_laser_color
        self.speed_factor = ai_settings.alien_laser_speed_factor

    def update(self):
        """Move the bullet down the screen."""
        # Update the decimal position of the bullet.
        self.y += self.speed_factor

        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)