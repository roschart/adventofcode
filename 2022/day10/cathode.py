from enum import Enum


class State(Enum):
    FREE = 0
    ADDING = 1


def execute(command: str) -> State:
    if command == 'noop':
        return State.FREE
    else:
        return State.ADDING


def app(filename: str) -> tuple[int, list[str]]:
    with open(filename, mode='r') as file:
        commands = [line.strip() for line in file.readlines()]
        x: int = 1
        checks: list[int] = [20, 60, 100, 140, 180, 220]
        strength: list[int] = []
        state: State = State.FREE
        command = "noop"
        pixels: list[str] = []
        i=1
        while len(commands)>0:
            p = (i-1)%40
            if (abs(p-x) < 2):
                pixels.append("#")
            else:
                pixels.append(".")

            if i in checks:
                strength.append(x*i)

            if state == State.FREE:
                command = commands.pop(0)
                state = execute(command)
            elif state == State.ADDING:
                state = State.FREE
                x += int(command.split()[1])
            i+=1
        return sum(strength), pixels

def print_crd(pixesl:list[str], replace:bool=False):
    s="".join(pixesl)
    if replace:
        s=s.replace(".", " ")
        
    print(s[0:40])
    print(s[40:80])
    print(s[80:120])
    print(s[120:160])
    print(s[160:200])
    print(s[200:240])

if __name__ == "__main__":
    e, ps = app("day10/example")
    if e != 13140:
        raise ValueError(f"Sinal streng of {e} no correct for the example")
    print_crd(ps)
    if "".join(ps)!= "##..##..##..##..##..##..##..##..##..##..###...###...###...###...###...###...###.####....####....####....####....####....#####.....#####.....#####.....#####.....######......######......######......###########.......#######.......#######.....":
        raise ValueError("Se ha pintado mal el ejemplo")
    
    i,ps = app("day10/input")
    print(f"El valor es {i}")
    print("------")
    print_crd(ps,True)
