import re
import numpy as np
import math

file = "06/input"
raw_data = [l.strip() for l in open(file)]
time = (int(x) for x in re.findall("\d+", raw_data[0]))
distance = (int(x) for x in re.findall("\d+", raw_data[1]))

races = zip(time, distance)


def get_margins(races):
    margin = []
    for t, d in races:
        roots = sorted(np.roots([1, -t, d]))
        delta = 0.000001  # Little tric to avoid matches
        i = math.ceil(roots[0]+delta)
        s = math.floor(roots[1]-delta)
        margin.append(s-i+1)
        print(roots)
    return margin


margin = get_margins(races)

s = math.prod(margin)

if file == "06/example" and s != 288:
    raise Exception

example_good_race = [(71530, 940200)]
margin = get_margins(example_good_race)

s = math.prod(margin)
if s != 71503:
    raise Exception


good_race = [(45988373, 295173412781210)]
margin = get_margins(good_race)
s = math.prod(margin)
print(s)
