#!/usr/bin/env python3
from os.path import abspath, dirname, join

# class TreeCell:
#     def __init__(self, row, col, value):
#         self.row = row
#         self.col = col
#         self.value = value

class TreeMap:
    def __init__(self, input_file:str=None, other_map=None):
        if other_map is not None:
            self.map = TreeMap.load_t(other_map)
        elif input_file is not None:
            self.map = TreeMap.load(input_file)
        self.size = len(self.map)        
        self.map_size = self.size * self.size

    def __repr__(self):
        lines = []
        for row in self.map:
            lines += [str(row)]
        
        return '\n'.join(lines)

    def show(self):
        print()
        for row in self.map:
            print(row)
    
    def show_t(self):
        t_map = self.transpose().map
        for row in t_map:
            print(row)

    def get_cell(self, row, col):
        return self.map[row][col]

    def is_edge(self, row, col):
        top_edge = row == 0
        bot_edge = row == self.size-1
        lft_edge = col == 0
        rgt_edge = col == self.size-1
        return top_edge or bot_edge or lft_edge or rgt_edge

    def transpose(self):
        t_map = [0] * self.size
        for row in range(self.size):
            row_cells = []
            for col in range(self.size):
                row_cells.append(self.get_cell(col,row))
            t_map[row] = row_cells
        return TreeMap(other_map=t_map)

    @staticmethod
    def load(input_file:str):
        lines = []
        with open(input_file, mode='r') as input_file:
            for line in input_file.readlines():
                lines.append(line.strip())
        new_map = [[0]*len(lines)] * len(lines)
        for row, row_str in enumerate(lines):
            row_cells = []
            for _, char in enumerate(row_str):
                row_cells.append(int(char))
            new_map[row] = row_cells
        return new_map

    @staticmethod
    def load_t(treemap_t:list):
        new_map = []
        for row in treemap_t:
            new_map.append(row)
        return new_map



def spiral_index(some_length):
    temp_array = [i for i in range(0,some_length)]
    new_array = []
    while len(temp_array) >0:
        
        new_array.append(temp_array[0])
        new_array.append(temp_array[-1])
        temp_array = temp_array[1:-1]
        if len(temp_array) == 1:
            new_array.append(temp_array[0])
            break
    return new_array

def left_to_right(trees:list):
    left_edge = trees[0]
    highest = max(trees)
    position = 1
    while position < len(trees): #trees.index(highest):
        if left_edge >= trees[position]:
            trees[position] *= -1
        elif left_edge < trees[position]:
            left_edge = trees[position]
        position += 1
    left_to_right_hidden = [x for x,y in enumerate(trees) if y < 0]
    for i,t in enumerate(trees):
        trees[i] = abs(t)
    # trees = [abs(t) for t in trees]
    return left_to_right_hidden

def right_to_left(trees_:list):
    trees = [abs(t) for t in trees_]
    right_edge = trees[-1]
    highest = max(trees)
    position = len(trees)-2
    while position > 0: # trees.index(highest):
        if right_edge >= trees[position]:
            trees[position] *= -1
        elif right_edge < trees[position]:
            right_edge = trees[position]
        position -= 1
    right_to_left_hidden = [x for x,y in enumerate(trees) if y < 0]
    for i,t in enumerate(trees):
        trees[i] = abs(t)
    # trees = [abs(t) for t in trees]
    return right_to_left_hidden

def scan_trees(trees:list):
    # print(f"scan l2r: {trees}")
    l2r_hidden = left_to_right(trees)
    # print(f"scan l2r hidden: {l2r_hidden}")
    # print(f"scan r2l: {trees}")
    r2l_hidden = right_to_left(trees)
    # print(f"scan r2l hidden: {r2l_hidden}")
    hidden = []
    for index in range(0,len(trees)):
        if index in l2r_hidden and index in r2l_hidden:
            hidden.append(index)
        else:
            hidden.append(0)
    return hidden        
        

def day8a(input_file:str):
    treemap = TreeMap(input_file)
    treemap.show()
    print("scanning rows...")
    hidden_l2r = []
    for row in treemap.map:
        hidden_l2r.append(scan_trees(row))
    hidden_map_l2r = TreeMap(other_map=hidden_l2r)
    hidden_map_l2r.show() 
    print()    

    treemap.show_t()
    print("scanning columns...")
    hidden_r2l = []
    treemap_t = treemap.transpose().map
    for col in treemap_t:
        hidden_r2l.append(scan_trees(col))     
    hidden_map_r2l = TreeMap(other_map=hidden_r2l)
    hidden_map_r2l.show() 
    print()

    hidden_r2l_transposed = hidden_map_r2l.transpose()
    hidden_r2l_transposed.show()
    hidden_count = 0
    for map_a,map_b in zip(hidden_map_l2r.map, hidden_r2l_transposed.map):
        for a,b in zip(map_a, map_b):
            if a > 0 and b > 0:
                hidden_count += 1
    
    return treemap.map_size - hidden_count


def day8b(input_file):
    treemap = TreeMap(input_file)
    return ''


if __name__ == "__main__":
    
    input_file = 'input.txt'
    # input_file = 'example.txt'
    print(day8a(input_file))
    print(day8b(input_file))
