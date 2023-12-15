import sys
from typing import List, Dict,Tuple
from collections import deque

def hash(step):
    val = 0
    for c in step:
        val += ord(c)
        val *= 17
        val %= 256
    return val

def sum_instructions(steps: List[str]) -> int:
    return sum(hash(step) for step in steps)

def perform_step(
        step: str, 
        boxes: List[deque], 
        focal_lengths: Dict[Tuple[int,str],str]
    ) -> None:
    remove = step[-1] == '-'
    if remove:
        label = step[:-1]
        f = None
    else:
        label,f = step.split('=')
    idx = hash(label)
    if remove and (idx,label) in focal_lengths:
        boxes[idx].remove(label)
        del focal_lengths[(idx,label)]
    elif not remove:
        if (idx,label) not in focal_lengths:
            boxes[idx].append(label)
        focal_lengths[(idx,label)] = f

def focusing_power(steps: List[str]) -> int:
    boxes = []
    for _ in range(256):
        # deque is secretly a doubly linked list
        boxes.append(deque([]))
    focal_lengths = {}
    for step in steps:
        perform_step(step, boxes, focal_lengths)

    power = 0
    for i,box in enumerate(boxes):
        for j,label in enumerate(box):
            power += (i+1)*(j+1)*int(focal_lengths[(i,label)])
    return power



if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        steps = f.read().splitlines()[0].split(',')
    print(sum(hash(step) for step in steps))
    print(focusing_power(steps))
