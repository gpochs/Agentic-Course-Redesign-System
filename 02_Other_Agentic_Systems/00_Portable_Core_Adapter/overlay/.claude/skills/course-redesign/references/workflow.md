# Lecturer-gated workflow

## Mission and loop

Together with the lecturer, produce the strongest defensible,
evidence-informed, constructively aligned, feasible redesign of the specific
course for its learners and context. Improve meaningful learning and
participation, purposeful AI competence, student experience, and valid
assessment while preserving worthwhile elements and respecting accessibility,
workload, rights, privacy, and institutional constraints.

Within an approved gate, repeat: plan the permitted subgoals; act using only
approved tools, data, and actions; observe evidence and uncertainty; evaluate
success and dependencies; replan unfinished downstream work. Increment the plan
version for consequential replanning. Never use replanning to change the main
goal, widen permissions, cross a gate, create write authority, reopen a settled
choice, or weaken a stop condition.

## Lecturer interaction contract

Keep exactly one unresolved decision before the lecturer at a time. Build
adaptive clusters from real dependencies rather than a fixed questionnaire;
the lecturer may split, merge, reorder, or rename clusters at any time. Keep
every valid option visible in its cluster. Never prune, hide or combine valid
choices merely to fit a card.

Use a native choice card only when the live host tool can show the complete
mutually exclusive option set plus a custom-answer path. If the control is
unavailable or unsupported, its capacity is unknown, or the complete set
exceeds its capacity, ask the same single ordinary-chat question listing every
valid numbered option plus `Other - type your answer`, then wait. Every valid
option remains visible; do not divide or truncate the set to force a card. Preserve
custom answers verbatim in the decision record, propose any normalized mapping,
and obtain confirmation before using that mapping.

Recommendations must be the safest truthful, evidence-aligned, reversible
option available and are never preselected. Make a factual declaration only
when it is true; missing or uncertain facts fail closed and become a question
or explicit blocker. Blank, skipped, partial, or ambiguous answers do not
resolve a decision or advance a gate.

Before every gate, recap the resolved decisions, current dependency clusters,
custom answers, uncertainty, and the exact authority about to be requested.
At a major pedagogical gate, the orchestrator may first ask for the lecturer's
criteria or preliminary view before offering advice. Keep this elicitation
separate from the exact authority gate; criteria, a preliminary view, or
agreement with advice never counts as gate approval.

Specialist roles are evidence lenses. They communicate through the
orchestrator, which remains the lecturer's single workflow interface and owns
questions, recaps, recommendations, mapping confirmations, and gate requests.
Track interdependencies explicitly. For example, an outcome change requires
rechecking assessment evidence, permitted AI use, and learning activities; an
assessment change requires rechecking outcomes, AI conditions, and practice;
an AI-use change requires rechecking validity, accessibility, and activity
design; and a student-experience or accessibility concern may require changes
to active-learning format, workload, support, or alternatives.

## Gate 0A: pre-source processing eligibility

Before source discovery, ask only non-identifying questions needed to classify
ownership/authorisation, licence and AI-processing authority, institutional
sensitivity, intended environment, and whether the collection is mixed or
uncertain. Do not enumerate, open, hash, copy, upload, or describe any course
file, and do not reveal a path, filename, title, excerpt, or manifest.

In a personal or unmanaged environment, allow privately owned or
rightsholder-authorised material. Appropriately licensed or public material may
proceed only when its licence or other explicit authority covers the intended
AI processing; public availability, classroom use, or a link alone is
insufficient. Institution-internal or restricted material is route-only unless
the record names an exact institution-approved environment reference, scope,
and non-expired approval. Mixed or uncertain material is blocked until every
component has an eligible route.

Persist the decision as a versioned processing-eligibility record with a
canonical SHA-256 fingerprint. A pass permits only the next source-boundary
step; it grants no source, role, tool, egress, audience, write, or gate
authority. A blocked or route-only result is a hard stop in this environment.

When the canonical shared helper is present, use
`scripts/create_material_processing_eligibility.py` in preview mode to produce
the deterministic candidate record, inspect the complete payload and target,
and write only after the exact no-overwrite action is separately approved. If
the host cannot run that helper, use the generic host fallback: collect the
same category-level declarations one unresolved decision at a time, render the
complete candidate JSON deterministically from the canonical template, show it
for review, and wait for exact-target approval before creating a new file.
Never overwrite an eligibility record, invent an answer, or add an MCP,
connector, authentication, or egress dependency.

