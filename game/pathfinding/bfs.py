"""
bfs.py - Breadth-First Search pathfinding on a grid.

BFS explores all neighbours at the current depth before moving to
nodes at the next depth level.  On an *unweighted* grid this
guarantees the shortest path — every edge has cost 1.

Complexity:  O(V + E) where V = passable cells, E = their edges.
"""

from collections import deque

_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def find_path(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return the shortest path from *start* to *goal* using BFS.

    Parameters
    ----------
    grid : list[list[int]]
        2-D grid where 0 = passable, 1 = wall.
    start : (col, row)
    goal  : (col, row)

    Returns
    -------
    list[(col, row)]
        Ordered waypoints inclusive of start and goal.
        Empty list if unreachable.
    """
    if start == goal:
        return [start]

    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    # FIFO queue of positions to explore
    queue: deque[tuple[int, int]] = deque([start])
    came_from: dict[tuple[int, int], tuple[int, int]] = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            # --- Reconstruct path ---
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path

        cx, cy = current
        for dx, dy in _DIRECTIONS:
            nx, ny = cx + dx, cy + dy

            if not (0 <= ny < rows and 0 <= nx < cols):
                continue
            if grid[ny][nx] == 1:
                continue

            neighbour = (nx, ny)
            if neighbour not in came_from:
                came_from[neighbour] = current
                queue.append(neighbour)

    return []  # No path found
