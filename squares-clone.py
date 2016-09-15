"""
Author: andy_boutin
Created on: 9/12/16

Gather black blobs to get bigger, avoid red blobs.
"""
import sys
import random
from enum import Enum
import pygame

white = 255, 255, 255
red = 255, 0, 0
black = 0, 0, 0
blue = 0, 0, 255

solid_shape = 0

num_enemies = 20
num_friendlies = 20


class GameManager():
    """Manages admin aspects of the game."""

    def __init__(self):
        """Initialize the game manager."""
        self.score = 0
        self.game_over = False


class Player():
    """Handles updating the player's cursor."""

    def __init__(self):
        """Set up the player and their cursor."""
        self.color = blue
        self.size = 2
        self.x = screen_size / 2
        self.y = screen_size / 2

        self._update_rect()

    def _update_rect(self):
        """Update the player's location boundary marker."""
        half_size = self.size / 2
        self.rect = pygame.Rect(self.x - half_size, self.y - half_size, self.size, self.size)

    def update(self):
        """Update the player's location and redraw the cursor on the screen."""
        x, y = pygame.mouse.get_pos()
        self.x = x
        self.y = y

        self._update_rect()
        pygame.draw.rect(screen, self.color, self.rect, solid_shape)


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

        self._update_rect()

    def _update_rect(self):
        """Update rectangle representing current location."""
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        """Update the location or respawn the block and then redraw."""
        if self._out_of_bounds():
            self._respawn()
        elif player.rect.colliderect(self.rect):
            self._handle_collision()
            self._respawn()
        else:
            self._update_loc()

        self._update_rect()
        pygame.draw.rect(screen, self.color, self.rect, solid_shape)


class Enemy(Block):
    """Block that kills the player."""

    def __init__(self):
        """Set up the block."""
        super().__init__(red)

    def _handle_collision(self):
        """Signal for the game to end."""
        game_manager.game_over = True


class Friendly(Block):
    """Block  that makes the player grow in size."""

    def __init__(self):
        """Set up the block."""
        super().__init__(black)

    def _handle_collision(self):
        """Increase the player's cursor and increment the score."""
        game_manager.score += 1
        player.size += 1


pygame.init()
pygame.mouse.set_visible(False)

infoObject = pygame.display.Info()
screen_size = 700 #screen_size = infoObject.current_h
screen = pygame.display.set_mode((screen_size, screen_size), 0, 32)

clock = pygame.time.Clock()

game_manager = GameManager()

player = Player()

blocks = []

for i in range(num_enemies):
    blocks.append(Enemy())

for i in range(num_friendlies):
    blocks.append(Friendly())

while not game_manager.game_over:
    # Control the frame rate
    time_passed = clock.tick(50)

    # exit if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(white)

    player.update()

    for block in blocks:
        block.update()

    # Update the UI
    pygame.display.flip()
