# -*- coding: utf-8 -*-

'''
Date: Птн 03 Июн 2011 15:23:42
File: monsters.py
Author: Igor V. Lashyn
Description: 
'''

import pygame
import random
import monsters
from settings import *
from events.messages import *
from exception import *

class Animal(monsters.Monsters):
    """docstring for Anymal"""
    name = "animal"

    def __init__(self,x,y):
        """docstring for __init__"""
        monsters.Monsters.__init__(self,x,y)
        self.timer = 0
        self.inventory = []
        self.message = Messages()
        self.message.rect.bottomleft = self.rect.topright
        self.direction = DIRECTION["stand"]
        self.next_move = self.move_on()
        self.hits = self.hit()

    def move_on(self, place=None):
        """docstring for move_on"""
        self.timer += 30
        if self.timer == 300:
            direction = random.choice(DIRECTION_KEY)
            self.timer = 0
            self.direction = DIRECTION[direction]

            x, y = self.new_position(self.direction[0], self.direction[1])
            if place.is_free(x,y):
                x_old, y_old = self.location()
                self.turn(direction)
                self.image = self.directed_bitmap[direction]
                for i in range(SPRITE_SIZE_Y):
                    self.rect.topleft = (x_old * SPRITE_SIZE_X + self.direction[0] * i, y_old * SPRITE_SIZE_Y +  self.direction[1]*i,)
                    yield None
                self.rect.topleft = (x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y,)

    def combat(self, messages):
        """docstring for combat"""
        try:
            messages.add(self.message)
            self.message.msg = self.hits.next()
            self.message.dirty = 1
            self.message.visible = 1
            self.message.update(self.rect)
            raise Combat(self, self.message.msg)
        except StopIteration:
            self.hits = self.hit()

    def hit(self):
        """docstring for hit"""
        questions = [u"Мяууу!!!", u"Где моя колбаска?", u"Бродят тут всякие..", u"Мяу! Мой хвостик!!", u"Усы, лапы и хвост. Вот мои документы."]
        for question in questions:
            yield question

    def update(self, place):
        try:
            self.next_move.next()
        except StopIteration:
            self.next_move = self.move_on(place)
            self.message.kill()
