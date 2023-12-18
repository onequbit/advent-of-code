#!/usr/bin/env python3
from tqdm import tqdm
import sys
from os import get_terminal_size
from os.path import abspath, dirname
sys.path.append(dirname(abspath("../..")))
from advent_of_code import load_input_lines
from advent_of_code import number_str_to_list

H_BAR = "#" * (get_terminal_size().columns - 2)

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

class SeedSpan:
    def __init__(self, start:int, span:int):
        self.start = start
        self.end = start + span
        self.span = span
        self._set = set(range(start, start+span))
    
    def __add__(self, other):
        if self._set.issuperset(other):
            return [self]
        if self._set.issubset(other):
            return [other]
        if self._set.isdisjoint(other):
            return [self, other]
        return self._set.union(other)
    
    def tolist(self):
        return list(self._set)

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
    print(f'{data["seeds"]=}')
    return data

def seed_in_span(seed:int, span_start:int, span_end:int):
    return seed >= span_start and seed <= span_start+span_end

def get_new_seed_list(data:dict):
    new_list = []
    seed_number = 0
    while seed_number + 1 < len(data["seeds"]):
        seed = data["seeds"][seed_number]
        span = data["seeds"][seed_number + 1]
        new_span = SeedSpan(seed, span)
        print(new_span)
        new_list += new_span.tolist()
        seed_number += 2
    return list(set(new_list))

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

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def part_1(data:dict):
    print("part_1")
    for seed in data["seeds"]:
        source = seed
        for section in MAP_SECTIONS:
            data[str(seed)][section] = get_path(source, section, data)
            source = data[str(seed)][section]
    destinations = [data[str(seed)][MAP_SECTIONS[-1]] for seed in data["seeds"]]
    lowest_location = min(destinations)
    print(f"{destinations=}")
    print(f"{lowest_location=}")
    
    
def part_2(data:dict):
    print("part_2")
    new_seed_list = [data["seeds"][i] for i, _ in enumerate(data["seeds"]) if i % 2 == 0]
    new_seed_span = [data["seeds"][i] for i, _ in enumerate(data["seeds"]) if i % 2 == 1]
    seed_ranges = [(seed, span) for seed, span in zip(new_seed_list, new_seed_span)] 
    all_seeds = {}
    for seed, span in tqdm(seed_ranges):
        all_seeds[(seed,span)] = range(seed, seed+span)
        print(f"({seed=},{span=}): {all_seeds[(seed,span)]=}")
    largest_range = max(new_seed_span)
    print(f"{largest_range=}")
    largest_seed_start = new_seed_list[new_seed_span.index(largest_range)]
    largest_span = all_seeds[(largest_seed_start,largest_range)]
    print(f"{largest_span=}")

if __name__ == "__main__":
    lines = load_input_lines(sys.argv[1])
    data = parse(lines)
    part_1(data)
    print(H_BAR)
    part_2(data)
    
    