#!/usr/bin/env python
from os.path import abspath, dirname, join

INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

def get_inputstrings():
    lines = []
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    return lines

# Examples: 
# mjqjpqmgbljsphdztnvjfqwrcgsmlb --> answer: 7
# bvwbjplbgvbhsrlpgdmjqwftvncz --> answer: 5
# nppdvjthqldpwncqszvftbrmjlhg --> answer: 6
# nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg --> answer: 10
# zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw --> answer: 11

def has_duplicates(input, size):
    for start in range(1, size):
        char = input[start-1]
        if char in input[start:]:
            return True
    return False

def sliding_window(input:str, size:int):
    if len(input) < size:
        return []
    def get_chars(index):
        return input[index:index+size]
    tail = len(input) - (size - 1)
    return [get_chars(index) for index in range(0,tail)]

def start_marker():
    result = []
    size = 4
    for input_str in get_inputstrings():
        window_strings = sliding_window(input_str, size)
        for index, window in enumerate(window_strings):
            if not has_duplicates(window, size):
                result.append(index+4)
                break
    return result

def message_marker():
    result = []
    size = 14
    for input_str in get_inputstrings():
        window_strings = sliding_window(input_str, size)
        for index, window in enumerate(window_strings):
            if not has_duplicates(window, size):
                result.append(index+size)
                break
    return result

if __name__ == '__main__':
    print(f"day 6a: {start_marker()}")
    print(f"day 6b: {message_marker()}")