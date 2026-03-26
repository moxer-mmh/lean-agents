---
description: Create or switch to a worktree for a branch or PR number
allowed-tools: Bash(wt:*), Bash(cd:*)
---

# Worktree Checkout

Create a worktree for a branch or PR, or navigate to an existing one.

## Usage

```bash
# Checkout a branch (creates worktree if needed)
wt checkout agent/mobile/KAN-132-feature

# Checkout a PR by number (fetches branch, creates worktree)
wt checkout pr:42

# Create a new branch from origin/main
wt create agent/backend/KAN-141-stripe
```

The command prints the worktree path. Navigate to it with `cd`.

**IMPORTANT:** This is the ONLY safe way to start working on a branch in a multi-worktree setup. Never use `git checkout` or `git switch` inside an existing worktree.
