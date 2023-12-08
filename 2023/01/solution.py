import re

word_to_num = {
    "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
}


def solve1(filename: str) -> int:
    with open(filename, "r") as f:
        total = 0
        for line in f:
            digits = [x for x in line if x >= "0" and x <= "9"]
            first = digits[:1]
            last = digits[-1:]
            n = "".join(first+last)
            total += int(n)
    return total


def solve2(filename: str) -> int:
    regex = r"\d|one|two|three|four|five|six|seven|eight|nine"
    rregex = r"\d|enin|thgie|neves|xis|evif|ruof|eerht|owt|eno"
    with open(filename, "r") as f:
        total = 0
        for line in f:
            line = line.strip()
            n = 0
            o = line[:]
            m = re.search(regex, line)
            if m is None:
                raise Exception
            d = m.group()
            if d.isdigit():
                n = int(d)*10
            else:
                n = word_to_num[d]*10
            rl = line[::-1]
            m = re.search(rregex, rl)
            d = m.group()
            if m is None:
                raise Exception
            if d.isdigit():
                n += int(d)
            else:
                n += word_to_num[d[::-1]]
            total += int(n)
    return total


s1 = solve1("example.data")
expected = 142
if s1 != expected:
    raise ValueError(f"The {s1}!=={expected}")


d1 = solve1("input")
print(d1)


s2 = solve2("example2.data")
expected = 281
if s2 != expected:
    raise ValueError(f"The {s1}!=={expected}")

d2 = solve2("input")
expected = 53539
send = 53551
if d2 == send:
    raise ValueError(f"{send} is too high")
if d2 != expected:
    raise ValueError(f"The {d2}!=={expected}")
