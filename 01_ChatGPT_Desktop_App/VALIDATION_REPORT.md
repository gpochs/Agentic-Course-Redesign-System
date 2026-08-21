# Validation report — v0.2.2 release source

- Candidate: `agentic-course-redesign` `0.2.2`
- Proposal: `ACR-SYS-20260820-004`
- Status: locally validated repository release source with disposable
  validation bundles; publication does not install, activate, or schedule it
- Validation date: 2026-08-21
- Base release: public `v0.2.1`
- OpenAI submission/review/publication status: not submitted, not reviewed, not
  approved, and not in the universal Plugins Directory

## Candidate scope and canonical parity

This report covers the ChatGPT Desktop/Codex implementation and its separate
OpenAI skills-only source under `01_ChatGPT_Desktop_App/**`. The full proposal
also covers the shared core and every other platform adapter; repository-level
validation reports their combined result separately.

The final ChatGPT schema trio is byte-identical to the frozen shared core and to
the public runtime mirror:

| File | Bytes | SHA-256 |
|---|---:|---|
| `state.json` | 48,320 | `AC5B629FA4FA3ED10F959BAC547B9BA3BD5D30636C2F46EA36F30845F5352628` |
| `migrate_state_v6_to_v7.py` | 24,891 | `B280A883DD08A06BD89927F26F6FCC3C1816E9C77E1E4904A98194417CC13031` |
| `validate_state.py` | 77,949 | `4EBFDD48010C5355DB05B092832408210F4D722CF4CACC3CB16852779718DE80` |

The complete custom and public runtime trees (`.codex-plugin`, `assets`,
`scripts`, and `skills`) are byte-identical. Both contain exactly six skills.

## Local validation results

| Check | Result |
|---|---|
| Frozen schema-7 state validator | PASS: inactive, `schedules=[]`, no errors |
| Official plugin and quick-skill validators | PASS: 14/14 across both plugin trees |
| Static format parsing | PASS: 12 JSON, 22 TOML, 12 YAML, 22 Python, 4 SVG |
| SVG deterministic line-ending rule | PASS: all SVG sources use LF |
| Unit tests | PASS: 22/22 |
| Disposable forward test | PASS: 41/41 checks |
| Public source scrub | PASS: 145 scoped source files, no findings |
| OpenAI-source validation | PASS: 37/37 checks, 52 runtime files, exactly six skills |
| Reviewer material | PASS: three starter prompts, nine positive and eight negative cases |
| Runtime source synchronisation | PASS: custom and public runtime trees byte-identical |
| Privilege boundary | PASS: no MCP, app, hook, connector, authentication or permission manifest payload; no registered schedule |
| v6-to-v7 migration | PASS: preview-only, source unchanged, proposal validates, preservation checks pass |
| Final workflow sequence | PASS: declaration → separate exact handoff approval → verification → current-lineage HITL 3 → persisted one-time offer/response |
| Review authority | PASS: yes authorises read-only review and one versioned proposal only |
| Stale release-evidence guard | PASS: rejects the historical mismatched v0.2.1 report/archive pair |

The installed official validator scripts require PyYAML, which is absent from
the default interpreter. Validation reused the existing ignored
`dist/local-validation/official-validator-deps/packages` folder; no package was
installed and no account, connector or network service was added.

Generated Python bytecode was moved into the existing ignored
`dist/local-validation/` quarantine area and all final Python runs used
`PYTHONDONTWRITEBYTECODE=1`. No cache artefact remains in the source tree.

## Commands

Run from the repository root with Python 3. For the official/static validators,
point `PYTHONPATH` at the existing local PyYAML folder when present.

```text
python 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/scripts/validate_state.py 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/assets/project-template/01_Control/state.json
python -m unittest discover -s 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/tests -p "test_*.py" -v
python 01_ChatGPT_Desktop_App/validation/forward_test.py
python 01_ChatGPT_Desktop_App/validation/public_scrub.py
python 01_ChatGPT_Desktop_App/validation/validate_public_submission.py
python 01_ChatGPT_Desktop_App/validation/validate_static_formats.py
python 01_ChatGPT_Desktop_App/validation/run_official_validators.py
python 01_ChatGPT_Desktop_App/validation/validate_release_evidence.py --report <report.json> --archive <exact.zip> --expected-version <version>
```

Portable and skills-only ZIPs were built locally to test deterministic
packaging, checksums and archive validation. Only the exact archives selected
for the v0.2.2 GitHub release become release assets; ignored local copies remain
validation artifacts. Publication performs no installation, activation, or
schedule registration.

## Historical release-evidence limitation

The published v0.2.1 system archive is 490,203 bytes with SHA-256
`77F44DB57FB70A6FF6906AF4A5DC11E2EB115C68B0E78EBF01C7C0B882B7AE70`.
The attached `system-release-validation-v0.2.1.json`, however, records the
earlier v0.2.0 archive: 481,578 bytes and SHA-256
`257ADE8C2205306252CE0F9BBFDE149DDC5ACA794497EB9548F0A247F8369632`.
The live v0.2.1 GitHub release also reports `immutable=false`.

The new read-only evidence guard correctly returned failure for that mismatched
pair on archive name/version, byte count and SHA-256. Historical v0.2.1 files
were not modified. The v0.2.2 release must attach only its matching
exact-version evidence.

## Residual limits and later decisions

- Source validation and repository publication do not install v0.2.2 or prove
  picker behaviour for an installed runtime.
- The last verified pre-release user-level plugin was v0.2.1. Version v0.2.2
  requires its own supported installation and fresh-task picker check.
- OpenAI directory owner fields, legal/support URLs, territory choices,
  attestations, safety scans and review remain unresolved owner actions.
- Workspace policy, account access and app version may restrict a custom
  marketplace even when source validation passes.
- OneDrive is cloud-synchronised rather than strictly local; protected material
  may be stored there only when authorised.
- Repository publication, installation, runtime activation and schedule
  registration remain separate decisions. The release creates no installation,
  activation, or schedule.
