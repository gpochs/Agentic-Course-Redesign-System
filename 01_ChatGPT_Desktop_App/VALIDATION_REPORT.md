# Validation report — v0.2.3 release source

- Release source: `agentic-course-redesign` `0.2.3`
- Proposal: `ACR-SYS-20260821-005`
- Validation date: 2026-08-21
- Base release: published and separately installed `v0.2.2`
- Runtime-template status: locally validated, `candidate_not_active`,
  `submission_ready=false`
- Repository status: authorised for exact-version commit, publication and
  installation; universal-directory submission remains separate

## Scope and canonical parity

This report covers only `01_ChatGPT_Desktop_App/**`. The frozen shared core is
the semantic source of truth for the project template, scripts, participant
quick start, and exactly six skills.

- Shared core to custom plugin: PASS, 30/30 canonical files byte-identical.
- Custom plugin to OpenAI source mirror: PASS, 52/52 runtime files
  byte-identical.
- Public source: 54 files including the public-only licence and notice files.
- Skill count: exactly six in both plugin trees.
- Runtime defaults: `candidate_not_active` and `schedules=[]`.

| Canonical file | Bytes | SHA-256 |
|---|---:|---|
| `state.json` | 61,104 | `931E7C22F62B015846D4F2CD30C4434010111144B0E8C8477C69FFB4E91E0E78` |
| `material-processing-eligibility.template.json` | 2,595 | `EFE8B8D8D6E7BA3CD9B0DC21E1F014AD65206AAA609468555974949E4496FBED` |
| `migrate_state_v7_to_v8.py` | 27,496 | `9C84FF55367319DFE8E406D85CFB6768C46F273096E79F3EE74E5C1589D5A52A` |
| `source_manifest.py` | 18,019 | `4E8B0E89BD53D4966987B816B8DF7AE57C831A736B71C934A8BD10B82556767C` |
| `validate_state.py` | 154,885 | `0CA9EBAF4E63C95411712C55060FB18128879B1E60BC4B8A43B3F7E31052ED55` |

## Behaviour verified

- Gate 0A is a hard pre-source boundary. The implementation validates material
  ownership or licence, explicit AI-processing authority, environment approval,
  sensitivity, student-data presence, and assessment security before any course
  source path is requested, resolved, listed, copied, read, or hashed.
- Public accessibility alone is insufficient. Private or rightsholder-authorised
  material and appropriately licensed/public material with explicit processing
  authority can proceed; mixed or uncertain material fails closed; restricted
  institutional material in a personal/unmanaged environment is route-only.
- Approved institutional processing requires an exact environment reference,
  policy reference, scope, and expiry.
- The adaptive contract supports course material across subject, educational
  level, programme, language, assessment, delivery, and lecturer constraints.
- Schema 8 binds the material-processing-eligibility fingerprint through source
  policy, run lineage, trigger, and schedule contracts.
- The v7-to-v8 helper is preview-only, never writes its input, preserves valid
  terminal run and inactive schedule history using canonical indexed SHA-256
  receipts, and requires reconfirmation before nonterminal continuation or a
  future schedule trigger.
- After verified production handoff and HITL 3 acceptance, the workflow asks the
  complete system-improvement question and waits for an explicit requested or
  declined response. Silence remains waiting. A response closes the run as
  `complete_dormant`; that run cannot resume.
- One post-closeout guidance offer may explain a fresh manual trigger or optional
  schedule setup. It is informational only and never registers or triggers
  anything. Every later trigger creates a fresh run.

## Final local validation

| Check | Result |
|---|---|
| Custom and public schema-8 state validators | PASS: no errors |
| Plugin unit tests | PASS: 25/25 |
| Disposable forward test | PASS: 42/42 |
| Public source scrub | PASS: 152 scoped files, no findings |
| OpenAI-source validation | PASS: 40/40; 12 positive and 11 negative cases |
| Static format parsing | PASS: 14 JSON, 22 TOML, 12 YAML, 24 Python, 4 SVG |
| Official plugin and quick-skill validators | PASS: 14/14 across both plugin trees |
| Direct official custom-plugin validator | PASS |
| Shared-core parity | PASS: 30/30 |
| Runtime/public mirror parity | PASS: 52/52 |
| Whitespace validation | PASS: `git diff --check -- 01_ChatGPT_Desktop_App` |
| Runtime defaults | PASS: inactive, no schedules |
| Privilege surface | PASS: no MCP/app/hook/provider-auth/permission/schedule payload |

The unchanged marketplace record retains the pre-existing
`policy.authentication: ON_INSTALL` host install-policy metadata. It is not a
bundled authentication provider, credential surface, or provider-auth payload.
No MCP server, app, connector, hook, account sign-in, API key, permission grant,
runtime activation, or schedule was added.

The official validator scripts used the existing ignored local PyYAML dependency
folder under `dist/local-validation`. Nothing was installed and no network
service or account was added. All Python runs used `-B` and
`PYTHONDONTWRITEBYTECODE=1`; no generated cache remains in the source scope.

## Reproduction commands

Run from the repository root with Python 3:

```text
python -B 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/scripts/validate_state.py 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/assets/project-template/01_Control/state.json
python -B -m unittest discover -s 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/tests -p "test_*.py" -v
python -B 01_ChatGPT_Desktop_App/validation/forward_test.py
python -B 01_ChatGPT_Desktop_App/validation/public_scrub.py
python -B 01_ChatGPT_Desktop_App/validation/validate_public_submission.py
python -B 01_ChatGPT_Desktop_App/validation/validate_static_formats.py
python -B 01_ChatGPT_Desktop_App/validation/run_official_validators.py
```

For the official/static validators, `PYTHONPATH` points at the existing
`dist/local-validation/official-validator-deps/packages` folder.

## Current release boundary and residual limits

The installed `v0.2.2` base separately passed a post-restart fresh-task picker,
umbrella-entry, and all-six-skills smoke test. That is base-release evidence, not
proof that `v0.2.3` has been installed.

The `v0.2.3` release source is complete and validated. These remain separate
actions from repository publication:

- install or activate `v0.2.3` and run its fresh-task picker smoke test;
- submit the OpenAI source after publisher identity, organisation, legal/support
  pages, territories, attestations, safety scans, review, and owner approval;
- configure any optional schedule through its separate course-specific gates.

No course-material file was read or changed during this system implementation.
Rollback remains the preserved `v0.2.2` release and does not rewrite its tag,
delete course projects, or erase run or schedule history.
