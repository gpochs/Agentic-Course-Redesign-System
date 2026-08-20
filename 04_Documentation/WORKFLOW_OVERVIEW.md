# Workflow overview

## Decision flow

```text
One isolated course project
        |
Gate 0: sources, data, rights, tools, egress, audiences
        |
Gate 1: course brief and fresh run contract
        |
Five-role preliminary scan + live alignment ledger
        |
HITL 1 / Gate 2A: lecturer chooses focus areas
        |
Deep research + cross-specialist reconciliation + red team
        |
HITL 2 / Gate 2B: lecturer decides concrete changes
        |              (research dossier/handoff targets only)
Gate 3: coherent blueprint + exact material targets
        |
Gated production + independent QA of every artefact
        |
HITL 3: lecturer accepts, revises or rejects materials
        |
Optional separate system-improvement proposal
        |
Optional later runtime activation
        |
Optional still-later expiring schedule contract
```

## Specialist team

The five core perspectives are course mapping, active learning, purposeful AI
integration, learner experience/accessibility/workload, and assessment with
constructive alignment. Assessment owns a live outcomes-activities-assessment
ledger from the preliminary scan. Source/citation and artefact/accessibility QA
are independent audit roles, not substitutes for the five perspectives.

## Gate semantics

- **Gate 0** permits only the bounded inventory and Gate 1 brief.
- **Gate 1** permits the five-role preliminary scan through the HITL 1 wait.
- **Gate 2A** permits deeper research through the HITL 2 wait.
- **Gate 2B** may approve only exact dated research dossier and handoff targets
  under `03_Research/`; it is not course-material write authority.
- **Gate 3** approves the integrated blueprint and exact typed material targets
  under `04_Working_Copies/` and `05_Approved/`.
- Named artefact gates and independent QA govern production.
- **HITL 3** is the lecturer's decision on the produced files.

Every record is bound to a fresh run, run-contract ID/version, task reference,
shared-context version, source-manifest fingerprint, source-policy
version/fingerprint and plan version. Stale lineage is rejected.

## Scheduled work

The first run is manual. A schedule is considered only after successful course
acceptance, validated system improvement and separate exact-version activation.
Its contract expires, never triggers an immediate run when approved, creates a
fresh lineage on every recurrence, stops at lecturer gates and never grants
standing course-material production authority.

