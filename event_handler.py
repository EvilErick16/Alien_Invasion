"""This file makes the game logic and handles events in the game"""

from pygame import *
from ship import Ship, Life, ShipExplosion
from ufo import Text, UfoExplosion, Ufo
from bullet import Bullet
from bunker import Bunker
from fleet import Fleet
from alien import Aliens, AlienExplosion
from random import choice
import sys


class SpaceInvaders(object):
    def __init__(self):
        mixer.pre_init(44100, -16, 1, 4096)
        init()
        # Colors (R, G, B)
        white = (255, 255, 255)
        green = (78, 255, 87)
        blue = (80, 255, 239)
        purple = (203, 0, 255)
        red = (237, 28, 36)
        self.clock = time.Clock()
        self.caption = display.set_caption('Space Invaders')
        self.screen = display.set_mode((800, 600))
        self.background = image.load('images/background.png').convert()
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False
        # Counter for alien starting position (increased each new round)
        self.alien_position = 65
        self.titleText = Text(50, 'Space Invaders', white, 164, 155)
        self.titleText2 = Text(25, 'Press Start to Play', white,
                               201, 225)
        self.game_over_text = Text(50, 'Game Over', white, 250, 270)
        self.nextRoundText = Text(50, 'Next Round', white, 240, 270)
        self.alien1_text = Text(25, '   =   10 pts', green, 368, 270)
        self.alien2_text = Text(25, '   =  20 pts', blue, 368, 320)
        self.alien3_text = Text(25, '   =  30 pts', purple, 368, 370)
        self.alien4_text = Text(25, '   =  ?????', red, 368, 420)
        self.scoreText = Text(20, 'Score', white, 5, 5)
        self.livesText = Text(20, 'Lives ', white, 640, 5)

        self.life1 = Life(self.screen, 715, 3)
        self.life2 = Life(self.screen, 742, 3)
        self.life3 = Life(self.screen, 769, 3)
        self.livesGroup = sprite.Group(self.life1, self.life2, self.life3)

    def reset(self, score):
        self.player = Ship(self.screen)
        self.playerGroup = sprite.Group(self.player)
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.ufo = Ufo(self.screen)
        self.ufo_group = sprite.Group(self.ufo)
        self.alien_bullets = sprite.Group()
        self.make_aliens()
        self.allSprites = sprite.Group(self.player, self.aliens,
                                       self.livesGroup, self.ufo)
        self.keys = key.get_pressed()

        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.shipTimer = time.get_ticks()
        self.score = score
        # self.create_audio()
        self.make_new_ship = False
        self.ship_alive = True

    def make_aliens(self):
        self.aliens = Fleet(10, 5)
        for row in range(5):
            for column in range(10):
                alien = Aliens(self.screen, row, column)
                alien.rect.x = 157 + (column * 50)
                alien.rect.y = self.alien_position + (row * 45)
                self.aliens.add(alien)

    def make_bunker(self, number):
        bunkers = sprite.Group()
        for row in range(4):
            for column in range(9):
                bunker = Bunker(self.screen, 10, (50, 255, 50), row, column)
                bunker.rect.x = 50 + (200 * number) + (column * bunker.width)
                bunker.rect.y = 450 + (row * bunker.height)
                bunkers.add(bunker)
        return bunkers

    @staticmethod
    def should_exit(evt):
        # type: (pygame.event.EventType) -> bool
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_q)

    def check_input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) == 0 and self.ship_alive:
                        bullet = Bullet(self.screen, self.player.rect.x + 23,
                                        self.player.rect.y + 5, -1,
                                        15, 'laser', 'center')
                        self.bullets.add(bullet)
                        self.allSprites.add(self.bullets)
                        # self.sounds['shoot'].play()
                if e.key == K_LEFT and self.player.rect.x > 5:
                    self.player.moving_left = True
                elif e.key == K_RIGHT and self.player.rect.x < 800:
                    self.player.moving_right = True
            elif e.type == KEYUP:
                if e.key == K_LEFT:
                    self.player.moving_left = False
                elif e.key == K_RIGHT:
                    self.player.moving_right = False

    def make_aliens_shoot(self):
        if (time.get_ticks() - self.timer) > 700 and self.aliens:
            alien = self.aliens.random_bottom()
            self.alien_bullets.add(
                Bullet(self.screen, alien.rect.x + 14, alien.rect.y + 20, 1, 5,
                       'enemylaser', 'center'))
            self.allSprites.add(self.alien_bullets)
            self.timer = time.get_ticks()

    def calculate_score(self, row):
        scores = {0: 30, 1: 20, 2: 20, 3: 10, 4: 10, 5: choice([50, 100, 150, 300])}
        score = scores[row]
        self.score += score
        return score

    def check_collisions(self):
        sprite.groupcollide(self.bullets, self.alien_bullets, True, True)

        for alien in sprite.groupcollide(self.aliens, self.bullets,
                                         True, True).keys():
            # self.sounds['invaderkilled'].play()
            self.calculate_score(alien.row)
            AlienExplosion(self.screen, alien, self.explosionsGroup)
            self.game_timer = time.get_ticks()

        for ufo in sprite.groupcollide(self.ufo_group, self.bullets,
                                       True, True).keys():
            # ufo.mysteryEntered.stop()
            # self.sounds['mysterykilled'].play()
            score = self.calculate_score(ufo.row)
            UfoExplosion(self.screen, ufo, score, self.explosionsGroup)
            new_ufo = Ufo(self.screen)
            self.allSprites.add(new_ufo)
            self.ufo_group.add(new_ufo)

        for player in sprite.groupcollide(self.playerGroup, self.alien_bullets,
                                          True, True).keys():
            if self.life3.alive():
                self.life3.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life1.alive():
                self.life1.kill()
            else:
                self.gameOver = True
                self.startGame = False
            # self.sounds['shipexplosion'].play()
            ShipExplosion(self.screen, self.player, self.explosionsGroup)
            self.make_new_ship = True
            self.shipTimer = time.get_ticks()
            self.ship_alive = False

        if self.aliens.bottom >= 540:
            sprite.groupcollide(self.aliens, self.playerGroup, True, True)
            if not self.player.alive() or self.aliens.bottom >= 600:
                self.gameOver = True
                self.startGame = False

        sprite.groupcollide(self.bullets, self.all_bunkers, True, True)
        sprite.groupcollide(self.alien_bullets, self.all_bunkers, True, True)
        if self.aliens.bottom >= 450:
            sprite.groupcollide(self.aliens, self.all_bunkers, False, True)

    def create_new_ship(self, create_ship, curr_time):
        if create_ship and (curr_time - self.shipTimer > 900):
            self.player = Ship(self.screen)
            self.allSprites.add(self.player)
            self.playerGroup.add(self.player)
            self.make_new_ship = False
            self.ship_alive = True

    def create_game_over(self, curr_time):
        self.screen.blit(self.background, (0, 0))
        passed = curr_time - self.timer
        if passed < 750:
            self.game_over_text.draw(self.screen)
        elif 750 < passed < 1500:
            self.screen.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.game_over_text.draw(self.screen)
        elif 2250 < passed < 2750:
            self.screen.blit(self.background, (0, 0))
        elif passed > 3000:
            self.mainScreen = True

        for e in event.get():
            if self.should_exit(e):
                sys.exit()

    def create_main_menu(self):
        self.enemy1 = image.load('images/enemy3_2.png')
        self.enemy1 = transform.scale(self.enemy1, (40, 40))
        self.enemy2 = image.load('images/enemy2_2.png')
        self.enemy2 = transform.scale(self.enemy2, (40, 40))
        self.enemy3 = image.load('images/enemy1_2.png')
        self.enemy3 = transform.scale(self.enemy3, (40, 40))
        self.enemy4 = image.load('images/ufo.png')
        self.enemy4 = transform.scale(self.enemy4, (80, 40))
        self.screen.blit(self.enemy1, (318, 270))
        self.screen.blit(self.enemy2, (318, 320))
        self.screen.blit(self.enemy3, (318, 370))
        self.screen.blit(self.enemy4, (299, 420))

    def main(self):
        while True:
            if self.mainScreen:
                self.screen.blit(self.background, (0, 0))
                self.titleText.draw(self.screen)
                self.titleText2.draw(self.screen)
                self.alien1_text.draw(self.screen)
                self.alien2_text.draw(self.screen)
                self.alien3_text.draw(self.screen)
                self.alien4_text.draw(self.screen)
                self.create_main_menu()
                for e in event.get():
                    if self.should_exit(e):
                        sys.exit()
                    if e.type == KEYUP:
                        # Only create blockers on a new game, not a new round
                        self.all_bunkers = sprite.Group(self.make_bunker(0),
                                                        self.make_bunker(1),
                                                        self.make_bunker(2),
                                                        self.make_bunker(3))
                        self.livesGroup.add(self.life1, self.life2, self.life3)
                        self.reset(0)
                        self.startGame = True
                        self.mainScreen = False

            elif self.startGame:
                if not self.aliens and not self.explosionsGroup:
                    curr_time = time.get_ticks()
                    if curr_time - self.game_timer < 3000:
                        self.screen.blit(self.background, (0, 0))
                        self.scoreText2 = Text(20, str(self.score),
                                               (78, 255, 87), 85, 5)
                        self.scoreText.draw(self.screen)
                        self.scoreText2.draw(self.screen)
                        self.nextRoundText.draw(self.screen)
                        self.livesText.draw(self.screen)
                        self.livesGroup.update()
                        self.check_input()
                    if curr_time - self.game_timer > 3000:
                        # Move enemies closer to bottom
                        self.alien_position += 35
                        self.reset(self.score)
                        self.game_timer += 3000
                else:
                    curr_time = time.get_ticks()
                    # self.play_main_music(curr_time)
                    self.screen.blit(self.background, (0, 0))
                    self.all_bunkers.update(self.screen)
                    self.scoreText2 = Text(20, str(self.score), (78, 255, 87),
                                           85, 5)
                    self.scoreText.draw(self.screen)
                    self.scoreText2.draw(self.screen)
                    self.livesText.draw(self.screen)
                    self.check_input()
                    self.aliens.update(curr_time)
                    self.allSprites.update(self.keys, curr_time)
                    self.explosionsGroup.update(curr_time)
                    self.check_collisions()
                    self.create_new_ship(self.make_new_ship, curr_time)
                    self.make_aliens_shoot()

            elif self.gameOver:
                curr_time = time.get_ticks()
                # Reset alien starting position
                self.alien_position = 65
                self.create_game_over(curr_time)

            display.update()
            self.clock.tick(60)

