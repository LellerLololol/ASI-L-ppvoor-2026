# AI Usage Documentation

This file tracks all AI usage within this project. To maintain a transparent and trackable history, all AI-assisted development must adhere strictly to the following rules based on the previous workspace's standards.

## Rules for AI Usage

1. **Separation by Prompts**: All documentation must be separated by the prompts given to the AI. Each prompt gets its own dedicated section.
2. **Commit Tracking**: Every single commit that was made during the generation of a specific prompt needs to be listed in that prompt's section. This ensures we can track exactly what commits were due to what prompts.
3. **Chronological Order**: The commits under each section must be listed in order.
4. **Descriptive Messages**: Commit messages must be descriptive and clearly state what was changed.
5. **Containment**: All AI usage documentation must be contained exclusively within this file.
6. **Prompt Entry**: Since the AI does not always know the exact prompt that initiated a task, the user will manually copy and paste the prompt into the documentation.

## Required Structure

Each prompt section must follow this exact format:

### Prompt [nr]

**The prompt:**

> [Copy and paste the user's prompt here]

**Commits:**

- `[Commit Hash]` - [Commit message]
- `[Commit Hash]` - [Commit message]

**Explanation of changes:**
[A clear and concise explanation of the changes that this prompt made to the repository.]

---

_(Example usage below based on the previous structure)_

### Prompt 1

**The prompt:**

> "We have to document ALL ai usage in this github project that we are going to do. I have an example file from a previous workspace that did a similar thing (
> AI_USAGE.md
> ) Format it to MD and explain the rules of the ai usage CLEARY and as they are given to you in the example file. The gist of it is that everything needs to be separated by prompts and every commit that came during the generation of that one prompt needs to go to that prompts section, so we can track exactly what commits where due to what prompts. The commits should all be in order and the commit messages should be descriptive. All AI usage should be contained to this file. Since you don't exactly know what the prompt is, i will copy it myself. So a section will look like this: Prompt nr
> The prompt
> Commit hashes with commit messages
> An explanation of the changes this prompt made to the repo.
> Continue"

**Commits:**

- No commits made

**Explanation of changes:**
Set up the AI_USAGE.md file with the agreed-upon rules and template format for tracking AI contributions based on the first prompt.

---

### Prompt 2

**The prompt:**

> "Also give the final commit command aswell to manually run and enter to the docs aswell"

**Commits:**

- `c3716d73654e3a1d859be45ee54fe3cf7436f802` - docs: Format AI_USAGE.md rules and add AI logs for Prompts 1 and 2

**Explanation of changes:**
Filled in the correct details for Prompt 1 and added the documentation section for Prompt 2, inserting placeholders for the commit hashes as requested.

---

### Prompt 3

**The prompt:**

> "THIS IS PERFECT! Create an antigravity agent skill file for this because yo understood it so perfectly."
> "Update the ai_usage docs to relfect your last changes"

**Commits:**

- `d8c5407ccb9bd44c11cf41c11769364683e64838` - build: Create AI Usage Documentation Agent Skill

**Explanation of changes:**
Created the `.agents/skills/document_ai_usage/SKILL.md` file to formalize the project's AI tracking rules as an agent "skill". This automatically instructs all future AI agents operating in this workspace on how to correctly document their usage in `AI_USAGE.md`.

---

### Prompt 4

**The prompt:**

