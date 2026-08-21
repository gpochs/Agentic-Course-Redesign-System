# Validation report — Google Antigravity adapter v0.2.2

- Date: 2026-08-21
- Status: PASS for static files, frozen schema-7 parity, fail-closed controls,
  installer behaviour, and local Python tests
- Runtime status: `candidate_not_active`; configuration only and not activated
- Antigravity access: not opened, installed, accessed, or signed into
- Provenance: current adapter contract v0.2.2 retains historical semantic
  provenance to validated base v0.1.0
- External effects: no runtime, schedule, hook, MCP server, connector,
  authentication, permission, plugin, or external egress added

## Final evidence

| Check | Result |
|---|---|
| Required adapter paths | PASS: 18 required paths |
| Release identity | PASS: top-level platform `google-antigravity`, adapter version `0.2.2`, status `candidate_not_active` |
| Historical semantic provenance | PASS: validated base/source provenance remains v0.1.0; current adapter candidate is v0.2.2 |
| Native customization layout | PASS: 3 rules, 4 workflows, 6 Agent Skills, 10 project-local custom subagents |
| Workflow completeness | PASS: Gate 0; production declaration; exact handoff approval and verification before HITL 3; persisted exactly-once post-HITL3 review offer; proposal-only authority; separate System Gate, activation, and schedule controls |
| Frozen shared parity | PASS: adapter state, state validator, and preview migration are byte-identical to final shared schema-7 files |
| Migration safety | PASS: schema 6 to 7 and already-schema-7 previews are non-mutating; no apply/write path; existing status, schedules, lineage, permissions/tools and activation records are preserved |
| Custom-agent safety | PASS: exact ten-role roster; subagent-only; selected-model inheritance; tools exactly `view_file` and `grep_search`; command execution and MCP inheritance off; no MCP servers or plugins; prompts forbid writes and egress |
| Skill/workflow frontmatter | PASS: names match folders; descriptions present |
| Documented file-size limits | PASS: every rule and workflow is below 12,000 characters |
| Static syntax | PASS: adapter JSON and Python parse |
| Source provenance | PASS: 42 historical source entries retained; this v0.2.2 adapter-only run did not live-reverify the optional external source root |
| Adapter integrity | PASS: 55 generated non-manifest files hashed in `adapter-manifest.json`; the manifest excludes only itself |
| Secret and personal-path scan | PASS: 0 findings |
| Course-specific pilot leakage | PASS: 0 findings |
| Active privileged customization scan | PASS: no overlay hook, MCP config, plugin, `_agents/plugins`, or `.codex` path |
| Optional privileged examples | PASS: outside overlay; hook disabled; MCP server disabled with all tools withheld |
| Inactive state | PASS: schema 7, `candidate_not_active`, no schedules, automatic activation forbidden |
| Gate/write boundaries | PASS: Gate 2B research-only; Gate 3 typed material targets; one-retry ceiling retained |
| Embedded state validator | PASS: complete lineage, handoff, HITL 3, offer/response, resume and System Gate schema validates with no errors |
| Installer preview | PASS: 44 overlay files, 0 conflicts, no write, no activation, no global configuration change |
| Installer apply/no-overwrite | PASS in disposable temporary directories |
| Unit tests | PASS: 15 tests |

## Commands

Run from this adapter directory with Python 3. The optional `--source-root`
performs a separate live check of the historical v0.1.0 source hashes:

```text
python validation/validate_adapter.py
python validation/validate_adapter.py --source-root <validated-v0.1.0-source-root>
python -m unittest discover -s validation -p "test_*.py" -v
python workspace-overlay/.agents/skills/course-redesign-setup/scripts/validate_state.py workspace-overlay/01_Control/state.json
python workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v6_to_v7.py <schema-6-state.json>
python scripts/install_workspace_overlay.py --target "C:\CourseProjects\ExampleCourse\Year1"
```

The migration command prints a preview report to standard output and cannot
apply or write the candidate. The final static validator run without the
optional historical source root returned:

```json
{
  "ok": true,
  "errors": [],
  "warnings": [
    "source root not supplied; recorded source hashes were not live-reverified"
  ],
  "checks": {
    "required_paths": 18,
    "skills": 6,
    "workflows": 4,
    "workflow_completeness_controls": 5,
    "rules": 3,
    "agents": 10,
    "secret_findings": 0,
    "source_hashes": 42,
    "generated_hashes": 55,
    "adapter_files": 56
  }
}
```

## Validation boundary

These checks prove the repository layout, content hashes, static safety
invariants, disabled privileged examples, schema/migration parity, and installer
behaviour. They do not prove that a specific Antigravity IDE build discovers or
obeys every instruction, persists a rule activation mode, or enforces a gate at
runtime. They also do not activate or register the requested May 31/December 31
schedule. Those actions remain separately gated after activation. Platform
limitations and required app-side verification are recorded in
`OFFICIAL_LIMITATIONS.md`.
