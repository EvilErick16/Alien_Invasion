"""This file handles events in for the gaame."""

import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

class EventHandler:

    # Check events
    def check_events(self):

    def check_keydown_events(self):

    def check_keyup_events(self):

    def check_play_button(self):

    def check_high_score(self):

    def update_screen(self):

    # Ship functions
    def ship_hit(self):

    def fire_bullet(self):

    # Alien functions
    class Aliens:
        """All functions related to aliens."""
        def __init__(self):

        # def get_number_of_aliens_x(self):

        # def get_number_of_rows(self):

        def create_alien(self):

        def create_fleet(self):

        def check_fleet_edges(self):

        def change_fleet_direction(self):

        def check_aliens_bottom(self):

        def update_aliens(self):

    # Bullets
    def update_bullets(self):

    def check_bullet_alien_collision(self):
