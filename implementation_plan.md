# Pac-Man Style Game — Full Implementation Plan

A top-down, grid-based Pac-Man game built with **Python + Pygame**. Features procedural maze generation, four enemy ghosts each with a unique pathfinding algorithm, collectibles, power-ups, and a clean modular codebase.

---

## Project Structure

```
ASI-Lõppvoor-2026/
├── main.py                  # Entry point — initializes Game and runs the loop
├── game/
│   ├── __init__.py
│   ├── engine.py            # [NEW] Game class — state machine (MENU, PLAYING, GAME_OVER)
│   ├── settings.py          # [NEW] All constants (colors, sizes, speeds, FPS)
│   ├── maze/
│   │   ├── __init__.py
│   │   ├── generator.py     # [NEW] Recursive Backtracker maze generation
│   │   └── renderer.py      # [NEW] Draws the maze grid to screen
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── player.py        # [NEW] Player class — movement, animation, collision
│   │   └── enemy.py         # [NEW] Enemy base class + 4 subclasses (one per AI)
│   ├── pathfinding/
│   │   ├── __init__.py
│   │   ├── astar.py         # [NEW] A* shortest-path algorithm
│   │   ├── bfs.py           # [NEW] Breadth-First Search algorithm
│   │   ├── interceptor.py   # [NEW] Predictive heuristic targeting
│   │   └── wanderer.py      # [NEW] Random walk + proximity chase
│   └── items/
│       ├── __init__.py
│       └── collectibles.py  # [NEW] Dots, PowerUps, moving obstacles
├── assets/
│   └── PacManCharacter.png  # (existing)
├── AI_USAGE.md
└── README.md
```

---

## Phase 1: Maze Generation & Rendering (Bonus Targeted)

### Goal

Generate a random, solvable maze every time the game launches — no hardcoded map.

### Algorithm: Recursive Backtracker (Randomized DFS)

```
1. Create a grid of cells, all initially walled.
2. Pick a starting cell, mark it as visited.
3. While there are unvisited cells:
   a. If current cell has unvisited neighbors:
      - Choose one at random.
      - Remove the wall between current and chosen.
      - Push current to stack, move to chosen.
   b. Else:
      - Pop from stack (backtrack).
4. Result: a perfect maze (exactly one path between any two cells).
```

### Files

#### [NEW] [settings.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/settings.py)

- `CELL_SIZE = 32` — pixel size of each grid cell.
- `MAZE_COLS = 19`, `MAZE_ROWS = 27` — odd numbers so walls align to a grid.
- `SCREEN_WIDTH = MAZE_COLS * CELL_SIZE` (608px), `SCREEN_HEIGHT = MAZE_ROWS * CELL_SIZE + HUD_HEIGHT` (920px).
- Color palette, FPS (60), player speed, enemy speeds.

#### [NEW] [generator.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/maze/generator.py)

- `MazeGenerator` class.
- `generate() -> list[list[int]]` — returns a 2D grid where `0 = path`, `1 = wall`.
- Uses the Recursive Backtracker algorithm described above.
- Guarantees open starting area for player (bottom-center) and enemy spawn zone (top-center).

#### [NEW] [renderer.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/maze/renderer.py)

- `MazeRenderer` class.
- `draw(surface, grid)` — iterates the grid and draws walls as colored rectangles, paths as darker background.

#### [MODIFY] [main.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/main.py)

- Replace current scaffold with a thin entry point: instantiate `Game`, call `game.run()`.

#### [NEW] [engine.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/engine.py)

- `Game` class that owns the Pygame loop, state machine, and all subsystems.
- Phase 1 version: generates maze on init, renders it every frame.

### Deliverable

Running `python main.py` shows a different random maze each launch.

---

## Phase 2: Player Character & Mechanics

### Goal

A responsive, grid-snapped player that cannot clip through walls.

### Movement Model

- The player occupies exactly one grid cell at a time.
- On key press, set `desired_direction`. On each update tick, attempt to move in `desired_direction`; if blocked, keep moving in `current_direction` if possible.
- Movement is interpolated smoothly between cells over several frames (lerp position).
- Collision check: before committing a move, verify the target cell is `0` (path) in the grid.

### Files

#### [NEW] [player.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/entities/player.py)

- `Player` class.
- Properties: `grid_x`, `grid_y`, `pixel_x`, `pixel_y`, `direction`, `desired_direction`, `speed`.
- `update(grid, dt)` — attempt to move, interpolate pixel position.
- `draw(surface)` — render using the existing `PacManCharacter.png` sprite (scaled to `CELL_SIZE`).
- `check_collision(grid, direction) -> bool` — returns `True` if the next cell in that direction is a wall.

#### [MODIFY] [engine.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/engine.py)

- Create `Player` on game start at the player spawn position.
- Pass keyboard input to player, call `player.update()` and `player.draw()`.

### Deliverable

Player moves smoothly through the maze, stops at walls, responds to Arrow keys and WASD.

---

## Phase 3: Enemy AI & Pathfinding (Bonus Targeted)

### Goal

Four ghosts, each using a completely different pathfinding algorithm, producing visibly distinct behaviors.

### Enemy Base Class

#### [NEW] [enemy.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/entities/enemy.py)

- `Enemy` base class — same grid-snapped movement model as `Player`.
- Properties: `color`, `speed`, `state` (`CHASE`, `FRIGHTENED`, `EATEN`).
- Abstract method: `choose_target(player, grid) -> (int, int)`.
- Subclasses override `choose_target` and plug in their specific algorithm.

### The Four Ghosts

