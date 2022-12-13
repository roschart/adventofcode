from dataclasses import dataclass
from enum import Enum

Element=list['Element']|int

@dataclass
class CompElemnt:
    value:Element
    def __lt__(self, other):
        if compare(self.value,other.value)==Order.L:
            return True
        return False

Pair=tuple[Element,Element]

class Order(Enum):
    L=-1
    E=0
    R=1
    
def puzzle1(filename: str) -> int:
    left:list[int]=[]
    lines:list[str]=[]
    with open(filename, mode='r') as file:
        lines = [line.strip() for line in file.readlines()]
    for i in range(len(lines)//3+1):
        l,r=read_pair(lines[i*3:i*3+2])
        c=compare(l,r)
        if c==Order.L:
            left.append(i+1)
    return sum(left)

def compare(a:Element, b:Element)->Order:
    if type(a)==int and type(b)==int:
        if a < b:
            return Order.L
        elif a>b:
            return Order.R
        else:
            return Order.E
    elif type(a)==list and type(b)==list:
        for x, y in zip(a,b):
            r=compare(x,y)
            if r==Order.L or r==Order.R:
                return r
        if len(a)<len(b):
            return Order.L
        elif len(a)>len(b):
            return Order.R
        return Order.E
    elif type(a)==int and type(b)==list:
        return compare([a],b)
    elif type(a)==list and type(b)==int:
        return compare(a,[b])
    raise ValueError(f"Comparation bad implemented {a}, {b}")

def check_compare(a:Element,b:Element,c:Order):
    r=compare(a,b)
    if r!=c:
        raise ValueError(f"Error comparation: {a} {b} -> {c}")
check_compare(1,2,Order.L)
check_compare(2,2,Order.E)
check_compare(3,2,Order.R)
check_compare([],[1], Order.L)
check_compare([1],[], Order.R)
check_compare([1,2],[1,3], Order.L)
check_compare([1,4],[1,3], Order.R)
check_compare([1,2],1,Order.R)

def read_pair(lines:list[str])->Pair:
    if(len(lines)!=2):
        raise ValueError(f"The is not two lines in list")
    e1= eval(lines[0])
    e2= eval(lines[1])
    return e1, e2

# def parse_element(s:str)->tuple[Element,str]:
#     c=s[0]
#     tail=s[1:]
#     if c=="[":
#         xs:list[Element]=[]
#         n,s=parse_element(tail)
#         while n!=-1:
#             xs.append(n)
#             n,s=parse_element(s)
#         return xs, ""
#     elif c=="]":
#         return -1,tail
#     return 0,s


# def check(s:str,e:Element):
#     r,_=parse_element(s)
#     if(r!=e):
#         raise ValueError("Check fail: {r}!={e}")

def puzzle2(filename: str) -> int:
    lines:list[str]=[]
    packets:list[CompElemnt]=[]
    with open(filename, mode='r') as file:
        lines = [line.strip() for line in file.readlines()]
    for i in range(len(lines)//3+1):
        l,r=read_pair(lines[i*3:i*3+2])
        packets+=[CompElemnt(l),CompElemnt(r)]
    packets+=[CompElemnt([[2]]),CompElemnt([[6]])]
    packets.sort()
    
    index:list[int]=[]
    for i in range(len(packets)):
        v=packets[i]
        if v.value==[[2]] or v.value==[[6]]:
            index.append(i+1)        
    a,b=index    
    return a*b

if __name__ == "__main__":
    # check("[]",[])
    # check("[[]]",[])
    # print("All checks passed")
    
    r = puzzle1("day13/example")
    if r!=13:
        raise ValueError(f"{r} is not correct in the example")
    r=puzzle1("day13/input")
    print(f"The solution puzzle 1 is= {r}")
    
    r = puzzle2("day13/example")
    if r!=140:
        raise ValueError(f"{r} is not correct in puzzle 2 example")
    r=puzzle2("day13/input")
    print(f"The solution puzzle 2 is= {r}")
    
