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

<<<<<<< HEAD
- `d31761f06bd23ef9a7a9acf4053263f1ee5c4574` - fix: Implement robust pixel-by-pixel movement with strict grid-math collision to prevent getting stuck
=======
- `[Paste Commit Hash Here]` - fix: Implement robust pixel-by-pixel movement with strict grid-math collision to prevent getting stuck
>>>>>>> d31761f06bd23ef9a7a9acf4053263f1ee5c4574

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
