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
        
    def radio(self)->int:
        return distance(self.sesor,self.beacon)


def distance(a: Point, b: Point) -> int:
    x = abs(a.x-b.x)
    y = abs(a.y-b.y)
    return x+y


def app(filiename: str) -> int:
    lines: list[str] = []
    with open(filiename, mode='r') as file:
        lines = [l.strip() for l in file.readlines()]
    pairs = generate_pairs(lines)
    left= min([p.sesor.x-p.radio() for p in pairs])
    right= max([c.sesor.x+c.radio() for c in pairs])
    return not_present_row(y=10, left=left, right=right,pairs=pairs)

def not_present_row(y:int, left:int, right:int, pairs:list[Pair])->int:
    count:int=0
    for x in range(left,right+1):
        if in_radius_of_some(Point(x,y),pairs):
            count+=1
    return count

def in_radius_of_some(p:Point, circles:list[Pair])->bool:
    for c in circles:
        if distance(p,c.sesor)<=c.radio():
            return True
    return False


def generate_pairs(lines: list[str]) -> list[Pair]:
    pattern = r"-?\d+"
    return [Pair(Point(int(a),int(b)),Point(int(c),int(d))) for a,b,c,d in [re.findall(pattern, l) for l in lines]]


if __name__ == "__main__":
    r = app("day15/example")
    if r != 26:
        raise ValueError(f"Value {r} nod valid for example puzzle 1")
    print("hello")
