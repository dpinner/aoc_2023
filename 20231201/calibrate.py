import sys, getopt

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


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.val = None
        self.counter = 0
        self.children = {}


class Trie:
    def __init__(self, val_map, suffix=False):
        self.root = TrieNode("")
        self.vals = val_map
        for k in val_map.keys():
            self.insert(k, suffix)

    def insert(self, word, suffix):
        node = self.root

        w = reversed(word) if suffix else word

        for char in w:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.val = self.vals.get(word, 0)

    def query(self, x):
        node = self.root

        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return (False, None)
        return (True, node.val)


def calibrate(*args):
    filename = args[0]
    string_mode = bool(args[1]) if len(args) > 1 else False
    tot = 0
    trie = Trie(ext_string_map if string_mode else string_map)
    suff_trie = Trie(ext_string_map, True) if string_mode else trie
    with open(filename, "r") as f:
        for line in f:
            l = line.rstrip()
            if not l:
                continue
            first, last = None, None
            prefixes = set()
            suffixes = set()
            for i in range(len(l)):
                if first is None:
                    next_level = set()
                    prefixes.add("")
                    while prefixes:
                        p = prefixes.pop()
                        contained, val = trie.query(p + l[i])
                        if val is not None:
                            first = val
                            break
                        if contained:
                            next_level.add(p + l[i])
                    if first is not None and last is not None:
                        break
                    prefixes = next_level
                if last is None:
                    next_level = set()
                    suffixes.add("")
                    while suffixes:
                        s = suffixes.pop()
                        contained, val = suff_trie.query(s + l[-(i + 1)])
                        if val is not None:
                            last = val
                            break
                        if contained:
                            next_level.add(s + l[-(i + 1)])
                    if first is not None and last is not None:
                        break
                    suffixes = next_level
            tot += int(str(first) + str(last))
    return tot


if __name__ == "__main__":
    print(calibrate(*sys.argv[1:]))
