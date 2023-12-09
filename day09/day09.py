import sys

def extrapolate(series):
    stack = [series]
    if all((v == 0 for v in stack[-1])):
        return 0
    while any((v != 0 for v in stack[-1])):
        stack.append([b-a for a,b in zip(stack[-1],stack[-1][1:])])
    delta = stack.pop()[-1]
    while len(stack) > 1:
        stack[-1].append(stack[-1][-1] + delta)
        delta = stack.pop()[-1]
    return stack[-1][-1] + delta


def sum_extrapolate(filename: str, prefix: bool) -> int:
    tot = 0
    with open(filename, "r") as f:
        for line in f:
            l = line.rstrip()
            if not l:
                continue
            tot += extrapolate([int(v) for v in l.split()][::(-1)**prefix])
        return tot


if __name__ == "__main__":
    filename = sys.argv[1]
    print(sum_extrapolate(filename, False))
    print(sum_extrapolate(filename, True))
