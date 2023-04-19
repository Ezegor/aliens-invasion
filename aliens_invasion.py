import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((600, 400), #pygame.FULLSCREEN,
                                              vsync=60)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Aliens Ivasion")

        #Is button pressed flags.
        self.lpressed = False
        self.rpressed = False

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

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

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        pygame.display.flip()
            
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
