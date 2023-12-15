#!/usr/bin/env python3

import sys
from os.path import abspath, dirname
sys.path.append(dirname(abspath("../..")))
from advent_of_code import load_input_lines
from re import finditer
from math import prod

SYMBOLS = "#$%&*+-/=@"

def create_mapping(lines):
    symbol_mapping = {}    
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char in SYMBOLS:
                symbol_mapping[(row,col)] = []
    return symbol_mapping

def get_symbol_span(row, found_symbol):
    symbol_span = set()
    for row in range(row-1,row+2):
        for col in range(found_symbol.start()-1, found_symbol.end()+1):
            symbol_span.add((row,col))
    return symbol_span


if __name__ == "__main__":
    lines = load_input_lines(sys.argv[1])
    mapping = create_mapping(lines)
    for row, line in enumerate(lines):
        for found in finditer(r"\d+", line):
            symbol_span = get_symbol_span(row, found)
            for coordinates in symbol_span & mapping.keys():
                mapping[coordinates].append(int(found.group()))
    result_1 = 0
    result_2 = 0
    for found in mapping.values():
        result_1 += sum(found)
        if len(found) == 2:
            result_2 += prod(found)
    print(result_1)
    print(result_2)

"""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..


467..~~~..   467
...*......   
..35..633.   35 + 633
......#...
617*......   617
.....+.~~.
..592.....   592
......755.   755
...$.*....
.664.598..   644 + 598

            ...4341
            
530540: too high
519123: too low

"""