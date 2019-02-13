"""This file defines the ship class"""

import pygame
from pygame.sprite import Sprite
from sprite_sheet_functions import SpriteSheet


class Ship(Sprite):

    def __init__(self, ai_settings, screen, sprite_sheet_data):
        """Initialize the ship and set its starting position."""
        # Ship constructor, takes in an array of values
        super(Ship, self).__init__()
        sprite_sheet = SpriteSheet("sprite_sheet.png")

        # Grab the image for this platform (x, y, width, length)
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        self.rect = self.image.get_rect()

        # Get the screen size and the settings info
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        # Load the ship image and get its rect.
        # self.image = pygame.image.load('images/ship.bmp')
        # self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on movement flags"""
        # Update the ship's center value
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update the rectangle object to center
        self.rect.centerx = self.center

    def build(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
