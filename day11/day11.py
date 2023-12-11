import sys
import re

def num_steps(filename: str, exp: int) -> int:
    galaxies = []
    with open(filename, "r") as f:
        map = f.read().splitlines()
        empty_rows = set(range(len(map)))
        empty_cols = set(range(len(map[0])))
    for i,r in enumerate(map):
        new_gals = [(i,m.start()) for m in re.finditer(r'\#',r)]
        if len(new_gals) > 0:
            empty_rows.remove(i)
        empty_cols -= {c for _,c in new_gals}
        galaxies += new_gals

    steps = 0
    for i,g1 in enumerate(galaxies):
        for g2 in galaxies[i+1:]:
            r0,r1 = min(g1[0],g2[0]), max(g1[0],g2[0])
            c0,c1 = min(g1[1],g2[1]), max(g1[1],g2[1])
            steps += (
                r1-r0 + 
                c1-c0 +
                (exp-1)*len(set(range(r0+1, r1)) & empty_rows) + 
                (exp-1)*len(set(range(c0+1,c1)) & empty_cols)
                )
    return steps


if __name__ == "__main__":
    filename = sys.argv[1]
    print(num_steps(filename, 2))
    print(num_steps(filename, 1000000))
