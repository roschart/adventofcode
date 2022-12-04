
def getpairs(line:str) ->tuple[tuple[int,int], tuple[int, int]]:
  a,b=line.split(",")
  x,y=a.split("-")
  z,t=b.split("-")
  return (int(x),int(y)),(int(z),int(t))

def contains(a: tuple[int,int], b:tuple[int,int])->bool:
  a_set = get_set(a)
  b_set = get_set(b)
  return a_set.union(b)==a_set

def get_set(a:tuple[int, int])->set[int]:
    a_set:set[int]=set(range(a[0], a[1]+1))
    return a_set

def overlaps(a: tuple[int,int], b:tuple[int,int])->bool:
  a_set = get_set(a)
  b_set = get_set(b)
  return len(a_set.intersection(b_set))>=1
  
def app(filename:str)->tuple[int,int]:
  total1:int=0
  total2:int=0
  with open(filename, mode ='r') as file:
    lines = file.readlines()
    for line in lines:
      line=line.strip()
      # First part
      a,b=getpairs(line)
      if (contains(a, b) or contains(b,a)):
        total1+=1
      # Second part
      if (overlaps(a,b)):
        total2+=1
    return total1,total2


  # print(f"For {filename} Total2= {total2}")

if __name__ == "__main__":
  e1,e2=app("day04/example")
  if (e1!=2):
    raise ValueError(f"Valor distinto de {e1}")
  print(f"For example Total1= {e1}")
  if (e2!=4):
    raise ValueError(f"Valor distinto de {e2}")
  print(f"For example Total2= {e2}")
  i1,i2=app("day04/input")
  print(f"For example Total1= {i1}")
  print(f"For example Total2= {i2}")

