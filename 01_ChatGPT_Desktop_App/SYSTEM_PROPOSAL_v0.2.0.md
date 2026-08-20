# Reusable-system release proposal

- Proposal ID: `ACR-SYS-20260820-002`
- Proposal version: `0.2.0`
- Status: `candidate under local release validation; not activated`
- Evidence run: the completed pilot course-redesign run, including its three
  lecturer-in-the-loop decisions, production corrections and independent QA.
- Intended public repository (not yet published or confirmed live):
  `https://github.com/gpochs/Agentic-Course-Redesign-System`.

## Demonstrated problem

The successful course run required a repeatable way to isolate one course,
protect original and teacher-only sources, coordinate specialist perspectives,
reconcile cross-role consequences, pause for consequential lecturer decisions,
produce editable files, validate them independently, and improve the system
only after the run. A prompt pack alone cannot reliably enforce file lineage,
source policy, state, retry ceilings, output audiences or later schedule safety.

## Proposed candidate

Mechanically preserve the validated v0.1.0 skills-first workflow, then package
it as v0.2.0 for supported ChatGPT desktop and Codex surfaces:

- repository marketplace `.agents/plugins/marketplace.json`;
- plugin manifest under `plugins/agentic-course-redesign/.codex-plugin/`;
- six bounded skills for setup, orchestration, research, assessment, material
  production and post-run system management;
- onboarding asset, protected one-course project template, `AGENTS.md`, state
  schema, ten custom-agent definitions and folder guidance;
- setup, manifest, canonical-policy-fingerprint and state-validation scripts;
- positive/negative behavioural cases, unit tests and disposable forward test;
- Python-3-based Windows/macOS project-template setup guides; and
- deterministic workshop ZIP plus SHA-256 after final validation;
- square SVG logo and composer icon within public-directory limits;
- a separate, byte-matched OpenAI skills-only source tree with no MCP, app,
  hook, UI, screenshot or authentication payload;
- three listing prompts, six positive and six negative reviewer cases, release
  notes, and explicit owner-supplied submission blockers; and
- deterministic skills-only ZIP plus SHA-256 after final validation.

These are the exact candidate roots. No existing global skill, plugin, memory,
Benchmark workflow or protected course source is an edit target.

## Benefits

- The first dialogue feels like educational consulting after a short setup.
- All course-specific decisions remain with the lecturer.
- Current objectives and assessment evidence are core specialist inputs.
- Research, assessment, activity design, AI integration and learner experience
  are reconciled before production.
- Installation and guided use are separated from autonomous runtime activation
  and from scheduling.
- Attendees can use the documented repo marketplace in Work mode or Codex in
  the ChatGPT desktop app where workspace policy permits it, with a portable
  project-template fallback if custom installation is unavailable.
- Repository distribution and universal public-directory publication are
  stated as separate routes.

## Possible regressions and mitigations

- App/CLI versions may not expose marketplace installation: ship and test the
  portable setup route and do not promise one-click installation.
- The Windows route is functionally tested on the development machine; the
  macOS guide is structurally reviewed but not independently machine-tested.
- Long cloud-synchronised paths can break Office: instruct attendees to use a
  short project path and create short distribution copies.
- Generic rules can miss institution-specific grading, rights or accessibility:
  require lecturer-confirmed course context and keep unknowns explicit.
- More controls add setup effort: keep the setup conversational and ask only
  questions that change access or design.
- Custom agents may not be available on every surface: the orchestrator can use
  bounded in-task subagents or a serial fallback while retaining the gates.

## Validation and success criteria

The candidate may be called activation-ready only if:

1. plugin and all six skills pass their official local validators;
2. JSON, TOML, YAML and Python parse;
3. setup preview/apply/no-overwrite tests pass;
4. source manifest creation, verification and tamper rejection pass;
5. canonical policy fingerprints ignore only the declared approval metadata;
6. the template is one-course, inactive and has no schedule;
7. at least five positive and three negative cases exist;
8. a disposable forward test passes without touching course files;
9. package inventory and deterministic ZIP verification pass; and
10. independent review finds no course-specific content or answer-key leakage;
11. custom and public runtime trees are byte-identical; and
12. the skills-only ZIP has one plugin root and excludes MCP/app/hook/screenshots.

## Activation boundary

Validation does not activate this candidate. A later lecturer decision must
name proposal `ACR-SYS-20260820-002`, version `0.2.0`, the final validation
evidence, residual-risk record and rollback record, and explicitly choose
activation. Keeping it inactive or revising and revalidating are valid choices.
No schedule may be proposed until that separate activation is complete.

GitHub publication, OpenAI Platform upload, policy attestation, review, and
universal-directory publication are also separate owner actions. This proposal
authorises none of them.
