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
- переход на 1 слой вверх-вниз
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

from pygame.locals import *

from settings import *
from maze import maze_generator
from exception import * 
import monsters
from monsters.animals import *
from monsters.human import *
from events.messages import *
from terrain.wall import *
from terrain.ladder import *
from items.sausage import *
import combatlog
import pickle


def get_key(array, item):
    """docstring for get_key"""
    for keys, items in array.iteritems():
        if items == item:
            return keys
    return None

class World(object):
    """docstring for World"""
    def __init__(self):
        self.levels_number = LEVELS_NUMBER
        self.maze = [ self.init_lvl(x) for x in range(self.levels_number) ]
        self.first()

    def init_lvl(self, lvl):
        """docstring for init_lvl"""
        print "Generate %s lvl from %s levels"%(lvl, self.levels_number)
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

        for object_name, count in LIFE_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                maze[x][y] = LIFE_OBJECTS[object_name]

        for object_name, count in LADDER_OBJECTS_COUNTS.iteritems():
            for i in range(count):
                while 1:
                    x = random.randint(0,SIZE_X-1)
                    y = random.randint(0,SIZE_Y-1)
                    if maze[x][y] == free:
                        break
                maze[x][y] = LADDER_OBJECTS[object_name]

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

        
class Level(object):
    """docstring for Level"""

    def __init__(self):
        self.place = []
        self.life_obj = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.fog_image = pygame.image.load(OBJECTS_IMAGES["not_visited"]).convert()
        self.messages = pygame.sprite.Group()
        self.maze = None 
        

    def regenerate(self, maze):
        """генерация лабиринта"""
        self.place = []
        self.walls.empty()
        self.maze = maze
        for x in range(SIZE_X):
            self.place.append([])
            for y in range(SIZE_Y):
                if self.maze[x][y] == OBJECTS_PRESENTS["wall"]:
                    wall = Wall(x,y)
                    self.place[-1].append(wall)
                    self.walls.add(wall) 
                else:
                    self.place[-1].append(None)

        self.fog_of_war = [[ DEBUG for y in range(SIZE_Y)] for x in range(SIZE_X)]


    def init(self, maze):
        """расположение на игровом поле живых и неживых объектов"""
        self.place = []
        self.maze = maze
        self.fog_of_war = [[ DEBUG for y in range(SIZE_Y)] for x in range(SIZE_X)]

        self.items.empty()
        self.life_obj.empty()
        self.messages.empty()
        self.ladders.empty()
        self.walls.empty()

        for x in range(SIZE_X):
            self.place.append([])
            for y in range(SIZE_Y):
                in_cells = self.maze[x][y]

                if  in_cells == OBJECTS_PRESENTS["wall"]:
                    wall = Wall(x,y)
                    self.place[-1].append(wall)
                    self.walls.add(wall) 
                else:
                    self.place[-1].append(None)

                if in_cells in UNLIFE_OBJECTS.values():
                    object_name = get_key(UNLIFE_OBJECTS, in_cells)
                    sprite = globals().get(object_name)(x,y) 
                    self.items.add(sprite)

                if in_cells in LIFE_OBJECTS.values():
                    object_name = get_key(LIFE_OBJECTS, in_cells)
                    sprite = globals().get(object_name)(x,y) 
                    self.life_obj.add(sprite)
                    self.messages.add(sprite.message)

                if in_cells in LADDER_OBJECTS.values():
                    object_name = get_key(LADDER_OBJECTS, in_cells)
                    sprite = globals().get(object_name)(x,y) 
                    self.ladders.add(sprite)
                    if object_name == "LadderUp":
                        self.init_human_position = (x,y,)

    def put_object(self, obj):
        """ размещает объект в игровом мире """
        x,y = obj.location()
        self.place[x][y] = obj


    def draw(self, surface):
        self.walls.draw(surface)
        self.items.draw(surface)
        self.life_obj.draw(surface)
        self.ladders.draw(surface)
        self.draw_fog_of_war(surface)
        self.messages.draw(surface)

    def draw_fog_of_war(self, surface):
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                if not self.is_visited(x,y):
                    surface.blit(self.fog_image,(x * SPRITE_SIZE_X, y * SPRITE_SIZE_Y))

    def is_visited(self, x,y):
        return self.fog_of_war[x][y]

    def visited(self, x,y):
        self.fog_of_war[x][y] = True

    def move_life_objects(self):
        """ перемещение по игровому полю живых объектов"""
        self.life_obj.update(self)


    def who_here(self,x,y):
        """ возвращает объект, который находится в указанных координатах"""
        if x in range(SIZE_X) and y in range(SIZE_Y):
            return self.place[x][y]
        else:
            return None

    def is_free(self, x, y):
        """docstring for is_free"""
        return not isinstance(self.who_here(x,y), Wall)

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
#        for i in range(self.world.levels_number):
#            self.world.lvl_print(i)
        self.level = Level()
        self.combatlog = combatlog.CombatLog()
        log_rect = pygame.Rect((0,self.window.get_rect().height - STATUS_LINE_HEIGHT), (self.window.get_rect().width, STATUS_LINE_HEIGHT))
        self.log_surface = self.window.subsurface(log_rect)
        

    def init_lvl(self, level):
        """docstring for init_lvl"""
        if level == 0:
            maze = self.world.first()
        elif level == 1:
            maze = self.world.next()
        elif level == -1:
            maze = self.world.prev()
        else: 
            maze = self.world.get_level(self.world.current)
        self.level.init(maze)
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
            message = u"Молодец! Ты собрал всю колбасу!"
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
