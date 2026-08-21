---
name: course-redesign-orchestrator
description: Run the lecturer-in-the-loop agentic course-redesign workflow from an approved manifest through preliminary scan, research, design dialogue, production, independent QA, and lecturer acceptance. Use when a lecturer wants to analyse, redesign, continue, or review a course project.
---

# Course Redesign Orchestrator

Behave as an educational consultant. Keep setup mechanics in the background once Gate 0 is complete.

## Invariants

- Read `AGENTS.md` and `01_Control/state.json` before acting.
- Require matching run ID, run-contract ID/version, task reference, context version, plan version, manifest fingerprint, and source-policy version/fingerprint on every specialist return and gate record.
- The orchestrator alone updates workflow state.
- Specialists receive bounded subgoals, dependencies, completion criteria, permitted source classes/tools/actions, and audience/security boundaries.
- Only one corrective retry is allowed for the same role and stage; replanning does not reset it.
- No gate, permission, target, or lecturer decision carries automatically into a new run.

## Run sequence

### Umbrella entry and Gate 0

The umbrella entry `Agentic Course Redesign` always routes here first and then
to Gate 0. Read `01_Control/state.json`; if the course scaffold is missing or
uninitialised, use `course-redesign-setup` in preview-only mode and obtain the
required setup approval. Gate 0 may inventory and hash candidate sources, but do
not analyse their content or launch specialists until the exact source manifest
and versioned source-access policy are approved.
Never infer Gate 0 from plugin selection, an earlier run, an existing folder or
an umbrella prompt.

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

### Production declaration and handoff

After all named artefact gates and QA pass, wait for a completed current-lineage
lecturer reply containing `DECLARE PRODUCTION COMPLETE` as a standalone line. Persist
that validated declaration before presenting the exact Production Handoff
target. Wait again for a second, separate completed current-lineage reply
containing `APPROVE PRODUCTION HANDOFF` as a standalone line and repeating the
exact target. A token-only, combined, stale-lineage or changed-target reply is
invalid. Save and independently verify
the handoff, then persist its verification receipt. Do not open HITL 3 until the
declaration, handoff approval and handoff verification are all complete.

### HITL 3

Only after the verified Production Handoff, give the lecturer editable files,
PDFs/previews, change log, limitations, and QA evidence. Ask the lecturer to
accept, request revision, or reject the materials. Conditional acceptance may
authorise only the named corrections; verify them before recording current-
lineage final acceptance and closing HITL 3.

## After success

Persist a system-improvement offer record and ask this complete question exactly
once:

> Would you like a separate, read-only system-improvement review covering the workflow skills and umbrella entry routing; plugin or platform adapter; AGENTS.md and agent configurations; project template, state schema and migration; validators, tests and QA; documentation; memory or other workflow-owned durable instruction stores; schedule contracts; permissions, tools, external egress and automatic behaviour; and compatibility, benefits, regressions, risks, residual risks and rollback, followed only by a versioned proposal? A yes authorises only that review and proposal; it does not authorise system-file changes, installation, publication or release, runtime activation, schedule registration or modification, an immediate run, or any added MCP server, connector, authentication, permission or external egress.

On resume, an `offered_awaiting_response` record means wait without asking
again. `requested` authorises only the read-only review and one versioned
proposal; `declined` ends without system action. Do not silently rewrite skills,
agents, memory, plugins or schedules. Candidate file changes require a separate
System Gate, and activation and scheduling remain later separate decisions. Use
`course-redesign-system` only after its prerequisites pass.
