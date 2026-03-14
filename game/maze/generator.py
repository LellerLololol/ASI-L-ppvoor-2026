"""
generator.py - Procedural maze generation using the Recursive Backtracker.

Algorithm (Randomised Depth-First Search):
    1.  Start with a grid where every cell is a wall.
    2.  Pick a starting cell (must be at an odd row/col so walls line up),
        mark it as a path, and push it onto a stack.
    3.  While the stack is not empty:
        a.  Look at all neighbours two steps away (N, S, E, W) that are
            still walls.
        b.  If at least one exists, pick one at random, carve the wall
            between the current cell and the chosen neighbour, mark the
            neighbour as a path, and push the neighbour onto the stack.
        c.  If none exist, pop the stack (backtrack).
    4.  The result is a *perfect* maze — exactly one path between any two
        cells, guaranteed solvable.

After generation a handful of extra walls are removed at random to create
loops and make the maze feel more like a classic Pac-Man board.
"""

import random
from game.settings import MAZE_COLS, MAZE_ROWS, MAZE_EXTRA_OPENINGS


class MazeGenerator:
    """Generates a random grid-based maze.

    The grid uses integer encoding:
        0 = path (passable)
        1 = wall (impassable)

    Parameters
    ----------
    cols : int
        Number of columns (should be odd).
    rows : int
        Number of rows (should be odd).
    """

    def __init__(self, cols: int = MAZE_COLS, rows: int = MAZE_ROWS):
        # Force odd dimensions so border walls are consistent
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.rows = rows if rows % 2 == 1 else rows + 1

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate(self) -> list[list[int]]:
        """Return a 2-D grid ``grid[row][col]`` of 0s and 1s.

        Also carves spawn zones for the player and enemies, and opens
        extra corridors to create loops.
        """
        grid = self._init_grid()
        self._carve_passages(grid)
        self._open_extra_corridors(grid)
        #self._carve_player_spawn(grid)
        self._carve_enemy_spawn(grid)
        return self.generate_suitable(grid)

    def generate_suitable(self, grid):
        target = (self.cols // 2, self.rows - 2)
        if grid[target[1]][target[0]] == 1:
            return self.generate()
        return grid

    # ------------------------------------------------------------------
    # Step 1 — blank grid (all walls)
    # ------------------------------------------------------------------
    def _init_grid(self) -> list[list[int]]:
        """Create a cols×rows grid filled with walls (1)."""
        return [[1] * self.cols for _ in range(self.rows)]

    # ------------------------------------------------------------------
    # Step 2 — Recursive Backtracker
    # ------------------------------------------------------------------
    def _carve_passages(self, grid: list[list[int]]) -> None:
        """Run the Recursive Backtracker starting from cell (1, 1).

        The algorithm uses an explicit stack (instead of recursion) to
        avoid hitting Python's recursion limit on large mazes.
        """
        start_row, start_col = (1, 1)
        grid[start_row][start_col] = 0          # mark start as path

        stack: list[tuple[int, int]] = [(start_row, start_col)]
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # N, S, W, E

        while stack:
            row, col = stack[-1]

            # Collect unvisited neighbours (two cells away)
            neighbours = []
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 < nr < self.rows - 1 and 0 < nc < self.cols - 1:
                    if grid[nr][nc] == 1:        # still a wall → unvisited
                        neighbours.append((nr, nc, dr, dc))

            if neighbours:
                # Pick a random neighbour
                nr, nc, dr, dc = random.choice(neighbours)
                # Remove the wall between current cell and neighbour
                grid[row + dr // 2][col + dc // 2] = 0
                grid[nr][nc] = 0
                stack.append((nr, nc))
            else:
                # Dead end — backtrack
                stack.pop()

    # ------------------------------------------------------------------
    # Step 3 — Extra openings (create loops)
    # ------------------------------------------------------------------
    def _open_extra_corridors(self, grid: list[list[int]]) -> None:
        """Remove a fraction of interior walls to create loops.

        This prevents the maze from being a strict tree, making it feel
        more like a classic Pac-Man level with multiple routes.
        """
        interior_walls: list[tuple[int, int]] = []
        for r in range(2, self.rows - 2):
            for c in range(2, self.cols - 2):
                if grid[r][c] == 1:
                    # Only consider walls that separate two path cells
                    # (removing them would connect two corridors)
                    adj_paths = sum(
                        1 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if grid[r + dr][c + dc] == 0
                    )
                    if adj_paths >= 2:
                        interior_walls.append((r, c))

        num_to_open = int(len(interior_walls) * MAZE_EXTRA_OPENINGS)
        for r, c in random.sample(interior_walls, min(num_to_open, len(interior_walls))):
            grid[r][c] = 0

    # ------------------------------------------------------------------
    # Step 4 — Spawn zones
    # ------------------------------------------------------------------
    def _carve_player_spawn(self, grid: list[list[int]]) -> None:
        """Clear a small area at the bottom-center for the player spawn."""
        center_col = self.cols // 2
        bottom_row = self.rows - 2
        for dr in range(0, 3):
            for dc in range(-1, 2):
                r, c = bottom_row - dr, center_col + dc
                if 0 < r < self.rows - 1 and 0 < c < self.cols - 1:
                    grid[r][c] = 0

    def _carve_enemy_spawn(self, grid: list[list[int]]) -> None:
        """Clear a small box near the top-center for the enemy spawn."""
        center_col = self.cols // 2
        top_row = 2
        for dr in range(0, 3):
            for dc in range(-1, 2):
                r, c = top_row + dr, center_col + dc
                if 0 < r < self.rows - 1 and 0 < c < self.cols - 1:
                    grid[r][c] = 2

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def get_player_spawn(self) -> tuple[int, int]:
        """Return the (col, row) grid coordinate for the player spawn."""
        return (self.cols // 2, self.rows - 2)

    def get_enemy_spawns(self) -> list[tuple[int, int]]:
        """Return four (col, row) grid coordinates for enemy spawns."""
        cx = self.cols // 2
        return [
            (cx - 1, 3),   # Blinky
            (cx,     3),   # Pinky
            (cx + 1, 3),   # Inky
            (cx,     2),   # Clyde
        ]
