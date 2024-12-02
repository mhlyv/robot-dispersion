#!/usr/bin/env python3

import lib
from lib import World, UnorientedWorld
from orientedrobot import OrientedRobot
from unorientedrobot import UnorientedRobot
import itertools
import concurrent.futures

def count_cycles(world):
    for i in itertools.count():
        if world.done():
            return i
        world.cycle()

s = 0
n = 500
sample = 1

with concurrent.futures.ThreadPoolExecutor() as executor:
    fs = [executor.submit(count_cycles, UnorientedWorld(n, UnorientedRobot)) for _ in range(sample)]
    for f in concurrent.futures.as_completed(fs):
        s += f.result()

print(f"n = {n}")
print(s / sample / n)
