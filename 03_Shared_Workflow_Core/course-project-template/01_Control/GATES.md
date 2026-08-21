# Lecturer decision gates

Every approval belongs to one run and records the run ID, run-contract ID/version, task/chat reference, shared-context version, source-manifest fingerprint, source-access-policy version/fingerprint, and plan version.

## Gate 0 — source, data, rights, tools, egress, audiences

Approve the exact source manifest and policy before specialist reading. Gate 0 allows the Gate 1 brief only.
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
