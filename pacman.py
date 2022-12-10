import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

import numpy as np
import math


class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.setSpeed(110)
        self.sprites = PacmanSprites(self)
        self.target_point = Vector2(0, 0) # Set the target Point of Pacman --- Need To Optimize
        self.target_set = False # If(reach_Target) target_set = false set a new Target_Point

        self.curmap = None # Map 2D that see ghosts like obstacles --- Idea create an 3D map, third dimension is time?
        self.basemap = self.basemap() # Map start

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt, ghosts, pelletList):
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt

        # direction = self.getValidKey()
        # print(self.position)

        self.updatemap(ghosts)
        direction = self.direction
        if ((self.position.x % 16 < 1.7 or self.position.x % 16 > 14.3)
                and (self.position.y % 16 < 1.7 or self.position.y % 16 > 14.3)):  # 3.4 = 1 frame
            if not self.target_set:
                self.target_point = np.random.randint(pelletList.__len__())
                self.target_set = True
            direction = self.a_star(pelletList[self.target_point%pelletList.__len__()].position.__div__(16))
            if direction is None:
                direction = STOP

        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False

    # --------------------------------------------------------
    def basemap(self):
        list = []
        f = open("maze1.txt", "r")

        row = NROWS
        while row > 0:
            a = f.readline()
            for x in a:
                if (x != " " and x != '\n'):
                    if (x != '.' and x != '+' and x != 'p' and x != '-' and x != '|' and x != 'n'):
                        list.append(False)
                    else:
                        list.append(True)
            row -= 1
        f.close()

        arr = np.array(list)
        arr = arr.reshape(NROWS, NCOLS)
        return arr.T

    def updatemap(self, ghosts):
        self.curmap = self.basemap.copy()
        for i in ghosts:
            x1 = math.floor(i.position.x / TILEWIDTH)
            x2 = math.ceil(i.position.x / TILEWIDTH)
            y1 = math.floor(i.position.y / TILEHEIGHT)
            y2 = math.ceil(i.position.y / TILEHEIGHT)
            self.curmap[x1][y1] = False
            self.curmap[x2][y1] = False
            self.curmap[x1][y2] = False
            self.curmap[x2][y2] = False

            self.curmap[(x1 - 1) % 28][y1] = False
            self.curmap[(x2 + 1) % 28][y1] = False
            self.curmap[(x1 - 1) % 28][y2] = False
            self.curmap[(x2 + 1) % 28][y2] = False

            self.curmap[x1][(y1 - 1) % 36] = False
            self.curmap[x2][(y1 - 1) % 36] = False
            self.curmap[x1][(y2 + 1) % 36] = False
            self.curmap[x2][(y2 + 1) % 36] = False
            # self.curmap[round(self.position.x/TILEWIDTH)][round(self.position.y/TILEHEIGHT)] = True

    def trace(self, celldetail, target):
        x = target.x
        y = target.y
        direction = None

        while celldetail[x][y].parent_x != x or celldetail[x][y].parent_y != y:
            self.path.append((x, y))
            if x > celldetail[x][y].parent_x:
                direction = RIGHT
            if x < celldetail[x][y].parent_x:
                direction = LEFT
            if y > celldetail[x][y].parent_y:
                direction = DOWN
            if y < celldetail[x][y].parent_y:
                direction = UP
            x = celldetail[x][y].parent_x
            y = celldetail[x][y].parent_y
        print(self.path)
        self.path = []
        # self.ghost.path[i] == self.path[i] re-calculate in i
        return direction

    def a_star(self, target):  # target is Vector2()
        curcell_x = round(self.position.x / TILEWIDTH)  # x (0, 28)
        curcell_y = round(self.position.y / TILEHEIGHT)  # y (0, 36)

        if curcell_x == target.x and curcell_y == target.y:
            self.target_set = False
            return

        closeList = np.random.choice([False], p=[1], size=NROWS * NCOLS)
        closeList = closeList.reshape(NCOLS, NROWS)

        list = []
        for i in range(NROWS * NCOLS):
            c = cell()
            list.append(c)

        arr = np.array(list)
        celldetail = arr.reshape(NCOLS, NROWS)

        celldetail[curcell_x][curcell_y].f = 0
        celldetail[curcell_x][curcell_y].g = 0
        celldetail[curcell_x][curcell_y].h = 0
        celldetail[curcell_x][curcell_y].parent_x = curcell_x
        celldetail[curcell_x][curcell_y].parent_y = curcell_y

        openList = []
        openList.append([0, curcell_x, curcell_y])

        while openList.__len__() != 0:
            openList.sort()
            p = openList[0]
            openList.pop(0)
            x = p[1]
            y = p[2]
            closeList[x, y] = True

            # Leftcell
            if (x - 1 >= 0):
                if (x - 1 == target.x and y == target.y):
                    celldetail[x - 1][y].parent_x = x
                    celldetail[x - 1][y].parent_y = y
                    return self.trace(celldetail, target)

                elif (closeList[x - 1][y] == False and self.curmap[x - 1][y] == True):
                    gnew = celldetail[x][y].g + 1
                    hnew = abs(x - 1 - target.x) + abs(y - target.y)
                    fnew = gnew + hnew
                    if (celldetail[x - 1][y].f > fnew):
                        openList.append([fnew, x - 1, y])
                        celldetail[x - 1][y].f = fnew
                        celldetail[x - 1][y].g = gnew
                        celldetail[x - 1][y].h = hnew
                        celldetail[x - 1][y].parent_x = x
                        celldetail[x - 1][y].parent_y = y

            # Rightcell
            if (x + 1 < NCOLS):
                if (x + 1 == target.x and y == target.y):
                    celldetail[x + 1][y].parent_x = x
                    celldetail[x + 1][y].parent_y = y
                    return self.trace(celldetail, target)

                elif (closeList[x + 1][y] == False and self.curmap[x + 1][y] == True):
                    gnew = celldetail[x][y].g + 1
                    hnew = abs(x + 1 - target.x) + abs(y - target.y)
                    fnew = gnew + hnew
                    if (celldetail[x + 1][y].f > fnew):
                        openList.append([fnew, x + 1, y])
                        celldetail[x + 1][y].f = fnew
                        celldetail[x + 1][y].g = gnew
                        celldetail[x + 1][y].h = hnew
                        celldetail[x + 1][y].parent_x = x
                        celldetail[x + 1][y].parent_y = y

            # Upcell
            if (y - 1 >= 0):
                if (x == target.x and y - 1 == target.y):
                    celldetail[x][y - 1].parent_x = x
                    celldetail[x][y - 1].parent_y = y
                    return self.trace(celldetail, target)

                elif (closeList[x][y - 1] == False and self.curmap[x][y - 1] == True):
                    gnew = celldetail[x][y].g + 1
                    hnew = abs(x - target.x) + abs(y - 1 - target.y)
                    fnew = gnew + hnew
                    if (celldetail[x][y - 1].f > fnew):
                        openList.append([fnew, x, y - 1])
                        celldetail[x][y - 1].f = fnew
                        celldetail[x][y - 1].g = gnew
                        celldetail[x][y - 1].h = hnew
                        celldetail[x][y - 1].parent_x = x
                        celldetail[x][y - 1].parent_y = y

            # Downcell
            if (y + 1 < NROWS):
                if (x == target.x and y + 1 == target.y):
                    celldetail[x][y + 1].parent_x = x
                    celldetail[x][y + 1].parent_y = y
                    return self.trace(celldetail, target)

                elif (closeList[x][y + 1] == False and self.curmap[x][y + 1] == True):
                    gnew = celldetail[x][y].g + 1
                    hnew = abs(x - target.x) + abs(y + 1 - target.y)
                    fnew = gnew + hnew
                    if (celldetail[x][y + 1].f > fnew):
                        openList.append([fnew, x, y + 1])
                        celldetail[x][y + 1].f = fnew
                        celldetail[x][y + 1].g = gnew
                        celldetail[x][y + 1].h = hnew
                        celldetail[x][y + 1].parent_x = x
                        celldetail[x][y + 1].parent_y = y


class cell:
    def __init__(self):
        self.parent_x = -1
        self.parent_y = -1
        self.f = np.inf
        self.g = np.inf
        self.h = np.inf
