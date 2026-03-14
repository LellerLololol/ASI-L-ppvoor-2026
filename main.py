"""
main.py - Entry point for the Pac-Man game.

Run this file to start the game:
    python main.py
"""

from game.engine import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
