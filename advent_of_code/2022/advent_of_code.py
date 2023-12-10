#!/usr/bin/env python

from day1.elf_calories import get_elves, get_top_elves
from day2.roshambo import run_game_1, run_game_2
from day3.rucksack_reorg import find_mispacked, get_badges
from day4.overlap_pairs import count_alloverlaps, count_fullycontained
from day5.stack_moving import find_stackresults, find_newstackresults
from day6.tuning_trouble import start_marker, message_marker

elves = get_elves()
top_elves = get_top_elves(3)
print(f"day 1a: {max(elves)}")
print(f"day 1b: {sum(top_elves)}")

game_score_1 = run_game_1()
print(f"day 2a: {sum(game_score_1)}")
game_score_2 = run_game_2()
print(f"day 2b: {sum(game_score_2)}")

print(f"day 3a: {find_mispacked()}")
print(f"day 3b: {sum(get_badges())}")

print(f"day 4a: {count_fullycontained()}")
print(f"day 4b: {count_alloverlaps()}")

print(f"day5a: {find_stackresults()}")
print(f"day5b: {find_newstackresults()}")

print(f"day 6a: {start_marker()}")
print(f"day 6b: {message_marker()}")
