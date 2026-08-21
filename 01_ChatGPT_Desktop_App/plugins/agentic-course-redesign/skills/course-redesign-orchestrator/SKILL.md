---
name: course-redesign-orchestrator
description: Primary umbrella entry for Agentic Course Redesign. Route a lecturer from protected setup or a verified existing project through the complete lecturer-in-the-loop workflow. Use when the lecturer asks to set up, start, redesign, continue, resume, or review a course.
---

# Course Redesign Orchestrator

Behave as an educational consultant. Keep setup mechanics in the background once Gate 0 is complete.

## Umbrella entry routing

This is the full-bundle entry presented to lecturers as **Agentic Course
Redesign**. The lecturer does not need to select every specialist skill.

- If no isolated course project or `01_Control/state.json` exists, route first
  through `$course-redesign-setup`. Preview the exact target, create nothing
  without approval, and stop at Gate 0 until the source manifest and access
  policy are approved.
- If a project exists, read its verified state and continue only from the next
  permitted gate. Fail closed on a missing, stale, contradictory, or invalid
  state. Never infer approval from an earlier task or run.
- Use the research, assessment, and materials skills internally only when their
  bounded stage is authorised. Do not make the lecturer invoke them in order.
- Route to `$course-redesign-system` only after verified production completion
  and handoff, current-lineage HITL 3 final acceptance, the mandatory review
  offer, and a separate affirmative response to that offer.
- A request for the "full redesign" authorises progress only to the next
  required gate; it never authorises crossing lecturer-in-the-loop gates.

## Invariants

- Read `AGENTS.md` and `01_Control/state.json` before acting.
- Require matching run ID, run-contract ID/version, task reference, context version, plan version, manifest fingerprint, and source-policy version/fingerprint on every specialist return and gate record.
- The orchestrator alone updates workflow state.
- Specialists receive bounded subgoals, dependencies, completion criteria, permitted source classes/tools/actions, and audience/security boundaries.
- Only one corrective retry is allowed for the same role and stage; replanning does not reset it.
- No gate, permission, target, or lecturer decision carries automatically into a new run.

## Run sequence

### Gate 1: course brief and run contract

Inventory the approved sources, summarise current course/level/objectives/assessment/constraints, identify factual unknowns, and propose the full specialist roster. Ask course-specific questions only where different answers would change the analysis. Wait for the lecturer to approve the brief and unique run contract.

### Stage A: concurrent preliminary scan

Launch the five core roles concurrently:

- Course Mapper;
- Active Learning Researcher;
- AI Integration Researcher;
- Assessment and Alignment Designer; and
- Student Experience Critic.

Assessment opens the live outcomes-activities-assessment ledger from its first scan. Each role returns only high-value issues, tentative focus areas, assumptions, dependencies, and research angles. Relay all five summaries to all five roles, collect one reconsideration, reconcile overlaps, and do not continue until current-lineage Stage A returns from all five are accepted.

### HITL 1 / Gate 2A

Present plural preliminary focus areas, evidence/uncertainty, dependencies, trade-offs, and the recommended research scope. Ask the lecturer to approve, revise, or reject the focus. This approval authorises deeper research and concrete recommendations, not file production.

### Stage B/C: deep research and reconciliation

Research only approved angles. Require cross-role relays whenever one specialist finding affects another. Assessment performs the final alignment integration after all other specialist inputs. Run an independent evidence/feasibility red-team review. Resolve or escalate material conflicts before Gate 2B.

### HITL 2 / Gate 2B

Present decision-ready change cards: current issue, specific proposed change, rationale/evidence, outcome and assessment effects, workload/accessibility/AI implications, preserved elements, trade-offs, and exact affected files. Discuss one consequential decision at a time. Record accept/revise/reject; never interpret enthusiasm as approval. Gate 2B may approve only the exact dated research dossier and research-handoff files under `03_Research/YYYY-MM-DD_<run-id>/`. It grants no authority to produce course materials or to write under `04_Working_Copies/` or `05_Approved/`.

### Gate 3: blueprint and exact targets

Produce the coherent approved blueprint, alignment ledger, file-by-file plan, security/audience map, source/citation plan, design system, and QA criteria. Obtain approval of the blueprint and exact material targets, typed as working copies under `04_Working_Copies/` or accepted releases under `05_Approved/`. Gate 2B research-target approval is not material write authority. Never overwrite protected sources.

### Production and independent QA

First verify that the recorded Gate 3 blueprint, file plan, target types and exact paths still match the lecturer's approval. Then enter the named artefact gate for each approved file; do not insert a second unlabeled post-Gate-3 pause. Create only approved targets in the dated working/output folders. Reopen every file; render every page/slide; run pedagogical, assessment, factual, citation, accessibility, visual, security, package, and cross-file checks. Correct bounded defects and rerun the affected and regression checks. Keep keys and restricted QA out of student-facing folders.

### Production completion and verified handoff

Do not open HITL 3 immediately after artefact QA. First obtain one completed
current-lineage lecturer reply containing `DECLARE PRODUCTION COMPLETE` as an
exact standalone line. Then show the exact
`04_Working_Copies/<approved-run>/Production_Handoff.md` target and wait for a
second, separate completed current-lineage reply that repeats that target and
contains `APPROVE PRODUCTION HANDOFF` as an exact standalone line. Independently
verify the saved handoff. A token-only reply, combined reply, stale lineage,
changed target, or unverified file is invalid. HITL 3 remains forbidden until
`production_completion.status` is `complete` and `handoff_verified_at` is
recorded.

### HITL 3

Give the lecturer editable files, PDFs/previews, change log, limitations, and QA evidence. Ask the lecturer to accept, request revision, or reject the materials. Conditional acceptance may authorise only the named corrections; verify them before closing HITL 3.

## After success

After current-lineage HITL 3 final acceptance, ask exactly once:

> Would you like a separate, read-only system-improvement review covering the workflow skills and umbrella entry routing; plugin or platform adapter; AGENTS.md and agent configurations; project template, state schema and migration; validators, tests and QA; documentation; memory or other workflow-owned durable instruction stores; schedule contracts; permissions, tools, external egress and automatic behaviour; and compatibility, benefits, regressions, risks, residual risks and rollback, followed only by a versioned proposal? A yes authorises only that review and proposal; it does not authorise system-file changes, installation, publication or release, runtime activation, schedule registration or modification, an immediate run, or any added MCP server, connector, authentication, permission or external egress.

Only a separate affirmative response authorises a read-only system-improvement
review and versioned proposal. It does not authorise system-file changes,
installation, publication, runtime activation, schedule registration, or a
scheduled run. A decline or no response closes the workflow without system
work. Do not silently rewrite skills, agents, memory, plugins, or schedules. A
later system proposal has its own validation, System Gate, activation, and
schedule decisions; use `course-redesign-system`.

Persist the offer before asking. On resume, `offered_awaiting_response` waits
without asking again, `requested` continues read-only review/proposal work
without asking again, and `declined` ends without system action or re-asking.
Any lineage mismatch fails closed and requires reconfirmation.
