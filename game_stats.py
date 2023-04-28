class GameStats:
    """Track statistcs for Alien Invasion."""

    def __init__(self, ai_game):
        """Initizlize statistics."""
        self.settings = ai_game.settings
        self.score = 0
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1