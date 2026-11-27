# Agentic Course Redesign for GitHub Copilot

Use version 0.3.4 to improve a single activity, a set of materials or an entire course. Open a project Session in the Copilot app and select the installed course-redesign orchestrator skill. [Review materials in Copilot](skills/course-redesign-orchestrator/references/native-intake.md). [Install or remove the plugin](PARTICIPANT_QUICK_START.md)

## Start with your course

> My learners can finish this exercise but struggle to explain their reasoning. Help me revise the task and draft a separate guide for the tutor.

1. **Start with your course.** Describe what you want learners to do. Choose **Skip for now** to go straight from your description to design, drafting and review. The material check helps keep course and student information in the right place.
2. **Choose the materials we can use.** You can combine a course site such as Moodle or OLAT, Word or PowerPoint files, cloud slides or spreadsheets, learning apps such as Kahoot! or Mentimeter, and other resources. Select several, name your own, or continue with just your teaching goal. You decide which items may be opened and who can see the drafts.
3. **Check the course brief.** Correct what the plugin understood. Leave a question open if the answer is unclear. Use your own words when explaining your priorities or giving feedback.

Later you choose the focus, compare suggested changes, approve the plan and files, try each draft, and decide what to use. The plugin briefly introduces optional tools and recommends one when it would help with a particular task. It explains the benefit, access and any cost. You can approve that task or batch, ask for setup help, or use the built-in option. Student materials and teacher-only keys have separate destinations.

[Follow all nine teaching steps](assets/PARTICIPANT_QUICK_START.md).

## Cost and support

The plugin is free under the MIT License and provided without a support SLA. Your existing GitHub Copilot plan and organisation policies apply.

<details>
<summary>For maintainers checking package contents and older Copilot compatibility</summary>

## Components

- Six full workflow skills, including the umbrella orchestrator.
- Ten read-only specialist agents covering course mapping, active learning,
  AI integration, assessment alignment, student-experience review, learning
  design, materials, source verification, accessibility/visual QA, and an
  evidence-feasibility red team.
- Preview-first setup, deterministic no-overwrite Gate-0A record generation,
  state-validation, migration, source-manifest, and fingerprinting helpers.
- A Copilot-aware inactive project template.

No MCP server, connector, API integration, authentication, hook, LSP server,
telemetry, schedule, automation, model provider, or additional permission is
declared by this plugin.

Every packaged skill and specialist profile follows the Copilot dialogue
contract. Keep one unresolved consequential question at a time and use the
native `ask_user` card for the complete valid option set whenever the live
GitHub Copilot host accepts it. A live Copilot host has demonstrated at least
five explicit choices plus a custom-answer field; this is an observed
capability, not a maximum. Do not state or assume an unsupported maximum. Never
prune, hide or combine valid choices merely to fit a card. If the host rejects
or cannot present the complete valid set, ask one ordinary chat question
listing every valid numbered option plus `Other`, then wait. For very long
sets, use dependency chunks only when choices share evidence or constrain one
another. Keep every valid option visible across chunks, preserve custom
answers, and let lecturers reshape the grouping. Recap chunks and gates, never
preselect a recommendation, fail closed on uncertainty, and keep exact
authority decisions separate. A blank reply grants no permission. Choosing the offered Skip for now option starts the design from a description.

In GitHub Copilot App/CLI 1.0.80 with an OpenAI-compatible BYOK provider such
as CommandCode Chat Completions, built-in `apply_patch` can be recorded as
`type=custom` and poison saved task history. Do not use `apply_patch` for any
file mutation in an affected session, not only Gate 0A. Use packaged helpers or
function-style PowerShell/Python. Preserve exact-target preview, the existing
lecturer approval, expected-current-SHA-256 verification for modifications,
atomic writes, reread, and validation.

If `expected "function"` occurs, do not retry in that task. Start a fresh
project task, recover durable state read-only, and verify whether the preceding
edit already succeeded before continuing. This is not a missing installable
function; adding an MCP server or plugin does not fix poisoned history. This
compatibility path changes no workflow semantics and adds no MCP server, hook,
authentication, or permission.

The preserved rollback package is `0.3.3`.

</details>
