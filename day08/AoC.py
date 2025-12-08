#!/usr/bin/python3

import sys
from typing import List, Tuple, DefaultDict, Set
from copy import deepcopy
from math import sqrt
from itertools import combinations, chain
from functools import cache
from math import prod, pow
from collections import defaultdict
import pprint

# calculate straight line distance between two points


@cache
def dist(a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
    return sqrt(sum(pow((x - y), 2) for x, y in zip(a, b)))


def get_circuit(point: Tuple[int, ...], edges: DefaultDict[Tuple[int, ...], List[Tuple[int, ...]]]) -> List[Tuple[int, ...]]:
    circuit = []
    stack = [point]
    while stack:
        current = stack.pop()
        circuit.append(current)
        for neighbor in edges[current]:
            if neighbor not in circuit:
                stack.append(neighbor)
    return circuit


def part1(f: List[Tuple[int, ...]]) -> int:
    distances: List[Tuple[Tuple[int, ...], Tuple[int, ...]]] = sorted(
        combinations(f, 2), key=lambda pair: dist(pair[0], pair[1])
    )

    NUMBER_OF_CONNECTIONS = 10
    edges: DefaultDict[Tuple[int, ...],
                       List[Tuple[int, ...]]] = defaultdict(list)
    for a, b in distances:
        if len(list(chain(*edges.values()))) // 2 >= NUMBER_OF_CONNECTIONS:
            break
        # if b in get_circuit(a, edges):
        #     continue
        print(f"{(len(list(chain(*edges.values()))) // 2) + 1}: Connecting {a} to {b} with distance {dist(a, b)}")
        edges[a].append(b)
        edges[b].append(a)
    pprint.pprint(edges)

    visited: Set[Tuple[int, ...]] = set()
    circuits: List[List[Tuple[int, ...]]] = []
    for point in f:
        if point in visited:
            continue
        circuits.append(get_circuit(point, edges))
        visited.update(circuits[-1])
    print(f"Found {len(circuits)} circuits")
    print([len(c) for c in sorted(circuits, key=len, reverse=True)])
    # print the sorted list of circuits in a prettyprint
    pprint.pprint(sorted(circuits, key=len, reverse=True))
    pprint.pprint(edges)
    return prod(len(c) for c in sorted(circuits, key=len, reverse=True)[:3])


def part2(f: List[Tuple[int, ...]]) -> int:
    return 0


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [tuple(map(int, l.strip().split(",")))
         for l in open(fname, "r").readlines() if l.strip()]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
# 377325 too high
