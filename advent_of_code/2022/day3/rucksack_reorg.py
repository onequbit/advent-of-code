#!/usr/bin/env python
from os.path import abspath, dirname, join
import string
from itertools import zip_longest


INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

def get_rucksacks():
    sacks = []
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        for line in input_file.readlines():
            sacks.append(line.strip())
        return sacks

def get_priority(letter):
    alphabet = string.ascii_lowercase + string.ascii_uppercase
    return alphabet.index(letter) + 1

def get_double(sack):
    half = len(sack)//2
    compartment_a, compartment_b = sack[:half],sack[half:]
    found_doubles = set()
    for item in compartment_a:
        if item in compartment_b:
            found_doubles.add(item)
    return list(found_doubles)

def find_mispacked():
    sacks = get_rucksacks()
    doubles = []
    for sack in sacks:
        doubles += get_double(sack)
    total = 0
    for double in doubles:
        total += get_priority(double)
    return total  

def find_group_badge(group):
    bag1, bag2, bag3 = group
    for item in bag1:
        if item in bag2 and item in bag3:
            return item
    for item in bag2:
        if item in bag1 and item in bag3:
            return item
    for item in bag3:
        if item in bag1 and item in bag2:
            return item
    raise Exception('no badge found')
            
def get_groups():
    sacks = get_rucksacks()
    groups = []
    while len(sacks) > 0:
        bag1, bag2, bag3 = sacks.pop(), sacks.pop(), sacks.pop()
        groups.append((bag1, bag2, bag3))
    return groups

def get_badges():
    groups = get_groups()
    badges = []
    for group in groups:
        badges.append(find_group_badge(group))
    badge_priorities = [get_priority(badge) for badge in badges]
    return badge_priorities

if __name__ == '__main__':
    print(f"day 3a: {find_mispacked()}")
    print(f"day 3b: {sum(get_badges())}")
    
          
    
