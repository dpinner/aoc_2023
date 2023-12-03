import sys
import re

def is_valid(match, f_array, i):
    symbol = r'((?!\d|\.).)+'
    begin = max(match.start()-1,0)
    return (
        (re.search(symbol, f_array[i][begin:match.end()+1]) is not None) or
        (i > 0 and re.search(symbol, f_array[i-1][begin:match.end()+1]) is not None) or
        (i < len(f_array)-1 and re.search(symbol, f_array[i+1][begin:match.end()+1]) is not None)
        )

def get_sum(filename: str) -> int:
    tot = 0
    with open(filename, "r") as f:
        f_array = f.read().splitlines()
    for i in range(len(f_array)):
        for match in re.finditer(r'\d+', f_array[i]):
            if is_valid(match, f_array, i):
                tot += int(match.group())
    return tot


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_sum(filename))
