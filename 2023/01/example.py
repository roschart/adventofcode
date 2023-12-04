
def solve1(filename:str)->int:
    with open(filename, "r") as f:
        total=0
        for line in f:
            digits=[x for x in line if x>="0" and x <="9"]
            first=digits[:1]
            last=digits[-1:]
            n="".join(first+last)
            total+=int(n)
    return total
            


s1=solve1("example.data")
expected=142    
if s1!= expected:
    raise ValueError(f"The {s1}!=={expected}")

s2=solve1("input")
print(s2)

    