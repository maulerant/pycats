# -*- coding: utf-8 -*-

'''
Date: Пнд 05 Дек 2011 15:57:47
File: level.py
Author: Igor V. Lashyn
Description: 
'''

import random
import sys
import os
import pickle
import time
import pygame
import gettext

from pygame.locals import *

from settings import *
from exception import * 
import monsters
from world import *
from monsters.animals import *
from monsters.human import *
from terrain.wall import *
from terrain.ladder import *
from items.sausage import *


def get_key(array, item):
    """docstring for get_key"""
    for keys, items in array.iteritems():
        if items == item:
            return keys
    return None

class Level(object):
    """docstring for Level"""

    def __init__(self):
        self.place = []
        self.life_obj = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.fog_image = pygame.image.load(OBJECTS_IMAGES["not_visited"]).convert()
        self.messages = pygame.sprite.Group()
        self.maze = None 
        

    def regenerate(self, maze):
        """генерация лабиринта"""
        self.place = []
        self.walls.empty()
        self.maze = maze
        for x in range(SIZE_X):
            self.place.append([])
            for y in range(SIZE_Y):
                if self.maze[x][y] == OBJECTS_PRESENTS["wall"]:
                    wall = Wall(x,y)
                    self.place[-1].append(wall)
                    self.walls.add(wall) 
                else:
                    self.place[-1].append(None)

        self.fog_of_war = [[ DEBUG for y in range(SIZE_Y)] for x in range(SIZE_X)]


    def init(self, maze):
        """расположение на игровом поле живых и неживых объектов"""
        self.place = []
        self.maze = maze
        self.fog_of_war = [[ DEBUG for y in range(SIZE_Y)] for x in range(SIZE_X)]

        self.items.empty()
        self.life_obj.empty()
        self.messages.empty()
        self.ladders.empty()
        self.walls.empty()

        for x in range(SIZE_X):
            self.place.append([])
            for y in range(SIZE_Y):
                in_cells = self.maze[x][y]

                if  in_cells == OBJECTS_PRESENTS["wall"]:
                    wall = Wall(x,y)
                    self.place[-1].append(wall)
                    self.walls.add(wall) 
                else:
                    self.place[-1].append(None)

                if in_cells in UNLIFE_OBJECTS.values():
                    object_name = get_key(UNLIFE_OBJECTS, in_cells)
                    sprite = globals().get(object_name)(x,y) 
                    self.items.add(sprite)

                if in_cells in LIFE_OBJECTS.values():
                    object_name = get_key(LIFE_OBJECTS, in_cells)
                    sprite = globals().get(object_name)(x,y) 
                    self.life_obj.add(sprite)
                    self.messages.add(sprite.message)

                if in_cells in LADDER_OBJECTS.values():
                    object_name = get_key(LADDER_OBJECTS, in_cells)
                    sprite = globals().get(object_name)(x,y) 
                    self.ladders.add(sprite)
                    if object_name == "LadderUp":
                        self.init_human_position = (x,y,)

    def put_object(self, obj):
        """ размещает объект в игровом мире """
        x,y = obj.location()
        self.place[x][y] = obj


    def draw(self, surface):
        self.walls.draw(surface)
        self.items.draw(surface)
        self.life_obj.draw(surface)
        self.ladders.draw(surface)
        self.draw_fog_of_war(surface)
        self.messages.draw(surface)

    def draw_fog_of_war(self, surface):
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                if not self.is_visited(x,y):
                    surface.blit(self.fog_image,(x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y))

    def is_visited(self, x,y):
        return self.fog_of_war[x][y]

    def visited(self, x,y):
        self.fog_of_war[x][y] = True

    def move_life_objects(self):
        """ перемещение по игровому полю живых объектов"""
        self.life_obj.update(self)


    def who_here(self,x,y):
        """ возвращает объект, который находится в указанных координатах"""
        if x in range(SIZE_X) and y in range(SIZE_Y):
            return self.place[x][y]
        else:
            return None

    def is_free(self, x, y):
        """docstring for is_free"""
        return not isinstance(self.who_here(x,y), Wall)
