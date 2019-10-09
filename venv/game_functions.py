import sys
from time import sleep
import pygame
from bullet import Bullet
from alien_laser import Alien_Laser
from aliens import Aliens
# from barrier import Barrier

def check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, alien_laser):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, alien_laser):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, alien_laser)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def display_high_score(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Reset the scoreboard images.
        '''
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        '''
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        pygame.mixer.Sound('sounds/laser.wav').play()
        
def alien_fire_laser(ai_settings, screen, aliens, alien_lasers):
    """Fire a laser, if limit not reached yet."""
    # Create a new laser, add to lasers group.
    curtime = pygame.time.get_ticks()
    if len(alien_lasers) < ai_settings.alien_lasers_allowed:
        if curtime - ai_settings.alien_laser_old_time > ai_settings.alien_laser_frequency:
            new_alien_laser = Alien_Laser(ai_settings, screen, aliens)
            alien_lasers.add(new_alien_laser)
            ai_settings.alien_laser_old_time = curtime

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, alien_lasers, play_button):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Draw death animations
    for death in ai_settings.death_que:
        screen.blit(death[0], death[1])

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_laser in alien_lasers.sprites():
        alien_laser.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets, alien_lasers):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    alien_lasers.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Get rid of lasers that have disappeared.
    for alien_laser in alien_lasers.copy():
        if alien_laser.rect.top >= 700:
            alien_lasers.remove(alien_laser)
    check_laser_ship_collision(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets, alien_lasers)

    # Create new alien laser
    alien_fire_laser(ai_settings, screen, aliens, alien_lasers)

def update_music(ai_settings):
    curtime = pygame.time.get_ticks()
    if curtime - ai_settings.music_old_time > ai_settings.music_speed:
        if ai_settings.music_step == 1:
            pygame.mixer.Sound('sounds/song1.wav').play()
            ai_settings.music_step = 2
        else:
            pygame.mixer.Sound('sounds/song2.wav').play()
            ai_settings.music_step = 1
        ai_settings.music_old_time = curtime

