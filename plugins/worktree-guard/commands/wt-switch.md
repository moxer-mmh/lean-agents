---
description: List all worktrees and help navigate to a different one
allowed-tools: Bash(git:*), Bash(ls:*)
---

# Worktree Switch

List all active worktrees and help the user navigate to a different one. In worktrees, you NEVER use `git checkout` to switch branches — you `cd` to the other worktree.

## Context

- Current location: !`pwd`
- Current branch: !`git branch --show-current`

## Steps

1. List all worktrees with their branches:
   ```bash
   git worktree list
   ```

2. Present each worktree as a numbered option:
   ```
   Active worktrees:
   1. /path/to/main           → main
   2. /path/to/worktree-1     → agent/mobile/KAN-132-feature
   3. /path/to/worktree-2     → agent/backend/KAN-141-stripe

   Current: #2 (agent/mobile/KAN-132-feature)
   ```

3. Tell the user to navigate with `cd`:
   ```
   To switch: cd /path/to/worktree-N
   ```

**IMPORTANT:** Never use `git checkout <branch>` or `git switch <branch>` in a worktree. Each worktree is locked to its branch. Navigate between worktrees using `cd`.
