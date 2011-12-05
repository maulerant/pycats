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
from level import *


class World(object):
    """docstring for World"""
    def __init__(self):
        self.levels_number = LEVELS_NUMBER
        self.levels = [ Level(x) for x in range(self.levels_number) ]
        self.first()


    def get_level(self, number):
        """docstring for get_level"""
        if number < 0:
            number = 0
        elif number >= self.levels_number:
            number = self.levels_number - 1 

        self.current = number 
        return self.levels[number]

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

    def save(self, path):
        """docstring for save"""
        fout = open (path, "wb")
        pickle.dump( self.levels_number, fout)
        pickle.dump( self.current, fout)
        for lvl in range(self.levels_number):
            self.levels[lvl].save(fout)

    def load(self, path):
        """docstring for load"""
        fin = open (path, "rb")
        self.levels_number = pickle.load(fin)
        self.levels = [ Level(x) for x in range(self.levels_number) ]
        self.current = pickle.load(fin)
        for lvl in range(self.levels_number):
            self.levels[lvl].load(fin)


