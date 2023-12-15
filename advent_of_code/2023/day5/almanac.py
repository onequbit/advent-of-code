#!/usr/bin/env python3

import sys
from os.path import abspath, dirname
sys.path.append(dirname(abspath("../..")))
from advent_of_code import load_input_lines
from advent_of_code import number_str_to_list


def parse(lines:list):
    data = {}
    line_num = 0
    while line_num < len(lines):
        line = lines[line_num]
        if line.startswith("seeds:"):
            seeds = line.split(":")[1]
            data["seeds"] = number_str_to_list(seeds)
        
        if line.endswith("map:"):
            map_name = line.split(" ")[0]
            print(map_name)
            map_line_num = line_num + 1
            map_data = []
            while map_line_num < len(lines) and (map_line := lines[map_line_num]):
                print(line_num, map_line_num, map_line)
                line_num = map_line_num
                map_data.append(number_str_to_list(map_line))
                map_line_num += 1
            data[map_name] = map_data
        line_num += 1

    return data

if __name__ == "__main__":
    lines = load_input_lines(sys.argv[1])
    
    data = parse(lines)
    print(data)
