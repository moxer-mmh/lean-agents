---
description: List all worktrees and navigate to a different one, or checkout a PR
allowed-tools: Bash(wt:*), Bash(git:*), Bash(cd:*)
---

# Worktree Switch

List all active worktrees and navigate to a different one. Supports checking out PRs into worktrees.

## Steps

1. List all worktrees:
   ```bash
   wt list
   ```

2. To switch to an existing worktree:
   ```bash
   cd <worktree-path>
   ```

3. To checkout a PR into a worktree:
   ```bash
   wt checkout pr:<number>
   # Then cd to the printed path
   ```

4. To checkout a branch into a worktree:
   ```bash
   wt checkout <branch-name>
   # Then cd to the printed path
   ```

**IMPORTANT:** Never use `git checkout <branch>` or `git switch <branch>` in a worktree. Each worktree is locked to its branch. Use `wt checkout` to create a new worktree, or `cd` to navigate between existing ones.
