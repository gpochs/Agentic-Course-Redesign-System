# GitHub Copilot capability boundary

## Native plugin

The `0.2.4-copilot.1` package supplies:

- Six Agentic Course Redesign workflow skills with the Copilot v0.2.4
  lecturer-dialogue contract.
- Ten manually selected, read-only specialist agents.
- Preview-first setup, deterministic no-overwrite Gate-0A record generation,
  source-manifest, fingerprinting, schema migration, and state-validation
  helpers.
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

The dialogue contract keeps one unresolved consequential question at a time
and uses the native `ask_user` card for the complete valid option set whenever
the live GitHub Copilot host accepts it. A live Copilot host has demonstrated
at least five explicit choices plus a custom-answer field; this is an observed
capability, not a maximum. Do not state or assume an unsupported maximum. Never
prune, hide or combine valid choices merely to fit a card. If the host rejects
or cannot present the complete valid set, it asks one ordinary chat question
listing every valid numbered option plus `Other`, then waits. For very long
sets, dependency chunks are allowed only when choices share evidence or
constrain one another. Keep every valid option visible across chunks. All paths
preserve custom answers, recap chunks/gates, fail closed on uncertainty, and
keep authority gates separate. A safest truthful, evidence-aligned, reversible
recommendation may be marked but is never preselected.

Copilot 1.0.80 BYOK compatibility invokes the packaged Gate-0A generator via
PowerShell/Python (known `type=function`), not `apply_patch`. An `expected
function` failure after `apply_patch` was recorded as `type=custom` may be
poisoned task history; use a fresh task and prefer GitHub-hosted GPT-5.4 or the
default Claude model. No MCP, hook, authentication, or permission is added.

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
