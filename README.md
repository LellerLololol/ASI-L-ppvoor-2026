# Pac-Man — ASI Lõppvoor 2026

A top-down, grid-based Pac-Man style game built with **Python 3** and **Pygame**.

## Features

- 🏗️ **Procedural maze generation** — random solvable maze every launch (Recursive Backtracker algorithm)
- 🎮 **Smooth grid-based movement** — WASD + Arrow key controls, squash & stretch animation
- 👻 **Four unique enemy AIs**, each using a different pathfinding algorithm:
  - **Blinky** (Red) — A\* shortest path chase
  - **Pinky** (Pink) — Predictive interception (targets ahead of player)
  - **Inky** (Cyan) — BFS flood-fill tracking
  - **Clyde** (Orange) — Random wandering → A\* chase within proximity
- 🟡 **Collectible dots** — collect all to win
- ⚡ **Power-ups** — Power Pellets (eat ghosts), Speed Boosts
- 💀 **Moving obstacle** — a rotating hazard patrolling the maze
- 📊 **HUD** — live score, lives, active power-up timer

## Quick Start

```bash
# Clone the repo
git clone https://github.com/LellerLololol/ASI-L-ppvoor-2026.git
cd ASI-L-ppvoor-2026

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Controls

| Key       | Action                           |
| --------- | -------------------------------- |
| `↑` / `W` | Move up                          |
| `↓` / `S` | Move down                        |
| `←` / `A` | Move left                        |
| `→` / `D` | Move right                       |
| `R`       | Restart (game over / win screen) |

## Project Structure

```
├── main.py                      # Entry point
├── game/
│   ├── engine.py                # Game loop & state machine
│   ├── settings.py              # All constants
│   ├── maze/
│   │   ├── generator.py         # Recursive Backtracker maze gen
│   │   └── renderer.py          # Maze + HUD rendering
│   ├── entities/
│   │   ├── player.py            # Player re-export
│   │   └── enemy.py             # Ghost base + 4 AI subclasses
│   ├── pathfinding/
│   │   ├── astar.py             # A* algorithm
│   │   ├── bfs.py               # Breadth-First Search
│   │   ├── interceptor.py       # Predictive targeting
│   │   └── wanderer.py          # Random walk + proximity chase
│   └── items/
│       └── collectibles.py      # Dots, Power Pellets, Speed Boosts
├── player.py                    # Original Player class (team member)
├── map.py                       # Original map module (team member)
├── assets/
│   └── PacManCharacter.png      # 16×16 pixel art sprite
├── requirements.txt
├── AI_USAGE.md
└── implementation_plan.md
```

## Team

ASI Lõppvoor 2026
