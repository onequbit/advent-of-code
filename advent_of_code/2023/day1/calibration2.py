#!/usr/bin/env python3
import os
import re
import sys

NUMBERS = ["one", "two", "three",
            "four", "five", "six",
            "seven", "eight", "nine"]

BAD_NUMBERS = {
    "sevenine": 79,
    "nineight": 98,
    "oneight": 18,
    "twone": 21,
    "threeight": 38,
    "fiveight": 58,
    "eightwo": 82,
    "eighthree": 83
}

def load_input_lines(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)
    with open(filename, 'r', encoding='utf-8') as input:
        return input.readlines()

def convert_number(number:str):
    if number not in NUMBERS:
        return str(number)
    return str(NUMBERS.index(number) + 1)

def decipher(lines:list):
    found_numbers = []
    for line in lines:
        line = line.strip()
        newline = line[:]
        for number in list(BAD_NUMBERS.keys()):
            if number in line:
                newline = newline.replace(number, str(BAD_NUMBERS[number]))
        for index, number in enumerate(NUMBERS):
            if number in line:
                newline = newline.replace(number, str(index+1))
        digits_only = ""
        for char in newline:
            if char.isdigit():
                digits_only += char
        found_number = digits_only[0] + digits_only[-1]
        print(line, found_number)
        found_numbers.append(found_number)
    return found_numbers

if __name__ == "__main__":
    calibrations = decipher(load_input_lines(sys.argv[1]))
    print(calibrations)
    total = 0
    for number in calibrations:
        total += int(number)
    print(total)
