#!/usr/bin/python3

import sys
from typing import List
from copy import deepcopy


def part1(coeff: List[List[int]], operands: List[str]) -> int:
    transposed = zip(*coeff)
    total = 0
    for operand, group in zip(operands, transposed):
        total += eval(operand.join(map(str, group)))
    return total


def part2(f: List[str]) -> int:
    f = [''.join(reversed(l)) for l in f]
    operands = [o.strip() for o in f[-1].split(" ") if o.strip()]
    ff = list(zip(*f[:-1]))
    coeff = [[]]
    for line in ff:
        if ''.join(line).strip():
            coeff[-1].append(int(''.join(line).strip()))
        else:
            coeff.append([])
    coeff = [[int(x) for x in c] for c in coeff if c]
    total = 0
    for operand, group in zip(operands, coeff):
        total += eval(operand.join(map(str, group)))
    return total


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l for l in open(fname, "r").readlines()]
    coeff = [[int(x.strip()) for x in line.split(" ") if x.strip()]
             for line in f[:-1]]
    operands = [o.strip() for o in f[-1].split(" ") if o.strip()]

    print("Part 1:", part1(deepcopy(coeff), deepcopy(operands)))
    print("Part 2:", part2(deepcopy(f)))
# not 7092293782
