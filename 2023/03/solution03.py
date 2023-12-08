from typing import Callable, Dict, List, Tuple
from enum import Enum, auto

import math as m
import re


schema = List[str]


def read_schema(filename: str) -> schema:
    sc: schema = []
    with open(filename, "r") as f:
        for l in f:
            sc.append(l.strip())
    return sc


class State(Enum):
    NO_NUMBER = auto()
    GETTING_NUMBER = auto()
    VALIDATING = auto()
    VALID = auto()


def neighbors(sch: schema, row: int, init: int,
              end: int) -> Dict[Tuple[int, int], str]:
    result: Dict[Tuple[int, int], str] = dict()
    coors = [[row - 1, x] for x in range(init - 1, end + 1)]
    coors += [[row, init - 1]] + [[row, end]]
    coors += [[row + 1, x] for x in range(init - 1, end + 1)]
    for coor in coors:
        r = coor[0]
        c = coor[1]
        if r >= 0 and r < len(sch) and c >= 0 and c < len(sch[0]):
            result[(r, c)] = sch[r][c]
    return result


def wrapper_validate(func: Callable[[schema,
                                     int,
                                     int,
                                     int],
                                    Tuple[bool,
                                          Dict[Tuple[int,
                                                     int],
                                               int]]]) -> Callable[[schema,
                                                                    int,
                                                                    int,
                                                                    int],
                                                                   Tuple[bool,
                                                                         Dict[Tuple[int,
                                                                                    int],
                                                                              List[int]]]]:
    def inner(sch: schema, row: int, init: int, end: int,
              gears: bool = False) -> Tuple[bool, Dict[Tuple[int, int], List[int]]]:
        v = False
        if not gears:
            v, g = func(sch, row, init, end)
            for k, value in g.items():
                inner.gears[k] = inner.gears.get(k, []) + [value]
        return (v, inner.gears)
    inner.gears: Dict[Tuple[int, int], List[int]] = dict()
    return inner


@wrapper_validate
def validate(sch: schema, row: int, init: int,
             end: int) -> Tuple[bool, Dict[Tuple[int, int], int]]:

    coors = [[row - 1, x] for x in range(init - 1, end + 1)]
    coors += [[row, init - 1]] + [[row, end]]
    coors += [[row + 1, x] for x in range(init - 1, end + 1)]

    ns = neighbors(sch, row, init, end)
    posible_gears: Dict[Tuple[int, int], int] = dict()
    good = False
    for k, v in ns.items():
        if not v.isdigit() and v != ".":
            good = True
        if v == "*":
            posible_gears[k] = int(sch[row][init:end])
    return (good, posible_gears)


validate.gears: Dict[Tuple[int, int], List[int]] = dict()


def get_numbers(sch: schema, row: int) -> List[int]:
    line = sch[row]
    state = State.NO_NUMBER
    number = ""
    init = 0
    end = 0
    result = []
    for column in range(len(line)):
        v = line[column]
        if state == State.NO_NUMBER:
            if v.isdigit():
                state = State.GETTING_NUMBER
                number += v
                init = column
                continue
        if state == State.GETTING_NUMBER:
            if not v.isdigit():
                end = column
                if validate(sch, row, init, end)[0]:
                    result.append(int(number))
                state = State.NO_NUMBER
                number = ""
                continue
            if v.isdigit():
                number += v
                if column == len(line) - 1:
                    end = column
                    if validate(sch, row, init, end + 1)[0]:
                        result.append(int(number))
                continue
            if validate(sch, row, init, end)[0]:
                result.append(int(number))
            state = State.NO_NUMBER
            number = ""
    return result


def solution(filename: str) -> int:
    sch = read_schema(filename)
    total = 0
    for r in range(len(sch)):
        numbers = get_numbers(sch, r)
        total += sum(numbers)
    return total


def solution2(filename: str) -> int:
    validate.gears = dict()
    sch = read_schema(filename)
    for r in range(len(sch)):
        get_numbers(sch, r)
    total = 0
    n_ast = sum([l.count('*') for l in sch])
    if len(validate.gears) != n_ast:
        raise Exception(f"len gears {len(validate.gears)} != {n_ast}")
    for c, ns in validate.gears.items():
        if len(ns) == 2:
            a, b = ns
            total += a * b
    return total

# e1=solution("03/example")
# expected=4361
# if e1!=expected:
#     raise Exception(f"In exaple 1!={expected}")


# s1=solution("03/input")
# expected=535078
# if s1!=expected:
#     raise Exception(f"Solution {s1}!={expected}")


# sch = read_schema("03/input")
# e1=0
# for r in range(len(sch)):
#     numbers=get_numbers(sch,r)
#     e1+=sum(numbers)

e2 = solution2("03/example")
expected = 467835
if e2 != expected:
    raise Exception(f"In exaple 1!={expected}")

s2 = solution2("03/input")
expected = 75312571
if s2 != expected:
    raise Exception(f"In exaple s2 !={expected}")
