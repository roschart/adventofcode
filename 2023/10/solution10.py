from enum import Enum
from typing import Dict, Set, Tuple
import sys

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


def print_map(map: Map, path: Set[Coord], x, y):
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


example1 = "10/example1"
example2 = "10/example2"
input = "10/input"
file = input

diagram = [line.strip() for line in open(file)]
rows = len(diagram)
columns = len(diagram[0])


map: Map = {(r, c): v for r, row in enumerate(diagram)
            for c, v in enumerate(row)}

init: Coord = next(k for k, v in map.items() if v == "S")


loop = get_loop(map, init)

for line in diagram:
    print(line)
print("----")
print_map(map, loop, rows, columns)

s = len(loop)/2

if file == example1 and s != 4:
    raise Exception(f"{s}")

if file == example2 and s != 8:
    raise Exception(f"{s}")


if file == input and s != 0:
    raise Exception(f"{s}")

