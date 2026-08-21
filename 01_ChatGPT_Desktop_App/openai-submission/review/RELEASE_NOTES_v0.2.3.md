# Agentic Course Redesign 0.2.3

This repository release preserves the published v0.2.2 tag and assets as its
rollback source. Its reusable runtime template remains inactive by default;
publication alone does not start a course run or register a schedule.

## Release changes

- Adds pre-source Gate 0A. No course/context path, filename, listing, content,
  copy or hash may be requested or accessed before the material and exact
  processing environment are eligible. The category-only record also captures
  sensitivity, student-data and protected-assessment/answer-key handling.
- Allows privately owned/rightsholder-authorised and appropriately licensed or
  public material only when AI-processing authority is explicit. Public
  availability alone is insufficient.
- Routes institution-internal or restricted material out of personal/unmanaged
  Codex without revealing source content or paths. An institution-approved
  environment must carry an exact reference, scope, policy reference and expiry.
- Keeps mixed or uncertain material fail-closed until segregation or
  clarification.
- Adapts the same six-skill workflow to lecturer-supplied school, vocational,
  professional-learning, higher-education or other contexts without assuming a
  subject, level, qualification, language, assessment model or delivery mode.
- Moves new projects to schema 8 and adds a preview-only v7-to-v8 migration;
  the helper never writes the source state. Valid terminal v0.2.2 run history
  is indexed with immutable canonical receipts, while nonterminal or malformed
  history fails closed rather than being upgraded in place.
- Binds Gate 0A's eligibility fingerprint into run lineage and any later
  schedule contract or trigger.
- Makes an explicit requested/declined post-HITL-3 system-review response close
  the course run as terminal `complete_dormant`; silence waits and never decides.
- Persists one informational post-closeout offer explaining a fresh manual
  trigger and staged optional schedule guidance. It never registers or triggers
  automation.

The release remains skills-only: exactly six skills, no MCP server, app,
connector, hook, authentication, additional permission, external egress or
registered schedule.
The custom marketplace's unchanged `policy.authentication: ON_INSTALL` value is
host install-policy metadata, not a bundled authentication provider or
credential capability.
