with open('input', mode ='r') as file:
    calories:list[int]=[]
    max_calories:int=0
    lines = file.readlines()
    current_elf_calories :int=0
    for line in lines:
        num=line.strip()
        if (num==""):
            calories.append(current_elf_calories)
            current_elf_calories=0
        else:
            current_elf_calories+=int(num)
calories.sort()
top3=calories[-3:]
print("Max=", max(calories))
print("top3", top3)
print("Last=", top3[2])
print("Total=", sum(top3))