## Gate 0: source access and integrity

Only after a matching Gate 0A pass, inventory sources read-only. Confirm
integrity, source classes, rights, role and tool access, data egress, output
audiences, exclusions, and the versioned source-access policy. Bind the
lecturer's approval to the processing-eligibility, manifest, and policy
fingerprints. Gate 0 authorizes only preparation of the Gate 1 brief.

## Gate 1: course brief and run contract

Confirm learner and course context; source status and completeness; objective,
assessment, key, and rubric relationships; canonical goal, non-goals,
constraints, success criteria, stop conditions, tools/actions, bounded Stage A
subgoals, and maximum stage. Create fresh run, contract, context, plan, gate,
retry, and artefact state. Never reuse approval from another run.

## Stage A and Gate 2A

Start or fairly interleave these five perspectives:

1. Course mapping and learning outcomes.
2. Active learning.
3. AI integration and AI competence.
4. Student experience, accessibility, and workload proxy review.
5. Assessment and constructive alignment.

Assessment opens the provisional alignment ledger immediately and owns it.
Course Mapping proposes the initial map; Assessment tests its coverage and
validity. Relay summaries, dependencies, overlaps, and conflicts among all five.
Do not present Gate 2A until all five current-lineage Stage A returns are
accepted, the exchange is complete, and the ledger has started.

At Gate 2A, the lecturer approves, revises, or rejects the interpreted mission,
focus areas, and two-to-five Stage B subgoals, success criteria, dependencies,
replan triggers, and research scope for each role. Gate 2A grants no write
target and no production authority.

## Stage B and Gate 2B

Perform only approved deeper research. Prefer official, primary, peer-reviewed,
credible university, and public/open sources; label practice signals. Keep
atomic claims with source, date/currentness, support, confidence, limits, and
rights status. Never process licensed full text or protected data without
explicit permission.

Reconcile findings, then let Assessment integrate last. Run the Source
Verification and Citation Auditor and the Evidence and Feasibility Red Team.
Separate factual accuracy, citation mechanics, and rights review.

At Gate 2B, present concrete decisions one at a time using the lecturer
interaction contract above. The
lecturer may approve only the exact dated dossier and research-handoff targets
under `03_Research/YYYY-MM-DD_<run-id>/`. Write nothing before that approval.
Gate 2B never authorizes course-material production.

## Blueprint and Gate 3

After Gate 2B, the Learning Designer integrates the selected decisions into one
coherent blueprint and tests alignment, feasibility, accessibility, assessment
security, workload, rights, and citations. Keep every valid option in the
interaction until the lecturer resolves it, and preserve the resulting decision
record until the lecturer approves the blueprint and a typed, exact file plan.

Gate 3 may name exact working-copy targets under `04_Working_Copies/` and exact
accepted targets under `05_Approved/`. Verify the approved blueprint and file
plan once before production.

## Gated production and QA

Produce one named artefact at a time only after exact-target approval. Preserve
source hashes and work only from approved copies. The Learning Material
Designer proposes the artefact; the independent Artefact Accessibility and
Visual QA Auditor reopens or renders every exact output available to the host
and checks content, citations, accessibility, layout, leakage, and consistency.

Assessment material requires separately named student-facing and teacher-only
targets. Prove that student-facing outputs contain no answers, model responses,
hidden layers, speaker-note keys, or teacher comments. The lecturer accepts,
conditionally accepts named corrections, requests revision, or rejects each
artefact.

Production completion requires two separate, current-lineage decisions. First,
the lecturer's completed reply must repeat the current run, run-contract,
task/chat, shared-context, source-manifest, source-access-policy, and plan
lineage and contain `DECLARE PRODUCTION COMPLETE` as a standalone line. Record
only that declaration. After the verified accepted-version/QA record and exact
`04_Working_Copies/<approved-run>/Production_Handoff.md` target are shown, a
second completed reply must repeat the same lineage and exact target and contain
`APPROVE PRODUCTION HANDOFF` as a standalone line. Either token alone is
insufficient. Save only that approved target, then reopen it and verify that it
matches the accepted versions, audience classifications, QA evidence,
unresolved issues, and approval record. Do not enter HITL 3 until this saved
handoff verification passes.

