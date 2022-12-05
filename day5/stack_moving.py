#!/usr/bin/env python
from os.path import abspath, dirname, join
from io import TextIOWrapper


INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

def all_numbers(line):
    tokens = line.split()
    count = 0
    for token in tokens:
        if token.isnumeric():
            count += 1
    return count == len(tokens)

def parse_setup(line) -> dict:
    setup_line = {}
    line = line.replace('    [','~~~ [')
    line = line.replace(']    ','] ~~~')
    line = line.replace('    ',' ~~~')
    line = line.replace('\n','')
    parts = line.split(' ')
    setup_line['stack'] = parts
    return setup_line

def assign_columns(line) -> dict:
    columns = {}
    return columns

def get_setup(input_file:TextIOWrapper) -> dict:
    setup = dict(line_count=0)
    line_count = 0
    line = input_file.readline()
    while not all_numbers(line):
        setup_line = parse_setup(line)
        setup[str(line_count)] = setup_line
        line_count += 1
        line = input_file.readline()
    setup.update(assign_columns(line))
    setup['line_count'] = line_count    
    return setup

def parse_procedure(line) -> dict:
    return {}

def get_procedures(input_file:TextIOWrapper) -> list:
    line = input_file.readline()
    procedures = []
    while not all_numbers(line):
        procedures.append(parse_procedure(line))
        line = input_file.readline()
    return procedures

def get_input() -> tuple[dict, list]:
    setup = {}
    procedures = []
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        setup = get_setup(input_file)
        procedures = get_procedures(input_file)
    return setup, procedures

def find_stackresults():
    setup, procedures = get_input()
    result = []
    return result


if __name__ == '__main__':
    setup, procedures = get_input()
    for key in setup.keys():
        print(setup[key])
