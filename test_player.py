"""
Temporary test script for player.py.
Spawns a window with the player character — no walls.
Delete after verification.
"""

import pygame
from player import Player

# ---- Config ----
TILE_SIZE = 30
COLS = 15
ROWS = 15
FPS = 60
BG_COLOR = (0, 0, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE))
    pygame.display.set_caption("Player Test")
    clock = pygame.time.Clock()

    # No walls — just an open area
    wall_rects = []

    # Create player at grid position (7, 7) — center of the screen
    player = Player(
        x=7,
        y=7,
        tile_size=TILE_SIZE,
        speed=2,
        squash_amount=0.15,
        eye_offset=(4, -4),
        trail_lifetime=18,
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_input(event)

        player.update(wall_rects)

        # Draw
        screen.fill(BG_COLOR)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