> Create the Pac-Man player character and movement system using Pygame. The code should be well-structured and clean. My part of the assignment is creating the character and making the movement. Use my hand-made 16x16 pixel art sprite (`assets/PacManCharacter.png`). Only create files directly connected to my part — just `player.py`, no settings or game loop files. Support both WASD and arrow keys. Make speed, squash & stretch strength, and all visual parameters configurable variables (don't hardcode anything). The sprite's eyes already exist in the pixel art, so position any overlay eyes correctly. Flip the character sprite to face the direction of movement.

**Commits:**

- `7df8635f27345b2361035a9ddb3ca4057f8e3230` - feat: Add Player class with grid-aligned movement and visual effects

**Explanation of changes:**
Created `player.py` containing the `Player` class (extends `pygame.sprite.Sprite`) responsible for the Pac-Man character and movement system. The class loads and scales the user's 16×16 pixel art sprite, pre-computes directional variants (flip/rotate) so the character faces its movement direction, and implements grid-aligned movement with wall collision detection. Visual effects include configurable squash & stretch animation, directional eye pupil overlay aligned with the sprite's existing eyes, and a fading particle trail. All parameters (speed, squash amount, eye offset, trail lifetime, colors, pupil size/shift) are passed via the constructor — nothing is hardcoded. Input supports both arrow keys and WASD.

---

### Prompt [5]

**The prompt:**

> You are an expert game developer and computer science algorithm specialist. Your task is to build a top-down, grid-based "Pac-Man" style game.

CRITICAL EVALUATION CRITERIA:
The final solution will be heavily judged on code structure, readability, adherence to clean code principles (SOLID, DRY), and the elegance of the algorithms used. Use a widely accessible technology stack (e.g., Python with Pygame, or HTML5 Canvas with JavaScript).

Please execute this project strictly in the following phases. Do not move to the next phase until the current one is fully functional.

### Phase 1: Maze Generation and Rendering (BONUS TARGETED)

- Do not use a hardcoded map. Implement a procedural maze generation algorithm (e.g., Randomized Depth-First Search, Prim's algorithm, or Recursive Backtracker) to generate a random solvable maze every time the game starts.
- Render the maze clearly on the screen. Ensure there are open paths and clear boundaries.

### Phase 2: Player Character and Mechanics

- Render a controllable player character on the screen.
- Implement smooth, grid-based movement controlled by the keyboard (Arrow keys or WASD).
- Implement strict collision detection. The player must absolutely not be able to pass through or clip into maze walls.

### Phase 3: Enemy AI and Pathfinding (BONUS TARGETED)

- Add multiple enemies (ghosts) that start at specific locations and navigate towards the player.
- CRITICAL BONUS REQUIREMENT: Implement a unique path-finding algorithm for each enemy to give them distinct behaviors. For example:
  - Enemy 1 (The Chaser): Uses A\* (A-star) algorithm to find the absolute shortest path to the player.
  - Enemy 2 (The Tracker): Uses Breadth-First Search (BFS) or Dijkstra's algorithm.
  - Enemy 3 (The Interceptor): Uses a heuristic to target the tile a few steps _ahead_ of the player's current direction.
  - Enemy 4 (The Wanderer): Uses a Random Walk algorithm or a Wall-Follower logic until it gets within a certain radius of the player.

### Phase 4: Game Elements

- Distribute collectible items (points/dots) throughout the generated maze paths.
- Implement a scoring system that updates as the player collects items.
- Add at least one type of moving obstacle and one "Power-Up" (e.g., temporary invincibility, speed boost, or the ability to eat enemies).

### Phase 5: Code Polish and Documentation

- Refactor the code to ensure it is highly modular (e.g., separate files or classes for Game Engine, Player, MazeGenerator, and Pathfinding algorithms).
- Add clear, descriptive comments explaining the logic behind the maze generation and pathfinding algorithms.

MAKE THIS WHOLE THING INTO A HUGE IMPLEMENTATION PLAN MD FILE SO THAT EVERYONE CAN FOLLOW!"

**Commits:**

- `30ad8f86fa34756f06653b5017afd5d98b901d0a` - Added a comprehensive implementation plan of the exercise.

**Explanation of changes:**
Added a comprehensive implementation plan of the exercise.

---

### Prompt 6

**The prompt:**

> Good implementation plan! I did a pull that synced some rudimentary solutions my team already did! Complete the whole implementation plan while building upon the stack that exists.

**Commits:**

- `31d498744e36c4954f5b2ad520b443c1f379edf6` - feat: Implement full Pac-Man game (maze gen, AI, items, engine)

**Explanation of changes:**
Implemented all 5 phases of the Pac-Man game:

- **Phase 1**: Created `game/settings.py` (all constants), `game/maze/generator.py` (Recursive Backtracker maze generation with spawn zones and extra corridor openings), `game/maze/renderer.py` (cached maze rendering, HUD, game over/win overlays), and `game/engine.py` (game loop with state machine).
- **Phase 2**: Integrated existing `player.py` via `game/entities/player.py` re-export shim. Wired player into the engine with collision detection against maze walls.
- **Phase 3**: Created four pathfinding algorithms — `game/pathfinding/astar.py` (A* with Manhattan heuristic), `game/pathfinding/bfs.py` (BFS), `game/pathfinding/interceptor.py` (predictive targeting 4 tiles ahead), `game/pathfinding/wanderer.py` (random walk + proximity A* chase). Created `game/entities/enemy.py` with base `Enemy` class and four subclasses: Blinky (A\*), Pinky (interceptor), Inky (BFS), Clyde (wanderer).
- **Phase 4**: Created `game/items/collectibles.py` with Dot, PowerPellet (pulsing glow), SpeedBoost (lightning bolt), and MovingObstacle (rotating spiky hazard). Scoring, lives, power-up timers, and win/lose conditions all wired into engine.
- **Phase 5**: Updated `main.py` to thin entry point, updated `README.md`, created `requirements.txt`.

---

### Prompt 7

**The prompt:**

> sometimes the player gets stuck in the wall and cant move. especially when picking up the wierd green thing. so if the player is in 1x1 corridor so there is a well next him on either side, if the player then moves into the wall then it gets stuck

**Commits:**

- `d31761f06bd23ef9a7a9acf4053263f1ee5c4574` - fix: Implement robust pixel-by-pixel movement with strict grid-math collision to prevent getting stuck

**Explanation of changes:**
Fixed two critical movement bugs in `player.py`. First, the speed boost item multiplied player speed by 1.5 (making it 3). Because 3 doesn't divide the grid cell size (32) evenly, the player skipped past exact grid alignments and got permanently stuck. This was fixed by implementing pixel-by-pixel movement under the hood. Second, the player could still get stuck in 1x1 tight corridors because the Pygame Rect collision allowed sinking 1 pixel into flush walls to avoid scraping, breaking the mathematical grid alignment required to turn. This was fixed by entirely replacing Pygame Rect collisions with strict mathematical grid-index overlapping checks, guaranteeing the player can never intersect a wall tile and will always arrive at intersections perfectly aligned.

> [The game crashed with `pygame.error: File is not a Windows BMP file` when loading the PNG sprite. User asked to reinstall the pygame build.]

**Commits:**

- No commits made

**Explanation of changes:**
The standard `pygame` package installed without SDL_image extended support on Python 3.14, so it could only load BMP files. Uninstalled `pygame` and installed `pygame-ce` (Pygame Community Edition), which includes full SDL_image support. Updated `requirements.txt` to reference `pygame-ce>=2.5.0`.

---

### Prompt 8

**The prompt:**

> "There is a problem with the ghosts clipping and running through the wall and sometimes even just exiting the map. This should not happen. The ghosts should be confined to the map borders and the places that the player can move to."

**Commits:**

- `9b19d87f9af64f03283af7622aa6cfdc3ce1ff31` - fix: Prevent ghost wall-clipping and switch to pygame-ce

**Explanation of changes:**
Fixed two root causes of ghost wall-clipping:

1. `ENEMY_SPEED` was 3 which doesn't divide `CELL_SIZE` (32) evenly, so ghosts were never detected as tile-aligned and could never check walls. Changed to 4 (and `EATEN_SPEED` from 6→8).
2. Rewrote `_follow_path()` in `game/entities/enemy.py` to validate every cell transition against the grid before moving, and to snap pixel position to exact grid coordinates to prevent cumulative drift. Verified with automated test: 0 wall violations across 2000 frames.

---

### Prompt 9

**The prompt:**

> "New problem, now the path finding algortihm works correctly and it is TOO GOOD: the ghosts just straigh beeline to the player with no counterplay possible."

**Commits:**

- `84fe1e24e07afee59cda185acdfc2ec747f5213e` - feat: Implement classic Pac-Man Scatter/Chase cycle and AI balancing

**Explanation of changes:**
To balance the perfect pathfinding, implemented the classic Pac-Man "Scatter vs Chase" alternating modes:

1. `game/settings.py`: Added constants `SCATTER_DURATION` (~7s) and `CHASE_DURATION` (~20s). Reduced base `ENEMY_SPEED` from 4 to 2 (Player speed is 4) so the player can actually outrun them on straightaways.
2. `game/entities/enemy.py`: Assigned individual corner targets to each ghost type (Blinky=Top-Right, Pinky=Top-Left, Inky=Bottom-Right, Clyde=Bottom-Left).
3. `game/engine.py`: Wired a `mode_timer` into the game loop. Every ~20 seconds, ghosts universally stop chasing and fall back/scatter towards their respective corners for ~7s. As in the classic arcade game, changing modes immediately reverses ghost direction, creating a rhythmic window of opportunity for the player to counter-attack or escape.

---

### Prompt 10

**The prompt:**

> "I did a pull and and it broke the ghost movement again."

**Commits:**

- `0cd45ed17964ff1c719067a769a570d2ace62877` - fix: Guarantee strict ghost grid alignment across fractional speeds via float accumulator

**Explanation of changes:**
The team updated ghost speeds to fractional values (`ENEMY_SPEED = 1.6`) in `settings.py`. The previous ghost movement logic relied on integers that cleanly divided into `CELL_SIZE` (`32`) to achieve perfect tile alignments (`pixel_x % 32 == 0`). Fractional speeds broke this, preventing ghosts from ever snapping to intersections to check walls.

Fixed by bringing the ghosts strictly to the same pixel-by-pixel robust movement standard implemented by the team for the player in the previous prompt, but enhanced for fractions. In `game/entities/enemy.py`, ghost pixel coordinates were cast to strictly `int`. A `movement_accum` float was added to `Enemy.__init__`. During `_follow_path()`, the ghost adds its speed (`1.6`) to the accumulator every frame, then peels off the integer part (`1` or `2`) and moves exactly that many discrete pixels inside a loop. This entirely eliminates fractional position drift and guarantees that ghosts will perfectly hit `X % 32 == 0` intersections to execute their pathfinding and wall collision logic, no matter what complex math multiplier or floating point speed is configured.

---

### Prompt 11

**The prompt:**

> "Make all speeds faster like 1.5x"

**Commits:**

- `ca8307c2b96381e15abc4bf42e18ac6bc38c7158` - feat: Increase all game speeds by 1.5x and add float accumulator to player

**Explanation of changes:**
Multiplied all movement speed constants in `game/settings.py` by 1.5:

- `PLAYER_SPEED` from 2 to 3
- `ENEMY_SPEED` from 1.6 to 2.4
- `ENEMY_FRIGHTENED_SPEED` from 1 to 1.5
- `ENEMY_EATEN_SPEED` from 6 to 9
- `OBSTACLE_SPEED` from 2 to 3

Additionally, proactively updated `player.py`'s movement logic to use a `movement_accum` float accumulator just like the ghosts do. The previous logic cast `self.speed` directly to an `int()`. Since the player base speed is now `3`, grabbing a 1.5x speed boost changes their speed to `4.5`. The old logic would have truncated this to exactly `4`, stripping away the `.5` advantage entirely and nerfing the powerup. The float accumulator allows the player to correctly bank and consume those fractions to effectively move at perfectly `4.5` pixels per frame.

---

### Prompt 12

> "the collisions currently seem to work only if the centers of each object collide. so for gathering points or collisions between the player and the ghosts the edges must be checked instead"

**Commits:**

- `29b4e3d2b53cdb688c548fff5b26e1951b1f94e2` - fix: Convert grid-coordinate collisions to edge-based rectangular hitboxes

**Explanation of changes:**
The original collision logic in `game/engine.py` strictly relied on comparing mathematical grid indices (e.g., `if dot.grid_pos == player_grid`), meaning collisions only registered when the dead-center of the player perfectly overlapped the dead-center of the item or enemy tile.

This was resolved by replacing all grid coordinate checks with standard `pygame.Rect.colliderect()` intersection evaluations. Bounding box pixel coordinates are now generated for the player, enemies, speed boosts, power pellets, dots, and moving obstacles. A universal 6-pixel 'forgiveness' margin was applied to these rectangles (shrinking a 32x32 hit box down to 20x20 in the center) so that players can cleanly sideswipe through dots and aren't unfairly clipped by enemies when barely grazing their outer edges.

---

### Prompt 13

**The prompt:**

> "the spinning blade is moving through walls"

**Commits:**

- `0726bf107be5daee35d872652bb5305ffdba17a1` - fix: Apply float accumulator pixel-by-pixel movement to MovingObstacle to stop wall clipping

**Explanation of changes:**
The user's previous modification to increase speeds by 1.5x set `OBSTACLE_SPEED = 3`. The `MovingObstacle` class in `game/items/collectibles.py` still relied on the old logic (`pixel_x % 32 == 0`) to detect map intersections and turn away from walls. Because a speed of 3 doesn't divide 32 evenly, the obstacle skipped right past the alignment check and clipped directly through the walls.

Fixed by refactoring `MovingObstacle.update()` to use the exact same float accumulator and pixel-by-pixel movement loop that the Player and Ghosts were upgraded to use in earlier commits. The obstacle now builds up fractional speed in an accumulator, extracts the integer distance, and processes wall collisions and turns one pixel at a time. This guarantees that the obstacle always perfectly slides onto `X % 32 == 0` alignments, reliably detecting and bouncing off walls regardless of its speed.

> "I added background music for the game in the assets folder. Also make it so that if the player gets the speed power up the background music also gets faster."

---

### Prompt 14

**The prompt:**

> "I added background music for the game in the assets folder. Also make it so that if the player gets the speed powerup the background music also gets faster."

**Commits:**

- `78c437304d9a7705beafabfa484c89a85d61437d` - feat: Add dynamic background music that speeds up with player powerups

**Explanation of changes:**
The provided asset `assets/Hechizo_en_la_Pista.mp4` was a video file, which `pygame.mixer.music` cannot play natively. FFmpeg was used to strip the video and convert the audio track into a standard `bgm_normal.wav` file. Then, it was used again with the `-filter:a "atempo=1.5"` flag to generate a pre-sped-up `bgm_fast.wav` track.

In `game/engine.py`, the `pygame.mixer` subsystem was initialized and `bgm_normal.wav` was set to endlessly loop upon game start. Logic was added to the main update loop so that when the player picks up a speed boost (or when the boost timer runs out), the engine calculates the exact playback position (`pygame.mixer.music.get_pos()`) and dynamically swaps between the normal and fast tracks using `pygame.mixer.music.play(-1, start=new_pos)`, maintaining a seamless chronological sync between the audio and gameplay state.

---

### Prompt 15

**The prompt:**

> "the movement checking for the ghosts and player are fundamentally different. use the grid system"

**Commits:**

- `73de0a627a98df2af0d61da5e0fd7b50fb53c381` - refactor: Unify Player and Ghost movement collision to exclusively use the 2D grid array

**Explanation of changes:**
The user correctly identified an architectural discrepancy: `Enemy` entities were verifying their movement directly against indices in the `grid` integer array (e.g., `grid[ny][nx] == 0`), while the `Player` was still relying on an expensive iteration over a list of `pygame.Rect` objects (`wall_rects`) to check for wall intersections.

This was resolved by rewriting `Player._can_move_dist()` in `player.py` to calculate exactly which grid columns and rows the player's bounding box overlaps, and checking those explicit indices in the `grid` array instead of rectangles.

Because both the player and the enemies now securely rely entirely on the grid array for movement bounding, the `_build_wall_rects()` method and the `self.wall_rects` variable were completely stripped out of `game/engine.py` and removed from the `Enemy` method signatures, saving memory and eliminating redundant coordinate conversions.

---

### Prompt 16

**The prompt:**

> "the player passed through the ghost even though now they are on the same system"

**Commits:**

- `435953065df59c327874cf0fd00fcd072b2a5608` - fix: Restore player death collision when ghosts are in the SCATTER state

**Explanation of changes:**
The user's reported bug was not actually a collision coordinate issue, but rather a state machine oversight. In Prompt 9, a new `"SCATTER"` mode was added to the game, alternating with `"CHASE"`.

However, the ghost collision logic in `game/engine.py` explicitly checked `elif enemy.state == "CHASE":` to trigger a player death. If the player happened to run into a ghost during the 7-second `"SCATTER"` window, the collision was detected but ignored by the game engine, allowing the player to pass cleanly through unharmed.

This was resolved by updating the game loop to check `elif enemy.state in ("CHASE", "SCATTER"):`, restoring lethality to the ghosts during their retreat phase.

---

### Prompt 19

**The prompt:**

> "analyse how respawning for the ghosts work currently? the problem is that they do not respawn, not always. The ghosts should by default move towards the respawn box after they are eaten by the player. Once in the box they should be normal again and continue chasing the player."

**Commits:**

- `[Paste Commit Hash Here]` - fix: Overhaul ghost EATEN→respawn lifecycle for reliable spawn box return

**Explanation of changes:**
Three interconnected bugs prevented eaten ghosts from reliably respawning:

1. **Spawn box cells blocked normal pathfinding:** The maze generator marks the spawn area with grid value `2`. All pathfinding modules (`wanderer.py`, `interceptor.py`) and the ghost's own movement validation treated only `0` as passable. So when an eaten ghost arrived at the spawn box and transitioned to SCATTER/CHASE, it immediately tried to path out using normal A\*—but the `2`-cells were considered walls, trapping it permanently inside the box.

2. **Arrival check was timing-dependent:** The "have I reached spawn?" check (`my_pos == spawn`) was gated behind the repath cooldown timer (`_repath_cd`). This meant the ghost could physically sit on its spawn tile but wouldn't register as "arrived" until the cooldown happened to expire—often missing the check entirely at high eaten-speeds.

3. **No continuous arrival detection during movement:** Movement happens pixel-by-pixel in `_follow_path()`, but the spawn arrival check was only in `update()`, outside the movement loop.

Fixed by: (a) adding a `_is_passable()` helper to `enemy.py` that treats grid values `0` and `2` as walkable, and updating all grid checks in `_follow_path()` to use it; (b) updating `wanderer.py` and `interceptor.py` to use `!= 1` instead of `== 0`; (c) moving the spawn arrival check directly into `_follow_path()` so it fires every frame the ghost is tile-aligned; (d) immediately resetting the path, cooldown, speed, and accumulator on arrival so the ghost starts normal behaviour without delay.

---

### Prompt 17

**The prompt:**

> "New problem: enemies (ghosts) when dead should go to their respawn point and do that by traveling through walls. Also, add a 3 second waiting windows upon starting the game."

**Commits:**

- `964483ce4b174819950d15753a6a3c7c4713204f` - feat: Add 3-second start delay and allow dead ghosts to path through walls

**Explanation of changes:**
Implemented the two requested features to bring the game closer to classic Pac-Man mechanics:

1. **Dead ghosts traveling through walls:**
   - Modified the A\* pathfinding algorithm in `game/pathfinding/astar.py` to accept an `ignore_walls` boolean flag. If `True`, it bypasses the `grid[ny][nx] == 1` check.
   - Updated `game/entities/enemy.py`. When a ghost is in the `EATEN` state, it now calls `astar.find_path(..., ignore_walls=True)`.
   - Additionally, updated the ghost's internal pixel-by-pixel `_follow_path` loop to also bypass its own wall-collision checks (`grid[ny][nx] != 1`) if `is_eaten == True`, allowing them to literally float straight through the maze walls back to the monster pen.

2. **3-Second start delay:**
   - Introduced a new `STATE_START_DELAY` alongside `STATE_PLAYING` in `game/engine.py`.
   - Set the initial `self.state` in `_setup_new_game` (and after player deaths) to this new state, accompanied by a `start_delay_timer` initialized to 3 times the frames-per-second (`FPS * 3`).
   - The engine's main `run()` loop was updated to tick this timer down and only transition to `STATE_PLAYING` once it hits zero.
   - Designed a new `draw_start_delay` method in `game/maze/renderer.py` that renders a bold yellow "GET READY!" string and the current countdown integer on top of the map.

---

### Prompt [18]

**The prompt:**

> CREATE AN agent skills system that completely defines every single part of the current repository. Then proceed to give me a handoff prompt.

**Commits:**

- `6f36b6a1c616f5b08ed82fd91dab882d16dff50b` - I've created five detailed .md skill files in .agents/skills/

**Explanation of changes:**
I've created five detailed .md skill files in .agents/skills/

---
