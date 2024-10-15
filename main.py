#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
import random

class Node:
    def __init__(self):
        self.neighbors = {}
        self.robots = set()

    def degree(self):
        return len(self.neighbors)

class Robot:
    def __init__(self, rid):
        self.rid = rid
        self.memory = {}

        self.memory["CYCLE"] = 0

    def execute(self, program, current_node):
        program(self, current_node)
        self.memory["CYCLE"] += 1

class World:
    def __init__(self, grid, robots):
        self.grid = grid
        self.robots = robots

    def cycle(self, program):
        pairs = [(robot, node) for node in grid_to_nodes(self.grid)
                 for robot in node.robots]

        # simulate paralell execution because spawning threads costs too much
        random.shuffle(pairs)

        for robot, node in pairs:
            robot.execute(program, node)

        # with ThreadPoolExecutor() as executor:
        #     for robot, node in pairs:
        #         executor.submit(robot.execute, program, node)

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

def drop_robots_on_grid(grid, robots):
    nodes = grid_to_nodes(grid)

    for robot in robots:
        random.choice(nodes).robots.add(robot)

def next_node_toward_min_edge(node):
    _, next_node = min(node.neighbors.items(), key = lambda p: p[0])
    return next_node

def next_node_toward_max_edge(node):
    edge, next_node = max(node.neighbors.items(), key = lambda p: p[0])
    return edge, next_node

def robot_move_to_corner(robot, current_node):
    match current_node.degree():
        case 3 | 4:
            # move toward minimum edge
            _, next_node = next_node_toward_min_edge(current_node)
            current_node.robots.remove(robot)
            next_node.robots.add(robot)

def robot_count_to_other_corner(robot, current_node):
    if "N" in robot.memory:
        return # already calculated

    if "TMP" not in robot.memory:
        robot.memory["TMP"] = robot.memory["CYCLE"]
    elif current_node.degree() == 2:
        robot.memory["N"] = robot.memory["CYCLE"] - robot.memory["TMP"] + 1
        del robot.memory["TMP"]
        return

    edge, next_node = next_node_toward_max_edge(current_node)
    current_node.robots.remove(robot)
    next_node.robots.add(robot)

def robot_decide_if_staying_in_corner(robot, current_node):
    n = robot.memory["N"]

    ids = sorted([robot.rid for robot in current_node.robots])
    max_to_stay = ids[:n*n//4][-1]

    robot.memory["STAY"] = robot.rid <= max_to_stay

def print_grid_population(grid):
    for row in grid:
        print("\t".join(str(len(node.robots)) for node in row))
    print()

if __name__ == '__main__':
    n = 4
    k = n * n

    grid = generate_oriented_grid(n)
    robots = [Robot(i) for i in range(k)]

    drop_robots_on_grid(grid, robots)

    world = World(grid, robots)

    print_grid_population(grid)

    for _ in range(2 * n):
        world.cycle(robot_move_to_corner)

    print_grid_population(grid)

    for _ in range(n):
        world.cycle(robot_count_to_other_corner)

    print_grid_population(grid)

    world.cycle(robot_decide_if_staying_in_corner)

    print(len(list(filter(lambda r: r.memory["STAY"], grid[0][n-1].robots))))
    print(list(robot.memory["N"] for robot in robots))

