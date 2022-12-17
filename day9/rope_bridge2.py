#!/usr/bin/env python3
import json
from math import dist
from enum import Enum

direction = { 'U':'up', 'D':'down', 'L':'left', 'R':'right' }

class RopeState(Enum):
    # 0 1 2
    # 3 4 5
    # 6 7 8
    NW = 0
    UP = 1
    NE = 2
    LEFT = 3
    STILL = 4
    RIGHT = 5
    SW = 6
    DOWN = 7
    SE = 8

DELTAXY = [ (-1,-1), (0,-1), (1,-1), (-1,0), (0,0), (1,0), (-1,1), (0,1), (1,1) ]
STATES = [ 'Q', 'U', 'E', 'L', '_', 'R', 'Z', 'D', 'C' ]
# Q U E
# L _ R
# Z D C

DIRECTION_TO_STATE = {  'U':RopeState.UP,
                        'D':RopeState.DOWN,
                        'L':RopeState.LEFT,
                        'R':RopeState.RIGHT }

class RopeBridge:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tx = 0
        self.ty = 0
        self.state = RopeState.STILL
        self.visited = []

    def __repr__(self):
        return str({
            'x':self.x,
            'y':self.y,
            'tx':self.tx,
            'ty':self.ty,
            'state':self.state,
            'visited':self.visited
        })

    def get_tail_distance(self):
        return dist((self.x,self.y),(self.tx,self.ty))

    def move_tail(self, direction:RopeState):
        NEXT_MOVEMENT = {   'UP':self.go_up, 'DOWN':self.go_down, 
                            'LEFT':self.go_left, 'RIGHT':self.go_right }
        NEXT_MOVEMENT[direction.name](steps=1,tail=True)

    def update(self):
        self.visited.append( (self.tx, self.ty) )
        tail_distance = self.get_tail_distance()
        if tail_distance > 1:
            self.move_tail(self.state)
        # print("tail_distance:", self.get_tail_distance())

    def go_up(self, steps:int, tail=False):
        if tail:
            self.ty -= 1
            return
        if steps == 0:
            return
        print("going up")
        self.update()
        self.state = RopeState.UP 
        self.y -= 1
        self.go_up(steps-1)
    
    def go_down(self, steps:int, tail=False):
        if tail:
            self.ty += 1
            return
        if steps == 0:
            return
        print("going down")
        self.update()
        self.state = RopeState.DOWN
        self.y += 1
        self.go_down(steps-1)

    def go_left(self, steps:int, tail=False):
        if tail:
            self.tx -= 1
            return
        if steps == 0:
            return
        print("going left")
        self.update()
        self.state = RopeState.LEFT
        self.x -= 1
        self.go_left(steps-1)
    
    def go_right(self, steps:int, tail=False):
        if tail:
            self.tx += 1
            return
        if steps == 0:
            return
        print("going right")
        self.update()
        self.state = RopeState.DOWN
        self.x += 1
        self.go_right(steps-1)

    def move(self, instruction:str):
        self.before = self.state
        direction, steps = instruction.split()
        steps = int(steps)
        NEXT_MOVEMENT = {   'U':self.go_up, 'D':self.go_down, 
                            'L':self.go_left, 'R':self.go_right }
        NEXT_MOVEMENT[direction](steps)

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
    
    while len(motion_list) > 0:
        head = motion_list[:2]
        motion_list = motion_list[2:]
        if head in diagonals.keys():
            codes += diagonals[head]
        else:
            codes += head
    return codes

def day9a(input_file):
    rope = RopeBridge()
    for motion in get_input(input_file):
        rope.move(motion)
        print(rope)

    print(len(set(rope.visited)))
    print(RopeState.UP.name)
    return ''

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