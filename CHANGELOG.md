# Changelog

## 0.2.3 - 2026-08-21

- Adds Gate 0A before any source-path disclosure or access, with fail-closed
  routing by ownership/licence, explicit AI-processing authority, sensitivity,
  assessment security, provider and institution-approved environment.
- Clarifies that publicly available material is not automatically authorised;
  personal or unmanaged processing is limited to privately owned,
  rightsholder-authorised or appropriately licensed/public material with the
  required processing authority.
- Makes a successfully accepted course run terminal only after the lecturer
  explicitly accepts or declines the post-HITL3 system-improvement review.
  Silence remains a wait state; a closed run becomes `complete_dormant` and
  cannot be resumed.
- Adds one post-closeout trigger-guidance offer. Manual triggering remains
  available; any automation requires an exact course, timezone, recurrence,
  non-null expiry, simulation and separate approval. A trigger always creates
  a fresh run and never grants standing production authority.
- Adds schema-8 state, preview-only schema-7-to-schema-8 migration, eligibility
  fingerprints bound to run and schedule lineage, and cross-adapter regression
  tests across synthetic course levels and disciplines.
- Keeps the public package course-independent, inactive and free of real course
  data, credentials, connectors, MCP servers, plugin/provider authentication
  payloads, permissions, hooks and registered schedules. The unchanged
  marketplace `policy.authentication: ON_INSTALL` value is host installation-
  policy metadata, not a bundled authentication provider.

## 0.2.2 - 2026-08-21

- Makes Gate 0 routing and the complete gate order explicit across the shared
  core, ChatGPT plugin and all project-local adapters.
- Requires current-lineage `DECLARE PRODUCTION COMPLETE`, a separate matching
  `APPROVE PRODUCTION HANDOFF`, and independent handoff verification before
  HITL 3.
- Requires a post-HITL3 offer of a separate read-only system-improvement
  review covering skills and umbrella routing; plugin/adapter; `AGENTS.md` and
  agent configurations; project template/state schema/migration;
  validators/tests/QA; documentation; workflow-owned durable instructions;
  schedule contracts; permissions/tools/egress/automatic behaviour; and
  compatibility/benefit/regression/risk/residual-risk/rollback, with explicit
  proposal-only authority.
- Adds durable schema-7 HITL3/review-offer state, preview-only schema-6 to
  schema-7 migration, and fail-closed regression tests for resumes and stale
  lineage.
- Strengthens archive/report version consistency and cross-platform SVG hash
  stability; documents the historical v0.2.1 validation-asset mismatch
  without moving or rewriting the v0.2.1 tag or release.
- Publishes the validated repository source and matching release evidence while
  keeping the runtime inactive by default. No course materials, connector, MCP
  server, plugin/provider authentication capability, permission, installation,
  activation or schedule is added by publication.

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
