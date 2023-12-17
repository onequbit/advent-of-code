#!/usr/bin/env python3

import sys
from os.path import abspath, dirname
sys.path.append(dirname(abspath("../..")))
from advent_of_code import load_input_lines
from advent_of_code import number_str_to_list


PHASES = [
            "soil",
            "fertilizer",
            "water",
            "light",
            "temperature",
            "humidity",
            "location"
        ]

MAP_SECTIONS = [
                "seed-to-soil",
                "soil-to-fertilizer",
                "fertilizer-to-water",
                "water-to-light",
                "light-to-temperature",
                "temperature-to-humidity",
                "humidity-to-location"
            ]

def _next(phase:str):
    if phase == PHASES[-1]:
        return None
    next_phase_index = PHASES.index(phase)+1
    return PHASES[next_phase_index]

def _last(phase:str):
    if phase == PHASES[0]:
        return None
    last_phase_index = PHASES.index(phase)-1
    return PHASES[last_phase_index]


def parse(lines:list):
    data = {}
    line_num = 0
    while line_num < len(lines):
        line = lines[line_num]
        if line.startswith("seeds:"):
            seeds = line.split(":")[1]
            data["seeds"] = number_str_to_list(seeds)
            for seed in data["seeds"]:
                data[str(seed)] = {section:{} for section in MAP_SECTIONS}

        elif line.endswith("map:"):
            map_name = line.split(" ")[0]
            map_line_num = line_num + 1
            map_data = []
            while map_line_num < len(lines) and (map_line := lines[map_line_num]):
                line_num = map_line_num
                map_data.append(number_str_to_list(map_line))
                
                map_line_num += 1
            data[map_name] = map_data
        line_num += 1
    return data

def parse_mapping(mapping_name:str):
    [source, destination] = mapping_name.split("-to-")
    return source, destination

def get_path(seed:int, mapping:str, map_data:dict):
    mappings = map_data[mapping]
    for [destination, source, span] in mappings:
        source_range = range(source, source+span)
        if seed in source_range:
            offset = seed - source
            return destination + offset
    return seed
        
if __name__ == "__main__":
    
    lines = load_input_lines(sys.argv[1])
    data = parse(lines)
    print(f"{data=}")
    seed_paths = {}
    for seed in data["seeds"]:
        source = seed
        print(f"{source=}")
        for section in MAP_SECTIONS:
            destination = get_path(source, section, data)
            data[str(seed)][section] = destination
            source = destination
    destinations = [data[str(seed)][MAP_SECTIONS[-1]] for seed in data["seeds"]]
    lowest_location = min(destinations)
    print(f"{destinations=}")
    print(f"{lowest_location=}")
