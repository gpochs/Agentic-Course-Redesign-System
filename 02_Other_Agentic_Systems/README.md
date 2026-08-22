# Other agentic systems

This area contains an inert native GitHub Copilot plugin package plus
project-local adapters for systems that do not use the OpenAI plugin package.
They implement the same course-independent workflow for different subjects,
educational levels, learner groups, assessment contexts, and material formats.
Each run adapts to the lecturer-supplied course while preserving the same
eligibility, lineage, lecturer-gate, and course-isolation controls. Each host
discovers instructions, skills, and specialist profiles from different paths.

## Choose exactly one platform route

1. For the GitHub Copilot app or CLI, use the native plugin route in
   `01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md`. The project-local overlay
   remains an advanced/manual alternative.
2. For Claude Code, OpenCode, Antigravity, or the manual Copilot route, start
   with `00_Portable_Core_Adapter/overlay/`, then add exactly one matching
   platform overlay.
3. Copy into one isolated course workspace only after reviewing every target.
4. Treat every collision as a manual decision; never overwrite an existing
   instruction or configuration automatically.
5. Open the resulting course folder in the selected host and verify discovery,
   permissions and read-only behavior before Gate 0A. Do not enumerate or read
   course sources until the pre-source processing-eligibility record passes.

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
