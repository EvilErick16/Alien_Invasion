from pygame.sprite import Sprite
from pygame import *


class Bunker(Sprite):
    def __init__(self, screen, size, bunker_color, row, column):
        Sprite.__init__(self)
        self.screen = screen
        self.height = size
        self.width = size
        self.color = bunker_color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column

    def update(self, keys, *args):
        self.screen.blit(self.image, self.rect)
