from typing import Any, Callable
from dataclasses import dataclass



@dataclass
class Element:
    type: str
    name: str
    size: int
    content: Any
    parent: Any
    
Pred=Callable[[Element], bool]

def process_line(ele:Element, line:str)->Element:
    if line == "$ cd /":
        while ele.parent!=None:
            ele=ele.parent
        return ele
    elif line== "$ ls":
        pass
    elif line[:4]=="dir ":
        dirname= line[4:]
        ele.content.append(Element("dir",dirname,-1,[],ele))
    elif line[0].isdecimal():
        size,filename=line.split()
        ele.content.append(Element("file",filename,int(size),None,ele))
    elif line=="$ cd ..":
        return ele.parent
    elif line[:4]=="$ cd":
        name=line[5:]
        for e in ele.content:
            if e.type=="dir" and e.name==name:
                return e
        
    return ele

def print_dir(e:Element,t:str=""):
    print(f"{t}{e.type} {e.name} {e.size}")
    if(e.type=="dir"):
        for x in e.content:
            print_dir(x, t+ "  ")

def calculate_sizes(e:Element)->int:
    if e.type=="file":
        return e.size
    else:
        l= [calculate_sizes(x) for x in e.content]
        e.size=int(sum(l))
        return e.size 
def get_dirs_by(ele:Element, acc:list[int], fun:Pred)->list[int]:
    if ele.type=="dir":
        if fun(ele):
            acc.append(ele.size)
        for e in ele.content:
            acc=get_dirs_by(e, acc, fun)
    return acc
    
    
def app(filename:str)->tuple[int,int]:
    directory:Element=Element("dir", "/", -1, [], None)
    with open(filename, mode = 'r') as file:
        lines=file.readlines()
        for line in lines:
            line=line.strip()
            directory=process_line(directory,line)
    parent=process_line(directory, "$ cd /")
    calculate_sizes(parent)
    r1=get_dirs_by(parent,[],lambda e: e.size<100000)
    #puzzle 2
    total=70000000
    needed=30000000
    used=parent.size
    required=needed-(total-used)
    r2=get_dirs_by(parent,[],lambda e: e.size>=required)
    return (sum(r1),min(r2))

if __name__ == "__main__":
    e1,e2=app("day07/example")
    if e1!=95437:
        raise ValueError("{e1}!=95437 for example")
    if e2!=24933642:
        raise ValueError("{e2}!=exected for example")
    i1,i2=app("day07/input")
    print(f"solucion 1= {i1}")
    print(f"solucion 1= {i2}")