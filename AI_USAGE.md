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
