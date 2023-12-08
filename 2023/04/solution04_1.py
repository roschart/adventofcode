import re
from typing import List, Set

cards = [line.strip() for line in open("04/input")]


def get_winners(cards: List[str]) -> List[Set[int]]:
    result = []
    for card in cards:
        _, rest = card.split(": ")
        ws, cs = rest.split(" | ")

        winners = {int(m.group()) for m in re.finditer("\\d+", ws)}
        numbers = {int(m.group()) for m in re.finditer("\\d+", cs)}
        w = winners & numbers
        result.append(w)
    return result


print(sum(2**(len(x) - 1) for x in get_winners(cards) if len(x) > 0))
