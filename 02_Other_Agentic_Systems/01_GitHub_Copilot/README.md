# GitHub Copilot adapter

Adapter release: `0.2.3`. Shared semantic base: inactive candidate
`ACR-SYS-20260821-005` version `0.2.3`.

This project-local overlay adds GitHub Copilot repository instructions and ten
custom-agent profiles to the portable core. It contains no installer, GitHub
App access, API calls, workflow, MCP server, secret, or plugin.

Release `0.2.3` inherits the portable core's pre-source Gate 0A, schema-8
lineage vocabulary, verified production handoff before HITL 3, terminal
`complete_dormant` lifecycle, and one-time informational trigger guidance. The
thin GitHub files add no independent gate, state, automation, permission, or
schedule behavior.

Compose `../00_Portable_Core_Adapter/overlay/` first, then this `overlay/`,
relative to the same reviewed project root:

```text
<project-root>/
├── AGENTS.md                                  # portable core
├── .claude/skills/course-redesign/            # portable core
└── .github/
    ├── copilot-instructions.md
    ├── instructions/
    │   └── course-redesign.instructions.md
    └── agents/
        └── <ten read-only role>.agent.md
```

The repository-wide and path-specific files are thin bridges to the shared
skill. Each custom agent enables only the documented `read` and `search` tool
aliases and sets `disable-model-invocation: true`, so it must be deliberately
selected rather than inferred automatically by Copilot cloud agent.

Review collisions manually and commit the chosen project-local files only if
the repository owner wants to share them. Copying the files does not turn on
Copilot, start a task, approve network use, or activate the course-redesign
runtime.

Official references:

- [Repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [Custom-instructions support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Agent Skills in repositories](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

Availability and precedence differ across GitHub.com, Copilot CLI, and IDE
surfaces; consult the current support matrix before relying on a feature.
