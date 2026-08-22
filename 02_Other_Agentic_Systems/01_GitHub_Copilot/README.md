# GitHub Copilot adapter

Adapter semantic release: `0.2.3`. Native Copilot package:
`0.2.3-copilot.1`. Candidate proposal: `ACR-SYS-20260822-006`.

This adapter now provides two ways to use Agentic Course Redesign with GitHub
Copilot:

1. **Native plugin — recommended for participants.** Register this repository
   as a Copilot plugin marketplace, then install
   `agentic-course-redesign@agentic-course-redesign-system`.
2. **Project-local overlay — advanced/manual alternative.** Copy the portable
   core overlay and this adapter's `overlay/` into one reviewed course
   project.

Both routes preserve the same v0.2.3 workflow semantics: pre-source Gate 0A,
schema-8 lineage, lecturer-controlled gates, verified production handoff before
HITL 3, terminal `complete_dormant` lifecycle, and a separate system-review
decision. Neither route starts a course run merely because files are installed.

## Native plugin

The self-contained package is:

```text
plugin/agentic-course-redesign/
├── plugin.json
├── skills/                         # six canonical workflow skills
├── agents/                         # ten full read-only specialist roles
├── scripts/                        # preview/validation helpers
├── assets/project-template/        # inactive Copilot-aware scaffold
├── PARTICIPANT_QUICK_START.md
└── LICENSE
```

The repository marketplace manifest is
`/.github/plugin/marketplace.json`. See
[PARTICIPANT_INSTALLATION.md](PARTICIPANT_INSTALLATION.md) for clickable app
links, command-line alternatives, verification, the first project-session
prompt, and removal instructions.

The native package mirrors the six canonical v0.2.3 skills and helpers
byte-for-byte. Its ten Copilot agents preserve the full specialist role
contracts from the published Codex package while translating only the host
manifest and read-only tool declaration.

It declares no MCP server, connector, API integration, authentication, hook,
LSP server, telemetry, schedule, automation, model provider, or additional
permission. It is provided as-is without a support SLA.

## Project-local overlay

For a manual repository configuration, compose
`../00_Portable_Core_Adapter/overlay/` first, then this `overlay/`, relative
to the same reviewed project root:

```text
<project-root>/
├── AGENTS.md
├── .claude/skills/course-redesign/
└── .github/
    ├── copilot-instructions.md
    ├── instructions/
    │   └── course-redesign.instructions.md
    └── agents/
        └── <ten read-only role>.agent.md
```

Review every collision manually. Copying these files does not turn on Copilot,
start a task, approve network use, or activate the course-redesign runtime.

## Validation

Run the native package and mutation checks from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python 02_Other_Agentic_Systems/01_GitHub_Copilot/validation/validate_native_plugin.py
python -m unittest discover -s 02_Other_Agentic_Systems/01_GitHub_Copilot/validation -p "test_*.py" -v
```

For a local host-discovery check, point the Copilot CLI at
`plugin/agentic-course-redesign/` with `--plugin-dir` and run
`plugin list`. This verifies manifest loading without installing into the
participant's live configuration or consuming a model turn. Copilot's plugin
list does not enumerate every custom agent, so agent count, tool ceilings, and
source fidelity are enforced separately by the static validator and mutation
tests.

## Official references

- [About Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [Creating a Copilot plugin](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)
- [Creating a plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
- [Finding and installing plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)
- [GitHub Copilot app customization](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app)
- [Custom-agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

Availability and organization policy can differ across the Copilot app, CLI,
GitHub.com, and IDE surfaces. Static repository validation is not proof that an
organization has enabled third-party plugins.
