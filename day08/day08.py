import sys
import math

class Node:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right

def count_steps(directions, nodes, start_node, ghost_mode):
    ptr = 0
    node = start_node
    count = 0
    def finished(n):
        return node.val[-1] == 'Z' if ghost_mode else node.val == 'ZZZ'
    while not finished(node):
        node = nodes[node.left] if directions[ptr] == 'L' else nodes[node.right]
        ptr = ptr + 1 if ptr < len(directions)-1 else 0
        count += 1
    return count

def num_steps(filename: str, ghost_mode: bool) -> int:
    nodes = {}
    with open(filename, "r") as f:
        directions = f.readline().rstrip()
        for line in f:
            l = line.rstrip()
            if not l:
                continue
            val, children = l.split('=')
            left,right = children.split(',')
            nodes[val.strip()] = Node(val.strip(), left.strip().strip('('), right.strip().strip(')'))
        start_nodes = [node for v,node in nodes.items() if v[-1] == 'A'] if ghost_mode else [nodes['AAA']]
        counts = [count_steps(directions, nodes, start, ghost_mode) for start in start_nodes]
        return math.lcm(*counts)


if __name__ == "__main__":
    filename = sys.argv[1]
    print(num_steps(filename, False))
    print(num_steps(filename, True))
