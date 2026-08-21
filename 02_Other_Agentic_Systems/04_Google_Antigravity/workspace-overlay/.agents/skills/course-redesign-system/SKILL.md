---
name: course-redesign-system
description: Review or validate a versioned improvement proposal for the inactive project-local course-redesign adapter only after a closed terminal course run and a recorded separate lecturer request.
---

# Course Redesign System

Course-material acceptance and system activation are separate decisions. Never update the live system merely because a course run succeeded.

## Required successful-run evidence

Before any system review, verify one closed terminal `complete_dormant`
current-lineage run with all of the
following durable records: valid production declaration; matching Production
Handoff approval; independently verified handoff; accepted HITL 3 (including
verification of any named conditional corrections); and a system-improvement
review offer whose explicit response is `requested`; the response and
termination receipts; and a top-level `active_run_id` that no longer names the
run. Reject stale or mixed run, contract, task/chat, shared-context,
material-processing eligibility, manifest, source-policy, or plan lineage.
System work is separate and never resumes the completed course run.

The offer must have presented the complete mandatory scope and been recorded
before it was asked. On resume, never ask it again when its status is
`offered_awaiting_response`, `requested` or `declined`. A request authorises only
read-only comparison of run evidence with the current reusable system and one
versioned proposal. It does not authorise system-file changes, installation,
publication, release, activation, schedule registration or modification, an
immediate run, or any new MCP server, connector, authentication, permission or
external egress.

Silence remains `offered_awaiting_response` and closes nothing. An explicit
request or decline closes the course run as terminal `complete_dormant`, clears
`active_run_id`, prevents resumption, and persists one informational trigger-
guidance offer. Decline ends system action; request opens only separate system
work. The guidance registers and triggers nothing.

## Improvement proposal

After those prerequisites pass, compare actual run evidence with the workflow
skills and umbrella routing; plugin or platform adapter; `AGENTS.md`, rules,
workflows, agent configurations and specialist-role reference; project
template, state schema and migration; validators, tests and QA; documentation;
memory or other workflow-owned durable instruction stores; schedule contracts;
permissions, tools, external egress and automatic behaviour; and compatibility,
benefits, regressions, risks, residual risks and rollback. Propose changes under
a unique proposal ID/version with:

- problem demonstrated by the run;
- affected system files;
- exact proposed change;
- benefit and possible regression;
- migration/compatibility impact;
- tests and success criteria;
- residual risk and rollback; and
- lecturer choices: keep current, revise proposal, or validate candidate.

Do not include course content, answer keys, personal data, or copyrighted assets
in the reusable adapter.

Do not inspect unrelated personal or global memory.

## System gate and validation

Create changes only after a separate completed System Gate approval with exact
current lineage, proposal ID/version, validation run, and exact targets, whose
reply contains `APPROVE SYSTEM FILES` as a standalone line. The token alone is
invalid. Keep the result in an inactive candidate. Validate manifests, JSON and
frontmatter, skill/rule/workflow structure, setup preview/apply/no-overwrite
behaviour, manifest hashing, lineage rejection, gate ceilings, answer-key
boundaries, target restrictions, retry rules, preview-only state migration,
and documentation. Forward-test
in a disposable course folder and verify the original candidate and fixtures
remain unchanged.

The System Gate may approve an activation-ready candidate, but never activates it. Record the exact proposal ID/version, validation run and evidence, residual risk, and rollback reference.

## Separate runtime activation

Activation requires a later lecturer decision naming the exact validated proposal ID/version. Missing or stale lineage leaves top-level state `candidate_not_active`. Activation, keeping inactive, and revise/revalidate are all valid choices.

## Standing schedule contract

Do not register a schedule until the runtime is active and the contract binds
to that exact activated version and current Gate-0A eligibility fingerprint.
Present a complete versioned contract containing exact course/project, task
type, canonical mission, goals/non-goals, success/stop criteria, tools/actions,
source classes, audiences, eligibility fingerprint, source-policy version/
fingerprint, assessment-security boundary, protected root, timezone,
recurrence, gate ceilings, retry/escalation/termination rules, unique output
naming, no-immediate-run rule, activation reference, and non-null expiry.

Run a no-write simulation first: no registration, trigger, web call, or file change.

Freeze the complete visible contract before approval. Store its validator-derived canonical SHA-256 as `approved_contract_snapshot_reference`, use offset-bearing `YYYY-MM-DDTHH:MM:SS+HH:MM[IANA/Timezone]` activation and expiry values, and recheck the snapshot, runtime, policy and expiry before registration and every recurrence.

Register only after one lecturer reply containing exactly and only these completed lines with matching values:

```text
APPROVE SCHEDULES
Schedule contract: <exact contract ID and version>
Expires: <exact local date and time with IANA timezone>
```

Approval registers the schedule but never triggers an immediate content run.
Each later recurrence creates a fresh run and lineage containing the current
eligibility fingerprint, then revalidates eligibility, sources, and policy,
waits at its first required gate, and stops at its stage ceiling. Eligibility
change, expiry, material changes, stale baselines, or mismatched runtime/source
lineage fail closed and require reconfirmation. Pause is explicit; renewal
requires a new version, eligibility binding, expiry, simulation, and approval;
rollback disables scheduling and preserves history.
