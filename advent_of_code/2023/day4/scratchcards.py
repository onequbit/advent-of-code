#!/usr/bin/env python3

import sys
from os.path import abspath, dirname
sys.path.append(dirname(abspath("../..")))
from advent_of_code import load_input_lines

def number_str_to_set(numbers:str):
    numbers = [num for num in numbers.strip().split(' ') if num]
    return set(sorted(numbers))

def count_points(matches:set):
    count = len(matches)
    if count == 0:
        return 0
    return int(2**(count-1))

if __name__ == "__main__":
    lines = load_input_lines(sys.argv[1])
    
    winning_numbers, scratch_numbers = [], []
    total_points = 0
    for line in lines:
        [winning, scratched] = line.split('|')
        winning = winning.split(':')[1].strip()
        winning = number_str_to_set(winning)
        scratched = number_str_to_set(scratched)
        matches = scratched.intersection(winning)
        print(f"{winning=}, {scratched=}")
        print(f"{matches=} --> {count_points(matches)}")
        total_points += count_points(matches)
    print(total_points) # answer: 25651

