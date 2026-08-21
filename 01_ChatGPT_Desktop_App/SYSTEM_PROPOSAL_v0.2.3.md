# Inactive system candidate proposal

- Proposal ID: `ACR-SYS-20260821-005`
- Proposal version: `0.2.3`
- Status: system-file candidate approved; implementation and validation are authorised, but commit, publication, installation, activation and scheduling remain separate
- Base: published `v0.2.2`

## Approved scope

The approved target classes are the canonical shared workflow in
`03_Shared_Workflow_Core/**`; ChatGPT/Codex plugin, public-source mirror and
supporting records in `01_ChatGPT_Desktop_App/**`; platform adapters in
`02_Other_Agentic_Systems/**`; current cross-platform guidance in
`04_Documentation/**`; and repository and release checks in
`05_Validation/**`. The candidate retains exactly six bundled skills and a
single umbrella entry routed to the orchestrator.

The mandatory completed-run review covers workflow skills and umbrella entry
routing; plugin or platform adapter; AGENTS.md and agent configurations;
project template, state schema and migration; validators, tests and QA;
documentation; memory or other workflow-owned durable instruction stores;
schedule contracts; permissions, tools, external egress and automatic
behaviour; and compatibility, benefits, regressions, risks, residual risks and
rollback.

## Approved inactive changes

1. Keep the reusable system course-independent. Each fresh run adapts to the
   supplied subject or discipline, educational level, programme or
   qualification, language, learners, objectives, assessment, delivery mode,
   accessibility needs and lecturer-confirmed constraints.
2. Add pre-source Gate 0A. Before requesting, disclosing, listing, reading,
   copying or hashing any course-source path, record the material category,
   sensitivity classification, assessment-security classification and handling
   authority, and exact processing-environment category only. Public
   availability alone is insufficient.
3. Permit personal or unmanaged processing only for privately owned or
   rightsholder-authorised material, or appropriately licensed/public material
   with explicit AI-processing authority, no student personal data, and an
   explicit assessment-security decision. Route institution-internal,
   restricted, student-personal or protected-assessment material without
   source/path leakage unless the exact approved institutional environment and
   handling scope permit it; fail closed for mixed or uncertain material or
   sensitivity/security classifications. An approved institutional exact
   environment requires a reference, policy, approved scope and non-expired
   expiry.
4. Move new templates to schema 8. Bind the material-processing eligibility
   fingerprint into source policy, run lineage and schedule validation. Bundle
   the preview-only `scripts/migrate_state_v7_to_v8.py`; automatic application
   is forbidden. Preserve valid terminal schema-7 history immutably with
   indexed canonical SHA-256 receipts; reject nonterminal or malformed legacy
   history rather than rewriting it. Reconfirm every schedule before a future
   trigger.
5. After verified production handoff and HITL 3 acceptance, require one explicit
   requested-or-declined response to the complete system-improvement question.
   Silence waits without deciding. The response closes the course run as
   terminal `complete_dormant`, clears `active_run_id`, and the closed run can
   never resume. Any requested system work is separate.
6. After closeout, persist one informational offer explaining a manual fresh
   trigger and optional staged schedule guidance. Never register or trigger
   automation. Every future trigger creates a fresh run and lineage.
7. Preserve `candidate_not_active`, `schedules=[]`, and no MCP/app/hook/auth/permission/schedule payload.

The repository marketplace retains its pre-existing `policy.authentication:
ON_INSTALL` host installation-policy metadata. This is not a bundled
authentication provider, credential, account integration or runtime auth
capability; v0.2.3 adds none of those surfaces.

## Validation and residual risk

Success requires canonical/adapter drift checks, schema validation, the six
skill checks, plugin unit and forward tests, public scrub, public-submission
validation, byte-identical custom/public runtime trees, and migration
non-mutation tests. Residual risks are intake friction, conservative blocking,
schema compatibility and provider-policy drift. Rollback restores the published
v0.2.2 source without rewriting its tag, release evidence or course history.

`APPROVE SYSTEM FILES` authorised only this candidate scope. It did not
authorise commit, publication, installation, activation, schedule registration,
an immediate course run, added tools, permissions, authentication or egress.
