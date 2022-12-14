#!/usr/bin/env python3

from math import dist
from enum import Enum

# class syntax
class TailState(Enum):
    STILL = 0
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    NW = 5
    NE = 6
    SW = 7
    SE = 8

class RopeTail:
    def __init__(self):
        self.state = TailState.STILL
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

    def go_west(self, steps):
        if steps == 0:
            return
        if self.state in self.not_direction(TailState.WEST):
            self.state = TailState.WEST
        else:
            self.x -= 1
            self.update_visited()
        self.go_west(steps-1)
    
    def go_east(self, steps):
        if steps == 0:
            return
        if self.state in self.not_direction(TailState.EAST):
            self.state = TailState.EAST
        else:
            self.x += 1
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
        [d_code, count] = step.split() 
        count = int(count)
        new_step = d_code * count
        instructions += new_step
    return instructions

def sign(num):
    return 1 if num >= 0 else -1

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


def day9a(input_file):
    visited = set()
    motions = get_input(input_file)
    # print(*motions, sep='\n')
    tail = RopeTail()
    for motion in motions:
        print(motion)
        tail = update_tail(tail, motion)
        print(tail)
    print(len(tail.visited))
    return tail.visited

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
    """
    