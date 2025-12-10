#!/usr/bin/python3

import sys
from typing import List
from copy import deepcopy
from pprint import pprint
from itertools import combinations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


class Machine:
    def __init__(self, leds: str, buttons: List[List[int]], joltages: List[int]):
        self.leds: int = 0
        for i, c in enumerate(leds):
            if c == "#":
                self.leds |= (1 << i)
        self.buttons: List[List[int]] = buttons
        self.joltages: List[int] = joltages

    def solve1(self) -> int:
        if self.leds == 0:
            return 0
        buttons_as_masks: List[int] = []
        for bg in self.buttons:
            b = 0
            for j in bg:
                b |= (1 << j)
            buttons_as_masks.append(b)
        for num_presses in range(len(buttons_as_masks) + 1):
            for combo in combinations(range(len(buttons_as_masks)), num_presses):
                state = 0
                for b in combo:
                    state ^= buttons_as_masks[b]
                if state == self.leds:
                    return num_presses
        print("No solution found!")
        return 0

    def solve2(self) -> int:
        if all(j == 0 for j in self.joltages):
            return 0

        # Linear algebra approach: Ax = b
        # A[i][j] = 1 if button j affects joltage position i
        # x[j] = number of times to press button j
        # b[i] = target joltage for position i
        # Minimize sum(x) subject to Ax = b, x >= 0, x integer

        num_joltages = len(self.joltages)
        num_buttons = len(self.buttons)

        # Let A be the buttons, encoded as ones or zeros for which joltages they affect
        A = np.zeros((num_joltages, num_buttons), dtype=int)
        for j, button in enumerate(self.buttons):
            for i in button:
                A[i][j] = 1
        b = np.array(self.joltages)  # target joltage vector
        c = np.ones(num_buttons)  # minimize total presses
        constraints = LinearConstraint(A, lb=b, ub=b)  # solution must be exact
        bounds = Bounds(lb=0, ub=np.inf)  # no negative presses
        integrality = np.ones(num_buttons)  # all variables must be integers
        # "Mixed-integer linear programming"
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
        result = milp(
            c=c,
            constraints=constraints,
            bounds=bounds,
            integrality=integrality
        )

        if result.success:
            return int(round(result.fun))
        else:
            print(f"Optimization failed: {result.message}")
            return 0

    def __repr__(self) -> str:
        return f"Machine(leds='{self.leds}', buttons={self.buttons}, joltages={self.joltages})"


def part1(machines: List[Machine]) -> int:
    return sum(m.solve1() for m in machines)


def part2(machines: List[Machine]) -> int:
    return sum(m.solve2() for m in machines)


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
