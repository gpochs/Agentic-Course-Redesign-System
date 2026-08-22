# Validation report — inactive ChatGPT/OpenAI v0.2.4 candidate

- Proposal: `ACR-SYS-20260822-007`
- Candidate version: `0.2.4`
- Validation date: 2026-08-22
- Scope: `01_ChatGPT_Desktop_App/**`
- Base and rollback source: published and operational `v0.2.3`
- Candidate state: validated, inactive, `submission_ready=false`

OpenAI v0.2.3 is already published. This report does not claim that v0.2.4 has
been committed, uploaded, published, installed, enabled or activated. A later
authorised OpenAI update should use the existing plugin page's **Upload** route
to create a v0.2.4 draft while v0.2.3 remains published. Do not delete or
unpublish v0.2.3 first.

## Scope and parity

The stable shared core is the semantic source for the project template,
scripts, participant quick start and exactly six skills.

- Shared core to custom runtime: PASS, 31/31 mapped files byte-identical.
- Shared core to OpenAI source: PASS, 31/31 mapped files byte-identical.
- Custom runtime to OpenAI runtime: PASS, 53/53 files byte-identical.
- OpenAI source: 55 files including the public-only licence and notice files.
- Skill count: exactly six in each runtime tree.
- Agent count: exactly ten in each project-template mirror.
- Runtime defaults: `candidate_not_active` and `schedules=[]`.

| File | SHA-256 |
|---|---|
| `.codex-plugin/plugin.json` | `FF2C41201BF9BE1AD029DA2F08CCDE00410BD0BE9C1B73283046F94BAB6A9D91` |
| `assets/project-template/01_Control/state.json` | `5AFBFADB8F6C7404AC100EB1614A52CDDC14B662704B0EF9E67D2F69920C85AB` |
| `scripts/create_material_processing_eligibility.py` | `45540D84DE61E6300D4A98C301ABD1BD3A27491AD65CED6A5DAA4A3E6AFA27AC` |

Both manifests identify the published developer as `GIAN PETER OCHSNER`, use
the repository root as `interface.websiteURL`, and pin
`interface.privacyPolicyURL` and `interface.termsOfServiceURL` to v0.2.4. No
support URL was invented.

## Interaction-only behaviour verified

- Every human-in-the-loop decision keeps one unresolved consequential question
  in view.
- A host card is permitted only when the live host tool contract can present
  the complete option set plus a custom answer. The current verified Codex
  `request_user_input` contract is available only in Plan mode, permits exactly
  two or three explicit options, and the client adds free-form `Other`. Outside
  Plan mode the card is unavailable and the complete ordinary-chat fallback
  applies. Public OpenAI documentation does not
  currently document the widget cardinality, and Work's exact maximum is not
  independently documented or exposed here.
- If card capacity is unknown, unavailable or exceeded, the same single
  question is asked in ordinary chat with every valid numbered option plus
  `Other - type your answer`, followed by a wait. Valid choices are never
  pruned, hidden or combined merely to fit a card.
- Long decisions are clustered only by real dependencies and keep every valid
  option visible. The lecturer may split, merge, reorder or rename a cluster.
- Custom answers are preserved verbatim, interpreted explicitly and included
  in an editable recap.
- Only the safest truthful, evidence-aligned and reversible option may be
  labelled `Recommended`; factual choices say `select only if true`.
- Blank or skipped required questions stay unresolved and fail closed.
- Gate meanings, approval tokens, specialist authority, substantive choices,
  state schema 8 and lifecycle transitions are unchanged.

The deterministic Gate-0A helper produces a canonical preview, writes only the
exact approved eligibility-record target on `--apply`, and refuses overwrite.
It also rejects a redirected or symbolic-linked `01_Control` directory and
revalidates the output parent before writing. It adds no plugin, tool, MCP
server, permission or runtime integration.

## Scoped validation results

| Check | Result |
|---|---|
| Custom and public schema-8 state validation | PASS: 2/2, no errors |
| Plugin unit suite | PASS: 28 passed; one symlink test skipped because this Windows account lacks symlink privilege |
| Disposable forward test | PASS: 46/46 |
| OpenAI source and review validation | PASS: 50/50; 55 files; 15 positive and 12 negative cases |
| Public source scrub | PASS: 157 scoped files; six plus six skills; ten plus ten agents; zero findings |
| Static format parsing | PASS: 14 JSON, 22 TOML, 12 YAML, 26 Python, 4 SVG |
| Official plugin and quick-skill validators | PASS: 14/14 across both plugin trees |
| Shared-core mapped parity | PASS: 31/31 in both mirrors |
| Runtime/public mirror parity | PASS: 53/53 |
| Deterministic OpenAI skills-only build | PASS: 5/5; 55 archive files |
| Deterministic portable bundle build | PASS: deterministic ZIP, inventory, sidecar and bundle validation |
| Whitespace validation | PASS: `git diff --check -- 01_ChatGPT_Desktop_App` |

The deterministic OpenAI candidate archive generated in the ignored local
`dist/` directory has SHA-256
`C4FBE1FB6E2783F6E8F9D4F520C6416712D0D6F463DB01461BCA24E5285EFBD3`.
It was validated but not uploaded, published, installed or copied to any
external staging folder.

The official and static validators used an existing ignored local PyYAML
dependency through `PYTHONPATH`; nothing was installed. UTF-8 mode and bytecode
suppression were enabled so canonical punctuation is parsed consistently on
Windows and no source cache is generated.

## Privilege and lifecycle boundary

The candidate contains no MCP server, app, connector, hook, provider
authentication, permission grant, telemetry, external-egress default, schedule
payload or automation registration. The marketplace's pre-existing
`policy.authentication: ON_INSTALL` value is host install-policy metadata, not
a bundled provider-authentication surface. The public package contains no
registered schedule.

No course-material path was requested, read, copied, hashed or changed during
this implementation. No course run or schedule was started. Publication,
installation and activation remain separate later decisions, as do publisher
attestations, final safety scans and live picker smoke testing.

## Reproduction commands

Run from the repository root with Python 3 and bytecode disabled:

```text
python -B 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/scripts/validate_state.py 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/assets/project-template/01_Control/state.json
python -B -m unittest discover -s 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/tests -p "test_*.py" -v
python -B 01_ChatGPT_Desktop_App/validation/forward_test.py
python -B 01_ChatGPT_Desktop_App/validation/public_scrub.py
python -B 01_ChatGPT_Desktop_App/validation/validate_public_submission.py
python -B 01_ChatGPT_Desktop_App/validation/validate_static_formats.py
python -B 01_ChatGPT_Desktop_App/validation/run_official_validators.py
python -B 01_ChatGPT_Desktop_App/validation/check_public_submission_build.py
python -B 01_ChatGPT_Desktop_App/validation/check_release_build.py
```

The two YAML-dependent commands require PyYAML on `PYTHONPATH`. On Windows,
set `PYTHONUTF8=1`; set `PYTHONDONTWRITEBYTECODE=1` for every command.
