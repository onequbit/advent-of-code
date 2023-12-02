#!/usr/bin/env python
from os.path import abspath, dirname, join
INPUT_FILE_NAME = join(dirname(abspath(__file__)),'input.txt')

def get_elves():
    all_calories = None
    with open(INPUT_FILE_NAME, mode='r') as input_file:
        all_calories = input_file.readlines()

    all_calories = [calories.strip() for calories in all_calories]

    for index, calories in enumerate(all_calories):
        if calories == '':
            all_calories[index] += '~'

    all_calories_str = ','.join(all_calories)
    all_calories = all_calories_str.split(',~,')
    all_calories = [calories.split() for calories in all_calories]

    elves = []
    for calories in all_calories:
        food = [int(item) for item in calories[0].split(',')]
        elves.append(sum(food))
    return elves

def get_top_elves(count:int):
    elves = get_elves()
    sorted_elves = sorted(elves, reverse=True)
    return sorted_elves[:count]


