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

from math import copysign
from icecream import ic

SAMPLE_FILE = "day2_sample.txt"
INPUT_FILE = "day2_input.txt"


def load_data(filename):
    data = open(filename, "r", encoding="utf-8").readlines()
    number_lines = [[int(n) for n in line.split()] for line in data]
    return number_lines


def strictly_increasing(L):
    return all(x < y for x, y in zip(L, L[1:]))
    
def strictly_decreasing(L):
    return all(x > y for x, y in zip(L, L[1:]))

def strictly_monotonic(L):
    return strictly_increasing(L) or strictly_decreasing(L)

def find_unstable(items):
    deltas = [abs(x-y) for x, y in zip(items[:-1], items[1:])]
    unstable = [items[i] for i, d in enumerate(deltas) if d > 3]
    return list(set(unstable))

def duplicate_found(number_list):
    duplicates = []
    for num in number_list:
        if num in duplicates:
            continue
        if number_list.count(num) > 1:
            duplicates.append(num)
    return duplicates

def is_safe(report):
    monotonic = strictly_monotonic(report)
    if not monotonic:
        return False
    if len(duplicate_found(report)) > 0:
        return False
    if len(find_unstable(report)) > 0:
        return False
    return True

def part_one(datafile: str):
    safe_count = 0
    report_data = load_data(datafile)
    for line in report_data:
        if is_safe(line):
            safe_count += 1
    print(f"part 1: {safe_count=}")

def part_two(datafile: str):
    safe = 0
    report_data = load_data(datafile)
    ic(len(report_data))

    def report_is_safe(seq, safe_range):
        for i in range(1, len(seq)):
            if seq[i] - seq[i-1] not in safe_range:
                return False
        return True    
    
    increasing = range(1, 4)
    decreasing = range(-3, 0)
    for line in report_data:
        safe += any(
            report_is_safe(line[:i] + line[i+1:], safe_range) 
            for safe_range in (increasing, decreasing)
            for i in range(len(line)) 
        )
    
    print(f"part 2: {safe=}")    


if __name__ == "__main__":
    part_one(INPUT_FILE)  # 624
    part_two(INPUT_FILE)  # 651 <-- too low!
    # 655 <-- wrong
    # 673 <-- wrong
    # 833 <-- too high
