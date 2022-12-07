#!/usr/bin/env python
from os.path import abspath, dirname, join
import json

INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

def get_input():
    lines = []
    with open(INPUT_FILE_NAME, mode='r') as input_file:
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

def day7a():
    limit = 100000
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
            else:
                directories.append(parts[2])
                path = collapsed_path(directories)
                directory[path] = dict(size=0, files=[], child_paths=[])
        elif parts[0].isnumeric(): 
            path = collapsed_path(directories)
            file_entry = dict(path=path, name = parts[1], size = parts[0])
            directory[path]['files'] += [file_entry]
            filesize = int(file_entry['size'])
            directory[path]['size'] += filesize
            for parent in get_parents(path):
                directory[parent]['size'] += filesize
                directory[parent]['child_paths'] += [path]

    for entry in directory.keys():
        size = directory[entry]['size']
        if size > 0 and size <= limit:
            total_size += size

    return total_size


def day7b():
    target = 30000000
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
            else:
                directories.append(parts[2])
                path = collapsed_path(directories)
                directory[path] = dict(size=0, files=[])
        elif parts[0].isnumeric(): 
            path = collapsed_path(directories)
            file_entry = dict(path=path, name = parts[1], size = parts[0])
            directory[path]['files'] += [file_entry]
            filesize = int(file_entry['size'])
            directory[path]['size'] += filesize
            parent = get_parent(path)
    
    print(json.dumps(directory, indent=4))

    directory_copy = directory.copy()
    keys = list(directory_copy.keys())
    root_paths = 0
    while len(keys) > root_paths:
        key = keys.pop(-1)
        if key not in directory_copy.keys():
            continue
        
        parent = get_parent(key)
        if parent == '//':
            root_paths += 1
            continue
        children = get_children(key, directory_copy)
        if len(children) == 0:            
            directory_copy[parent]['size'] += int(directory_copy[key]['size'])
            directory_copy.pop(key)
            keys = list(directory_copy.keys())
        else:
            keys += children
    
    for key in list(directory_copy.keys()):
        entry = directory_copy[key]
        print(key, json.dumps(entry))




if __name__ == '__main__':
    print(f"day 7a: {day7a()}") # day 7a: 1427048
    
    print(f"day 7b: {day7b()}")
