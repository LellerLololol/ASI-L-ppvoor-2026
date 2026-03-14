"""
astar.py - A* (A-star) shortest-path algorithm on a grid.

A* combines the actual distance from the start (g-cost) with a
heuristic estimate to the goal (h-cost) so it expands far fewer
nodes than a brute-force search while still guaranteeing the
shortest path.

Complexity:  O(E log V) where E = edges, V = vertices.
Heuristic:   Manhattan distance (admissible for 4-directional grids).
"""

import heapq

# 4-directional movement
_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def find_path(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return the shortest path from *start* to *goal* as a list of (col, row).

    Parameters
    ----------
    grid : list[list[int]]
        2-D grid where 0 = passable, 1 = wall.
    start : (col, row)
        Starting cell.
    goal : (col, row)
        Target cell.

    Returns
    -------
    list[(col, row)]
        Ordered waypoints from start to goal (inclusive).
        Empty list if no path exists.
    """
    if start == goal:
        return [start]

    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    # --- Heuristic: Manhattan distance ---
    def h(pos: tuple[int, int]) -> int:
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    # Open set: min-heap of (f_score, tie-breaker, (col, row))
    counter = 0
    open_set: list[tuple[int, int, tuple[int, int]]] = []
    heapq.heappush(open_set, (h(start), counter, start))

    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score: dict[tuple[int, int], int] = {start: 0}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == goal:
            # --- Reconstruct path ---
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        cx, cy = current
        for dx, dy in _DIRECTIONS:
            nx, ny = cx + dx, cy + dy

            # Bounds and wall check
            if not (0 <= ny < rows and 0 <= nx < cols):
                continue
            if grid[ny][nx] == 1:
                continue

            neighbour = (nx, ny)
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbour, float("inf")):
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g
                f = tentative_g + h(neighbour)
                counter += 1
                heapq.heappush(open_set, (f, counter, neighbour))

    return []  # No path found
