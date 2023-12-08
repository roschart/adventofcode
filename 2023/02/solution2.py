
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Set:
    red: int = 0
    blue: int = 0
    green: int = 0

    @staticmethod
    def from_string(set_string: str):
        colors = {'red': 0, 'blue': 0, 'green': 0}
        for color_info in set_string.split(','):
            color_info = color_info.strip()
            if color_info:
                number, color = color_info.split()
                colors[color] = int(number)
        return Set(**colors)


@dataclass
class Game:
    id: int
    sets: List[Set]

    @staticmethod
    def from_string(game_string: str):
        game_id_str, sets_str = game_string.split(':', 1)
        game_id = int(game_id_str.split()[1])
        sets = [Set.from_string(s) for s in sets_str.split(';')]
        return Game(game_id, sets)


LIMITS = Set(red=12, green=13, blue=14)


def is_posible(game: Game) -> bool:
    limits = LIMITS
    for s in game.sets:
        if s.blue > limits.blue or s.green > limits.green or s.red > limits.red:
            return False
    return True


def process_posible(game: Game, acc: int) -> int:
    if is_posible(game):
        acc += game.id
    return acc


def process_potential(game: Game, acc: int) -> int:
    potential = Set()
    for s in game.sets:
        if s.red > potential.red:
            potential.red = s.red
        if s.blue > potential.blue:
            potential.blue = s.blue
        if s.green > potential.green:
            potential.green = s.green
    value = potential.red * potential.green * potential.blue
    return value + acc


g1 = Game.from_string("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")

if not is_posible(g1):
    raise Exception("g1 must be posible")

if process_potential(g1, 0) != 48:
    raise Exception("g1 potential !=48")


def process_file(filename: str, proc: Callable[[Game, int], int]) -> int:
    total = 0
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            game = Game.from_string(line)
            total = proc(game, total)
    return total


e1 = process_file("02/example", process_posible)
expected = 8
if e1 != expected:
    raise Exception(f"{e1}!={expected}")

s1 = process_file("02/input", process_posible)
expected = 2632
if s1 != expected:
    raise Exception(f"{s1}!={expected}")


e2 = process_file("02/example", process_potential)
expected = 2286
if e2 != expected:
    raise Exception(f"{e2}!={expected}")

s2 = process_file("02/input", process_potential)
expected = 69629
if s2 != expected:
    raise Exception(f"{s2}!={expected}")
