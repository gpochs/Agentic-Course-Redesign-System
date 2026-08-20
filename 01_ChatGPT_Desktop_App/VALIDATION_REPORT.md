# Validation report — v0.2.1

- Candidate: `agentic-course-redesign` `0.2.1`
- Proposal: `ACR-SYS-20260820-003`
- Status: locally validated candidate; not activated
- Validation date: 2026-08-20
- Public repository:
  <https://github.com/gpochs/Agentic-Course-Redesign-System>
- OpenAI submission/review/publication status: not submitted, not reviewed, not
  approved, and not in the universal Plugins Directory

## Validated-source preservation

The v0.1.0 source remained read-only. Its 66-file deterministic aggregate
SHA-256 was measured before and after this implementation and matched exactly:

`A2F550A08D602156C15281C777AB0BFE1681665C061275AB7C87BE2A13CCCD7C`

The original validated workflow and all ten specialist definitions remain
preserved. Version `0.2.1` updates release metadata, template version fields,
portable distribution controls, and the orchestrator's user-facing metadata
and entry routing. The orchestrator is now the **Agentic Course Redesign**
umbrella choice and can route a new course to protected setup without changing
the established gates or specialist boundaries.

## Local validation results

| Check | Result |
|---|---|
| Official plugin-structure validator | PASS for custom marketplace plugin and separate OpenAI source |
| Official installed quick skill validator | PASS for all six skills in both trees: 12 checks |
| Static format parsing | PASS: 12 JSON, 22 TOML, 12 YAML, 19 Python, 4 SVG |
| Unit tests | PASS: 17 tests, including umbrella-entry and every inherited test |
| State validator | PASS: `candidate_not_active`, no schedule, no errors |
| Disposable forward test | PASS: 32 checks covering the umbrella, skills, agents, lineage, gates, setup, hashing, tamper rejection, and scrub |
| Public source scrub | PASS: 6 custom skills, 6 public skills, 10 custom agents, 10 public agents, no findings |
| OpenAI-source validation | PASS: 51 files, one manifest, exact six skills, no MCP/app/hook/screenshots, valid 512-square SVG assets |
| Runtime source synchronisation | PASS: custom and public runtime trees byte-identical |
| Reviewer material | PASS: three starter prompts, seven positive and six negative complete cases |
| Portable workshop build | PASS: deterministic ZIP, inventory, sidecar, CRC, safe paths, and package validator |
| Skills-only OpenAI build | PASS: deterministic ZIP, one top-level plugin root, 51 files, sidecar, and source-hash match |

The installed official validator scripts required PyYAML, which was absent from
the active Python environment. PyYAML 6.0.3 was installed only in a target-local
validation folder, the official checks were rerun successfully, and that local
dependency folder was moved under ignored `dist/local-validation/`. It is
excluded from both inventories and both release ZIPs.

## Commands

Run from the repository root with Python 3 and PyYAML available:

```text
python validation/public_scrub.py
python validation/validate_static_formats.py
python validation/validate_public_submission.py
python -m unittest discover -s plugins/agentic-course-redesign/tests -p "test_*.py" -v
python plugins/agentic-course-redesign/scripts/validate_state.py plugins/agentic-course-redesign/assets/project-template/01_Control/state.json
python validation/forward_test.py
python validation/run_official_validators.py
python validation/check_release_build.py
python validation/check_public_submission_build.py
```

The repository-root GitHub Actions workflow runs the cross-platform source
checks and deterministic Ubuntu release build. A duplicate workflow is
deliberately not shipped inside this subfolder because GitHub executes
workflows only from the repository root.

## Pre-publication verification

- Candidate commit and immutable `v0.2.1` tag: pending.
- Candidate GitHub Actions run: pending.
- User-level ChatGPT Desktop/Codex smoke test: pending the post-publication
  update from installed `0.2.0` to `0.2.1`. Structural validation confirms the
  packaged umbrella metadata; the report must not call the current picker
  verified until a new task loads the `0.2.1` cache.
- The clean Windows Git clone of `v0.2.0` exposed line-ending-dependent hashes
  in twelve Antigravity manifest records. System patch `v0.2.1` fixes the
  checkout rules and adds the umbrella picker entry without changing the gated
  workflow semantics, permissions, or activation boundary.
- Immutable tag, release downloads, checksums and successful fresh-clone
  evidence remain pending for the GitHub `v0.2.1` release. When complete, those
  checks will not imply an OpenAI universal-directory listing or installation
  for other users.

## Residual limits and owner blockers

- Local validation proves package structure and the tested workflow controls;
  it does not prove that an attendee's current account, workspace policy, or app
  build exposes a custom marketplace or permits installation.
- OpenAI documentation says `@` can invoke a plugin or bundled skill. The tested
  Desktop build flattened this skills-only plugin, so the same display name is
  applied to its orchestrator as a reliable full-workflow choice; this does not
  guarantee that every build will render a separate parent-plugin row.
- Current OpenAI documentation supports repo marketplaces in Work mode and
  Codex in the ChatGPT desktop app. Some CLI builds may expose marketplace
  commands, but the tested Codex CLI `0.118.0` did not. Plugins are not
  supported in the Codex IDE extension.
- The Windows project-template fallback was inherited from the validated source.
  The macOS guide remains structurally reviewed but was not executed on macOS in
  this run.
- Validation did not activate a runtime or schedule, publish to a ChatGPT
  workspace, submit to OpenAI, or create a universal-directory release. GitHub
  repository and release publication were separately authorised.
- The verified publisher identity, owning OpenAI organization/project, Apps
  Management Write submitter, public website/support/privacy/terms URLs,
  countries/regions, and attestations remain owner-supplied.
- OpenAI skill safety/security scans and human review have not run. A local pass
  cannot predict review outcome or timing.
- OneDrive is cloud-synchronised rather than strictly local. Protected course or
  assessment material may be stored there only when authorised.

See `openai-submission/review/LISTING_METADATA_CHECKLIST.md` for the exact
unresolved fields and final submission sequence.
