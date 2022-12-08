#!/usr/bin/env python
from os.path import abspath, dirname, join
import json
import copy

INPUT_FILE_NAME = join(dirname(abspath(__file__)),'example.txt')

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

def get_directory():    
    input_lines = get_input()
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

def get_directory_b():    
    input_lines = get_input()
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
                directory[path] = dict(size=0, child_paths=[])
        elif parts[0].isnumeric(): 
            path = collapsed_path(directories)
            filesize = int(parts[0])
            directory[path]['size'] += filesize
    return directory

@staticmethod
def gettotalsize(path:str, directory:dict):
    entry = directory[path]
    if entry['child_paths'] == 0:
        parent = directory[get_parent(path)]
        parent['size'] += entry['size']
        # parent['child_paths'].pop(path)
    else:
        for child in entry['child_paths']:
            gettotalsize(child, directory)
    return directory

def day7a():
    limit = 100000
    total_size = 0
    directory = get_directory()
    for entry in directory.keys():
        size = directory[entry]['size']
        if size > 0 and size <= limit:
            print(entry, size)
            total_size += size
    return total_size

def day7b():
    target = 8381165
    target_path = ''
    path_sizes = {}
    directory = get_directory()
    for entry in directory.keys():
        this_dir = directory[entry]
        children = get_children(entry, directory)
        # print(entry, children)
        this_size = this_dir['size']
        # for child in children:
        #     child_entry = directory[child]
        #     this_size += child_entry['size']
        path_sizes[str(this_size)] = entry
    # print(path_sizes)
    sizes = list(sorted([int(key) for key in path_sizes.keys()]))
    print(sizes)
    for size in sizes:
        if size <= target:
            path = path_sizes[str(size)]
            # print(path, size)
            print(f"*** {path} ***\n{directory[path]}")
    # target_path = path_sizes[str(max(sizes))]
    return target_path
    
        
if __name__ == '__main__':
    print()
    # print(f"day 7a: {day7a()}") # day 7a: 1427048
    print(f"day 7b: {day7b()}")

    
    