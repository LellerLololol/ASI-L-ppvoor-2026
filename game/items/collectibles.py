"""
collectibles.py - Dots, power pellets, speed boosts, and moving obstacles.

Each item knows its grid position and how to draw itself.  The game
engine handles collision detection and scoring.
"""

import math
import random
import pygame

from game.settings import (
    CELL_SIZE, COLOR_DOT, COLOR_POWER_PELLET, COLOR_SPEED_BOOST,
)


class Dot:
    """Small collectible dot placed on path cells.

    Collecting all dots is the win condition.
    """

    def __init__(self, col: int, row: int, tile_size: int):
        self.grid_pos = (col, row)
        self.tile_size = tile_size
        self.radius = max(2, tile_size // 10)
        self._cx = col * tile_size + tile_size // 2
        self._cy = row * tile_size + tile_size // 2

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, COLOR_DOT, (self._cx, self._cy), self.radius)


class PowerPellet:
    """Larger glowing pellet that causes ghosts to enter FRIGHTENED state.

    Rendered with a pulsing animation for visual emphasis.
    """

    def __init__(self, col: int, row: int, tile_size: int):
        self.grid_pos = (col, row)
        self.tile_size = tile_size
        self.base_radius = max(4, tile_size // 4)
        self._cx = col * tile_size + tile_size // 2
        self._cy = row * tile_size + tile_size // 2
        self._frame = 0

    def draw(self, surface: pygame.Surface) -> None:
        self._frame += 1
        # Pulsing radius
        pulse = math.sin(self._frame * 0.1) * 2
        r = max(2, int(self.base_radius + pulse))

        # Glow (larger transparent circle behind)
        glow_surface = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        glow_color = (*COLOR_POWER_PELLET[:3], 60)
        pygame.draw.circle(glow_surface, glow_color, (r * 2, r * 2), r * 2)
        surface.blit(glow_surface, (self._cx - r * 2, self._cy - r * 2))

        # Core
        pygame.draw.circle(surface, COLOR_POWER_PELLET, (self._cx, self._cy), r)


class SpeedBoost:
    """Temporary speed boost pickup.

    Drawn as a small lightning bolt shape.
    """

    def __init__(self, col: int, row: int, tile_size: int):
        self.grid_pos = (col, row)
        self.tile_size = tile_size
        self._cx = col * tile_size + tile_size // 2
        self._cy = row * tile_size + tile_size // 2
        self._frame = 0

    def draw(self, surface: pygame.Surface) -> None:
        self._frame += 1
        s = self.tile_size // 3

        # Lightning bolt polygon (simplified)
        points = [
            (self._cx - 2, self._cy - s),
            (self._cx + 3, self._cy - 2),
            (self._cx,     self._cy),
            (self._cx + 4, self._cy + 1),
            (self._cx - 1, self._cy + s),
            (self._cx + 1, self._cy + 2),
            (self._cx - 3, self._cy),
        ]

        # Flicker alpha
        alpha = 180 + int(60 * math.sin(self._frame * 0.2))
        bolt_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        offset_points = [
            (px - self._cx + self.tile_size // 2, py - self._cy + self.tile_size // 2)
            for px, py in points
        ]
        bolt_color = (*COLOR_SPEED_BOOST[:3], alpha)
        pygame.draw.polygon(bolt_surface, bolt_color, offset_points)
        surface.blit(
            bolt_surface,
            (self._cx - self.tile_size // 2, self._cy - self.tile_size // 2),
        )


class MovingObstacle:
    """A hazard that patrols maze corridors.

    Moves in a straight line until hitting a wall, then picks a new
    random direction.  Kills the player on contact (unless powered up).
    """

    def __init__(self, col: int, row: int, tile_size: int, speed: int):
        self.tile_size = tile_size
        self.speed = speed
        self.pixel_x: float = col * tile_size
        self.pixel_y: float = row * tile_size
        self.direction: tuple[int, int] = random.choice(
            [(0, -1), (0, 1), (-1, 0), (1, 0)]
        )
        self.color = (200, 50, 50)
        self._frame = 0

    def get_grid_pos(self) -> tuple[int, int]:
        return (
            int(self.pixel_x // self.tile_size),
            int(self.pixel_y // self.tile_size),
        )

    def update(self, grid: list[list[int]]) -> None:
        """Move forward; pick a new direction on wall collision."""
        self._frame += 1
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        if self.pixel_x % self.tile_size == 0 and self.pixel_y % self.tile_size == 0:
            cx, cy = self.get_grid_pos()
            nx = cx + self.direction[0]
            ny = cy + self.direction[1]

            if not (0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0):
                # Hit a wall — pick new direction
                valid = []
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nnx, nny = cx + dx, cy + dy
                    if 0 <= nny < rows and 0 <= nnx < cols and grid[nny][nnx] == 0:
                        valid.append((dx, dy))
                if valid:
                    self.direction = random.choice(valid)
                else:
                    self.direction = (0, 0)

        self.pixel_x += self.direction[0] * self.speed
        self.pixel_y += self.direction[1] * self.speed

    def draw(self, surface: pygame.Surface) -> None:
        cx = int(self.pixel_x) + self.tile_size // 2
        cy = int(self.pixel_y) + self.tile_size // 2
        radius = self.tile_size // 2 - 3

        # Spiky appearance (rotating)
        angle_offset = self._frame * 0.05
        points = []
        num_spikes = 6
        for i in range(num_spikes * 2):
            angle = angle_offset + i * math.pi / num_spikes
            r = radius if i % 2 == 0 else radius // 2
            px = cx + int(r * math.cos(angle))
            py = cy + int(r * math.sin(angle))
            points.append((px, py))

        if len(points) >= 3:
            pygame.draw.polygon(surface, self.color, points)
            pygame.draw.polygon(surface, (255, 100, 100), points, width=1)
