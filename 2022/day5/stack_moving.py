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

def parse_setup(line, number) -> list:
    setup_line = {}
    line = line.replace('    [','~~~ [')
    line = line.replace(']    ','] ~~~')
    line = line.replace('    ',' ~~~')
    line = line.replace('\n','')
    parts = line.split(' ')
    return parts

def assign_columns(line) -> dict:
    columns = {}
    return columns

def get_setup(input_file:TextIOWrapper) -> dict:
    setup = {}
    line_count = 0
    line = input_file.readline()
    while not all_numbers(line):
        setup_line = parse_setup(line, line_count)
        setup[f"row{line_count}"] = setup_line
        line_count += 1
        line = input_file.readline()
    bottom_row = setup[f"row{line_count - 1}"]
    for column in range(len(bottom_row)):
        setup[str(column+1)] = []
    for row_number in range(line_count-1,-1,-1):
        columns = setup[f"row{row_number}"]
        for stack_number, column in enumerate(columns):
            if column != '~~~':
                setup[str(stack_number+1)] += [column.replace('[','').replace(']','')]
        del setup[f"row{row_number}"]
    return setup

def parse_procedure(line) -> dict:
    parts = line.strip().split(' ')
    # move X from Y to Z
    count = parts[1]
    source = parts[3]
    dest = parts[5]
    procedure = dict(count=count, source=source, dest=dest, txt=line)
    # print(procedure)
    return procedure

def run_procedure(procedure:dict, stacks:dict):
    count = int(procedure['count'])
    source = procedure['source']
    dest = procedure['dest']
    for i in range(count):
        item = stacks[source].pop()
        stacks[dest].append(item)
    return stacks

def run_newprocedure(procedure:dict, stacks:dict):
    count = int(procedure['count'])
    source = procedure['source']
    dest = procedure['dest']
    items = ''
    for i in range(count):
        items = stacks[source].pop() + items
    stacks[dest] += items
    return stacks

def get_procedures(input_file:TextIOWrapper) -> list:
    line = input_file.readline()
    procedures = []
    while line != '':
        procedures.append(parse_procedure(line))
        line = input_file.readline()
    return procedures

def get_input() -> tuple[dict, list]:
    setup = {}
    procedures = []
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        setup = get_setup(input_file)
        _ = input_file.readline()
        procedures = get_procedures(input_file)
    # print(f"get_input:\nsetup:{setup},\n procedures:{procedures}")
    return setup, procedures

def find_stackresults():
    stacks, procedures = get_input()
    for procedure in procedures:
        stacks = run_procedure(procedure,stacks)
    top_items = ''
    for column in stacks.keys():
        top_items += stacks[column][-1]
    return top_items

def find_newstackresults():
    stacks, procedures = get_input()
    for procedure in procedures:
        stacks = run_newprocedure(procedure,stacks)
    top_items = ''
    for column in stacks.keys():
        top_items += stacks[column][-1]
    return top_items

if __name__ == '__main__':
    print(f"day5a: {find_stackresults()}")
    print(f"day5b: {find_newstackresults()}")

#         [Z]
#         [N]
#         [D]
# [C] [M] [P]
#  1   2   3