def update_animations(ai_settings, screen):
    curtime = pygame.time.get_ticks()
    ai_settings.death_que.clear()
    for alien in ai_settings.dying_alien:
        rect = pygame.Rect(alien[0], alien[1], ai_settings.alien_width, ai_settings.alien_height)
        if alien[2] is 1:
            if alien[3] is 1:
                pic = ai_settings.pica1d1
            elif alien[3] is 2:
                pic = ai_settings.pica1d2
            elif alien[3] is 3:
                pic = ai_settings.pica1d3
                ai_settings.dying_alien.remove(alien)
        elif alien[2] is 2:
            if alien[3] is 1:
                pic = ai_settings.pica2d1
            elif alien[3] is 2:
                pic = ai_settings.pica2d2
            elif alien[3] is 3:
                pic = ai_settings.pica2d3
                ai_settings.dying_alien.remove(alien)
        else:
            if alien[3] is 1:
                pic = ai_settings.pica3d1
            elif alien[3] is 2:
                pic = ai_settings.pica3d2
            elif alien[3] is 3:
                pic = ai_settings.pica3d3
        image = pygame.transform.scale(pic, (ai_settings.alien_width, ai_settings.alien_height))
        ai_settings.death_que.append((image, rect))
        if curtime - ai_settings.alien_death_old_time > ai_settings.alien_death_wait:
            alien[3] += 1
            ai_settings.alien_death_old_time = curtime
            if alien[3] is 4:
                ai_settings.dying_alien.remove(alien)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    for alien in aliens:
        for bullet in bullets:
            if bullet.rect.colliderect(alien):
                if alien.type == 1:
                    stats.score += ai_settings.alien1_points
                elif alien.type == 2:
                    stats.score += ai_settings.alien2_points
                else:
                    stats.score += ai_settings.alien3_points
                ai_settings.dying_alien.append([alien.rect.x, alien.rect.y, alien.type, 1])
                sb.prep_score()
                ai_settings.music_speed *= ai_settings.music_speedup_scale
    check_high_score(stats, sb)
    pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:

        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_laser_ship_collision(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets, alien_lasers):
    for alien_laser in alien_lasers.copy():
        if alien_laser.rect.colliderect(ship):
            alien_lasers.remove(alien_laser)
            ship_hit(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    ai_settings.fleet_direction *= -1
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        alien.rect.x += (ai_settings.alien_speed_factor * ai_settings.fleet_direction)

def ship_hit(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:

        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        display_high_scores(ai_settings, screen, sb, high_scores)

    death_position = pygame.Rect(ship.rect.left, ship.rect.top, ship.rect.width, ship.rect.height)
    death_frames = [death_position, death_position, death_position, death_position, death_position, death_position, death_position]
    death_frames_pics = [pygame.image.load('images/Shipd1.png'), pygame.image.load('images/Shipd2.png'), pygame.image.load('images/Shipd3.png'),\
                    pygame.image.load('images/Shipd4.png'), pygame.image.load('images/Shipd5.png'), pygame.image.load('images/Shipd6.png'), pygame.image.load('images/Shipd7.png')]
    i = 0
    death_frames_images = [0, 0, 0, 0, 0, 0, 0]
    for pics in death_frames_pics:
        death_frames_images[i] = pygame.transform.scale(pics, (ship.rect.width, ship.rect.height))
        i += 1
    ship_death = Ship_Destroy_Animation(death_frames_images)
    i = 0
    while not ship_death.finished:
        while ship_death.imagerect() != death_frames_images[i]:
            ''''''
            # Continue until next image is ready to display
        ship.blitblank()
        ship.blitdeath(death_frames_images[i])
        pygame.display.flip()
        i += 1
    ship_death.reset()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)

def display_high_scores(ai_settings, screen, sb, high_scores):
    high_scores.display(sb.rounded_score)

def check_aliens_bottom(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:

            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets, alien_lasers):
    """
    Check if the fleet is at an edge, then update the postions of all aliens in the fleet.
    """
    curtime = pygame.time.get_ticks()

    check_fleet_edges(ai_settings, aliens)
    if curtime - ai_settings.old_time > ai_settings.wait:
        aliens.update()
        ai_settings.old_time = curtime

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, high_scores, ship, aliens, bullets)

def create_alien(ai_settings, screen, aliens, alien_number, row_number, type):
    """Create an alien, and place it in the row."""
    alien = Aliens(ai_settings, screen, alien_number, type)
    alien_width = alien.rect.width
    alien.x = 232 + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""

    ai_settings.music_speed = ai_settings.music_default_speed
    number_aliens_x = 11
    number_rows = 6

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        if row_number < 2:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number, 1)
        elif row_number < 4:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number, 2)
        elif row_number < 6:
            for alien_number in range(number_aliens_x):
                create_alien(ai_settings, screen, aliens, alien_number, row_number, 3)
'''
def create_barriers():
    # Delete old barriers

    # Create new barriers
    for i in range(24):
        # create barrier
    for i in range(4):
        # create barrierBR
    for i in range(4):
        #
    for i in range(4):
        #
    for i in range(4):
        #
'''

class Ship_Destroy_Animation:
    def __init__(self, frames, wait = 100, frameindex = 0, step = 1, looponce = True):
        self.frames = frames
        self.wait = wait
        self.frameindex = frameindex
        self.step = step
        self.looponce = looponce
        self.finished = False
        self.lastframe = len(frames) - 1 if step == 1 else 0
        self.last = None
    def frame_index(self):
        now = pygame.time.get_ticks()
        if self.last is None:
            self.last = now
            self.frameindex = 0 if self.step == 1 else len(self.frames) - 1
            return 0
        elif not self.finished and now - self.last > self.wait:
            self.frameindex += self.step
            if self.looponce and self.frameindex == self.lastframe:
                self.finished = True
            else:
                self.frameindex %= len(self.frames)
            self.last = now
        return self.frameindex
    def reset(self):
        self.last = None
        self.finished = False
    def __str__(self): return 'Timer(frames=' + self.frames + ', wait=' + str(self.wait) + ', index=' + str(self.frameindex) + ')'
    def imagerect(self):
        return self.frames[self.frame_index()]