---
name: Documenting AI Usage
description: Strict rules and formatting for tracking AI contributions in the project's AI_USAGE.md file.
---

# Documenting AI Usage

You must strictly document all AI usage within this project in the `AI_USAGE.md` file at the root of the repository. To maintain a transparent and trackable history, all AI-assisted development must adhere strictly to the following rules:

## Rules for AI Usage

1. **Separation by Prompts**: All documentation must be separated by the prompts given to the AI. Each prompt gets its own dedicated section.
2. **Commit Tracking**: Every single commit that was made during the generation of a specific prompt needs to be listed in that prompt's section. This ensures we can track exactly what commits were due to what prompts.
3. **Chronological Order**: The commits under each section must be listed in chronological order.
4. **Descriptive Messages**: Commit messages must be descriptive and clearly state what was changed.
5. **Containment**: All AI usage documentation must be contained exclusively within `AI_USAGE.md`.
6. **Prompt Entry**: The original prompt should be collected from the user (or provided directly) and added to the document exactly as it was written.

## Required Format

When documenting a new prompt or set of changes, append a section in `AI_USAGE.md` exactly like this template:

### Prompt [nr]

**The prompt:**

> [Copy and paste the user's prompt here]

**Commits:**

- `[Commit Hash]` - [Commit message]
- `[Commit Hash]` - [Commit message]

**Explanation of changes:**
[A clear and concise explanation of the changes that this prompt made to the repository.]

## Workflow for Agents

1. Perform the task requested by the user.
2. Make distinct, atomic commits for the changes.
3. Before concluding your execution, ensure that `AI_USAGE.md` is updated with the respective commit hashes, messages, and explanation of changes.
4. If you do not have the exact prompt, ask the user to provide it or leave a placeholder in the `> [Copy and paste the user's prompt here]` section and explicitly remind the user to fill it in.

Additional info:
I have updated the

AI_USAGE.md
file to properly document both Prompt 1 and your current Prompt 2. I also added placeholders [Paste Prompt 1 Commit Hash Here] and [Paste Prompt 2 Commit Hash Here] in the respective sections for you to fill in.

If you are committing both of these changes together as a single commit right now, you can use the following commands in your terminal:

bash
git add AI_USAGE.md
git commit -m "docs: Format AI_USAGE.md rules and add AI logs for Prompts 1 and 2"
Once you have run that commit, you can grab the commit hash (you can use git log -1 --format="%H" to get the exact hash easily) and paste it over the placeholders in the document.

Since updating the markdown file with the commit hash is technically another change, you could follow it up with a quick amend or a secondary small commit if you want the hash baked into the repository version perfectly:

bash
git add AI_USAGE.md
git commit --amend --no-edit
