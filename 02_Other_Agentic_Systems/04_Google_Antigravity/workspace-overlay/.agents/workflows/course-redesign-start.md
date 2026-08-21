---
description: Prepare Gate 0A and then the one-course Gate 0 boundary without activating a runtime or disclosing course sources before eligibility passes.
---

# Start a gated course-redesign run

1. Read root `AGENTS.md`, `PROJECT_SETUP.md`, `01_Control/GATES.md`, and
   `01_Control/state.json`.
2. Use the `course-redesign-setup` skill.
3. Verify schema 8, top-level `candidate_not_active`, no registered schedules,
   and `setup.next_permitted_action` before doing anything else.
4. Before asking for or inspecting any source path, filename, list, content, or
   hash, ask only the material and environment categories required by Gate 0A.
   Fingerprint the decision. Public availability alone is insufficient; route
   institution-internal/restricted material without source leakage and block
   mixed/uncertain material until segregated or clarified.
5. Only after Gate 0A permits this exact environment, confirm this workspace
   contains one course and ask the minimum intake questions needed for source,
   assessment, rights, tool/egress, and audience boundaries. Gate 0 may inspect
   paths, types, sizes, hashes, lecturer-supplied classifications, and filename-
   based security candidates, but may not perform specialist content analysis.
6. Prepare and verify the source manifest and versioned source-access policy.
   Request review before every terminal command and before writing any control
   record.
7. Present the exact workspace, eligibility, manifest and policy lineage, classifications,
   exclusions, capabilities, egress, audiences, unresolved questions, and the
   one next permitted action.
8. Stop and wait for explicit matching Gate 0 approval. Do not begin Gate 1,
   activate a runtime, register a schedule, or use external tools.
