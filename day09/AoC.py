#!/usr/bin/python3

import sys
from typing import Iterable, List, Tuple
from copy import deepcopy
from itertools import combinations, pairwise, product


def part1(f: List[Tuple[int, ...]]) -> int:
    return max(((abs(b[0]-a[0]) + 1) * (abs(b[1]-a[1]) + 1)) for a, b in combinations(f, 2))


def draw_line(a: Tuple[int, int], b: Tuple[int, int]) -> List[List[int]]:
    points = []
    if a[0] == b[0]:
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            points.append([a[0], y])
    elif a[1] == b[1]:
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            points.append([x, a[1]])
    return points


def draw_grid(points: Iterable[Tuple[int, int]]) -> None:
    min_x = min(p[0] for p in points) - 1
    max_x = max(p[0] for p in points) + 1
    min_y = min(p[1] for p in points) - 1
    max_y = max(p[1] for p in points) + 1
    grid = [["." for _ in range(min_x, max_x + 1)]
            for _ in range(min_y, max_y + 1)]
    for x, y in points:
        grid[y - min_y][x - min_x] = "#"
    for row in grid:
        print("".join(row))


def part2(f: List[Tuple[int, ...]]) -> int:
    perimeter = set()
    print("Calculating perimeter...")
    for a, b in pairwise(f + [f[0]]):
        line = draw_line(a, b)
        perimeter.update(tuple(p) for p in line)
    perimeter = list(perimeter)
    # start by filling in the area inside the perimeter
    min_x, min_y, max_x, max_y = (
        min(p[0] for p in perimeter),
        min(p[1] for p in perimeter),
        max(p[0] for p in perimeter),
        max(p[1] for p in perimeter),
    )
    print(f"Perimeter bounds: x={min_x}..{max_x}, y={min_y}..{max_y}")
    print(
        f"Total simulated area size: {(max_x - min_x + 3) * (max_y - min_y + 3)}")
    grid = {(x, y): (1 if (x, y) in perimeter else 0) for x, y in product(range(
        min_x - 1, max_x + 2), range(min_y - 1, max_y + 2))}
    print("Starting flood fill...")
    # flood fill from outside the perimeter
    stack = [(min_x - 1, min_y - 1), (max_x + 1, max_y + 1),
             (min_x - 1, max_y + 1), (max_x + 1, min_y - 1)]
    stack_iterations = 0
    while stack:
        stack_iterations += 1
        print(
            f"Flood fill iteration {stack_iterations}, stack size: {len(stack)}")
        x, y = stack.pop()
        if grid[(x, y)] == 0:
            grid[(x, y)] = 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) in grid and grid[(nx, ny)] == 0:
                    stack.append((nx, ny))
    # now we can make a list of the points that are inside the perimeter
    inside = [p for p, v in grid.items() if v == 0]
    points = set(inside + perimeter)
    # now, we can use the points to find the largest rectangular area where only points are inside
    draw_grid(points)
    rectangles = []
    for a, b in combinations(f, 2):
        if all((x, y) in points for x, y in product(range(a[0], b[0] + 1), range(a[1], b[1] + 1))):
            rectangles.append((abs(b[0]-a[0]) + 1) * (abs(b[1]-a[1]) + 1))
    return max(rectangles)


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [tuple(int(x) for x in l.strip().split(","))
         for l in open(fname, "r").readlines() if l.strip()]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
