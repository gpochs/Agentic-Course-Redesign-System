# Agentic Course Redesign for Claude Code

## Install for an account or a project

From the repository root, build the standalone plugin with Python 3.11 or newer. For a personal installation, pass a new directory under `~/.claude/skills/agentic-course-redesign`. For one course project, use `<project>/.claude/skills/agentic-course-redesign`. Expand the home path in your shell. The builder refuses to replace an existing directory.

```shell
python 02_Other_Agentic_Systems/build_host_package.py claude <new-plugin-directory>
claude plugin validate <new-plugin-directory>
```

Open your course project, reload plugins and choose a Fable or Opus model included with your Claude subscription. Start with `/gpochs-course-redesign` or select the installed course-redesign orchestrator skill. Each specialist inherits the conversation model.

## Start with your course

> My class can recall the key terms but struggles to use them in a case. Help me revise one seminar and its handout.

1. **Start with your course.** Describe what you want learners to do. Choose **Skip for now** to go straight from your description to design, drafting and review. The material check helps keep course and student information in the right place.
2. **Choose the materials we can use.** You can combine a course site such as Moodle or OLAT, Word or PowerPoint files, cloud slides or spreadsheets, learning apps such as Kahoot! or Mentimeter, and other resources. Select several, name your own, or continue with just your teaching goal. You decide which items may be opened and who can see the drafts.
3. **Check the course brief.** Correct what the plugin understood. Leave a question open if the answer is unclear. Use your own words when explaining your priorities or giving feedback.

Later you choose the focus, compare suggested changes, approve the plan and files, try each draft, and decide what to use. The plugin briefly introduces optional tools and recommends one when it would help with a particular task. It explains the benefit, access and any cost. You can approve that task or batch, ask for setup help, or use the built-in option. Student materials and teacher-only keys have separate destinations.

[Follow all nine teaching steps](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md).

Claude shows the next question as a choice card when it fits, or in chat when you need to explain. For a document or presentation, ask for the editable draft and open it in its usual application. Ask Claude what it actually checked. [Claude skills](https://code.claude.com/docs/en/skills) · [Installing skill-directory plugins](https://code.claude.com/docs/en/plugins/create)

<details>
<summary>For maintainers using the manual project overlay</summary>

## Manual project overlay


Adapter release: `0.3.2`. Shared semantic base: inactive candidate
`ACR-SYS-20261127-003` version `0.3.2`.

This overlay adds a project `CLAUDE.md`, one path-scoped rule, and ten
project-local Claude Code subagents to the portable core. It does not open or
configure Claude Code, install a plugin, add hooks, define MCP servers, or alter
user/managed settings.

Use the choice tool available in the live host only when it can show all valid answers and a custom reply. When several answers can apply, preserve their combinations or use chat.

Compose `../00_Portable_Core_Adapter/overlay/` first, then this `overlay/`,
relative to the same reviewed project root:

```text
<project-root>/
├── AGENTS.md                                  # portable core
├── CLAUDE.md                                  # imports AGENTS.md
└── .claude/
    ├── skills/course-redesign/                # portable core
    ├── rules/course-redesign.md
    └── agents/<ten read-only role>.md
```

Each subagent preloads the shared `course-redesign` skill and exposes only
`Read`, `Glob`, and `Grep`. It must receive a current orchestrator state capsule
and fail closed otherwise. The wrappers do not duplicate the gate sequence or
specialist contracts.

Review collisions manually and commit these project files only if the
repository owner wants them shared. Copying the overlay does not launch Claude
Code, invoke a subagent, approve data egress, or activate a reusable runtime.

Official references:

- [Claude Code memory and `CLAUDE.md`](https://code.claude.com/docs/en/memory)
- [Claude Code rules](https://code.claude.com/docs/en/memory#organize-rules-with-clauderules)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference)

</details>
