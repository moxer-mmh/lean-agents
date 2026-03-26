---
description: Show git worktree health — branch tracking, upstream, ahead/behind main
allowed-tools: Bash(wt:*), Bash(git:*)
---

# Worktree Status

Comprehensive health check of the current worktree and all active worktrees.

## Steps

1. Run the status check:
   ```bash
   wt status
   ```

2. If `wt` is not available, fall back to:
   ```bash
   git worktree list
   git branch -vv --no-color
   git rev-list --left-right --count origin/main...HEAD 2>/dev/null
   git status --short
   ```
