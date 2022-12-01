import os
import pathlib

with open('input', mode ='r') as file:
    max_calories:int=0
    lines = file.readlines()
    current_elf_calories :int=0
    for line in lines:
        num=line.strip()
        if (num==""):
            if(current_elf_calories>max_calories):
                max_calories=current_elf_calories
            current_elf_calories=0
        else:
            current_elf_calories+=int(num)
print(max_calories)