## HITL 3: final lecturer acceptance

After the verified handoff, present the complete review package to the lecturer:
all editable deliverables and representative previews, the approved change log,
known limitations and rights boundaries, and the final quality-assurance
evidence. Make clear which files are student-facing, lecturer-only, or safe for
public distribution.

The lecturer may accept the package, conditionally accept it with named
revisions, request revision, or reject it. Treat conditional acceptance as
authority only for the named corrections, rerun proportionate independent QA,
and return the corrected package for a fresh HITL 3 decision. Do not mark the
course redesign complete until the lecturer gives current-lineage final
acceptance.

Immediately after unconditional current-lineage acceptance, persist the offer
record and ask this complete question exactly once:

> Would you like a separate, read-only system-improvement review covering the workflow skills and umbrella entry routing; plugin or platform adapter; AGENTS.md and agent configurations; project template, state schema and migration; validators, tests and QA; documentation; memory or other workflow-owned durable instruction stores; schedule contracts; permissions, tools, external egress and automatic behaviour; and compatibility, benefits, regressions, risks, residual risks and rollback, followed only by a versioned proposal? A yes authorises only that review and proposal; it does not authorise system-file changes, installation, publication or release, runtime activation, schedule registration or modification, an immediate run, or any added MCP server, connector, authentication, permission or external egress.

Ask only after successful HITL 3, not after conditional acceptance, revision,
or rejection. Use the run ID plus final HITL-3 acceptance reference as the
idempotency key. On resume, `offered_awaiting_response` means wait silently
without asking again, completing the run, or inferring a choice. A current-
lineage explicit `requested` or `declined` response closes the course run as
terminal `complete_dormant`, records the terminal reason and timestamp, and
clears `active_run_id`. `requested` authorises only a separate read-only review
and one versioned proposal; `declined` creates no system work. Reusable-system
work may begin only after the recorded separate request, and it never reopens
the completed course run.

After recording `complete_dormant`, offer this informational trigger guidance
once: future redesign work starts only from a fresh manual trigger, or from a
fresh scheduled trigger under a separately activated runtime and separately
approved, unexpired schedule contract. The offer creates or registers no task,
automation, schedule, hook, connector, permission, or immediate run. Silence on
the guidance offer requires no follow-up. Never continue the dormant run.

## Separate reusable-system lifecycle

Course acceptance does not authorize a system change. After a successful,
terminal dormant run, a separately requested improvement review may propose a new proposal ID,
version, exact diff, tests, risks, permissions, rollback, and plain-language
behaviour summary. Compare the workflow skills and umbrella routing; plugin or
platform adapter; `AGENTS.md` and agent configurations; project template,
state schema and migration; validators, tests and QA; documentation; memory or
other workflow-owned durable instructions; schedule contracts; permissions,
tools, external egress and automatic behaviour; and compatibility, benefits,
regressions, risks, residual risks and rollback.
Creating system files requires current lineage and a completed
reply containing `APPROVE SYSTEM FILES` as a standalone line. The result remains
an inactive candidate with `status=candidate_not_active`.

Activation is a later decision that names the exact validated proposal version,
passing evidence, residual risks, and rollback. Keeping it inactive remains a
valid choice.

Do not propose a schedule while inactive. Even after separate activation,
schedule registration requires a versioned standing contract with a non-null
expiry and a no-write simulation. Freeze that complete contract first, store its
validator-derived canonical
SHA-256 snapshot reference, use offset-bearing
`YYYY-MM-DDTHH:MM:SS+HH:MM[IANA/Timezone]` activation and expiry values, and
recheck the snapshot, runtime, policy and expiry before registration and every
recurrence.

Register only after one lecturer reply containing exactly and only these three
completed lines with actual values matching the visible contract:

```text
APPROVE SCHEDULES
Schedule contract: <exact contract ID and version>
Expires: <exact local date and time with IANA timezone>
```

The token alone, placeholders, or mismatched values are invalid. Registration
never triggers an immediate run. A later scheduled trigger creates a fresh run
and fresh Gate 0A, source, policy, contract, and gate lineage; it never resumes
the dormant run. A scheduled run performs at most the approved scan/research
sequence, creates no course materials, and ends at Gate 2B unless the lecturer
manually extends it.
