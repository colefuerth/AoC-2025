#!/usr/bin/python3

import sys
from typing import List
from copy import deepcopy
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def process_bank(bank: List[int], num_batteries: int) -> int:
    m = 0
    for positions in combinations(range(len(bank)), num_batteries):
            positions = sorted(positions, reverse=True)
            num = 0
            for i in range(len(positions)):
                num += bank[positions[i]] * (10 ** i)
            m = max(m, num)
    return m

def solve(f: List[List[int]], num_batteries: int) -> int:
    with ProcessPoolExecutor() as executor:
        results = executor.map(partial(process_bank, num_batteries=num_batteries), f)
    return sum(results)

def part1(f: List[List[int]]) -> int:
    return solve(f, 2)

def part2(f: List[List[int]]) -> int:
    return solve(f, 12)


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]
    f = [[int(x) for x in l] for l in f]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
