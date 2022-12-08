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

    def get_size(self):
        size = 0
        for file in self.files:
            size += int(file.size)
        for child in self.children:
            size += self.children[child].get_size()
        return size

    def get_sizes_under(self, limit:int) -> list:
        my_size = self.get_size()
        path_sizes = {f"{self.path}":my_size}
        for key in self.children:
            child_sizes = self.children[key].get_sizes_under(limit)
            path_sizes.update(child_sizes)
        sizes = [(key, path_sizes[key]) for key in path_sizes.keys()]
        sizes = [(name,size) for name,size in sizes if size <= limit]
        return sizes

    def root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.root()

    def find(self, path:str):
        result = self
        if self.path == path:
            return self
        for child in self.children.keys():
            if child in path:
                result = self.children[child].find(path)
        return result

    def find_children(self):
        if len(self.children) == 0:
            return []
        collection = [join(self.path,child) for child in self.children.keys()]
        for child in collection:
            child_dir = self.find(child)
            collection += child_dir.find_children()
        return list(set(sorted(collection)))

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
        
def is_cd(line:str):
    return line.startswith("$ cd")

def is_dir(line:str):
    return line.startswith("dir")

def is_file(line:str):
    if line == '':
        return False
    if is_cd(line):
        return False
    return line.split()[0].isnumeric()

def build_tree(input_file):
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
                dir_path = join(node.path, dir_name)
                sub_dir = DirectoryNode(name=dir_name, parent=node)
                node.children[dir_name] = sub_dir
                continue            
            
    result = node.root()
    return result
    

def day7a(input_file):
    limit = 100000
    tree = build_tree(input_file)
    sizes = tree.get_sizes_under(limit)
    # print(sizes)
    sizes = [int(size) for _,size in sizes]
    return sum(sizes)

def day7b(input_file:str):
    target = 30000000
    tree = build_tree(input_file)
    child_sizes = []
    for key in tree.children.keys():
        child = tree.find(key)
        child_sizes.append((child.path, child.get_size()))
    print(*child_sizes, sep='\n')
    print(". . .")
    selected = [(path, size) for path,size in child_sizes if size <= target]
    selected, _ = sorted(selected, key=lambda a: a[1])[-1]
    print(selected)
    children = tree.find('/ctd').find_children()
    total_size = 0
    for child in children:
        node = tree.find(child)
        total_size += node.get_size()
        # print(child, node.get_size())
    return total_size
    # print(tree)
    all_branches = tree.find_children()
    # path_sizes = []
    # for key in all_branches:
    #     size = tree.find(key).get_size()
    #     if size <= target:
    #         print(f"{key} --> size: {size}")
    #         path_sizes.append((key, size))

    # found = tree.get_sizes_under(target)
    # print(*found, sep='\n')
    # root = tree.root()
    # children = [tree.find(child) for child in tree.children]
    # for key in tree.children.keys():
    #     child = tree.find(key)
    #     child_output = []
    #     for key2 in child.children.keys():
    #         sub_child = tree.find(key2)
    #         sub_sizes = sub_child.get_sizes_under(target)
    #         sub_total = 0
    #         for _, sub_size in sub_sizes:
    #             sub_total += sub_size
    #         child_output.append(f"{key2} {sub_total}")
    #     sizes = child.get_sizes_under(target)
    #     total_size = 0
    #     for path,size in sizes:
    #         total_size += size
    #     print(f"{key} {total_size}: . . .", )
    #     print(*child_output, sep='\n')
    #     print("...")

    # print(tree)
    # print("*****************************")
    # path_sizes = [(path,size) for path,size in tree.get_sizes_under(target)]
    # print(*path_sizes, sep='\n')
    # sizes_only = [size for _, size in path_sizes]
    # # print(*sizes_only, sep='\n')
    # target_size = max(sizes_only)
    # # [(a,b) for a,b in sizes if b == target_size]
    # item_path = ''
    # for path, size in path_sizes:
    #     if size == target_size:
    #         item_path = path
    #         break
    # print(target_size, item_path)
    # print(f"target path: {item_path}")
    # subtree = tree.find(item_path)
    # print(f"target found: {subtree.path}")

    # print(f"target found size: {subtree.get_size()}")
    # print(f"target found tree: {subtree.find_children()}")
    # return max(sizes_only)
    return 0
        
if __name__ == '__main__':
    # print(day7a()) # day 7a: 1427048

    input_file = 'input.txt'
    
    # print(f"day 7a: {day7a(input_file)}") # day 7a: 1427048
    # print("#" * 120)
    # print("#" * 120)
    # print("#" * 120)
    print(f"day 7b:\n{day7b(input_file)}")
    # _ = day7b(input_file)
    
    