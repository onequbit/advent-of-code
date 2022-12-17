#!/usr/bin/env python3
import json
from math import dist, sqrt
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

class RopeBridge:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tx = 0
        self.ty = 0
        self.px = 0
        self.py = 0
        self.state = RopeState.STILL
        self.prev_state = RopeState.STILL
        self.visited = set()

    def __repr__(self):
        return str({
            'x':self.x,
            'y':self.y,
            'tx':self.tx,
            'ty':self.ty,
            'px':self.px,
            'py':self.py,
            'state':self.state,
            'visited':self.visited
        })

    def get_tail_distance(self):
        return dist((self.x,self.y),(self.tx,self.ty))

    def move_tail(self): #, direction:RopeState):
        self.tx, self.ty = self.px, self.py 
        self.visited.add( (self.tx, self.ty) )

    def update_tail(self):
        self.visited.add( (self.tx, self.ty) )
        tail_distance = self.get_tail_distance()
        if tail_distance > sqrt(2):
            self.move_tail() # self.tail_state)

    def go_up(self, steps:int, tail=False):
        if steps == 0:
            return
        self.state = RopeState.UP 
        self.y -= 1
    
    def go_down(self, steps:int, tail=False):
        if steps == 0:
            return
        self.state = RopeState.DOWN
        self.y += 1

    def go_left(self, steps:int, tail=False):
        if steps == 0:
            return
        self.state = RopeState.LEFT
        self.x -= 1
    
    def go_right(self, steps:int, tail=False):
        if steps == 0:
            return
        self.state = RopeState.RIGHT
        self.x += 1

    def move(self, instruction:str):
        self.before = self.state
        direction, steps = instruction.split()
        steps = int(steps)
        self.tail_state = self.state
        NEXT_MOVEMENT = {   'U':self.go_up, 'D':self.go_down, 
                            'L':self.go_left, 'R':self.go_right }
        for step in range(steps):
            self.prev_state = self.state
            self.px, self.py = self.x, self.y
            NEXT_MOVEMENT[direction](steps=1)
            self.update_tail()

def get_input(input_file):
    lines = []
    with open(input_file, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    return lines

def day9a(input_file):
    rope = RopeBridge()
    for motion in get_input(input_file):
        rope.move(motion)
        # print(rope)

    return len(set(rope.visited))


def day9b(input_file):


    return


if __name__ == "__main__":
    
    input_file = 'input.txt'
    # input_file = 'example.txt'
    print(day9a(input_file)) # <-- 6563  :)
    print(day9b(input_file))
