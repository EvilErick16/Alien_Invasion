"""This file is used to create the sprite animations."""

import pygame


class SpriteSheet(object):
        """Grab images out of a sprite sheet."""
        def __init__(self, file_name):
            """Constructor"""

            # Load the sprite sheet
            self.sprite_sheet = pygame.image.load(file_name).convert()

        def get_image(self, x, y, width, length):
            """Get the image from the sprite sheet."""

            # Create a blank image
            image = pygame.Surface([width, length]).convert()

            # Copy the sprite from the sheet to the image
            image.blit(self.sprite_sheet, (0, 0), (x, y, width, length))

            # Return the image
            return image
