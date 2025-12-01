#!/usr/bin/python3

import sys
from typing import List, Tuple
from copy import deepcopy


def rotate(angle: int, direction: str, current: int) -> Tuple[int, int]:
    passes = angle // 100
    angle %= 100
    if current != 0:
        passes += current + angle >= 100 if direction == "R" else current - angle <= 0
    if direction == "R":
        current += angle
    else:
        current -= angle
    current %= 100
    return current, passes


def part1(f: List[Tuple[str, int]]) -> int:
    position = 50
    count = 0
    for direction, angle in f:
        position, _ = rotate(angle, direction, position)
        if position == 0:
            count += 1
    return count


def part2(f: List[Tuple[str, int]]) -> int:
    position = 50
    count = 0
    for direction, angle in f:
        position, passes = rotate(angle, direction, position)
        count += passes
    return count


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]
    c = [(l[0], int(l[1:])) for l in f]

    print("Part 1:", part1(deepcopy(c)))
    print("Part 2:", part2(deepcopy(c)))