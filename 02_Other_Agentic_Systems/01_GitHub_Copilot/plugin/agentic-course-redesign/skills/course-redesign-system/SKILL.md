---
name: course-redesign-system
description: Review, validate, activate, schedule, pause, renew, or roll back the reusable agentic course-redesign system after a successful course run. Use for skills, plugin, AGENTS.md, custom agents, state schemas, memory, validators, runtime activation, or scheduled workflow contracts.
---

# Course Redesign System

## Lecturer Decision Dialogue Contract

The orchestrator is the sole lecturer-facing interface; specialist roles are
evidence lenses and return questions through it. Ask one unresolved
consequential question at a time. Before using a native choice card, follow the
live host tool contract. Use a card only when it can present the complete,
mutually exclusive option set and a custom-answer path without omission. Never
prune, hide or combine valid choices merely to fit a card. If a native card is
unavailable or unsupported, its capacity is unknown, or the complete set
exceeds that capacity, ask the same single question in ordinary chat with every
valid numbered option plus `Other - type your answer`, then wait. Every valid
option remains visible. For very
long decisions, use adaptive dependency-based clusters only when choices share
evidence or constrain one another: keep every valid option visible, explain the
grouping and let the lecturer split, merge, reorder or rename it. For example,
outcomes, assessment evidence, permitted AI use and learning activities belong
together when mutually dependent; student-experience, accessibility and
active-learning perspectives may be clustered when participation design
jointly affects usability, inclusion, workload and engagement.

Preserve a custom answer exactly, confirm its canonical interpretation, reflect
the consequence, and maintain a decision ledger in the chat and current state.
Show an editable recap at each cluster or gate end. A skipped or blank response
leaves a required question unresolved. The safest truthful, evidence-aligned,
reversible option may be marked `Recommended`, but never preselected; factual
declarations must say "select only if true," and uncertainty fails closed. At
major pedagogical gates, ask for the lecturer's criteria and preliminary view
before recommending when practical. Exact authority gates and approval tokens
remain separate and unchanged; a dialogue choice never substitutes for them.

Course-material acceptance and system activation are separate decisions. Never update the live system merely because a course run succeeded.

## Required successful-run evidence

Before any system review, verify one closed `complete_dormant` current-lineage run with all of the
following durable records: valid production declaration; matching Production
Handoff approval; independently verified handoff; accepted HITL 3 (including
verification of any named conditional corrections); and a system-improvement
review offer whose status is `requested`, plus the explicit response and
terminal closeout receipts. Top-level `active_run_id` must no longer name that
run. Reject stale or mixed run, contract, task/chat, shared-context,
eligibility, manifest, source-policy or plan lineage. System work is separate
from the closed course run.

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
`active_run_id`, prevents resumption and persists one informational trigger-
guidance offer. Decline ends system action; request opens only separate system
work.

The recorded question must be exactly:

> Would you like a separate, read-only system-improvement review covering the workflow skills and umbrella entry routing; plugin or platform adapter; AGENTS.md and agent configurations; project template, state schema and migration; validators, tests and QA; documentation; memory or other workflow-owned durable instruction stores; schedule contracts; permissions, tools, external egress and automatic behaviour; and compatibility, benefits, regressions, risks, residual risks and rollback, followed only by a versioned proposal? A yes authorises only that review and proposal; it does not authorise system-file changes, installation, publication or release, runtime activation, schedule registration or modification, an immediate run, or any added MCP server, connector, authentication, permission or external egress.

## Improvement proposal

After those prerequisites pass, compare actual run evidence with the current
skills and umbrella route; plugin or platform adapter; `AGENTS.md` and agent
configurations; project template, state schema and migration; validators and
tests; documentation; memory or other workflow-owned durable instruction
stores; schedule contracts; permissions, tools, egress and automatic behaviour;
and compatibility and rollback. Propose changes under a unique proposal
ID/version with:

- problem demonstrated by the run;
- affected system files;
- exact proposed change;
- benefit and possible regression;
- migration/compatibility impact;
- tests and success criteria;
- residual risk and rollback; and
- lecturer choices: keep current, revise proposal, or validate candidate.

Do not include course content, answer keys, personal data, or copyrighted assets in the reusable plugin.

## System gate and validation

Create changes only after a separate completed System Gate reply with exact
current lineage, proposal ID/version, validation evidence and exact targets,
and `APPROVE SYSTEM FILES` as a standalone line. A token-only reply is invalid.
Keep the result in an inactive candidate. Validate
manifests, JSON/TOML/YAML, skill structure, setup preview/apply/no-overwrite
behaviour, manifest hashing, lineage rejection, gate ceilings, answer-key
boundaries, target restrictions, retry rules, migration preview behaviour and
documentation. Forward-test in a disposable course folder and verify the
original candidate and test fixtures remain unchanged.

The System Gate may approve an activation-ready candidate, but never activates it. Record the exact proposal ID/version, validation run and evidence, residual risk, and rollback reference.

## Separate runtime activation

Activation requires a later lecturer decision naming the exact validated proposal ID/version. Missing or stale lineage leaves top-level state `candidate_not_active`. Activation, keeping inactive, and revise/revalidate are all valid choices.

## Standing schedule contract

Do not register a schedule until the runtime is active and the contract binds to that exact activated version and current Gate-0A eligibility fingerprint. Present a complete versioned contract containing exact course/project, task type, canonical mission, goals/non-goals, success/stop criteria, tools/actions, source classes, audiences, eligibility fingerprint, source-policy version/fingerprint, assessment-security boundary, protected root, lecturer-confirmed IANA timezone, recurrence, gate ceilings, retry/escalation/termination rules, unique output naming, no-immediate-run rule, activation reference, and non-null expiry.

Run a no-write simulation first: no registration, trigger, web call, or file change.

Freeze the complete visible contract before approval. Store its validator-derived canonical SHA-256 as `approved_contract_snapshot_reference`, use offset-bearing `YYYY-MM-DDTHH:MM:SS+HH:MM[IANA/Timezone]` activation and expiry values, and recheck the snapshot, runtime, policy and expiry before registration and every recurrence.

Register only after one lecturer reply containing exactly and only these completed lines with matching values:

```text
APPROVE SCHEDULES
Schedule contract: <exact contract ID and version>
Expires: <exact local date and time with IANA timezone>
```

Approval registers the schedule but never triggers an immediate content run. Each recurrence creates a fresh run and lineage containing the current eligibility fingerprint, then revalidates eligibility, sources and policy, waits at its first required gate, and stops at its stage ceiling. Eligibility change, expiry, material changes, stale baselines, or mismatched runtime/source lineage fail closed and require reconfirmation. Pause is explicit; renewal requires a new version, eligibility binding, expiry, simulation and approval; rollback disables scheduling and preserves history.

## GitHub Copilot native `ask_user` capacity override

This Copilot-only host rule applies the shared core's host-capacity contract to the demonstrated GitHub Copilot host; it changes no option, gate, evidence requirement, or workflow meaning. Keep one unresolved consequential question at a time. Use the native `ask_user` card for the complete valid option set whenever the live GitHub Copilot host accepts it. A live Copilot host has demonstrated at least five explicit choices plus a custom-answer field; this is an observed capability, not a maximum. Do not state or assume an unsupported maximum. Never prune, hide or combine valid choices merely to fit a card. If the host rejects or cannot present the complete valid set, ask one ordinary chat question listing every valid numbered option plus `Other`, then wait. For very long sets, dependency chunks are allowed only when choices share evidence or constrain one another; keep every valid option visible across chunks, explain the grouping, and let the lecturer split, merge, reorder or rename it.
