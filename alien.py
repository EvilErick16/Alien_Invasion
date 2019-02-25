"""This file creates the Alien and the Alien explosions """

from pygame import *
from pygame.sprite import Sprite


class Aliens(Sprite):
    def __init__(self, screen,  row, column):
        Sprite.__init__(self)
        self.screen = screen
        self.row = row
        self.column = column
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def update(self, *args):
        self.screen.blit(self.image, self.rect)

    def load_images(self):
        image_names = ['enemy1_1', 'enemy1_2',
                       'enemy2_1', 'enemy2_2',
                       'enemy3_1', 'enemy3_2']
        load_images = {name: image.load('images/' + '{}.png'.format(name)).convert_alpha() for name in image_names}

        images = {0: ['1_2', '1_1'],
                  1: ['2_2', '2_1'],
                  2: ['2_2', '2_1'],
                  3: ['3_1', '3_2'],
                  4: ['3_1', '3_2'],
                  }
        img1, img2 = (load_images['enemy{}'.format(img_num)] for img_num in
                      images[self.row])
        self.images.append(transform.scale(img1, (40, 35)))
        self.images.append(transform.scale(img2, (40, 35)))


class AlienExplosion(Sprite):
    def __init__(self, screen,  enemy, *groups):
        super(AlienExplosion, self).__init__(*groups)
        self.screen = screen
        self.image = transform.scale(self.get_image(enemy.row), (40, 35))
        self.image2 = transform.scale(self.get_image(enemy.row), (50, 45))
        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.timer = time.get_ticks()

    @staticmethod
    def get_image(row):
        image_names = ['explosionblue', 'explosiongreen', 'explosionpurple']
        images_load = {name: image.load('images/' + '{}.png'.format(name)).convert_alpha()
                       for name in image_names}
        img_colors = ['purple', 'blue', 'blue', 'green', 'green']
        return images_load['explosion{}'.format(img_colors[row])]

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 100:
            self.screen.blit(self.image, self.rect)
        elif passed <= 200:
            self.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < passed:
            self.kill()
