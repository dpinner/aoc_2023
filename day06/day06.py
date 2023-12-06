import sys
from typing import List
import math 


def get_combos(filename: str, kern: bool) -> int:
    with open(filename, "r") as f:
        lines = [l.split(":")[-1].split() for l in f.read().splitlines()]
        races = zip(*[[''.join(l)] for l in lines]) if kern else zip(*lines)
        ways = 1
        for race in races:
            tmax = 0.5*int(race[0]) + 0.5*math.sqrt(int(race[0])**2 - 4*int(race[1]))
            tmax = int(tmax) if tmax - int(tmax) > 0 else int(tmax)-1
            tmin = int(0.5*int(race[0]) - 0.5*math.sqrt(int(race[0])**2 - 4*int(race[1])))+1
            ways *= (1+tmax-tmin)
        return ways


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_combos(filename, False))
    print(get_combos(filename, True))
