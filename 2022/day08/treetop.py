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

def app(filename:str)->int:
    forest:Forest=[] 
    with open(filename, mode='r') as file:
        for line in file.readlines():
            line=line.strip()
            row=list(line)
            forest.append([int(x) for x in row])
    total1=0
    for i in range (len(forest)):
        for j in range(len(forest[0])):
            if (is_visible(forest,i,j)):
                total1+=1
        
    return total1
        

if __name__=='__main__':
    e1:int=app("day08/example")
    if e1!=21:
        raise ValueError(f"Value of {e1} incorrect for example")
    i1:int=app("day08/input")
    print(f"Visible trees= {i1}")