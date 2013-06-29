# -*- coding: utf-8 -*-

"""
Date: Вто 06 Дек 2011 09:21:56
File: inventory.py
Author: Igor V. Lashyn
Description: 
"""

import pygame
from pygame.locals import *

from settings import *


class Inventory(pygame.sprite.Group):
    """docstring for Inventory"""

    def __init__(self, *sprites):
        super(Inventory, self).__init__(*sprites)

    def move_on(self, direction):
        """docstring for move_on"""
        print direction

    def events(self, place, event):
        """docstring for events"""
        if event.type == KEYDOWN and event.key in (K_UP, K_LEFT, K_DOWN, K_RIGHT):
            self.move_on(event.key)

    def add(self, *item):
        """docstring for add"""
        super(Inventory, self).add(*item)
