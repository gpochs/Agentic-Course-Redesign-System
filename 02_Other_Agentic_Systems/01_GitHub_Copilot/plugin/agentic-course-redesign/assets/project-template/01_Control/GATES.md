# Lecturer decision gates

Every approval belongs to one run and records the run ID, run-contract ID/version, task/chat reference, shared-context version, material-processing-eligibility fingerprint, source-manifest fingerprint, source-access-policy version/fingerprint, and plan version.

## Lecturer Decision Dialogue Contract

The orchestrator is the sole lecturer-facing interface and specialist roles are
evidence lenses. Ask one unresolved consequential question at a time. Before
using a native choice card, follow the live host tool contract. Use a card only
when it can present the complete mutually exclusive option set and a
custom-answer path without omission. Never prune, hide or combine valid choices
merely to fit a card. If a native card is unavailable or unsupported, its
capacity is unknown, or the complete set exceeds that capacity, ask the same
single question in ordinary chat with every valid numbered option plus `Other -
type your answer`, then wait. Every valid option remains visible. Cluster a very
long decision only where choices share
evidence or constrain one another; keep every valid option visible, explain the
dependency grouping and let the lecturer split, merge, reorder or rename it.
Mutually dependent outcomes, assessment evidence, permitted AI use and
learning activities belong together. Student-experience, accessibility and
active-learning perspectives may be clustered where participation design
jointly affects usability, inclusion, workload and engagement.

Preserve custom answers exactly and confirm their canonical interpretation.
Reflect each consequence in the chat/current-state decision ledger and show an
editable recap at each cluster or gate end. Skip or blank leaves a required
question unresolved. The safest truthful, evidence-aligned and reversible
option may be marked `Recommended` but is never preselected. Factual
declarations say “select only if true”; uncertainty fails closed. At major
pedagogical gates, ask for the lecturer's criteria and preliminary view before
recommending when practical. This dialogue never substitutes for the exact
authority gate, lineage record or approval token defined below.

## Gate 0A — material and processing-environment eligibility

This gate precedes any course-source path, filename, list, read, copy, hash or
other intake. Ask only for the material category, environment category,
internal/restricted and student-data flags, sensitivity classification,
assessment-security classification and authority to handle that assessment
security class, then record a canonical fingerprint. Null, inconsistent,
mixed or uncertain declarations fail closed. An approved record with
`reconfirmation_required=true` does not permit source intake. Do not ask the
lecturer to disclose source details before the gate passes.

In a personal/unmanaged environment, proceed only for privately owned or
rightsholder-authorised material, or appropriately licensed/public material
with explicit AI-processing authority. Public availability alone is
insufficient. Institution-internal/restricted material is route-only with zero
source/path leakage. Mixed material fails closed until segregated; uncertain
material fails closed until clarified. An approved institutional exact
environment must record its policy reference, approved scope and non-expired
expiry.

## Gate 0 — source, data, rights, tools, egress, audiences

Only after approved Gate 0A, inventory and hash sources. Approve the exact source manifest and policy before specialist reading. Gate 0 allows the Gate 1 brief only.
The `Agentic Course Redesign` umbrella entry always routes here; selecting it is
not approval and does not authorise course-content analysis. Gate 0 may inventory
and hash candidate sources only to present the exact manifest and policy.

## Gate 1 — course brief and run contract

Confirm the course/learner/assessment context, canonical goal, constraints, success/stop criteria, specialist roster, bounded Stage A subgoals, and maximum stage.

## HITL 1 / Gate 2A — preliminary focus areas

After all five core specialists complete Stage A and exchange summaries, approve/revise/reject plural focus areas and deep-research role contracts. No production.

## HITL 2 / Gate 2B — concrete redesign decisions

Review reconciled evidence and specific change cards. Decide one consequential
design point at a time. Gate 2B may approve only the exact dated research
dossier and research-handoff files under
`03_Research/YYYY-MM-DD_<run-id>/`. It does not authorise course-material
production or writes under `04_Working_Copies/` or `05_Approved/`.

## Gate 3 — coherent blueprint and exact file plan

Approve the alignment-tested blueprint, assessment/security map,
design/citation plan, QA criteria, and typed exact material targets: working
copies under `04_Working_Copies/` and accepted releases under `05_Approved/`.
The approved plan is verified once, then production proceeds through the named
gate for each artefact; there is no additional unlabeled approval pause.

## Production completion and handoff

The first completed reply must carry current lineage and contain this standalone line:

```text
DECLARE PRODUCTION COMPLETE
```

After the verified production record and exact handoff target are shown, a second completed reply must repeat the target and carry current lineage with:

```text
APPROVE PRODUCTION HANDOFF
```

## HITL 3 — lecturer acceptance

HITL 3 opens only after both production replies and independent verification of
the saved Production Handoff. The lecturer reviews editable files/previews,
change log, QA evidence, limitations, and preserved-source proof, then accepts,
conditionally accepts named corrections, requests revision, or rejects.

## Mandatory system-improvement review offer

After current-lineage HITL-3 acceptance, record the offer before asking the
complete system-improvement question exactly once. A request authorises only a
read-only review and one versioned proposal. It grants no authority to change
files, install, publish, activate, schedule, add permissions/connectors/auth or
trigger a run. On resume, wait on an existing offer rather than asking again.
Silence is `offered_awaiting_response`, never a request or decline.

After an explicit requested or declined response, atomically close the course
run as terminal `complete_dormant`, clear `active_run_id`, and never resume that
run. If requested, system-improvement work proceeds as a separate system
record, not as an extension of the course run. Persist one informational
trigger-guidance offer after closeout: manual triggering is available and
always creates a fresh run; optional scheduling needs exact course, project,
timezone, recurrence, non-null expiry and its own gates, with no immediate run.

## System Gate

System files are a separate proposal, available only after the recorded offer
was requested. Approval requires exact current lineage, proposal ID/version,
exact targets, validation evidence, risks, and rollback, plus:

```text
APPROVE SYSTEM FILES
```

This creates an activation-ready candidate only.

## Separate runtime activation

The lecturer must explicitly name and activate the exact validated proposal version. Keeping it inactive or revising/revalidating remains valid.

## Standing schedule

After active-runtime matching and a no-write simulation, schedule registration requires exactly and only:

```text
APPROVE SCHEDULES
Schedule contract: <exact contract ID and version>
Expires: <exact local date and time with IANA timezone>
```

Registration never triggers an immediate content run.
Every scheduled trigger records a fresh trigger/run/lineage, the current
eligibility fingerprint, the approved immutable contract-snapshot reference
and a valid offset timestamp. An active trigger must fall on or after contract
activation and before expiry. Pausing, expiry or cancellation disables future
triggers but preserves contract and run history; an on/after-expiry trigger
records an expired no-course-action receipt rather than analysing the course.

## GitHub Copilot native `ask_user` capacity override

This Copilot-only host rule applies the shared core's host-capacity contract to the demonstrated GitHub Copilot host; it changes no option, gate, evidence requirement, or workflow meaning. Keep one unresolved consequential question at a time. Use the native `ask_user` card for the complete valid option set whenever the live GitHub Copilot host accepts it. A live Copilot host has demonstrated at least five explicit choices plus a custom-answer field; this is an observed capability, not a maximum. Do not state or assume an unsupported maximum. Never prune, hide or combine valid choices merely to fit a card. If the host rejects or cannot present the complete valid set, ask one ordinary chat question listing every valid numbered option plus `Other`, then wait. For very long sets, dependency chunks are allowed only when choices share evidence or constrain one another; keep every valid option visible across chunks, explain the grouping, and let the lecturer split, merge, reorder or rename it.
