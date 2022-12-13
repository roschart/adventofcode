from dataclasses import dataclass
import os
import time

@dataclass(unsafe_hash=True)
class Point: 
    r:int
    c:int

@dataclass()
class Node:
    v:str = ""
    g:int = 1440*420
    h:int = 1440*420
    parent:"Point|None" = None

Map = dict[Point,Node]

def read_map(lines:list[str])->tuple[Map, Point, Point]:
    map:Map=dict()
    start=Point(0,0)
    end=Point(0,0)
    for r in range(len(lines)):
        for c in range(len(lines[r])):
            n=Node(lines[r][c])
            point=Point(r,c)
            map[point]=n
            if n.v=="S":
                start=point
            if n.v=="E":
                end=point
    return map, start, end

def nexts(map:Map, point:Point)->set[Point]:
    up=Point(point.r-1,point.c)
    down=Point(point.r+1,point.c)
    left=Point(point.r,point.c-1)
    right=Point(point.r,point.c+1)
    next=set()
    v1=map[point].v
    if v1=="S":
        v1="a"
    for p in [up, down, left, right]:
        if p in map:
            v2=map[p].v
            if v2=="E":
                v2="z"
            if ord(v2)-ord(v1)<=1:
                next.add(p)
    return next
    

def distance(s:str)->int:
    if s=="S":
        s="a"
    if s=="E":
        s="z"
    return ord("z") - ord(s)

def red(s:str):
    return f"\033[91m{s}\033[00m"
    
def print_map(map:Map, current:Point, closed:set[Point]):
    time.sleep(0.2)
    os.system('clear')
    for r in range(41):
        print()
        for c in range(143):
            p=Point(r,c)
            s= map[p].v if p in map else ""
            printing=p
            if current==printing:
                s="X"
            if printing in closed:
                s=red(s)
            print(s, end="")
    print("\n------")
            

def get_path(map:Map, end:Point)->set[Point]:
    p:set[Point]=set([end])
    c= end
    while map[c].parent!=None:
        c=Point(map[c].parent.r, map[c].parent.c)
        p.add(c)
    return p
    
def get_least_cost(map:Map,opened:set[Point])->Point:
    e=sorted(opened,key=lambda p: map[p].g+map[p].h)[0]
    opened.remove(e)
    return e
     
def find_path(map:Map, start:Point, end:Point)->Point:
    map[start].h=distance(map[start].v)
    map[start].g=0
    opened:set[Point]=set([start])
    closed:set[Point]=set()
    while len(opened)>0:
        c=get_least_cost(map,opened)
        ns=nexts(map,c)
        for n in ns:
            if n==end:
                map[n].parent=c
                return n
            g=map[c].g+1
            h=distance(map[n].v)
            if n in opened:
                if map[n].g+map[n].h<g+h:
                    continue
            if n in closed:
                if map[n].g+map[n].h<g+h:
                    continue
          
            
            map[n].g=g
            map[n].h=h
            map[n].parent=c
            opened.add(n)
        closed.add(c)
        # if len(open)==0:
        #     print_map(map, c,closed)
    return end
def puzzle1(filename:str)->int:
    lines = read_file(filename)
    map,start,end = read_map(lines)
    return min_path_len(map, start, end)

def min_path_len(map, start, end):
    n=find_path(map, start, end)
    ph=get_path(map,n)
    return len(ph)-1

def read_file(filename:str)->list[str]:
    lines:list[str]=[]
    with open(filename,mode='r') as file:
        lines=[l.strip() for l in file.readlines()]
    return lines

def puzzle2(filename:str)->int:
    lines=read_file(filename)
    map,start,end=read_map(lines)
    solutions:set[int]=set()
    solutions.add(min_path_len(map, start, end))
    i:int=0
    for r in range(41):
        for c in range(143):
            p=Point(r,c)
            s= map[p].v if p in map else ""
            if s=="a":
                i+=1
                print(f"{i}: resolviendo para {p} ")
                map,start,end=read_map(lines)
                map[start].v="a"
                l=min_path_len(map,p,end)
                if l<29:
                    raise ValueError(f"Socion demasiado baja {l} para el punto {p}")
                solutions.add(l)
    result=sorted(solutions)[0]
    return result
    
if __name__=="__main__":
    r=puzzle1("day12/example")
    if r!= 31:
        raise ValueError(f"The number os steps {r} in not correct for the example")
    r=puzzle1("day12/input")
    if r!=468:
        raise ValueError(f"{r} is incorrect for imput")
    print(f"solution puzzle 1 is {r}")
    
    r=puzzle2("day12/example")   
    if r!= 29:
        raise ValueError(f"The number os steps {r} in not the minimun for the example") 
    r=puzzle2("day12/input") 
    print(f"solution puzzle 2 is {r}")
