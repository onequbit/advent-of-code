#!/usr/bin/env python3
import json
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

def parse(lines:list):
    data = {"seeds":[], "seeds2": [], "seeds_copy":[]}
    line_num = 0
    while line_num < len(lines):
        line = lines[line_num]
        if line.startswith("seeds:"):
            seeds = line.split(":")[1]
            if not data["seeds"]:
                data["seeds"] += (number_str_to_list(seeds))
            seeds_copy = list(data["seeds"])
            data["seeds_copy"] += seeds_copy
            print(f"{seeds_copy=}")
            for number in range(0, len(seeds_copy), 2):
                seed, span = seeds_copy[number], seeds_copy[number+1]
                data["seeds2"] += [(seed,span)]
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
    print(f"get_path: {mappings=}")
    for [destination, seed_mapping, span] in mappings:
        map_range = range(seed_mapping, seed_mapping+span)
        print(f"get_path: {seed=}, {span=}, {mapping=}, {map_range=}")
        if seed in map_range:
            offset = seed - seed_mapping
            return destination + offset
    return seed

def get_path2(seed:int, span:int, mapping:str, map_data:dict):
    source_range = set(range(seed, seed + span))
    print(f"get_path2: {seed=}, {span=}, {mapping=}, {source_range=}")
    for source_seed in source_range:
        destination = get_path(source_seed, mapping, map_data)
        if destination == seed:
            continue
        return destination
    return seed

if __name__ == "__main__":
    
    lines = load_input_lines(sys.argv[1])
    data = parse(lines)
    print(f"{data=}")
    print("Part 1: " + "-"*100)
    print(f"{data['seeds']=}")
    print(f"size: {len(data['seeds'])}")
    seed_paths = {}
    for seed in data["seeds"]:
        source = seed
        for section in MAP_SECTIONS:
            destination = get_path(source, section, data)
            data[str(seed)][section] = destination
            source = destination
    destinations = [data[str(seed)][MAP_SECTIONS[-1]] for seed in list(data["seeds"])] 
    lowest_location = min(destinations)
    print(f"{destinations=}")
    print(f"{lowest_location=}")
    # *** puzzle answer: 88151870
    
    # print("Part 2: " + "-"*100)
    # print(f"{data['seeds2']=}")
    # print(f"size: {len(data['seeds2'])}")
    # for seed2, span in data["seeds2"]:
    #     print(f"seeds2 loop: {seed2=}, {span=}...")
    #     source = seed2
    #     for section in MAP_SECTIONS:
    #         destination = get_path2(source, span, section, data)
    #         data[str(seed2)][section] = destination
    #         source = destination
        
    # destinations2 = [data[str(seed)][MAP_SECTIONS[-1]] for seed,_ in data["seeds2"]]
    # lowest_location2 = min(destinations2)
    # print(f"{destinations2=}")
    # print(f"{lowest_location2=}")