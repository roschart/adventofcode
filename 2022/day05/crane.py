import copy
import re

def put_in_stacs(stacks:list[list[str]],line:str)->list[list[str]]:
  for i, v in enumerate(line):
    if v.isalpha():
      stacks[i//4].append(v)
  return stacks

def get_moves(line:str)->tuple[int,int,int]:
  t= [int(x) for x in re.findall(r'\d+',line)]
  if (len(t)!=3):
    raise ValueError(f"Incorrect size of {t} for the line {line}")  
  return t[0],t[1]-1,t[2]-1

def execute_move(stacks:list[list[str]], move:tuple[int,int,int], is9001:bool=False)->list[list[str]]:
  m=stacks[move[1]][:move[0]]
  if(not is9001):
    m.reverse()
  stacks[move[2]]= m + stacks[move[2]] 
  stacks[move[1]]=stacks[move[1]][move[0]:]
  return stacks

def get_tops(stacks:list[list[str]])->str:
  r:str=""
  for s in stacks:
    r+=s[0]
  return r 

def app(filename:str, size:int)->tuple[str,str]:
  stacks1:list[list[str]]=[[] for x in range(size)]
  stacks2:list[list[str]]=[]
  with open(filename, mode ='r') as file:
    reading_crates:bool=True
    lines = file.readlines()
    for line in lines:
      # First part
      if(reading_crates):
        if(line[0:2]==" 1"):
          reading_crates=False
          stacks2=copy.deepcopy(stacks1)
        else:
          stacks1=put_in_stacs(stacks1,line)
      else:
        if(line.strip()==""):
          continue
        m=get_moves(line)
        stacks1=execute_move(stacks1, m)
        stacks2=execute_move(stacks2,m, True)
        

      # Second part
    r1 = get_tops(stacks1)
    r2 = get_tops(stacks2)
    return r1,r2


  # print(f"For {filename} Total2= {total2}")

if __name__ == "__main__":
  e1,e2=app("day05/example",3)
  if (e1!="CMZ"):
    raise ValueError(f"Valor {e1} distinto de CMZ")
  print(f"For example Total1= {e1}")
  if (e2!="MCD"):
    raise ValueError(f"Valor distinto de {e2}")
  print(f"For example Total2= {e2}")
  i1,i2=app("day05/input",9)
  print(f"For input Total1= {i1}")
  print(f"For input Total2= {i2}")

