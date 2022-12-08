from itertools import takewhile
Forest=list[list[int]]

def is_visible(forest:Forest,i:int,j:int)->bool:
    t=forest[i][j]
    ls=forest[i][:j]
    rs=forest[i][j+1:]
    ts= [forest[x][j] for x in range(i)]
    bs= [forest[x][j] for x in range(i+1, len(forest))]
       
    # from left
    if len(ls)==0 or t>max(ls):
        return True
    # from right
    elif len(rs)==0 or t>max(rs):
        return True
    elif len(ts)==0 or t>max(ts):
        return True
    elif len(bs)==0 or t>max(bs):
        return True
    return False


def count_trees(xs:list[int], t:int)->int:
    if len(xs)==0:
        return 0
    result=1
    for x in xs:
        if x >= t:
            return result
        else:
            result+=1
    if result>len(xs):
        return len(xs)
    return result
def scenic(forest,i,j)->int:
 
    t=forest[i][j]
    
    ls=list(reversed(forest[i][:j]))
    rs=forest[i][j+1:]
    ts= [forest[x][j] for x in reversed(range(i))]
    bs= [forest[x][j] for x in range(i+1, len(forest))]

    a=count_trees(ls,t)
    b=count_trees(rs,t)
    c=count_trees(ts,t)
    d=count_trees(bs,t)
    
    return a*b*c*d
def app(filename:str)->tuple[int,int]:
    forest:Forest=[] 
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line=line.strip()
            row=list(line)
            forest.append([int(x) for x in row])
    total1=0
    highest_scenic=0
    for i in range (len(forest)):
        for j in range(len(forest[0])):
            if (is_visible(forest,i,j)):
                total1+=1
            s=scenic(forest,i,j)
            if s> highest_scenic:
                highest_scenic=s
        
    return total1,highest_scenic
        

if __name__=='__main__':
    e1,e2=app("day08/example")
    if e1!=21:
        raise ValueError(f"Visible of {e1} incorrect for example")
    if e2!=8:
        raise ValueError(f"hight_scene of {e2} incorrect for example")
    i1,i2=app("day08/input")
    print(f"Visible trees= {i1}")
    print(f"High Scene= {i2}")