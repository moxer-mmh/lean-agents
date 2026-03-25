---
description: Safely sync current worktree branch with main (fetch + rebase, no merge commits)
allowed-tools: Bash(git:*)
---

# Worktree Sync

Safely rebase the current worktree branch onto the latest main. This avoids the merge commits and tracking issues that `git pull` causes in worktrees.

## Context

- Current branch: !`git branch --show-current`
- Worktree check: !`test -f .git && echo "IN WORKTREE" || echo "MAIN REPO"`
- Uncommitted changes: !`git status --porcelain`

## Steps

1. If there are uncommitted changes, stash them first:
   ```bash
   git stash push -m "wt-sync: auto-stash before rebase"
   ```

2. Fetch latest main from remote:
   ```bash
   git fetch origin main
   ```

3. Rebase current branch onto main:
   ```bash
   git rebase origin/main
   ```

4. If rebase has conflicts, stop and inform the user. Do NOT force or abort automatically.

5. If changes were stashed in step 1, pop the stash:
   ```bash
   git stash pop
   ```

6. Show final status:
   ```bash
   git log --oneline origin/main..HEAD
   git status --short
   ```

**IMPORTANT:** Never use `git pull` in a worktree. Always use `git fetch` + `git rebase`.
