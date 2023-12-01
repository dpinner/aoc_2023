import sys
from typing import Dict, Optional

string_map = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 0,
}

ext_string_map = {
    **string_map,
    **{
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    },
}

def str2bool(v):
  return v.lower() in {"y", "yes", "true", "t", "1"}


class TrieNode:
    char: str
    val: Optional[int]
    children: Dict[str, "TrieNode"]

    def __init__(self, char: str):
        self.char = char
        self.val = None
        self.children = {}


class Trie:
    root: TrieNode
    vals: Dict[str, int]
    suffix: bool

    def __init__(self, val_map: Dict[str, int], suffix: bool):
        self.root = TrieNode("")
        self.vals = val_map
        self.suffix = suffix

        for k in val_map.keys():
            self.insert(k)

    def insert(self, word: str) -> None:
        node = self.root

        w = reversed(word) if self.suffix else word

        for char in w:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.val = self.vals.get(word, 0)

    def query(self, x: str, start: Optional[TrieNode] = None) -> Optional[TrieNode]:
        node = start or self.root

        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node

def parse_line(l: str, trie: Trie, suff_trie: Trie) -> int:
    first, last = None, None
    prefix_nodes = set()
    suffix_nodes = set()
    i = 0
    while first is None or last is None:
        next_level = set()
        prefix_nodes.add(trie.root)

        while prefix_nodes and first is None:
            n = prefix_nodes.pop()
            child = trie.query(l[i],start=n)
            if child is not None:
                first = child.val
                next_level.add(child)

        prefix_nodes = next_level
        next_level = set()
        suffix_nodes.add(suff_trie.root)

        while suffix_nodes and last is None:
            n = suffix_nodes.pop()
            child = suff_trie.query(l[-(i + 1)], start=n)
            if child is not None:
                last = child.val
                next_level.add(child)

        suffix_nodes = next_level
        i += 1
    return int(str(first) + str(last))


def calibrate(filename: str, string_mode: bool) -> int:
    tot = 0
    trie = Trie(ext_string_map if string_mode else string_map, False)
    suff_trie = Trie(ext_string_map, True) if string_mode else trie
    with open(filename, "r") as f:
        for line in f:
            l = line.rstrip()
            if not l:
                continue
            tot += parse_line(line, trie, suff_trie)
    return tot


if __name__ == "__main__":
    filename = sys.argv[1]
    string_mode = str2bool(sys.argv[2]) if len(sys.argv) > 2 else False
    print(calibrate(filename, string_mode))
