# Agentic Course Redesign System

Version `0.2.3` is the current published GitHub and OpenAI Plugins Directory
release for lecturer-controlled, evidence-led course redesign. Version `0.2.4`
is an inactive, interaction-only maintenance candidate under proposal
`ACR-SYS-20260822-007`; it has not been committed, uploaded, published,
installed or activated. The preserved `v0.2.3` release is its rollback base.
Publication or installation does not activate a course runtime, register a
schedule, or start a course run. The system is course-independent: every fresh
run adapts to the supplied subject,
level, programme, language, learners, objectives, assessment, delivery mode and
constraints.

Public repository:
<https://github.com/gpochs/Agentic-Course-Redesign-System>.

The historical v0.2.1 and v0.2.2 tags, assets and checksums remain unchanged.
The OpenAI Platform currently shows Agentic Course Redesign `0.2.3` as
**Published** with a live directory link. The existing plugin page exposes a
plugin-level **Upload** route for a new draft. Therefore a v0.2.4 update should
be uploaded under that existing plugin and validated before publication; do not
delete or unpublish v0.2.3 first. The separate **Unpublish** action is a
delisting/rollback control, not the normal version-update step.

## What is installable now

Participants can install the published v0.2.3 listing from the public Plugins
Directory on supported ChatGPT/Work/Codex desktop surfaces when their account,
workspace policy and app version permit. The checked-out or extracted
repository also remains a valid custom marketplace source. Some Codex CLI
builds can configure a local or Git-backed marketplace; use that route only
when the installed CLI exposes marketplace commands, then start a new session
after installation.

Current OpenAI documentation says plugins work in Chat and Work across supported
ChatGPT surfaces and in Codex in the ChatGPT desktop app. The Codex IDE extension
does not support plugins. Workspace policy, product access, app version, and
administrator controls can still restrict installation or sharing.

See `INSTALLATION.md` for the current directory and pinned public-GitHub routes.
A GitHub repository can distribute the custom marketplace, but GitHub
publication alone does not update the independently published OpenAI listing.

The preserved operational v0.2.3 package remains the rollback baseline while
v0.2.4 is validated. No v0.2.4 installation, picker result or public listing is
claimed until the later exact-version activation and publication steps are
completed and checked in a fresh task.
On builds that flatten skills-only
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
2. complete pre-source Gate 0A before any course path, filename, listing, read,
   copy or hash, distinguishing material ownership/authority, sensitivity,
   student personal data, protected assessment/answer-key handling, exact
   processing environment, and mixed/uncertain cases;
3. answer one unresolved consequential question at a time: use a native card
   only when the live host tool contract can present the complete option set
   plus a custom answer. The current verified Codex contract permits exactly
   two or three explicit choices and adds free-form `Other`; Work's exact
   maximum is not independently documented or exposed here. If capacity is
   unknown, unavailable or exceeded, ask one ordinary chat question with every
   valid numbered option plus `Other`, then wait. Never prune, hide or combine
   valid choices merely to fit a card. Long dependency-based chunks keep every
   valid option visible, and the lecturer may split, merge, reorder or rename
   the grouping;
4. classify and hash eligible course, context, assessment, and teacher-only
   sources, then approve a versioned source-access policy and per-run contract;
5. run all five preliminary specialist perspectives before Gate 2A;
6. research only lecturer-approved focus areas;
7. reconcile evidence, feasibility, accessibility, workload, AI, and assessment;
8. approve only exact research targets at Gate 2B;
9. approve a blueprint and typed material targets separately at Gate 3;
10. produce one approved artefact at a time with independent QA;
11. declare production complete, separately approve and verify the exact
    Production Handoff, then accept, revise, or reject at HITL 3;
12. answer the one-time post-HITL-3 system-review offer; silence waits, while an
    explicit request or decline closes the course run terminal
    `complete_dormant` and it never resumes;
13. receive one informational manual-fresh-trigger and optional staged-schedule
    guidance offer, with no registration or trigger; and
14. consider system files, installation, publication, reusable-system activation
    or scheduling only through later,
    exact-version decisions.

Installing the plugin does not activate a runtime, register a schedule, upload
course files, or grant blanket write access.
The repository marketplace's pre-existing `policy.authentication: ON_INSTALL`
value is host installation-policy metadata, not a bundled authentication
provider, credential or account integration.

## Repository layout

- `.agents/plugins/marketplace.json`: custom repo marketplace for Work mode and
  Codex in the ChatGPT desktop app, and for CLI builds that expose marketplace
  discovery.
- `plugins/agentic-course-redesign/`: inactive v0.2.4 candidate source with six skills,
  scripts, project template, tests, and square SVG branding assets.
- `openai-submission/source/agentic-course-redesign/`: separate skills-only
  public-submission source tree, with no MCP, app, hook, or screenshot payload.
- `openai-submission/review/`: starter prompts, reviewer cases, release notes,
  update guidance, and an explicit publisher-owned listing checklist.
- `validation/`: unit, state, forward, package, scrub, and public-source checks.
- `PORTABLE_SETUP_WINDOWS.md` and `PORTABLE_SETUP_MACOS.md`: project-template
  fallback when a supported custom marketplace is unavailable.

## Privacy and assessment security

The default system remains `candidate_not_active` with `schedules=[]`. Gate 0A
allows personal/unmanaged processing only for owned/rightsholder-authorised or
appropriately licensed/public material with explicit AI-processing authority;
public accessibility alone is insufficient. Institution-internal or restricted
material and student personal data are route-only there; protected assessment
or answer-key material requires explicit handling authority. Mixed or uncertain
material, sensitivity or assessment-security classification fails closed.
Protected sources become
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
