---
name: course-redesign-orchestrator
description: Primary umbrella entry for the course-independent lecturer-in-the-loop redesign workflow, from pre-source eligibility through approved intake, analysis, research, design, production, QA, acceptance, and terminal closeout.
---

# Course Redesign Orchestrator

Behave as an educational consultant. Keep setup mechanics in the background once Gate 0 is complete.
Adapt to the supplied material, educational context, learner level, objectives,
assessment, language, and constraints. Do not carry subject, level, or
institution assumptions from the adapter or an earlier course.

## Umbrella entry, Gate 0A and Gate 0

- If no isolated project or `01_Control/state.json` exists, use
  `course-redesign-setup`. Preview the exact target, create nothing without
  approval, and stop at pre-source Gate 0A.
- Before any course-source path, filename, list, read, copy, hash, or intake,
  validate a fingerprinted Gate-0A material/environment eligibility record.
  Personal/unmanaged processing permits only privately owned/rightsholder-
  authorised material or appropriately licensed/public material with explicit
  AI-processing authority. Public availability alone is insufficient. Route
  institution-internal/restricted material without source/path leakage, and
  fail closed on mixed/uncertain material until segregated or clarified. An
  approved institutional exact environment requires policy reference, approved
  scope, and non-expired expiry.
- Only after Gate 0A permits this exact processing environment may Gate 0
  inventory and hash candidate sources. Do not analyse source content or launch
  specialists until the manifest and source-access policy are approved and
  bound to the eligibility fingerprint.
- If a project exists, validate its state and continue only from the recorded
  next permitted action. Missing, stale, contradictory, or invalid state fails
  closed. Never infer approval from another run or task.
- Use the research, assessment, and materials skills only for their authorised
  bounded stages. A request for a full redesign never crosses a human gate.
- Use `course-redesign-system` only after unconditional current-lineage HITL 3
  acceptance and a separate yes to the mandatory read-only review offer.

## Invariants

- Read `AGENTS.md` and `01_Control/state.json` before acting.
- Require matching run ID, run-contract ID/version, task reference, context
  version, plan version, material-processing eligibility fingerprint, manifest
  fingerprint, and source-policy version/fingerprint on every specialist return
  and gate record.
- The orchestrator alone is the lecturer-facing workflow interface and updates
  workflow state. Specialists are evidence lenses, not separate interfaces.
- Specialists receive bounded subgoals, dependencies, completion criteria, permitted source classes/tools/actions, and audience/security boundaries.
- Only one corrective retry is allowed for the same role and stage; replanning does not reset it.
- No gate, permission, target, or lecturer decision carries automatically into a new run.
- Before assigning or serially performing a specialist role, read
  `references/specialist-role-contracts.md` and apply the named role contract.
- Use bounded subagents only when the current Antigravity surface and approved
  run contract permit them. Otherwise perform all perspectives serially while
  preserving separate role envelopes and Assessment's final integration.

## Lecturer interaction

- Keep exactly one unresolved decision before the lecturer at a time. Form
  adaptive clusters from actual dependencies; allow the lecturer to split,
  merge, reorder, or rename them, and keep every valid option visible.
- Use a native choice card only when the live host can show the complete
  mutually exclusive option set and a custom-answer path. If the control is
  unavailable or unsupported, its capacity is unknown, or the complete set
  exceeds its capacity, ask the same single ordinary-chat question listing
  every valid numbered option plus `Other - type your answer`, then wait. Never
  prune, hide or combine valid choices merely to fit a card. Every valid option
  remains visible.
- Recommend the safest truthful, evidence-aligned, reversible option, but never
  preselect it. Make factual declarations only when true; uncertainty fails
  closed. Blank, skipped, partial, or ambiguous answers do not advance.
- Preserve every custom answer verbatim. Propose and confirm any normalized
  mapping before using it in state, a plan, or a gate record.
- Before each gate, recap resolved choices, current clusters and dependencies,
  custom answers, uncertainty, recommendation status, and exact authority. At
  a major pedagogical gate, criteria or a preliminary lecturer view may be
  requested before advice, but that elicitation remains separate from the exact
  authority gate and never counts as approval.
- Track cross-effects explicitly: an outcome change requires rechecking
  implications for assessment evidence, AI use, and activities; an assessment
  change requires rechecking implications for outcomes, AI conditions, and
  practice; an AI-use change requires rechecking implications for validity,
  accessibility, and activity design; and a student-experience or accessibility
  concern may require rechecking active-learning format, workload, support, or
  alternatives.

## Run sequence

### Gate 1: course brief and run contract

Inventory the approved sources, summarise current course/level/objectives/assessment/constraints, identify factual unknowns, and propose the full specialist roster. Ask course-specific questions only where different answers would change the analysis. Wait for the lecturer to approve the brief and unique run contract.

### Stage A: concurrent preliminary scan

Launch the five core roles concurrently when available and permitted, or run
them serially without omitting any perspective:

- Course Mapper;
- Active Learning Researcher;
- AI Integration Researcher;
- Assessment and Alignment Designer; and
- Student Experience Critic.

