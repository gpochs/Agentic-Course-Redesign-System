---
description: Run read-only project-local integrity and inactive-state checks, reporting failures without repairing or activating anything.
---

# Validate the local course workspace

1. Read root `AGENTS.md` and use the `course-redesign-setup` skill.
2. Request review, then run the state validator against
   `01_Control/state.json`.
3. If a source manifest exists, verify it read-only against
   `00_Source_Materials/` and `00_Context/`; do not replace it.
4. Verify that protected roots contain no redirecting links or junctions and
   that no source hash has changed.
5. Confirm `candidate_not_active`, empty schedules, automatic activation
   forbidden, Gate 2B research-only targets, and Gate 3 material-target rules.
6. Report exact commands, exit codes, fingerprints, failures, and limitations.
   Do not repair state, activate a runtime, register a schedule, or proceed to a
   later gate.
