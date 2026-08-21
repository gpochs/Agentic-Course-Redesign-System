---
description: Prepare the one-course workspace and Gate 0 boundary without activating a runtime or reading protected content for specialist analysis.
---

# Start a gated course-redesign run

1. Read root `AGENTS.md`, `PROJECT_SETUP.md`, `01_Control/GATES.md`, and
   `01_Control/state.json`.
2. Use the `course-redesign-setup` skill.
3. Verify schema 7, top-level `candidate_not_active`, no registered schedules,
   and `setup.next_permitted_action` before doing anything else.
4. Confirm this workspace contains one course only and ask the minimum intake
   questions needed for source, assessment, rights, tool/egress, and audience
   boundaries.
5. Before Gate 0, inspect only file paths, types, sizes, hashes, lecturer-supplied
   classifications, and filename-based security candidates. Do not perform
   specialist content analysis.
6. Prepare and verify the source manifest and versioned source-access policy.
   Request review before every terminal command and before writing any control
   record.
7. Present the exact workspace, manifest and policy lineage, classifications,
   exclusions, capabilities, egress, audiences, unresolved questions, and the
   one next permitted action.
8. Stop and wait for explicit matching Gate 0 approval. Do not begin Gate 1,
   activate a runtime, register a schedule, or use external tools.
