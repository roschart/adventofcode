import re
from typing import List


def extrapolate(secuences: List[List[int]]) -> int:
    n = 0
    for s in secuences[-2::-1]:
        a = s[-1]
        n += a
    return n


def nexts(repots: List[List[int]]) -> List[int]:
    nexts: List[int] = []
    for secuence in reports:
        secuences: List[List[int]] = [secuence]
        while not all(e == 0 for e in secuence):
            secuence = [b-a for a, b in zip(secuence, secuence[1:])]
            secuences.append(secuence)

        nexts.append(extrapolate(secuences))
    return nexts


example = "09/example"
file = example
row_data = [lines.strip() for lines in open(file)]

reports = [[int(num) for num in re.findall(r"-?\d+", line)]
           for line in row_data]

s = sum(nexts(reports))
if file == example and s != 114:
    raise Exception

print(s)
