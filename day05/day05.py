import sys
from typing import List

# a & b
def intersection(a: tuple, b: tuple) -> tuple:
    return (max(a[0],b[0]), min(a[1],b[1]))

def is_empty(a: tuple) -> bool:
    return a[0] >= a[1]

# a - b
def remove(a: tuple, b: tuple) -> List[tuple]:
    if is_empty(intersection(a,b)):
        return [a]
    return [(a[0],b[0]),(b[1],a[1])]

class SeedMap:

    def __init__(self):
        self.maps = []

    def get_value(self, input):
        if isinstance(input, tuple) or isinstance(input,list):
            return self.get_values(input)
        for value_start, range_start, range_len in self.maps:
            if input >= range_start and input < range_start + range_len:
                return value_start + (input - range_start)
        return input
    
    def get_values(self, input):
        inputs = [input] if isinstance(input,tuple) else input
        remainders = []
        outputs = []

        for value_start, range_start, range_len in self.maps:
            for ival in inputs:
                if is_empty(ival):
                    continue
                x = intersection((range_start, range_len+range_start), ival)
                if is_empty(x):
                    remainders.append(ival)
                    continue
                remainders += remove(ival, x)
                outputs.append((value_start + x[0] - range_start, value_start + x[1] - range_start))
                
            inputs = remainders
            remainders = []
        return outputs + inputs       




def get_smallest_loc(filename: str, seed_ranges: bool) -> int:
    maps = {
        "seed-to-soil": SeedMap(), 
        "soil-to-fertilizer": SeedMap(), 
        "fertilizer-to-water":  SeedMap(), 
        "water-to-light": SeedMap(), 
        "light-to-temperature": SeedMap(), 
        "temperature-to-humidity": SeedMap(), 
        "humidity-to-location": SeedMap()
    }
    seeds = []
    category = None
    with open(filename, "r") as f:
        for line in f:
            l = line.rstrip()
            if not l:
                continue
            if len(l.split(":")) > 1:
                category = l.split(":")[0].split()[0]
                if category == "seeds":
                    seeds = [int(x) for x in l.split(":")[1].split()]
                    if seed_ranges:
                        seeds = list(zip(seeds[::2], seeds[1::2]))
                        seeds = [(a,a+b) for a,b in seeds]
                continue
            maps[category].maps.append([int(x) for x in l.split()])
    locations = [
        maps["humidity-to-location"].get_value(
        maps["temperature-to-humidity"].get_value(
        maps["light-to-temperature"].get_value(
        maps["water-to-light"].get_value(
        maps["fertilizer-to-water"].get_value(
        maps["soil-to-fertilizer"].get_value(
        maps["seed-to-soil"].get_value(seed)
        )))))) for seed in seeds]
    return min([loc[0] for locs in locations for loc in locs]) if seed_ranges else min(locations)


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_smallest_loc(filename, False))
    print(get_smallest_loc(filename, True))
