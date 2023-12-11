from enum import Enum
from typing import Dict, Set, Tuple
import sys

example1 = "10/example1"
example2 = "10/example2"
example3 = "10/example3"
example4 = "10/example4"
example5 = "10/example5"
example6 = "10/example6"
input = "10/input"
file = input


Coord = Tuple[int, int]
Map = Dict[Coord, str]


class Direction(Enum):
    N = (-1, 0)
    S = (1, 0)
    W = (0, -1)
    E = (0, 1)


# The directions if from perspective can came form move to
from_dir: Dict[str, Set[Direction]] = {
    "|": {Direction.N, Direction.S},
    "-": {Direction.E, Direction.W},
    "L": {Direction.S, Direction.W},
    "J": {Direction.S, Direction.E},
    "7": {Direction.N, Direction.E},
    "F": {Direction.N, Direction.W},
    ".": set(),
    "S": set()
}

# The directions if from perspective can came form move to
pipe_next: Dict[str, Set[Direction]] = {
    "|": {Direction.N, Direction.S},
    "-": {Direction.E, Direction.W},
    "L": {Direction.N, Direction.E},
    "J": {Direction.N, Direction.W},
    "7": {Direction.S, Direction.W},
    "F": {Direction.S, Direction.E},
    ".": set(),
    "S": {Direction.N, Direction.S, Direction.E, Direction.W}
}


def print_map(map: Map, path: Set[Coord], x: int, y: int):
    for i in range(x):
        for j in range(y):
            if (i, j) in path:
                print(f"\033[31m{map[(i,j)]}\033[0m", end="")
            else:
                print(map[(i, j)], end="")
        print()


def get_loop(map: Map, init: Coord) -> Set[Coord]:
    path: Set[Coord] = set([init])
    current = init
    while True:
        nexts: Set[Coord] = set()
        for d in pipe_next[map[current]]:
            neighbor: Coord = (current[0]+d.value[0], current[1]+d.value[1])
            if neighbor in map.keys():
                if d in from_dir[map[neighbor]]:
                    nexts.add(neighbor)
        ns = len(nexts)
        if ns == 0 or ns > 2:
            print(
                f"Error in nexts={nexts}, "
                f"for curent {current}={map[current]}",
                file=sys.stderr)
            raise Exception

        s: Set[Coord] = nexts-path
        if len(s) == 0:
            return path
        path = path.union(s)
        current = s.pop()


def traped(map: Map, path: Set[Coord], x: int, y: int) -> Set[Coord]:
    ts: Set[Coord] = set()
    for i in range(x):
        out = True
        openborder = ""
        for j in range(y):
            k = (i, j)
            v = map[k]
            if k in path:
                if v == "|":
                    out = not out
                elif v == "F":
                    openborder = "F"
                elif v == "L":
                    openborder = "L"
                elif v == "7":
                    if openborder == "L":
                        out = not out
                elif v == "J":
                    if openborder == "F":
                        out = not out

            if not out and k not in path:
                map[k] = "I"
                ts.add(k)
            elif k not in path:
                map[k] = "O"
    return ts


diagram = [line.strip() for line in open(file)]
rows = len(diagram)
columns = len(diagram[0])


map: Map = {(r, c): v for r, row in enumerate(diagram)
            for c, v in enumerate(row)}

init: Coord = next(k for k, v in map.items() if v == "S")

loop = get_loop(map, init)

s = len(loop)/2


for line in diagram:
    print(line)
print("----")
print_map(map, loop, rows, columns)


if file == example1 and s != 4:
    raise Exception(f"{s}")

if file == example2 and s != 8:
    raise Exception(f"{s}")

if file == input and s != 6907:
    raise Exception(f"{s}")


# Replace init
ns: Set[Direction] = set()
for d in Direction:
    neighbor: Coord = (init[0]+d.value[0], init[1]+d.value[1])
    if neighbor in map.keys():
        if d in from_dir[map[neighbor]]:
            ns.add(d)


if ns == set([Direction.S, Direction.E]):
    map[init] = "F"
elif ns == set([Direction.S, Direction.W]):
    map[init] = "7"
else:
    raise Exception(f"{ns} not ready")

ts = traped(map, loop, rows, columns)

s2 = len(ts)
if file == example3 and s2 != 4:
    raise Exception(f"{s2}")

if file == example4 and s2 != 4:
    raise Exception(f"{s2}")

if file == example5 and s2 != 8:
    raise Exception(f"{s2}")

if file == example6 and s2 != 10:
    raise Exception(f"{s2}")

if file == input and s2 != 541:
    raise Exception(f"{s2}")


print("----")
print_map(map, loop, rows, columns)
