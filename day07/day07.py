import sys

rank = {
    'A':14,
    'K':13,
    'Q':12,
    'J':11,
    'T':10,
    '9':9,
    '8':8,
    '7':7,
    '6':6,
    '5':5,
    '4':4,
    '3':3,
    '2':2,
    'j':1
    }

def score(hand, joker):
    counts = {}
    if joker:
        # jacks are wild
        hand[0] = hand[0].replace('J','j')
    for card in hand[0]:
        counts[card] = counts.get(card,0)+1
    cards_by_count = sorted(counts,key=counts.get, reverse=True)
    # most frequent non-joker
    max_key = (
        cards_by_count[0] 
        if cards_by_count[0] != 'j' or len(cards_by_count) == 1 
        else cards_by_count[1]
        )
    # don't double-add jokers
    joker_count = counts.get('j',0) if max_key != 'j' else 0
    score = [counts[max_key]+joker_count,0] + [rank[c] for c in hand[0]]
    if score[0] in [2,3]:
        # deal with full house and 2 pair
        # get count of second most frequent non-joker
        next_key = cards_by_count[1] if 'j' not in cards_by_count[:2] else cards_by_count[2]
        score[1] = counts[next_key]
    return score

def get_winnings(filename: str, joker: bool) -> int:
    winnings = 0
    with open(filename, "r") as f:
        hands = [l.split() for l in f.read().splitlines()]
        sorted_hands = sorted(hands, key=lambda h: score(h,joker))
        for i,h in enumerate(sorted_hands):
            winnings += (i+1)*int(h[1])
    return winnings


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_winnings(filename, False))
    print(get_winnings(filename, True))
