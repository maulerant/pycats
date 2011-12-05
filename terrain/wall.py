# -*- coding: utf-8 -*-

'''
Date: Пнд 06 Июн 2011 20:29:23
File: wall.py
Author: Igor V. Lashyn
Description: 
'''

import pygame
from settings import *
from objects import *

class Wall(Objects):
    """docstring for Wall"""
    name = "wall"

    def __init__(self, x, y):
        """docstring for __init__"""
        Objects.__init__(self, x, y)
        self.load_single_image()
