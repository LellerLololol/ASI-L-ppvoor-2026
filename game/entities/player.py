"""
player.py - Re-exports the project-root Player class for the game package.

The original Player implementation lives at the repo root (player.py)
because it was created by a team member as a standalone module.  This
shim simply re-exports it so the engine can import from a consistent
package path:  ``from game.entities.player import Player``.
"""

from player import Player  # noqa: F401 — re-export

__all__ = ["Player"]
