"""
engine.py - Main game controller with state machine.

States
------
PLAYING   – active gameplay
GAME_OVER – player lost all lives
WIN       – player collected every dot
"""

import sys
import pygame

from game.settings import (
    FPS, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, COLOR_BG,
    CELL_SIZE, PLAYER_SPEED, PLAYER_SQUASH, PLAYER_EYE_OFFSET,
    PLAYER_TRAIL_LIFETIME, PLAYER_LIVES, ENEMY_SPEED,
    FRIGHTENED_DURATION, SPEED_BOOST_DURATION, SPEED_BOOST_MULTIPLIER,
    SPEED_BOOST_SPAWN_INTERVAL, OBSTACLE_SPEED,
    SCORE_DOT, SCORE_POWER_PELLET, SCORE_GHOST_EAT,
    COLOR_BLINKY, COLOR_PINKY, COLOR_INKY, COLOR_CLYDE,
    MAZE_COLS, MAZE_ROWS,
)
from game.maze.generator import MazeGenerator
from game.maze.renderer import MazeRenderer
from game.entities.player import Player
from game.entities.enemy import Blinky, Pinky, Inky, Clyde
from game.items.collectibles import Dot, PowerPellet, SpeedBoost, MovingObstacle


# Game states
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_WIN = "WIN"


