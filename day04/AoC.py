#!/usr/bin/python3

import sys
from typing import List
from copy import deepcopy
from itertools import product

ADJ = list(product([-1, 0, 1], repeat=2))
ADJ.remove((0, 0))


def is_valid(x: int, y: int, grid: List[str]) -> bool:
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])


def find_all_removable(f: List[str]) -> List[tuple[int, int]]:
    removable = []
    for x, y in product(range(len(f)), range(len(f[0]))):
        if f[x][y] == '@':
            adj = 0
            for dx, dy in ADJ:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny, f) and f[nx][ny] == '@':
                    adj += 1
            if adj < 4:
                removable.append((x, y))
    return removable


def part1(f: List[str]) -> int:
    return len(find_all_removable(f))


def part2(f: List[str]) -> int:
    count = 0
    while True:
        removable = find_all_removable(f)
        if not removable:
            break
        for x, y in removable:
            f[x] = f[x][:y] + '.' + f[x][y+1:]
        count += len(removable)
    return count


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
