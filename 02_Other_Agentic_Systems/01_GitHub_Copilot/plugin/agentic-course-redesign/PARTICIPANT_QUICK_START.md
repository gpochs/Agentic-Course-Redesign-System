# Participant quick start — GitHub Copilot app

These instructions are for the standalone GitHub Copilot app, not GitHub
Desktop or an editor extension.

## Before installation

You need a GitHub account, access to a GitHub Copilot plan, the GitHub Copilot
app installed and signed in, and Git installed. If your Copilot access is
managed by an organization, its administrator may restrict the app or
third-party plugin marketplaces.

The plugin uses your existing Copilot access. It does not require an external
model provider, API key, MCP server, publisher account, or publisher-operated
service.

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

## Start one course project

Use a project **Session**, not the app's general **Chats** area.

1. Add or select one isolated folder or repository for one course.
2. Start a new session inside that project.
3. Choose **Interactive** mode.
4. Paste:

   ```text
   /agentic-course-redesign/course-redesign-orchestrator

   Set up an agentic redesign project for this one course. Begin with Gate 0A only. Do not list, open, copy, hash, upload, or change course files yet. Ask me only for the minimum processing-eligibility information, present the proposed setup, and then stop for my approval.
   ```

   If the app does not autocomplete the qualified slash name, select the
   `course-redesign-orchestrator` skill from the installed
   `agentic-course-redesign` plugin and paste the remaining text.

Do not initially disclose student personal data, submissions, grades,
credentials, secrets, source filenames, or source paths. Only use material you
are authorized to process with AI.

Installation alone does not inspect files, start a redesign, activate a
runtime, register automation, or schedule a run.

## Remove

In **Settings → Plugins**, uninstall `agentic-course-redesign`, then remove
the `agentic-course-redesign-system` marketplace.

```powershell
copilot plugin uninstall agentic-course-redesign
copilot plugin marketplace remove agentic-course-redesign-system
```

Remove the plugin first: Copilot normally refuses to remove a marketplace while
one of its plugins remains installed.

## Cost and support boundary

The plugin is provided free of charge and as-is. It has no publisher-operated
server, API key, MCP service, authentication service, paid hosting, telemetry,
or support SLA. Your normal GitHub Copilot plan, usage limits, organization
policies, and any associated GitHub costs still apply. Account, policy, or
platform problems belong with GitHub or your organization's IT support.
