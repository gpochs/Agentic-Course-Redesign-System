# OpenCode V2 capability boundary

## Supported by the composed overlays

- Active project instructions through root `AGENTS.md`.
- Portable skill discovery from `.claude/skills/course-redesign/`.
- The portable core's pre-source Gate 0A and complete Gate 0-through-HITL3
  sequence, verified production handoff, explicit terminal dormant lifecycle,
  and proposal-only post-HITL3 system-review offer.
- Ten project-local subagents in `.opencode/agents/`.
- Ordered agent permissions that deny every action first and then allow only
  `read`, `glob`, `grep`, and the `course-redesign` skill.
- Git sharing of static Markdown templates after human review.

## Unsupported or intentionally omitted

- Edit/write/patch, shell, external-directory, web, nested-subagent, MCP,
  session, integration, provider/model, or publication authority.
- An `instructions` config array, because current V2 retains but does not
  resolve its entries into model context.
- Executable `.opencode/plugins/` content or configured package plugins. The V2
  plugin API is beta and plugins run in-process; no executable extension is
  required for this adapter.
- OpenCode installation, activation, account access, or runtime verification.
- Course-material production, scheduling, or reusable-system activation.
- Any source discovery before Gate 0A, or automatic continuation of a terminal
  `complete_dormant` run. Trigger guidance is informational only.

The permission rules are defense in depth; the shared state capsule, source
policy, gate sequence, and lecturer decision rights remain mandatory. If a host
version does not recognize these current V2 fields, do not fall back to a
broader agent—stop and review the version-specific documentation.
