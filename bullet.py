"""This file creates the bullet class for both aliens and ship"""

from pygame import *
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the alien or ship"""

    def __init__(self, screen, x_pos, y_pos, direction, speed, filename, side):
        """Create a bullet object at the shooter's current position."""
        super(Bullet, self).__init__()
        self.image = image.load('images/' + filename + '.png')
        self.screen = screen

        # create a bullet rect at (0,0) and then set the correct position
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.speed = speed
        self.direction = direction
        self.side = side
        self.filename = filename

        # Store the bullet's position as a decimal value.
        # self.y = float(self.rect.y)

        # self.color = ai_settings.bullet_color
        # self.speed_factor = ai_settings.bullet_speed_factor

    def update(self, keys, *args):
        """Update bullet position."""
        self.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 15 or self.rect.y > 650:
            self.kill()
        # update the decimal position of the bullet
        # self.y -= self.speed_factor
        # update the rect position
        # self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
