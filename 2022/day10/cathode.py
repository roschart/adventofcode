from enum import Enum

class State(Enum):
    FREE = 0
    ADDING = 1

def execute( command:str) -> State:
    if command=='noop':
        return State.FREE
    else:
        return State.ADDING
    
def app(filename:str)->int:
    with open(filename, mode='r') as file:
        commands=[line.strip() for line in file.readlines()]
        x:int=1
        checks:list[int]=[20,60,100, 140, 180, 220]
        strength:list[int]=[]
        state:State =State.FREE
        command="noop"
        for i in range(1,221):
            if i in checks:
                strength.append(x*i)
            if state==State.FREE:
                command=commands.pop(0)
                state=execute(command)
            elif state==State.ADDING:
                state=State.FREE
                x+=int(command.split()[1])              
                 
            print(f"Cicle {i}, status {state}, lastCommand= {command} \t x={x}")
        print(f"Strengz\n{strength}\n----")
        return sum(strength)
            

if __name__== "__main__":
    e=app("day10/example")
    if e!=13140:
        raise ValueError(f"Sinal streng of {e} no correct for the example")
    i=app("day10/input")
    print(f"El valor es {i}")
    
