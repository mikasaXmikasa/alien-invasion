import os
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to manage the aliens"""

    def __init__(self, ai_game):
        """Create a Alien object at the screen's top left"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Load the alien image and get its rect

        self.image = pygame.image.load(os.path.join('resources', 'alien.bmp'))
        self.rect = self.image.get_rect()
        
        # Start each new alien near the top left of the screen
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact horizontal position

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if alien is at the edge of the screen"""
        return (self.rect.right >= self.screen_rect.right) or (self.rect.left <= self.screen_rect.left)

    def update(self):
        """Move the alien to the right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
