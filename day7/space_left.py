#!/usr/bin/env python
from os.path import abspath, dirname, join
import json


class DirectoryNode(dict):
    def __init__(self, name, parent=None):
        super().__init__()
        self.path = name
        if parent is not None:
            self.path = join(parent.path, name)
        self.parent = parent
        self.name = name
        self.files = list()
        self.children = {}
        # print(self.toJSON())

    def get_size(self):
        size = 0
        for file in self.files:
            size += file.size
        for child in self.children:
            size += child.get_size()
        return size

    def root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.root()

    def toJSON(self):
        files = [file.__dict__() for file in self.files]
        parent = '' if self.parent is None else self.parent.name
        child_dirs = [self.children[key] for key in self.children.keys()]
        children = [child for child in child_dirs]
        json_str = str({"type":"Dir", "name":self.name, "parent":parent, "path":self.path,
                "files":files, "children":children}).replace("'", '"')
        return json_str

    def __repr__(self):
        return self.toJSON()

    def __str__(self):
        return self.toJSON()

class FileNode(dict):
    def __init__(self, name:str, size:int, parent:DirectoryNode):
        super().__init__()
        self.parent = parent
        self.name = name
        self.size = size

    def __dict__(self):
        return {"type":"File", "name":self.name, "size":self.size}

    def toJSON(self):
        return str(self.__dict__())
        

    # def __str__(self):
    #     return self.toJSON()

def is_cd(line:str):
    # print(f"is_cd: {line}")
    return line.startswith("$ cd")

def is_dir(line:str):
    # print(f"is_dir: {line}, {line.split(' ')}")
    return line.startswith("dir")

def is_file(line:str):
    if line == '':
        return False
    if is_cd(line):
        return False
    # print(f"is_file: {line}, {len(line)} chars")
    return line.split()[0].isnumeric()

def build_tree(input_file):
    lines = []
    with open(input_file, mode='r') as input_file:        
        root = DirectoryNode(name='/')
        node = root

        while True:
            line = input_file.readline().strip()
            if not line:
                break
            if line == '$ cd /':
                node = root
                continue
            if line == '$ ls':
                continue
            if is_file(line):
                [size, name] = line.split(' ')
                file = FileNode(name=name, size=size, parent=node)
                node.files.append(file)
                continue
            if is_cd(line):
                dir_name = line.split(' ')[2]
                if dir_name == '..':
                    node = node.parent
                else:
                    node = node.children[dir_name]
                continue
            if is_dir(line):
                dir_name = line.split(' ')[1]
                sub_dir = DirectoryNode(name=dir_name, parent=node)
                node.children[dir_name] = sub_dir
                continue            
            
    result = node.root()
    return result
    

def day7a():
    limit = 100000
    tree = build_tree("example.txt")
    return tree

def day7b():
    target = 8381165
    return
    
        
if __name__ == '__main__':
    print(day7a()) # day 7a: 1427048
    # print(f"day 7a:\n{day7a()}") # day 7a: 1427048
    # print(f"day 7b:\n{day7b()}")

    
    