"""
wanderer.py - Random-walk logic for the Wanderer ghost (Clyde).

The wanderer picks random valid directions at intersections (never
reverses unless it's a dead end).  When it comes within a configurable
radius of the player, it switches to A* for a direct chase.
"""

import random
from game.pathfinding import astar
from game.settings import CLYDE_CHASE_RADIUS

_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Opposite direction lookup for preventing 180° turns
_OPPOSITE = {
    (0, -1): (0, 1),
    (0, 1):  (0, -1),
    (-1, 0): (1, 0),
    (1, 0):  (-1, 0),
    (0, 0):  (0, 0),
}


def is_in_range(
    pos: tuple[int, int],
    target: tuple[int, int],
    radius: int = CLYDE_CHASE_RADIUS,
) -> bool:
    """Return True if *pos* is within *radius* Manhattan tiles of *target*."""
    return abs(pos[0] - target[0]) + abs(pos[1] - target[1]) <= radius


def get_random_direction(
    grid: list[list[int]],
    pos: tuple[int, int],
    current_dir: tuple[int, int],
) -> tuple[int, int]:
    """Choose a random passable direction at *pos*.

    Avoids reversing unless there is no other option (dead end).

    Parameters
    ----------
    grid : 2-D grid (0 = path, 1 = wall)
    pos : (col, row) current position
    current_dir : (dx, dy) current movement direction

    Returns
    -------
    (dx, dy) chosen direction vector.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    cx, cy = pos

    # Gather all valid directions (passable neighbour)
    valid = []
    for dx, dy in _DIRECTIONS:
        nx, ny = cx + dx, cy + dy
        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] != 1:
            valid.append((dx, dy))

    if not valid:
        return (0, 0)  # completely stuck (shouldn't happen in a connected maze)

    # Prefer directions that are NOT the reverse of current
    non_reverse = [d for d in valid if d != _OPPOSITE.get(current_dir, (0, 0))]
    choices = non_reverse if non_reverse else valid

    return random.choice(choices)


def get_wanderer_action(
    grid: list[list[int]],
    ghost_pos: tuple[int, int],
    ghost_dir: tuple[int, int],
    player_pos: tuple[int, int],
) -> list[tuple[int, int]] | None:
    """Decide whether to wander randomly or chase.

    Returns
    -------
    list[(col, row)] if within chase radius (A* path), else None
    (caller should use ``get_random_direction`` instead).
    """
    if is_in_range(ghost_pos, player_pos):
        path = astar.find_path(grid, ghost_pos, player_pos)
        if path:
            return path
    return None
