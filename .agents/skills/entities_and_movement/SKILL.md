---
name: Entities and Movement
description: Guide on the robust pixel-by-pixel float-accumulator movement logic for the Player and Ghosts.
---

# Entities and Movement

The project features a highly robust custom pixel-by-pixel movement system capable of handling complex floating-point fractional speeds cleanly.

## `player.py` (`Player`)

The player character is controlled via keyboard inputs but moves strictly along the grid lines.

### Key Mechanics:

- **Fractional Speed Accumulator**: The player defines `speed = 3` (or `4.5` during a 1.5x boost). To process fractional pixels without precision loss or truncation, movement uses a `movement_accum` float queue. Every frame, `speed` is added to the accumulator, the integer part is extracted via `int()`, and the player moves exactly that many discrete pixels.
- **Pixel-by-Pixel Movement**: The extracted `pixels_to_move` integer runs a loop `for _ in range(pixels_to_move):`. At _every single pixel_ step, the player checks if they are perfectly tile-aligned (`_is_tile_aligned()`).
- **Grid Turning**: The player can only perform 90-degree turns when `_is_tile_aligned()` returns `True` (i.e., `pixel_x % 32 == 0`). A `queued_direction` allows players to press turn keys slightly early. 180-degree reversals are allowed instantly anywhere.
- **Wall Collisions**: `_can_move_dist` mathematically calculates which grid cells the player's bounding box will overlap. It queries the 2D array `grid` directly instead of iterating through rectangle arrays. **Treats values `1` (wall) and `2` (enemy spawn box) as impassable.**

## `game/entities/enemy.py` (`Enemy` and subclasses)

Ghosts use the exact same float accumulator and pixel-by-pixel movement logic as the player to guarantee they never drift off the absolute grid lines, even when traveling at speeds like `1.5` or `2.4`.

### Key Mechanics:

- Every pixel moved, if `_is_tile_aligned()`, the ghost executes its AI (A\* or Wanderer) to pick the next direction.
- **EATEN State Wall Pass-Through**: When eaten, ghosts immediately ignore `grid[ny][nx] != 1` checks and float directly through the map back to their `spawn_x, spawn_y`.

## Best Practices

- **Never rely on modulo math alone to detect movement boundaries** for game logic without the pixel-by-pixel accumulator loop. Because speeds are fractional, an entity's coordinate might jump from `30` to `33`, missing the `32` intersection entirely. The accumulator loop guarantees `30 -> 31 -> 32 (trigger alignment) -> 33`.
