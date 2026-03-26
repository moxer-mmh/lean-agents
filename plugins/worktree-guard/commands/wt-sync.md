---
description: Safely sync current worktree branch with main (fetch + rebase, no merge commits)
allowed-tools: Bash(wt:*), Bash(git:*)
---

# Worktree Sync

Safely rebase the current worktree branch onto the latest main.

## Steps

1. Run the sync:
   ```bash
   wt sync
   ```

2. If `wt` is not available, fall back to:
   ```bash
   git stash push -m "wt-sync: auto-stash" 2>/dev/null
   git fetch origin main
   git rebase origin/main
   git stash pop 2>/dev/null
   ```

3. If rebase has conflicts, stop and inform the user. Do NOT force or abort automatically.

**IMPORTANT:** Never use `git pull` in a worktree. Always use `wt sync` or `git fetch` + `git rebase`.
