# Participant quick start — GitHub Copilot app

These instructions are for the standalone GitHub Copilot app, not GitHub
Desktop or an editor extension.

## Before installation

You need a GitHub account, access to a GitHub Copilot plan, the GitHub Copilot
app installed and signed in, Git installed, and Python 3 available as `python`
for the packaged deterministic helpers. If your Copilot access is managed by
an organization, its administrator may restrict the app or third-party plugin
marketplaces.

The plugin uses your existing Copilot access. It does not require an external
model provider, API key, MCP server, publisher account, or publisher-operated
service.

Read the [lecturer’s walkthrough](assets/PARTICIPANT_QUICK_START.md) for
the skip route, tool choices, and an example of the first decision.

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

   Set up an agentic redesign project for this one course. Offer the short onboarding or Skip for now. Do not list, open, copy, hash, upload, or change course files yet. If I skip, continue from my description through every design and production decision.
   ```

   If the app does not autocomplete the qualified slash name, select the
   `course-redesign-orchestrator` skill from the installed
   `agentic-course-redesign` plugin and paste the remaining text.

Do not initially disclose student personal data, submissions, grades,
credentials, secrets, source filenames, or source paths. Only use material you
are authorized to process with AI.

Installation alone does not inspect files, start a redesign, activate a
runtime, register automation, or schedule a run.



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
`0.2.4-copilot.2`; rollback does not install or activate itself.

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
