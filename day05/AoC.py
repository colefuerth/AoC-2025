#!/usr/bin/python3

import sys
from typing import List, Tuple
from copy import deepcopy


def part1(ranges: List[Tuple[int, int]], ingredients: List[int]) -> int:
    return sum(
        1
        for ing in ingredients
        if any(low <= ing <= high for low, high in ranges)
    )


def part2(ranges: List[Tuple[int, int]]) -> int:
    merged_ranges = []
    for low, high in sorted(ranges):
        if not merged_ranges or merged_ranges[-1][1] < low - 1:
            merged_ranges.append([low, high])
        else:
            merged_ranges[-1][1] = max(merged_ranges[-1][1], high)
    return sum(high - low + 1 for low, high in merged_ranges)


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines()]
    blank_line_index = f.index('')
    ranges = [(int(low), int(high)) for low, high in (line.split('-')
                                                      for line in f[:blank_line_index])]
    ingredients = [int(x) for x in f[blank_line_index+1:]]

    print("Part 1:", part1(deepcopy(ranges), deepcopy(ingredients)))
    print("Part 2:", part2(deepcopy(ranges)))
