import pygame
import os

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        # load the ship image and get its rect
        self.image = pygame.image.load(os.path.join('resources', 'ship.bmp'))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_left = False
        self.moving_right = False


        # Ships position

        self.x = float(self.rect.x)


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_left:
            if self.rect.left >= self.screen_rect.left:
                self.x -= self.settings.ship_speed
        if self.moving_right:
            if self.rect.right <= self.screen_rect.right:
                self.x += self.settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)