from typing import List, Tuple


Ranges = Tuple[int, int, int]

file = "05/input"
data = [line.strip() for line in open(file)]


def transform(ranges: List[Ranges], value: int) -> int:
    for d, s, r in ranges:
        if value >= s and value < s + r:
            return value + d - s
    return value


seeds = [int(x) for x in data[0].split(": ")[1].split(" ")]

init_maps = [n + 1 for n, l in enumerate(data) if l == ""]

maps = list(zip(init_maps, init_maps[1:]))
maps.append((init_maps[-1], len(data) + 1))

initial = seeds
for s, e in list(maps):
    transformations: List[Ranges] = []
    for l in range(s + 1, e - 1):
        t = [int(x) for x in data[l].split(" ")]
        transformations.append((t[0], t[1], t[2]))
    for i, v in enumerate(initial):
        n = transform(transformations, v)
        initial[i] = n

s = min(initial)


if file == "05/example" and s != 35:
    raise Exception

if file == "05/input" and s != 650599855:
    raise Exception


print(s)
