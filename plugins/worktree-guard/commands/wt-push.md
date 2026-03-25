---
description: Push current worktree branch with proper upstream tracking
allowed-tools: Bash(git:*)
---

# Worktree Push

Push the current branch with correct upstream tracking set. Always uses `-u origin HEAD` to avoid the wrong-branch-target issue common in worktrees.

## Context

- Current branch: !`git branch --show-current`
- Current tracking: !`git branch -vv --no-color | grep '^\*'`
- Worktree check: !`test -f .git && echo "IN WORKTREE" || echo "MAIN REPO"`

## Steps

1. Verify we are NOT on main:
   ```bash
   git branch --show-current
   ```
   If on `main` or `master`, STOP and tell the user to switch to a feature branch.

2. Push with upstream tracking:
   ```bash
   git push -u origin HEAD
   ```

3. Verify tracking was set correctly:
   ```bash
   git branch -vv --no-color | grep '^\*'
   ```

4. Show the remote URL for confirmation:
   ```bash
   git remote get-url origin
   ```

**IMPORTANT:** Always use `git push -u origin HEAD`, never bare `git push`. HEAD resolves to the current branch name, ensuring the push targets the correct remote branch.
