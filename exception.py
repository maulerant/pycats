# -*- coding: utf-8 -*-

"""
Date: Пнд 06 Июн 2011 11:26:51
File: exception.py
Author: Igor V. Lashyn
Description: игровые исключения. 
"""


class MoveException(Exception):
    """docstring for MoveException"""

    def __init__(self):
        pass


class MoveBump(MoveException):
    """docstring for MoveBump"""

    def __init__(self, enemyes):
        self.enemyes = enemyes

    def __str__(self):
        """docstring for __str__"""
        print "Bump in %s" % self.enemyes

    def to_log(self):
        """docstring for to_log"""
        return "Bump in %s" % self.enemyes


class MoveFindItem(MoveException):
    def __init__(self, items):
        self.items = items

    def __str__(self):
        print "Find items: %s" % self.items

    def to_log(self):
        """docstring for to_log"""
        return "Find items: %s" % self.items


class Combat(Exception):
    """docstring for Combat"""

    def __init__(self, who, hits):
        self.who = who
        self.hits = hits

    def __str__(self):
        print "%s hits %s" % (self.who.name, self.hits)

    def to_log(self):
        """docstring for to_log"""
        return "%s hits %s" % (self.who.name, self.hits)


class FindLadder(Exception):
    """docstring for FindLadder"""

    def __init__(self, ladder):
        self.ladder = ladder

    def __str__(self):
        print "Find ladder: %s" % self.ladder

    def to_log(self):
        """docstring for to_log"""
        return "Find ladder: %s" % self.ladder
