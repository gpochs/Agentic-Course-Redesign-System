# Install Agentic Course Redesign in the GitHub Copilot app

This guide is for course participants using the standalone GitHub Copilot app.
The plugin is a static skills-and-agents package; it does not run a publisher
server or create a support subscription.

## Requirements

- A GitHub account with GitHub Copilot access.
- The GitHub Copilot app installed and signed in.
- Git installed.
- Organization permission for third-party plugins, when the account is
  organization-managed.

No separate API key or model provider is required.

## Recommended installation

1. [Add the Agentic Course Redesign marketplace](https://github.com/copilot/app/launch?open=ghapp%3A%2F%2Fplugins%2Fmarketplace%2Fadd%3Fsource%3Dgpochs%252FAgentic-Course-Redesign-System).
2. Confirm that its source is
   `gpochs/Agentic-Course-Redesign-System`.
3. [Install the Agentic Course Redesign plugin](https://github.com/copilot/app/launch?open=ghapp%3A%2F%2Fplugins%2Finstall%3Fsource%3Dagentic-course-redesign%2540agentic-course-redesign-system).
4. Confirm that the plugin specification is
   `agentic-course-redesign@agentic-course-redesign-system`.
5. Open **Settings → Plugins** and confirm that
   `agentic-course-redesign` is installed and enabled.
6. Open **Settings → Skills**, search for `course-redesign`, and confirm the
   six skills.

The links open pre-filled confirmation forms in the app. They do not install
anything automatically.

Command-line alternative:

```powershell
copilot plugin marketplace add gpochs/Agentic-Course-Redesign-System
copilot plugin install agentic-course-redesign@agentic-course-redesign-system
copilot plugin list
```

## Begin in the project chat

Work in a project **Session**, not the general **Chats** area:

1. Add one isolated course folder or repository as a project.
2. Start a new session inside that project.
3. Select **Interactive** mode.
4. Paste:

```text
/agentic-course-redesign/course-redesign-orchestrator

Set up an agentic redesign project for this one course. Begin with Gate 0A only. Do not list, open, copy, hash, upload, or change course files yet. Ask me only for the minimum processing-eligibility information, present the proposed setup, and then stop for my approval.
```

If the app does not autocomplete that qualified slash name, select the
`course-redesign-orchestrator` skill from the installed
`agentic-course-redesign` plugin and paste the remaining text.

Gate 0A deliberately comes before source paths or filenames. Do not initially
provide student personal data, submissions, grades, credentials, secrets, or
protected source details.



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
be true, uncertainty fails closed, custom answers are preserved and confirmed,
blank or `Skip` cannot advance, and exact authority approvals remain separate.

## Copilot 1.0.80 BYOK compatibility

For Gate 0A, the setup skill must invoke
`scripts/create_material_processing_eligibility.py` through PowerShell/Python as a normal
shell function call. It first runs a preview without `--apply`, displays the
complete deterministic record, fingerprint, exact target and
`overwrite: false`, and waits for exact-target approval. Only then may it
repeat the same call with `--apply`. The helper accepts only an absolute
project directory through `--project <absolute project directory>`, derives
`01_Control/material-processing-eligibility.json` beneath that project, rejects
a redirected `01_Control`, and refuses overwrite.

Do not ask Copilot to invoke this helper through `apply_patch`. In Copilot
1.0.80 BYOK, `expected function` can come from poisoned task history after an
earlier `apply_patch` call was recorded as `type=custom`; it is not a missing
installable function or MCP server. Start a fresh task in the project. For an affected
BYOK session, prefer GitHub-hosted GPT-5.4 or the default Claude model. No MCP,
hook, authentication, or permission is required or added.

Rollback, if deliberately chosen by the operator, is
`0.2.3-copilot.1`; rollback does not install or activate itself.

## Remove

```powershell
copilot plugin uninstall agentic-course-redesign
copilot plugin marketplace remove agentic-course-redesign-system
```

The plugin is free and provided as-is, without a support SLA or guaranteed
maintenance. Participants use their own GitHub Copilot plan and remain subject
to its plan limits and organization policies.

Official GitHub references:

- [GitHub Copilot app quickstart](https://docs.github.com/en/copilot/how-tos/github-copilot-app/getting-started)
- [Opening the app with links](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/github-copilot-app/open-with-deep-links)
- [Finding and installing plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)
- [Creating a plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
