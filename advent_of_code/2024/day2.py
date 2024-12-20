#!/usr/bin/env python3
"""
--- Day 2: Red-Nosed Reports ---
Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.

While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.

They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.

The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.
So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?

--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?

"""
from enum import Enum
from math import copysign
from operator import is_
from icecream import ic

SAMPLE_FILE = "day2_sample.txt"
INPUT_FILE = "day2_input.txt"


class DuplicateException(Exception):
    pass


def load_data(filename):
    data = open(filename, "r", encoding="utf-8").readlines()
    number_lines = [[int(n) for n in line.split()] for line in data]
    return number_lines


def strictly_increasing(L):
    return all( x < y for x, y in zip(L, L[1:]))
    
def strictly_decreasing(L):
    return all( x > y for x, y in zip(L, L[1:]))

def strictly_monotonic(L):
    return strictly_increasing(L) or strictly_decreasing(L)

def find_unstable(items):
    deltas = [abs(x-y) for x, y in zip(items[:-1], items[1:])]
    unstable = [items[i+1] for i, d in enumerate(deltas) if d > 3]
    return unstable

def find_reversals(items):
    signs = [copysign(1, x-y) for x, y in zip(items, items[1:])]
    # ic(signs)
    reversals = []
    for index, delta in enumerate(signs[:-1]):
        next_sign = signs[index+1]
        if delta != next_sign:
            reversals.append(items[index+1])
    return reversals

def duplicate_found(number_list):
    duplicates = []
    for num in number_list:
        if num in duplicates:
            continue
        if number_list.count(num) > 1:
            duplicates.append(num)
    return duplicates

def find_unsafe_levels(report):
    unstables = find_unstable(report)
    duplicates_found = duplicate_found(report)
    reversals = find_reversals(report)
    unsafe_levels = list(set(unstables + duplicates_found + reversals))
    if len(unsafe_levels) > 0:
        ic(unsafe_levels, report)
    return unsafe_levels

def is_safe(report):
    return len(find_unsafe_levels(report)) == 0
    # monotonic = strictly_monotonic(report)
    # duplicates_found = duplicate_found(report)
    # unstable_items = find_unstable(report)
    # return monotonic and (not duplicates_found) and (not unstable_items) 

def part_one(datafile:str):
    safe_count = 0
    report_data = load_data(datafile)
    for line in report_data:
        if is_safe(line):
            safe_count += 1
    print(f"part 1: {safe_count=}")


def part_two(datafile:str):
    safe_count = 0
    report_data = load_data(datafile)
    safe_reports = []
    saved_lines = []
    for line in report_data:
        if not line:
            break
        if is_safe(line):
            # print(f"*{line}******************** SAFE")
            safe_reports.append(line)
        else:
            print("----------------------------------------------------------")
            print(line)
            unsafe = list(set(find_unsafe_levels(line)))
            for item in unsafe:
                modified_line = line.copy()
                modified_line.remove(item)
                if is_safe(modified_line):
                    saved_lines.append(modified_line)
                    print(f"*** SAVED! {modified_line} ***")
                    break
    ic(len(saved_lines))
    ic(len(safe_reports))
    safe_count = len(safe_reports + saved_lines)
    print(f"part 2: {safe_count=}")



if __name__ == "__main__":
    part_one(INPUT_FILE)  # 624
    part_two(INPUT_FILE)  # 651 <-- too low!