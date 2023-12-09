from dataclasses import dataclass
from typing import Dict


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


current = "AAA"
count = 0
while current != "ZZZ":
    for m in moves:
        count += 1
        if m == "L":
            current = map[current].L
        else:
            current = map[current].R

if file == "08/example1" and count != 2:
    raise Exception

if file == "08/example2" and count != 6:
    raise Exception

if file == "08/input" and count != 21883:
    raise Exception(f"c={count}")
