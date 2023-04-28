import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Aliens Ivasion")

        # Create an instance to store game statistcs.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.bg_surf = pygame.image.load('images/kosmos.jpg').convert()
        self.bg_surf = pygame.transform.scale(self.bg_surf,
                                              (self.settings.screen_width, self.settings.screen_height))
        #Is button pressed flags.
        self.lpressed = False
        self.rpressed = False

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        
        # Make the Play Button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_enents()

            if self.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_enents(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clcks Play."""
        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:

            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and centered the ship
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            self.ship.moving_left = False
            self.rpressed = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            self.ship.moving_right = False
            self.lpressed = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        

    def _check_keyup_events(self, event):
        """Respond to releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.rpressed = False
            if self.lpressed:
                self.ship.moving_left = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.lpressed = False
            if self.rpressed:
                self.ship.moving_right = True
        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()

        #Get rid of bullets that have disappeard.
        for bullet in self.bullets.copy():
            if(bullet.rect.bottom <= 0):
                self.bullets.remove(bullet)
        
        self._check_bulett_alien_collisions()
       
    
    def _check_bulett_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
        self.bullets, self.aliens, self.settings.kill_bullet, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
        

    def _create_fleet(self):
        """Create the fleet of aiens."""
        # Make an alien and keep adding aliens until ther's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        current_x = alien_width
        current_y = alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value, and increment y value.
            current_y += 2 * alien_height
            current_x = alien_width

    def _create_alien(self, x_position : int, y_position : int):
        """Create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop th etire fleet and chage the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        # Look for aliens hitting the bottom og the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._sheep_hit()



    def _sheep_hit(self):
        """Respond to the ship being hit an alien."""
        if self.stats.ships_left > 0:
            #Decrement ship_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any remainng bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.bg_surf, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        if not self.game_active:
            self.play_button.draw_button()
        self.sb.show_score()
        pygame.display.flip()
            
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
