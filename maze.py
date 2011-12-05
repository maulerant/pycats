# -*- coding: utf-8 -*-

'''
Date: Срд 18 Май 2011 10:54:02
File: maze.py
Author: Igor V. Lashyn
Description: генератор лабиринтов по "ширинному" методу
'''

#   1. создаем массив под лабиринт, заполняем его стенами
#   1.1 создаем массив "начал" тунелей
#   2. случайным образом получаем начальную точку для прогрызания хода, заносим в массив начал
#   3. для каждого из направлений вызываем процедуру прогрызания. первоначальную 
#   точку удаляем из этого массива
#   3.1 процедура определяет (рандомно) будем ли копать в данном направлении
#   и есть ли возможность копать (соседи, пограничные стены)
#   3.2 случайным образом определяем глубину тунеля
#   3.3 копаем пока не выберем длинну или не наткнемся на существующий тунель (пограничную стену)
#   3.4 сохраняем конец тунеля в массив начал

import random

SIZE_X = 30
SIZE_Y = 20
DIRECTION = { "up" : (0,1), "down" : (0, -1), "left" : (-1,0), "right": (1,0) }

wall = "#"
tunnel = " "
tunnel_max_lenght = 10

def mole(maze, size_x, size_y,  begin_point, delta):
    """docstring for mole"""
    x_begin, y_begin = begin_point
    x_end, y_end = (-1,-1)
    dx, dy  = delta

    if random.randint(0, 10) < 8 and (x_begin +dx) in range(size_x) and (y_begin+ dy) in range(size_y) and maze[x_begin+dx][y_begin+dy] == wall :
        tunnel_len = random.randint(1, tunnel_max_lenght)
        for step in range(tunnel_len):
            x_next, y_next = (x_begin + step * dx, y_begin + step * dy)
            x_hop, y_hop = (x_begin + (step + 1) * dx, y_begin + (step + 1) * dy)

#TODO: добавить проверку на наличие стенок в диагональных клетках, что бы избегать "комнат"
#            if x_hop in range(SIZE_X) and y_hop in range(SIZE_Y) and maze[x_next+1][y_next+1] == wall and   maze[x_next-1][y_next-1] == wall and   maze[x_next+1][y_next-1] == wall and   maze[x_next-1][y_next+1] == wall and   maze[x_hop][y_hop] == wall:

            if x_hop in range(size_x) and y_hop in range(size_y) and  maze[x_next][y_next] == wall and maze[x_hop][y_hop] == wall:
                maze[x_next][y_next] = tunnel
                x_end = x_next
                y_end = y_next

    return (x_end, y_end)

def maze_generator(size_x, size_y, wall, tunnel):
    """ x_size, y_size dimension of maze, wall and  tunnel symbol для обозначения проходимых и не проходимых клеток"""
    maze = [[wall for y in range(size_y)] for x in range(size_x)]
    begins = []
    begins.append((random.randint(2, size_x-2), random.randint(2, size_y-2)))
    maze[begins[0][0]][begins[0][1]] = tunnel

    while len(begins) > 0:
        for direct, deltas in DIRECTION.iteritems():
            endpoint = mole(maze, size_x, size_y, begins[0], deltas)
            if endpoint != (-1,-1):
                begins.append(endpoint)
        begins.pop(0)
    return maze


if __name__ == '__main__':
    maze = maze_generator(SIZE_X, SIZE_Y, wall, tunnel)
    for y in range(SIZE_Y):
        test = [ maze [x][y] for x in range(SIZE_X) ]
        print "".join(test)

