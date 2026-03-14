"""
enemy.py - Ghost enemies with distinct AI behaviours.

Base class ``Enemy`` handles grid-snapped movement and rendering.
Four concrete subclasses override ``_choose_target`` to plug in
different pathfinding strategies:

    Blinky  — A* direct chase
    Pinky   — Intercept (aim ahead of the player)
    Inky    — BFS flood-fill
    Clyde   — Random wander until close, then A*
"""

import math
import pygame

from game.settings import (
    CELL_SIZE, ENEMY_SPEED, ENEMY_FRIGHTENED_SPEED, ENEMY_EATEN_SPEED,
    COLOR_FRIGHTENED, COLOR_EYES,
)
from game.pathfinding import astar, bfs, interceptor, wanderer


# Refresh pathfinding every N frames (avoids recalculating every tick)
_REPATH_INTERVAL = 10

# 4-directional movement
_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


class Enemy:
    """Base ghost class with grid-snapped movement.

    Parameters
    ----------
    x, y : int
        Starting position in grid coordinates (col, row).
    tile_size : int
        Pixel size of one grid cell.
    speed : int
        Pixels moved per frame (must divide tile_size evenly).
    color : tuple
        RGB colour for this ghost.
    """

    def __init__(
        self,
        x: int,
        y: int,
        tile_size: int,
        speed: int,
        color: tuple[int, int, int],
    ):
        self.tile_size = tile_size
        self.base_speed = speed
        self.speed = speed
        self.color = color

        self.spawn_x = x
        self.spawn_y = y
        self.pixel_x: float = x * tile_size
        self.pixel_y: float = y * tile_size
        self.direction: tuple[int, int] = (0, 0)

        # States: "CHASE", "FRIGHTENED", "EATEN"
        self.state: str = "CHASE"

        self._path: list[tuple[int, int]] = []
        self._path_index: int = 0
        self._repath_cd: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def update(
        self,
        grid: list[list[int]],
        wall_rects: list[pygame.Rect],
        player,
        all_enemies: list,
    ) -> None:
        """Advance one frame of enemy logic."""
        # Adjust speed based on state
        if self.state == "FRIGHTENED":
            self.speed = ENEMY_FRIGHTENED_SPEED
        elif self.state == "EATEN":
            self.speed = ENEMY_EATEN_SPEED
        else:
            self.speed = self.base_speed

        # Only recalculate path periodically
        self._repath_cd -= 1
        if self._repath_cd <= 0 and self._is_tile_aligned():
            self._repath_cd = _REPATH_INTERVAL
            my_pos = self.get_grid_pos()

            if self.state == "EATEN":
                # Head back to spawn
                spawn = (self.spawn_x, self.spawn_y)
                self._path = astar.find_path(grid, my_pos, spawn)
                if my_pos == spawn:
                    self.state = "CHASE"
                    self._path = []
            elif self.state == "FRIGHTENED":
                # Run away: pick a random direction
                self._path = []
                d = wanderer.get_random_direction(grid, my_pos, self.direction)
                self.direction = d
            else:
                # Subclass-specific targeting
                self._path = self._choose_target(grid, player, all_enemies)

            self._path_index = 1  # skip index 0 (current pos)

        # Follow the computed path
        self._follow_path(grid)

    def draw(self, surface: pygame.Surface) -> None:
        """Render the ghost onto *surface*."""
        cx = int(self.pixel_x) + self.tile_size // 2
        cy = int(self.pixel_y) + self.tile_size // 2
        radius = self.tile_size // 2 - 2

        if self.state == "EATEN":
            # Just eyes returning to spawn
            self._draw_eyes(surface, cx, cy, radius)
            return

        # Body colour
        body_color = COLOR_FRIGHTENED if self.state == "FRIGHTENED" else self.color

        # Ghost body: semicircle top + wavy bottom
        body_rect = pygame.Rect(
            cx - radius, cy - radius,
            radius * 2, radius * 2,
        )
        # Draw main circle
        pygame.draw.circle(surface, body_color, (cx, cy - 2), radius)
        # Draw bottom rectangle (skirt)
        skirt_rect = pygame.Rect(cx - radius, cy - 2, radius * 2, radius)
        pygame.draw.rect(surface, body_color, skirt_rect)

        # Wavy bottom edge
        wave_y = cy + radius - 4
        num_waves = 3
        wave_width = (radius * 2) // num_waves
        for i in range(num_waves):
            wx = cx - radius + i * wave_width + wave_width // 2
            pygame.draw.circle(surface, body_color, (wx, wave_y), wave_width // 2)

        # Eyes
        self._draw_eyes(surface, cx, cy, radius)

    # ------------------------------------------------------------------
    # Subclass hook
    # ------------------------------------------------------------------
    def _choose_target(
        self,
        grid: list[list[int]],
        player,
        all_enemies: list,
    ) -> list[tuple[int, int]]:
        """Return a path (list of grid coords) towards the target.

        Must be overridden by subclasses.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def get_grid_pos(self) -> tuple[int, int]:
        """Return (col, row) grid position."""
        return (
            int(self.pixel_x // self.tile_size),
            int(self.pixel_y // self.tile_size),
        )

    def _is_tile_aligned(self) -> bool:
        return (
            self.pixel_x % self.tile_size == 0
            and self.pixel_y % self.tile_size == 0
        )

    def _follow_path(self, grid: list[list[int]]) -> None:
        """Move towards the next waypoint in the current path."""
        if not self._path or self._path_index >= len(self._path):
            # No path — keep moving in current direction if possible
            if self.direction != (0, 0):
                cx, cy = self.get_grid_pos()
                nx, ny = cx + self.direction[0], cy + self.direction[1]
                rows, cols = len(grid), len(grid[0])
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0:
                    self.pixel_x += self.direction[0] * self.speed
                    self.pixel_y += self.direction[1] * self.speed
                else:
                    # Pick a new random direction when hitting a wall
                    d = wanderer.get_random_direction(grid, (cx, cy), self.direction)
                    self.direction = d
            return

        # Move towards the next waypoint
        if self._is_tile_aligned():
            target = self._path[self._path_index]
            my_pos = self.get_grid_pos()
            dx = target[0] - my_pos[0]
            dy = target[1] - my_pos[1]

            # Clamp to unit direction
            if dx != 0:
                dx = dx // abs(dx)
            if dy != 0:
                dy = dy // abs(dy)

            self.direction = (dx, dy)
            self._path_index += 1

        self.pixel_x += self.direction[0] * self.speed
        self.pixel_y += self.direction[1] * self.speed

    def _draw_eyes(self, surface: pygame.Surface, cx: int, cy: int, radius: int) -> None:
        """Draw ghost eyes with pupils looking in movement direction."""
        eye_radius = max(3, radius // 3)
        pupil_radius = max(1, eye_radius // 2)
        eye_y = cy - 4

        for sign in (-1, 1):
            ex = cx + sign * (radius // 3)
            # White of the eye
            pygame.draw.circle(surface, COLOR_EYES, (ex, eye_y), eye_radius)
            # Pupil shifted in movement direction
            px = ex + self.direction[0] * 2
            py = eye_y + self.direction[1] * 2
            pygame.draw.circle(surface, (0, 0, 100), (px, py), pupil_radius)


# ======================================================================
# Concrete ghost subclasses
# ======================================================================

class Blinky(Enemy):
    """The Chaser — uses A* to find the shortest path directly to the player."""

    def _choose_target(self, grid, player, all_enemies):
        return astar.find_path(grid, self.get_grid_pos(), player.get_grid_pos())


class Pinky(Enemy):
    """The Interceptor — targets the cell 4 tiles ahead of the player."""

    def _choose_target(self, grid, player, all_enemies):
        return interceptor.find_intercept_path(
            grid,
            self.get_grid_pos(),
            player.get_grid_pos(),
            player.direction,
        )


class Inky(Enemy):
    """The Tracker — uses BFS to flood-fill towards the player."""

    def _choose_target(self, grid, player, all_enemies):
        return bfs.find_path(grid, self.get_grid_pos(), player.get_grid_pos())


class Clyde(Enemy):
    """The Wanderer — random walk until within 8 tiles, then switches to A*."""

    def _choose_target(self, grid, player, all_enemies):
        result = wanderer.get_wanderer_action(
            grid,
            self.get_grid_pos(),
            self.direction,
            player.get_grid_pos(),
        )
        if result is not None:
            return result
        # Random direction handled in the base update via empty path
        return []
