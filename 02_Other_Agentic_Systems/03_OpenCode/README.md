# OpenCode V2 adapter

## Install the native skills and agents

OpenCode discovers Markdown skills and subagents at project or account scope. From the repository root, build the edition into a new directory with Python 3.11 or newer.

```shell
python 02_Other_Agentic_Systems/build_host_package.py opencode <new-package-directory>
```

For global use, copy the generated `skills/course-redesign/` into `~/.config/opencode/skills/` and the ten `agents/*.md` into `~/.config/opencode/agents/`. For one project, use `<project>/.opencode/skills/` and `<project>/.opencode/agents/` instead. Review filename collisions before copying. The skill contains the six stage guides, reference material, setup scripts and course template. OpenCode uses its existing provider connection. Select an included model in the desktop app and start a fresh local session, then ask it to use the course-redesign skill. Try “Skip the material check and design from my goal.” The lecturer still approves the plan and each output. The project overlay below is also available for existing layouts.

[OpenCode skills](https://opencode.ai/docs/skills/) · [OpenCode subagents](https://opencode.ai/docs/agents/)

## Manual project overlay


Adapter release: `0.3.1`. Shared semantic base: inactive candidate
`ACR-SYS-20261127-002` version `0.3.1`.

This overlay adds ten project-local OpenCode V2 subagent profiles to the
portable core. OpenCode V2 natively discovers the core's root `AGENTS.md` and
the compatibility skill at `.claude/skills/course-redesign/`, so no duplicate
instruction file or `opencode.jsonc` is needed.

Release `0.3.1` inherits the portable core's pre-source Gate 0A, unchanged
schema-8 lineage vocabulary, one-decision interaction contract, verified
production handoff before HITL 3, terminal `complete_dormant` lifecycle, and
one-time informational trigger guidance. OpenCode documents a native question
tool with options and a custom answer but no maximum. The adapter may use it
only when the live host accepts the complete option set plus that custom-answer
path; otherwise it uses the portable ordinary-chat fallback with every valid
numbered option plus `Other`. It never prunes, hides or combines choices to
simulate a card. The wrappers add no independent gate, state, automation,
permission, or schedule behavior.

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
