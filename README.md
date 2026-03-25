# Claude Toolbox

A Claude Code plugin marketplace with tools for multi-agent workflows.

## Plugins

### lean-agents

Lightweight subagent replacements that avoid context bloat from inherited MCP tool schemas. When you have many MCP servers configured, Claude Code's built-in agents (Explore, Plan, general-purpose) can fail because the inherited tool schemas exceed context limits. These agents use explicit tool allowlists or Opus's 1M context to work around that.

This plugin provides lightweight agent replacements that use explicit `tools:` allowlists to try to reduce or avoid inheriting MCP tool schemas. This is a runtime-dependent workaround rather than a guaranteed fix (see [Limitations](#limitations)):

| Agent | Model | Tools | Use Instead Of |
|-------|-------|-------|----------------|
| `lean-explore` | Sonnet | Glob, Grep, Read, Bash, LS | Explore |
| `lean-plan` | Sonnet | Read, Grep, Glob | Plan |
| `lean-general` | Sonnet | Read, Write, Edit, Bash, Grep, Glob | general-purpose |
| `lean-explore-safe` | Opus | All (1M context) | Explore |
| `lean-plan-safe` | Opus | All (1M context) | Plan |
| `lean-general-safe` | Opus | All (1M context) | general-purpose |

- **Standard variants** (`lean-explore`, `lean-plan`, `lean-general`): Use Sonnet with a restricted tool set. Cheaper and faster. Try these first.
- **Safe variants** (`lean-explore-safe`, `lean-plan-safe`, `lean-general-safe`): Use Opus with 1M context window. Much less likely to hit prompt limits. Use these if the standard variants still fail.

### worktree-guard

Automatic safety guards for git worktrees. Claude Code has well-documented issues with worktrees: wrong branch detection, push to wrong upstream, broken pull/rebase, and `git checkout` corrupting worktree state. This plugin fixes all of that with automatic hooks and safe commands.

**Hooks (automatic, no user action needed):**
- Blocks `git push` to main/master
- Blocks `git push` without upstream tracking (suggests `git push -u origin HEAD`)
- Warns on bare `git pull` in worktrees (suggests fetch + rebase)
- Blocks `git checkout <branch>` in worktrees (explains to use `cd`)
- Blocks `git commit` on main/master
- Blocks git operations on detached HEAD
- Shows branch tracking info after push/commit

**Commands:**
- `/wt-sync` — Safe rebase from main (fetch + rebase, auto-stash)
- `/wt-push` — Push with correct upstream tracking
- `/wt-status` — Worktree health check (tracking, ahead/behind, all worktrees)
- `/wt-switch` — List worktrees and navigate between them

**Skill:**
- `worktree-safety` — Teaches Claude Code worktree-safe git patterns (auto-activates when in a worktree)

**Agent:**
- `worktree-doctor` — Diagnoses and fixes worktree issues (wrong upstream, stale worktrees, detached HEAD)

## Installation

### From the marketplace

1. Inside Claude Code, run `/plugin` and select "Add Marketplace"
2. Enter `moxer-mmh/lean-agents`
3. Install `lean-agents` and/or `worktree-guard` from the marketplace
4. Restart Claude Code

### Manual (settings.json)

Add this marketplace to your Claude Code settings:

```json
// ~/.claude/settings.json
{
  "extraKnownMarketplaces": {
    "claude-toolbox": {
      "source": {
        "source": "git",
        "url": "https://github.com/moxer-mmh/lean-agents.git"
      }
    }
  },
  "enabledPlugins": {
    "lean-agents@claude-toolbox": true,
    "worktree-guard@claude-toolbox": true
  }
}
```

Or enable selectively — you can use one without the other.

### From this repository (local testing)

If you've cloned this repo, you can point Claude Code at the local directory:

```bash
# Copy lean-agents to your user agents directory for immediate use
cp plugins/lean-agents/agents/*.md ~/.claude/agents/
```

## How It Works

### worktree-guard hooks

The hooks run automatically on every `Bash` tool call that contains a git command. They read the tool input from stdin, check for dangerous patterns, and either:
- **Block** (exit code 2) — prevents the operation with an explanation
- **Warn** (stdout JSON with `systemMessage`) — allows but injects guidance
- **Allow** (exit code 0) — no-op for non-git commands

Performance impact is negligible — the hook exits immediately for non-git commands.

### Worktree detection

The plugin detects worktrees by checking if `.git` is a **file** (worktrees) vs a **directory** (main repo). Some guards only activate in worktrees (e.g., checkout blocking), while others apply everywhere (e.g., push-to-main blocking).

## Limitations

- **Standard variants** (Sonnet) restrict tools via `tools:` allowlist, so they intentionally exclude MCP tools. They may still fail if the runtime doesn't respect the allowlist for MCP tool schema filtering (this is the core bug in [#37793](https://github.com/anthropics/claude-code/issues/37793))
- **Safe variants** (Opus) do not restrict tools — they rely on the 1M context window to fit everything. They may still receive MCP tools. While much less likely to hit prompt limits, extremely large MCP configurations could theoretically still overflow
- Standard variants are designed for pure codebase work without MCP tools. Safe variants may have MCP access depending on the runtime's tool inheritance behavior
- This is a workaround, not a fix. The proper solution is for Claude Code to support controllable subagent context ([#31623](https://github.com/anthropics/claude-code/issues/31623))

## Requirements

- Python 3.8+ (for worktree-guard hooks)
- Git 2.20+ (for worktree support)
- Claude Code

## License

MIT
