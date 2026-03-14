---
name: Core Game Engine Setup
description: Guide on the central game loop, state management, and Pygame integration in ASI-Lõppvoor-2026.
---

# Core Game Engine

The entry point of the game is `main.py`, which simply instantiates the `Game` class from `game/engine.py`.

## `game/engine.py`

This is the central controller of the game, managing state, the Pygame loop, and orchestrating updates across all entities.

### Key Responsibilities

1. **State Machine**: The game operates strictly on a state machine via strings (`STATE_PLAYING`, `STATE_GAME_OVER`, `STATE_WIN`, `STATE_START_DELAY`). Modifying the game flow usually requires interacting with these states.
2. **Setup (`_setup_new_game`)**: Generates the maze, places items, initializes the player and ghost instances.
3. **The Update Loop (`_update`)**:
   - Ticks all gameplay timers (power up, scatter/chase modes, speed boosts).
   - Handles Ghost mode switching (Scatter vs Chase) globally based on a timer. Reverses ghost direction on mode switch.
   - Moves the player and checks for item collision (Dots, Power Pellets, Speed Boosts). Item collisions use `pygame.Rect.colliderect` with a shrunken `margin=6` hitbox to make grazing forgiving.
   - Updates enemies and handles Entity-to-Player collision (killing the player or eating the enemy).
4. **Audio Subsystem**: Initializes `pygame.mixer.music` to play and seamlessly swap between `assets/bgm_normal.wav` and a 1.5x sped-up `assets/bgm_fast.wav` based on the player's current speed boost state.

## Best Practices & Guidelines

- **Modifying State Logic**: Ensure changes respect the `STATE_START_DELAY` countdown. Entities should not update while in `START_DELAY`.
- **Collisions**: The game transitioned _away_ from integer grid-based collisions (`if target == player_grid`) to forgiving Pygame Rects with a 6-pixel margin for entity-item collisions. When adding new collectables or hazards, follow the `obs_rect.colliderect(player_rect)` pattern in `engine.py`.
- **Audio Integration**: Audio tracks are swapped dynamically using `get_pos()` to calculate playback position. Do not call `.play()` blindly without preserving time continuity if the powerup state changes.
