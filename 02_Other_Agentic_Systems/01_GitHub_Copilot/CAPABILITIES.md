# GitHub Copilot capability boundary

## Native plugin

The `0.3.1` package supplies:

- Six Agentic Course Redesign workflow skills with the Copilot v0.3.1
  lecturer-dialogue contract.
- Ten orchestrator-assigned, read-only specialist agents.
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

In GitHub Copilot App/CLI 1.0.80 with an OpenAI-compatible BYOK provider such
as CommandCode Chat Completions, `apply_patch` can be recorded as `type=custom`
and poison the saved task history. The compatibility rule therefore applies to
every file mutation, not only Gate 0A: never use `apply_patch` in an affected
session. Use a packaged helper or function-style PowerShell/Python, while
retaining exact-target preview, the existing approval gate, expected-current-
SHA-256 checks for modifications, atomic writes, reread, and validation.

If the host returns `expected "function"`, do not retry in that task. Start a
fresh project task, recover durable state read-only, and first verify whether
the prior edit already succeeded. This is a tool-history serialization defect,
not a missing function. No MCP server, plugin, hook, authentication, or added
permission fixes it or is required by this package.

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
