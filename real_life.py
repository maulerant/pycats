# -*- coding: utf-8 -*-

'''
Date: Вто 17 Май 2011 11:26:32
File: real_life.py
Author: Igor V. Lashyn
Description: small game roguestyle
'''
#TODO:
"""
- !!!! ошибка при генерации лабиринта
- обработка искулюченией заинтересованными объектами (битва с котикаи )
- объединить картинки спрайтов в наборы, анимация движения живых объектов
- разобраться с ресурсами (символы, графнаборы етк)
- Добавить РПГ параметры монстрам
- вводим разрушаемость стен. 
- показ инвентаря. операции с инвентарем.
- крафт?
- сохранение игры и состояния уровней в файлы
- Класс эффектов, хинтов, вопросов
- REFACTORING!!!!!

"""

import random
import sys
import os
import pickle
import time
import pygame
import gettext

from pygame.locals import *

from settings import *
from exception import * 
import monsters
from world import *
from level import *
from monsters.animals import *
from monsters.human import *
from events.messages import *
from terrain.wall import *
from terrain.ladder import *
from items.sausage import *
import combatlog


gettext.install("pycats","./locale", unicode=True)



        

class Game(object):
    """docstring for Game"""
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('real_life')
        pygame.key.set_repeat(100,100)
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((SCREEN_SIZE_X,SCREEN_SIZE_Y))
        self.background = pygame.image.load(OBJECTS_IMAGES["clear"]).convert()
        self.human = Human(0,0)
        self.world = World()
        self.level = self.world.first()
        self.combatlog = combatlog.CombatLog()
        log_rect = pygame.Rect((0,self.window.get_rect().height - STATUS_LINE_HEIGHT), (self.window.get_rect().width, STATUS_LINE_HEIGHT))
        self.log_surface = self.window.subsurface(log_rect)
        

    def init_lvl(self, level):
        """docstring for init_lvl"""
        if level == 0:
            self.level = self.world.first()
        elif level == 1:
            self.level = self.world.next()
        elif level == -1:
            self.level = self.world.prev()
        else: 
            self.level = self.world.get_level(self.world.current)
        rect = self.log_surface.get_rect()
        self.log_surface.fill ((0,0,0,0),rect) 
        x,y = self.level.init_human_position
        self.human.arrange(x,y)
        

    def draw_bg(self, surface, bg):
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                rect = bg.get_rect()
                rect.topleft = (x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y)
                surface.blit(bg, rect)

    def event(self):
        """docstring for event"""
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key in (K_UP, K_LEFT, K_DOWN, K_RIGHT):
                try:
                    self.human.move_on(self.level,event.key) 
                except MoveBump as bump:
                    self.combatlog.push(bump.to_log())
                    for enemye in bump.enemyes:
                        try:
                            message = enemye.combat(self.level.messages)
                        except Combat as combat:
                            self.combatlog.push(combat.to_log())
                except MoveFindItem as finditems:
                    self.combatlog.push(finditems.to_log())
                except FindLadder as ladders:
                    self.combatlog.push(ladders.to_log())
                
            elif event.type == KEYDOWN and event.key == K_F1:
                ladders = pygame.sprite.spritecollide(self.human,self.level.ladders, False)
                if ladders != None:
                    for ladder in ladders:
                        if isinstance(ladder,LadderUp):
                            self.init_lvl(-1)
                        elif isinstance(ladder, LadderDown):
                            self.init_lvl(1)

            elif event.type == KEYDOWN and event.key == K_F2:
                self.combatlog.draw(self.window)

    def update(self):
        """docstring for update"""
        self.human.look_around(self.level)
        self.level.move_life_objects()

    def draw(self):
        """docstring for draw"""
        self.draw_bg(self.window, self.background)
        self.level.draw(self.window)
        self.human.draw(self.window)
        if self.human.item_count() == UNLIFE_OBJECTS_COUNTS["Sausage"]:
            message = _("You find all sausage")
            font = pygame.font.Font(None, 24)
            text = font.render(message, 1, (255,250,250))
            # copy the rendered message onto the board
            self.log_surface.blit (text, (10, 5)) 

def main():
    """main function for real_life"""
    game = Game()
    game.init_lvl(0)

    pygame.display.flip()


    while True:
        game.event()
        game.update()
        game.draw()

        pygame.display.flip()
        game.clock.tick(30)
    
if __name__ == '__main__':

    main()
