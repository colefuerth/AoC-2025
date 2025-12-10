#!/usr/bin/python3

import sys
from typing import List
from copy import deepcopy
from pprint import pprint
from itertools import combinations, combinations_with_replacement, count


class Machine:
    def __init__(self, leds: str, buttons: List[List[int]], joltages: List[int]):
        self.leds: int = 0
        for i, c in enumerate(leds):
            if c == "#":
                self.leds |= (1 << i)
        self.buttons_as_masks: List[int] = []
        for bg in buttons:
            b = 0
            for j in bg:
                b |= (1 << j)
            self.buttons_as_masks.append(b)
        self.buttons: List[List[int]] = buttons
        
        self.joltages: List[int] = joltages
    
    def solve1(self) -> int:
        if self.leds == 0:
            return 0
        for num_presses in range(len(self.buttons_as_masks) + 1):
            for combo in combinations(range(len(self.buttons_as_masks)), num_presses):
                state = 0
                for b in combo:
                    state ^= self.buttons_as_masks[b]
                if state == self.leds:
                    return num_presses
        print("No solution found!")
        return 0

    def solve2(self) -> int:
        if all(j == 0 for j in self.joltages):
            return 0
        for num_presses in count(1):
            for combo in combinations_with_replacement(range(len(self.buttons)), num_presses):
                joltage_counter = [0] * len(self.joltages)
                for b in combo:
                    for j in self.buttons[b]:
                        joltage_counter[j] += 1
                if joltage_counter == self.joltages:
                    return num_presses
        print("No solution found!")
        return 0


    def __repr__(self) -> str:
        return f"Machine(leds='{self.leds}', buttons={self.buttons}, joltages={self.joltages})"


def part1(machines: List[Machine]) -> int:
    return sum(m.solve1() for m in machines)


def part2(machines: List[Machine]) -> int:
    # return sum(m.solve2() for m in machines)
    solution = 0
    for i, m in enumerate(machines):
        res = m.solve2()
        print(f"Machine {i+1}/{len(machines)} solved with {res} presses")
        solution += res
    return solution


if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    f = [l.strip() for l in open(fname, "r").readlines() if l.strip()]
    machines: List[Machine] = []
    for line in f:
        line = line.split(" ")
        machine = {}
        machines.append(Machine(leds=line[0][1:-1],
                                buttons=[[int(x) for x in bg[1:-1].split(",")]
                                         for bg in line[1:-1]],
                                joltages=[int(x) for x in line[-1][1:-1].split(",")]))

    print("Part 1:", part1(deepcopy(machines)))
    print("Part 2:", part2(deepcopy(machines)))
