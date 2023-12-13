import sys
from functools import lru_cache

# def is_valid(s,sizes):
#     counts = []
#     in_block = False
#     for c in s:
#         if c == '#' and in_block:
#             counts[-1] += 1
#         elif c == '#':
#             counts.append(1)
#             in_block = True
#         else:
#             in_block = False
#     return counts == sizes

@lru_cache(maxsize=None)
def combinatorics(s,sizes,i,j,cur_size):
    if i == len(s):
        if (
            (j == len(sizes) and cur_size == 0) or 
            (j == len(sizes)-1 and cur_size == sizes[-1])
        ):
            return 1
        return 0
    
    if s[i] == '#':
        # add one to the current size, stay in the block
        return combinatorics(s,sizes,i+1,j,cur_size+1)
    
    if s[i] == '.' and cur_size > 0:
        # end the current block and move to the next one
        return (
            combinatorics(s,sizes,i+1,j+1,0) 
            if j < len(sizes) and cur_size == sizes[j] 
            else 0
            )
    
    if s[i] == '.':
        # cur_size == 0, just keep moving
        return combinatorics(s,sizes,i+1,j,0)
        
    # s[i] == '?', try both things
    return (
        combinatorics(s, sizes,i+1, j, cur_size+1) + 
        (
            combinatorics(s,sizes,i+1,j+1,0) 
            if j < len(sizes) and cur_size == sizes[j] 
            else 0
        ) + 
        (combinatorics(s,sizes,i+1,j,0) if cur_size == 0 else 0)
        )


def sum_combinatorics(filename: str, folded: bool) -> int:
    tot = 0
    with open(filename, "r") as f:
        for line in f:
            s,sizes = line.split()
            sizes = tuple(int(x) for x in sizes.split(','))
            if folded:
                sizes *= 5
                s = ((s+'?')*5)[:-1] # remove trailing '?'
            tot += combinatorics(s,sizes,0,0,0)
            combinatorics.cache_clear()
    return tot


if __name__ == "__main__":
    filename = sys.argv[1]
    print(sum_combinatorics(filename, False))
    print(sum_combinatorics(filename, True))
