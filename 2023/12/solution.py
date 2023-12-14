from dataclasses import dataclass
from typing import Dict, Tuple
import re


@dataclass(frozen=True)
class Record:
    condition: str
    groups: Tuple[int, ...]


def left_simplify(record: Record) -> Record:
    condition = re.sub(r'\.+', '.', record.condition)
    condition = condition.strip(".")
    if len(record.groups) == 0:
        return Record(condition, record.groups)
    first_char = condition[:1]
    groups = record.groups[:]

    if "#" in first_char:
        g = groups[0]
        m = 0
        if "#" in first_char:
            f = condition.find("?")
            if f >= 0:
                if g > f:
                    return Record(condition, groups)
                m = min(g, f)+1
            else:
                m = g+1
        if m >= g:
            groups = groups[1:]
        else:
            groups = (g-m,)+groups[1:]
        condition = condition[m:]
        first_char = condition[:1]
    return Record(condition, groups)


def simplify(record: Record) -> Record:
    r = left_simplify(record)
    s = left_simplify(Record(r.condition[::-1], r.groups[::-1]))
    return Record(s.condition[::-1], s.groups[::-1])


# Test
sim: Dict[Record, Record] = {
    Record("#?", (2,)): Record("#?", (2,)),
    Record("#", (1,)): Record("", ()),
    Record("?#", (2,)): Record("?#", (2,)),
    Record("??", (2,)): Record("??", (2,)),
    Record("#???", (2, 1)): Record("#???", (2, 1)),
    Record("#??", (2,)): Record("#??", (2,)),
    Record("#??", (1,)): Record("?", ()),
    Record("?.??.#", (1, 1)): Record("?.??", (1,)),
    Record("##..#", (2, 1)): Record("", ()),
    Record("#??.#", (1, 1)): Record("?", ()),
}


for sim_k, sim_v in sim.items():
    e = simplify(sim_k)
    if e != sim_v:
        raise Exception(f"{sim_k}->{sim_v}!={e}")


# Voya a intentar resolver el ejercicio de forma recurvisa
def arragements(record: Record) -> int:
    record = simplify(record)
    condition = re.sub(r'\.+', '.', record.condition)
    condition = condition.strip(".")
    cuestions = condition.count("?")
    wrongs = condition.count("#")
    minimun = sum(record.groups)+len(record.groups)-1
    if len(condition) < minimun:
        return 0
    if cuestions + wrongs < sum(record.groups):
        return 0
    if condition == "":
        return 0
    if cuestions == 0:
        return 0
    if len(record.groups) == 0:
        return 0
    if wrongs == sum(record.groups):
        return 0
    if cuestions + wrongs == sum(record.groups):
        return 1

    p = record.groups[0]
    b = ""
    c = ""
    for i, c in enumerate(condition):
        if c == "?" or c == "#":
            # a = condition[:i]
            b = condition[i:]
            break
    if c == "?":
        # ? = .
        x = arragements(Record(b[1:], record.groups))
        # ? = #
        inter = b[:p]

        if "." not in inter and "#" not in b[p:p+1]:
            rest = b[p+1:]
            y = arragements(Record(rest, record.groups[1:]))
            z = y
            if y == 0:
                z = 1

            return x + z
        return x
    if c == "#":
        if "." in b[:p]:
            return 0
        if "#" in b[p:p+1]:
            return 0
        y = arragements(Record(b[p+1:], record.groups[1:]))

        if "?" not in b[:p]:
            return y
        return max(y, 1)

    raise Exception("This point will be never raised")


def is_solution(condition: str, groups: Tuple[int, ...]) -> bool:
    # Remove consecutive dots
    condition_without_consecutive_dots = re.sub(r'\.+', '.', condition)

    # Strip dots from the beginning and end
    cleaned_condition = condition_without_consecutive_dots.strip(".")

    # Create a tuple with the length of each group
    r = tuple(len(x) for x in cleaned_condition.split(".") if x)

    return r == groups

# No ha funcionado, así que lo hago por fuerza bruta.


def arragements_brut(record: Record) -> int:
    if len(record.groups) == 0:
        return 0
    condition = record.condition
    cuestions = condition.count("?")
    wrongs = condition.count("#")

    if cuestions == 0:
        return 0
    if cuestions + wrongs < sum(record.groups):
        return 0
    if wrongs == sum(record.groups):
        return 0
    permutations = 0
    for i in range(2**cuestions):
        binary = "{:0{longitud}b}".format(i, longitud=cuestions)
        replaced = ""
        n = 0
        for c in condition:
            if c == "?":
                if binary[n] == "1":
                    replaced = replaced+"#"
                else:
                    replaced = replaced+"."
                n += 1
            else:
                replaced = replaced+c
        if is_solution(replaced, record.groups):
            permutations += 1
    return permutations


# Tests
tests: Dict[Record, int] = {
    # Record(condition='????????#???#?', groups=(1, 8)): 9,
    Record(".", ()): 0,
    Record("?", ()): 0,
    Record("#", ()): 0,
    Record("?", (1,)): 1,
    Record("#", (1,)): 0,
    Record("..", ()): 0,
    Record(".#", (1,)): 0,
    Record("#.", (1,)): 0,
    Record("#?", (1,)): 0,
    Record("?#", (1,)): 0,
    Record("??", (1,)): 2,
    Record("??", (2,)): 1,
    Record("#??", (1,)): 0,
    Record("#??", (2,)): 1,
    Record("?#?", (1,)): 0,
    Record("??#)", (1,)): 0,
    Record("???", (1,)): 3,
    Record("???", (1, 1)): 1,
    Record("????", (1,)): 4,
    Record("????", (1, 1)): 3,
    Record("????", (2, 1)): 1,
    Record("????", (1, 2)): 1,
    Record("???.###", (1, 1, 3)): 1,
    Record("??.?##", (1, 1, 3)): 0,
    Record(".??...?##.", (1, 1, 3)): 0,
    Record(".??..??...?##.", (1, 1, 3)): 4,
    Record("#?##?#????.?..??",   (9, 1)): 3,
    Record("#?#?#?#?#?#?#?", (1, 3, 1, 6)): 1,
    Record("?#?#?#?#?#?#?#?", (1, 3, 1, 6)): 1,
    Record("????.#...#...", (4, 1, 1)): 1,
    Record("????.######..#####.", (1, 6, 5)): 4,
    Record("?#?##?#????.?..??",   (9, 1)): 7,

}

for s, v in tests.items():
    d = arragements(s)
    d2 = arragements_brut(s)
    if d2 != d:
        print(f"{d}!={d2} for {s}")
    if d != v:
        raise Exception(f"{s}->{d}!={v}")


example = "12/example"
input = "12/input"
file = input
data = [line.strip() for line in open(file)]
cs = [line.split(" ")[0] for line in data]
gs = [[int(i) for i in x]
      for line in data for x in [line.split(" ")[1].split(",")]]
records = [Record(c, tuple(s)) for c, s in zip(cs, gs)]

arrs = []
for i, r in enumerate(records):
    # s1 = arragements(r)
    s2 = arragements_brut(r)
    # if (s1 != s2):
    #     raise Exception(f"s1={s1}!={s2}=s2 for {r}")
    print(f"{i}: {r}={s2}")
    arrs.append(s2)


solution = sum(arrs)

arrs2 = [arragements_brut(r) for r in records]

if file == example and solution != 21:
    raise Exception(f"{solution}")

if file == input and solution >= 10369:
    raise Exception("Solution too high")
print(solution)

if file == input and solution <= 7108:
    raise Exception("Solution too loo")