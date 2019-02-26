"""This file defines the ship, ship explosion, and the life classes"""

from pygame import *
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.moving_left = False
        self.moving_right = False

        # Load the ship image, and get its rect.
        self.image = image.load('images/Truck.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = self. screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.speed = 5

    def update(self, key_press, *args):
        """Update the ship's position"""
        # Update the ship's center value
        if self.moving_left and self.rect.x > 5:
            self.rect.centerx -= self.speed
        elif self.moving_right and self.rect.x < 800:
            self.rect.centerx += self.speed
        # Update the ship
        self.screen.blit(self.image, self.rect)


class ShipExplosion(Sprite):
    def __init__(self, screen, ship, *groups):
        super(ShipExplosion, self).__init__(*groups)
        self.screen = screen
        self.image = image.load('images/explosionblue.png')
        self.rect = self.image.get_rect(topleft=(ship.rect.x, ship.rect.y))
        self.timer = time.get_ticks()

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if 300 < passed <= 600:
            self.screen.blit(self.image, self.rect)
        elif 900 < passed:
            self.kill()


class Life(sprite.Sprite):
    def __init__(self, screen,  xpos, ypos):
        self.screen = screen
        sprite.Sprite.__init__(self)
        self.image = image.load('images/Truck.png')
        self.image = transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

    def update(self, *args):
        self.screen.blit(self.image, self.rect)
