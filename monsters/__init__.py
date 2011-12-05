# -*- coding: utf-8 -*-

'''
Date: Пнд 06 Июн 2011 20:08:20
File: __init__.py
Author: Igor V. Lashyn
Description: 
'''
import pygame
import objects 
from settings import *

class Monsters(objects.Objects):
    """docstring for Monsters"""
        

    def __init__(self, x, y):
        objects.Objects.__init__(self, x, y)
        self.life = True
        self.directed_bitmap = {}
        for direction, file_name in OBJECTS_IMAGES[self.name].iteritems():
            self.directed_bitmap[direction] = pygame.image.load(file_name).convert()
            colorkey = self.directed_bitmap[direction].get_at((0,0))
            self.directed_bitmap[direction].set_colorkey(colorkey, RLEACCEL)
        self.image = self.directed_bitmap[K_RIGHT]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y,)

    def new_position(self, delta_x, delta_y):
        """рассчет новой позиции объекта"""
        return (self.position[0] + delta_x, self.position[1] + delta_y)

    def turn(self, direction):
        """docstring for turn"""
        delta_x, delta_y = DIRECTION[direction]
        self.position = self.new_position(delta_x, delta_y)



