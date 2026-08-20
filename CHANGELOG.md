# Changelog

## 0.2.1 - 2026-08-20

- Enforces LF checkout rules for extensionless and text-template files so
  adapter manifest hashes validate identically on Windows and Unix.
- Updates the ChatGPT repository plugin to `0.2.1` and presents the existing
  orchestrator as **Agentic Course Redesign**, a single umbrella entry that
  routes protected setup, continuation, and the complete gated workflow.
- Keeps the six-skill architecture, inactive runtime state, permissions, data
  boundaries, HITL gates, and schedule boundary unchanged; no connector or MCP
  server is added.
- Keeps the shared workflow core and four project-local adapters at `0.2.0`;
  their contracts and workflow semantics did not change.
- Supersedes the repository-install guidance in `v0.2.0` without silently
  moving its published tag.

## 0.2.0 - 2026-08-20

- Preserves the validated ChatGPT/Codex 0.1.0 gated workflow.
- Adds a prepared skills-only OpenAI submission candidate; publisher metadata,
  submission, scans, review, approval and universal-directory publication
  remain pending.
- Publishes the public GitHub repository marketplace with verified release
  assets, inventories and checksums.
- Adds thin project adapters for GitHub Copilot, Claude Code, OpenCode and
  Google Antigravity.
- Introduces a shared workflow core and cross-adapter drift validation.
- Keeps plugins, hooks, MCP servers, schedules and external egress inactive by
  default.
- Adds public privacy, support, security and release documentation.

## 0.1.0

- Initial validated course-independent ChatGPT/Codex candidate with six skills,
  ten specialist role definitions, gated state, safe scaffold and portable
  setup validation.