class Game:
    """Top-level controller that owns the Pygame loop and all subsystems."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        self._setup_new_game()

    # ------------------------------------------------------------------
    # Setup / Reset
    # ------------------------------------------------------------------
    def _setup_new_game(self) -> None:
        """Initialise (or re-initialise) all game objects."""
        self.state = STATE_PLAYING
        self.score = 0
        self.lives = PLAYER_LIVES
        self.power_timer = 0
        self.speed_boost_timer = 0
        self.speed_boost_spawn_cd = SPEED_BOOST_SPAWN_INTERVAL
        self.ghost_eat_combo = 1  # doubles per ghost eaten in one power-up

        # ---- Maze ----
        self.maze_gen = MazeGenerator()
        self.grid = self.maze_gen.generate()
        self.renderer = MazeRenderer()

        # Build wall rects list (used by player / enemy collision)
        self.wall_rects = self._build_wall_rects()

        # ---- Player ----
        spawn_col, spawn_row = self.maze_gen.get_player_spawn()
        self.player = Player(
            x=spawn_col,
            y=spawn_row,
            tile_size=CELL_SIZE,
            speed=PLAYER_SPEED,
            squash_amount=PLAYER_SQUASH,
            eye_offset=PLAYER_EYE_OFFSET,
            trail_lifetime=PLAYER_TRAIL_LIFETIME,
        )

        # ---- Enemies ----
        spawns = self.maze_gen.get_enemy_spawns()
        self.enemies = [
            Blinky(spawns[0][0], spawns[0][1], CELL_SIZE, ENEMY_SPEED, COLOR_BLINKY),
            Pinky(spawns[1][0], spawns[1][1], CELL_SIZE, ENEMY_SPEED, COLOR_PINKY),
            Inky(spawns[2][0], spawns[2][1], CELL_SIZE, ENEMY_SPEED, COLOR_INKY),
            Clyde(spawns[3][0], spawns[3][1], CELL_SIZE, ENEMY_SPEED, COLOR_CLYDE),
        ]

        # ---- Collectibles ----
        self.dots: list[Dot] = []
        self.power_pellets: list[PowerPellet] = []
        self.speed_boosts: list[SpeedBoost] = []
        self._place_dots()
        self._place_power_pellets()

        # ---- Moving obstacle ----
        self.obstacle = self._create_obstacle()

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Enter the main game loop — blocks until the window is closed."""
        while True:
            self._handle_events()

            if self.state == STATE_PLAYING:
                self._update()

            self._draw()
            self.clock.tick(FPS)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Restart on 'R' from end screens
                if event.key == pygame.K_r and self.state in (STATE_GAME_OVER, STATE_WIN):
                    self._setup_new_game()
                    return

                # Player input
                if self.state == STATE_PLAYING:
                    self.player.handle_input(event)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def _update(self) -> None:
        """Advance one frame of gameplay."""
        # -- Timers --
        if self.power_timer > 0:
            self.power_timer -= 1
            if self.power_timer == 0:
                self.ghost_eat_combo = 1
                for enemy in self.enemies:
                    if enemy.state == "FRIGHTENED":
                        enemy.state = "CHASE"

        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.player.speed = PLAYER_SPEED

        # -- Speed boost spawning --
        self.speed_boost_spawn_cd -= 1
        if self.speed_boost_spawn_cd <= 0:
            self._spawn_speed_boost()
            self.speed_boost_spawn_cd = SPEED_BOOST_SPAWN_INTERVAL

        # -- Player --
        self.player.update(self.wall_rects)
        player_grid = self.player.get_grid_pos()

        # -- Dot collection --
        for dot in self.dots[:]:
            if dot.grid_pos == player_grid:
                self.dots.remove(dot)
                self.score += SCORE_DOT

        # -- Power pellet collection --
        for pellet in self.power_pellets[:]:
            if pellet.grid_pos == player_grid:
                self.power_pellets.remove(pellet)
                self.score += SCORE_POWER_PELLET
                self.power_timer = FRIGHTENED_DURATION
                self.ghost_eat_combo = 1
                for enemy in self.enemies:
                    if enemy.state != "EATEN":
                        enemy.state = "FRIGHTENED"

        # -- Speed boost collection --
        for boost in self.speed_boosts[:]:
            if boost.grid_pos == player_grid:
                self.speed_boosts.remove(boost)
                self.speed_boost_timer = SPEED_BOOST_DURATION
                self.player.speed = int(PLAYER_SPEED * SPEED_BOOST_MULTIPLIER)

        # -- Win check --
        if not self.dots and not self.power_pellets:
            self.state = STATE_WIN
            return

        # -- Enemies --
        for enemy in self.enemies:
            enemy.update(self.grid, self.wall_rects, self.player, self.enemies)

            # Collision with player
            if enemy.get_grid_pos() == player_grid:
                if enemy.state == "FRIGHTENED":
                    # Eat the ghost
                    self.score += SCORE_GHOST_EAT * self.ghost_eat_combo
                    self.ghost_eat_combo *= 2
                    enemy.state = "EATEN"
                elif enemy.state == "CHASE":
                    self._player_dies()
                    return

        # -- Moving obstacle --
        if self.obstacle:
            self.obstacle.update(self.grid)
            if self.obstacle.get_grid_pos() == player_grid:
                if self.power_timer > 0:
                    # Destroy obstacle when powered up
                    self.obstacle = None
                else:
                    self._player_dies()
                    return

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def _draw(self) -> None:
        """Render everything to screen."""
        self.screen.fill(COLOR_BG)

        # Maze
        self.renderer.draw_maze(self.screen, self.grid)

        # Dots & pellets
        for dot in self.dots:
            dot.draw(self.screen)
        for pellet in self.power_pellets:
            pellet.draw(self.screen)
        for boost in self.speed_boosts:
            boost.draw(self.screen)

        # Moving obstacle
        if self.obstacle:
            self.obstacle.draw(self.screen)

        # Enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Player
        self.player.draw(self.screen)

        # HUD
        self.renderer.draw_hud(self.screen, self.score, self.lives, self.power_timer)

        # Overlay screens
        if self.state == STATE_GAME_OVER:
            self.renderer.draw_game_over(self.screen, self.score)
        elif self.state == STATE_WIN:
            self.renderer.draw_win_screen(self.screen, self.score)

        pygame.display.flip()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _build_wall_rects(self) -> list[pygame.Rect]:
        """Convert grid 1-cells into a list of pygame.Rect for collision."""
        rects = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 1:
                    rects.append(
                        pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
        return rects

    def _place_dots(self) -> None:
        """Put a dot on every open path cell (excluding spawn zones)."""
        player_spawn = self.maze_gen.get_player_spawn()
        enemy_spawns = set(self.maze_gen.get_enemy_spawns())
        spawn_zone = {player_spawn} | enemy_spawns
        # Also exclude cells adjacent to spawns
        for sc, sr in list(spawn_zone):
            for dc in range(-1, 2):
                for dr in range(-1, 2):
                    spawn_zone.add((sc + dc, sr + dr))

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 0 and (col, row) not in spawn_zone:
                    self.dots.append(Dot(col, row, CELL_SIZE))

    def _place_power_pellets(self) -> None:
        """Place four power pellets near the corners of the maze."""
        corners = [
            (1, 1),
            (MAZE_COLS - 2, 1),
            (1, MAZE_ROWS - 2),
            (MAZE_COLS - 2, MAZE_ROWS - 2),
        ]
        for col, row in corners:
            # Find nearest open cell to the corner
            placed = False
            for dr in range(0, 4):
                for dc in range(0, 4):
                    r, c = row + dr, col + dc
                    if 0 <= r < MAZE_ROWS and 0 <= c < MAZE_COLS and self.grid[r][c] == 0:
                        self.power_pellets.append(PowerPellet(c, r, CELL_SIZE))
                        # Remove any dot at this position
                        self.dots = [d for d in self.dots if d.grid_pos != (c, r)]
                        placed = True
                        break
                if placed:
                    break

    def _spawn_speed_boost(self) -> None:
        """Place a speed boost on a random open cell."""
        import random
        open_cells = [
            (col, row)
            for row in range(len(self.grid))
            for col in range(len(self.grid[row]))
            if self.grid[row][col] == 0
        ]
        if open_cells:
            col, row = random.choice(open_cells)
            self.speed_boosts.append(SpeedBoost(col, row, CELL_SIZE))

    def _create_obstacle(self) -> MovingObstacle | None:
        """Create a moving obstacle in the maze."""
        # Place it near the center
        center_col, center_row = MAZE_COLS // 2, MAZE_ROWS // 2
        for dr in range(-3, 4):
            for dc in range(-3, 4):
                r, c = center_row + dr, center_col + dc
                if 0 <= r < MAZE_ROWS and 0 <= c < MAZE_COLS and self.grid[r][c] == 0:
                    return MovingObstacle(c, r, CELL_SIZE, OBSTACLE_SPEED)
        return None

    def _player_dies(self) -> None:
        """Handle player death — lose a life or game over."""
        self.lives -= 1
        if self.lives <= 0:
            self.state = STATE_GAME_OVER
        else:
            # Reset positions
            spawn_col, spawn_row = self.maze_gen.get_player_spawn()
            self.player.pixel_x = spawn_col * CELL_SIZE
            self.player.pixel_y = spawn_row * CELL_SIZE
            self.player.direction = (0, 0)
            self.player.queued_direction = (0, 0)

            spawns = self.maze_gen.get_enemy_spawns()
            for i, enemy in enumerate(self.enemies):
                enemy.pixel_x = spawns[i][0] * CELL_SIZE
                enemy.pixel_y = spawns[i][1] * CELL_SIZE
                enemy.state = "CHASE"
                enemy.direction = (0, 0)
