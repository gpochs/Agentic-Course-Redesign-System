---
description: Run read-only project-local integrity and inactive-state checks, reporting failures without repairing or activating anything.
---

# Validate the local course workspace

1. Read root `AGENTS.md` and use the `course-redesign-setup` skill.
2. Request review, then run the state validator against
   `01_Control/state.json`.
3. Before touching any source manifest or source path, verify the current
   Gate-0A material-processing eligibility fingerprint. If it is absent, stale,
   route-only, failed closed, mixed, or uncertain, stop without source detail.
   If a source manifest exists and Gate 0A permits this exact environment,
   verify it read-only against
   `00_Source_Materials/` and `00_Context/`; do not replace it.
4. Verify that protected roots contain no redirecting links or junctions and
   that no source hash has changed.
5. Confirm schema 8, `candidate_not_active`, empty schedules, automatic
   activation forbidden, Gate 2B research-only targets, Gate 3 material-target
   rules, production-handoff-before-HITL3 ordering, and durable idempotent
   system-review-offer/response, terminal dormant closeout, and trigger-guidance
   receipts. For schema 7, preview the v7-to-v8 migration only; never
   apply it from this workflow.
6. Report exact commands, exit codes, fingerprints, failures, and limitations.
   Do not repair state, activate a runtime, register a schedule, or proceed to a
   later gate.
