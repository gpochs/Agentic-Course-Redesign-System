# Agentic Course Redesign System

Version `0.2.1` is the released skills-only repository plugin for
lecturer-controlled, evidence-led course redesign. It is course-agnostic: each
run adapts to the
approved materials, learner context, institutional rules, and assessment system
for one course.

Public repository:
<https://github.com/gpochs/Agentic-Course-Redesign-System>.

The local source/package checks, public CI and fresh Windows clone pass. The
immutable tag, release assets and checksums are published with the GitHub
release. This package has **not been submitted to, reviewed by, approved by, or
published in OpenAI's universal Plugins Directory**.

## What is installable now

The checked-out or extracted repository is a valid custom marketplace source
for supported ChatGPT desktop surfaces. In Work mode or Codex in the ChatGPT
desktop app, a repo marketplace can appear as a selectable source in the Plugins
Directory. Some Codex CLI builds can configure a local or Git-backed
marketplace; use that route only when the installed CLI exposes marketplace
commands, then start a new session after installation.

Current OpenAI documentation says plugins work in Chat and Work across supported
ChatGPT surfaces and in Codex in the ChatGPT desktop app. The Codex IDE extension
does not support plugins. Workspace policy, product access, app version, and
administrator controls can still restrict installation or sharing.

See `INSTALLATION.md` for the local and public GitHub routes. A GitHub
repository can distribute this custom marketplace, but GitHub publication alone
cannot create a universal public-directory listing.

The release host currently has a verified user-level installation of version
`0.2.0`. The version `0.2.1` package structurally validates
`@Agentic Course Redesign` as the single full-workflow umbrella plus five direct
component entries; live picker evidence is recorded only after a new supported
Work/Codex task has loaded the `0.2.1` cache. On builds that flatten skills-only
plugins, the umbrella is the user-facing name of
`course-redesign-orchestrator`; it routes a new course to protected setup and an
existing course to its next verified gate.
That evidence does not establish availability for every app version, user,
device, account, workspace or the Codex IDE extension. The tested Codex CLI
`0.118.0` did not expose a marketplace command.

## Workflow

The plugin contributes six bundled skills: one umbrella entry plus five focused
component entries. Together they help a lecturer:

1. create one protected project and isolated folder per course;
2. classify and hash course, context, assessment, and teacher-only sources;
3. approve a versioned source-access policy and per-run contract;
4. run all five preliminary specialist perspectives before Gate 2A;
5. research only lecturer-approved focus areas;
6. reconcile evidence, feasibility, accessibility, workload, AI, and assessment;
7. approve only exact research targets at Gate 2B;
8. approve a blueprint and typed material targets separately at Gate 3;
9. produce one approved artefact at a time with independent QA;
10. accept, revise, or reject each output; and
11. consider reusable-system activation or scheduling only through later,
    exact-version decisions.

Installing the plugin does not activate a runtime, register a schedule, upload
course files, or grant blanket write access.

## Repository layout

- `.agents/plugins/marketplace.json`: custom repo marketplace for Work mode and
  Codex in the ChatGPT desktop app, and for CLI builds that expose marketplace
  discovery.
- `plugins/agentic-course-redesign/`: installable v0.2.1 plugin with six skills,
  scripts, project template, tests, and square SVG branding assets.
- `openai-submission/source/agentic-course-redesign/`: separate skills-only
  public-submission source tree, with no MCP, app, hook, or screenshot payload.
- `openai-submission/review/`: starter prompts, reviewer cases, release notes,
  and an explicit user-owned listing checklist.
- `validation/`: unit, state, forward, package, scrub, and public-source checks.
- `PORTABLE_SETUP_WINDOWS.md` and `PORTABLE_SETUP_MACOS.md`: project-template
  fallback when a supported custom marketplace is unavailable.

## Privacy and assessment security

The default system remains `candidate_not_active`. Protected sources become
immutable after the approved manifest; answer keys and unreleased assessments
remain lecturer-only; data egress requires an exact approved source/role/tool/
audience policy; and production may write only to typed, lecturer-approved
targets. Personal data, submissions, grades, credentials, and secrets are
excluded by default.

OneDrive is cloud-synchronised, not strictly local. Use it for protected course
or assessment material only when institutional, privacy, rights, and security
rules permit that storage.

## Official references

- <https://developers.openai.com/plugins/build/plugins>
- <https://developers.openai.com/plugins/deploy/connect-chatgpt>
- <https://developers.openai.com/plugins/deploy/submission>
- <https://developers.openai.com/plugins/deploy/submission-errors>
- <https://learn.chatgpt.com/docs/plugins>
