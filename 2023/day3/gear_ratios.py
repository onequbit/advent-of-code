#!/usr/bin/env python3

import sys
from advent_lib import load_input_lines

DOT = "."
SYMBOLS = "-@*/&#%+="

def is_symbol(char):
    return char in SYMBOLS

def symbol_adjacent(charmap, row, col):
    lastrow = len(charmap)-1
    lastcol = len(charmap[0])-1
    in_top = row > 0
    in_bottom = row < lastrow
    in_left = col > 0
    in_right = col < lastcol
    N = in_top and is_symbol(charmap[row-1][col])
    S = in_bottom and is_symbol(charmap[row+1][col])
    W = in_left and is_symbol(charmap[row][col-1])
    E = in_right and is_symbol(charmap[row][col+1])
    NW = in_top and in_left and is_symbol(charmap[row-1][col-1])
    SW = in_bottom and in_left and is_symbol(charmap[row+1][col-1])
    NE = in_top and in_right and is_symbol(charmap[row-1][col+1])
    SE = in_bottom and in_right and is_symbol(charmap[row+1][col+1])
    symbol_is_adjacent = any([N,S,W,E,NW,SW,NE,SE])
    debug_str = f"{row}:{col} '{charmap[row][col]}' --> {[N,S,W,E,NW,SW,NE,SE]}: {symbol_is_adjacent})"
    print(debug_str)
    return symbol_is_adjacent

if __name__ == "__main__":
    lines = load_input_lines(sys.argv[1])
    char_map = [[char.replace('.',' ') for char in line] for line in lines]
    print(*char_map, sep='\n')
    
    prox_map = [[False] * len(lines[0])] * len(lines)
    for row, line in enumerate(char_map):
        for col, char in enumerate(line):
            if char.isdigit():
                prox_map[row][col] = symbol_adjacent(char_map, row, col)
    
    print(*prox_map, sep='\n')