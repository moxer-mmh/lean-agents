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

## Rules

### 1. Push: ALWAYS use `-u origin HEAD`

```bash
# NEVER do this:
git push
git push origin my-branch

# ALWAYS do this:
git push -u origin HEAD
```

**Why:** Worktrees often lack upstream tracking. `HEAD` resolves to the current branch name, ensuring the push targets the correct remote branch. The `-u` flag sets tracking for future operations.

### 2. Sync from main: fetch + rebase, NEVER bare pull

```bash
# NEVER do this:
git pull
git pull origin main

# ALWAYS do this:
git fetch origin main
git rebase origin/main
```

**Why:** `git pull` in worktrees creates merge commits and can corrupt tracking. Fetch + rebase keeps linear history and avoids worktree-specific tracking bugs.

Use `/wt-sync` for a safe one-command alternative.

### 3. Branch switching: NEVER use git checkout or git switch

```bash
# NEVER do this in a worktree:
git checkout other-branch
git switch other-branch

# ALWAYS do this:
cd /path/to/other/worktree
```

**Why:** Each worktree is locked to exactly one branch. Attempting to switch branches corrupts the worktree state. Navigate between worktrees using `cd`.

Use `/wt-switch` to list available worktrees.

### 4. Before every commit: verify branch

```bash
# Always check first:
BRANCH=$(git branch --show-current)
echo "Committing on: $BRANCH"
```

Block if on `main`, `master`, or if HEAD is detached (empty branch name).

### 5. After creating a worktree: set upstream immediately

```bash
# After first commit in a new worktree:
git push -u origin HEAD
```

This prevents all future push/pull tracking issues.

### 6. Creating new worktrees

```bash
# From the main repo (not from inside another worktree):
git worktree add /path/to/new-worktree -b branch-name origin/main
```

### 7. Cleaning up worktrees

```bash
# After merging a branch:
git worktree remove /path/to/worktree
git branch -d branch-name
```

## Quick Reference

| Operation | Wrong | Right |
|-----------|-------|-------|
| Push | `git push` | `git push -u origin HEAD` |
| Sync main | `git pull` | `git fetch origin main && git rebase origin/main` |
| Switch branch | `git checkout X` | `cd /path/to/worktree-X` |
| Check branch | _(skip)_ | `git branch --show-current` before commit |

## Available Commands

- `/wt-sync` — Safe rebase from main
- `/wt-push` — Push with correct upstream
- `/wt-status` — Worktree health check
- `/wt-switch` — Navigate between worktrees
