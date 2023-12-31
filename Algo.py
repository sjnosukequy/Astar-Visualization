import math
import pygame
import time
import random, numpy

class PioQueue:
    def __init__(self):
        '''
        Pos, G, H, F
        '''
        self.list = []
    
    def push(self, obj):
        '''
        Pos, G, H, F
        '''
        if not self.list:
            self.list.append(obj)
        else:
            minf = self.list[0][3]
            idx = 0
            for i in self.list:
                if obj[3] <= minf:
                    break
                idx += 1
            self.list.insert(idx, obj)

    def pop(self):
        return self.list.pop(0)
    
    def copy(self):
        return self

# Checking = [(1, 0, 10), (-1, 0, 10), (0, 1, 10), (0, -1, 10), (1, 1, 14), (-1, 1, 14), (1, -1, 14), (-1, -1, 14)]
Checking = [(1, 0, 10), (-1, 0, 10), (0, 1, 10), (0, -1, 10)]

open_list_copy = []
close_list_copy = []

def ASearch(game, start, end, result, time_res, idx):

    #Clearing
    open_list = PioQueue()
    close_list = []
    open_list_copy.clear()
    close_list_copy.clear()
    Found = False

    #timing
    timer = time.perf_counter()

    #PATH
    path = []

    #Adding the first node
    intial_h = int(math.sqrt(math.pow((end[0] - start[0]) * 16, 2) + math.pow((end[1] - start[1]) * 16, 2)))
                     #Pos ,G  ,H         ,F
    open_list.push( [ start, 0, intial_h, 0 ] )

    #while loop
    while len(open_list.list) > 0 and not Found:
        q = open_list.pop()
        Coll = game.Around(q[0])

        for dir in Checking:
            if dir in Coll:
                continue
            successor_pos = [q[0][0] + dir[0], q[0][1] + dir[1]]
            if successor_pos[0] < -1 or successor_pos[0] > 80:
                break
            if successor_pos[1] < 0 or successor_pos[1] > 45:
                break
            if successor_pos == end:
                Found = True
                break
            else:
                h = int( math.sqrt(math.pow((end[0] - successor_pos[0]) * 16, 2) + math.pow((end[1] - successor_pos[1])* 16, 2)) )
                g = q[1] + dir[2]
                f = int(g + h)

                Exact = False
                for i in open_list.list:
                    if successor_pos == i[0]:
                            if i[3] > f:
                                i[3] = f
                                i[4] = q[0]
                            Exact = True
                            break

                for i in close_list:
                    if successor_pos == i[0]:
                        Exact = True
                        break

                if not Exact:
                    open_list.push( [successor_pos, g, h, f, q[0]] )
                    open_list_copy.append( (successor_pos, g, h, f, q[0]) )

        close_list.append(q)
        close_list_copy.append(q)

    if Found:
        if len(close_list) <= 1:
            pass
        else:
            # path.append(end)
            N = len(close_list) - 1
            pior = close_list[N][4]
            path.append(close_list[N][0])
            while pior != start:
                path.append(pior)
                while close_list[N][0] != pior:
                    N -= 1
                pior = close_list[N][4]
    
    timer -= time.perf_counter()
    result[idx] = path
    time_res.append(timer)
    return
    # return path, timer

def Draw_open(surf):
    box = pygame.Surface((16,16))
    box.fill('blue')
    for i in open_list_copy:
        surf.blit(box, (i[0][0] * 16, i[0][1] * 16))

def Draw_close(surf):
    box = pygame.Surface((16,16))
    box.fill('orange')
    for i in close_list_copy:
        surf.blit(box, (i[0][0] * 16, i[0][1] * 16))

def Clear_visual():
    close_list_copy.clear()
    open_list_copy.clear()

def Maze(width, height, Block_size):
    w_block, h_block = width // Block_size, height // Block_size
    cells = numpy.zeros((w_block, h_block))
    stack = []
    wall = []

    ini_pos = [0, 0]
    stack.append(ini_pos)
    cells[0,0] = 1

    while stack:
        obj = stack[-1]
        stack.remove(obj)

        x = obj[0]
        y= obj[1]

        Neighbours = []
        for dir in Checking:
            if x >= 0 and x < w_block - 1:
                if y >= 0 and y < h_block - 1:
                    if cells[x + dir[0], y + dir[1]] == 0:
                        Neighbours.append(dir)
        # print(Neighbours)
        
        if Neighbours:
            stack.append(obj)
            choice = random.choice(Neighbours)
            cells[x + choice[0], y + choice[1]] = 1
            stack.append( [x + choice[0], y + choice[1]] )

            for dir in Neighbours:
                if dir[0] != choice[0] and dir[1] != choice[1]:
                    cells[x + dir[0], y + dir[1]] = -1
    
    ##BULDING WALL
    for i in range(w_block):
        for k in range(h_block):
            if cells[i][k] == -1 or cells[i][k] == 0:
                wall.append([i, k])

    return wall

def extract(game, wall):
    for i in wall:
        loco = str(i[0]) + ',' + str(i[1])
        game.Block[loco] = {'type' : 'Wall' , 'Color' : 'black', 'Pos' : (i[0], i[1])}











        
