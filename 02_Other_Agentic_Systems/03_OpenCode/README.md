# Agentic Course Redesign for OpenCode

## Install the native skills and agents

OpenCode discovers Markdown skills and subagents at project or account scope. From the repository root, build the edition into a new directory with Python 3.11 or newer.

```shell
python 02_Other_Agentic_Systems/build_host_package.py opencode <new-package-directory>
```

For global use, copy the generated `skills/course-redesign/` into `~/.config/opencode/skills/` and the ten `agents/*.md` into `~/.config/opencode/agents/`. For one project, use `<project>/.opencode/skills/` and `<project>/.opencode/agents/` instead. Review filename collisions before copying.

Open the course project in OpenCode, select a model covered by your subscription, start a new conversation and ask it to use the course-redesign skill. To use an OpenAI subscription, choose the ChatGPT sign-in option for the provider.

## Start with your course

> My trainees can read a payslip but struggle to explain a deduction. Help me build one practice exercise with feedback.

1. **Start with your course.** Describe what you want learners to do. Choose **Skip for now** to go straight from your description to design, drafting and review. The material check helps keep course and student information in the right place.
2. **Choose the materials we can use.** You can combine a course site such as Moodle or OLAT, Word or PowerPoint files, cloud slides or spreadsheets, learning apps such as Kahoot! or Mentimeter, and other resources. Select several, name your own, or continue with just your teaching goal. You decide which items may be opened and who can see the drafts.
3. **Check the course brief.** Correct what the plugin understood. Leave a question open if the answer is unclear. Use your own words when explaining your priorities or giving feedback.

Later you choose the focus, compare suggested changes, approve the plan and files, try each draft, and decide what to use. The plugin briefly introduces optional tools and recommends one when it would help with a particular task. It explains the benefit, access and any cost. You can approve that task or batch, ask for setup help, or use the built-in option. Student materials and teacher-only keys have separate destinations.

[Follow all nine teaching steps](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md).

For an online activity, you can lend its tab with the optional Browse extension when it is available. Open the intended course yourself, sign in and identify the private draft you want to use. Ask the plugin to verify the destination before editing, reopen that draft afterwards and show you the result. You can also use an authorised export or a description. [OpenCode Browse](https://opencode.ai/product/browse) · [OpenCode skills](https://opencode.ai/docs/skills/) · [OpenCode agents](https://opencode.ai/docs/agents/)

<details>
<summary>For maintainers using the manual project overlay</summary>

## Manual project overlay


Adapter release: `0.3.3`. Shared semantic base: inactive candidate
`ACR-SYS-20261127-004` version `0.3.3`.

This overlay adds ten project-local OpenCode V2 subagent profiles to the
portable core. OpenCode V2 natively discovers the core's root `AGENTS.md` and
the compatibility skill at `.claude/skills/course-redesign/`, so no duplicate
instruction file or `opencode.jsonc` is needed.

Use the choice tool available in the live host only when it can show all valid answers and a custom reply. When several answers can apply, preserve their combinations or use chat.

Compose `../00_Portable_Core_Adapter/overlay/` first, then this `overlay/`,
relative to the same reviewed project root:

```text
<project-root>/
├── AGENTS.md                                  # portable core; active V2 source
├── .claude/skills/course-redesign/            # portable core; discovered
└── .opencode/
    └── agents/
        └── <ten read-only role>.md
```

Every agent uses `mode: subagent` and ordered V2 permission rules: deny all,
then allow only project reads, globbing, grepping, and skill loading. No model or
provider is selected. The wrappers require a current orchestrator state capsule
and contain no independent workflow logic.

No executable OpenCode plugin is included. Static instructions, skills, and
agent Markdown cover the need; V2 plugins execute in-process, local plugin files
are auto-discovered, and the official plugin API is currently beta. Adding a
plugin would therefore create unnecessary activation and execution risk.

No `instructions` config entry is included either. Current V2 documentation
says the schema retains that array but does not resolve its entries into model
instructions; `AGENTS.md` is the active project mechanism.

Official references:

- [OpenCode V2 instructions](https://opencode.ai/v2/docs/instructions)
- [OpenCode V2 agents](https://opencode.ai/v2/docs/agents)
- [OpenCode V2 skills](https://opencode.ai/v2/docs/skills)
- [OpenCode V2 permissions](https://opencode.ai/v2/docs/permissions)
- [OpenCode V2 plugins](https://opencode.ai/v2/docs/build/plugins)

</details>
