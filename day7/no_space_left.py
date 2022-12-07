#!/usr/bin/env python
from os.path import abspath, dirname, join
from enum import Enum
import re
import json

INPUT_FILE_NAME = join(dirname(abspath(__file__)),'example.txt')

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
    return reversed(parents)

def has_children(this_path:str, directories:dict):
    other_paths = directories.keys()
    for path in other_paths:
        if len(path) > len(this_path) and path.startswith(this_path):
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
    skipdir = ''
    for line in input_lines:
        parts = line.split()
        if parts[0] == "$" and parts[1] == 'cd':
            if (parts[2]) == '..':
                old_dir = collapsed_path(directories)
                directories.pop(-1)
                new_dir = collapsed_path(directories)
                print(f"old_dir: {old_dir}, new_dir: {new_dir}")
                skipdir = ''
            elif skipdir == '':
                directories.append(parts[2])
                path = collapsed_path(directories)
                directory[path] = dict(size=0, files=[])
                print(f"new dir: {path}, size: {directory[path]}")
        elif parts[0].isnumeric() and skipdir == '':
            path = collapsed_path(directories)
            file_entry = dict(path=path, name = parts[1], size = parts[0])
            directory[path]['files'] += [file_entry]
            filesize = int(file_entry['size'])
            print(f"file: {file_entry}, size: {filesize}")
            directory[path]['size'] += filesize
                
    # print(json.dumps(directory, indent=4))
    
    # for entry in directory.keys():
    #     if entry == '//':
    #         continue
    #     size = int(directory[entry]['size'])
    #     if size <= limit: #  and get_parent(entry) not in sizes.keys():
    #         sizes[entry] = size

    # while len(directory.keys()) > 0:
    #     key = list(directory.keys())[-1]
    #     subdir = directory[key]
    #     total_size += subdir['size']
    #     directory.pop(key)

    print(total_size)
    print(json.dumps(directory, indent=4))

    return total_size



def day7b():
    pass

if __name__ == '__main__':
    print(f"day 7a: {day7a()}")
    print(f"day 7b: {day7b()}")
