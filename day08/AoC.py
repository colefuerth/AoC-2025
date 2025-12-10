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


@cache
def dist(a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
    return sqrt(sum(pow((x - y), 2) for x, y in zip(a, b)))


def get_circuit(point: Tuple[int, ...], connections: DefaultDict[Tuple[int, ...], List[Tuple[int, ...]]]) -> List[Tuple[int, ...]]:
    circuit = []
    stack = [point]
    while stack:
        current = stack.pop()
        circuit.append(current)
        for neighbor in connections[current]:
            if neighbor not in circuit:
                stack.append(neighbor)
    return circuit


def part1(f: List[Tuple[int, ...]]) -> int:
    distances: List[Tuple[Tuple[int, ...], Tuple[int, ...]]] = sorted(
        combinations(f, 2), key=lambda pair: dist(*pair)
    )

    NUMBER_OF_PAIRS_TO_TRY = 1000
    connections: DefaultDict[Tuple[int, ...],
                       List[Tuple[int, ...]]] = defaultdict(list)
    for (a, b) in distances[:NUMBER_OF_PAIRS_TO_TRY]:
        if b in get_circuit(a, connections):
            continue
        connections[a].append(b)
        connections[b].append(a)

    visited: Set[Tuple[int, ...]] = set()
    circuits: List[List[Tuple[int, ...]]] = []
    for point in f:
        if point in visited:
            continue
        circuits.append(get_circuit(point, connections))
        visited.update(circuits[-1])
    return prod(len(c) for c in sorted(circuits, key=len, reverse=True)[:3])


def part2(f: List[Tuple[int, ...]]) -> int:
    distances: List[Tuple[Tuple[int, ...], Tuple[int, ...]]] = sorted(
        combinations(f, 2), key=lambda pair: dist(*pair)
    )

    connections: DefaultDict[Tuple[int, ...],
                       List[Tuple[int, ...]]] = defaultdict(list)
    last_connection = distances[0]
    for (a, b) in distances:
        circuit = get_circuit(a, connections)
        if len(circuit) == len(f):
            break
        if b in get_circuit(a, connections):
            continue
        connections[a].append(b)
        connections[b].append(a)
        last_connection = (a, b)
    return last_connection[0][0] * last_connection[1][0]


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [tuple(map(int, l.strip().split(",")))
         for l in open(fname, "r").readlines() if l.strip()]

    print("Part 1:", part1(deepcopy(f)))
    print("Part 2:", part2(deepcopy(f)))
# 377325 too high
