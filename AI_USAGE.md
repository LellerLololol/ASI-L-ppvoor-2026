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

- `[Paste Commit Hash Here]` - feat: Add Player class with grid-aligned movement and visual effects

**Explanation of changes:**
Created `player.py` containing the `Player` class (extends `pygame.sprite.Sprite`) responsible for the Pac-Man character and movement system. The class loads and scales the user's 16×16 pixel art sprite, pre-computes directional variants (flip/rotate) so the character faces its movement direction, and implements grid-aligned movement with wall collision detection. Visual effects include configurable squash & stretch animation, directional eye pupil overlay aligned with the sprite's existing eyes, and a fading particle trail. All parameters (speed, squash amount, eye offset, trail lifetime, colors, pupil size/shift) are passed via the constructor — nothing is hardcoded. Input supports both arrow keys and WASD.
