# OpenCode V2 adapter

Adapter release: `0.2.3`. Shared semantic base: inactive candidate
`ACR-SYS-20260821-005` version `0.2.3`.

This overlay adds ten project-local OpenCode V2 subagent profiles to the
portable core. OpenCode V2 natively discovers the core's root `AGENTS.md` and
the compatibility skill at `.claude/skills/course-redesign/`, so no duplicate
instruction file or `opencode.jsonc` is needed.

Release `0.2.3` inherits the portable core's pre-source Gate 0A, schema-8
lineage vocabulary, verified production handoff before HITL 3, terminal
`complete_dormant` lifecycle, and one-time informational trigger guidance. The
OpenCode wrappers add no independent gate, state, automation, permission, or
schedule behavior.

Compose `../00_Portable_Core_Adapter/overlay/` first, then this `overlay/`,
relative to the same reviewed project root:

```text
<project-root>/
├── AGENTS.md                                  # portable core; active V2 source
├── .claude/skills/course-redesign/            # portable core; discovered
└── .opencode/
    └── agents/
        └── <ten read-only role>.md
```

Every agent uses `mode: subagent` and ordered V2 permission rules: deny all,
then allow only project reads, globbing, grepping, and skill loading. No model or
provider is selected. The wrappers require a current orchestrator state capsule
and contain no independent workflow logic.

No executable OpenCode plugin is included. Static instructions, skills, and
agent Markdown cover the need; V2 plugins execute in-process, local plugin files
are auto-discovered, and the official plugin API is currently beta. Adding a
plugin would therefore create unnecessary activation and execution risk.

No `instructions` config entry is included either. Current V2 documentation
says the schema retains that array but does not resolve its entries into model
instructions; `AGENTS.md` is the active project mechanism.

Official references:

- [OpenCode V2 instructions](https://opencode.ai/v2/docs/instructions)
- [OpenCode V2 agents](https://opencode.ai/v2/docs/agents)
- [OpenCode V2 skills](https://opencode.ai/v2/docs/skills)
- [OpenCode V2 permissions](https://opencode.ai/v2/docs/permissions)
- [OpenCode V2 plugins](https://opencode.ai/v2/docs/build/plugins)
