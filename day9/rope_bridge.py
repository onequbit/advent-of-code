#!/usr/bin/env python3
import json
from math import dist
from enum import Enum

direction = { 'U':'up', 'D':'down', 'L':'left', 'R':'right' }

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

DIRECTION_TO_STATE = {  'U':TailState.NORTH,
                        'D':TailState.SOUTH,
                        'L':TailState.WEST,
                        'R':TailState.EAST }

# STATES_TO_DELTA = {}
# for k,v in zip(STATES, DELTAXY):
#     STATES_TO_DELTA[k] = v

# STATES_TO_DELTA['LU'] = STATES_TO_DELTA['UL'] = STATES_TO_DELTA['Q']
# STATES_TO_DELTA['LD'] = STATES_TO_DELTA['DL'] = STATES_TO_DELTA['Z']
# STATES_TO_DELTA['RU'] = STATES_TO_DELTA['UR'] = STATES_TO_DELTA['E']
# STATES_TO_DELTA['RD'] = STATES_TO_DELTA['DR'] = STATES_TO_DELTA['C']

# for item in STATES_TO_DELTA.items():
#     print(item)

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

    def update(self, x, y):
        print( (x,y) )
        self.x += x
        self.y += y
        self.update_visited()

    @staticmethod
    def dir_other_than(direction:TailState):
        return [e for e in TailState if e != direction]

    def go_north(self):
        print('going up')
        if self.before in RopeTail.dir_other_than(TailState.NORTH):
            if self.before == TailState.WEST:
                self.state = TailState.NW
                self.update(0,-1)    
            elif self.before == TailState.EAST:
                self.state = TailState.NE
                self.update(0,-1)
            elif self.before == TailState.SOUTH:
                self.state = TailState.STILL
            elif self.before in [TailState.NW, TailState.NE]:
                self.state = TailState.NORTH
                self.update(0,-1)
        else:
            self.update(0,-1)
        return

    def go_south(self):
        print('going down')
        if self.before in RopeTail.dir_other_than(TailState.SOUTH):
            if self.before == TailState.WEST:
                self.state = TailState.SW
                self.update(0,1)
            elif self.before == TailState.EAST:
                self.state = TailState.SE
                self.update(0,1)
            elif self.before == TailState.NORTH:
                self.state = TailState.STILL
        else:
            self.update(0,1)
        return

    def go_west(self):
        print('going left')
        if self.before in RopeTail.dir_other_than(TailState.WEST):
            if self.before == TailState.NORTH:
                self.state = TailState.NW
                self.update(-1,0)
            elif self.before == TailState.SOUTH:
                self.state = TailState.SW
                self.update(-1,0)
            elif self.before == TailState.EAST:
                self.state = TailState.STILL
        else:
            self.update(-1,0)
        return

    def go_east(self):
        print('going right')
        if self.before in RopeTail.dir_other_than(TailState.EAST):
            if self.before == TailState.NORTH:
                self.state = TailState.NE
                self.update(1,0)
            elif self.before == TailState.SOUTH:
                self.state = TailState.SE
                self.update(1,0)
            elif self.before == TailState.WEST:
                self.state = TailState.STILL
        else:
            self.update(1,0)
        return

    def move(self, direction:str):
        self.before = self.state
        if self.before == TailState.STILL:
            self.state = DIRECTION_TO_STATE[direction]
            return
        next_movement = {   'U':self.go_north, 'D':self.go_south, 
                            'L':self.go_west, 'R':self.go_east }
        next_movement[direction]()

def get_input(input_file):
    lines = []
    with open(input_file, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    return lines


def get_tail_motion(motion_steps):
    instructions = ''
    for step in motion_steps:
        [d_code, count] = step.split(' ') 
        count = int(count)
        new_step = d_code * count
        instructions += new_step
    return instructions

def get_codes(motion_list:str):
    codes = 's'
    # Q U E
    # L _ R
    # Z D C
    
    diagonals = {   'LU':'Q', 'UL':'Q',
                    'RU':'E', 'UR':'E',
                    'LD':'Z', 'DL':'Z',
                    'RD':'C', 'DR':'C',
                    'RR':'R', 'LL':'L',
                    'UU':'U', 'DD':'D',
                    '_':'' }
    # if len(motion_list) % 2 != 0:
    #     motion_list = '_' + motion_list
    
    while len(motion_list) > 0:
        head = motion_list[:2]
        motion_list = motion_list[2:]
        if head in diagonals.keys():
            codes += diagonals[head]
        else:
            codes += head
    return codes

def day9a(input_file):
    head_motions = get_input(input_file)
    tail_motion = get_tail_motion(head_motions)
    tail = RopeTail()
    print(tail_motion)
    for direction in tail_motion:
        tail.move(direction)
    # codes = get_codes(tail_motion)
    # print("codes:", codes)
    print(len(tail.visited))
    return len(tail.visited)
    

def day9b(input_file):


    return


if __name__ == "__main__":
    
    # input_file = 'input.txt'
    input_file = 'example.txt'
    print(day9a(input_file)) # 399
    print(day9b(input_file))
    
    """
    wrong answers:
    7347 (too high)
    399 (too low)
    6181 (too low)
    * somewhere between 6181 and 7347 *
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