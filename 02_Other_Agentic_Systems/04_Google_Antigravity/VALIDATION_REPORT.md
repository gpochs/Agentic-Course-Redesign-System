# Validation report — Google Antigravity adapter v0.2.3

- Date: 2026-08-21
- Status: PASS for static files, canonical schema-8 parity, fail-closed
  controls, installer behaviour, and local Python tests
- Runtime status: `candidate_not_active`; configuration only and not activated
- Antigravity access: not opened, installed, accessed, or signed into
- Provenance: approved inactive proposal `ACR-SYS-20260821-005`, version
  `0.2.3`, reconciled against `03_Shared_Workflow_Core`
- External effects: no runtime, schedule, hook, MCP server, connector,
  authentication, permission, plugin, or external egress added

## Final evidence

| Check | Result |
|---|---|
| Required adapter paths | PASS: 24 required paths |
| Release identity | PASS: top-level platform `google-antigravity`, adapter version `0.2.3`, status `candidate_not_active` |
| Native customization layout | PASS: 3 rules, 4 workflows, 6 Agent Skills, 10 project-local custom subagents |
| Course independence | PASS: the adapter adapts to lecturer-supplied context, level, learners, objectives, assessment, language, and constraints without assuming a discipline or institution |
| Gate 0A processing eligibility | PASS: no source path, filename, list, content, copy, or hash may be disclosed or accessed before a fingerprinted eligibility decision; public availability alone is insufficient; mixed or uncertain material fails closed |
| Restricted-material routing | PASS: institution-internal or restricted material is route-only unless an exact institution-approved environment, scope, and expiry are recorded; route-only handling prohibits source-detail leakage |
| Workflow completeness | PASS: Gate 0A through HITL 3; explicit requested/declined system-improvement response; terminal `complete_dormant` closeout; fresh-run-only manual or scheduled triggers |
| Canonical shared parity | PASS: declared shared files, state validator, and both preview migrations match the canonical core where mirrored |
| Migration safety | PASS: schema 6 to 7 and schema 7 to 8 migrations are preview-only; schema-8 input is idempotent; material eligibility, nonterminal runs, and schedules require reconfirmation after schema-7 migration |
| Schema-8 lineage | PASS: eligibility fingerprint is bound into source policy, run contracts, specialist returns, retry history, activation, and schedule checks |
| Dormant lifecycle | PASS: silence remains waiting; accepted runs close only after an explicit improvement response; terminal runs clear `active_run_id`, never resume, and require a fresh trigger and lineage |
| Automation guidance boundary | PASS: one informational manual/optional-automation guidance offer registers or triggers nothing |
| Custom-agent safety | PASS: exact ten-role roster; subagent-only; selected-model inheritance; tools exactly `view_file` and `grep_search`; command execution and MCP inheritance off; prompts forbid writes and egress |
| Skill/workflow frontmatter | PASS: names match folders; descriptions present |
| Documented file-size limits | PASS: every rule and workflow is below 12,000 characters |
| Static syntax | PASS: adapter JSON and Python parse |
| Source provenance | PASS: 12 declared canonical source hashes live-reverified against `03_Shared_Workflow_Core` |
| Adapter integrity | PASS: 57 generated non-manifest files hashed in `adapter-manifest.json`; the manifest excludes only itself |
| Secret and personal-path scan | PASS: 0 findings |
| Course-specific pilot leakage | PASS: 0 findings |
| Active privileged customization scan | PASS: no overlay hook, MCP config, plugin, `_agents/plugins`, or `.codex` path |
| Optional privileged examples | PASS: outside overlay; hook disabled; MCP server disabled with all tools withheld |
| Inactive state | PASS: schema 8, `candidate_not_active`, no schedules, automatic activation forbidden |
| Gate/write boundaries | PASS: Gate 2B research-only; Gate 3 typed material targets; one-retry ceiling retained |
| Embedded state validator | PASS: Gate 0A, lineage, handoff, HITL 3, explicit improvement response, dormant closeout, trigger, activation, and schedule schema validates with no errors |
| Installer preview | PASS: preview-only by default, no overwrite, no activation, and no global configuration change |
| Installer apply/no-overwrite | PASS in disposable temporary directories |
| Unit tests | PASS: 17 tests |

## Commands

Run from this adapter directory with Python 3. Supplying `--source-root` performs
the live canonical-source hash check used for this report:

```text
python -B validation/validate_adapter.py --source-root ../../03_Shared_Workflow_Core
python -B -m unittest discover -s validation -p "test_*.py" -v
python -B workspace-overlay/.agents/skills/course-redesign-setup/scripts/validate_state.py workspace-overlay/01_Control/state.json
python -B workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v6_to_v7.py <schema-6-state.json>
python -B workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v7_to_v8.py <schema-7-or-8-state.json>
python -B scripts/install_workspace_overlay.py --target "C:\CourseProjects\ExampleCourse\Year1"
```

Both migration commands print preview reports and cannot apply or write a
candidate. The final static validator returned:

```json
{
  "ok": true,
  "errors": [],
  "warnings": [],
  "checks": {
    "required_paths": 24,
    "skills": 6,
    "workflows": 4,
    "workflow_completeness_controls": 5,
    "rules": 3,
    "agents": 10,
    "secret_findings": 0,
    "source_hashes": 12,
    "generated_hashes": 57,
    "adapter_files": 58
  }
}
```

## Validation boundary

These checks prove repository layout, declared content hashes, static safety
invariants, disabled privileged examples, schema/migration parity, and installer
behaviour. They do not prove that a specific Antigravity IDE build discovers or
obeys every instruction, persists a rule activation mode, or enforces a gate at
runtime. They do not activate a runtime or register, alter, or trigger a
schedule. Any future activation or schedule remains a separate explicit gated
decision. Platform limitations and required app-side verification are recorded
in `OFFICIAL_LIMITATIONS.md`.
