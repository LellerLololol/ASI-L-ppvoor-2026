"""
player.py - Pac-Man character with grid-aligned movement and visual effects.

This module contains the Player class responsible for:
- Loading and rendering the Pac-Man pixel art sprite
- Grid-aligned movement with wall collision (arrow keys + WASD)
- Squash & stretch animation
- Directional eye overlay
- Particle trail effect
"""

import os
import math
import pygame


# ---------------------------------------------------------------------------
# Direction vectors
# ---------------------------------------------------------------------------
DIR_NONE  = (0, 0)
DIR_UP    = (0, -1)
DIR_DOWN  = (0, 1)
DIR_LEFT  = (-1, 0)
DIR_RIGHT = (1, 0)

# Map keyboard keys to direction vectors
KEY_TO_DIRECTION = {
    # Arrow keys
    pygame.K_UP:    DIR_UP,
    pygame.K_DOWN:  DIR_DOWN,
    pygame.K_LEFT:  DIR_LEFT,
    pygame.K_RIGHT: DIR_RIGHT,
    # WASD
    pygame.K_w: DIR_UP,
    pygame.K_s: DIR_DOWN,
    pygame.K_a: DIR_LEFT,
    pygame.K_d: DIR_RIGHT,
}


# ---------------------------------------------------------------------------
# Particle (trail effect)
# ---------------------------------------------------------------------------
class _Particle:
    """A single fading trail particle left behind by the player."""

    def __init__(self, x: float, y: float, lifetime: int, color: tuple):
        self.x = x
        self.y = y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color

    def update(self) -> bool:
        """Decrease lifetime. Returns True while still alive."""
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface):
        """Draw the particle with fading alpha."""
        alpha = max(0, int(255 * (self.lifetime / self.max_lifetime)))
        radius = max(1, int(3 * (self.lifetime / self.max_lifetime)))
        particle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        faded_color = (*self.color[:3], alpha)
        pygame.draw.circle(particle_surface, faded_color, (radius, radius), radius)
        surface.blit(particle_surface, (self.x - radius, self.y - radius))


# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    """Pac-Man player character.

    Parameters
    ----------
    x, y : int
        Starting position in *grid* coordinates (column, row).
    tile_size : int
        Pixel width/height of a single grid cell.
    speed : int
        Pixels moved per frame.  Must divide ``tile_size`` evenly.
    squash_amount : float
        Fraction of compression along movement axis (e.g. 0.15 = 15 %).
    eye_offset : tuple[int, int]
        Base (dx, dy) in pixels from the sprite center to place pupil dots,
        used to align with the eyes already in the pixel art.
    trail_lifetime : int
        Number of frames each trail particle stays visible.
    sprite_path : str
        Path to the character sprite image (default: ``assets/PacManCharacter.png``).
    trail_color : tuple
        RGB color for trail particles (default: yellow).
    pupil_color : tuple
        RGB color for the directional eye pupils (default: dark blue).
    pupil_radius : int
        Pixel radius of each pupil dot (default: 1).
    pupil_shift : int
        How many pixels the pupils move in the look direction (default: 2).
    """

    def __init__(
        self,
        x: int,
        y: int,
        tile_size: int,
        speed: int,
        squash_amount: float = 0.15,
        eye_offset: tuple = (3, -3),
        trail_lifetime: int = 20,
        sprite_path: str = None,
        trail_color: tuple = (255, 255, 80),
        pupil_color: tuple = (10, 10, 60),
        pupil_radius: int = 1,
        pupil_shift: int = 2,
    ):
        super().__init__()

        # ---- configurable values ----
        self.tile_size = tile_size
        self.speed = speed
        self.squash_amount = squash_amount
        self.eye_offset = eye_offset
        self.trail_lifetime = trail_lifetime
        self.trail_color = trail_color
        self.pupil_color = pupil_color
        self.pupil_radius = pupil_radius
        self.pupil_shift = pupil_shift

        # ---- load and scale sprite ----
        if sprite_path is None:
            sprite_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "assets",
                "PacManCharacter.png",
            )
        raw_image = pygame.image.load(sprite_path).convert_alpha()
        scaled = pygame.transform.scale(raw_image, (tile_size, tile_size))

        # ---- pre-compute directional sprites ----
        # base sprite assumed to face LEFT
        self.base_image = scaled
        self._dir_images = {
            DIR_LEFT:  scaled,
            DIR_RIGHT: pygame.transform.flip(scaled, True, False),
            DIR_UP:    pygame.transform.rotate(scaled, -90),
            DIR_DOWN:  pygame.transform.rotate(scaled, 90),
            DIR_NONE:  scaled,
        }

        # ---- position (pixel coords, strictly int) ----
        self.pixel_x: int = x * tile_size
        self.pixel_y: int = y * tile_size

        # ---- movement state ----
        self.direction: tuple = DIR_NONE
        self.queued_direction: tuple = DIR_NONE
        self.movement_accum: float = 0.0

        # ---- animation / effects ----
        self._particles: list[_Particle] = []
        self._frame_counter: int = 0

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_input(self, event: pygame.event.Event):
        """Process a ``KEYDOWN`` event and queue the requested direction."""
        if event.type != pygame.KEYDOWN:
            return
        new_dir = KEY_TO_DIRECTION.get(event.key)
        if new_dir is not None:
            self.queued_direction = new_dir

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, wall_rects: list[pygame.Rect]):
        """Advance one frame: move, collide, spawn particles.

        Parameters
        ----------
        wall_rects : list[pygame.Rect]
            Rectangles representing impassable walls.
        """
        self._frame_counter += 1

        # -- move pixel-by-pixel --
        # This makes the game robust to any speed value (even ones that
        # do not divide tile_size evenly), preventing grid skipping.
        moved_any = False

        # Allow immediate 180-degree reversal even if not tile-aligned
        if self.direction != DIR_NONE and self.queued_direction == (-self.direction[0], -self.direction[1]):
            self.direction = self.queued_direction

        self.movement_accum += self.speed
        pixels_to_move = int(self.movement_accum)
        self.movement_accum -= pixels_to_move

        for _ in range(pixels_to_move):
            # 1. Try to turn when exactly on a tile intersection
            if self._is_tile_aligned():
                if self._can_move_dist(self.queued_direction, 1, wall_rects):
                    self.direction = self.queued_direction

            # 2. Stop if hitting a wall, otherwise move 1 pixel
            if self.direction != DIR_NONE:
                if not self._can_move_dist(self.direction, 1, wall_rects):
                    # Only zero out direction perfectly on grid so we don't get stuck slightly off
                    if self._is_tile_aligned():
                        self.direction = DIR_NONE
                    break
                
                self.pixel_x += self.direction[0]
                self.pixel_y += self.direction[1]
                moved_any = True

        if moved_any:
            self._spawn_trail_particle()

        # -- update existing particles --
        self._particles = [p for p in self._particles if p.update()]

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw(self, surface: pygame.Surface):
        """Render the player (trail → sprite → eyes) onto *surface*."""
        # 1. Trail particles (behind the character)
        for particle in self._particles:
            particle.draw(surface)

        # 2. Squash & stretch sprite
        image = self._get_squashed_image()
        img_rect = image.get_rect(
            center=(
                self.pixel_x + self.tile_size // 2,
                self.pixel_y + self.tile_size // 2,
            )
        )
        surface.blit(image, img_rect)

        # 3. Directional eyes (pupils)
        self._draw_eyes(surface)

    # ------------------------------------------------------------------
    # Helpers – movement
    # ------------------------------------------------------------------
    def _is_tile_aligned(self) -> bool:
        """Return True when the player sits exactly on a grid intersection."""
        return (
            self.pixel_x % self.tile_size == 0
            and self.pixel_y % self.tile_size == 0
        )

    def _can_move_dist(
        self, direction: tuple, dist: int, wall_rects: list[pygame.Rect]
    ) -> bool:
        """Check whether moving *dist* pixels in *direction* hits a wall."""
        future_x = self.pixel_x + direction[0] * dist
        future_y = self.pixel_y + direction[1] * dist

        # Mathematical grid validation:
        # A player at (x, y) with size T occupies tiles from x to x+T-1.
        # We calculate exactly which grid columns and rows the player overlaps.
        left_col = future_x // self.tile_size
        right_col = (future_x + self.tile_size - 1) // self.tile_size
        top_row = future_y // self.tile_size
        bottom_row = (future_y + self.tile_size - 1) // self.tile_size

        # Check if any of the overlapping grid cells contain a wall
        for r in range(top_row, bottom_row + 1):
            for c in range(left_col, right_col + 1):
                # We identify walls by their grid position (derived from the rect)
                wall_x = c * self.tile_size
                wall_y = r * self.tile_size
                # Since wall_rects are provided directly, we just check if 
                # a wall exists at this exact grid coordinate.
                for w in wall_rects:
                    if w.x == wall_x and w.y == wall_y:
                        return False
        return True

    # ------------------------------------------------------------------
    # Helpers – visual effects
    # ------------------------------------------------------------------
    def _get_squashed_image(self) -> pygame.Surface:
        """Return the direction-flipped sprite with squash & stretch applied."""
        # pick the correct directional sprite
        image = self._dir_images.get(self.direction, self.base_image)

        if self.direction == DIR_NONE or self.squash_amount == 0:
            return image

        # oscillate squash with a sine wave for a breathing feel
        t = math.sin(self._frame_counter * 0.3) * self.squash_amount
        dx, dy = self.direction

        if dx != 0:
            # horizontal movement → compress width, expand height
            w = int(self.tile_size * (1 - t))
            h = int(self.tile_size * (1 + t))
        else:
            # vertical movement → compress height, expand width
            w = int(self.tile_size * (1 + t))
            h = int(self.tile_size * (1 - t))

        # clamp to at least 1 px
        w = max(1, w)
        h = max(1, h)

        return pygame.transform.scale(image, (w, h))

    def _draw_eyes(self, surface: pygame.Surface):
        """Draw small pupil dots that shift towards the movement direction."""
        center_x = self.pixel_x + self.tile_size // 2
        center_y = self.pixel_y + self.tile_size // 2
        ox, oy = self.eye_offset

        # shift pupils in movement direction
        dx = self.direction[0] * self.pupil_shift
        dy = self.direction[1] * self.pupil_shift

        # left eye and right eye are mirrored on the x-axis
        for sign in (-1, 1):
            ex = center_x + sign * ox + dx
            ey = center_y + oy + dy
            pygame.draw.circle(
                surface, self.pupil_color, (int(ex), int(ey)), self.pupil_radius
            )

    def _spawn_trail_particle(self):
        """Add a new trail particle at the center of the player."""
        cx = self.pixel_x + self.tile_size // 2
        cy = self.pixel_y + self.tile_size // 2
        self._particles.append(
            _Particle(cx, cy, self.trail_lifetime, self.trail_color)
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def get_rect(self) -> pygame.Rect:
        """Return the current bounding rectangle (useful for other modules)."""
        return pygame.Rect(
            self.pixel_x, self.pixel_y, self.tile_size, self.tile_size
        )

    def get_grid_pos(self) -> tuple:
        """Return the current (column, row) grid position."""
        return (
            int(self.pixel_x // self.tile_size),
            int(self.pixel_y // self.tile_size),
        )
