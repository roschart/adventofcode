from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum, auto
from collections import Counter
from math import prod


class TypeHand(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


file = "07/input"
lines = [l.strip() for l in open(file)]


@dataclass
class Hand:
    value: str
    _type_hand: TypeHand = field(init=False)

    values = {
        'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9,
        '9': 8, '8': 7, '7': 6, '6': 5, '5': 4,
        '4': 3, '3': 2, '2': 1
    }

    def __post_init__(self):
        groups = Counter(self.value)
        if len(groups) == 5:
            self._type_hand = TypeHand.HIGH_CARD
            return
        if len(groups) == 1:
            self._type_hand = TypeHand.FIVE_OF_A_KIND
            return
        if len(groups) == 2:
            v = next(iter(groups.values()))
            if v == 1 or v == 4:
                self._type_hand = TypeHand.FOUR_OF_A_KIND
                return
            self._type_hand = TypeHand.FULL_HOUSE
            return
        if len(groups) == 3:
            v = max(groups.values())
            if v == 3:
                self._type_hand = TypeHand.THREE_OF_A_KIND
                return
            self._type_hand = TypeHand.TWO_PAIR
            return
        if len(groups) == 4:
            self._type_hand = TypeHand.ONE_PAIR
            return
        raise ValueError(self.value)

    @property
    def type_hand(self) -> TypeHand:
        return self._type_hand

    def __lt__(self, other: 'Hand'):
        if self.type_hand != other.type_hand:
            return self._type_hand.value < other._type_hand.value
        for a, b in zip(self.value, other.value):
            if Hand.values[a] != Hand.values[b]:
                return Hand.values[a] < Hand.values[b]
        return False


# print(Hand("AAAAA"))
# print(Hand("AA8AA"))
# print(Hand("23332"))
# print(Hand("AAB33"))
# print(Hand("A23A4"))
# print(Hand("23456"))


@dataclass
class Round:
    hand: Hand
    bind: int

    def __lt__(self, other: 'Round'):
        return self.hand < other.hand


rounds = [Round(Hand(x[0]), int(x[1])) for l in lines for x in [l.split(" ")]]

s = sum((i + 1) * r.bind for i, r in enumerate(sorted(rounds)))

if file == "07/example" and s != 6440:
    raise Exception

print(s)
