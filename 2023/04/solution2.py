import re
from typing import Dict, List, Set

cards = [line.strip() for line in open("04/input")]

copies: Dict[int, int] = {x+1: 1 for x in range(len(cards))}


def get_winners(cards: List[str]) -> List[Set[int]]:
    result = []
    for card in cards:
        _, rest = card.split(": ")
        ws, cs = rest.split(" | ")

        winners = {int(m.group()) for m in re.finditer("\d+", ws)}
        numbers = {int(m.group()) for m in re.finditer("\d+", cs)}
        w = winners & numbers
        result.append(w)
    return result


for e, w in enumerate(get_winners(cards)):
    e = e+1
    wins = len(w)
    for i in range(e+1, e+wins+1):
        copies[i] += copies[e]


print(sum(copies.values()))
