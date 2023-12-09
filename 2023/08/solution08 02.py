from dataclasses import dataclass
from typing import Dict, List
import math


@dataclass
class Next:
    L: str
    R: str


Map = Dict[str, Next]


file = "08/input"
data = [lines.strip() for lines in open(file)]
moves = data[0]


map: Map = dict()
for line in data[2:]:
    k = line[:3]
    L = line[7:10]
    R = line[12:15]
    map[k] = Next(L, R)


def get_currents() -> List[str]:
    currents: List[str] = []
    for k in map.keys():
        if k[-1] == "A":
            currents.append(k)
    return currents


def check_end(currents: List[str]) -> bool:
    for current in currents:
        if current[-1] != "Z":
            return False
    return True


currents = get_currents()
solutions: List[int] = []
for current in currents:
    count = 0
    cont = True
    while cont:
        for m in moves:
            count += 1
            if m == "L":
                current = map[current].L
            else:
                current = map[current].R
        if current[-1] == "Z":
            solutions.append(count)
            cont = False

s = math.lcm(*solutions)

if file == "08/example3" and s != 6:
    print(solutions)
    print(s)
    raise Exception

if file == "08/input" and s != 12833235391111:
    print(solutions)
    print(s)
    raise Exception
