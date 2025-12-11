#!/usr/bin/python3

import sys
from typing import List, Dict
from copy import deepcopy
from pprint import pprint


def part1(f: Dict[str, List[str]]) -> int:
    def traverse(cur: str, target: str) -> int:
        if cur == target:
            return 1
        return sum(traverse(nxt, target) for nxt in f[cur])
    return traverse("you", "out")


def part2(f: Dict[str, List[str]]) -> int:
    def traverse(cur: str, target: str, required_passes: List[str]) -> int:
        if cur == target:
            return int(len(required_passes) == 0)
        if cur in required_passes:
            required_passes = required_passes[:]
            required_passes.remove(cur)
        return sum(traverse(nxt, target, required_passes) for nxt in f[cur])
    return traverse("svr", "out", ["fft", "dac"])


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]
    circuit = {l.strip():[rr.strip() for rr in r.strip().split(" ")] for l, r in (line.split(":") for line in f)}

    print("Part 1:", part1(deepcopy(circuit)))
    print("Part 2:", part2(deepcopy(circuit)))
