#!/usr/bin/env python
from os.path import abspath, dirname, join
INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

def get_strategy():
    strategy = None
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        lines = input_file.readlines()
    strategy = []
    for line in lines:
        (them, you) = line.strip().split(' ')
        strategy.append(dict(them=them, you=you))
    return strategy

# A, X ==> rock
# B, Y ==> paper
# C, Z ==> scissors

# paper beats rock      B,X or Y,A
# rock beats scissors   A,Z or X,C
# scissors beats paper  C,Y or Z,B

# WIN: A,Y or C,X or B,Z --> 6pts
# LOSE: B,X or C,Y, or A,Z --> 0pts
# DRAW: A,X or B,Y or C,Z --> 3pts

SCORING = {
    'AY' : 6 + 2,
    'CX' : 6 + 1,
    'BZ' : 6 + 3,
    'AX' : 3 + 1,
    'BY' : 3 + 2,
    'CZ' : 3 + 3,
    'AZ' : 0 + 3,
    'BX' : 0 + 1,
    'CY' : 0 + 2
}

# X --> lose
# Y --> draw
# Z --> win

# (to lose): AX --> Z, BX --> X, CX --> Y
# (to draw): AY --> X, BY --> Y, CY --> Z
# (to win): AZ --> Y, BZ --> Z, CZ --> X

REAL_STRATEGY = {
    'AX' : 'Z',
    'AY' : 'X',
    'AZ' : 'Y',
    'BX' : 'X',
    'BY' : 'Y',
    'BZ' : 'Z',
    'CX' : 'Y',
    'CY' : 'Z',
    'CZ' : 'X'
}

def get_score(round:dict):
    key = round['them'] + round['you']
    return SCORING[key]

def get_choice(round:dict):
    key = round['them'] + round['you']
    return REAL_STRATEGY[key]

def run_game_1():
    strategy = get_strategy()
    points = []
    for round in strategy:
        points.append(get_score(round))
    return points

def run_game_2():
    strategy = get_strategy()
    points = []
    for round in strategy:
        choice = get_choice(round)
        planned_round = round
        planned_round['you'] = choice
        points.append(get_score(planned_round))
    return points


if __name__ == '__main__':
    part1 = run_game_1()
    part2 = run_game_2()
    print(f"part 1: {sum(part1)}")
    print(f"part 2: {sum(part2)}")
