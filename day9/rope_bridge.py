#!/usr/bin/env python3
import json
from math import dist
from enum import Enum

# class syntax
class TailState(Enum):
    # 0 1 2
    # 3 4 5
    # 6 7 8
    NW = 0
    NORTH = 1
    NE = 2
    WEST = 3
    STILL = 4
    EAST = 5
    SW = 6
    SOUTH = 7
    SE = 8

DELTAXY = [ (-1,-1), (0,-1), (1,-1), (-1,0), (0,0), (1,0), (-1,1), (0,1), (1,1) ]
STATES = [ 'Q', 'U', 'E', 'L', '_', 'R', 'Z', 'D', 'C' ]
# Q U E
# L _ R
# Z D C

STATES_TO_DELTA = {}
for k,v in zip(STATES, DELTAXY):
    STATES_TO_DELTA[k] = v

STATES_TO_DELTA['LU'] = STATES_TO_DELTA['UL'] = STATES_TO_DELTA['Q']
STATES_TO_DELTA['LD'] = STATES_TO_DELTA['DL'] = STATES_TO_DELTA['Z']
STATES_TO_DELTA['RU'] = STATES_TO_DELTA['UR'] = STATES_TO_DELTA['E']
STATES_TO_DELTA['RD'] = STATES_TO_DELTA['DR'] = STATES_TO_DELTA['C']

for item in STATES_TO_DELTA.items():
    print(item)

class RopeTail:
    def __init__(self):
        self.state = TailState.STILL
        self.before = TailState.STILL
        self.x = 0
        self.y = 0
        self.visited = set( (self.x, self.y) )
        self.update_visited()

    def __repr__(self):
        return str({ 'state':self.state, 'x':self.x, 'y':self.y, 'visited':self.visited })

    def facing(self, direction:TailState):
        return self.state == direction

    def diagonal(self):
        return self.state in [TailState.NW, TailState.SW, TailState.NE, TailState.SE]

    def update_visited(self):
        self.visited.add( (self.x, self.y) )

    def not_direction(self, direction:TailState):
        return [e for e in TailState if e != direction]
"""
    def go_west(self, steps):
        if steps == 0:
            return
        self.before = self.state
        if self.before == TailState.STILL:
            self.state = TailState.WEST
            self.go_west(steps - 1)
            return
        if self.before == TailState.WEST:
            self.state = TailState.WEST
            self.x -= 1
            self.update_visited()
            self.go_west(steps - 1)
            return

        if self.before == TailState.EAST:
            self.state = TailState.STILL
            self.go_west(steps - 1)
            return
        if self.before == TailState.NORTH:
            self.state == 

        if steps == 0:
            return
        if self.state in self.not_direction(TailState.WEST):
            self.state = TailState.WEST
        else:
            self.x -= 1
            if self.before == TailState.NORTH:
                self.y -= 1
            if self.before == TailState.SOUTH:
                self.y += 1
            self.update_visited()
        self.go_west(steps-1)
    
    def go_east(self, steps):
        self.before = self.state
        if steps == 0:
            return
        if self.state in self.not_direction(TailState.EAST):
            self.state = TailState.EAST
        else:
            self.x += 1
            if self.before == TailState.NORTH:
                self.y -= 1
            if self.before == TailState.SOUTH:
                self.y += 1
            self.update_visited()
        self.go_east(steps-1)

    def go_north(self, steps):
        if steps == 0:
            return
        if self.state in self.not_direction(TailState.NORTH):
            self.state = TailState.NORTH
        else:
            self.y -= 1
            self.update_visited()
        self.go_north(steps-1)
    
    def go_south(self, steps):
        if steps == 0:
            return
        if self.state in self.not_direction(TailState.SOUTH):
            self.state = TailState.SOUTH
        else:
            self.y += 1
            self.update_visited()
        self.go_south(steps-1)
"""

