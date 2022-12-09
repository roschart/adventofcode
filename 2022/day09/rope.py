from dataclasses import dataclass
from enum import Enum



class Direction(Enum):
    R="R"
    L="L"
    U="U"
    D="D"

@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    
Points=set[Point]

@dataclass
class Move:
    direction: Direction
    steps: int

def read_move(line:str)-> Move:
    d, s= line.split(" ")
    return Move(Direction[d], int(s))

def in_touch(H:Point,T:Point)->bool:
    if abs(H.x - T.x) > 1:
        return False
    if abs(H.y -T.y) > 1:
        return False
    return True

def move_tail(H:Point,T:Point)->Point:
    x=T.x
    y=T.y
    if not in_touch(H,T):
        if H.x>T.x:
            x+=1
        if H.x<T.x:
            x-=1
        if H.y>T.y:
            y+=1
        if H.y<T.y:
            y-=1   
    return Point(x,y)

def execute_move(move:Move, H:Point, T:Point,  visited:Points)->tuple[ Point, Point, Points]:
    if move.direction==Direction.R:
        H=Point(H.x+1,H.y)
        T=move_tail(H,T)
    if move.direction==Direction.L:
        H=Point(H.x-1,H.y)
        T=move_tail(H,T)
    if move.direction==Direction.U:
        H=Point(H.x,H.y+1)
        T=move_tail(H,T)
    if move.direction==Direction.D:
        H=Point(H.x,H.y-1)
        T=move_tail(H,T)
    visited.add(T)
    if move.steps>1:
        H,T,visited=execute_move(Move(move.direction,move.steps-1), H, T, visited)
    return H, T, visited

def app(filename:str)->int:
    visited: Points=set([Point(0,0)])
    H=Point(0,0)
    T=Point(0,0)
    with open(filename,mode='r') as file: 
        for line in file.readlines():
            line=line.strip()
            move:Move=read_move(line)
            H, T, visited =execute_move(move, H, T, visited)
            print(f"after {line}")
            print(visited)
            print("---------")
    print(f"Visited= {visited}")
    return len(visited)
            
if __name__=="__main__":
    e1=app("day09/example")
    if e1!= 13:
        raise ValueError(f"Visit positions {e1} incoorrect for the example data")
    
    i1=app("day09/input")
    print(f"Visit points {i1}")