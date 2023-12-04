import sys
import math


def get_score(filename: str) -> int:
    tot = 0
    with open(filename, "r") as f:
        for line in f:
            card = line.rstrip().split(":")[-1]
            want,have = tuple(set(int(x) for x in g.split()) for g in card.split("|"))
            matches = len(want & have)
            tot += math.floor(2**(matches-1))
    return tot


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_score(filename))
