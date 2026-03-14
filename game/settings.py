"""
settings.py - Central configuration for the Pac-Man game.

All game constants are defined here so that tuning values never
requires hunting through multiple files.
"""

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
FPS = 60
CELL_SIZE = 32          # Pixel size of each grid cell

# Maze dimensions in cells (must be ODD for the generator algorithm)
MAZE_COLS = 21
MAZE_ROWS = 21

HUD_HEIGHT = 56         # Pixel height of the score/lives bar

SCREEN_WIDTH = MAZE_COLS * CELL_SIZE          # 672
SCREEN_HEIGHT = MAZE_ROWS * CELL_SIZE + HUD_HEIGHT  # 728

WINDOW_TITLE = "Pac-Man — ASI Lõppvoor 2026"

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
COLOR_BG          = (15, 15, 35)       # Deep navy background
COLOR_WALL        = (33, 33, 222)      # Classic Pac-Man blue walls
COLOR_WALL_EDGE   = (60, 60, 255)      # Lighter wall border
COLOR_PATH        = (15, 15, 35)       # Same as BG (paths blend in)
COLOR_DOT         = (255, 255, 200)    # Creamy dots
COLOR_POWER_PELLET = (255, 180, 80)    # Orange glow
COLOR_SPEED_BOOST = (100, 220, 255)    # Cyan lightning
COLOR_HUD_BG      = (10, 10, 25)       # HUD bar background
COLOR_HUD_TEXT    = (255, 255, 255)    # HUD text
COLOR_GAME_OVER   = (255, 50, 50)      # Red game-over text

# Ghost colors
COLOR_BLINKY = (255, 0, 0)         # Red  - The Chaser
COLOR_PINKY  = (255, 184, 255)     # Pink - The Interceptor
COLOR_INKY   = (0, 255, 255)       # Cyan - The Tracker
COLOR_CLYDE  = (255, 184, 82)      # Orange - The Wanderer
COLOR_FRIGHTENED = (30, 30, 200)   # Blue frightened ghost
COLOR_EYES   = (255, 255, 255)     # Ghost eye whites

# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
PLAYER_SPEED = 4             # Pixels per frame (must divide CELL_SIZE evenly)
PLAYER_SQUASH = 0.12         # Squash & stretch intensity
PLAYER_EYE_OFFSET = (3, -3)  # Eye position relative to center
PLAYER_TRAIL_LIFETIME = 14   # Frames a trail particle lives
PLAYER_LIVES = 3

# ---------------------------------------------------------------------------
# Enemies
# ---------------------------------------------------------------------------
ENEMY_SPEED = 4              # Base ghost speed (must divide CELL_SIZE=32 evenly)
ENEMY_FRIGHTENED_SPEED = 2   # Speed while frightened
ENEMY_EATEN_SPEED = 8        # Speed when returning to spawn
FRIGHTENED_DURATION = 480     # Frames (~8 seconds at 60 FPS)
CLYDE_CHASE_RADIUS = 8       # Tiles — Clyde switches to A* inside this

# ---------------------------------------------------------------------------
# Items / Scoring
# ---------------------------------------------------------------------------
SCORE_DOT = 10
SCORE_POWER_PELLET = 50
SCORE_GHOST_EAT = 200
SPEED_BOOST_DURATION = 300    # Frames (~5 seconds)
SPEED_BOOST_MULTIPLIER = 1.5
SPEED_BOOST_SPAWN_INTERVAL = 1800  # Every ~30 seconds
OBSTACLE_SPEED = 2            # Must divide CELL_SIZE evenly

# ---------------------------------------------------------------------------
# Maze generation
# ---------------------------------------------------------------------------
# Extra corridors to open (fraction of total walls removed after generation)
MAZE_EXTRA_OPENINGS = 0.08
