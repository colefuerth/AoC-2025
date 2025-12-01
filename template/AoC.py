#!/usr/bin/python3

import sys
from typing import List
from copy import deepcopy


def part1(f: List[str]) -> int:
    return 0


def part2(f: List[str]) -> int:
    return 0


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
