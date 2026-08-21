# Repository validation report — v0.2.3 release source

- Proposal: `ACR-SYS-20260821-005`
- Release version: `0.2.3`
- Result: **PASS — validated repository release source**
- Base and rollback source: published `v0.2.2`

## Scope and boundary

The approved shared core, six-skill ChatGPT/Codex package, public runtime
mirror, five platform adapters, schema-8 state and preview-only migration,
documentation, manifests, validators and release controls were reviewed as one
candidate. No course-material path was changed. No real course material,
student data, answer key, credential, local absolute path or enabled runtime
state is included in the repository.

Exactly six skills remain available and the umbrella entry routes first to the
orchestrator and pre-source Gate 0A. The public package contains no registered
schedule and remains `candidate_not_active` with `schedules=[]`.

## Decisive validation evidence

| Check | Result |
|---|---|
| Repository unit suite | PASS: 79/79 tests |
| Independent adversarial reproductions | PASS: 27/27 previously failing boundary cases now fail closed or validate their preserved history correctly |
| Canonical schema-8 state | PASS: validator returned `ok=true` with no errors |
| Canonical mirrors | PASS: shared state and scripts match the ChatGPT public/custom and Antigravity runtime mirrors |
| Portable adapters | PASS: four release adapters, 49 frozen files, 39 overlays and 30 role wrappers; manifest hashes match |
| Google Antigravity | PASS: static validator; 17/17 tests; 12 canonical and 57 generated hashes; zero secret findings |
| Course adaptation | PASS: synthetic school, vocational, professional, higher-education and lecturer-defined profiles |
| Migration | PASS: preview-only v7-to-v8; immutable terminal-run and inactive-schedule receipts; malformed, active or unsupported history fails closed; no source write path |
| Gate and lifecycle sequencing | PASS: Gate 0A, source controls, Gates 0–3, artefact gates, production, handoff, HITL3, explicit review response and `complete_dormant` are ordered and current-lineage bound |
| Schedule safety | PASS: fresh trigger/run/contract lineage, immutable trigger-time receipt, time-window/expiry validation and no-immediate-run controls |
| Repository drift and formatting | PASS: repository validator and `git diff --check` |

The ChatGPT/Codex package-specific forward, public-submission, scrub, static
format, mirror and official-validator results are also recorded in
`01_ChatGPT_Desktop_App/VALIDATION_REPORT.md`.

## Capability and permission audit

No MCP server, app, connector, hook, authentication, permission, schedule or
external-egress capability was added to the runtime plugin. More precisely,
the package adds no plugin/provider authentication payload, credential flow or
authentication provider. The unchanged marketplace
`policy.authentication: ON_INSTALL` value is host installation-policy metadata,
not a runtime authentication capability.

The public package contains no registered schedule. Its informational
automation guidance cannot register or execute a task; any host-local schedule
requires a separate user decision and remains outside the repository package.

## Residual risks and rollback

Residual risks remain intake friction, conservative blocking, schema
compatibility and provider-policy drift. Rollback restores the published
`v0.2.2` source and validation evidence, preserves course and schedule history,
and does not move or rewrite the v0.2.2 tag or release.

This report validates source only. Commit, publication, installation and
activation remain separately controlled actions.
