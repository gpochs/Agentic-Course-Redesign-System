# Start a course redesign in the GitHub Copilot app

Sign in to the GitHub Copilot app with your existing plan. Choose a model included in your plan. For files and saved projects, the packaged helpers use Python 3.11 or later. The marketplace route uses Git. Check with your administrator if your organisation restricts third-party plugins.

## Install

1. Open the
   [marketplace-registration link](https://github.com/copilot/app/launch?open=ghapp%3A%2F%2Fplugins%2Fmarketplace%2Fadd%3Fsource%3Dgpochs%252FAgentic-Course-Redesign-System).
2. In the Copilot app, verify the pre-filled marketplace source:

   ```text
   gpochs/Agentic-Course-Redesign-System
   ```

3. Confirm the marketplace addition.
4. Open the
   [plugin-installation link](https://github.com/copilot/app/launch?open=ghapp%3A%2F%2Fplugins%2Finstall%3Fsource%3Dagentic-course-redesign%2540agentic-course-redesign-system).
5. Verify the pre-filled plugin specification:

   ```text
   agentic-course-redesign@agentic-course-redesign-system
   ```

6. Confirm installation. These links only pre-fill forms; they never install
   anything without your confirmation.
7. In **Settings → Plugins**, verify that `agentic-course-redesign` is
   installed and enabled. In **Settings → Skills**, search for
   `course-redesign` and confirm that the six plugin skills are visible.

Command-line alternative:

```powershell
copilot plugin marketplace add gpochs/Agentic-Course-Redesign-System
copilot plugin install agentic-course-redesign@agentic-course-redesign-system
copilot plugin list
```

## Install for one project

For instructions for a single project, see the [Copilot installation guide](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/02_Other_Agentic_Systems/01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md).

## Open a course project

1. Open one course folder in a new project **Session**.
2. Choose **Interactive** mode.
3. With the account plugin, select the installed course-redesign orchestrator skill or type `/agentic-course-redesign/course-redesign-orchestrator` if Copilot offers it. For a project-only installation, ask for the `course-redesign` skill.
4. Start with an example of your own, like the one below. Share the kind of material first. Keep individual learner records and teacher-only answers private.

## Start with your course

> My students tend to choose the right answer but cannot explain it. Help me revise one quiz question and its feedback. I may choose Skip for now and begin with this teaching goal alone.

1. **Start with your course.** Describe what you want learners to do. Choose **Skip for now** to go straight from your description to design, drafting and review. The material check helps keep course and student information in the right place.
2. **Choose the materials we can use.** You can combine a course site such as Moodle or OLAT, Word or PowerPoint files, cloud slides or spreadsheets, learning apps such as Kahoot! or Mentimeter, and other resources. Select several, name your own, or continue with just your teaching goal. You decide which items may be opened and who can see the drafts.
3. **Check the course brief.** Correct what the plugin understood. Leave a question open if the answer is unclear. Use your own words when explaining your priorities or giving feedback.

Later you choose the focus, compare suggested changes, approve the plan and files, try each draft, and decide what to use. The plugin briefly introduces optional tools and recommends one when it would help with a particular task. It explains the benefit, access and any cost. You can approve that task or batch, ask for setup help, or use the built-in option. Student materials and teacher-only keys have separate destinations.

[Follow all nine teaching steps](assets/PARTICIPANT_QUICK_START.md).

## Remove

In **Settings → Plugins**, uninstall `agentic-course-redesign`, then remove
the `agentic-course-redesign-system` marketplace.

```powershell
copilot plugin uninstall agentic-course-redesign
copilot plugin marketplace remove agentic-course-redesign-system
```

Remove the plugin first: Copilot normally refuses to remove a marketplace while
one of its plugins remains installed.

## Costs and support

The plugin itself is free. Use the models covered by your existing Copilot plan. GitHub's usage limits and your organisation's policies still apply. For account access or a blocked installation, contact GitHub or your organisation's IT team. The publisher provides the plugin as-is, without a support SLA.

<details>
<summary>For maintainers troubleshooting an older Copilot installation</summary>

## Copilot dialogue behavior

The plugin keeps one unresolved consequential question at a time. It uses the
native `ask_user` card for the complete valid option set whenever the live
GitHub Copilot host accepts it. A live Copilot host has demonstrated at least
five explicit choices plus a custom-answer field; this is an observed
capability, not a maximum. Do not state or assume an unsupported maximum. Never
prune, hide or combine valid choices merely to fit a card. If the host rejects
or cannot present the complete valid set, the plugin asks one ordinary chat
question listing every valid numbered option plus `Other`, then waits. For very
long sets, it may use dependency chunks only where choices share evidence or
constrain one another. Keep every valid option visible across chunks; you may
split, merge, reorder or rename their grouping. Recommendations are
evidence-aligned, reversible, and never preselected; factual declarations must
be true, uncertainty fails closed, custom answers are preserved and confirmed.
An unanswered approval cannot advance. Choosing “Skip for now” at onboarding starts a source-free redesign, and exact authority approvals remain separate.

## Copilot 1.0.80 BYOK compatibility

With an OpenAI-compatible BYOK provider such as CommandCode Chat Completions,
Copilot 1.0.80 can record a built-in `apply_patch` edit as `type=custom`. The
edit may have succeeded, but the malformed saved history can make the next
request fail with `expected "function"`. In an affected session, do not use
`apply_patch` for any workflow file. This includes Gate-0A records, manifests,
working notes, course-material candidates, QA records, state, and system-review
records.

Use a packaged helper or function-style PowerShell/Python instead. Every write
must still preview the exact target and content or diff, wait for the existing
required lecturer approval, compare the expected current SHA-256 before
modifying an existing file, write atomically, and reread and revalidate the
result. For Gate 0A, invoke
`scripts/create_material_processing_eligibility.py` through function-style
PowerShell/Python. Run it without `--apply` first so it displays the complete
deterministic record, fingerprint, exact target and `overwrite: false`; only
after exact-target approval may the identical command be repeated with
`--apply`. The helper accepts only an absolute project directory through
`--project <absolute project directory>`, derives
`01_Control/material-processing-eligibility.json` beneath that project,
rejects a redirected `01_Control`, and refuses overwrite.

If `expected "function"` appears, do not retry in that task:

1. Start a fresh task inside the same project.
2. Ask it to recover durable control state read-only.
3. Verify whether the preceding file edit already completed before repeating
   any step.
4. Continue with function-style PowerShell/Python only.

This failure is not evidence of a missing installable function. Another MCP
server or plugin does not repair poisoned task history; no MCP, hook,
authentication, or additional permission is required or added.

Rollback, if deliberately chosen by the operator, is
`0.3.2`; rollback does not install or activate itself.

</details>
