# Validation report — inactive OpenAI/Codex v0.2.5 candidate

- Proposal: `ACR-SYS-20260825-009`
- OpenAI/Codex package: `0.2.5`
- Base workflow: Agentic Course Redesign System `0.2.4`
- Validation date: 2026-08-25
- Scope: description-only cross-renderer compatibility maintenance
- Rollback source: published and installed OpenAI/Codex `0.2.4`
- Candidate state: validated, inactive, `submission_ready=false`

This report does not claim that v0.2.5 has been committed, pushed, tagged,
released, uploaded, published, installed, enabled or activated. OpenAI/Codex
v0.2.4 remains the live rollback source. A later authorised update should use
the existing plugin page's **Upload** route to create a v0.2.5 draft while
v0.2.4 remains published; unpublishing v0.2.4 first is neither required nor
recommended.

## Change and preservation result

The candidate replaces Markdown-dependent list markers in the public long
description with five visible `◆` section separators and fifteen `•` item
separators. The structure therefore remains visible in both clients that
preserve line breaks and clients that collapse whitespace. The wording and
claims remain unchanged: lecturer control, all ten specialist roles, every
listed gate and HITL stage, decision-dialogue rules and the no-automation and
no-permission boundary are all present in the whitespace-collapsed form.

The package version and version-mirrored OpenAI review records are `0.2.5`.
The embedded project template and shared workflow remain `0.2.4`; no schema or
runtime migration was introduced. The custom-runtime and public-submission
manifests are byte-identical.

All twelve files across the six skill trees (each tree's `SKILL.md` and
`agents/openai.yaml`) match their fixed v0.2.4 SHA-256 baselines in both the
custom-runtime and public-submission trees. No file under the shared core,
GitHub Copilot package or marketplace, Claude Code, OpenCode, Antigravity,
course-project templates, or course materials was changed.

## Interaction contract preserved

- One unresolved consequential question is presented at a time.
- A card is used only if the live host can display every valid choice plus a
  custom answer. The current verified Codex `request_user_input` contract is
  available only in Plan mode, permits exactly two or three explicit choices,
  and the client adds free-form `Other`. Outside
  Plan mode the card is unavailable and the complete ordinary-chat fallback
  applies. Work's exact maximum is not independently documented.
- If card capacity is unknown, unavailable or exceeded, the complete
  ordinary-chat fallback presents every valid numbered option plus
  `Other - type your answer`, then waits. Choices are never pruned, hidden or
  combined merely to fit a card.
- Longer decisions may use dependency-based clusters with every option
  visible. Custom answers remain verbatim and recaps remain editable.
- Gate meanings, approval tokens, specialist authority, substantive choices,
  schema 8 and lifecycle transitions are unchanged.

## Validation evidence

| Check | Result |
|---|---|
| Public source scrub | PASS: 161 scoped files, six plus six skills, ten plus ten agents, zero findings |
| Static format parsing | PASS: 14 JSON, 22 TOML, 12 YAML, 26 Python and 4 SVG files |
| Public submission validation | PASS: 55 source files, exactly six skills, 15 positive and 12 negative reviewer cases, fixed v0.2.4 skill-tree hash locks |
| Official local plugin validator | PASS for both the custom-runtime and public-submission plugin roots |
| Plugin unit suite | PASS: 29 tests; one expected Windows symlink-privilege skip |
| Template state validation | PASS: schema 8, workflow/plugin base `0.2.4`, inactive defaults and no schedule |
| Disposable forward test | PASS with package `0.2.5` and base workflow `0.2.4` separated correctly |
| Repository validator | PASS: 392 source files, six shared skills, five adapter manifests, zero findings |
| Full repository unit suite | PASS: 97 tests |
| Deterministic OpenAI skills-only build | PASS: two independent 55-file archives are byte-identical |
| Whitespace validation | PASS: no `git diff --check` findings |

The two ignored local candidate archives have the same SHA-256:

`F10F789C5F7EA9E176C24D1D8ADF46A1AD753FFA9BA3BF86664BAD0CC151E749`

Validated archive filename:
`agentic-course-redesign-openai-skills-only-v0.2.5.zip`.

An existing ignored local PyYAML dependency was supplied through
`PYTHONPATH`; no dependency was installed. Python bytecode generation was
disabled. The candidate contains no generated cache files.

## Privilege and lifecycle boundary

The candidate adds no MCP server, app, connector, hook, provider
authentication, permission, telemetry, external egress, schedule, automation
or paid resource. It does not start a course run or alter any course material.
Publication, installation, activation, publisher attestations, portal review
and a fresh-task live picker smoke test remain separate later decisions.

## Reproduction commands

Run from the repository root with Python 3 and bytecode disabled. The
YAML-dependent validators require PyYAML on `PYTHONPATH`.

```text
python -B 01_ChatGPT_Desktop_App/validation/public_scrub.py
python -B 01_ChatGPT_Desktop_App/validation/validate_static_formats.py
python -B 01_ChatGPT_Desktop_App/validation/validate_public_submission.py --archive <candidate-zip>
python -B -m unittest discover -s 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/tests -p "test_*.py" -v
python -B 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/scripts/validate_state.py 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/assets/project-template/01_Control/state.json
python -B 01_ChatGPT_Desktop_App/validation/forward_test.py
python -B 05_Validation/validate_repository.py
python -B -m unittest discover -s 05_Validation/tests -p "test_*.py" -v
python -B <plugin-creator>/scripts/validate_plugin.py 01_ChatGPT_Desktop_App/plugins/agentic-course-redesign
python -B <plugin-creator>/scripts/validate_plugin.py 01_ChatGPT_Desktop_App/openai-submission/source/agentic-course-redesign
```
