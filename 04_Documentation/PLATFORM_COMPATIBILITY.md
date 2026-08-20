# Platform compatibility

The workflow is shared; discovery paths, agent profiles and plugin formats are
not. Each adapter is therefore a thin project overlay with an explicit support
boundary.

| Platform | Shared instructions | Skills | Native adapter | Important limit |
|---|---|---|---|---|
| ChatGPT Desktop / Work / Codex | Plugin skills plus project `AGENTS.md` | OpenAI skills-only plugin | `01_ChatGPT_Desktop_App/` | User-level installation works only on supported Work/Codex surfaces and may be restricted by app version, account or workspace policy. The Codex IDE extension does not support plugins; universal listing requires separate OpenAI review and publication. |
| GitHub Copilot | `AGENTS.md` and Copilot instructions | Agent Skills | `01_GitHub_Copilot/` | Feature support differs by GitHub.com, CLI and IDE surface. |
| Claude Code | `CLAUDE.md` imports `AGENTS.md` | `.claude/skills/` | `02_Claude_Code/` | Claude Code does not automatically read `AGENTS.md`. |
| OpenCode V2 | `AGENTS.md` | `.opencode/skills/` or compatible Agent Skills | `03_OpenCode/` | Its executable plugin API is beta; the safe adapter need not enable one. |
| Google Antigravity | `AGENTS.md` plus `.agents/rules/` | `.agents/skills/` | `04_Google_Antigravity/` | Rules/workflows need native paths; hooks, MCP and plugins remain optional and disabled. |

Adapter files stored inside this repository are templates. They become active
only after an attendee deliberately copies the matching overlay into the root
of one course workspace or installs the documented plugin. Do not open the
repository root as if all platform adapters should activate together.

No adapter commits a fixed model ID, account entitlement, credential, MCP
server, hook, external connector or schedule. Users may select the strongest
available model in their own account, but model selection is a user/platform
setting rather than a portable repository guarantee.
