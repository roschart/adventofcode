import re
from typing import Iterator, List


def next(secuences: List[List[int]]) -> int:
    n = 0
    for s in secuences[-2::-1]:
        a = s[-1]
        n += a
    return n


def previous(secuences: List[List[int]]) -> int:
    n = 0
    for s in secuences[-2::-1]:
        a = s[0]
        n = a - n
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
file = input
row_data = [lines.strip() for lines in open(file)]

reports = [[int(num) for num in re.findall(r"-?\d+", line)]
           for line in row_data]

history = list(generate(reports))
n = sum(next(s) for s in history)
p = sum(previous(s) for s in history)
if file == example and n != 114:
    raise Exception

if file == example and p != 2:
    raise Exception(f"{p}")

if file == input and n != 1993300041:
    raise Exception(f"{n}")

if file == input and p != 1038:
    raise Exception(f"{p}")
