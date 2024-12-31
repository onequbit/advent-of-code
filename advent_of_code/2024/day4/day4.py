#!/usr/bin/env python3

"""

--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?

_____________________________________________________________________________

--- Part Two ---

The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

"""
from icecream import ic
import re

def rotate_clockwise(matrix):
    """Rotates a 2D matrix 90 degrees clockwise in-place."""
    # Transpose the matrix
    matrix[:] = list(zip(*matrix[::-1]))
    return matrix

def rotate_str_list(str_list):
    matrix = [[cell for cell in line.strip()] for line in str_list]
    rotated = rotate_clockwise(matrix)
    return [''.join(line) for line in rotated]

def load_data(filename):
    lines = open(filename, "r", encoding="utf-8").readlines()
    return [line.strip() for line in lines]

def do_search(input_data, term):
    all_matches = []
    for line in input_data:
        all_matches += re.findall(term, line)
    return all_matches

def do_diagonal_search(input_data, term):
    num_rows = len(input_data)
    term_len = len(term)
    found = 0

    def diagonal_check(row, col):
        found_chars = []
        for index, char in enumerate(term):
            found_chars.append(input_data[row+index][col+index] == char)
        return all(found_chars)

    for row_index, row in enumerate(input_data):
        if row_index > len(input_data)-term_len:
            continue
        for col_index, char in enumerate(row):
            if col_index > len(row)-term_len:
                continue
            if diagonal_check(row_index, col_index):
                found += 1

    return found

def part_one(input_data):
    found = 0
    found += len(do_search(input_data, "XMAS"))
    found += do_diagonal_search(input_data, "XMAS")

    input_data = rotate_str_list(input_data)
    found += len(do_search(input_data, "XMAS"))
    found += do_diagonal_search(input_data, "XMAS")

    input_data = rotate_str_list(input_data)
    found += len(do_search(input_data, "XMAS"))
    found += do_diagonal_search(input_data, "XMAS")

    input_data = rotate_str_list(input_data)
    found += len(do_search(input_data, "XMAS"))
    found += do_diagonal_search(input_data, "XMAS")
    
    print(found)


def part_two(input_data):
    found = 0
    wings = {"M", "S"}
    for r in range(1, len(input_data) - 1):
        for c in range(1, len(input_data[0]) - 1):
            if input_data[r][c] == "A":
                if {input_data[r - 1][c - 1], input_data[r + 1][c + 1]} == wings and {input_data[r - 1][c + 1], input_data[r + 1][c - 1]} == wings:
                    found += 1
    print(found)

if __name__ == "__main__":
    
    # input_data = load_data("day4_example.txt")
    input_data = load_data("day4_input.txt")

    part_one(input_data)  # 2462

    part_two(input_data)
    # 5395 <-- too high
    # 2680 <-- too high
    # 2641 <-- too high
    # 1554 <-- wrong
