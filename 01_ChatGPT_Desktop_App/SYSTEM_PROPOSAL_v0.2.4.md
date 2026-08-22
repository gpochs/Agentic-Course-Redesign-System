# Inactive interaction-only maintenance candidate

- Proposal ID: `ACR-SYS-20260822-007`
- Proposal version: `0.2.4`
- Maintenance evidence: `ACR-MAINT-20260822-001`
- GitHub Copilot package: `0.2.4-copilot.1`
- Status: system-file candidate approved; implementation and validation are
  authorised, while commit, publication, upload, installation, activation and
  scheduling remain separate
- Base: published `v0.2.3`

## Whole-system target scope

This interaction-only candidate applies consistently to
`03_Shared_Workflow_Core/**`, `01_ChatGPT_Desktop_App/**`,
`02_Other_Agentic_Systems/**`, `04_Documentation/**`, and
`05_Validation/**`. Exactly six bundled skills remain available. The candidate
makes no course-material changes, keeps the template at `schedules=[]`, and
keeps publication, installation and activation separate from implementation
and validation.

## Legacy-run disclosure and exception boundary

Historical run `CR-20260820-002` remains accepted-with-corrections-verified
evidence, but it is not represented as satisfying the current-lineage
production declaration, Production Handoff, independent handoff verification,
system-review response, terminal closeout and `complete_dormant` prerequisites
introduced in v0.2.3. The explicit maintenance exception applies only to
interaction proposal `ACR-SYS-20260822-007`; future semantic or pedagogical
changes still require a genuine current-lineage complete-dormant course run.

Every complete future system review must cover workflow skills and umbrella
entry routing; plugin or platform adapter; AGENTS.md and agent configurations;
project template, state schema and migration; validators, tests and QA;
documentation; memory or other workflow-owned durable instruction stores;
schedule contracts; permissions, tools, external egress and automatic
behaviour; and compatibility, benefits, regressions, risks, residual risks and
rollback.

## Approved interaction-only changes

1. Ask one unresolved consequential question at a time through the
   orchestrator; specialists remain evidence lenses rather than extra user
   interfaces.
2. Use a native card only when the live host tool contract can present the
   complete option set plus a custom answer. The current verified Codex
   contract permits exactly two or three explicit options and adds free-form
   `Other`. Public OpenAI documentation does not currently document the widget
   cardinality, and Work's exact maximum is not independently documented or
   exposed here.
3. If card capacity is unknown, unavailable or exceeded, ask one ordinary chat
   question listing every valid numbered option plus
   `Other - type your answer`, then wait. Every valid option remains visible;
   never prune, hide or combine valid choices merely to fit a card.
4. Cluster very long decisions only by dependency when choices share evidence
   or constrain one another. Keep every valid option visible, explain the
   grouping and let the lecturer split, merge, reorder or rename it.
5. Preserve custom answers exactly, confirm their canonical interpretation,
   reflect consequences and show an editable recap at each cluster or gate end.
6. Leave blank or skipped required questions unresolved. Label at most the
   safest truthful, evidence-aligned, reversible option `Recommended`, never
   preselect it, mark factual choices `select only if true`, and fail closed on
   uncertainty.
7. Keep exact authority gates and tokens separate from the conversational
   choice interface.
8. Add a deterministic preview-first, exact-target, no-overwrite Gate-0A record
   generator callable through Python or PowerShell in affected GitHub Copilot
   BYOK environments, without a new plugin, tool, MCP server or permission.

For semantic validation, the contract is exact: use a native card only when the
live host tool contract can present the complete option set plus a custom
answer. In the current verified Codex contract this means exactly two or three
explicit choices plus client-added free-form `Other`; no fixed Work maximum is
claimed. If capacity is unknown, unavailable or exceeded, list every valid
numbered option plus `Other` in ordinary chat, then wait. Never prune, hide or
combine valid choices merely to fit a card; keep every valid option visible in
adaptive dependency-based clusters and let the lecturer split, merge, reorder
or rename the grouping; preserve a custom answer exactly. The bundled helper is
`scripts/create_material_processing_eligibility.py`. Publication, installation
and activation remain separate decisions.

The state schema remains 8 and all eligibility categories/outcomes,
substantive choices, course semantics, specialist authority, gate meanings,
approval tokens and lifecycle transitions remain unchanged.

## ChatGPT and OpenAI distribution state

The v0.2.4 ChatGPT/Codex runtime mirror and OpenAI skills-only source are
inactive candidate trees and must remain byte-identical where required. OpenAI
v0.2.3 is already published. The normal later update route is the existing
plugin's **Upload** action, which creates a new draft without first unpublishing
v0.2.3. No upload, publication, installation or activation is authorised by
this proposal record.

## Residual risk and success criteria

Residual risks are host card differences, visible Skip controls,
recommendation anchoring, question fatigue, dependency-cluster size,
resumed-task drift, package-cache drift and unresolved upstream Copilot BYOK
tool compatibility. Success requires six-skill parity, runtime/public mirror
parity, complete interaction-contract tests, deterministic helper
preview/apply/overwrite/target checks, public scrub, package validation and no
new integration or automation surface.
