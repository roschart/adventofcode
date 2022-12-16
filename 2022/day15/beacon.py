import re
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int


@dataclass
class Pair:
    sesor: Point
    beacon: Point

    def radio(self) -> int:
        return distance(self.sesor, self.beacon)


def distance(a: Point, b: Point) -> int:
    x = abs(a.x-b.x)
    y = abs(a.y-b.y)
    return x+y


def app(filiename: str,row:int) -> int:
    pairs = get_pairs_from_file(filiename)
    left = min([p.sesor.x-p.radio() for p in pairs])
    right = max([c.sesor.x+c.radio() for c in pairs])
    return not_present_row(y=row, left=left, right=right, pairs=pairs)

def app2(filiename: str, n:int) -> int:
    pairs = get_pairs_from_file(filiename)
    for y in range(n+1):
        x=0
        while x<=n:
            e,next= in_radius_of_some(Point(x,y),pairs)
            if e:
                x=next
            else:
                return x*4000000+y
            x+=1
        
    for y in range(n+1):
        for x in range(n+1):
            if not in_radius_of_some(Point(x,y),pairs):
                return x*4000000+y
        print(f"Linea {y} procesada")
    raise ValueError("app2 without solution")

def get_pairs_from_file(filiename)->list[Pair]:
    lines: list[str] = []
    with open(filiename, mode='r') as file:
        lines = [l.strip() for l in file.readlines()]
    pairs = generate_pairs(lines)
    return pairs


def not_present_row(y: int, left: int, right: int, pairs: list[Pair]) -> int:
    count: int = 0
    sensors = set((p.sesor for p in pairs))
    beacons = set((p.beacon for p in pairs))
    for x in range(left, right+1):
        if Point(x,y) in sensors:
            continue
        if Point(x,y) in beacons:
            continue
        b,_=in_radius_of_some(Point(x, y), pairs)
        if b:
            count += 1
    return count


def in_radius_of_some(p: Point, pairs: list[Pair]) -> tuple[bool,int]:

    for c in pairs:
        if distance(p, c.sesor) <= c.radio():
            d=p.x-c.sesor.x
            return True, c.sesor.x+d
    return False, 0


def generate_pairs(lines: list[str]) -> list[Pair]:
    pattern = r"-?\d+"
    return [Pair(Point(int(a), int(b)), Point(int(c), int(d))) for a, b, c, d in [re.findall(pattern, l) for l in lines]]


if __name__ == "__main__":
    r = app("day15/example",10)
    if r != 26:
        raise ValueError(f"Value {r} nod valid for example puzzle 1")
    r = app("day15/example",11)
    if r != 27:
        raise ValueError(f"Value {r} nod valid for example puzzle 1")
    r = app("day15/example",9)
    if r != 25:
        raise ValueError(f"Value {r} nod valid for example puzzle 1")
    r = app("day15/input",2000000)
    if r != 6124805:
        raise ValueError(f"Value {r} nod valid for example puzzle 1")
    
    # r=app2("day15/example",20)
    # if r!=56000011:
    #     raise ValueError(f"Value {r} nod valid for example puzzle 2")
    # r=app2("day15/input",4000000)
    # if r!=0:
    #     raise ValueError(f"Value {r} nod valid for example puzzle 2")
    # print("hello")
