import sys
from typing import Tuple

def transpose(pattern):
    return [''.join(z) for z in zip(*pattern)]

def get_sym_rows(pattern,exclude):
    potential_rows = []
    max_smudges = 0 if exclude is None else 1
    for i,pair in enumerate(zip(pattern,pattern[1:])):
        if i+1 == exclude:
            continue
        smudge_count = 0
        for j in range(len(pair[0])):
            if pair[0][j] != pair[1][j]:
                smudge_count += 1

        if smudge_count <= max_smudges:
            potential_rows.append((i+1,smudge_count))

    for row,s in potential_rows:
        max_val = 1+len(pattern)-row if row > len(pattern)//2 else row + 1
        smudge_count = s
        for i in range(2,max_val):
            for j in range(len(pattern[0])):
                if pattern[row+i-1][j] != pattern[row-i][j]:
                    smudge_count += 1
            if smudge_count > max_smudges:
                break
        if smudge_count <= max_smudges:
            return row
    return 0


def get_reflections(filename: str) -> Tuple[int,int]:
    no_smudge = 0
    smudge = 0
    patterns = [[]]
    with open(filename, "r") as f:
        for line in f:
            l = line.rstrip()
            if l:
                patterns[-1].append(l)
            else:
                patterns.append([])
    for pattern in patterns:
        r = get_sym_rows(pattern,None)
        c = get_sym_rows(transpose(pattern),None)
        no_smudge += 100*r
        no_smudge += c
        smudge += 100*get_sym_rows(pattern,r)
        smudge += get_sym_rows(transpose(pattern),c)
    return no_smudge,smudge


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_reflections(filename))
