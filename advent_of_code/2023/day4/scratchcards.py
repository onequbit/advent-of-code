#!/usr/bin/env python3

import sys
from os.path import abspath, dirname
sys.path.append(dirname(abspath("../..")))
from advent_of_code import load_input_lines
from advent_of_code import number_str_to_set

def count_points(matches:set):
    count = len(matches)
    if count == 0:
        return 0
    return int(2**(count-1))

if __name__ == "__main__":
    lines = load_input_lines(sys.argv[1])
    copies = [1]*len(lines)
    winning_numbers, scratch_numbers = [], []
    total_points = 0
    line_number = 0
    while line_number < len(lines):
        line = lines[line_number]
        [winning, scratched] = line.split('|')
        winning = winning.split(':')[1].strip()
        winning = number_str_to_set(winning)
        scratched = number_str_to_set(scratched)
        matches = scratched.intersection(winning)
        print(f"{line=}... {matches=} --> {count_points(matches)}")
        print(f"card copies: {len(matches) * copies[line_number]}")
        for i in range(len(matches)):
            copies[line_number + 1 + i] += copies[line_number]
        print(f"{copies=}")
        print(f"{winning=}, {scratched=}")
        
        card_points = count_points(matches)#  * copies[line_number]
        total_points += card_points
        line_number += 1
    total_cards = sum(copies)
    print(f"{total_points=}") # answer: 25651
    print(f"{total_cards=}")
    # 1139 -> too low
