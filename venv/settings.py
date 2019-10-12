import pygame
import random


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 4
        self.bullet_height = 30
        self.bullet_color = 180, 0, 0
        self.bullets_allowed = 5

        # Alien settings.
        self.fleet_drop_speed = 30
        self.alien_width = 35
        self.alien_height = 35

        # UFO settings.
        self.UFO_width = 100
        self.UFO_height = 35
        self.UFO_speed = 1
        self.UFO_old_time = 0
        self.UFO_wait = random.randint(10000, 30000)

        # Barrier settings.
        self.bar_width = 35
        self.bar_height = 35
        
        # Alien laser settings.
        self.alien_laser_width = 4
        self.alien_laser_height = 30
        self.alien_laser_color = 0, 180, 0
        self.alien_lasers_allowed = 1
        
        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        self.alien_speedup_scale = 0.9
        self.music_speedup_scale = 0.99

        # How quickly the alien point values increase.
        self.score_scale = 1.5
        self.UFO_score_scale = 1.5
        self.initialize_dynamic_settings()

        # Alien time management
        self.old_time = 0
        self.wait = 1000

        self.alien_laser_frequency = 5000
        self.alien_laser_old_time = 0

        # Music time management
        self.music_default_speed = 1000
        self.music_speed = self.music_default_speed
        self.music_old_time = 0
        self.music_step = 1

        # Alien death images load
        self.pica1d1 = pygame.image.load('images/alien1d1.png')
        self.pica1d2 = pygame.image.load('images/alien1d2.png')
        self.pica1d3 = pygame.image.load('images/alien1d3.png')
        self.pica2d1 = pygame.image.load('images/alien2d1.png')
        self.pica2d2 = pygame.image.load('images/alien2d2.png')
        self.pica2d3 = pygame.image.load('images/alien2d3.png')
        self.pica3d1 = pygame.image.load('images/alien3d1.png')
        self.pica3d2 = pygame.image.load('images/alien3d2.png')
        self.pica3d3 = pygame.image.load('images/alien3d3.png')
        self.picUFOd1 = pygame.image.load('images/UFOd1.png')
        self.picUFOd2 = pygame.image.load('images/UFOd2.png')
        self.picUFOd3 = pygame.image.load('images/UFOd3.png')
        
        # Alien death animation
        self.dying_alien = []
        self.dying_UFO = []
        self.UFO_points_display = []
        self.death_que = []
        self.alien_death_wait = 40
        self.alien_death_old_time = 0

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 30
        self.alien_laser_speed_factor = 3

        # Scoring.
        self.alien1_points = 40
        self.alien2_points = 20
        self.alien3_points = 10
        self.UFO_points = random.randint(50, 150)

        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.wait *= self.alien_speedup_scale
        self.alien_laser_speed_factor *= self.speedup_scale
        self.alien_laser_frequency *= self.alien_speedup_scale
        self.alien1_points = int(self.alien1_points * self.score_scale)
        self.alien2_points = int(self.alien2_points * self.score_scale)
        self.alien3_points = int(self.alien3_points * self.score_scale)