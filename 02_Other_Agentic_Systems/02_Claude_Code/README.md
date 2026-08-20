# Claude Code adapter

Adapter release: `0.2.0`. Validated semantic base: `0.1.0`.

This overlay adds a project `CLAUDE.md`, one path-scoped rule, and ten
project-local Claude Code subagents to the portable core. It does not open or
configure Claude Code, install a plugin, add hooks, define MCP servers, or alter
user/managed settings.

Compose `../00_Portable_Core_Adapter/overlay/` first, then this `overlay/`,
relative to the same reviewed project root:

```text
<project-root>/
├── AGENTS.md                                  # portable core
├── CLAUDE.md                                  # imports AGENTS.md
└── .claude/
    ├── skills/course-redesign/                # portable core
    ├── rules/course-redesign.md
    └── agents/<ten read-only role>.md
```

Each subagent preloads the shared `course-redesign` skill and exposes only
`Read`, `Glob`, and `Grep`. It must receive a current orchestrator state capsule
and fail closed otherwise. The wrappers do not duplicate the gate sequence or
specialist contracts.

Review collisions manually and commit these project files only if the
repository owner wants them shared. Copying the overlay does not launch Claude
Code, invoke a subagent, approve data egress, or activate a reusable runtime.

Official references:

- [Claude Code memory and `CLAUDE.md`](https://code.claude.com/docs/en/memory)
- [Claude Code rules](https://code.claude.com/docs/en/memory#organize-rules-with-clauderules)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)
