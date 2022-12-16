from enum import Enum

class State(Enum):
    rest = 0
    falling = 1
    end = 2


Point = tuple[int, int]
Map = dict[Point, str]
INIT = (500,0) 


def app(filename: str) -> int:
    lines: list[str] = []
    with open(filename, mode='r') as file:
        lines = [line.strip() for line in file.readlines()]
    map = generate_map(lines)
    print_map(map)
    count=-1
    state:State=State.rest
    p=INIT
    while state!=State.end:
        if state==State.rest:
            count+=1
            p=INIT
            state,p=move(map,p)
        elif state== State.falling:
            state,p=move(map,p)    

    print_map(map)
    return count

def move(map:Map, p:Point)->tuple[State,Point]:
    x, y = p
    if not (x, y+1) in map:
        return State.end, INIT
    if map[x, y+1]=='.':
        return State.falling, (x,y+1)
    if not (x-1, y+1) in map:
        return State.end, INIT
    if  map[x-1, y+1]=='.':
        return State.falling,(x-1,y+1) 
    if not (x+1, y+1) in map:
        return State.end, INIT
    if map[x+1, y+1]=='.':
        return State.falling,(x+1,y+1)
    map[x,y]="o"
    return State.rest,INIT
            
def generate_map(scans: list[str]) -> Map:
    map: Map = dict()
    print()
    for scan in scans:
        ls = scan.split(" -> ")
        for i in range(len(ls)-1):
            x1, y1 = [int(x) for x in ls[i].split(",")]
            x2, y2 = [int(x) for x in ls[i+1].split(",")]
            map.update(generate_row(x1, y1, x2, y2))
    return map


def generate_row(x1: int, y1: int, x2: int, y2: int) -> Map:
    map: Map = dict()
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2)+1):
            map[(x1, i)] = "#"
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2)+1):
            map[(i, y1)] = "#"
    else:
        raise ValueError(f"Incorrect row {(x1,y1)}->{(x2,y2)}")
    return map


def print_map(map: Map) -> None:
    map[INIT] = "+"
    xs = [x for x,  _ in [k for k in map]]
    ys = [y for _,  y in [k for k in map]]
    xm = min(xs)
    ym = min(ys)
    for j in range(max(ys)-min(ys)+1):
        for i in range(max(xs)-min(xs)+1):
            if not (i+xm, j+ym) in map:
                map[(i+xm, j+ym)]="."
            print(map[(i+xm, j+ym)], end="")
        print()


if __name__ == "__main__":
    r = app("day14/example")
    if r != 24:
        raise ValueError(f"{r} is no valid for the puzzle 1 example")
    r = app("day14/input")
    if r != 838:
        raise ValueError(f"{r} is no valid for the puzzle 1 example")
    r = app("day14/input")
   

