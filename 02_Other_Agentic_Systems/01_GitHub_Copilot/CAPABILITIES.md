# GitHub Copilot capability boundary

## Native plugin

The `0.2.3-copilot.1` package supplies:

- Six canonical Agentic Course Redesign workflow skills.
- Ten manually selected, read-only specialist agents.
- Preview-first setup, source-manifest, fingerprinting, schema migration, and
  state-validation helpers.
- An inactive Copilot-aware one-course project template.
- A repository marketplace entry for
  `agentic-course-redesign@agentic-course-redesign-system`.
- Participant installation, first-session, verification, removal, cost, and
  support-boundary guidance.

The plugin manifest declares only `skills/` and `agents/`. It contains no
MCP server, connector, application/API integration, authentication, hook, LSP
server, telemetry, schedule, automation, model provider, secret, or additional
permission.

Installing it adds reusable instructions and agent definitions. It does not
read course files, activate the reusable runtime, register a schedule, or
trigger a redesign.

## Project-local overlay

The existing manual overlay remains available and supplies:

- Repository guidance in `.github/copilot-instructions.md`.
- Path-specific evidence-handling guidance in
  `.github/instructions/course-redesign.instructions.md` on supporting
  surfaces.
- Ten project agents in `.github/agents/*.agent.md`.
- The portable `.claude/skills/course-redesign/` skill when composed after
  the portable-core overlay.

Project-level agents or skills with matching names can take precedence over
installed plugin components. Use one route deliberately and review collisions.

## Deliberately unsupported

- Automatic marketplace registration or plugin installation: participants
  confirm both steps.
- Automatic custom-agent inference: every supplied specialist must be
  deliberately selected or assigned within the current run.
- MCP, external authentication, provider accounts, publisher services, or
  background processes.
- Course-material writes without the exact lecturer-approved stage and target.
- Publication, schedule registration, or reusable runtime activation.
- Source discovery before Gate 0A.
- Resuming a terminal `complete_dormant` run.
- A support SLA, guaranteed maintenance, or assumption that the plugin itself
  makes GitHub Copilot free. Participants use their own Copilot access.

If research or production is required, define and review its course-specific
source, tool, egress, audience, and exact-target authority after the relevant
lecturer gate. Never widen shared plugin permissions silently.
