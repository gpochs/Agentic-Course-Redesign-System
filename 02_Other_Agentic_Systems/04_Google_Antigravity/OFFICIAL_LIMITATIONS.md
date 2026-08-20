# Official Antigravity limitations and non-claims

Checked against Google documentation on 2026-08-20. This adapter was built and
validated as files only; Antigravity was not opened, installed, accessed, or
signed into.

## Confirmed IDE conventions used

- Workspace rules are Markdown files under `.agents/rules/`; Google documents
  Manual, Always On, Model Decision, and Glob activation modes, `@` references,
  and a 12,000-character rule-file limit:
  <https://antigravity.google/docs/ide/rules>
- Agent Skills use `.agents/skills/<skill>/SKILL.md` with a required
  `description` and optional supporting scripts/resources:
  <https://antigravity.google/docs/skills>
- Workflows are Markdown, invoked as `/workflow-name`, can call other workflows,
  and have a 12,000-character file limit:
  <https://antigravity.google/docs/ide/workflows>
- Project-local custom subagents are Markdown files under
  `.agents/agents/<name>.md` or `.agents/agents/<name>/agent.md`. Their YAML
  frontmatter can constrain tools, primary-agent selection, subagent invocation,
  model inheritance, command execution, skills, MCP servers, and plugins:
  <https://antigravity.google/docs/subagents>
- The official IDE changelog records support for reading rules from `AGENTS.md`
  in addition to `GEMINI.md`:
  <https://www.antigravity.google/changelog>

## Deliberate non-claims

- Google's rules page does not publish a stable file schema for rule activation
  metadata. These files do not claim to set or verify an IDE-side activation
  mode; inspect the Customizations UI on the actual installed build.
- Skills and workflows are model instructions, not a deterministic workflow
  engine. The file validators can prove layout and fail-closed static controls,
  not model compliance or runtime behaviour.
- The current IDE overview maps the editor to a single workspace. Antigravity
  2.0 separately documents multi-folder Projects and scoped settings; no
  repository-committed IDE project manifest is claimed here:
  <https://antigravity.google/docs/ide/overview> and
  <https://antigravity.google/docs/projects>
- This adapter does not modify Strict/Request Review mode, sandboxing,
  non-workspace access, browser allowlists, permissions, telemetry, global
  rules, or global customizations. Configure and verify those in the IDE.
  Google's settings documentation describes Always Proceed as high risk and
  Strict mode as enforcing review and workspace isolation:
  <https://antigravity.google/docs/ide/settings>
- Current IDE plugin documentation supports skills, rules, MCP configuration,
  and hooks in a plugin but does not list workflows as plugin components. This
  adapter therefore is not packaged as a plugin:
  <https://antigravity.google/docs/ide/plugins>
- Hooks can execute commands and MCP configurations can expose local processes
  or remote services. No active hook, MCP server, or plugin is present under the
  overlay. Disabled examples remain outside it:
  <https://antigravity.google/docs/ide/hooks> and
  <https://antigravity.google/docs/ide/mcp>
- The ten project-local custom subagents use the documented Markdown format,
  set `mainAgent: false` and `subagent: true`, inherit the selected model, allow
  only `view_file` and `grep_search`, set command execution to `off`, disable MCP
  inheritance, and declare no MCP server or plugin dependency. Their prompts
  additionally forbid writes, execution, browsing, network egress, publication,
  and state persistence.
- Frontmatter and prompts are fail-closed configuration, not proof that a
  particular installed build discovers or obeys an agent. Antigravity also
  documents that subagents inherit parent safety scopes and may surface approval
  requests. Verify discovery, the displayed tool list, Request Review or Strict
  mode, sandboxing, workspace scope, and browser restrictions in the installed
  build before any protected-file analysis. This adapter was not runtime-tested.
- The source candidate's state field `plugin_id: agentic-course-redesign` is
  preserved as workflow provenance. It does not mean an Antigravity plugin is
  installed or active.
