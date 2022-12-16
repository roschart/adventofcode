from enum import Enum
from dataclasses import dataclass


class State(Enum):
    REST = 0
    FALLING = 1
    END = 2


class Terrain(Enum):
    EMPTY = "."
    ROCK = "#"
    SAND = "o"
    INIT = "+"


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int


Points = dict[Point, Terrain]


@dataclass
class Map:
    _points: Points
    _deep: int
    
    def deep(self)->int:
        if self._deep!=0:
            return self._deep
        else:
            ys = [k.y for k in self._points]
            self._deep = max(ys)+2
            return self._deep
            

    def get(self, p: Point) -> Terrain:
        if p.y >= self.deep():
            return Terrain.ROCK
        if p in self._points:
            return self._points[p]
        return Terrain.EMPTY

    def set(self, p: Point, t: Terrain) -> None:
        if self.get(p) != Terrain.EMPTY:
            raise ValueError(f"Can not put {t.value} in {p}")
        self._points[p] = t

    def generate_row(self, fm: Point, to: Point) -> None:
        points: Points = dict()
        if fm.x == to.x:
            for i in range(min(fm.y, to.y), max(fm.y, to.y)+1):
                points[Point(fm.x, i)] = Terrain.ROCK
        elif fm.y == to.y:
            for i in range(min(fm.x, to.x), max(fm.x, to.x)+1):
                points[Point(i, fm.y)] = Terrain.ROCK
        else:
            raise ValueError(f"Incorrect row {fm}->{to}")
        self._points.update(points)

    def print(self) -> None:
        self._points[INIT] = Terrain.INIT
        xs = [k.x for k in self._points]
        ys = [k.y for k in self._points]
        xmin = min(xs)
        ym = min(ys)
        xrange = max(xs)-min(xs)+1
        for j in range(self.deep()-min(ys)):
            for i in range(xrange):
                if not Point(i+xmin, j+ym) in self._points:
                    print(Terrain.EMPTY.value, end="")
                else:
                    print(self._points[Point(i+xmin, j+ym)].value, end="")
            print()
        print(Terrain.ROCK.value*xrange)


INIT = Point(500, 0)


def app(filename: str) -> int:
    lines: list[str] = []
    with open(filename, mode='r') as file:
        lines = [line.strip() for line in file.readlines()]
    map = generate_map(lines)
    count = 0
    state: State = State.REST
    p = INIT
    while state != State.END:
        if state == State.REST:
            count += 1
            p = INIT
            state, p = move(map, p)
        elif state == State.FALLING:
            state, p = move(map, p)

    map.print()
    return count


def generate_map(scans: list[str]) -> Map:
    map = Map(dict(), 0)
    for scan in scans:
        ls = scan.split(" -> ")
        for i in range(len(ls)-1):
            x1, y1 = [int(x) for x in ls[i].split(",")]
            x2, y2 = [int(x) for x in ls[i+1].split(",")]
            map.generate_row(Point(x1, y1), Point(x2, y2))
    return map


def move(map: Map, p: Point) -> tuple[State, Point]:
    down = Point(p.x, p.y+1)
    t = map.get(down)
    if t == Terrain.EMPTY:
        return State.FALLING, down
    left = Point(p.x-1, p.y+1)
    t = map.get(left)
    if t == Terrain.EMPTY:
        return State.FALLING, left
    right = Point(p.x+1, p.y+1)
    t = map.get(right)
    if t == Terrain.EMPTY:
        return State.FALLING, right
    if p == INIT:
        return State.END, INIT
    map.set(p, Terrain.SAND)
    return State.REST, INIT


if __name__ == "__main__":
    r = app("day14/example")
    if r != 93:
        raise ValueError(f"{r} is no valid for the puzzle 1 example")
    r = app("day14/input")
    if r != 27539:
        raise ValueError(f"{r} is no valid for the puzzle 1 input")
    r = app("day14/input")
