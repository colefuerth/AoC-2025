#!/usr/bin/python3

import sys
from typing import List
from copy import deepcopy


def process_bank(bank: List[int], num_batteries: int) -> int:
    i = max(range(len(bank) - num_batteries + 1), key=lambda x: bank[x])
    return ((bank[i] * (10 ** (num_batteries - 1))) + process_bank(bank[i+1:], num_batteries - 1)) if num_batteries > 1 else bank[i]


def solve(f: List[List[int]], num_batteries: int) -> int:
    return sum(process_bank(bank, num_batteries) for bank in f)


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
