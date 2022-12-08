#!/usr/bin/env python
from os.path import abspath, dirname, join
import json
import copy

INPUT_FILE_NAME = join(dirname(abspath(__file__)),'example.txt')

def get_input(input_file:str):
    lines = []
    with open(input_file, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    return lines

def collapsed_path(directories):
    path = '/'.join(directories) + '/'
    return path

def get_parent(this_path):
    parts = this_path.replace('//','/').split('/')[:-1]
    return '/' + '/'.join(parts[:-1]) + '/'

def get_parents(this_path):
    parents = []
    parts = this_path.replace('//','/').split('/')[:-1]
    for index, _ in enumerate(parts):
        path = '/' + '/'.join(parts[:index]) + '/'
        parents.append(path)
    parents = list(set(parents))
    parents = [parent for parent in list(reversed(parents)) if parent != '//']
    return parents

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
    children = list(set(children))
    return children

def get_directory(input_file:str):    
    input_lines = get_input(input_file)
    directory = {}
    directories = []
    for line in input_lines:
        parts = line.split()
        if parts[0] == "$" and parts[1] == 'cd':
            if (parts[2]) == '..':
                directories.pop(-1)
            else:
                directories.append(parts[2])
                path = collapsed_path(directories)
                directory[path] = {}
                directory[path]['size'] = 0
                directory[path]['files'] = []
                directory[path]['child_paths'] = []
        elif parts[0].isnumeric(): 
            path = collapsed_path(directories)
            file_entry = dict(path=path, name = parts[1], size = parts[0])
            directory[path]['files'] += [file_entry]
            filesize = int(file_entry['size'])
            directory[path]['size'] += filesize
            for parent in get_parents(path):
                directory[parent]['size'] += filesize
                directory[parent]['child_paths'] += [path]
    return directory


def day7a(input_file):
    limit = 100000
    total_size = 0
    directory = get_directory(input_file)
    for entry in directory.keys():
        size = directory[entry]['size']
        if size > 0 and size <= limit:
            print(entry, size)
            total_size += size
    return total_size


if __name__ == '__main__':
    print(f"day 7a: {day7a('input.txt')}") # day 7a: 1427048

    
    