| Ghost | Name                        | Color  | Algorithm   | Behavior                                                    |
| ----- | --------------------------- | ------ | ----------- | ----------------------------------------------------------- |
| 1     | **Blinky** (The Chaser)     | Red    | A\*         | Shortest path directly to player's current cell             |
| 2     | **Pinky** (The Interceptor) | Pink   | Heuristic   | Targets the cell 4 tiles ahead of player's facing direction |
| 3     | **Inky** (The Tracker)      | Cyan   | BFS         | Flood-fills from its own position to find the player        |
| 4     | **Clyde** (The Wanderer)    | Orange | Random Walk | Random movement; switches to A\* when within 8-tile radius  |

### Pathfinding Files

#### [NEW] [astar.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/pathfinding/astar.py)

- `find_path(grid, start, goal) -> list[tuple]`
- Uses Manhattan distance as heuristic, binary heap for the open set.
- Returns list of `(col, row)` waypoints.

#### [NEW] [bfs.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/pathfinding/bfs.py)

- `find_path(grid, start, goal) -> list[tuple]`
- Standard BFS using a deque. Guarantees shortest path on unweighted grid.

#### [NEW] [interceptor.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/pathfinding/interceptor.py)

- `get_intercept_target(player_pos, player_dir, grid) -> (int, int)`
- Calculates a tile 4 cells ahead of player. If that tile is a wall, finds nearest valid path cell.
- Then uses A\* internally to route to that target.

#### [NEW] [wanderer.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/pathfinding/wanderer.py)

- `get_random_direction(grid, pos, current_dir) -> direction`
- At intersections: picks a random valid direction (never reverses).
- `is_in_range(pos, target, radius) -> bool` — proximity check to switch modes.

### Deliverable

Four colored ghosts roaming the maze with visually distinct movement patterns, all converging toward the player.

---

## Phase 4: Game Elements

### Goal

Dots, power-ups, a score display, a moving obstacle, and win/lose conditions.

### Items

#### [NEW] [collectibles.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/items/collectibles.py)

| Item                | Description                                 | Effect                                                                                           |
| ------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Dot**             | Small circle on every path cell             | +10 points. Collect all to win.                                                                  |
| **Power Pellet**    | Larger glowing circle (4 placed in corners) | +50 points. Ghosts enter `FRIGHTENED` state for 8 seconds — player can eat them for +200 points. |
| **Speed Boost**     | Lightning icon (spawns randomly every 30s)  | Player moves 1.5× speed for 5 seconds.                                                           |
| **Moving Obstacle** | A bouncing hazard that travels paths        | Kills player on contact (unless powered up). Follows a simple patrol route.                      |

### Scoring & HUD

- HUD bar at the bottom of the screen: **Score**, **Lives** (3), **Active Power-Up timer**.
- Win condition: all dots collected.
- Lose condition: lives reach 0.
- Game Over screen with final score and "Press R to Restart".

#### [MODIFY] [engine.py](file:///Users/kds/Code/ASI-Lõppvoor-2026/game/engine.py)

- State machine: `MENU → PLAYING → GAME_OVER`.
- Spawn dots on all path cells, place power pellets, manage timers.
- Collision detection between player ↔ dots, player ↔ enemies, player ↔ obstacles.

### Deliverable

Fully playable game with scoring, lives, power-ups, and win/lose screens.

---

## Phase 5: Code Polish & Documentation

### Goal

Clean, readable, well-documented code that scores highly on structure and elegance.

### Tasks

1. **Docstrings**: Every class and public method gets a clear docstring.
2. **Type hints**: All function signatures use Python type hints.
3. **Algorithm comments**: Inline comments in `generator.py`, `astar.py`, `bfs.py` explaining each step of the algorithm.
4. **README.md update**: How to install, how to run, game controls, project structure overview.
5. **requirements.txt**: Pin `pygame` version.
6. **Final cleanup**: Remove dead code, ensure consistent naming (`snake_case`), verify no circular imports.

#### [MODIFY] [README.md](file:///Users/kds/Code/ASI-Lõppvoor-2026/README.md)

- Project description, screenshot, install instructions, controls, architecture overview.

#### [NEW] [requirements.txt](file:///Users/kds/Code/ASI-Lõppvoor-2026/requirements.txt)

- `pygame>=2.5.0`

---

## Verification Plan

### Automated / Script-Based

Since Pygame is a graphical application, traditional unit tests are limited. We will use the following approach:

1. **Maze generation validation script** (`/tmp/test_maze.py`):
   - Generate 100 mazes, verify each has exactly one connected component (flood fill from start reaches all path cells).
   - Verify player spawn and enemy spawn are on path cells.
   - Run: `python /tmp/test_maze.py`

2. **Pathfinding validation script** (`/tmp/test_pathfinding.py`):
   - For a generated maze, run A\* and BFS from the same start/goal and verify both find a valid path.
   - Verify A\* path length ≤ BFS path length (they should be equal on an unweighted grid).
   - Run: `python /tmp/test_pathfinding.py`

### Manual Verification

3. **Visual maze test**: Run `python main.py` three times — confirm a different maze appears each time.
4. **Player movement test**: Use arrow keys and WASD to move the player. Confirm:
   - Player cannot walk through walls.
   - Movement feels smooth (not teleporting between cells).
5. **Enemy AI test**: Observe the four ghosts:
   - Red ghost (Blinky) should pursue the player aggressively.
   - Pink ghost (Pinky) should try to get ahead of the player.
   - Cyan ghost (Inky) should approach from a different angle than Blinky.
   - Orange ghost (Clyde) should wander randomly until close, then chase.
6. **Collectibles test**: Walk over dots and power pellets, confirm score updates. Eat a power pellet and verify ghosts turn blue/frightened and can be eaten.
7. **Win/Lose test**: Collect all dots → win screen. Die 3 times → game over screen.
