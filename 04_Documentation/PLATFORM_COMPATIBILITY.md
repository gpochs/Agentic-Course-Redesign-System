# Platform compatibility

The workflow is shared; discovery paths, agent profiles and plugin formats are
not. Each distribution is therefore a thin platform package or project overlay
with an explicit support boundary.

| Platform | Shared instructions | Skills | Native adapter | Important limit |
|---|---|---|---|---|
| ChatGPT Desktop / Work / Codex | Plugin skills plus project `AGENTS.md` | OpenAI skills-only plugin | `01_ChatGPT_Desktop_App/` | In the current Codex host, `request_user_input` is available only in **Plan mode**, accepts **2–3 explicit choices**, and adds a free-text **Other** path automatically. Outside Plan mode it is unavailable, so the complete ordinary-chat fallback applies. The current public Work documentation does not state a card maximum, so Work must use the live host contract and fall back when capacity is unavailable or unknown. User-level installation may be restricted by app version, account or workspace policy. The Codex IDE extension does not support plugins. |
| GitHub Copilot | Plugin skills and agents; optional project `AGENTS.md` and Copilot instructions | Native Copilot plugin (recommended) or Agent Skills overlay | `01_GitHub_Copilot/` | The current app was observed presenting **at least five explicit choices plus a custom-answer row**; this is evidence of supported capacity, not a documented maximum. The adapter uses a native card only when the complete set fits the live host. Add this repository marketplace and install the native plugin, or deliberately use the advanced overlay. GitHub Copilot App/CLI 1.0.80 BYOK sessions were observed to reject replayed `apply_patch` history after a successful patch; the v0.2.4 package uses a function-style PowerShell/Python Gate-0A generator and documents a fresh-session fallback. No extra plugin or MCP server is required. |
| Claude Code | `CLAUDE.md` imports `AGENTS.md` | `.claude/skills/` | `02_Claude_Code/` | Claude Code's documented `AskUserQuestion` contract accepts **2–4 explicit options**; this adapter requires the documented additional **Other** free-text path. A complete set larger than four uses the ordinary-chat fallback. Claude Code does not automatically read `AGENTS.md`. |
| OpenCode V2 | `AGENTS.md` | `.opencode/skills/` or compatible Agent Skills | `03_OpenCode/` | OpenCode documents options plus a custom answer for its question tool but no maximum. Use the complete set only when accepted by the live host; otherwise use ordinary chat. Its executable plugin API is beta; the safe adapter need not enable one. |
| Google Antigravity | `AGENTS.md` plus `.agents/rules/` | `.agents/skills/` | `04_Google_Antigravity/` | Antigravity supports interactive questions, but its public documentation does not establish a maximum. Use the complete set only when accepted by the live host; otherwise use ordinary chat. Rules/workflows need native paths; hooks, MCP and plugins remain optional and disabled. |

Adapter files stored inside this repository are templates. They become active
only after an attendee deliberately copies the matching overlay into the root
of one course workspace or installs the documented plugin. Do not open the
repository root as if all platform adapters should activate together.

No adapter commits a fixed model ID, account entitlement, credential, MCP
server, hook, external connector or schedule. Users may select the strongest
available model in their own account, but model selection is a user/platform
setting rather than a portable repository guarantee.

All adapters preserve the same interaction semantics even when their widgets
differ: one unresolved consequential question at a time, complete choices,
no pruning/hiding/combining to fit cards, every valid option visible in
dependency-based lecturer-editable clusters, verbatim custom answers, editable
recaps, and exact authority gates kept separate from conversational choices.

Primary platform references: [Claude Code Agent SDK user input](https://platform.claude.com/docs/en/agent-sdk/user-input),
[GitHub Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference),
[OpenCode tools](https://opencode.ai/docs/tools/), and
[Google Antigravity interactive-question codelab](https://codelabs.developers.google.com/build-deploy-embed-agy-agents-cli).
Where a provider does not publish a maximum, this matrix records no invented
limit; the fail-safe ordinary-chat fallback remains authoritative.

Gate 0A is platform-independent. A consumer or personal account is not assumed
to be suitable for institution-internal material. Institution-provisioned AI,
institution-managed coding assistants and institution-approved self-hosted or
API deployments with appropriate contractual controls are conditional routing
examples only; their availability, cost, scope and policy approval must be
verified from current institutional and provider sources.
