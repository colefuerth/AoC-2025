#!/usr/bin/python3

import sys
from typing import List, Tuple
from copy import deepcopy
from math import log10
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat


def is_valid(n: int, splits: int = 2) -> bool:
    scale = int(log10(n))
    if scale % splits == 0:
        # if theres an odd number of digits, we cant split evenly
        return False
    parts = []
    for _ in range(splits):
        parts.append(n % (10 ** (scale // splits + 1)))
        n = n // (10 ** (scale // splits + 1))
    for l, r in zip(parts, parts[1:]):
        if l != r:
            return False
    return True


def _process_range_part1(range_tuple: Tuple[int, int]) -> int:
    l, r = range_tuple
    return sum(n for n in range(l, r + 1) if is_valid(n))


def part1(f: List[Tuple[int, int]]) -> int:
    with ProcessPoolExecutor() as executor:
        results = executor.map(_process_range_part1, f)
    return sum(results)


def _process_range_part2(range_tuple: Tuple[int, int]) -> int:
    l, r = range_tuple
    valid = []
    for n in range(l, r + 1):
        scale = int(log10(n))
        for x in range(2, scale + 2):
            if (scale + 1) % x == 0 and is_valid(n, splits=x):
                valid.append(n)
                break
    return sum(valid)


def part2(f: List[Tuple[int, int]]) -> int:
    with ProcessPoolExecutor() as executor:
        results = executor.map(_process_range_part2, f)
    return sum(results)


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]
    f = "".join(f).split(",")
    f = [(int(l), int(r)) for l, r in (x.split("-") for x in f)]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
