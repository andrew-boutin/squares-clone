"""
Author: andy_boutin
Created on: 9/12/16

Gather black blobs to get bigger, avoid red blobs.
"""
import sys
import random
from enum import Enum
import pygame

background_color = 255, 255, 255
red = 255, 0, 0
black = 0, 0, 0

num_enemies = 20
num_friendlies = 20


class Direction(Enum):
    up, down, left, right = range(4)


class Block():
    def __init__(self, color):
        self.color = color
        self.thickness = 0

        self._respawn()

    def _update_loc(self):
        if self.dir == Direction.down:
            self.y += self.speed
        elif self.dir == Direction.up:
            self.y -= self.speed
        elif self.dir == Direction.left:
            self.x -= self.speed
        elif self.dir == Direction.right:
            self.x += self.speed

    def update(self):
        if self._out_of_bounds():
            self._respawn()
        else:
            self._update_loc()

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size), self.thickness)

    def _respawn(self):
        self.dir = random.choice(list(Direction))
        self.speed = random.randint(1, 5)

        # Choose size between a bound
        self.size = 20

        # Choose starting x or y
        self.x = random.randint(0, screen_size)
        self.y = random.randint(0, screen_size)

    def _out_of_bounds(self):
        if self.x + self.size < 0:
            return True
        if self.x > screen_size:
            return True
        if self.y + self.size < 0:
            return True
        if self.y > screen_size:
            return True

        return False


class Enemy(Block):
    def __init__(self):
        super().__init__(black)


class Friendly(Block):
    def __init__(self):
        super().__init__(red)


pygame.init()

infoObject = pygame.display.Info()

screen_size = 700 #screen_size = infoObject.current_h

screen = pygame.display.set_mode((screen_size, screen_size), 0, 32)

clock = pygame.time.Clock()

blocks = []

for i in range(num_enemies):
    blocks.append(Enemy())

for i in range(num_friendlies):
    blocks.append(Friendly())

while True:
    # Control the frame rate
    time_passed = clock.tick(50)

    # exit if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(background_color)

    for block in blocks:
        block.update()

    # Update the UI
    pygame.display.flip()
