# -*- coding: utf-8 -*-

'''
Date: Пнд 06 Июн 2011 20:51:25
File: combatlog.py
Author: Igor V. Lashyn
Description: 
'''


class CombatLog(object):
    """docstring for CombatLog"""
    def __init__(self):
        self.events = []
       
    def push(self, event):
        """docstring for push"""
        self.events.append(event)

    def pop(self):
        """docstring for pop"""
        event = ""
        if len(self.events) != 0:
            event = self.events.pop(0)
        return event

    def draw(self, surface):
        """docstring for draw"""
        for i in range(len(self.events)):
            print self.events[i]
    
    def save(self, file_name):
        pass
