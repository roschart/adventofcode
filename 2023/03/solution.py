from typing import List, Tuple, Dict
from enum import Enum, auto


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



def neighbors(sch: schema, row:int, init: int, end: int)->Dict[Tuple[int,int],str]:
    result: Dict[Tuple[int,int],str]=dict()
    coors=[[row-1,x] for x in range(init-1,end+1)]
    coors+=[[row,init-1]]+[[row,end]]
    coors+=[[row+1,x] for x in range(init-1,end+1)]
    for coor in coors:
        r=coor[0]
        c=coor[1]
        if r >= 0 and r < len(sch) and c >= 0 and c < len(sch[0]):
            result[(r,c)]=sch[r][c]
    return result

def validate(sch: schema, row:int, init: int, end: int) -> Tuple[bool,Dict[Tuple[int,int],List[int]]]:
     
    coors=[[row-1,x] for x in range(init-1,end+1)]
    coors+=[[row,init-1]]+[[row,end]]
    coors+=[[row+1,x] for x in range(init-1,end+1)]
    
    ns=neighbors(sch, row, init, end)
    posible_gears:Dict[Tuple[int,int],List[int]]=dict()
    good=False
    for k,v in ns.items():
        if not v.isdigit() and v!=".":
            good=True
        if v=="*":
            posible_gears[k]=posible_gears.get(k, []) + [int(sch[row][init:end])]
    return (good,posible_gears)
        
def wrapper_validate(sch: schema, row:int, init: int, end: int, resume:bool=False):
    gears:Dict[Tuple[int,int],List[int]]=dict()
    if init:
        return True
    return 2
    
  

def get_numbers(sch: schema, row: int) -> List[int]:
    line = sch[row]
    state = State.NO_NUMBER
    number = ""
    init=0
    end=0
    result=[]
    for column in range(len(line)):
        v = line[column]
        if state == State.NO_NUMBER:
            if v.isdigit():
                state = State.GETTING_NUMBER
                number += v
                init=column
                continue
        if state == State.GETTING_NUMBER:
            if not v.isdigit():
                end=column
                if validate(sch,row,init,end)[0]:
                    result.append(int(number))
                state=State.NO_NUMBER
                number=""
                continue
            if v.isdigit():
                number += v
                if column==len(line)-1:
                    end=column
                    if validate(sch,row,init,end)[0]:
                        result.append(int(number))
                        # state=State.NO_NUMBER
                        # number=""
                continue
            if validate(sch,row,init,end)[0]:
                result.append(int(number))
            state=State.NO_NUMBER
            number=""
    return result


def solution(filename:str)->int:
    sch = read_schema(filename)
    total=0
    for r in range(len(sch)):
        numbers=get_numbers(sch,r)
        total+=sum(numbers)
    return total

e1=solution("03/example")
expected=4361
if e1!=expected:
    raise Exception(f"In exaple 1!={expected}")


s1=solution("03/input")
expected=535078
if s1!=expected:
    raise Exception(f"Solution {s1}!={expected}")


sch = read_schema("03/input")
e1=0
for r in range(len(sch)):
    numbers=get_numbers(sch,r)
    e1+=sum(numbers)
