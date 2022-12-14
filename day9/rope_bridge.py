#!/usr/bin/env python3

from math import dist

def get_input(input_file):
    lines = []
    with open(input_file, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    return lines

direction = { 'U':'up', 'D':'down', 'L':'left', 'R':'right' }

def sign(num):
    return 1 if num >= 0 else -1

def day9a(input_file):
    visited = set()
    motions = get_input(input_file)
    headX, headY = 0,0
    tailX, tailY = 0,0
    allsteps = 0
    for m in motions:
        d, steps = m.split()
        steps = int(steps)
        allsteps += steps
        for s in range(steps):            
            headX -= 1 if d == 'L' else 0
            headX += 1 if d == 'R' else 0
            headY += 1 if d == 'U' else 0
            headY -= 1 if d == 'D' else 0
            distance = int(dist([headX,headY],[tailX, tailY]))
            oldX, oldY = tailX, tailY
            if distance > 1:
                visited.add( (tailX, tailY) )
                tailX -= 1 if d == 'L' else 0
                tailX += 1 if d == 'R' else 0
                tailY += 1 if d == 'U' else 0
                tailY -= 1 if d == 'D' else 0
            # visited.add( (tailX, tailY) )
            # oldX, oldY = tailX, tailY
            # visited.add( (oldX, oldY) )
            # if distance > 1:
            #     if d == 'L':
            #         tailX -= (steps-1)
            #         for x in range(oldX, tailX-1, -1):
            #             visited.add( (x, tailY) )
            #     if d == 'R':
            #         tailX += (steps-1)
            #         for x in range(oldX, tailX+1):
            #             visited.add( (x, tailY) )
            #     if d == 'U':
            #         tailY += (steps-1)
            #         for y in range(oldY, tailY-1, -1):
            #             visited.add( (tailX, y) )
            #     if d == 'D':
            #         tailY -= (steps-1)
            #         for y in range(oldY, tailY+1):
            #             visited.add( (tailX, y) )
            # visited.add( (tailX, tailY) )
        print(f"{direction[d]} {steps}, O:{(oldX,oldY)}, T:{(tailX,tailY)}, visited: {visited}")
    print(allsteps)
    # print(visited)
    print(len(visited))
    print(allsteps - len(visited))
    return allsteps - len(visited)


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
    