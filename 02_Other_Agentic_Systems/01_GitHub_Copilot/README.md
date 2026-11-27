# Agentic Course Redesign for GitHub Copilot

Version 0.3.3 works in the GitHub Copilot app. Install the plugin for your account or add the skill and specialists to a single course project. [Installation and removal](PARTICIPANT_INSTALLATION.md)

Open a project **Session** in **Interactive** mode and choose the installed course-redesign orchestrator skill. Use a model included with your Copilot plan.

## Start with your course

> My students can spot a historical claim but accept the first source they find. Help me redesign one activity so they practise weighing evidence.

1. **Start with your course.** Describe what you want learners to do. Choose **Skip for now** to go straight from your description to design, drafting and review. The material check helps keep course and student information in the right place.
2. **Choose the materials we can use.** You can combine a course site such as Moodle or OLAT, Word or PowerPoint files, cloud slides or spreadsheets, learning apps such as Kahoot! or Mentimeter, and other resources. Select several, name your own, or continue with just your teaching goal. You decide which items may be opened and who can see the drafts.
3. **Check the course brief.** Correct what the plugin understood. Leave a question open if the answer is unclear. Use your own words when explaining your priorities or giving feedback.

Later you choose the focus, compare suggested changes, approve the plan and files, try each draft, and decide what to use. The plugin briefly introduces optional tools and recommends one when it would help with a particular task. It explains the benefit, access and any cost. You can approve that task or batch, ask for setup help, or use the built-in option. Student materials and teacher-only keys have separate destinations.

[Follow all nine teaching steps](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md).

If your example uses an online course, show the plugin the intended draft once you have agreed which material it may open. If your Copilot session cannot preview that site, use an approved local export or ask to review the draft in the application you normally use.

<details>
<summary>For maintainers installing or testing the Copilot edition</summary>

## Native plugin

The self-contained package is:

```text
plugin/agentic-course-redesign/
├── plugin.json
├── skills/                         # six canonical workflow skills
├── agents/                         # ten full read-only specialist roles
├── scripts/                        # preview/validation helpers
├── assets/project-template/        # inactive Copilot-aware scaffold
├── PARTICIPANT_QUICK_START.md
└── LICENSE
```

The repository marketplace manifest is
`/.github/plugin/marketplace.json`. See
[PARTICIPANT_INSTALLATION.md](PARTICIPANT_INSTALLATION.md) for clickable app
links, command-line alternatives, verification, the first project-session
prompt, and removal instructions.

The native package preserves the complete six-skill v0.3.3 workflow text and
adds Copilot-specific guidance for choices and older host versions. Helpers remain
byte-identical to the canonical core. Its ten Copilot agents preserve the full
specialist role contracts and add the host dialogue boundary while retaining
read-only tool declarations.

It declares no MCP server, connector, API integration, authentication, hook,
LSP server, telemetry, schedule, automation, model provider, or additional
permission. It is provided as-is without a support SLA.

## Dialogue and Copilot 1.0.80 compatibility

Lecturer dialogue keeps one unresolved consequential question at a time. Use
the native `ask_user` card for the complete valid option set whenever the live
GitHub Copilot host accepts it. A live Copilot host has demonstrated at least
five explicit choices plus a custom-answer field; this is an observed
capability, not a maximum. Do not state or assume an unsupported maximum. Never
prune, hide or combine valid choices merely to fit a card. If the host rejects
or cannot present the complete valid set, ask one ordinary chat question
listing every valid numbered option plus `Other`, then wait. For very long
sets, use dependency chunks only when choices share evidence or constrain one
another. Keep every valid option visible across chunks and let the lecturer
split, merge, reorder or rename the grouping. Recommendations are never
preselected, custom answers are preserved and confirmed. An unanswered approval cannot advance. Choosing “Skip for now” at onboarding starts a source-free redesign, and exact authority gates remain separate.

In GitHub Copilot App/CLI 1.0.80 with an OpenAI-compatible BYOK provider such
as CommandCode Chat Completions, a built-in `apply_patch` call can be stored as
`type=custom` even after its edit succeeds. That malformed history can make the
next provider request fail with `expected "function"`. Therefore this adapter
must not use `apply_patch` for **any** file mutation in an affected session,
including control records, manifests, notes, materials, QA records, state, and
system-review files. Use packaged helpers or function-style PowerShell/Python.

Every permitted write still requires the existing workflow safeguards: preview
the exact target and proposed content or diff; obtain the already-required
lecturer approval; verify the expected current SHA-256 before changing an
existing file; write atomically; then reread and revalidate the result. This
transport workaround changes no gate, option, approval, target, or permission.
If `expected "function"` occurs, do not retry in that task. Start a fresh
project task, recover durable state read-only, and confirm whether the preceding
edit already succeeded before continuing. Installing another plugin or MCP
server does not repair poisoned history.

Rollback remains the prior package `0.3.2`; rollback is a separate
operator decision and does not activate or install either version.

## Project-local overlay

For a manual repository configuration, compose
`../00_Portable_Core_Adapter/overlay/` first, then this `overlay/`, relative
to the same reviewed project root:

```text
<project-root>/
├── AGENTS.md
├── .claude/skills/course-redesign/
└── .github/
    ├── copilot-instructions.md
    ├── instructions/
    │   └── course-redesign.instructions.md
    └── agents/
        └── <ten read-only role>.agent.md
```

Review every collision manually. Copying these files does not turn on Copilot,
start a task, approve network use, or activate the course-redesign runtime.

## Validation

Run the native package and mutation checks from the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
python 02_Other_Agentic_Systems/01_GitHub_Copilot/validation/validate_native_plugin.py
python -m unittest discover -s 02_Other_Agentic_Systems/01_GitHub_Copilot/validation -p "test_*.py" -v
```

For a local host-discovery check, point the Copilot CLI at
`plugin/agentic-course-redesign/` with `--plugin-dir` and run
`plugin list`. This verifies manifest loading without installing into the
participant's live configuration or consuming a model turn. Copilot's plugin
list does not enumerate every custom agent, so agent count, tool ceilings, and
source fidelity are enforced separately by the static validator and mutation
tests.

## Official references

- [About Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [Creating a Copilot plugin](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)
- [Creating a plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
- [Finding and installing plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)
- [GitHub Copilot app customization](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app)
- [Custom-agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)

Availability and organization policy can differ across the Copilot app, CLI,
GitHub.com, and IDE surfaces. Static repository validation is not proof that an
organization has enabled third-party plugins.

</details>
