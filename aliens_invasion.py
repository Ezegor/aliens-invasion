import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,
                                              vsync=60)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Aliens Ivasion")

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

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_enents()
            self.ship.update()
            self._updae_bullets()
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

    def _updae_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()

        #Get rid of bullets that have disappeard.
        for bullet in self.bullets.copy():
            if(bullet.rect.bottom <= 0):
                self.bullets.remove(bullet)

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


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(self.bg_surf, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()
            
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
