# Google Antigravity adapter for Agentic Course Redesign

Adapter version `0.2.3` is a project-local, course-independent inactive
candidate reconciled to shared candidate `ACR-SYS-20260821-005` v0.2.3. It
adapts to the lecturer-supplied subject, educational level, learners,
objectives, assessment, language, constraints, and material formats. It makes
pre-source Gate 0A, verified production handoff before HITL 3, durable schema-8
recovery, terminal `complete_dormant` closeout, and the proposal-only system-
review lifecycle explicit. It does not activate any runtime or schedule. It contains one complete
one-course workspace overlay with root `AGENTS.md`, native rules, slash
workflows, six Agent Skills, ten read-only custom subagents, source-integrity
helpers, and the inactive Gate/state scaffold.

Machine-readable release identity is exposed at the top level of
`adapter-manifest.json` as platform `google-antigravity`, adapter version
`0.2.3`, and status `candidate_not_active`.

It does **not** install or access Antigravity, change global configuration or
IDE permissions, activate a runtime, register a schedule, connect an MCP
server, enable a hook, install a plugin, upload files, or include course or
student data.

## One-course and storage boundary

Use one isolated workspace and one normal conversation per course. Store only
lecturer-controlled copies in `00_Source_Materials/` and authorised context in
`00_Context/`; keep originals elsewhere. A personal OneDrive is
cloud-synchronised rather than strictly local, so protected or assessment
material belongs there only when institutional, rights, privacy, and security
rules permit it. Exclude student personal data, submissions, grades,
credentials, and secrets by default.

## Safe installation

The `.agents` folder is nested under `workspace-overlay/` in this distribution
and is not intended to activate from the adapter repository root. Copy the
overlay contents into one exact new course-workspace root.

1. Review this README, `OFFICIAL_LIMITATIONS.md`, `adapter-manifest.json`, and
   every file under `workspace-overlay/`.
2. Choose a short, isolated empty folder for exactly one course. Do not choose a
   drive root, home folder, repository root, mixed-course folder, or an existing
   configured agent workspace.
3. From this adapter directory, preview all destinations without writing:

   ```text
   python scripts/install_workspace_overlay.py --target "C:\CourseProjects\Biology\Year2"
   ```

4. Review the exact resolved target, planned file list and hashes, existing
   entries, and conflicts. The default command never writes.
5. After explicitly confirming that exact target, apply once:

   ```text
   python scripts/install_workspace_overlay.py --target "C:\CourseProjects\Biology\Year2" --apply
   ```

   Use `--allow-nonempty` only after reviewing every existing top-level entry;
   it never permits overwriting an existing overlay path.
6. Verify the copied project before opening it:

   ```text
   python "C:\CourseProjects\Biology\Year2\.agents\skills\course-redesign-setup\scripts\validate_state.py" "C:\CourseProjects\Biology\Year2\01_Control\state.json"
   ```

7. Open only that copied course folder as the Antigravity IDE workspace. In the
   actual IDE, verify Request Review or Strict mode, workspace-only access,
   sandboxing where supported, browser restrictions, and the discovered rules,
   workflows, skills, and custom subagents. Confirm that each custom subagent
   exposes only `view_file` and `grep_search`. Do not enable global
   customizations or optional privileged examples.
8. Invoke `/course-redesign-start` before disclosing source paths or filenames.
   Review and fingerprint Gate 0A using only category-level declarations. Add
   authorised copies only after that gate permits this exact environment, then
   review Gate 0 before substantive protected-file reading or specialist
   analysis.

The installer is copy-only, verifies SHA-256 after each copy, and refuses
conflicts, broad targets, symlink targets, and targets within or above this
adapter. It performs no app action or runtime activation.

## Native adapter layout

- `workspace-overlay/AGENTS.md`: full trusted orchestration contract.
- `workspace-overlay/.agents/rules/`: trust, gate, lineage, and assessment
  security constraints.
- `workspace-overlay/.agents/workflows/`: start, continue, validate, and separate
  system-review slash workflows.
- `workspace-overlay/.agents/skills/`: six adapted Agent Skills; the orchestrator
  skill contains the shared specialist-role contracts and serial fallback.
- `workspace-overlay/.agents/agents/`: ten native, project-local specialist
  wrappers. Each is subagent-only, inherits the selected model, loads the
  orchestrator constraints, permits only `view_file` and `grep_search`, disables
  command execution and MCP inheritance, and has no MCP or plugin dependency.
- `workspace-overlay/01_Control/`: schema-8 inactive state, Gate-0A eligibility
  template, and gate templates.
- `workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v7_to_v8.py`:
  preview-only migration helper with no apply or write path.
- `optional-privileged-examples/`: disabled hook/MCP examples outside the
  overlay and all auto-discovery paths.
- `validation/`: static adapter checks and unit tests.

## Local validation

Run from this adapter directory with Python 3:

```text
python validation/validate_adapter.py
python -m unittest discover -s validation -p "test_*.py" -v
```

Validation checks required paths, skill/workflow and custom-agent frontmatter,
the exact ten-role roster, read-only agent tool allowlists, file-size limits,
manifest hashes, JSON and Python syntax, secret-like material, absence of active
hooks/MCP/plugins, inactive state, empty schedules, source/tool/egress controls,
Gate 2B/Gate 3 target boundaries, production-handoff-before-HITL3 order,
schema-8 Gate-0A, dormant-run, trigger-guidance, and proposal-only review-offer
controls, preview-only migration,
installer preview/apply/no-overwrite, and optional-example disablement. Static
PASS does not prove Antigravity runtime behaviour; see
`OFFICIAL_LIMITATIONS.md`.

## Source and licence

`adapter-manifest.json` records the actual SHA-256 values of the shared v0.2.3
canonical files used and every adapter output covered by integrity checks. The
shared source was read only. Adapted material remains under the included MIT
licence; third-party and data boundaries are in `THIRD_PARTY_NOTICES.md`.
