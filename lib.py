import random

class Node:
    def __init__(self):
        self.neighbors = {}
        self.robots = set()

    def degree(self):
        return len(self.neighbors)

class Robot:
    def __init__(self, rid, node):
        self.rid = rid
        self.memory = {}
        self.node = node
        self.program = lambda: None
        self.deferred = None

        self.memory["CYCLE"] = 0
        self.memory["CHECKPOINT"] = 0

    def elapsed(self):
        return self.memory["CYCLE"] - self.memory["CHECKPOINT"]

    def set_checkpoint(self):
        self.memory["CHECKPOINT"] = self.memory["CYCLE"]

    def compute(self):
        self.program()

    # compute and execute are separated to simulate parallellism
    def execute(self):
        if self.deferred is not None:
            self.deferred()
            self.deferred = None

        self.memory["CYCLE"] += 1

    def move(self, to):
        self.node.robots.remove(self)
        self.node = to
        self.node.robots.add(self)

class World:
    def __init__(self, n, robot_type):
        self.n = n
        self.k = n * n
        self.grid = generate_oriented_grid(n)
        self.robots = drop_robots_on_grid(self.grid, self.k, robot_type)

    def cycle(self):
        for robot in self.robots:
            robot.compute()

        for robot in self.robots:
            robot.execute()

    def print(self):
        for row in self.grid:
            print("\t".join(str(len(node.robots)) for node in row))
        print()

def generate_oriented_grid(n):
    view = [[Node() for _ in range(n)] for _ in range(n)]
    columns = [[view[j][i] for j in range(n)] for i in range(n)]

    for row in view:
        for left, right in zip(row, row[1:]):
            left.neighbors[3] = right
            right.neighbors[1] = left

    for column in columns:
        for up, down in zip(column, column[1:]):
            up.neighbors[2] = down
            down.neighbors[4] = up

    return view

def grid_to_nodes(grid):
    return [node for row in grid for node in row]

def drop_robots_on_grid(grid, k, robot_type):
    nodes = grid_to_nodes(grid)
    robots = []

    for i in range(k):
        node = random.choice(nodes)
        robot = robot_type(i, node)
        node.robots.add(robot)
        robots.append(robot)

    return robots

def print_grid_population(grid):
    for row in grid:
        print("\t".join(str(len(node.robots)) for node in row))
    print()
