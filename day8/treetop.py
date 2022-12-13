#!/usr/bin/env python
from os.path import abspath, dirname, join

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

        self.map2 = [[{}] * len(lines)] * len(lines)
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

    def neighbors(self, row:int, column:int):
        top, bottom, left, right = 0,0,0,0
        if row == 0: 
            top = -1
        else:
            top = self.map[row-1][column]
        if row == self.size-1:
            bottom == -1
        else:
            bottom = self.map[row+1][column]
        if column == 0: 
            left = -1
        else:
            left = self.map[row][column-1]
        if column == self.size-1:
            right == -1
        else:
            right = self.map[row][column+1]
        
        return { 'top':top, 'left':left, 'right':right, 'bottom':bottom }

    def north_view(self,row,column):
        viewable = []
        my_height = self.map[row][column]
        if row == 0:
            return []
        rows = [r for r in range(0,row)][::-1]
        for row in rows:
            height = self.map[row][column]
            if len(viewable)>0 and viewable[-1] > height:
                break
            viewable.append(height)
            if height >= my_height:
                break
        return viewable

    def south_view(self,row,column):
        viewable = []
        my_height = self.map[row][column]
        if row == self.size - 1:
            return []
        rows = [r for r in range(row+1,self.size)]
        for r in rows:
            height = self.map[r][column]
            if len(viewable)>0 and viewable[-1] >= height:
                break
            viewable.append(height)
            if height >= my_height:
                break
        return viewable

    def west_view(self,row,column):
        viewable = []
        my_height = self.map[row][column]
        if column == 0:
            return []
        cols = [c for c in range(0,column)][::-1]
        for c in cols:
            height = self.map[row][c]
            if len(viewable)>0 and viewable[-1] > height:
                break
            viewable.append(height)
            if height >= my_height:
                break
        return viewable

    def east_view(self,row,column):
        viewable = []
        my_height = self.map[row][column]
        if column == self.size - 1:
            return []
        cols = [c for c in range(column+1,self.size)]
        for c in cols:
            height = self.map[row][c]
            if len(viewable)>0 and viewable[-1] > height:
                break
            viewable.append(height)
            if height >= my_height:
                break
        return viewable

    def scenic_score(self, row, column):
        north = self.north_view(row,column)
        south = self.south_view(row,column)
        west = self.west_view(row,column)
        east = self.east_view(row,column)
        print(f"north: {north}, south: {south}, west: {west}, east: {east}")
        north_score = len(north)
        if north_score == 0:
            north_score = 1
        south_score = len(south)
        if south_score == 0:
            south_score = 1
        west_score = len(west)
        if west_score == 0:
            west_score = 1
        east_score = len(east)
        if east_score == 0:
            east_score = 1
        print(f"north_score: {north_score}, south_score: {south_score}, west_score: {west_score}, east_score: {east_score}")
        return north_score * south_score * west_score * east_score

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
    hidden_rows = [0] * treemap.size
    for index, row in enumerate(treemap.map):
        hidden_rows[index] = scan_row(row)
    columns_map = transpose(treemap.map)
    hidden_columns = [0] * treemap.size
    for index, column in enumerate(columns_map):
        hidden_columns[index] = scan_row(column)
    hidden_columns = transpose(hidden_columns)
    hidden = []
    for row in range(treemap.size):
        combined_row = [(a,b) for a,b in zip(hidden_rows[row], hidden_columns[row])]
        combined_hidden = [1 if a==2 and b==2 else 0 for a,b in combined_row]
        hidden.append(combined_hidden)
    total_hidden = sum([sum(h) for h in hidden])
    total_visible = (treemap.size ** 2) - total_hidden
    return total_visible # answer --> 1779



def day8b(input_file):
    treemap = TreeMap(input_file)
    treemap.show()
    print('\n...')
    max_scores = []
    scores = []
    for row in range(treemap.size):
        for col in range(treemap.size):
            scores += [treemap.scenic_score(row,col)]
        max_scores += [max(scores)]
    
    return max(max_scores)


if __name__ == "__main__":
    
    input_file = 'input.txt'
    # input_file = 'example.txt'
    print(day8a(input_file)) # answer --> 1779
    print(day8b(input_file))
    # foo_table = [[1,2,3,4,5],[6,7,8,9,0],['a','b','c','d','e'],[1,2,3,4,5],[6,7,8,9,0]]
    # print(*foo_table, sep='\n')
    # bar_rable = transpose(foo_table)
    # print(*bar_rable, sep='\n')
