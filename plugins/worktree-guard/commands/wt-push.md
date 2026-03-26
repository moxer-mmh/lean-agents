---
description: Push current worktree branch with proper upstream tracking
allowed-tools: Bash(wt:*), Bash(git:*)
---

# Worktree Push

Push the current branch with correct upstream tracking.

## Steps

1. Run the push:
   ```bash
   wt push
   ```

2. If `wt` is not available, fall back to:
   ```bash
   git push -u origin HEAD
   ```

**IMPORTANT:** Never use bare `git push` in a worktree. Always use `wt push` or `git push -u origin HEAD`.
