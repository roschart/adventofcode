from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    R = "R"
    L = "L"
    U = "U"
    D = "D"


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int


Points = set[Point]
Rope = list[Point]


@dataclass
class Move:
    direction: Direction
    steps: int


def read_move(line: str) -> Move:
    d, s = line.split(" ")
    return Move(Direction[d], int(s))


def in_touch(H: Point, T: Point) -> bool:
    if abs(H.x - T.x) > 1:
        return False
    if abs(H.y - T.y) > 1:
        return False
    return True


def move_tail(H: Point, T: Point) -> Point:
    x = T.x
    y = T.y
    if not in_touch(H, T):
        if H.x > T.x:
            x += 1
        if H.x < T.x:
            x -= 1
        if H.y > T.y:
            y += 1
        if H.y < T.y:
            y -= 1
    return Point(x, y)


def execute_move(move: Move, rope: Rope,  visited: Points) -> tuple[Rope, Points]:
    H = rope[0]
    if move.direction == Direction.R:
        H = Point(H.x+1, H.y)
    if move.direction == Direction.L:
        H = Point(H.x-1, H.y)
    if move.direction == Direction.U:
        H = Point(H.x, H.y+1)
    if move.direction == Direction.D:
        H = Point(H.x, H.y-1)

    rope[0] = H
    for i in range(len(rope)-1):
        rope[i+1] = move_tail(rope[i], rope[i+1])
    visited.add(rope[-1])
    if move.steps > 1:
        rope, visited = execute_move(
            Move(move.direction, move.steps-1), rope, visited)

    return rope, visited


def app(filename: str, size_rope: int) -> int:
    rope = []
    for i in range(size_rope):
        rope.append(Point(0, 0))
    visited: Points = set([Point(0, 0)])
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line = line.strip()
            move: Move = read_move(line)
            rope, visited = execute_move(move, rope, visited)
    return len(visited)


if __name__ == "__main__":
    e1 = app("day09/example",2)
    if e1 != 13:
        raise ValueError(
            f"Visit positions {e1} incoorrect for the example data")
    e1 = app("day09/example", 10)
    if e1 != 1:
        raise ValueError(
            f"Visit positions {e1} incoorrect for the example data")
    e1 = app("day09/example2", 10)
    if e1 != 36:
        raise ValueError(
            f"Visit positions {e1} incoorrect for the example data")
    i1 = app("day09/input", 2)
    print(f"Visit points puzzle 1= {i1}")
    i1 = app("day09/input", 10)
    print(f"Visit points puzzle 2 = {i1}")
