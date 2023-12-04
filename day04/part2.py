import sys
import math


def get_score(filename: str) -> int:
    with open(filename, "r") as f:
        games = f.read().splitlines()
        num_cards = [1]*len(games)
        for i,game in enumerate(games):
            card = game.split(":")[-1]
            want,have = (set(int(x) for x in g.split()) for g in card.split("|"))
            matches = len(want & have)
            for j in range(1,matches+1):
                num_cards[i+j] += num_cards[i]
    return sum(num_cards)


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_score(filename))
