# -*- coding: utf-8 -*-

"""
Date: Пнд 30 Май 2011 20:33:39
File: objects.py
Author: Igor V. Lashyn
Description: 
"""

import pygame
import random

from settings import *


class Objects(pygame.sprite.Sprite):
    """ base class for all objects in game"""

    def __init__(self, x=random.randint(0, SIZE_X - 1), y=random.randint(0, SIZE_Y - 1)):
        pygame.sprite.Sprite.__init__(self)
        self.position = (x, y)

    def location(self):
        return self.position

    def arrange(self, x, y):
        """docstring for arrange"""
        if x in range(SIZE_X) and y in range(SIZE_Y):
            self.position = (x, y)
            self.rect.topleft = (x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y,)

    def load_single_image(self):
        """docstring for load_single_image"""
        x, y = self.location()
        self.image = pygame.image.load(OBJECTS_IMAGES[self.name]).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y,)
