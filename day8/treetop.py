#!/usr/bin/env python
from os.path import abspath, dirname, join

# class TreeCell:
#     def __init__(self, row, col, value):
#         self.row = row
#         self.col = col
#         self.value = value

class TreeMap:
    def __init__(self, input_file:str):
        lines = TreeMap.load(input_file)
        self.size = len(lines)
        self.map = [[0]*len(lines)] * len(lines)
        for row, row_str in enumerate(lines):
            row_cells = []
            for col, char in enumerate(row_str):
                row_cells.append(int(char))
            self.map[row] = row_cells

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
        t_map = self.transpose()
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
        return t_map

    @staticmethod
    def load(input_file):
        lines = []
        with open(input_file, mode='r') as input_file:
            for line in input_file.readlines():
                lines.append(line.strip())
        return lines

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


def scan_trees(trees:list):
    hidden = []
    left = trees[0]
    right = trees[-1]
    inner_trees = trees[1:-1]
    if len(trees) == 0:
        return hidden
    indexes = [i for i in spiral_index(len(trees))][2:]
    for index in indexes:
        tree = abs(trees[index])
        print(f"index:{index}, value:{tree}, left:{left}, inner:{inner_trees}, right:{right} >")
        if (tree <= left and tree < right) or (tree < left and tree <= right):
            hidden.append(tree)
            trees[index+1] *= -1
        if tree > left:
            left = tree
        if tree > right:
            right = tree
        print(f"index:{index}, value:{tree}, left:{left}, inner:{inner_trees}, right:{right} <-")
    print()
    return hidden
        
        






def day8a(input_file):
    treemap = TreeMap(input_file)
    print(treemap)
    # print()
    # treemap.show_t()

    # for n in range(treemap.size):
    #     print(treemap.get_cell(n,n))

    print("scanning rows...")
    for row in treemap.map:
        scan_trees(row)
    print(treemap)
    print("scanning columns...")
    for row in treemap.transpose():
        scan_trees(row)
    print(treemap)
    
    for test in range(10, 14):
        test_list = [i for i in range(0,test)]
        print(test_list)
        print(spiral_index(test))

    return ''


def day8b(input_file):
    treemap = TreeMap(input_file)
    return ''


if __name__ == "__main__":
    
    # input_file = 'input.txt'
    input_file = 'example.txt'
    print(day8a(input_file))
    print(day8b(input_file))
