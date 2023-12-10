#!/usr/bin/env python3

import sys
from advent_of_code import load_input_lines

COLORS = ['blue', 'green', 'red']
TEST_COUNTS = {'blue': 14, 'green':13, 'red': 12}

class CubeGameRound:
    def __init__(self, src_rounds:str):
        rounds = src_rounds.split(';')
        self.rounds = [game_round.split() for game_round in rounds]

class CubeGame:
    def __init__(self, src_line:str):
        self.source = src_line
        [game_number, rounds_str] = src_line.split(':')
        self._id = int(game_number.replace("Game ",""))
        self.rounds = [round.strip() for round in rounds_str.split(';')]
        self.counts = { 'blue':0, 'green':0, 'red':0 }
        for round in self.rounds:
            samples = round.split(', ')
            for sample in samples:
                count, color = sample.split(' ')
                if int(count) > self.counts[color]:
                    self.counts[color] = int(count)

    def __repr__(self):
        return str({
                    # 'source': self.source,
                    'number': self._id,
                    'blues': self.counts['blue'],
                    'greens': self.counts['green'],
                    'reds': self.counts['red']
                })
        
    def is_possible(self, stats:dict) -> bool:
        for color in stats:
            if self.counts[color] > stats[color]:
                return False
        return True
    
    def power(self):
        red = self.counts['red']
        blue = self.counts['blue']
        green = self.counts['green']
        return red * blue * green

def parse_game(game_line:str):
    return CubeGame(game_line)

if __name__ == "__main__":
    lines = load_input_lines(sys.argv[1])
    ids = []
    powers = []
    for line in lines:
        game = CubeGame(line)
        print(line)
        print(CubeGame(line))
        if game.is_possible({'red':12,'green':13,'blue':14}):
            ids.append(game._id)
        powers.append(game.power())
    print(sum(ids), sum(powers))
