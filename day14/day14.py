import sys
import re
from collections import deque
from typing import List

_cache = {}

def transpose(pattern):
    return [''.join(z) for z in zip(*pattern)]

def tilt_west(pattern, reverse=False):
    rows = [None]*len(pattern)
    peek = -1 if reverse else 0
    step = -1 if reverse else 1
    for j,row in enumerate(pattern):
        rocks = deque([m.start() for m in re.finditer(r'O',row)])
        blocks = deque([m.start() for m in re.finditer(r'\#',row)])
        new_row = ['.']*len(row)
        i = len(row)-1 if reverse else 0
        while rocks:
            if (
                blocks and 
                (
                    (reverse and rocks[peek] < blocks[peek]) or 
                    (not reverse and rocks[peek] > blocks[peek])
                )
            ):
                if blocks[peek] == i:
                    _ = blocks.pop() if reverse else blocks.popleft()
                    new_row[i] = '#'
                i += step
                continue
            _ = rocks.pop() if reverse else rocks.popleft()
            new_row[i] = 'O'
            i += step
    
        while blocks:
            block = blocks.pop() if reverse else blocks.popleft()
            new_row[block] = '#'
        rows[j] = ''.join(new_row)

    return rows

def tilt_east(pattern):
    return tilt_west(pattern, reverse=True)

def tilt_north(pattern):
    return transpose(tilt_west(transpose(pattern)))

def tilt_south(pattern):
    return transpose(tilt_east(transpose(pattern)))

def cycle(pattern):
    return tilt_east(tilt_south(tilt_west(tilt_north(pattern))))


def get_load(pattern: List[str]) -> int:
    load = 0
    num_rows = len(pattern)
    for i,row in enumerate(pattern):
        load += (num_rows-i)*len(re.findall(r'O',row))
    return load

def spin(pattern: List[str], cycles: int) -> int:
    _cache[tuple(pattern)] = 0
    for i in range(cycles):
        pattern = tuple(cycle(pattern))
        if pattern in _cache:
            break
        _cache[pattern] = i

    rem_cycles = (cycles - _cache[pattern]-1) % (i - _cache[pattern])
    for i in range(rem_cycles):
        pattern = cycle(pattern)
    return pattern


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        pattern = f.read().splitlines()
    print(get_load(tilt_north(pattern)))
    print(get_load(spin(pattern,1000000000)))
