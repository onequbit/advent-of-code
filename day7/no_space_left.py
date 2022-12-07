#!/usr/bin/env python
from os.path import abspath, dirname, join

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
                directory[path] = dict(size=0, files=[])
        elif parts[0].isnumeric(): 
            path = collapsed_path(directories)
            file_entry = dict(path=path, name = parts[1], size = parts[0])
            directory[path]['files'] += [file_entry]
            filesize = int(file_entry['size'])
            directory[path]['size'] += filesize
            for parent in get_parents(path):
                directory[parent]['size'] += filesize

    for entry in directory.keys():
        parents = get_parents(entry) 
        size = directory[entry]['size']
        if size > 0 and size <= limit:
            total_size += size

    return total_size


def day7b():
    pass

if __name__ == '__main__':
    print(f"day 7a: {day7a()}") # day 7a: 1427048
    print(f"day 7b: {day7b()}")
