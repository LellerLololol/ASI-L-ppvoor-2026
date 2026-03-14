---
name: AI Pathfinding Behaviors
description: Guide on the ghost pathfinding algorithms (A*, BFS, Wanderer) and state cycles.
---

# AI Pathfinding Behaviors

The classic 4 Pac-Man ghosts each feature distinct movement logic, orchestrated by `Enemy._choose_target()` in `game/entities/enemy.py`, supported by modular algorithms in `game/pathfinding/`.

## The Algorithms

1. **`astar.py`**: A standard A\* heuristic pathfinder using Manhattan distance. This is the primary workhorse for ghosts determining the absolute shortest path to a kill. Extended to support `ignore_walls=True` so dead ghosts can fly straight back to spawn.
2. **`bfs.py`**: A Breadth-First-Search pathfinder. Used minimally.
3. **`wanderer.py`**: Custom ghost "fallback" AI. When a ghost has no destination or loses the player, it picks random valid paths. **Crucially, it is programmed not to Reverse direction by 180-degrees** unless it enters a 3-wall dead end, mimicking classic Pac-Man restrictions.

## Ghost Archetypes (`game/entities/enemy.py`)

- **Blinky**: Aggressive. Straight A\* pathing to the player's exact coordinate at all times. Scatter target: Top Right.
- **Pinky**: Ambusher. A* paths 4 tiles *ahead\* of the player's current direction. Scatter target: Top Left.
- **Inky**: Interceptor. Uses BFS pathing to find alternative flanking routes to the player. Scatter target: Bottom Right.
- **Clyde**: Territorial. Uses `wanderer` randomly. But if he gets within 8 tiles of the player, he switches to an aggressive A\* chase. Scatter target: Bottom Left.

## Path Execution

Ghosts do not calculate A* every single frame (it would kill the CPU). They calculate a multi-step `self._path` array. They follow it step-by-step. They only recalculate a new A* path every `ENEMY_REPATH_INTERVAL` frames (set to 20 tick cycles).
