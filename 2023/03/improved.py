# Lo he sacado de una versión de internet adaptado un poco a mi gusto
# mi código orinal era una mierda comparado con este

import re
from math import prod
board = [line.strip() for line in open('03/input')]
rs = len(board)
cs = len(board[0])
asterisks: dict = {(r, c): [] for r in range(rs)
                   for c in range(cs) if board[r][c] == "*"}


def updateAsteriskNeighbors(asterisks, r, n):
    edge = {(r, c) for r in (r - 1, r, r + 1)
            for c in range(n.start() - 1, n.end() + 1)}
    for o in edge & asterisks.keys():
        asterisks[o].append(int(n.group()))


for r, row in enumerate(board):
    for n in re.finditer(r'\d+', row):
        updateAsteriskNeighbors(asterisks, r, n)

x = [prod(p) for p in asterisks.values() if len(p) == 2]
print(sum(x))
