
from enum import Enum

Element=list['Element']|int

Pair=tuple[Element,Element]

class Order(Enum):
    L=-1
    E=0
    R=1
    
def app(filename: str) -> int:
    lines:list[str]=[]
    left:list[int]=[]
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

if __name__ == "__main__":
    # check("[]",[])
    # check("[[]]",[])
    # print("All checks passed")
    
    r = app("day13/example")
    if r!=13:
        raise ValueError(f"{r} is not correct in the example")
    r=app("day13/input")
    print(f"The solutio puzzle 1 is= {r}")
    
