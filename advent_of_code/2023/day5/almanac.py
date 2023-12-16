#!/usr/bin/env python3

import sys
from tqdm import tqdm
from os.path import abspath, dirname
import json
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

LAST_PHASE = PHASES[-1]

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
    if phase == LAST_PHASE:
        return None
    next_phase_index = PHASES.index(phase)+1
    return PHASES[next_phase_index]

def parse(lines:list):
    data = {}
    line_num = 0
    while line_num < len(lines):
        line = lines[line_num]
        if line.startswith("seeds:"):
            seeds = line.split(":")[1]
            data["seeds"] = number_str_to_list(seeds)
            for seed in data["seeds"]:
                data[str(seed)] = {}
        
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
    for seed in tqdm(data["seeds"]):
        source = seed
        print(f"{source=}")
        for phase in tqdm(PHASES[:-1]):
            section = f"{phase}-to-{_next(phase)}"
            destination = get_path(source, section, data)
            data[str(source)]["destination"] = destination
        source = destination
    data["destinations"] = {}
    for seed in data["seeds"]:
        data["destinations"][str(seed)] = data[str(seed)]["destination"]
    destinations = [data["destinations"][str(seed)] for seed in data["seeds"]]
    dereferences = {str(location):seed for seed,location in data["destinations"].items()}
    locations = [int(location) for location in dereferences.keys()]
    lowest_location = min(locations)
    print(data["destinations"])
    print(dereferences)
    print(dereferences[str(lowest_location)])
    # 1901414562 -> too high