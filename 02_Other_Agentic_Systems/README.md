# Other agentic systems

These are inert, project-local adapters for systems that do not use the OpenAI
plugin package. They share the same lecturer gates and course-isolation model,
but each host discovers instructions, skills and specialist profiles from
different root-relative paths.

## Choose exactly one platform overlay

1. Start with `00_Portable_Core_Adapter/overlay/`.
2. Add one matching platform overlay:
   - `01_GitHub_Copilot/`
   - `02_Claude_Code/`
   - `03_OpenCode/`
   - `04_Google_Antigravity/`
3. Copy into one isolated course workspace only after reviewing every target.
4. Treat every collision as a manual decision; never overwrite an existing
   instruction or configuration automatically.
5. Open the resulting course folder in the selected host and verify discovery,
   permissions and read-only behavior before Gate 0.

The adapters do not install applications, choose paid models, sign in, enable
MCP servers or hooks, grant shell access, register schedules or expose course
files. Use the strongest model available and authorised in the lecturer's own
account, but do not hard-code a model ID in a portable repository.

## Adapter roles

- **Portable core:** shared `AGENTS.md`, one portable Agent Skill and workflow
  references used by Copilot, Claude Code and OpenCode.
- **GitHub Copilot:** Copilot instructions, path instructions and ten native
  read/search-only agent profiles.
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

