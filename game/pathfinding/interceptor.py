"""
interceptor.py - Predictive targeting for the Interceptor ghost (Pinky).

Instead of chasing the player's *current* cell, the interceptor aims
for the cell several tiles *ahead* of the player's facing direction.
If that tile is a wall, it falls back to the nearest reachable path
cell in that general area.

Uses A* internally once the target is known.
"""

from game.pathfinding import astar

_DIRECTIONS_MAP = {
    (0, -1): "UP",
    (0, 1):  "DOWN",
    (-1, 0): "LEFT",
    (1, 0):  "RIGHT",
    (0, 0):  "NONE",
}

LOOK_AHEAD_TILES = 4  # How far ahead of the player to target


def get_intercept_target(
    player_pos: tuple[int, int],
    player_dir: tuple[int, int],
    grid: list[list[int]],
) -> tuple[int, int]:
    """Calculate the best interception target.

    Parameters
    ----------
    player_pos : (col, row)
    player_dir : (dx, dy) direction vector
    grid : 2-D grid

    Returns
    -------
    (col, row) of the target cell.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    # Project ahead of the player
    target_col = player_pos[0] + player_dir[0] * LOOK_AHEAD_TILES
    target_row = player_pos[1] + player_dir[1] * LOOK_AHEAD_TILES

    # Clamp to grid bounds
    target_col = max(0, min(cols - 1, target_col))
    target_row = max(0, min(rows - 1, target_row))

    # If the projected cell is passable, use it
    if grid[target_row][target_col] == 0:
        return (target_col, target_row)

    # Otherwise, spiral outwards to find the nearest open cell
    for radius in range(1, max(rows, cols)):
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                r, c = target_row + dr, target_col + dc
                if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                    return (c, r)

    # Fallback: just target the player directly
    return player_pos


def find_intercept_path(
    grid: list[list[int]],
    ghost_pos: tuple[int, int],
    player_pos: tuple[int, int],
    player_dir: tuple[int, int],
) -> list[tuple[int, int]]:
    """Full helper: compute target then A* to it.

    Returns the waypoint list from *ghost_pos* to the intercept target.
    """
    target = get_intercept_target(player_pos, player_dir, grid)
    return astar.find_path(grid, ghost_pos, target)
