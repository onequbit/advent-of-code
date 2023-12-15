#!/usr/bin/env python3

from os.path import basename, dirname, isfile, join
import inspect

def load_input_lines(filename):
    if not isfile(filename):
        caller_file = inspect.stack()[1].filename
        newpath = join(dirname(caller_file), basename(filename))
        if not isfile(newpath):
            raise FileNotFoundError(filename)
        filename = newpath
    with open(filename, 'r', encoding='utf-8') as input:
        return [line.strip() for line in input.readlines()]

def number_str_to_list(numbers:str):
    return [int(num) for num in numbers.strip().split(' ') if num]
    
def number_str_to_set(numbers:str):
    return set(number_str_to_list(numbers))
