#!/usr/bin/env python3

import lib
from lib import World, UnorientedWorld
from orientedrobot import OrientedRobot
from unorientedrobot import UnorientedRobot
import pygame
from pygame.locals import *
import sys

pygame.init()
screen = pygame.display.set_mode((500, 500), RESIZABLE)
font = pygame.font.Font(None, 22)
cycle_event = USEREVENT + 45

FPS = 1000
fps_clock = pygame.time.Clock()
clock = pygame.time.Clock()

n = 20
# world = World(n, OrientedRobot)
world = UnorientedWorld(n, UnorientedRobot)

def draw_world(screen, world):
    screen.fill((0, 0, 0))
    size = min(screen.get_size())
    grid_size = size // world.n

    for row in range(world.n):
        for col in range(world.n):
            n_robots = len(world.grid[row][col].robots)

            color = (int(255 * (n_robots / (n * n))),) * 3

            pygame.draw.rect(screen, color, pygame.Rect(col * grid_size, row * grid_size, grid_size, grid_size))

            if n_robots != 0:
                text = font.render(str(n_robots), True, (255, 0, 0))
                text_rect = text.get_rect(center=(col * grid_size + grid_size // 2, row * grid_size + grid_size // 2))
                screen.blit(text, text_rect)

run = False

while True:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = not run

    if run:
        if not world.done():
            world.cycle()
        else:
            print(world.steps)
            print(world.steps / world.n)
            run = False

    draw_world(screen, world)
    pygame.display.flip()
    pygame.display.update()
    fps_clock.tick(FPS)
