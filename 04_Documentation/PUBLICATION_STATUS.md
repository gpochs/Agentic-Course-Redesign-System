# Publication status

## GitHub

The public repository is available at:

<https://github.com/gpochs/Agentic-Course-Redesign-System>

System release candidate `0.2.1` packages ChatGPT plugin version `0.2.1` and
passes the recorded local source and package checks. The latest immutable
published release remains `v0.2.0` until the `v0.2.1` tag, CI result, release
assets, checksums and fresh-clone validation have been verified.
The shared workflow core and four project-local adapters remain at `0.2.0`
because their contracts and gated workflow semantics are unchanged.

## ChatGPT and Codex

A GitHub marketplace can provide an installable custom source on supported
surfaces. It does not automatically create a listing in OpenAI's universal
Plugins Directory.

The release host currently has a verified user-level installation of version
`0.2.0`. Version `0.2.1` structurally validates one full-workflow umbrella named
`@Agentic Course Redesign` plus five direct component entries; the picker smoke
test is recorded only after a new supported Work/Codex task has loaded the
`0.2.1` cache. On surfaces that flatten skills-only bundles, the umbrella is
shown as the orchestrator skill rather than a separate parent row. This is not
a global push to other users, devices, accounts or workspaces. App version,
account access and workspace policy may restrict custom marketplaces, and the
Codex IDE extension does not support plugins.

A universal listing requires a separate OpenAI Platform submission, verified
publisher identity, public metadata and policies, test cases, automated scans,
review, approval and a later developer publish action. Until those steps have
actually completed, use the wording **prepared skills-only OpenAI submission
candidate** or **installable from the repository marketplace on supported
surfaces**.

## Other systems

Copilot, Claude Code, OpenCode and Antigravity adapters are project-local
configuration packages. Their presence in GitHub is not proof of installation,
activation or end-to-end testing in a user's account. Each README distinguishes
documented compatibility from exercised validation.
