import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from high_scores import High_Scores
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    # Make the Buttons.
    play_button = Button(ai_settings, screen, "Play")
    high_score_button = Button(ai_settings, screen, "High Scores")

    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    high_scores = High_Scores(ai_settings, screen)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alien_lasers = Group()
    aliens = Group()
    UFOs = Group()
    barriers = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, UFOs, bullets, barriers)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, high_score_button, ship, aliens, UFOs, bullets, alien_lasers, barriers)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, high_scores, ship, aliens, UFOs, bullets, alien_lasers, barriers)
            gf.update_aliens(ai_settings, screen, stats, sb, high_scores, ship, aliens, UFOs, bullets, alien_lasers, barriers)
            gf.update_UFOs(ai_settings, screen, UFOs)
            gf.update_music(ai_settings)
            gf.update_animations(ai_settings, screen)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, UFOs, bullets, alien_lasers, play_button,high_score_button, barriers)

run_game()