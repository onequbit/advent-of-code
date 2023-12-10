#!/usr/bin/env python3
import os
import re
import sys

def load_input_lines(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)
    with open(filename, 'r', encoding='utf-8') as input:
        return input.readlines()

def decipher(lines:list):
    sums = []
    for line in lines:
        print(line.strip())
        first_digit = re.search(r"\d", line)
        first_digit = line[first_digit.start()]
        last_digit = re.search(r"\d", line[::-1])
        last_digit = line[::-1][last_digit.start()]
        sums.append(int(first_digit + last_digit))
    return sums

if __name__ == "__main__":
    calibrations = decipher(load_input_lines(sys.argv[1]))
    print(calibrations)
    print(sum(calibrations))
