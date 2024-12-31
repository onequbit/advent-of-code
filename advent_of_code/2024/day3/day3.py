#!/usr/bin/env python3

"""
--- Day 3: Mull It Over ---
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

Your puzzle answer was 173419328.

________________
--- Part Two ---
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?


"""

import re
from icecream import ic


SAMPLE_INPUT = ["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"]


def load_data(filename):
    data = open(filename, "r", encoding="utf-8").readlines()
    return ''.join(data)

def find_mul_instructions(line):
    found = re.finditer(r"mul\((?P<first_op>[0-9]{1,3}),(?P<second_op>[0-9]{1,3})\)", line)
    return [f for f in found]

def find_enabled_blocks(line):
    strings = []
    found = re.findall(r"(?P<block1>.*)don't\(\)(?P<block2>.*)do\(\)(?P<block3>.*)", line)
    for a, b, c in found:
        ic(line, a, c)
        strings += [a, c]
    return ''.join(strings)

def parse_sections(line, separator):
    sep_index = line.find(separator)
    if sep_index == -1:
        return "", ""
    second_index = sep_index + len(separator)
    return line[:sep_index], line[second_index:]

def filter_code(line):
    enabled_parts = []
    DONT = "don't()"
    DO = "do()"
    start_enabled = str(line)
    enabled, start_disabled = parse_sections(line, DONT)
    a, b = enabled, start_disabled
    while a or b:
        enabled_parts.append(enabled)
        _, start_enabled = parse_sections(start_disabled, DO)
        enabled, start_disabled = parse_sections(start_enabled, DONT)
        a, b = enabled, start_disabled
    filtered_code = ''.join(enabled_parts)
    ic(line)
    ic(filtered_code)
    return filtered_code

def part_one(input_data):
    ic(len(input_data))
    found = find_mul_instructions(input_data)
    pairs = [(int(f.groups()[0]), int(f.groups()[1])) for f in found]
    products = [x * y for x, y in pairs]
    ic(sum(products))

def part_two(input_data):
    filtered = filter_code(input_data)
    part_one(filtered)


if __name__ == "__main__":
    input_data = load_data("day3_input.txt")

    part_one(input_data)
    # part_one: 173419328
    part_two(input_data)  
    # part_two: 1040515968 <-- too high
    # part_two: 144837267 <-- too high
    # part_two:  90669332