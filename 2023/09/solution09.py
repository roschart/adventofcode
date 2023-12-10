import re
from typing import Iterator, List


def nexts(secuences: List[List[int]]) -> int:
    n = 0
    for s in secuences[-2::-1]:
        a = s[-1]
        n += a
    return n


def generate(repots: List[List[int]]) -> Iterator[List[List[int]]]:
    for secuence in reports:
        secuences: List[List[int]] = [secuence]
        while not all(e == 0 for e in secuence):
            secuence = [b-a for a, b in zip(secuence, secuence[1:])]
            secuences.append(secuence)
        yield secuences


example = "09/example"
input = "09/input"
file = example
row_data = [lines.strip() for lines in open(file)]

reports = [[int(num) for num in re.findall(r"-?\d+", line)]
           for line in row_data]


s = sum(nexts(s) for s in generate(reports))
if file == example and s != 114:
    raise Exception

if file == input and s != 1993300041:
    raise Exception
