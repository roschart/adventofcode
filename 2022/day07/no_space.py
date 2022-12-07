from typing import Any
from dataclasses import dataclass

@dataclass
class Element:
    type: str
    name: str
    size: int
    content: Any
    parent: Any

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
def get_dirs_at_most(ele:Element, most:int, acc:list[int])->list[int]:
    if ele.type=="dir":
        if ele.size<most:
            acc.append(ele.size)
        for e in ele.content:
            acc=get_dirs_at_most(e, most, acc)
    return acc
    
    
def app(filename:str)->tuple[int]:
    directory:Element=Element("dir", "/", -1, [], None)
    with open(filename, mode = 'r') as file:
        lines=file.readlines()
        for line in lines:
            line=line.strip()
            directory=process_line(directory,line)
            print(line)
    parent=process_line(directory, "$ cd /")
    calculate_sizes(parent)
    print_dir(parent)
    r=get_dirs_at_most(parent,100000,[])
    print(r)   
    
    return (sum(r),)

if __name__ == "__main__":
    e1,=app("day07/example")
    if e1!=95437:
        raise ValueError("{e1}!=95437 for example")
    i1,=app("day07/input")
    print(f"solucion 1= {i1}")