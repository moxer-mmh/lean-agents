---
name: worktree-safety
description: Use this skill when performing any git operation (commit, push, pull, rebase, checkout, branch, switch) inside a git worktree, when the user mentions worktrees, multi-agent workflows, parallel development branches, or when you detect that .git is a file (not directory). Also activates when git push fails due to tracking issues or when git pull creates unexpected merge commits.
---

# Worktree-Safe Git Operations

## How to Detect You're in a Worktree

```bash
# .git is a FILE in worktrees, a DIRECTORY in the main repo
test -f .git && echo "WORKTREE" || echo "MAIN REPO"
```

If `.git` is a file, ALL rules below are mandatory.

## Primary Tool: `wt` CLI

The `wt` command handles all worktree operations safely. **Always use `wt` instead of raw git worktree commands.**

```bash
wt help          # Show all available commands
wt status        # Health check of current worktree
wt list          # List all worktrees
```

## Rules

### 1. Push: use `wt push`

```bash
# NEVER do this:
git push
git push origin my-branch

# ALWAYS do this:
wt push
```

**Why:** `wt push` always uses `-u origin HEAD`, which sets upstream tracking correctly. Raw `git push` in worktrees often fails due to missing upstream tracking.

### 2. Sync from main: use `wt sync`

```bash
# NEVER do this:
git pull
git pull origin main

# ALWAYS do this:
wt sync
```

**Why:** `wt sync` does `git fetch origin main && git rebase origin/main` with automatic stash/unstash. `git pull` creates merge commits and corrupts tracking in worktrees.

### 3. Branch switching: use `wt checkout` or `cd`

```bash
# NEVER do this in a worktree:
git checkout other-branch
git switch other-branch

# ALWAYS do this:
wt checkout other-branch   # Creates/finds worktree, prints path
cd /path/to/worktree       # Navigate to it

# For PRs:
wt checkout pr:42          # Fetches PR branch, creates worktree
```

**Why:** Each worktree is locked to exactly one branch. Attempting to switch branches corrupts the worktree state.

### 4. Creating worktrees: use `wt create`

```bash
# NEVER do this:
git worktree add /some/path -b branch-name origin/main

# ALWAYS do this:
wt create agent/mobile/KAN-132-feature
wt create agent/backend/KAN-141-stripe origin/main
```

**Why:** `wt create` handles directory naming, upstream tracking, and fetches the latest main automatically.

### 5. Before every commit: verify branch

```bash
# Always check first:
git branch --show-current
```

Block if on `main`, `master`, or if HEAD is detached (empty branch name).

### 6. Cleanup: use `wt clean`

```bash
wt clean    # Prunes stale worktrees + deletes merged branches via gh-poi
```

## Quick Reference

| Operation | Wrong | Right |
|-----------|-------|-------|
| Push | `git push` | `wt push` |
| Sync main | `git pull` | `wt sync` |
| Switch branch | `git checkout X` | `wt checkout X` then `cd` |
| Create worktree | `git worktree add ...` | `wt create <branch>` |
| Checkout PR | manual fetch + checkout | `wt checkout pr:42` |
| Check health | manual git commands | `wt status` |
| Cleanup | manual prune | `wt clean` |

## Available Commands

- `/wt-checkout` — Create/switch to a worktree for a branch or PR
- `/wt-sync` — Safe rebase from main
- `/wt-push` — Push with correct upstream
- `/wt-status` — Worktree health check
- `/wt-switch` — List and navigate between worktrees
- `/wt-clean` — Prune stale worktrees and merged branches

## Fallback (if `wt` is not installed)

If `wt` command is not available, use these raw git equivalents:

| Operation | Fallback |
|-----------|----------|
| Push | `git push -u origin HEAD` |
| Sync | `git fetch origin main && git rebase origin/main` |
| Create worktree | `git worktree add <path> -b <branch> origin/main` |
| List | `git worktree list` |
| Clean | `git worktree prune && gh poi` |
