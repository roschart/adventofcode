
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
        print (f"Monkey {id}:")
        for i in range(len(m.items)):
            e=m.items.pop(0)
            m.inspected+=1
            print(f"  Monkey inspects an item with a worry level of {e}.")
            e=m.opertion(e)
            print(f"    Worry level is {e}.")
            e=e//3
            print(f"    Monkey gets bored with item. Worry level is divided by 3 to {e}")
            div= e % m.test
            if div!=0:
                print(f"    Current worry level is not divisible by {m.test}.")
                print(f"    Item with worry level {e} is thrown to monkey {m.if_false}")
                monkesy[m.if_false].items.append(e)
            else:
                print(f"    Current worry level is divisible by {m.test}.")
                print(f"    Item with worry level {e} is thrown to monkey {m.if_true}")
                monkesy[m.if_true].items.append(e)
            
def app(filename:str)->int:
    lines:list[str]=[]
    monkeys:Monkeys=dict()
    with open(filename, mode='r') as file:
        lines=[l.strip() for l in file.readlines()]
    for i in range((len(lines)+1)//7):
        m=Monkey.from_lines(lines[i*7:i*7+7])
        monkeys[m.id]=m
    for i in range(20):
        round(monkeys)
        print(f"After Round {i+1}")
        for id in range(len(monkeys)):
            print(f"Monkey {id}: {monkeys[id].items}")
    xs=[]
    for id in range(len(monkeys)):
        xs.append(monkeys[id].inspected)
        print(f"Monkey {id} inspected items {monkeys[id].inspected} times.")
    xs.sort()
    return xs[-2]*xs[-1]

if __name__=="__main__":
    r=app("day11/example")
    if r!=10605:
        raise ValueError(f"Bad response {r} for the example")
    r=app("day11/input")
    print(F"El valor del puzzle 1 es {r}")