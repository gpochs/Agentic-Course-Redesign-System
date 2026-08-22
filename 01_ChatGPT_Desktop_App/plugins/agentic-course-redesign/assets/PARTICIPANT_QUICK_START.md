# Participant quick start

## Before opening the agentic workspace

1. Choose one course. It may be school, vocational, professional, higher
   education or another explicitly described context. Never combine unrelated
   courses in one project.
2. Create a short isolated folder on a personal computer or lecturer-controlled
   storage. A personal OneDrive is cloud-synchronised, not strictly local; use
   it for protected or assessment material only when authorised.
3. Before naming, listing, opening, copying or hashing course sources, declare
   only the material category, processing environment, internal/restricted and
   student-data flags, sensitivity class, assessment-security class and
   handling authority for Gate 0A. Do not disclose source paths or filenames
   at this stage.
4. A personal/unmanaged environment may proceed only for privately owned or
   rightsholder-authorised material, or appropriately licensed/public material
   with explicit AI-processing authority. Public availability alone is not
   enough. Institution-internal/restricted material is route-only there; mixed
   or uncertain sets must be segregated or clarified first. A record awaiting
   reconfirmation does not permit intake.
5. An approved institutional environment requires its exact policy reference,
   approved scope and non-expired expiry.
6. Exclude student personal data, submissions, grades, credentials and secrets
   by default.
7. Select only the adapter for the platform you will use.

## In the project

1. Copy the adapter overlay and inactive course scaffold into the exact one-
   course folder using its preview-first instructions.
2. Answer one Gate-0A declaration at a time. Select factual declarations only
   if true; a blank, skipped or uncertain answer remains unresolved and fails
   closed. Preview the exact record with
   `scripts/create_material_processing_eligibility.py`, review its inferred
   outcome and canonical fingerprint, then explicitly approve rerunning the
   same arguments with `--apply`. The helper creates only
   `01_Control/material-processing-eligibility.json`, refuses overwrite, and
   needs no MCP server.
3. Only after Gate 0A permits processing, put copied current files in `00_Source_Materials/` and context in
   `00_Context/`.
4. Start a new task and say: `Set up an agentic redesign project for this one course.`
5. Review the generated paths and confirm that no existing file will be
   overwritten.
6. Review source hashes, classifications, processing rights, teacher-only
   assessment boundaries, permitted roles/tools/egress and output audiences.
7. Approve Gate 0 only when those exact records are correct.

## What follows

The system moves from course brief to five-perspective preliminary scan, HITL
1, deeper research and reconciliation, HITL 2, blueprint and exact-target
approval, gated production, independent QA and HITL 3. The first run is manual.
After HITL 3 and an explicit requested/declined system-review response, that
course run becomes complete and dormant. Reusable-system changes, activation,
a fresh manual trigger and an optional expiring schedule are separate decisions.

Installation alone never reads course files, uploads content, activates a
runtime or registers a schedule.

Throughout the redesign, the orchestrator asks one consequential question at a
time. A native card is used only when the live host tool contract can present
the complete mutually exclusive option set and a custom-answer path without
omission. If the control is unavailable or unsupported, its capacity is
unknown, or the complete set exceeds that capacity, the orchestrator asks the
same single question in ordinary chat with every valid numbered option plus
`Other - type your answer`, then waits. It never prunes, hides or combines valid
choices to fit a card. Every valid option
remains visible in long dependency-based chunks. You may split, merge, reorder
or rename any chunk, and you can edit each recap before a gate.
Recommendations are suggestions only and are never preselected. Exact gate
approval lines remain separate.
