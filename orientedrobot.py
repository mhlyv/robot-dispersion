#!/usr/bin/env python3

import lib
from lib import Node, Robot, World
import math

class OrientedRobot(Robot):
    def __init__(self, rid, node):
        super().__init__(rid, node)
        self.program = self.travel_to_min_corner

    def travel_to_min_corner(self):
        match self.node.degree():
            case 2:
                self.program = self.count_n
            case 3 | 4:
                self.deferred = lambda: self.move(
                        self.get_min_corner_direction()[1])

    def get_min_corner_direction(self):
        return min(self.node.neighbors.items(), key = lambda p: p[0])

    def choose_min_corner_direction(self):
        if "MIN" not in self.memory:
            self.memory["MIN"] = self.get_min_corner_direction()[0]
        return self.memory["MIN"]

    # count the size of the grid from one corner to another
    def count_n(self):
        if "N" in self.memory:
            # wait until 3n so every robot is finished with this phase
            if self.elapsed() >= self.memory["N"] * 3:
                self.set_checkpoint()
                self.program = self.disperse_to_corners
            return

        if "TMP" not in self.memory:
            self.memory["TMP"] = self.memory["CYCLE"]
        elif self.node.degree() == 2:
            self.memory["N"] = self.memory["CYCLE"] - self.memory["TMP"] + 1
            del self.memory["TMP"]
            return

        self.deferred = lambda: self.move(self.node.neighbors[self.choose_min_corner_direction()])

    def disperse_to_corners(self):
        n = self.memory["N"]

        if self.elapsed() >= 4 * n:
            if "DIR" in self.memory:
                del self.memory["DIR"]
            self.set_checkpoint()
            self.program = self.disperse_to_columns
            return

        if self.node.degree() == 2:
            if len(self.node.robots) <= n * n / 4:
                return

            if self.decide_if_staying_in_corner():
                return

            # move in a circle
            self.memory["DIR"] = self.get_circle_direction()

        self.deferred = lambda: self.move(self.node.neighbors[self.memory["DIR"]])

    def get_circle_direction(self):
            match sorted(self.node.neighbors.keys()):
                case [2, 3]:
                    return 3
                case [1, 2]:
                    return 2
                case [1, 4]:
                    return 1
                case [3, 4]:
                    return 4

    def decide_if_staying_in_corner(self):
        n = self.memory["N"]

        ids = sorted([robot.rid for robot in self.node.robots])
        max_to_stay = ids[:n*n//4][-1]

        return self.rid <= max_to_stay

    def disperse_to_columns(self):
        if "DIR" not in self.memory:
            self.memory["DIR"] = self.get_circle_direction()

        if self.elapsed() >= self.memory["N"] // 2:
            self.set_checkpoint()
            self.program = self.disperse_to_rows
            return

        if self.decide_if_staying_in_column():
            return

        self.deferred = lambda: self.move(self.node.neighbors[self.memory["DIR"]])

    def decide_if_staying_in_column(self):
        n = self.memory["N"]
        q = n * n // 4
        c = q // (n // 2)

        ids = sorted([robot.rid for robot in self.node.robots])
        max_to_stay = ids[:c][-1]

        return self.rid <= max_to_stay

    def row_dir(self):
        return 4 if self.memory["DIR"] == 1 else self.memory["DIR"] - 1

    def disperse_to_rows(self):
        ids = sorted([robot.rid for robot in self.node.robots])

        if ids[0] == self.rid:
            # stay
            return

        self.deferred = lambda: self.move(self.node.neighbors[self.row_dir()])


if __name__ == '__main__':
    n = 10
    world = World(n, OrientedRobot)

    world.print()

    for i in range(n + n):
        world.cycle()

    for i in range(n):
        world.cycle()

    for i in range(4 * n):
        world.cycle()

    a = len(world.grid[0][0].robots)
    b = len(world.grid[0][n-1].robots)
    c = len(world.grid[n-1][0].robots)
    d = len(world.grid[n-1][n-1].robots)

    assert len({a, b, c, d}) == 1 if n // 2 == 0 else 2

    world.print()

    while True:
        world.cycle()
        world.print()
        input()


