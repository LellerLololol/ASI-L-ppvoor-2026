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
    SCATTER_DURATION, CHASE_DURATION, ENEMY_REPATH_INTERVAL,
    MAZE_COLS, MAZE_ROWS,
)
from game.pathfinding import astar, bfs, interceptor, wanderer


# Scatter target corners (col, row) — one per ghost
_SCATTER_CORNERS = [
    (MAZE_COLS - 2, 1),          # top-right   (Blinky)
    (1, 1),                      # top-left    (Pinky)
    (MAZE_COLS - 2, MAZE_ROWS - 2),  # bottom-right (Inky)
    (1, MAZE_ROWS - 2),          # bottom-left (Clyde)
]

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

        # States: "CHASE", "SCATTER", "FRIGHTENED", "EATEN"
        self.state: str = "SCATTER"

        self._path: list[tuple[int, int]] = []
        self._path_index: int = 0
        self._repath_cd: int = 0

        # Scatter/chase cycle timer (shared via class var, set by engine)
        self.scatter_target: tuple[int, int] = (1, 1)  # set per ghost

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
            self._repath_cd = ENEMY_REPATH_INTERVAL
            my_pos = self.get_grid_pos()

            if self.state == "EATEN":
                # Head back to spawn
                spawn = (self.spawn_x, self.spawn_y)
                self._path = astar.find_path(grid, my_pos, spawn)
                if my_pos == spawn:
                    self.state = "SCATTER"
                    self._path = []
            elif self.state == "FRIGHTENED":
                # Run away: pick a random direction
                self._path = []
                d = wanderer.get_random_direction(grid, my_pos, self.direction)
                self.direction = d
            elif self.state == "SCATTER":
                # Retreat to assigned corner
                self._path = astar.find_path(grid, my_pos, self._nearest_valid(grid, self.scatter_target))
            else:
                # CHASE — subclass-specific targeting
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

    def _nearest_valid(self, grid: list[list[int]], target: tuple[int, int]) -> tuple[int, int]:
        """Find the nearest passable cell to *target* (in case it's a wall)."""
        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        tc, tr = target
        if 0 <= tr < rows and 0 <= tc < cols and grid[tr][tc] == 0:
            return target
        for radius in range(1, max(rows, cols)):
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    r, c = tr + dr, tc + dc
                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                        return (c, r)
        return target

    def _is_tile_aligned(self) -> bool:
        return (
            self.pixel_x % self.tile_size == 0
            and self.pixel_y % self.tile_size == 0
        )

    def _follow_path(self, grid: list[list[int]]) -> None:
        """Move towards the next waypoint, with strict wall collision.

        Movement only occurs into cells that are verified as paths (0).
        Direction changes happen exclusively when tile-aligned.
        """
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        if self._is_tile_aligned():
            cx, cy = self.get_grid_pos()

            # Determine next desired direction
            next_dir = self.direction

            if self._path and self._path_index < len(self._path):
                # Follow the path
                target = self._path[self._path_index]
                dx = target[0] - cx
                dy = target[1] - cy

                # Clamp to unit direction
                if dx != 0:
                    dx = 1 if dx > 0 else -1
                if dy != 0:
                    dy = 1 if dy > 0 else -1

                next_dir = (dx, dy)
                self._path_index += 1
            elif self.direction == (0, 0):
                # Stopped with no path — pick a random direction
                next_dir = wanderer.get_random_direction(grid, (cx, cy), self.direction)
            else:
                # No path, already moving — check if we can keep going
                nx, ny = cx + self.direction[0], cy + self.direction[1]
                if not (0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0):
                    # Blocked — pick a new random valid direction
                    next_dir = wanderer.get_random_direction(grid, (cx, cy), self.direction)

            # Validate the chosen direction against the grid
            nx, ny = cx + next_dir[0], cy + next_dir[1]
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0:
                self.direction = next_dir
            else:
                # Even the chosen direction is blocked — stop
                self.direction = (0, 0)
                return

            # Snap pixel position to exact grid (prevents cumulative drift)
            self.pixel_x = cx * self.tile_size
            self.pixel_y = cy * self.tile_size

        # Only move if we have a valid direction
        if self.direction != (0, 0):
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
    def __init__(self, x, y, tile_size, speed, color):
        super().__init__(x, y, tile_size, speed, color)
        self.scatter_target = _SCATTER_CORNERS[0]

    def _choose_target(self, grid, player, all_enemies):
        return astar.find_path(grid, self.get_grid_pos(), player.get_grid_pos())


class Pinky(Enemy):
    """The Interceptor — targets the cell 4 tiles ahead of the player."""
    def __init__(self, x, y, tile_size, speed, color):
        super().__init__(x, y, tile_size, speed, color)
        self.scatter_target = _SCATTER_CORNERS[1]

    def _choose_target(self, grid, player, all_enemies):
        return interceptor.find_intercept_path(
            grid,
            self.get_grid_pos(),
            player.get_grid_pos(),
            player.direction,
        )


class Inky(Enemy):
    """The Tracker — uses BFS to flood-fill towards the player."""
    def __init__(self, x, y, tile_size, speed, color):
        super().__init__(x, y, tile_size, speed, color)
        self.scatter_target = _SCATTER_CORNERS[2]

    def _choose_target(self, grid, player, all_enemies):
        return bfs.find_path(grid, self.get_grid_pos(), player.get_grid_pos())


class Clyde(Enemy):
    """The Wanderer — random walk until within 8 tiles, then switches to A*."""
    def __init__(self, x, y, tile_size, speed, color):
        super().__init__(x, y, tile_size, speed, color)
        self.scatter_target = _SCATTER_CORNERS[3]

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
