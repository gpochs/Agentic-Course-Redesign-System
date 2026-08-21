# Reusable-system patch proposal

- Proposal ID: `ACR-SYS-20260820-004`
- Proposal version: `0.2.2`
- Status: system-file candidate approved; repository publication separately
  authorised; runtime not installed, activated, or scheduled by that publication
- Base: published `v0.2.1`
- Approved system scope: shared core; ChatGPT/Codex custom and public-source
  trees; every portable/platform adapter; state schemas and migrations;
  validators and tests; current documentation; manifests, hashes, provenance,
  versioning, proposal and rollback records

## Exact target classes

- canonical semantics and template: `03_Shared_Workflow_Core/**`;
- ChatGPT/Codex implementation and public-submission mirror:
  `01_ChatGPT_Desktop_App/**`;
- portable core, GitHub Copilot, Claude Code, OpenCode and Antigravity adapters:
  `02_Other_Agentic_Systems/**`;
- current cross-platform documentation: `04_Documentation/**`;
- repository, release-evidence and adapter validation: `05_Validation/**`;
- repository-level version/provenance controls, including `.gitattributes`,
  `README.md`, `CHANGELOG.md`, and generated manifest/hash records explicitly
  named by the approved build process.

Canonical workflow semantics originate in `03_Shared_Workflow_Core/**`.
Platform trees are derived mirrors or thin inheritance bridges and may add only
platform-specific packaging or capability declarations; they may not weaken a
gate or invent activation/schedule authority.

## Problem demonstrated by the completed run

The v0.2.1 workflow described artefact production and HITL 3, but the explicit
production-completion declaration, separate Production Handoff approval,
independent handoff verification, HITL 3 final-acceptance receipt, and final
system-review offer were not all represented as one validated, resumable state
chain. A later task could therefore infer a completed checkpoint from prose or
repeat/skip the final offer.

## Approved inactive change

1. Preserve **Agentic Course Redesign** as the Gate-0-aware umbrella and keep
   exactly six bundled skills.
2. Require a valid current-lineage `DECLARE PRODUCTION COMPLETE` reply, then a
   separate reply repeating the exact handoff target with `APPROVE PRODUCTION
   HANDOFF`, then independent verification of the saved handoff before HITL 3.
3. Record current-lineage HITL 3 decisions and final acceptance.
4. After final acceptance, durably record and ask exactly once: `Would you like
   a separate, read-only system-improvement review covering the workflow skills
   and umbrella entry routing; plugin or platform adapter; AGENTS.md and agent
   configurations; project template, state schema and migration; validators,
   tests and QA; documentation; memory or other workflow-owned durable
   instruction stores; schedule contracts; permissions, tools, external egress
   and automatic behaviour; and compatibility, benefits, regressions, risks,
   residual risks and rollback, followed only by a versioned proposal? A yes
   authorises only that review and proposal; it does not authorise system-file
   changes, installation, publication or release, runtime activation, schedule
   registration or modification, an immediate run, or any added MCP server,
   connector, authentication, permission or external egress.`
5. Treat a separate affirmative answer as authority for read-only system/run
   review and one versioned proposal only. It grants no file change,
   installation, publication, activation, schedule registration, immediate
   run, MCP server, connector, authentication, permission, or egress change.
6. Move the template to state schema 7, add fail-closed resume receipts, and add
   a preview-only `scripts/migrate_state_v6_to_v7.py`. The helper has no apply
   or write path and preserves existing status, schedules, lineage, source
   policy, and tool permissions.
7. Reconcile the portable core and every explicit platform adapter with those
   semantics without making a candidate active or registering automation.
8. Add validator, regression, forward, reviewer-case, adapter-inheritance and
   documentation checks for the new sequence while keeping generated mirrors
   consistent and the ChatGPT custom/public runtime trees byte-identical.

The System Gate token `APPROVE SYSTEM FILES` still authorises only the exact
validated proposal targets. It does not install, publish, activate, register a
schedule, or run anything. Schedule registration remains possible only for a
separately active matching runtime after a no-write simulation and the exact
three-line `APPROVE SCHEDULES` reply.

## Migration and compatibility

New projects use schema 7. Existing schema-6 state is never edited by the
bundled migration helper: it emits a proposed schema-7 document and validation
report to standard output for review. Applying any migration requires a later
explicit exact-target file decision outside this candidate implementation.
Unknown, partially migrated, active-with-unexpected-schedules, or invalid state
fails closed.

## Validation and success criteria

- manifests and all JSON, TOML, YAML, Python and SVG sources parse;
- SVG sources use LF line endings;
- canonical shared semantics and all platform adapters pass drift/inheritance
  validation, and custom/public runtime trees are byte-identical;
- exactly six skills remain and no MCP/app/hook/auth/permission/schedule payload
  is introduced;
- the untouched schema-7 template validates inactive with `schedules=[]`;
- premature HITL 3 and system review fail validation;
- a complete current-lineage closeout sequence validates;
- the v6-to-v7 preview leaves its source bytes unchanged and its proposal
  validates;
- disposable setup, manifest tamper detection, public scrub, public-submission
  checks and forward tests pass.

## Legacy release-evidence limitation

The published v0.2.1 release remains the compatibility base, not evidence for
this candidate. Its attached `system-release-validation-v0.2.1.json` names and
hashes the earlier v0.2.0 system archive rather than the v0.2.1 archive, and the
live GitHub release reports `immutable=false`. Those historical assets are not
modified. A new read-only evidence guard must reject a report whose internal
archive name, version, byte count, or SHA-256 does not match the archive being
validated. A disposable deterministic validation build is not a release. No
The System Gate approval alone made no v0.2.2 release claim. Repository
publication was separately authorised and must use matching exact-version
validation evidence; installation and live picker verification remain separate.

## Risks and rollback

Schema-7 consumers must understand the new durable records; schema-6 consumers
must not be pointed at a migrated proposal as if it were applied. Over-strict
lineage checks may pause a legitimate legacy run, which is safer than silently
crossing a gate. The rollback procedure covers every approved target class and
is in `ROLLBACK_v0.2.2.md`.
