import sys
import pygame
from time import sleep
from settings import Settings
from bullet  import Bullet
from ship import Ship
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # self.screen object is called a surface in pygame is a part of the screen where a game element can be displayed
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.full_screen = False
        # alternatively we can set full screen using following
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        
        # Create an instance to store game statistics

        self.stats = GameStats(self)

        # Ship
        self.ship = Ship(self)
        
        # Bullets
        self.bullets = pygame.sprite.Group()

        # Alien fleet

        self.aliens = pygame.sprite.Group()
        self.__create_fleet()

        # Game is active or not
        self.game_active = True

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # watch for keyboard and mouse events
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

            # Python will do its best to run the while loop 60 times
            self.clock.tick(60)
    

    def _check_events(self):
        """Responds to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()         
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_q:
            sys.exit()
        

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # makes the most recently drawn screen visible
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_bullet_alien_collisions(self):
        """Respond to bullet alien collision"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self.__create_fleet()


    def _update_bullets(self):
        """Update the bullets, delete the old bullets and remove bullets that have hit the aliens"""
        
        self.bullets.update()

        # check for any bullets that have hit aliens
        # if so, get rid of the bullet and the alien
        self._check_bullet_alien_collisions()

        # get rid of bullets that have disappered
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def __create_alien(self, x, y):
        alien = Alien(self)
        alien.x = x
        alien.y = y
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def __create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and keep adding aliens until there's no room left
        # spacing between aliens is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height


        while current_y < self.settings.screen_height - 4 * alien_height:
            while current_x < self.settings.screen_width - 2 * alien_width:
                new_alien = self.__create_alien(current_x, current_y)
                current_x += 1.5 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _change_fleet_direction_and_drop(self):
        """Drop the entire fleet and changes the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction_and_drop()


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_aliens(self):
        """Update all the aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Ship hit!!!")


        self._check_aliens_bottom()
        


    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Get rid of any remaining bullets and aliens
            self.__create_fleet
            self.ship.center_ship()

            # Pause
            sleep(1)
        else:
            self.game_active = False
       
if __name__ == '__main__':
    # make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game() 