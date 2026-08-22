# Workflow overview

## Decision flow

Every human-in-the-loop phase uses one shared dialogue contract. The
orchestrator is the sole lecturer-facing interface and asks one unresolved
consequential question at a time. It uses a native card only when the live host
can show the complete mutually exclusive option set plus a custom-answer path.
If that control is unavailable or unsupported, its capacity is unknown, or the
complete set exceeds its capacity, the orchestrator shows every valid numbered
option plus Other in one ordinary-chat question. It never prunes, hides or
combines valid choices to fit a card. Long decisions are clustered only by real evidence or consequence
dependencies; every valid option remains visible, and the
lecturer may split, merge, reorder or rename a cluster. Exact custom answers,
consequences and editable recaps are recorded; no recommendation is preselected
and no conversational selection replaces an authority gate.

```text
One isolated course project
        |
Gate 0A: material basis + provider/environment eligibility
        | eligible here, or route/segregate/stop before source paths
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
Current-lineage production-complete declaration
        |
Separate exact handoff approval + independent verification
        |
HITL 3: lecturer accepts, revises or rejects materials
        |
Mandatory question: separate read-only system-improvement review?
        | explicit yes or no required; silence waits
Record the explicit response; yes authorises later review only
        |
Close accepted course run as terminal complete_dormant
        |
One informational trigger-guidance offer
        |
Optional separate system review/change/activation lifecycle
        |
Fresh manual trigger, or separately approved expiring schedule trigger
        | always creates a new run and lineage
```

## Specialist team

The five core perspectives are course mapping, active learning, purposeful AI
integration, learner experience/accessibility/workload, and assessment with
constructive alignment. Assessment owns a live outcomes-activities-assessment
ledger from the preliminary scan. Source/citation and artefact/accessibility QA
are independent audit roles, not substitutes for the five perspectives.
Specialists are evidence lenses rather than separate user interfaces: they
return lecturer-only questions to the orchestrator for the same guided
decision process.

## Gate semantics

- **Gate 0A** occurs before a source path is requested, listed, read, copied or
  fingerprinted. It records the material basis, AI-processing authority,
  sensitivity, assessment security, selected provider and approved environment.
  Institution-internal/restricted, mixed or uncertain material routes or blocks
  without leaking path or filename metadata.
- **Gate 0** permits only the bounded inventory and Gate 1 brief.
- **Gate 1** permits the five-role preliminary scan through the HITL 1 wait.
- **Gate 2A** permits deeper research through the HITL 2 wait.
- **Gate 2B** may approve only exact dated research dossier and handoff targets
  under `03_Research/`; it is not course-material write authority.
- **Gate 3** approves the integrated blueprint and exact typed material targets
  under `04_Working_Copies/` and `05_Approved/`.
- Named artefact gates and independent QA govern production.
- Production cannot enter HITL 3 until a completed current-lineage reply
  contains standalone `DECLARE PRODUCTION COMPLETE`, a second completed reply
  repeats the exact handoff target with standalone
  `APPROVE PRODUCTION HANDOFF`, and the handoff is independently verified.
- **HITL 3** is the lecturer's decision on the produced files.
- Only unconditional current-lineage HITL 3 acceptance causes the orchestrator
  to ask whether the lecturer wants a separate read-only system-improvement
  review. A yes permits evidence review and a versioned proposal only; it does
  not permit edits, installation, publication, activation or scheduling.
- The lecturer must explicitly accept or decline that offer. Silence is not a
  decision. After the answer is recorded, the accepted course run becomes
  terminal `complete_dormant`, clears its active run ID and cannot resume.
- The orchestrator then makes one informational offer explaining manual and
  optional scheduled triggers. It does not register a schedule or start a run.

Every record is bound to a fresh run, run-contract ID/version, task reference,
shared-context version, source-manifest fingerprint, source-policy
version/fingerprint, material-processing-eligibility fingerprint and plan
version. Stale lineage is rejected.

## Scheduled work

Manual triggering is always available. An optional schedule is planned only
for an exact course and control workspace after successful closeout. Its
contract records timezone, recurrence, eligibility fingerprint and a non-null
expiry; it is simulated without writes and separately approved. Registration
never triggers an immediate run. Every recurrence creates fresh lineage, stops
at lecturer gates and grants no standing course-material production authority.
