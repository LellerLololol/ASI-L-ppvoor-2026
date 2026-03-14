---
name: Collectible Items and Hazards
description: Guide on the dots, power pellets, speed boosts, and moving obstacles in ASI-Lõppvoor-2026.
---

# Collectible Items and Hazards

The game features several types of pickups and one specific environmental hazard, all defined in `game/items/collectibles.py`.

## Collectible Types

1. **Dot**: The core score item. Collecting all dots triggers the `STATE_WIN` condition in `engine.py`.
2. **PowerPellet**: Causes all ghosts to enter the `FRIGHTENED` state for a fixed duration (`POWER_UP_DURATION`). Rendered with a glowing, pulsing animation.
3. **SpeedBoost**: Grants the player a 1.5x speed multiplier for 5 seconds. This also triggers the background music to speed up to `assets/bgm_fast.wav`.

## Movement and Collision

- Items are stationary (except `MovingObstacle`) and initialized at a specific `grid_pos`.
- Collision is handled in `game/engine.py` using a 6-pixel margin: `pygame.Rect(item.pixel_pos...).colliderect(player_rect)`.
- **MovingObstacle**: A unique hazard that patrols the corridors. It uses the same **fractional speed accumulator** and **pixel-by-pixel** movement as the Player and Ghosts. It bounces off walls by picking a new valid direction from the `grid` when it hits an intersection.

## Best Practices

- When adding a new item, ensure you register its collision handler in `engine.py` using the `Rect.colliderect` method with an appropriate margin to keep the gameplay feel "forgiving".
- Items like `SpeedBoost` and `PowerPellet` are placed randomly on available `0` (path) tiles during maze generation. Ensure new items follow this pattern to avoid items spawning inside walls.
