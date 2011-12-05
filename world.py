# -*- coding: utf-8 -*-

'''
Date: Пнд 05 Дек 2011 15:54:10
File: world.py
Author: Igor V. Lashyn
Description: 
'''

import pickle
import random
import sys
import os

from settings import *
from maze import maze_generator
from level import *


class World(object):
    """docstring for World"""
    def __init__(self):
        self.levels_number = LEVELS_NUMBER
        self.maze = [ self.init_lvl(x) for x in range(self.levels_number) ]
        self.first()

    def init_lvl(self, lvl):
        """docstring for init_lvl"""
        maze = maze_generator(SIZE_X, SIZE_Y, OBJECTS_PRESENTS["wall"], OBJECTS_PRESENTS["clear"]) 
        free = OBJECTS_PRESENTS["clear"]

        for object_name, count in UNLIFE_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                maze[x][y] = UNLIFE_OBJECTS[object_name]

        for object_name, count in LADDER_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                maze[x][y] = LADDER_OBJECTS[object_name]

        for object_name, count in LIFE_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                maze[x][y] = LIFE_OBJECTS[object_name]


        return maze

    def get_level(self, number):
        """docstring for get_level"""
        if number < 0:
            number = 0
        if number >= self.levels_number:
            number = self.levels_number - 1 

        self.current = number 
        return self.maze[number]

    def first(self):
        return self.get_level(0)

    def last(self):
        return self.get_level(self.levels_number)

    def prev(self):
        """docstring for prev"""
        return self.get_level(self.current - 1)

    def next(self):
        """docstring for next"""
        return self.get_level(self.current + 1)

    def draw(self):
        """docstring for draw"""
        for lvl in range(LEVELS_NUMBER):
            self.lvl_print(lvl)

    def lvl_print(self, lvl):
        for y in range(SIZE_Y):
            maze = [ self.maze [lvl][x][y] for x in range(SIZE_X) ]
            
            print "".join(maze)

    def save(self, path):
        """docstring for save"""
        fout = open (path, "wb")
        pickle.dump( self.levels_number, fout)
        pickle.dump( self.current, fout)
        pickle.dump( self.maze, fout)

    def load(self, path):
        """docstring for load"""
        fin = open (path, "rb")
        self.levels_number = pickle.load(fin)
        self.current = pickle.load(fin)
        self.maze = pickle.load(fin)


