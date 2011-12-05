# -*- coding: utf-8 -*-

'''
Date: Пнд 06 Июн 2011 21:44:29
File: sausage.py
Author: Igor V. Lashyn
Description: 
'''

from objects import *

class Sausage(Objects):
    """docstring for Stone"""
    name = "sausage"

    def __init__(self, x, y):
        """docstring for __init__"""
        Objects.__init__(self, x, y)
        self.load_single_image()
