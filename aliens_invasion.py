import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manege game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), vsync=60)
        pygame.display.set_caption("Aliens Ivasion")

        #Is button pressed flags.
        self.lpressed = False
        self.rpressed = False

        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_enents()
            self.ship.update_pos()
            self._update_screen()
            self.clock.tick(60)

    def _check_enents(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                    self.ship.moving_left = False
                    self.rpressed = True
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                    self.ship.moving_right = False
                    self.lpressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                    self.rpressed = False
                    if self.lpressed:
                        self.ship.moving_left = True
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                    self.lpressed = False
                    if self.rpressed:
                        self.ship.moving_right = True


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()
            
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
