# Other agentic systems

This area contains an inert native GitHub Copilot plugin package plus
project-local adapters for systems that do not use the OpenAI plugin package.
They implement the same course-independent workflow for different subjects,
educational levels, learner groups, assessment contexts, and material formats.
Each run adapts to the lecturer-supplied course while preserving the same
eligibility, lineage, lecturer-gate, and course-isolation controls. Each host
discovers instructions, skills, and specialist profiles from different paths.

## Choose a platform

The native editions support the same course-independent human decisions. Choose **Skip for now** to begin a full redesign from a description, with no existing course materials. New editable drafts can be produced and reviewed through the existing approval stages. Open a live LMS, document, spreadsheet, presentation, quiz, or web app only when the lecturer chooses it and the host provides access.

| Host | Install and start |
| --- | --- |
| GitHub Copilot | [Native marketplace package or per-project installation](01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md) |
| Claude Code | [Global and project plugins](02_Claude_Code/README.md) |
| OpenCode | [Global and project skills and agents](03_OpenCode/README.md) |
| Google Antigravity | [Global and project plugins](04_Google_Antigravity/README.md) |

Each package uses the model and reasoning level selected in the existing account. No model API key is required. Local permissions, tool availability and subscriptions determine whether an artifact can be edited live. For a host without native browsing, use approved local materials or an export.

The adapters do not install applications, choose paid models, sign in, enable
MCP servers or hooks, grant shell access, register schedules or expose course
files. Use the strongest model available and authorised in the lecturer's own
account, but do not hard-code a model ID in a portable repository.

Gate 0A fails closed before source discovery. In a personal or unmanaged
environment, privately owned or rightsholder-authorised material may proceed;
appropriately licensed or public material may proceed only when the licence or
other authority explicitly permits the intended AI processing. Public
availability by itself is insufficient. Institution-internal or restricted
material is route-only unless an exact institution-approved environment
reference, scope, and expiry have been recorded; do not expose its source path,
filename, or content while routing. Mixed or uncertain collections remain
blocked.

## Adapter roles

- **Portable core:** shared `AGENTS.md`, one portable Agent Skill and workflow
  references used by Copilot, Claude Code and OpenCode.
- **GitHub Copilot:** native repository-marketplace plugin with six skills and
  ten read/search-only agent profiles; project overlay retained as an advanced
  alternative.
- **Claude Code:** `CLAUDE.md` bridge, scoped rules and ten read-only subagents.
- **OpenCode:** V2 agent wrappers with ordered deny-by-default permissions; no
  beta executable plugin.
- **Antigravity:** its own complete workspace overlay because native rules and
  slash workflows require `.agents/`; hooks, MCP and plugins remain outside
  auto-discovery and disabled.

Run the validator from this directory:

```text
python 00_Portable_Core_Adapter/validation/validate_adapters.py
```

Antigravity has additional validation commands in its own README. Static
validation proves layout and fail-closed defaults, not runtime behavior in an
unopened host application.