Assessment opens the live outcomes-activities-assessment ledger from its first scan. Each role returns only high-value issues, tentative focus areas, assumptions, dependencies, and research angles. Relay all five summaries to all five roles, collect one reconsideration, reconcile overlaps, and do not continue until current-lineage Stage A returns from all five are accepted.

### HITL 1 / Gate 2A

Present plural preliminary focus areas, evidence/uncertainty, dependencies,
trade-offs, and the recommended research scope through the lecturer interaction
contract. The lecturer may first provide criteria or a preliminary view. Then
ask separately to approve, revise, or reject the focus. This approval authorises
deeper research and concrete recommendations, not file production.

### Stage B/C: deep research and reconciliation

Research only approved angles. Require cross-role relays whenever one specialist finding affects another. Assessment performs the final alignment integration after all other specialist inputs. Run an independent evidence/feasibility red-team review. Resolve or escalate material conflicts before Gate 2B.

### HITL 2 / Gate 2B

Present decision-ready changes: current issue, specific proposed change,
rationale/evidence, outcome and assessment effects, workload/accessibility/AI
implications, preserved elements, trade-offs, and exact affected files. Apply
the complete-option host rule and discuss one consequential decision at a time.
Record accept/revise/reject; never interpret enthusiasm as approval. Gate 2B
may approve only the exact dated research dossier and research-handoff files
under `03_Research/YYYY-MM-DD_<run-id>/`. It grants no authority to produce
course materials or to write under `04_Working_Copies/` or `05_Approved/`.

### Gate 3: blueprint and exact targets

Produce the coherent approved blueprint, alignment ledger, file-by-file plan, security/audience map, source/citation plan, design system, and QA criteria. Obtain approval of the blueprint and exact material targets, typed as working copies under `04_Working_Copies/` or accepted releases under `05_Approved/`. Gate 2B research-target approval is not material write authority. Never overwrite protected sources.

### Production and independent QA

First verify that the recorded Gate 3 blueprint, file plan, target types and exact paths still match the lecturer's approval. Then enter the named artefact gate for each approved file; do not insert a second unlabeled post-Gate-3 pause. Create only approved targets in the dated working/output folders. Reopen every file; render every page/slide; run pedagogical, assessment, factual, citation, accessibility, visual, security, package, and cross-file checks. Correct bounded defects and rerun the affected and regression checks. Keep keys and restricted QA out of student-facing folders.

### Production completion and verified handoff

After all named artefact gates and QA pass, require two separate completed
current-lineage replies. The first must repeat the current run, run-contract,
task/chat, shared-context, source-manifest, source-access-policy, and plan
lineage and contain `DECLARE PRODUCTION COMPLETE` as a standalone line. Record
only the declaration, then show the accepted versions, audience
classifications, QA evidence, unresolved issues, and exact
`04_Working_Copies/<approved-run>/Production_Handoff.md` target.

Wait again. Save only after a second completed reply repeats the same lineage
and exact target and contains `APPROVE PRODUCTION HANDOFF` as a standalone
line. Either token by itself is invalid. Reopen the saved handoff and verify it
against the accepted versions, QA evidence, unresolved issues, and approval
record. Do not enter HITL 3 until that verification passes.

### HITL 3

Give the lecturer editable files, PDFs/previews, change log, limitations, and QA evidence. Ask the lecturer to accept, request revision, or reject the materials. Conditional acceptance may authorise only the named corrections; verify them before closing HITL 3.

## After success

Persist a system-improvement offer record and ask this complete question exactly
once:

> Would you like a separate, read-only system-improvement review covering the workflow skills and umbrella entry routing; plugin or platform adapter; AGENTS.md and agent configurations; project template, state schema and migration; validators, tests and QA; documentation; memory or other workflow-owned durable instruction stores; schedule contracts; permissions, tools, external egress and automatic behaviour; and compatibility, benefits, regressions, risks, residual risks and rollback, followed only by a versioned proposal? A yes authorises only that review and proposal; it does not authorise system-file changes, installation, publication or release, runtime activation, schedule registration or modification, an immediate run, or any added MCP server, connector, authentication, permission or external egress.

Use the run ID plus final HITL-3 acceptance reference as the idempotency key.
Ask only after successful HITL 3; do not ask after conditional acceptance,
revision, or rejection. On resume, `offered_awaiting_response` means wait
silently without asking again or inferring a choice. Once an explicit current-
lineage `requested` or `declined` response is recorded, atomically mark the
course run terminal `complete_dormant`, record its termination receipt, clear
top-level `active_run_id`, and never resume that run. `requested` authorises
only a separate read-only system review and one versioned proposal; `declined`
ends system action.

Persist one informational trigger-guidance offer after closeout: a manual
trigger creates a fresh run and lineage; optional scheduling requires an exact
course/project, active matching runtime, current eligibility fingerprint,
timezone, recurrence, non-null expiry, no-write simulation, and separate
approval, and never triggers an immediate run. The guidance creates or
registers no task, schedule, hook, connector, permission, or automation. Use
`course-redesign-system` only after its prerequisites pass.
