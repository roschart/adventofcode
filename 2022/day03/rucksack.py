

def containers(s:str) -> tuple[str, str]:
  string_length = len(s)
  # Split the string into two parts, each of length string_length / 2
  first_part = s[:string_length // 2]
  second_part = s[string_length // 2:]
  if (len(first_part)!=len(second_part)):
    raise ValueError(f"Listas no iguales {first_part}, {second_part}")
  return first_part, second_part


def share(a:str,b:str)->str:

  set_a:set[str]=set(a)
  set_b:set[str]=set(b)
  s=set_a.intersection(b)
  if (len(s)!=1):
    raise ValueError(f"Invalid input, a={a}, b={b}")
  return s.pop()
  
def priority(s:str)->int:
  if("A"<=s<="Z"):
    return ord(s)-ord("A")+27
  return ord(s)-ord("a")+1

def app(filename:str)->None:
  with open(filename, mode ='r') as file:
    total1: int =0
    total2:int =0
    member=0
    lines = file.readlines()
    for line in lines:
      line=line.strip()
      # First part
      a,b=containers(line)
      s= share(a,b)
      p = priority(s)
      total1+=p
      # Second part
      if (member==0):
        acc=set(line)
      else:
        acc = acc.intersection(set(line))
      member+=1
      if(member==3):
        if(len(acc)!=1):
          raise ValueError("There is no only 1 intersection {acc}")
        member=0
        total2+=priority(acc.pop())



  print(f"For {filename} Total1= {total1}")
  print(f"For {filename} Total2= {total2}")

if __name__ == "__main__":
  app("example")
  app("input")

