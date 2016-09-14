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
blue = 0, 0, 255

solid_shape = 0

num_enemies = 20
num_friendlies = 20


class Direction(Enum):
    """Cardinal directions."""
    up, down, left, right = range(4)


class Block():
    """Represents a block that moves around the screen."""

    def __init__(self, color):
        """Handle setting up the block."""
        self.color = color

        self._respawn()

    def _update_loc(self):
        """Moves the block in a straight line in it's vector."""
        if self.dir == Direction.down:
            self.y += self.speed
        elif self.dir == Direction.up:
            self.y -= self.speed
        elif self.dir == Direction.left:
            self.x -= self.speed
        elif self.dir == Direction.right:
            self.x += self.speed

    def _out_of_bounds(self):
        """Determine if the block is off the visible screen."""
        if self.x + self.size < 0:
            return True
        if self.x > screen_size:
            return True
        if self.y + self.size < 0:
            return True
        if self.y > screen_size:
            return True

        return False

    def _respawn(self):
        """Set variables that change when the block respawns."""
        self.dir = random.choice(list(Direction))
        self.speed = random.randint(1, 5)

        # Choose size between a bound
        self.size = 20

        # Choose starting x and y to place on the edge of the screen
        if self.dir in [Direction.down, Direction.up]:
            self.x = random.randint(0, screen_size - self.size)

            if self.dir == Direction.down:
                self.y = -self.size
            else:
                self.y = screen_size

        elif self.dir in [Direction.left, Direction.right]:
            self.y = random.randint(0, screen_size - self.size)

            if self.dir == Direction.left:
                self.x = screen_size
            else:
                self.x = -self.size

    def update(self):
        """Update the location or respawn the block and then redraw."""
        if self._out_of_bounds():
            self._respawn()
        else:
            self._update_loc()

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size), solid_shape)


class Enemy(Block):
    """Block that kills the player."""

    def __init__(self):
        """Set up the block."""
        super().__init__(black)


class Friendly(Block):
    """Block  that makes the player grow in size."""

    def __init__(self):
        """Set up the block."""
        super().__init__(red)


pygame.init()
pygame.mouse.set_visible(False)

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

    mouse_size = 20
    half_mouse_size = mouse_size / 2
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, blue, (mouse_x - half_mouse_size, mouse_y - half_mouse_size, mouse_size, mouse_size), solid_shape)

    # Update the UI
    pygame.display.flip()
