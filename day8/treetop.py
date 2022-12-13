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
        m = self.map
        return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

    @staticmethod
    def load(input_file):
        lines = []
        with open(input_file, mode='r') as input_file:
            for line in input_file.readlines():
                lines.append(line.strip())
        return lines

def scan_row(tree_row:list):
    height = 0
    hidden = [0] * len(tree_row)
    hidden[0] = -1
    hidden[-1] = -1
    
    for index, tree in enumerate(tree_row):
        if tree > 0 and tree > height:
            height = tree
        else:
            hidden[index] += 1
    # hidden_r2l = [0] * len(tree_row)
    height = 0
    for index in range(len(tree_row)-1,-1,-1):
        tree = tree_row[index]
        if tree > height:
            height = tree
        else:
            hidden[index] += 1
    return hidden

def transpose(some_array):
    m = some_array
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

def day8a(input_file):
    treemap = TreeMap(input_file)
    treemap.show()

    print("scanning rows...")

    hidden_rows = [0] * treemap.size
    for index, row in enumerate(treemap.map):
        hidden_rows[index] = scan_row(row)
    print(*hidden_rows, sep='\n')
    print("scanning columns...")
    columns_map = transpose(treemap.map)
    hidden_columns = [0] * treemap.size
    for index, column in enumerate(columns_map):
        hidden_columns[index] = scan_row(column)
    hidden_columns = transpose(hidden_columns)
    print(*hidden_columns, sep='\n')
    print("combined")
    hidden = []
    for row in range(treemap.size):
        combined_row = [(a,b) for a,b in zip(hidden_rows[row], hidden_columns[row])]
        print(combined_row)
        combined_hidden = [1 if a==2 and b==2 else 0 for a,b in combined_row]
        hidden.append(combined_hidden)
    print(*hidden, sep='\n')
    total_hidden = sum([sum(h) for h in hidden])
    total_visible = (treemap.size ** 2) - total_hidden
    return total_visible


def day8b(input_file):
    treemap = TreeMap(input_file)
    return ''


if __name__ == "__main__":
    
    input_file = 'input.txt'
    # input_file = 'example.txt'
    print(day8a(input_file))
    # print(day8b(input_file))
    # foo_table = [[1,2,3,4,5],[6,7,8,9,0],['a','b','c','d','e'],[1,2,3,4,5],[6,7,8,9,0]]
    # print(*foo_table, sep='\n')
    # bar_rable = transpose(foo_table)
    # print(*bar_rable, sep='\n')
