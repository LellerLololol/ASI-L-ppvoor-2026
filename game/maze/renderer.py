"""
renderer.py - Draws the maze grid and HUD onto a Pygame surface.

Wall cells are drawn as rounded-corner rectangles with a subtle edge
highlight to give them a classic retro-neon feel.
"""

import pygame
from game.settings import (
    CELL_SIZE, COLOR_WALL, COLOR_WALL_EDGE, COLOR_ENEMY_SPAWN, COLOR_PATH,
    COLOR_HUD_BG, COLOR_HUD_TEXT, HUD_HEIGHT, SCREEN_WIDTH,
    MAZE_COLS, MAZE_ROWS, PLAYER_LIVES,
)


class MazeRenderer:
    """Renders the maze grid, dots, and the HUD bar.

    The renderer pre-builds a static surface on first call and only
    redraws it when the maze changes (which is never mid-game). Dots
    and dynamic elements are drawn on top each frame.
    """

    def __init__(self):
        self._cached_surface: pygame.Surface | None = None
        self._font: pygame.font.Font | None = None

    # ------------------------------------------------------------------
    # Maze drawing
    # ------------------------------------------------------------------
    def draw_maze(self, surface: pygame.Surface, grid: list[list[int]]) -> None:
        """Draw the maze (walls only) onto *surface*.

        Uses a cached surface so the grid isn't redrawn every frame.
        """
        if self._cached_surface is None:
            self._cached_surface = pygame.Surface(
                (MAZE_COLS * CELL_SIZE, MAZE_ROWS * CELL_SIZE)
            )
            self._cached_surface.fill(COLOR_PATH)

            rememberedEnemyCell = []

            for row in range(len(grid)):
                for col in range(len(grid[row])):
                    if grid[row][col] == 1:
                        self._draw_wall_cell(self._cached_surface, col, row)
                    if grid[row][col] == 2:
                        rememberedEnemyCell.append([col, row])
            
            self._draw_enemey_spawn(self._cached_surface, rememberedEnemyCell)

        surface.blit(self._cached_surface, (0, 0))

    def _draw_wall_cell(self, surface: pygame.Surface, col: int, row: int) -> None:
        """Draw a single wall cell with a slight 3-D edge effect."""
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        # Main wall fill
        pygame.draw.rect(surface, COLOR_WALL, rect)
        # Lighter border for depth
        pygame.draw.rect(surface, COLOR_WALL_EDGE, rect, width=1, border_radius=3)

    def _draw_enemey_spawn(self, surface: pygame.Surface, cells) -> None:
        dx, dy = (-cells[0][0] + cells[-1][0]) + 1, (-cells[0][1] + cells[-1][1]) + 1
        """Draw a single wall cell with a slight 3-D edge effect."""
        x = cells[len(cells) // 2][0] * CELL_SIZE - CELL_SIZE
        y = cells[len(cells) // 2][1] * CELL_SIZE - CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE * dx, CELL_SIZE * dy)

        # Main wall fill
        #pygame.draw.rect(surface, COLOR_WALL, rect)
        # Lighter border for depth
        pygame.draw.rect(surface, COLOR_ENEMY_SPAWN, rect, width=1, border_radius=3)

    # ------------------------------------------------------------------
    # HUD
    # ------------------------------------------------------------------
    def draw_hud(
        self,
        surface: pygame.Surface,
        score: int,
        lives: int,
        power_up_timer: int = 0,
    ) -> None:
        """Draw the heads-up-display bar at the bottom of the screen."""
        if self._font is None:
            self._font = pygame.font.SysFont("monospace", 22, bold=True)

        hud_y = MAZE_ROWS * CELL_SIZE
        hud_rect = pygame.Rect(0, hud_y, SCREEN_WIDTH, HUD_HEIGHT)
        pygame.draw.rect(surface, COLOR_HUD_BG, hud_rect)

        # Score
        score_text = self._font.render(f"SCORE: {score}", True, COLOR_HUD_TEXT)
        surface.blit(score_text, (12, hud_y + 16))

        # Lives (as small circles)
        for i in range(lives):
            cx = SCREEN_WIDTH - 30 - i * 28
            cy = hud_y + HUD_HEIGHT // 2
            pygame.draw.circle(surface, (255, 255, 0), (cx, cy), 10)

        # Power-up timer
        if power_up_timer > 0:
            timer_text = self._font.render(
                f"POWER: {power_up_timer // 60 + 1}s", True, (100, 200, 255)
            )
            surface.blit(timer_text, (SCREEN_WIDTH // 2 - 50, hud_y + 16))

    # ------------------------------------------------------------------
    # Overlay screens
    # ------------------------------------------------------------------
    def draw_game_over(self, surface: pygame.Surface, score: int) -> None:
        """Draw the GAME OVER overlay."""
        font_big = pygame.font.SysFont("monospace", 48, bold=True)
        font_small = pygame.font.SysFont("monospace", 22)

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        text = font_big.render("GAME OVER", True, (255, 50, 50))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, MAZE_ROWS * CELL_SIZE // 2 - 30))
        surface.blit(text, rect)

        score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, MAZE_ROWS * CELL_SIZE // 2 + 20))
        surface.blit(score_text, score_rect)

        restart_text = font_small.render("Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, MAZE_ROWS * CELL_SIZE // 2 + 55))
        surface.blit(restart_text, restart_rect)

    def draw_win_screen(self, surface: pygame.Surface, score: int) -> None:
        """Draw the YOU WIN overlay."""
        font_big = pygame.font.SysFont("monospace", 48, bold=True)
        font_small = pygame.font.SysFont("monospace", 22)

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        text = font_big.render("YOU WIN!", True, (50, 255, 50))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, MAZE_ROWS * CELL_SIZE // 2 - 30))
        surface.blit(text, rect)

        score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, MAZE_ROWS * CELL_SIZE // 2 + 20))
        surface.blit(score_text, score_rect)

        restart_text = font_small.render("Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, MAZE_ROWS * CELL_SIZE // 2 + 55))
        surface.blit(restart_text, restart_rect)

    def invalidate_cache(self) -> None:
        """Force the maze surface to be redrawn (call after generating a new maze)."""
        self._cached_surface = None
