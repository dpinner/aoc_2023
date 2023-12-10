import sys

deltas = {
    ('7',(0,1)): (1,0),
    ('7',(-1,0)): (0,-1),
    ('|', (-1,0)): (-1,0),
    ('|', (1,0)): (1,0),
    ('-', (0,1)): (0,1),
    ('-', (0,-1)): (0,-1),
    ('L', (1,0)): (0,1),
    ('L', (0,-1)): (-1,0),
    ('J', (0,1)): (-1,0),
    ('J', (1,0)): (0,-1),
    ('F', (-1,0)): (0,1),
    ('F', (0,-1)): (1,0),
}

def get_start_idx(map):
    for i,r in enumerate(map):
        j = r.find('S')
        if j != -1:
            return i,j
        
def first_step(map,i,j):
    if i > 0 and map[i-1][j] in {'7','F','|'}:
        return (i-1,j)
    if i < len(map)-1 and map[i+1][j] in {'J','L','|'}:
        return (i+1,j)
    if j > 0 and map[i][j-1] in {'L','-','F'}:
        return (i,j-1)
    if j < len(map[0])-1 and map[i][j+1] in {'J','-','7'}:
        return (i,j+1)
    
def replace_S(map, loop):
    for i,j in loop:
        if map[i][j] == 'S':
            break
    if (
        (i+1,j) in loop and 
        map[i+1][j] in {'L','|','J'} and 
        (i-1,j) in loop and 
        map[i-1][j] in {'7','|','F'}
    ):
        pipe = '|'
    elif (
        (i+1,j) in loop and 
        map[i+1][j] in {'L','|','J'} and 
        (i,j+1) in loop and 
        map[i][j+1] in {'J','-','7'}
    ):
        pipe = 'F'
    elif (
        (i+1,j) in loop and 
        map[i+1][j] in {'L','|','J'} and 
        (i,j-1) in loop and 
        map[i][j-1] in {'L','-','F'}
    ):
        pipe = '7'
    elif (
        (i,j+1) in loop and 
        map[i][j+1] in {'J','-','7'} and
        (i,j-1) in loop and 
        map[i][j-1] in {'L','-','F'}
    ):
        pipe = '-'
    elif (
        (i,j-1) in loop and 
        map[i][j-1] in {'L','-','F'} and
        (i-1,j) in loop and 
        map[i-1][j] in {'7','|','F'}
    ):
        pipe = 'J'
    else:
        pipe = 'L'
    
    map[i] = map[i][:j] + pipe + map[i][j+1:]
        

def get_loop(map):
    i0,j0 = get_start_idx(map)
    i,j = first_step(map,i0,j0)
    delta = (i-i0,j-j0)
    loop = {(i0,j0),(i,j)}
    while (i,j) != (i0,j0):
        delta = deltas[(map[i][j],delta)]
        i,j = (i+delta[0],j+delta[1])
        loop.add((i,j))
    return loop

def is_inside(map, loop, i,j):
    exit = None
    crossings = 0
    for p in loop[i]:
        if p[1] > j:
            continue
        pipe = map[p[0]][p[1]]
        if exit is None:
            crossings += 1
            if pipe == '7':
                exit = {'L': 0,'F': 1}
            if pipe == 'J':
                exit = {'L': 1, 'F': 0}
            continue

        if pipe not in exit:
            continue
        crossings += exit[pipe]
        exit = None
        
    return crossings % 2 == 1 # odd number of crossings means inside

def get_area(map,loop):
    replace_S(map, loop)
    sorted_loop = [[]]*len(map)
    for i in range(len(map)):
        sorted_loop[i] = sorted({p for p in loop if p[0] == i}, key = lambda p: p[1], reverse=True)
    inside_count = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if (i,j) in loop or i == 0 or j == 0 or i == len(map) or j == len(map[0]):
                continue
            if is_inside(map,sorted_loop,i,j):
                inside_count += 1
    return inside_count


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        map = f.read().splitlines()
    loop = get_loop(map)
    print(len(loop)//2)
    print(get_area(map,loop))
