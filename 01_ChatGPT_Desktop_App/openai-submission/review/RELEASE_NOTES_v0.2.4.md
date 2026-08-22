# Agentic Course Redesign 0.2.4

This interaction-only maintenance candidate preserves the published OpenAI and
GitHub v0.2.3 release as its operational rollback source. It does not change
eligibility outcomes, substantive option sets, course semantics, specialist
authority, gate order, approval tokens, state schema or lifecycle transitions.

## Candidate changes

- Keeps one unresolved consequential lecturer question in view at a time.
- Uses a native choice card only when the live host tool contract can present
  the complete option set plus a custom answer. The current verified Codex
  contract permits exactly two or three explicit options and adds free-form
  `Other`. Public OpenAI documentation does not currently document widget
  cardinality, and Work's exact maximum is not independently documented here.
- If capacity is unknown, unavailable or exceeded, uses one ordinary-chat
  question listing every valid numbered option plus `Other - type your answer`,
  then waits. It never prunes, hides or combines valid choices merely to fit a
  card.
- Groups very long decisions only by actual dependencies when choices share
  evidence or constrain one another, while keeping every valid option visible.
  The orchestrator explains the grouping and lets the lecturer split, merge,
  reorder or rename it.
- Preserves custom answers verbatim, confirms their canonical interpretation,
  reflects consequences and shows an editable recap before continuing.
- Permits at most the safest truthful, evidence-aligned, reversible option to
  be labelled `Recommended`; it is never preselected. Factual declarations say
  `select only if true`, and uncertainty fails closed.
- Bundles a deterministic, preview-first Gate-0A record generator that creates
  only the exact control target after explicit apply and refuses overwrite.
  This avoids a documented Copilot BYOK `apply_patch` history-serialization
  failure without adding a plugin, MCP server, permission or external service.

The candidate remains skills-only: exactly six skills, no MCP server, app,
connector, hook, provider authentication, telemetry, additional permission,
external egress, registered schedule or automatic course run.

## OpenAI update boundary

OpenAI v0.2.3 is already published. The existing plugin page exposes a
plugin-level **Upload** route, so v0.2.4 should later be uploaded as a new draft
under that plugin while v0.2.3 stays published. Do not delete or unpublish the
old version first. The current v0.2.4 source has not been uploaded, reviewed,
published, installed or activated.
