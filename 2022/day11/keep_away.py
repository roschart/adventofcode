
from dataclasses import dataclass
from typing import Callable

@dataclass
class Monkey:
    id: int
    items: list[int]
    opertion: Callable[[int], int]
    test: int
    if_true: int
    if_false: int
    inspected: int = 0
    
    @staticmethod
    def from_lines(lines:list[str])->'Monkey':
        id=int(lines[0][7])
        items= [int(x) for x in lines[1][16:].split(", ")]
        operation=None
        if lines[2].split(" ")[-1] == "old":
            operation=(lambda a: a+a) if "+" in lines[2] else (lambda a: a*a)
        else:
            x =int(lines[2].split(" ")[-1])
            operation=(lambda a: a+x ) if "+" in lines[2] else (lambda a: a*x)
        test =int(lines[3].split(" ")[-1])
        if_true =int(lines[4].split(" ")[-1])
        if_false =int(lines[5].split(" ")[-1])
        return Monkey(id,items,operation,test,if_true,if_false)
    

           
Monkeys= dict[int,Monkey]

def round(monkesy:Monkeys):
    for id in range(len(monkesy)):
        m=monkesy[id]
        for i in range(len(m.items)):
            e=m.items.pop(0)
            m.inspected+=1
            e=m.opertion(e)
            e=e//3
            div= e % m.test
            if div!=0:
                monkesy[m.if_false].items.append(e)
            else:
                monkesy[m.if_true].items.append(e)
            
def app(filename:str)->int:
    lines:list[str]=[]
    monkeys:Monkeys=dict()
    with open(filename, mode='r') as file:
        lines=[l.strip() for l in file.readlines()]
    for i in range((len(lines)+1)//7):
        m=Monkey.from_lines(lines[i*7:i*7+7])
        monkeys[m.id]=m
    xs:list[int]=[]
    for i in range(20):
        xs=[]
        round(monkeys)
    print(f"After Round {i+1}")
    for id in range(len(monkeys)):
        xs.append(monkeys[id].inspected)
        print(f"Monkey {id} inspected items {monkeys[id].inspected} times.")
    xs.sort()
    return xs[-2]*xs[-1]




@dataclass
class Item:
    values:dict[int,int]
    
    @staticmethod
    def from_str(s:str)->'Item':
        i=int(s)
        primes=[2,3,5,7, 11, 13,17,19,23]
        v={p:i%p for  p in primes}
        return Item(v)
    def add(self, x:int)->'Item':
        return Item({k:(v +x)%k for k, v in self.values.items()})
    def mul(self, x:int)->'Item':
        return Item({k:(v * x)%k for k, v in self.values.items()})
    def square (self )->'Item':
        return Item({k:(v * v)%k for k, v in self.values.items()})
    def is_divisible_by(self,v:int)->bool:
        return self.values[v]==0
         

@dataclass
class Monkey2:
    id: int
    items: list[Item]
    opertion: str
    test: int
    if_true: int
    if_false: int
    inspected: int = 0
    
    @staticmethod
    def from_lines(lines:list[str])->'Monkey2':
        id=int(lines[0][7])
        items= [Item.from_str(x) for x in lines[1][16:].split(", ")]
        operation=lines[2]
        test =int(lines[3].split(" ")[-1])
        if_true =int(lines[4].split(" ")[-1])
        if_false =int(lines[5].split(" ")[-1])
        return Monkey2(id,items,operation,test,if_true,if_false)

Monkeys2= dict[int,Monkey2]

def round2(monkeys2:Monkeys2):
    for id in range(len(monkeys2)):
        m=monkeys2[id]
        for j in range(len(m.items)):
            i=m.items.pop(0)
            m.inspected+=1
            if "+" in m.opertion:
                x =int(m.opertion.split(" ")[-1])
                i= i.add(x)
            elif "old * old" in m.opertion:
                i=i.square() 
            elif "*" in m.opertion:
                x =int(m.opertion.split(" ")[-1])
                i= i.mul(x)
            else:
                raise ValueError(f"No valid operation {m.opertion}")
            
            if i.is_divisible_by(m.test):
                monkeys2[m.if_true].items.append(i)
            else:
                monkeys2[m.if_false].items.append(i)    
    
def app2(filename:str)->int:
    lines:list[str]=[]
    monkeys2:Monkeys2=dict()
    with open(filename, mode='r') as file:
        lines=[l.strip() for l in file.readlines()]
    for i in range((len(lines)+1)//7):
        m=Monkey2.from_lines(lines[i*7:i*7+7])
        monkeys2[m.id]=m
    for i in range(10000):
        round2(monkeys2)
    xs=[]
    for id in range(len(monkeys2)):
        xs.append(monkeys2[id].inspected)
        print(f"Monkey {id} inspected items {monkeys2[id].inspected} times.")
    xs.sort()
    return xs[-2]*xs[-1]

    
if __name__=="__main__":
    r=app("day11/example")
    if r!=10605:
        raise ValueError(f"Bad response {r} for the example")
    r=app2("day11/example")
    if r!=2713310158:
        raise ValueError(f"Bad response {r} for the example 2")    
    r=app("day11/input")
    print(F"El valor del puzzle 1 es {r}")
    r=app2("day11/input")
    print(F"El valor del puzzle 2 es {r}")
    