# Agentic Course Redesign for a local course project

Version 0.3.5. Choose the instructions for your app. [GitHub Copilot](../01_GitHub_Copilot/README.md) · [Claude Code](../02_Claude_Code/README.md) · [OpenCode](../03_OpenCode/README.md) · [Antigravity](../04_Google_Antigravity/README.md)

## Start with your course

> Help me redesign my first workshop. Learners can follow a worked example, but they need practice choosing a method on their own.

1. **Start with your course.** Describe what you want learners to do. Choose **Skip for now** to go straight from your description to design, drafting and review. The material check helps keep course and student information in the right place.
2. **Choose the materials we can use.** You can combine a course site such as Moodle or OLAT, Word or PowerPoint files, cloud slides or spreadsheets, learning apps such as Kahoot! or Mentimeter, and other resources. Select several, name your own, or continue with just your teaching goal. You decide which items may be opened and who can see the drafts.
3. **Check the course brief.** Correct what the plugin understood. Leave a question open if the answer is unclear. Use your own words when explaining your priorities or giving feedback.

Later you choose the focus, compare suggested changes, approve the plan and files, try each draft, and decide what to use. The plugin briefly introduces optional tools and recommends one when it would help with a particular task. It explains the benefit, access and any cost. You can approve that task or batch, ask for setup help, or use the built-in option. Student materials and teacher-only keys have separate destinations.

[Follow all nine teaching steps](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md).

<details>
<summary>For maintainers building a project manually</summary>

The `overlay/` directory is laid out relative to a future project root:

```text
<project-root>/
├── AGENTS.md
└── .claude/
    └── skills/
        └── course-redesign/
            ├── SKILL.md
            └── references/
                ├── control-contract.md
                ├── role-contracts.md
                └── workflow.md
```

`AGENTS.md` is the shared always-on safety envelope. The skill holds the shared
workflow contract and uses the portable Agent Skills format. The
`.claude/skills/` location is deliberately reused because current Claude Code,
GitHub Copilot, and OpenCode documentation all describe project skill discovery
there. Platform folders beside this adapter add only native instruction and
agent wrappers.

The portable instructions use the live host’s choice controls when they support every valid answer and a custom reply. Otherwise the same choices are presented in chat. The source-free route keeps every later approval. Source inspection and durable control records require the official deterministic helpers. A fresh project can start without any existing course material.

## Safe composition

1. Review the target project and this overlay without changing either.
2. Compose this overlay first and exactly one platform overlay second.
3. Treat every collision as a manual merge decision. Do not overwrite an
   existing instruction, skill, or agent file automatically.
4. Commit the reviewed files to the project repository if the repository owner
   wants them shared.
5. Copying files does not approve Gate 0A or Gate 0, activate a reusable
   runtime, enable a schedule, authorize network use, or authorize any write to
   course materials.

No copy/install script is supplied intentionally: the adapter must not mutate a
project or turn itself on merely because the public repository was cloned.

## Static validation

Repository maintainers can preview deterministic shared-core mirror and
manifest reconciliation without writing:

```text
python 00_Portable_Core_Adapter/validation/reconcile_adapters.py
```

After reviewing the change list, `--apply` refreshes the declared shared and host-specific copies and their manifests. It never copies
an overlay into a course project, activates a runtime, or registers automation.

From `02_Other_Agentic_Systems/`, validate the portable, Claude Code and OpenCode adapter records without invoking a
host application:

```text
python 00_Portable_Core_Adapter/validation/validate_adapters.py
```

Pass the validated canonical source root as the optional sole argument to also
recompute every recorded source SHA-256. The validator checks manifests,
root-relative inventories, the portable skill contract, the twenty Claude Code
and OpenCode native role
sets, thin-wrapper references, fail-closed escalation, read-only tool or
permission declarations, absence of an executable OpenCode plugin, and private
absolute-path leakage. It also checks the production-handoff-before-HITL3
order, terminal dormant lifecycle, the interaction contract and Gate-0A helper
fallback, and the full post-HITL3 review offer and proposal-only authority.

Each manifest's top-level `files` array freezes every file under that adapter
root except `adapter-manifest.json` itself. The self-exclusion is explicit in
`file_inventory.manifest_self_excluded`; excluding the manifest avoids an
impossible recursive self-hash.

## Source and specification references

- [Agent Skills specification](https://agentskills.io/specification)
- [GitHub Copilot repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [GitHub Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Claude Code memory and project instructions](https://code.claude.com/docs/en/memory)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenCode V2 instructions](https://opencode.ai/v2/docs/instructions)
- [OpenCode V2 skills](https://opencode.ai/v2/docs/skills)

See `CAPABILITIES.md` for the deliberately narrow capability boundary and
`adapter-manifest.json` for provenance and the root-relative inventory.

</details>
