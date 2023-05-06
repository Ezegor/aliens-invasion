class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        #Screen settings
        self.screen_width = 600
        self.screen_height = 400
        self.bg_color = (230, 230, 230)

        #Sheep settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 3
        self.kill_bullet = True

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.alien_points = 50
        # fleet_direction fo 1 represnt right, -1 represents left.
        self.fleet_direction = 1

        # How quickly the game speed up
        self.speedup_scale = 1.1

        self.score_scale = 1.5

    
    def initialize_dynamic_settings(self):
        """Initialzie settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2
        self.alien_speed = 1.0
        self.alien_points = 50


        # fleet_direction fo 1 represnt right, -1 represents left.
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
