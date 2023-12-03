import sys
import re

def get_ratio(match, f_array, i):
    nums = []
    for j in range(max(i-1,0),min(i+2,len(f_array))):
        sanitized = re.sub(r'\*','.',f_array[j])
        line = sanitized[:match.start()] + '*' + sanitized[match.start()+1:]
        match_one = re.search(r'\d+\*',line)
        match_two = re.search(r'\*\d+',line)
        if match_one is None and match_two is None:
            if f_array[j][match.start()].isdigit():
                nums.append(f_array[j][match.start()])
            continue
        start = match_one.start() if match_one is not None else match_two.start()
        end = match_two.end() if match_two is not None else match_one.end()
        nums += re.findall(r'\d+', f_array[j][start:end])
    return int(nums[0])*int(nums[1]) if len(nums) == 2 else 0


def get_sum(filename: str) -> int:
    tot = 0
    with open(filename, "r") as f:
        f_array = f.read().splitlines()
    for i in range(len(f_array)):
        for match in re.finditer(r'\*', f_array[i]):
            tot += get_ratio(match, f_array, i)
    return tot


if __name__ == "__main__":
    filename = sys.argv[1]
    print(get_sum(filename))
