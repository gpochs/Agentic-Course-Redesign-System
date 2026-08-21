# Publication status

## GitHub

The public repository is available at:

<https://github.com/gpochs/Agentic-Course-Redesign-System>

System release `0.2.2` packages ChatGPT plugin version `0.2.2`, shared workflow
core `0.2.2`, and reconciled platform adapters `0.2.2`. Its tag and exact
release archives, checksums, inventories and validation evidence are published
with the GitHub release. Repository publication does not install the plugin,
activate a reusable runtime, or register a schedule.

The historical `system-release-validation-v0.2.1.json` asset is mislabeled internally: it
describes the v0.2.0 archive. The v0.2.1 ZIP and checksum remain valid; the
v0.2.2 evidence guard records the mismatch and makes validation fail when report
name, archive name, embedded inventory version, digest or byte count disagree.

## ChatGPT and Codex

A GitHub marketplace can provide an installable custom source on supported
surfaces. It does not automatically create a listing in OpenAI's universal
Plugins Directory.

At the pre-release validation checkpoint, the release host had a verified
user-level installation of version `0.2.1`. A new supported Codex task loaded
that cache and invoked the
`@Agentic Course Redesign` umbrella; all six bundled skills were available. On
surfaces that flatten skills-only bundles, the umbrella is shown as the
orchestrator skill rather than a separate parent row. Version `0.2.2` needs its
own exact-version installation and fresh-task picker verification; release
publication is not that evidence. Installation is not a global push
to other users, devices, accounts or workspaces. App version, account access
and workspace policy may restrict custom marketplaces, and the Codex IDE
extension does not support plugins.

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
