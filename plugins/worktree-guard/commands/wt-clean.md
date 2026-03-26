---
description: Prune stale worktrees and clean up merged branches
allowed-tools: Bash(wt:*), Bash(git:*), Bash(gh:*)
---

# Worktree Clean

Prune stale worktrees (paths that no longer exist) and clean up local branches that have been merged.

## Steps

1. Run the cleanup:
   ```bash
   wt clean
   ```

This will:
- Prune stale worktrees with `git worktree prune`
- Use `gh poi` to safely delete local branches whose PRs have been merged
