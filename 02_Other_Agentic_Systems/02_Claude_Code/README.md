# Claude Code adapter

## Install for an account or a project

From the repository root, build the standalone plugin with Python 3.11 or newer. For a personal installation, pass a new directory under `~/.claude/skills/agentic-course-redesign`. For one course project, use `<project>/.claude/skills/agentic-course-redesign`. Expand the home path in your shell. The builder refuses to replace an existing directory.

```shell
python 02_Other_Agentic_Systems/build_host_package.py claude <new-plugin-directory>
claude plugin validate <new-plugin-directory>
```

Open a trusted local Claude Code project and reload plugins. Invoke `/gpochs-course-redesign` or the namespaced `course-redesign-orchestrator` skill. Select an included Fable or Opus model in Claude. Agents inherit the session model. Start with a course description, choose **Skip for now**, and review an editable example after the usual human decisions. If native delegation or a choice card is unavailable, the orchestrator can run the perspectives sequentially and ask the same question in chat. The older overlay below remains available for existing project layouts.

[Claude skill discovery](https://code.claude.com/docs/en/skills) · [Skill-directory plugins](https://code.claude.com/docs/en/plugins/create)

## Manual project overlay


Adapter release: `0.3.0`. Shared semantic base: inactive candidate
`ACR-SYS-20261127-001` version `0.3.0`.

This overlay adds a project `CLAUDE.md`, one path-scoped rule, and ten
project-local Claude Code subagents to the portable core. It does not open or
configure Claude Code, install a plugin, add hooks, define MCP servers, or alter
user/managed settings.

Release `0.3.0` inherits the portable core's pre-source Gate 0A, unchanged
schema-8 lineage vocabulary, one-decision interaction contract, verified
production handoff before HITL 3, terminal `complete_dormant` lifecycle, and
one-time informational trigger guidance. Claude Code's documented
`AskUserQuestion` contract accepts two to four explicit options; this adapter
requires the documented additional `Other` free-text path. Use that card only
when it contains the complete mutually
exclusive option set. If the control is unavailable or unsupported, or the
complete set has more than four options, use the portable ordinary-chat
fallback with every valid numbered option plus `Other - type your answer`.
Never prune, hide or combine choices to fit a card. Long dependency
chunks also keep every valid option visible. The Claude wrappers add no
independent gate, state, automation, permission, or schedule behavior.

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
