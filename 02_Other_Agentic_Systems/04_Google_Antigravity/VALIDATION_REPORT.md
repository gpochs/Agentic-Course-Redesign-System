# Validation report — Google Antigravity adapter v0.2.0

- Date: 2026-08-20
- Status: PASS for static files, provenance, fail-closed controls, installer, and
  local Python tests
- Runtime status: `candidate_not_active`; configuration only and not activated
- Antigravity access: not opened, installed, accessed, or signed into
- Provenance: workflow semantics derive from validated base v0.1.0
- Source handling: validated base v0.1.0 read only

## Final evidence

| Check | Result |
|---|---|
| Required adapter paths | PASS: 16 required paths |
| Release identity | PASS: top-level platform `google-antigravity`, adapter version `0.2.0`, status `candidate_not_active` |
| Semantic provenance | PASS: adapter v0.2.0 declares workflow semantics derived from validated base v0.1.0 |
| Native customization layout | PASS: 3 rules, 4 workflows, 6 Agent Skills, 10 project-local custom subagents |
| Custom-agent safety | PASS: exact ten-role roster; subagent-only; selected-model inheritance; tools exactly `view_file` and `grep_search`; command execution and MCP inheritance off; no MCP servers or plugins; prompts forbid writes and egress |
| Skill/workflow frontmatter | PASS: names match folders; descriptions present |
| Documented file-size limits | PASS: every rule and workflow is below 12,000 characters |
| Static syntax | PASS: adapter JSON and Python parse |
| Source provenance | PASS: 42 selected source files live-rehashed with SHA-256 against the supplied read-only v0.1.0 source |
| Adapter integrity | PASS: 54 generated files hashed in `adapter-manifest.json`; the manifest excludes only itself |
| Secret and personal-path scan | PASS: 0 findings |
| Course-specific pilot leakage | PASS: 0 findings |
| Active privileged customization scan | PASS: no overlay hook, MCP config, plugin, `_agents/plugins`, or `.codex` path |
| Optional privileged examples | PASS: outside overlay; hook disabled; MCP server disabled with all tools withheld |
| Inactive state | PASS: schema 6, `candidate_not_active`, no schedules, automatic activation forbidden |
| Gate/write boundaries | PASS: Gate 2B research-only; Gate 3 typed material targets; one-retry ceiling retained |
| Source state validator | PASS: no errors |
| Installer preview | PASS: 43 overlay files, 0 conflicts, no write, no activation, no global configuration change |
| Installer apply/no-overwrite | PASS in disposable temporary directories |
| Unit tests | PASS: 8 tests |

## Commands

Run from this adapter directory with Python 3. For live source-provenance
verification, substitute the exact supplied read-only source root:

```text
python validation/validate_adapter.py --source-root <validated-v0.1.0-source-root>
python -m unittest discover -s validation -p "test_*.py" -v
python workspace-overlay/.agents/skills/course-redesign-setup/scripts/validate_state.py workspace-overlay/01_Control/state.json
python scripts/install_workspace_overlay.py --target "C:\CourseProjects\ExampleCourse\Year1"
```

The final static validator result is:

```json
{
  "ok": true,
  "errors": [],
  "warnings": [],
  "checks": {
    "required_paths": 16,
    "skills": 6,
    "workflows": 4,
    "rules": 3,
    "agents": 10,
    "secret_findings": 0,
    "source_hashes": 42,
    "generated_hashes": 54,
    "adapter_files": 55
  }
}
```

## Validation boundary

These checks prove the repository layout, content hashes, static safety
invariants, disabled privileged examples, source lineage, and installer
behaviour. They do not prove that a specific Antigravity IDE build discovers or
obeys every instruction, persists a rule activation mode, or enforces a gate at
runtime. Those limitations and the required app-side verification are recorded
in `OFFICIAL_LIMITATIONS.md`.
