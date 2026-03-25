#!/usr/bin/env python3
"""
Worktree Guard — PreToolUse and PostToolUse hook for Claude Code.

Prevents common git mistakes in worktrees:
- Push to main branch
- Push without upstream tracking
- Bare git pull (should use fetch+rebase)
- git checkout in worktree (should use cd)
- Commit on main branch
- Operations on detached HEAD

Usage (from hooks.json):
  python3 worktree_guard.py pre   # PreToolUse
  python3 worktree_guard.py post  # PostToolUse
"""

import json
import os
import subprocess
import sys


def git(*args):
    """Run a git command and return stripped stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def is_worktree():
    """Check if current directory is a git worktree (not the main repo)."""
    git_path = os.path.join(os.getcwd(), ".git")
    return os.path.isfile(git_path)


def current_branch():
    """Get current branch name, or None if detached."""
    return git("branch", "--show-current") or None


def has_upstream():
    """Check if current branch has an upstream tracking branch."""
    return git("rev-parse", "--abbrev-ref", "@{u}") is not None


def is_detached_head():
    """Check if HEAD is detached."""
    branch = git("branch", "--show-current")
    return branch == "" or branch is None


def extract_command(tool_input):
    """Extract the shell command string from tool_input."""
    if isinstance(tool_input, dict):
        return tool_input.get("command", "")
    return ""


def is_git_command(cmd, *subcommands):
    """Check if a command string contains a git subcommand."""
    for sub in subcommands:
        if f"git {sub}" in cmd:
            return True
    return False


def has_flag(cmd, *flags):
    """Check if command contains any of the given flags."""
    for flag in flags:
        if flag in cmd:
            return True
    return False


def block(message):
    """Block the operation (PreToolUse exit code 2)."""
    print(message, file=sys.stderr)
    sys.exit(2)


def warn(message):
    """Allow but inject a warning message into Claude's context."""
    output = {"systemMessage": message}
    print(json.dumps(output), file=sys.stdout)
    sys.exit(0)


def allow():
    """Allow the operation silently."""
    sys.exit(0)


# ─── PreToolUse Guards ──────────────────────────────────────────────────────


def pre_tool_use(cmd):
    """Run all PreToolUse guards on a Bash command."""

    # Guard: commit on main
    if is_git_command(cmd, "commit"):
        branch = current_branch()
        if branch == "main" or branch == "master":
            block(
                "❌ BLOCKED: Cannot commit directly to main.\n"
                "   Create a feature branch first:\n"
                "   git checkout -b agent/<domain>/KAN-XXX-description"
            )
        if is_detached_head():
            block(
                "❌ BLOCKED: HEAD is detached — commit would be lost.\n"
                "   Create or switch to a branch first:\n"
                "   git checkout -b <branch-name>"
            )

    # Guard: push to main
    if is_git_command(cmd, "push"):
        branch = current_branch()
        if branch == "main" or branch == "master":
            block(
                "❌ BLOCKED: Cannot push directly to main.\n"
                "   Work on a feature branch instead."
            )
        # Guard: push without upstream
        if not has_flag(cmd, "-u", "--set-upstream"):
            if not has_upstream():
                block(
                    "❌ BLOCKED: No upstream tracking branch set.\n"
                    "   Use: git push -u origin HEAD\n"
                    "   This sets the upstream so future pushes work correctly."
                )

    # Guard: bare git pull (should use fetch+rebase in worktrees)
    if is_git_command(cmd, "pull"):
        if is_worktree():
            # Allow if explicit remote+branch specified
            parts = cmd.split()
            try:
                pull_idx = parts.index("pull")
                has_remote = len(parts) > pull_idx + 1 and not parts[
                    pull_idx + 1
                ].startswith("-")
            except (ValueError, IndexError):
                has_remote = False

            if not has_remote and not has_flag(cmd, "--rebase"):
                warn(
                    "⚠️ WARNING: Bare `git pull` in a worktree can create "
                    "merge commits and tracking issues.\n"
                    "   Prefer: git fetch origin main && git rebase origin/main\n"
                    "   Or use: /wt-sync for a safe one-command sync."
                )

    # Guard: git checkout <branch> in worktree
    if is_git_command(cmd, "checkout"):
        if is_worktree():
            # Allow checkout of files (git checkout -- file)
            # Block checkout of branches
            if not has_flag(cmd, "--", "-b", "-B", "-p", "--patch"):
                # Check if it looks like a branch switch
                parts = cmd.split()
                try:
                    co_idx = parts.index("checkout")
                    if co_idx + 1 < len(parts):
                        next_arg = parts[co_idx + 1]
                        if not next_arg.startswith("-"):
                            block(
                                "❌ BLOCKED: Cannot switch branches in a "
                                "worktree with `git checkout`.\n"
                                "   Each worktree is locked to its branch.\n"
                                "   To work on another branch, navigate to "
                                "its worktree:\n"
                                "   cd <worktree-path>\n"
                                "   Or create a new worktree:\n"
                                "   git worktree add ../<name> -b <branch>"
                            )
                except (ValueError, IndexError):
                    pass

    # Guard: git switch in worktree (same issue as checkout)
    if is_git_command(cmd, "switch"):
        if is_worktree():
            if not has_flag(cmd, "-c", "-C", "--create"):
                block(
                    "❌ BLOCKED: Cannot switch branches in a worktree.\n"
                    "   Each worktree is locked to its branch.\n"
                    "   Navigate to the other worktree with `cd` instead."
                )


# ─── PostToolUse Info ────────────────────────────────────────────────────────


def post_tool_use(cmd):
    """Run PostToolUse informational checks."""

    # After push: show tracking info
    if is_git_command(cmd, "push"):
        tracking = git("branch", "-vv", "--no-color")
        if tracking:
            current = None
            for line in tracking.splitlines():
                if line.startswith("*"):
                    current = line
                    break
            if current:
                warn(f"📡 Branch tracking after push:\n   {current.strip()}")

    # After commit: confirm branch
    if is_git_command(cmd, "commit"):
        branch = current_branch()
        if branch:
            warn(f"✅ Committed on branch: {branch}")


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"

    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        allow()

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only process Bash tool calls
    if tool_name != "Bash":
        allow()

    cmd = extract_command(tool_input)

    # Fast exit: skip non-git commands entirely
    if "git " not in cmd and "git\t" not in cmd:
        allow()

    if mode == "pre":
        pre_tool_use(cmd)
    elif mode == "post":
        post_tool_use(cmd)

    allow()


if __name__ == "__main__":
    main()
