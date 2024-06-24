class Settings:
    """A class to store all settings for alien invasion"""
    def __init__(self):
        """Initialize the game's settings"""
        # Screen Settings
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # bullet settings

        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.max_num_of_bullets = 100
        self.bullets_allowed = 10
        # alien settings

        self.alien_speed = 1.5
        self.fleet_drop_speed = 10

        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1