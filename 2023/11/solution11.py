from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass(frozen=True)
class Coord:
    r: int
    c: int


def get_galaxies(data: List[str]) -> Set[Coord]:
    galaxies: Set[Coord] = set()
    for i, line in enumerate(data):
        for j, v in enumerate(line):
            if v == "#":
                galaxies.add(Coord(i, j))
    return galaxies


def distance(pair: Tuple[Coord, Coord]) -> int:
    a, b = pair
    d = abs(a.r-b.r)+abs(a.c-b.c)
    return d


def distances(file: str, expand: int = 2) -> List[int]:
    expand -= 1
    data = [line.strip() for line in open(file)]

    rows = len(data)
    cols = len(data[0])

    original_galaxies = get_galaxies(data)

    rows_to_expand = set(range(rows))
    cols_to_expand = set(range(cols))

    for coord in original_galaxies:
        rows_to_expand.discard(coord.r)
        cols_to_expand.discard(coord.c)

    galaxies: Set[Coord] = set()
    for coord in original_galaxies:
        len_r = len([r for r in rows_to_expand if r < coord.r])
        r = coord.r+expand*len_r
        len_c = len([c for c in cols_to_expand if c < coord.c])
        c = coord.c+expand*len_c
        galaxies.add(Coord(r, c))

    pairs: Set[Tuple[Coord, Coord]] = set()
    galaxies_copy = galaxies.copy()
    a = galaxies_copy.pop()
    while (len(galaxies_copy) > 0):
        for b in galaxies_copy:
            pairs.add((a, b))
        a = galaxies_copy.pop()

    # Checks
    if file == "11/example" and expand == 1:
        one = Coord(0, 4)
        seven = Coord(10, 9)
        three = Coord(2, 0)
        six = Coord(7, 12)
        eight = Coord(11, 0)
        nine = Coord(11, 5)

        cs = [one, seven, three, six, eight, nine]
        for coord in cs:
            if coord not in galaxies:
                print(galaxies)
                raise Exception(f"{coord}")

        d: Dict[Tuple[Coord, Coord], int] = {
            (one, seven): 15, (three, six): 17, (eight, nine): 5}
        for k, v in d.items():
            if distance(k) != v:
                raise Exception(f"{k},{v}")

    ds: List[int] = list()
    for p in pairs:
        ds.append(distance(p))
    return ds


file = "11/example"
s = sum(distances(file))
if s != 374:
    raise Exception(f"for {file}:{s}")

file = "11/input"
s = sum(distances(file))
if s != 9724940:
    raise Exception(f"for {file}:{s}")

file = "11/example"
s = sum(distances(file, 10))
if s != 1030:
    raise Exception(f"for {file}:{s}")

file = "11/example"
s = sum(distances(file, 100))
if s != 8410:
    raise Exception(f"for {file}:{s}")


file = "11/input"
s = sum(distances(file, 1000000))
if s != 569052586852:
    raise Exception(f"for {file}:{s}")
