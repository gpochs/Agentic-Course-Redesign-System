# Claude Code capability boundary

## Supported by this overlay

- Root project guidance through `CLAUDE.md` importing the portable `AGENTS.md`.
- Path-scoped safety guidance under `.claude/rules/`.
- The native project skill location `.claude/skills/course-redesign/` supplied
  by the portable core.
- Ten project subagents under `.claude/agents/`, each with the shared skill
  preloaded and only `Read`, `Glob`, and `Grep` available.
- Version control of project instructions, rules, skills, and agents.

## Unsupported or intentionally omitted

- Write, Edit, Bash, PowerShell, WebFetch, WebSearch, MCP, hook, background,
  worktree, team, scheduling, or application/account authority.
- User-level or managed configuration.
- Claude Code plugin packaging or a plugin marketplace. Project-native files
  already cover the adapter, while plugins require separate installation and
  enablement decisions.
- Automatic exact-target production, publication, or runtime activation.

Claude Code may invoke a described subagent when it judges it relevant. Every
profile therefore validates the current capsule and stops before analysis when
the orchestrator has not assigned that role and stage. Host permission modes
can affect behavior; the explicit three-tool allowlist is the adapter's primary
read-only boundary.

