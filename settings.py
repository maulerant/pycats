# -*- coding: utf-8 -*-

'''
Date: Пнд 30 Май 2011 19:45:29
File: settings.py
Author: Igor V. Lashyn
Description: 
'''

import os
from pygame.locals import *

DEBUG = True

GAMER_AVATAR = "robot"
RESOURCE_DIR = "data"


STATUS_LINE_HEIGHT = 30
# play field dimension size_x*size_y

SPRITE_SIZE_X = 30
SPRITE_SIZE_Y = 30

SIZE_X = 25
SIZE_Y = 20
INV_WINDOW_SIZE_X = 5
INV_WINDOW_SIZE_Y = 5

X = 0
Y = 1
START_LEVEL = 0
LEVELS_NUMBER = 10

# direction управление awsd 

DIRECTION = { "stand": (0,0), K_DOWN: (0,1), K_UP: (0,-1), K_LEFT: (-1,0), K_RIGHT: (1,0), }
DIRECTION_KEY = (K_DOWN, K_UP, K_LEFT, K_RIGHT)

SCREEN_SIZE_X = SIZE_X * SPRITE_SIZE_X
SCREEN_SIZE_Y = SIZE_Y * SPRITE_SIZE_Y + STATUS_LINE_HEIGHT

OBJECTS_PRESENTS = { "human": "0", "sausage": "@", "clear": " ", "wall": "#", "animal": "*", "undeground": "?"}
OBJECTS_IMAGES = { "human": {   K_DOWN:os.path.join(RESOURCE_DIR,GAMER_AVATAR,"down.gif"), 
                                K_UP:os.path.join(RESOURCE_DIR,GAMER_AVATAR,"up.gif"), 
                                K_LEFT:os.path.join(RESOURCE_DIR,GAMER_AVATAR,"left.gif"), 
                                K_RIGHT:os.path.join(RESOURCE_DIR,GAMER_AVATAR,"right.gif"),}, 
                    "sausage": os.path.join(RESOURCE_DIR,"sausage.gif"), 
                    "inventory": os.path.join(RESOURCE_DIR,"inventory_bg.gif"), 
                    "clear": os.path.join(RESOURCE_DIR,"clear.gif"), 
                    "wall": os.path.join(RESOURCE_DIR,"wall.gif"), 
                    "animal": { K_DOWN:os.path.join(RESOURCE_DIR,"animal","down.gif"), 
                                K_UP:os.path.join(RESOURCE_DIR,"animal","up.gif"), 
                                K_LEFT:os.path.join(RESOURCE_DIR,"animal","left.gif"), 
                                K_RIGHT:os.path.join(RESOURCE_DIR,"animal","right.gif"),},
                    "not_visited": os.path.join(RESOURCE_DIR,"not_visited.gif"), 
                    "ladder": os.path.join(RESOURCE_DIR, "ladder.gif"),
                    "ladderup": os.path.join(RESOURCE_DIR, "ladderup.gif"),
                    "ladderdown": os.path.join(RESOURCE_DIR, "ladderdown.gif"),}


# objects count for fill game place

LADDER_OBJECTS_COUNTS = { "LadderUp": 1,"LadderDown": 1,}
UNLIFE_OBJECTS_COUNTS = { "Sausage": 4, }
LIFE_OBJECTS_COUNTS = { "Animal": 7, }
LADDER_OBJECTS = { "LadderUp": ">","LadderDown": "<",}
UNLIFE_OBJECTS = { "Sausage": "@", }
LIFE_OBJECTS = { "Animal": "*", }

