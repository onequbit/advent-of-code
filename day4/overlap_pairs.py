#!/usr/bin/env python
from os.path import abspath, dirname, join

INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

def parse_line(line):
    range1, range2 = line.split(',')
    start1, end1 = range1.split('-')
    start2, end2 = range2.split('-')
    return (int(start1),int(end1),int(start2),int(end2))

def get_filedata():
    lines = []
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())
    data = []
    for line in lines:
        data.append(parse_line(line))
    return data

def count_fullycontained():
    data = get_filedata()
    count = 0
    for range_pair in data:
        s1,e1,s2,e2 = range_pair
        s2_is_contained = s1 <= s2 and e2 <= e1
        s1_is_contained = s2 <= s1 and e1 <= e2
        if s1_is_contained or s2_is_contained:
            count += 1
    return count

def count_alloverlaps():
    data = get_filedata()
    count = 0
    for range_pair in data:
        s1,e1,s2,e2 = range_pair
        non_overlap = s1 > e2 or s2 > e1
        if non_overlap:
            count += 1
    return len(data) - count

if __name__ == '__main__':
    print(f"day 4a: {count_fullycontained()}")
    print(f"day 4b: {count_alloverlaps()}")
    
