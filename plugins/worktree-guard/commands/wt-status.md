---
description: Show git worktree health — branch tracking, upstream, ahead/behind main
allowed-tools: Bash(git:*)
---

# Worktree Status

Comprehensive health check of the current worktree and all active worktrees.

## Context

- Worktree check: !`test -f .git && echo "IN WORKTREE" || echo "MAIN REPO"`

## Steps

Run all of these commands and present the results in a clear summary:

1. **All worktrees:**
   ```bash
   git worktree list
   ```

2. **Current branch + tracking:**
   ```bash
   git branch -vv --no-color
   ```

3. **Ahead/behind main:**
   ```bash
   git rev-list --left-right --count origin/main...HEAD 2>/dev/null || echo "No upstream or main not fetched"
   ```

4. **Working tree status:**
   ```bash
   git status --short
   ```

5. **Stashed changes:**
   ```bash
   git stash list
   ```

## Output Format

Present results as a clear summary table:

```
Worktree Status
───────────────────────────────────────
Location:   /path/to/worktree
Branch:     agent/mobile/KAN-132-feature
Upstream:   origin/agent/mobile/KAN-132-feature (or NONE)
vs main:    3 ahead, 0 behind
Dirty:      2 modified, 1 untracked
Stashed:    0 entries

All Worktrees:
  /path/main          main          [active]
  /path/worktree-1    branch-1      [active]
  /path/worktree-2    branch-2      [active]
```
