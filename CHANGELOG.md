# Changelog

## 0.3.0 — 2026-11-27

- Lecturers can skip material classification and complete a redesign from a course description. A specific protected source can be cleared later when it becomes relevant.
- All ten specialists connect their recommendations to course evidence, practical constraints and a change the lecturer can inspect. The orchestrator asks about missing materials and offers optional tools when they would improve the work.
- Local files, cloud documents and draft LMS activities can be reviewed through the available editor or browser. Each artefact returns to the lecturer for acceptance, revision or rejection.
- The five host editions share six skills and retain the existing Research, Plan and Implementation sequence and human decisions. Release checks cover scope boundaries, untrusted source instructions and the contents of distributable archives.

## 0.2.5 (inactive OpenAI/Codex candidate) - 2026-08-25

- Replaces Markdown-dependent public-description bullets with `◆` section and
  `•` item separators that remain legible when a client collapses line breaks.
- Preserves the v0.2.4 wording, workflow claims, ten specialist roles, gates,
  decision dialogue and boundary.
- Keeps all six skill trees byte-for-byte unchanged and leaves the shared core,
  course template, other adapters and GitHub Copilot `0.2.4-copilot.2`
  unchanged.
- Adds no course-material, schedule, MCP, connector, authentication, hook,
  telemetry, permission, external-egress, installation or activation change.
- Preserves published and installed OpenAI/Codex v0.2.4 until a separate
  exact-version publication and installation decision is approved and verified.

## 0.2.4-copilot.2 - 2026-08-22

- Adds a Copilot-only transport compatibility override for GitHub Copilot App
  and CLI 1.0.80 sessions that use an OpenAI-compatible BYOK provider such as
  CommandCode Chat Completions. The semantic workflow remains `0.2.4`.
- Forbids built-in `apply_patch` for every file mutation in an affected task,
  because Copilot can persist the completed call as `type=custom` and make the
  next provider request fail with `expected "function"`.
- Requires function-style PowerShell/Python or packaged helpers while
  preserving exact-target preview, existing approvals, expected-current-hash
  checks, atomic writes, reread and validation.
- Adds fresh-task, read-only recovery guidance and makes the existing Python 3
  prerequisite explicit. It adds no MCP server, connector, authentication,
  hook, telemetry, permission, schedule or publisher-operated service.
- Preserves `0.2.4-copilot.1` as the immediate rollback package and leaves the
  OpenAI/Codex plugin, shared workflow core and `v0.2.4` tag/release unchanged.

## 0.2.4 - 2026-08-22

- Adds one shared Lecturer Decision Dialogue Contract across every
  human-in-the-loop phase without changing gate order, substantive option sets,
  specialist authority, course semantics, schema 8 or lifecycle transitions.
- Keeps one unresolved consequential question in view. A native card is used
  only when the live host can show the complete mutually exclusive option set
  plus a custom-answer path. If the control is unavailable or unsupported, its
  capacity is unknown, or the complete set exceeds its capacity, the workflow
  shows every valid option as one numbered chat question plus Other. Valid
  choices are never pruned, hidden or combined merely to fit a card.
- Makes long decision clusters adaptive and dependency-based rather than fixed
  pedagogical silos. The lecturer may split, merge, rename, reorder or defer a
  cluster while every valid option remains visible, and receives an editable
  recap before continuation.
- Preserves custom answers verbatim, confirms their canonical interpretation,
  labels only the safest truthful evidence-aligned reversible option as
  recommended, never preselects it, and treats blank, skipped or uncertain
  required decisions as unresolved.
- Adds a deterministic preview-first/no-overwrite Gate-0A eligibility-record
  generator for local PowerShell/Python invocation. It addresses an observed
  GitHub Copilot BYOK `apply_patch` history-serialization defect without adding
  an MCP server, connector, hook, authentication, telemetry, permission or
  publisher-run service.
- Prepares matching `0.2.4` ChatGPT/OpenAI, portable, Claude Code, OpenCode and
  Antigravity sources and `0.2.4-copilot.1` GitHub Copilot package metadata as
  inactive candidates. Published OpenAI/Codex 0.2.3 and Copilot
  0.2.3-copilot.1 remain rollback versions until separately replaced.

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