def get_input(input_file):
    lines = []
    with open(input_file, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    return lines

direction = { 'U':'up', 'D':'down', 'L':'left', 'R':'right' }

def get_tail_motion(motion_steps):
    instructions = ''
    for step in motion_steps:
        [d_code, count] = step.split(' ') 
        count = int(count)
        new_step = d_code * count
        instructions += new_step
    return instructions

@staticmethod
def update_tail(tail:RopeTail, motion):
    d_code, steps = motion.split()
    steps = int(steps) - 1

    if d_code == 'L':
        tail.go_west(steps)
    if d_code == 'R':
        tail.go_east(steps)
    if d_code == 'U':
        tail.go_north(steps)
    if d_code == 'D':
        tail.go_south(steps)
    return tail

# def day9a(input_file):
#     visited = set()
#     motions = get_input(input_file)
#     headX, headY = 0,0
#     tailX, tailY = 0,0
#     allsteps = 0
#     for m in motions:
#         d, steps = m.split()
#         steps = int(steps)
#         allsteps += steps
#         for s in range(steps):            
#             headX -= 1 if d == 'L' else 0
#             headX += 1 if d == 'R' else 0
#             headY += 1 if d == 'U' else 0
#             headY -= 1 if d == 'D' else 0
#             distance = int(dist([headX,headY],[tailX, tailY]))
#             oldX, oldY = tailX, tailY
#             if distance > 1:
#                 visited.add( (tailX, tailY) )
#                 tailX -= 1 if d == 'L' else 0
#                 tailX += 1 if d == 'R' else 0
#                 tailY += 1 if d == 'U' else 0
#                 tailY -= 1 if d == 'D' else 0
#             # visited.add( (tailX, tailY) )
#             # oldX, oldY = tailX, tailY
#             # visited.add( (oldX, oldY) )
#             # if distance > 1:
#             #     if d == 'L':
#             #         tailX -= (steps-1)
#             #         for x in range(oldX, tailX-1, -1):
#             #             visited.add( (x, tailY) )
#             #     if d == 'R':
#             #         tailX += (steps-1)
#             #         for x in range(oldX, tailX+1):
#             #             visited.add( (x, tailY) )
#             #     if d == 'U':
#             #         tailY += (steps-1)
#             #         for y in range(oldY, tailY-1, -1):
#             #             visited.add( (tailX, y) )
#             #     if d == 'D':
#             #         tailY -= (steps-1)
#             #         for y in range(oldY, tailY+1):
#             #             visited.add( (tailX, y) )
#             # visited.add( (tailX, tailY) )
#         print(f"{direction[d]} {steps}, O:{(oldX,oldY)}, T:{(tailX,tailY)}, visited: {visited}")
#     print(allsteps)
#     # print(visited)
#     print(len(visited))
#     print(allsteps - len(visited))
#     return allsteps - len(visited)

def get_delta(previous:str, current:str):
    code = previous + current
    delta = STATES_TO_DELTA[code]
    return delta
    #     if current == previous:
    #     if current == 'U':
    #         return (0,-1)
    #     if current == 'D':
    #         return (0,1)
    #     if current == 'L':
    #         return (-1,0)
    #     if current == 'R':
    #         return (1,0)
    # # else:

def get_codes(motion_list:str):
    # print("get_codes:", motion_list)
    codes = []
    # Q U E
    # L _ R
    # Z D C
    diagonals = {   'LU':'Q', 'UL':'Q',
                    'RU':'E', 'UR':'E',
                    'LD':'Z', 'DL':'Z',
                    'RD':'C', 'DR':'C',
                    'RR':'R', 'LL':'L',
                    'UU':'U', 'DD':'D' }
    if len(motion_list) < 2:
        return [motion_list]
    head = motion_list[:2]
    remainder = motion_list[2:]
    # print("get_codes:", head, remainder)
    if head in diagonals.keys():
        codes += [diagonals[head]]
    else:
        codes += head
    return codes + get_codes(remainder)

def day9a(input_file):
    head_motions = get_input(input_file)
    tail_motion = get_tail_motion(head_motions)
    # print(tail_motion)
    tail = RopeTail()
    codes = get_codes(tail_motion)
    print("codes:", codes)
    print(len(codes))
    return tail.visited

def day9b(input_file):


    return


if __name__ == "__main__":
    
    input_file = 'input.txt'
    # input_file = 'example.txt'
    print(day9a(input_file)) # 399
    print(day9b(input_file))
    
    """
    wrong answers:
    7347 (too high)
    399 (too low)
    """
    


"""
R 4  RRRR
U 4  UUUU
L 3  LLL
D 1  D
R 4  R
D 1  D
L 5  LLLLL
R 2  RR
RRRRUUUULLLDRDLLLLLRR  ... 21
QUE
L_R
ZDC
RRR RU UU UL L LD RD LLLL LR R
3    1  2  1 0 1  1    4  1  0 = 14

RDL = D = 1
RUL = U = 1

LDR = D = 1
LUR = U = 1

URD = R = 1
ULD = L = 1

DRU = R = 1
DLU = L = 1




_,RR,RR,RR,RR,UU,UU,UU,UU,LL,LL,LL,DD,RR,RR,RR,RR,DD,LL,LL,LL,LL,LL,RR,R
 ,RR,RR,RR,RR,UU,UU,UU,UU,LL,LL,LL,DD,RR,RR,RR,RR,DD,LL,LL,LL,LL,LL,RR,

"""