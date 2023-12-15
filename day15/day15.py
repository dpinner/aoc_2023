import sys
from typing import List, Dict,Tuple
from collections import OrderedDict

def hash(step):
    val = 0
    for c in step:
        val += ord(c)
        val *= 17
        val %= 256
    return val

def sum_instructions(steps: List[str]) -> int:
    return sum(hash(step) for step in steps)

def perform_step(step: str, boxes: OrderedDict) -> None:
    if step[-1] == '-':
        label = step[:-1]
        idx = hash(label)
        if label in boxes[idx]:
            boxes[idx].pop(label)
    else:
        label,f = step.split('=')
        idx = hash(label)
        boxes[idx][label] = int(f)

def focusing_power(steps: List[str]) -> int:
    boxes = [OrderedDict() for _ in range(256)]
    for step in steps:
        perform_step(step, boxes)

    power = 0
    for i,box in enumerate(boxes):
        j = 1
        for _,f in box.items():
            power += (i+1)*(j)*f
            j += 1
    return power



if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        steps = f.read().splitlines()[0].split(',')
    print(sum(hash(step) for step in steps))
    print(focusing_power(steps))
