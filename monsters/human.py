# -*- coding: utf-8 -*:wq

'''
Date: Пнд 06 Июн 2011 20:24:01
File: human.py
Author: Igor V. Lashyn
Description: 
'''

import pygame
import monsters
from settings import *
from terrain.wall import *
from exception import *

class Human(monsters.Monsters):
    """docstring for Human"""
    name = "human"

    def __init__(self,x,y):
        """docstring for __init__"""
        monsters.Monsters.__init__(self,x,y)
        self.inventory = pygame.sprite.Group()


    def move_on(self, place, direction):
        """ перемещаем персонажа на один шаг по игровому пространству"""
        x, y = self.new_position(DIRECTION[direction][0], DIRECTION[direction][1])
        neighbor = place.who_here(x,y)
        if not isinstance(neighbor, Wall):
            self.turn(direction)
            self.image = self.directed_bitmap[direction]
            self.rect.topleft = (x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y,)
            self.look_around(place)
            # если ли рядом итемы, если  есть собираем
            collide = pygame.sprite.spritecollide(self, place.items, True)
            if collide != []:
                self.inventory.add(collide)
                raise MoveFindItem(collide)
            # столкнулись с живностью? взаимодействуем
            collide = pygame.sprite.spritecollide(self, place.life_obj, False)
            if collide != []:
                raise MoveBump(collide)
            
            # ladders?
            collide = pygame.sprite.spritecollide(self, place.ladders, False)
            if collide != []:
                raise FindLadder(collide)

    def draw(self, surface):
        surface.blit(self.image,self.rect)

    
    def look_around(self, place):
        """убираем туман войны с соедних клеток"""
        x,y = self.location()
        for dx in range(-1,2):
            for dy in range(-1,2):
                if not place.is_visited(x+dx,y+dy):
                    place.visited(x+dx, y+dy)

    def turf(self, item):
        """ выбросить предмет из инвентаря """
        pass
    
    def item_count(self):
        """docstring for item_count"""
        return len(self.inventory)

    def arrange(self, x, y):
        """docstring for arrange"""
        super(Human, self).arrange(x,y)
        self.inventory.empty()
