# -*- coding: utf-8 -*-

"""
Date: Пнд 06 Июн 2011 21:50:01
File: ladder.py
Author: Igor V. Lashyn
Description: 
"""

import objects


class Ladder(objects.Objects):
    """Спуск или подъем на соседний уровень"""
    name = "ladder"

    def __init__(self, x, y):
        """docstring for __init__"""
        objects.Objects.__init__(self, x, y)
        self.load_single_image()


class LadderUp(Ladder):
    """docstring for LadderUp"""
    name = "ladderup"


class LadderDown(Ladder):
    """docstring for LadderDown"""
    name = "ladderdown"
