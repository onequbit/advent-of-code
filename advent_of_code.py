#!/usr/bin/env python

from day1.elf_calories import get_elves, get_top_elves
from day2.roshambo import run_game_1, run_game_2

elves = get_elves()
top_elves = get_top_elves(3)
print(f"day 1a: {max(elves)}")
print(f"day 1b: {sum(top_elves)}")

game_score_1 = run_game_1()
print(f"day 2a: {sum(game_score_1)}")
game_score_2 = run_game_2()
print(f"day 2b: {sum(game_score_2)}")