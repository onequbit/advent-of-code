#!/usr/bin/env python3


"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

Your puzzle answer was 4580.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?

"""

from icecream import ic
from enum import Enum


class Facing(Enum):
    WEST = 0, "West"
    NORTH = 1, "North"
    EAST = 2, "East"
    SOUTH = 3, "South"

SYMBOLS = "<^>v"

COMPASS = {
    "<": Facing.WEST,
    "^": Facing.NORTH,
    ">": Facing.EAST,
    "v": Facing.SOUTH
}

DIRECTION = {
    chr(ord("<")): (-1, 0),
    chr(ord("^")): (0, -1),
    chr(ord(">")): (1, 0),
    chr(ord("v")): (0, 1)
}



def load_data(filename):
    guard_map = [[char for char in line.strip()] for line in open(filename, "r", encoding="utf-8").readlines()]
    return guard_map


def get_position(guard_map):
    x, y = -1, -1
    for index, line in enumerate(guard_map):
        for char in SYMBOLS:
            if char in line: 
                y = index
                x = line.index(char)
                return x, y


def get_facing(guard_map, x=None, y=None):
    if not x or not y:
        x, y = get_position(guard_map)
    assert guard_map[y][x] in f"{SYMBOLS}", "invalid coordinates"
    char = guard_map[y][x]
    # ic("get_facing", char)
    return COMPASS[char]


def is_valid_position(guard_map, next_x, next_y):
    up_down_valid = next_y >= 0 and next_y < len(guard_map)
    left_right_valid = next_x >= 0 and next_x < len(guard_map[0])
    # ic(next_x, next_y, up_down_valid, left_right_valid)
    return up_down_valid and left_right_valid


def turn(guard_map, x, y):
    facing = guard_map[y][x]
    # ic("turn", facing)
    next_face = (SYMBOLS.index(str(facing))+1) % len(SYMBOLS)
    return SYMBOLS[next_face]


def next_obstacle(guard_map, x=None, y=None):
    if not x or not y:
        x, y = get_position(guard_map)
    facing = guard_map[y][x]
    # ic("next_obstacle", facing)
    steps = 0
    # ic(x, y, guard_map[y][x], facing, DIRECTION)
    delta_x, delta_y = DIRECTION[facing]
    next_x = x + (delta_x * steps)
    next_y = y + (delta_y * steps)
    valid_position = is_valid_position(guard_map, next_x, next_y)
    guard_map[y][x] = "X"
    while valid_position:
        if guard_map[next_y][next_x] == "#":
            next_x = delta_x * (steps-1)
            next_y = delta_y * (steps-1)
            guard_map[y + next_y][x + next_x] = facing
            break
        guard_map[next_y][next_x] = "X"
        steps += 1
        next_x = x + (delta_x * steps)
        next_y = y + (delta_y * steps)
        # ic(steps, next_x, next_y)
        valid_position = is_valid_position(guard_map, next_x, next_y)
    return next_x, next_y
    

def part_one(input_file):
    guard_map = load_data(input_file)
    print(*guard_map, sep="\n")
    x, y = get_position(guard_map)
    while True:
        _x, _y = next_obstacle(guard_map, x, y)
        x += _x
        y += _y
        if not is_valid_position(guard_map, x, y):
            break
        # ic(x, y, guard_map[y][x])
        guard_map[y][x] = turn(guard_map, x, y)    
    print("=" * len(guard_map[0]) * 5)
    print(*guard_map, sep="\n")
    count = 0
    for line in guard_map:
        for position in line:
            if position == "X":
                count += 1
    return count

if __name__ == "__main__":
    # input_file = "day6_sample.txt"
    input_file = "day6_input.txt"

    part_one_answer = part_one(input_file)
    ic("part_one:", part_one_answer)
    if "sample" in input_file:
        assert part_one_answer == 41, f"{part_one_answer=}"
    if "input" in input_file:
        assert part_one_answer == 4580, f"{part_one_answer=}"

