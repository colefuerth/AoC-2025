#!/usr/bin/python3

import sys
from typing import Tuple
from pprint import pprint


def part1(shapes: Tuple[Tuple[Tuple[int, int], ...], ...], regions: Tuple[Tuple[Tuple[int, ...], Tuple[int, ...]], ...]) -> int:
    return 0


def part2(shapes: Tuple[Tuple[Tuple[int, int], ...], ...], regions: Tuple[Tuple[Tuple[int, ...], Tuple[int, ...]], ...]) -> int:
    return 0


if __name__ == "__main__":
    from itertools import groupby

    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines()]

    groups = [tuple(group)
              for key, group in groupby(f, lambda x: x == '') if not key]
    shapes, regions = [group[1:] for group in groups[:-1]], groups[-1]
    shapes = tuple(
        tuple(
            (x, y) for x, line in enumerate(shape) for y, c in enumerate(line) if c == '#'
        ) for shape in shapes
    )
    regions = tuple(
        (
            tuple(int(x) for x in line.split(": ")[0].split('x')),
            tuple(int(i) for i in line.split(": ")[1].strip().split(' '))
        )
        for line in regions
    )
    pprint(shapes)
    pprint(regions)

    print("Part 1:", part1(shapes, regions))
    print("Part 2:", part2(shapes, regions))
