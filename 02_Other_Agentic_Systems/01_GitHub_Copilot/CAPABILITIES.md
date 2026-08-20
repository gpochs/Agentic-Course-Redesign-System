# GitHub Copilot capability boundary

## Supported by this overlay

- Repository-wide guidance in `.github/copilot-instructions.md`.
- Path-specific evidence-handling guidance in
  `.github/instructions/course-redesign.instructions.md` on supporting
  surfaces.
- Ten project custom agents in `.github/agents/*.agent.md`.
- The portable skill in `.claude/skills/course-redesign/` supplied by the core
  overlay.
- Read-only specialist discovery and reporting with `read` and `search` tools.

## Unsupported or intentionally omitted

- Automatic custom-agent inference: every supplied profile disables it.
- `edit`, `execute`, `web`, `agent`, MCP, GitHub API, pull-request, issue,
  Actions, secret, or repository-administration authority.
- Copilot plugin packaging. A plugin is unnecessary for static project files
  and would add installation and activation state.
- Any guarantee that a given Copilot surface supports all three instruction,
  skill, and custom-agent mechanisms. Current official support is
  surface-dependent.
- Course-material writes, publication, schedule registration, or reusable
  runtime activation.

If a later project needs research or exact-target production, define and review
that course-specific authority separately after the relevant lecturer gate; do
not widen these shared profiles silently.

