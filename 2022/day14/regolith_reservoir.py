
Point=tuple[int,int]
Map = dict[Point,str]

def app(filename:str)->int:
    lines:list[str]=[]
    with open(filename, mode='r') as file:
        lines=[line.strip() for line in file.readlines()]
    map=generate_map(lines)
    print_map(map)
    return 0

def generate_map(scans:list[str])->Map:
    map:Map=dict()
    
    for scan in scans:
        ls = scan.split(" -> ")
        for i in range(len(ls)-1):
            x1,y1 = [int(x) for x in ls[i].split(",")]
            x2,y2 = [int(x) for x in ls[i+1].split(",")]
            map.update(generate_row(x1,y1,x2,y2))
    return map
            
def generate_row(x1:int,y1:int,x2:int,y2:int)->Map:
    map:Map=dict()
    if x1==x2:
        for i in range(min(y1,y2), max(y1,y2)+1):
            map[(x1,i)]="#"
    elif y1==y2:
        for i in range(min(x1,x2), max(x1,x2)+1):
            map[(i,y1)]="#"
    else:
        raise ValueError(f"Incorrect row {(x1,y1)}->{(x2,y2)}")
    return map

def print_map(map:Map)->None:
    map[(500,0)]="+"
    
    xs=[x for x,  _ in [k  for k in map]]
    ys=[y for _,  y in [k  for k in map]]
    xm=min(xs)
    ym=min(ys)
    for j in range(max(ys)-min(ys)+1):
        for i in range(max(xs)-min(xs)+1):
            if (i+xm,j+ym) in map:
                print(map[(i+xm,j+ym)], end="")
            else:
                print(".", end="")
        print()
        
    
    
    
if __name__=="__main__":
    r=app("day14/example")
    if r!=24:
        raise ValueError(f"{r} is no valid for the puzzle 1 example")
    print("Hola")