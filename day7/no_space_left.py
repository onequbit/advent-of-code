#!/usr/bin/env python
from os.path import abspath, dirname, join
from enum import Enum
import re
import json

INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

class ConsoleLine(Enum):
    LS = 1
    CD = 2
    DIR = 3
    FILE = 4

def get_input():
    lines = []
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    return lines

def get_path(directories):
    full_path = '/'.join(directories)
    return full_path

def collapsed_path(directories):
    path = '/'.join(directories) + '/'
    return path

def get_parent(path):
    parts = path.replace('//','/').split('/')
    return '/' + '/'.join(parts[:-2]) + '/'

def get_parents(this_path):
    parents = []
    parts = this_path.replace('//','/').split('/')[:-1]
    for index, _ in enumerate(parts):
        path = '/' + '/'.join(parts[:index]) + '/'
        parents.append(path)
    parents = [parent for parent in list(reversed(parents)) if parent != '//']
    return list(reversed(parents))

def has_children(this_path:str, directories:dict):
    other_paths = directories.keys()
    for path in other_paths:
        if path.startswith(this_path) and len(path) > len(this_path):
            return True
    return False

def get_children(this_path:str, directories:dict):
    if not has_children(this_path, directories):
        return []
    other_paths = directories.keys()
    children = []
    for path in other_paths:
        if len(path) > len(this_path) and path.startswith(this_path):
            children.append(path)
    return children

def get_children_sizes(this_path:str, directories:dict):
    child_paths = get_children(this_path, directories)
    total_size = 0
    for path in child_paths:
        total_size += directories[path]['size']    
    return total_size

def day7a():
    limit = 100000
    sizes = {}
    total_size = 0
    input_lines = get_input()
    directory = {}
    directories = []
    for line in input_lines:
        parts = line.split()
        if parts[0] == "$" and parts[1] == 'cd':
            if (parts[2]) == '..':
                old_dir = collapsed_path(directories)
                directories.pop(-1)
                new_dir = collapsed_path(directories)
                print(f"old_dir: {old_dir}, new_dir: {new_dir}")
            else:
                directories.append(parts[2])
                path = collapsed_path(directories)
                directory[path] = dict(size=0, files=[])
                print(f"new dir: {path}, size: {directory[path]}")
        elif parts[0].isnumeric(): 
            path = collapsed_path(directories)
            file_entry = dict(path=path, name = parts[1], size = parts[0])
            directory[path]['files'] += [file_entry]
            filesize = int(file_entry['size'])
            print(f"file: {file_entry}, size: {filesize}")
            directory[path]['size'] += filesize
            for parent in get_parents(path):
                directory[parent]['size'] += filesize

    for entry in directory.keys():
        parents = get_parents(entry) 
        size = directory[entry]['size']
        if size > 0 and size <= limit:
            total_size += size
            print(f"entry:{entry}, size:{size}, parents:{parents}")

    return total_size



def day7b():
    pass

if __name__ == '__main__':
    print(f"day 7a: {day7a()}")
    print(f"day 7b: {day7b()}")
