"""This file contains the ufo class and the ufo explosion class"""

from pygame.sprite import Sprite
from pygame import *


class Ufo(Sprite):
    def __init__(self, screen):
        Sprite.__init__(self)
        self.screen = screen
        self.image = image.load('images/ufo.png')
        self.image = transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.moveTime = 25000
        self.direction = 1
        self.timer = time.get_ticks()
        # self.ufo_appeared = mixer.Sound('sounds/ufo.wav')  # mystery entered file
        # self.ufo_appeared.set_volume(0.3)
        # self.playSound = True

    def update(self, keys, curr_time, *args):
        reset_timer = False
        passed = curr_time - self.timer
        if passed > self.moveTime:
            if self.rect.x < 850 and self.direction == 1:
                self.rect.x += 2
                self.screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.rect.x -= 2
                self.screen.blit(self.image, self.rect)

        if self.rect.x > 850:
            self.direction = -1
            reset_timer = True
        if self.rect.x < -90:
            self.direction = 1
            reset_timer = True
        if passed > self.moveTime and reset_timer:
            self.timer = curr_time


class UfoExplosion(sprite.Sprite):
    def __init__(self, screen, ufo, score, *groups):
        super(UfoExplosion, self).__init__(*groups)
        self.text = Text(20, str(score), (255, 255, 255),
                         ufo.rect.x + 20, ufo.rect.y + 6)
        self.timer = time.get_ticks()
        self.screen = screen

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 200 or 400 < passed <= 600:
            self.text.draw(self.screen)
        elif 600 < passed:
            self.kill()


class Text(object):
    def __init__(self, size, msg, msg_color, xpos, ypos):
        self.font = font.SysFont("Arial", size)
        self.surface = self.font.render(msg, True, msg_color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)
