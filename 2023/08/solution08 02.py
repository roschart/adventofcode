from dataclasses import dataclass
from typing import Dict, List


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
count = 0
cont = True
while cont:
    for m in moves:
        count += 1
        if m == "L":
            for i, current in enumerate(currents):
                currents[i] = map[current].L
        else:
            for i, current in enumerate(currents):
                currents[i] = map[current].R
        if check_end(currents):
            cont = False
            break
if file == "08/example3" and count != 6:
    raise Exception

if file == "08/input" and count != 6:
    raise Exception(f"count={count}")

