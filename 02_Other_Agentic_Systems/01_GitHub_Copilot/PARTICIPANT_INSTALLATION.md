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
