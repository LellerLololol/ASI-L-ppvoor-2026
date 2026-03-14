---
name: Maze Generation & Rendering
description: Guide on procedural maze generation (Recursive Backtracker) and Pygame rendering.
---

# Maze Generation & Rendering

The game does not use hardcoded maps. A new map is procedurally generated via a Depth-First Search algorithm on startup.

## `game/maze/generator.py`

### Process:

1. Initialize an array of `1`s (walls).
2. Start an explicit stack recursive backtracker. It carves paths `0` by randomly selecting neighbors 2 tiles away and breaking the wall between them. This guarantees exactly one solvable continuous path spanning the entire board.
3. Automatically breaks down a configurable random percentage of walls (`MAZE_EXTRA_OPENINGS = 0.08`) to create loops, avoiding the maze feeling like a frustrating dead-end tree.
4. Carves out the player spawn at the bottom center, and an enemy spawn box near the top center (represented by integer `2` instead of `0`). It deliberately punches a hole `grid[1][center_col] = 0` so ghosts can exit the spawn box.

## `game/maze/renderer.py`

To maintain a high frame rate, the maze walls are NOT drawn every frame.

- **Surface Caching**: The maze geometry (which never changes inside a round) is drawn once onto `_cached_surface`. During gameplay, the engine simply blits this pre-rendered image.
- **Dynamic Elements**: Things that change (Player, ghosts, items, HUD, start delay text) are drawn dynamically on top.
- If you need to redraw the maze geometry (e.g. dynamic destruction or map shift), you must call `renderer.invalidate_cache()`.
