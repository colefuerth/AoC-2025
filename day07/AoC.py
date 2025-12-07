#!/usr/bin/python3

import sys
from typing import List, Tuple
from copy import deepcopy
from functools import cache


def part1(f: List[str]) -> int:
    grid = [list(map(str, line)) for line in f]
    grid[1][grid[0].index('S')] = '|'
    splits = 0
    for up, line in zip(grid[:-1], grid[1:]):
        for i, (c, u) in enumerate(zip(line, up)):
            if c == "^" and u == "|":
                line[i-1] = "|"
                line[i+1] = "|"
                splits += 1
            elif u == "|":
                line[i] = "|"
    return splits


def part2(f: List[str]) -> int:
    @cache
    def dfs(x: int, y: int) -> int:
        if y == len(f) - 1:
            return 1
        c = f[y][x]
        if c == '^':
            return dfs(x - 1, y) + dfs(x + 1, y)
        return dfs(x, y + 1)
    return dfs(f[0].index('S'), 1)


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
