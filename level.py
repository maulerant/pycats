# -*- coding: utf-8 -*-

'''
Date: Пнд 05 Дек 2011 15:57:47
File: level.py
Author: Igor V. Lashyn
Description: 
'''

import random
import pickle
import pygame
import gettext

from pygame.locals import *

from settings import *
import monsters
from world import *
from monsters.animals import *
from terrain.wall import *
from terrain.ladder import *
from items.sausage import *
from maze import maze_generator


class Level(object):
    """docstring for Level"""

    def __init__(self, lvl):
        self.place = []
        self.number = lvl
        self.life_obj = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.messages = pygame.sprite.Group()
        self.fog_image = pygame.image.load(OBJECTS_IMAGES["not_visited"]).convert()
        self.init_maze() 
        self.fog_of_war = [[ DEBUG for y in range(SIZE_Y)] for x in range(SIZE_X)]
        
    def init_maze(self):
        """docstring for init_lvl"""
        maze = maze_generator(SIZE_X, SIZE_Y, OBJECTS_PRESENTS["wall"], OBJECTS_PRESENTS["clear"]) 
        free = OBJECTS_PRESENTS["clear"]
        self.place = []

        self.items.empty()
        self.life_obj.empty()
        self.messages.empty()
        self.ladders.empty()
        self.walls.empty()

        for object_name, count in UNLIFE_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                sprite = globals().get(object_name)(x,y) 
                self.items.add(sprite)
                maze[x][y] = UNLIFE_OBJECTS[object_name]

        for object_name, count in LADDER_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                sprite = globals().get(object_name)(x,y) 
                self.ladders.add(sprite)
                if object_name == "LadderUp":
                    self.init_human_position = (x,y,)
                maze[x][y] = LADDER_OBJECTS[object_name]

        for object_name, count in LIFE_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                sprite = globals().get(object_name)(x,y) 
                self.life_obj.add(sprite)
                self.messages.add(sprite.message)
                maze[x][y] = LIFE_OBJECTS[object_name]

        for x in range(SIZE_X):
            self.place.append([])
            for y in range(SIZE_Y):
                in_cells = maze[x][y]

                if  in_cells == OBJECTS_PRESENTS["wall"]:
                    wall = Wall(x,y)
                    self.place[-1].append(wall)
                    self.walls.add(wall) 
                else:
                    self.place[-1].append(None)


        return maze


    def put_object(self, obj):
        """ размещает объект в игровом мире """
        x,y = obj.location()
        self.place[x][y] = obj


    def draw(self, surface):
        self.walls.draw(surface)
        self.items.draw(surface)
        self.ladders.draw(surface)
        self.life_obj.draw(surface)
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

    def save(self, fout):
        """docstring for save"""
        pass

    def load(self, fin):
        """docstring for load"""
        pass

