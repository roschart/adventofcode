def puntuation(round:str)-> int:
  switch={
    "A X": 1+3,
    "A Y": 2+6,
    "A Z": 3+0,
    "B X": 1+0,
    "B Y": 2+3,
    "B Z": 3+6,
    "C X": 1+6,
    "C Y": 2+0,
    "C Z": 3+3
    }
  return switch.get(round, 0)

def reaction(round:str)-> str:
  switch={
    "A X": "A Z",
    "A Y": "A X",
    "A Z": "A Y",
    "B X": "B X",
    "B Y": "B Y",
    "B Z": "B Z",
    "C X": "C Y",
    "C Y": "C Z",
    "C Z": "C X"
    }
  return switch.get(round, "")


with open('day02/input', mode ='r') as file:
  total1:int = 0
  total2:int = 0
  lines = file.readlines()
  for line in lines:
    line=line.strip()
    result=puntuation(line)
    if(result==0):
      print(f"Error in {line} with result {result}")
      exit(-1)
    total1+=result
    result2=puntuation(reaction(line))
    if(result2==0):
      print(f"Error in {line} with result {result2}")
      exit(-1)
    total2+=result2

print("Total1=", total1)
print("Total2=", total2)