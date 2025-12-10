#!/usr/bin/python3

import sys
from typing import Iterable, List, Tuple
from copy import deepcopy
from itertools import combinations, pairwise, product


def part1(f: List[Tuple[int, ...]]) -> int:
    return max(((abs(b[0]-a[0]) + 1) * (abs(b[1]-a[1]) + 1)) for a, b in combinations(f, 2))


def draw_line(a: Tuple[int, ...], b: Tuple[int, ...]) -> List[List[int]]:
    points = []
    if a[0] == b[0]:
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            points.append([a[0], y])
    elif a[1] == b[1]:
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            points.append([x, a[1]])
    return points


def part2(f: List[Tuple[int, ...]]) -> int:
    edges = [(a, b) for a, b in pairwise(f + [f[0]])]
    perimeter = set()
    for a, b in edges:
        line = draw_line(a, b)
        perimeter.update(tuple(p) for p in line)

    def point_in_polygon(x, y):
        """Check if point (x,y) is inside or on the polygon using ray casting."""
        if (x, y) in perimeter:
            return True
        inside = False
        for (x1, y1), (x2, y2) in edges:
            if ((y1 > y) != (y2 > y)) and \
               (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside

    candidates = []
    for a, b in combinations(f, 2):
        min_x, max_x = min(a[0], b[0]), max(a[0], b[0])
        min_y, max_y = min(a[1], b[1]), max(a[1], b[1])
        area = (max_x - min_x + 1) * (max_y - min_y + 1)
        candidates.append((area, min_x, max_x, min_y, max_y))
    candidates.sort(reverse=True)

    for idx, (area, min_x, max_x, min_y, max_y) in enumerate(candidates):
        width, height = max_x - min_x + 1, max_y - min_y + 1
        valid = True
        if area > 10000:
            # Sample corners, edges, and interior for large rectangles
            sample_points = set()

            # Corners
            for cx, cy in [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]:
                sample_points.add((cx, cy))

            # Edges
            step = max(1, min(width, height) // 100)
            for x in range(min_x, max_x + 1, step):
                sample_points.add((x, min_y))
                sample_points.add((x, max_y))
            for y in range(min_y, max_y + 1, step):
                sample_points.add((min_x, y))
                sample_points.add((max_x, y))

            # Interior sample
            for x in range(min_x + 1, max_x, max(1, width // 20)):
                for y in range(min_y + 1, max_y, max(1, height // 20)):
                    sample_points.add((x, y))

            valid = all(point_in_polygon(x, y) for x, y in sample_points)
        else:
            # Check all points for small rectangles
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if not point_in_polygon(x, y):
                        valid = False
                        break
                if not valid:
                    break

        if valid:
            return area

    return 0


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [tuple(int(x) for x in l.strip().split(","))
         for l in open(fname, "r").readlines() if l.strip()]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
