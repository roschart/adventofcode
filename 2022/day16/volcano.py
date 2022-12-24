from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
import re

Id = str

@dataclass
class Node:
    id: Id
    rate: int
    next: list[Id] = field(default_factory=list)

    def open(self) -> None:
        self.__open = True

class Action(Enum):
    Move = 0
    Open = 1


class State:
    nodes: dict[Id, Node]
    pending: set[Id]
    last_action: Action
    postion: Id
    timer: int
    free: int
    potential: int
    parent: Id

    def current(self) -> Node:
        return self.nodes[self.postion]

    def next_states(self) -> list['State']:
        c = self.current()
        ns: list[State] = []
        # You can alwasy move but not if is previous one
        for n in c.next:
            if n != self.last_position:
                ns.append(self.move(n))
        if c.id in self.pending and c.rate > 0 and self.last_action == Action.Move:
            ns.append(self.open())
        return ns

    def __init__(self,     nodes: dict[Id, Node],
                 pending: set[Id],
                 last_action: Action,
                 postion: Id,
                 timer: int,
                 free: int,
                 potential: int,
                 last_postion: Id) -> None:
        self.nodes = nodes
        self.pending = pending
        self.last_action = last_action
        self.postion = postion
        self.timer = timer
        self.free = free
        self.last_position=last_postion

        if potential == 0:
            pending_rates = [self.nodes[id].rate for id in pending]
            pending_rates.sort(reverse=True)
            self.potential = sum(
                [a*b for a, b in zip(pending_rates, range(timer-1, -1, -2))])
        else:
            self.potential = potential

    def open(self) -> 'State':
        c = self.current()
        pending = set(self.pending)
        pending.remove(self.postion)
        pending_rates = [self.nodes[id].rate for id in pending]
        pending_rates.sort(reverse=True)
        free = c.rate*(self.timer-1)
        potencial = self.free + free+sum(
            [a*b for a, b in zip(pending_rates, range(self.timer-3, -1, -2))])
        return State(self.nodes, pending, Action.Open, self.postion, self.timer-1, self.free+free, potencial,self.postion)

    def move(self, id: Id) -> 'State':
        c = self.current()
        pending = set(self.pending)
        pending_rates = [self.nodes[id].rate for id in pending]
        pending_rates.sort(reverse=True)
        timer = self.timer-2
        potencial = self.free + sum(
            [a*b for a, b in zip(pending_rates, range(timer, -1, -2))])
        return State(self.nodes, pending, Action.Move, id, self.timer-1, self.free, potencial,self.postion)

    def __repr__(self) -> str:
        return f"{{{self.last_action}[{self.postion}], {self.pending},t={self.timer}, f={self.free}, p={self.potential}}}"


def get_best(xs: list[State]) -> State:
    potential: Callable[[State], int] = lambda s: s.potential
    xs.sort(key=potential)
    return xs.pop()


def find(init: State)->int:
    open = init.next_states()
    i=-1
    while open:
        i+=1
        cs = get_best(open)
        if i%1000==0:
            print(f"best {i}: {cs}, l_open={len(open)}")

        ns = cs.next_states()
        for n in ns:
            open.append(n)
            open = [o for o in open if o.potential > n.free]
            if not open:
                return n.free
    raise ValueError("Bad end of while loop")


def puzzle1(filename:str)->int:
    nodes: dict[Id, Node]=dict()
    pending: set[Id]=set()
    first:str=""
    with open(filename, mode='r') as file:
        for line  in file.readlines():
            n,p= process_line(line.strip())
            nodes[n.id]=n
            pending=pending.union(p)
            if first=="":
                first=n.id
    INIT= State(nodes,pending,Action.Move,first,30,0,0,first)
    return find(INIT)

def process_line(line:str)-> tuple[Node, set[Id]]:

    pattern = r"\d+"
    matches = re.findall(pattern, line)
    rate=int(matches[0])
    
    pattern=r"[A-Z]{2}"
    matches = re.findall(pattern, line)
    id=matches[0]
    s:set[Id]=set()
    if rate>0:
        s.add(id)
    n= Node(id,rate,next=list(matches[1:]))
    return n,s  
    
if __name__=="__main__":
    r=puzzle1("day16/example")
    if r!=1651:
        raise ValueError(f"Presión libreada {r} es incorrecta en puzzle1 example")
    r=puzzle1("day16/input")
    if r<=1613:
        raise ValueError(f"Presión libreada {r} es incorrecta en puzzle1 imput")
    print("fin")
# a = Node('a', 5)
# b = Node('b', 20)
# c = Node ('c', 15)
# a.next = [b.id]
# b.next = [a.id,c.id]
# c.next = [b.id]

# INIT = State({a.id: a, b.id: b, c.id:c}, {a.id, b.id, c.id}, Action.Move, a.id, 30, 0)
# print("----------------")
# print(f"INIT={INIT}")
# s=find(INIT)
# print(f"solución={s}")