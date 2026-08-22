# Publication status

## GitHub

The public repository is available at:

<https://github.com/gpochs/Agentic-Course-Redesign-System>

System source `0.2.4` is an inactive interaction-only maintenance candidate
under proposal `ACR-SYS-20260822-007`. The published GitHub rollback release is
`v0.2.3`. A future `v0.2.4` tag must point to the exact validated commit and use
matching archives, checksums, inventories and validation evidence. Repository
publication does not install the plugin, activate a reusable runtime, or
register a schedule.

Version `0.2.3` was validated and released under proposal
`ACR-SYS-20260821-005`. Its Gate 0A, schema-8, terminal-closeout and trigger-
guidance changes passed repository, adapter, migration, privacy, packaging,
adversarial and release-evidence validation. The published `v0.2.2` tag and
assets remain unchanged as the rollback source.

The historical `system-release-validation-v0.2.1.json` asset is mislabeled internally: it
describes the v0.2.0 archive. The v0.2.1 ZIP and checksum remain valid; the
v0.2.2 evidence guard records the mismatch and makes validation fail when report
name, archive name, embedded inventory version, digest or byte count disagree.

## ChatGPT and Codex

A GitHub marketplace can provide an installable custom source on supported
surfaces. It does not automatically create a listing in OpenAI's universal
Plugins Directory.

OpenAI plugin `0.2.3` is published in the universal directory and remains the
live rollback version. The OpenAI Platform shows the released version as
read-only and provides **Upload draft** at the plugin level; the separate
released-version menu provides **Unpublish**. Therefore the safe update plan is
to upload the exact validated 0.2.4 draft under the existing plugin, pass scans
and review, and publish it without deleting or unpublishing 0.2.3 first.

On surfaces that flatten skills-only bundles, the umbrella is shown as the
orchestrator skill rather than a separate parent row. Every local 0.2.4
installation still requires an exact-version, post-restart, fresh-task picker
and six-skill check. Such checks are host-specific evidence, not a global push
to other users, devices, accounts or workspaces. App version, account access and
workspace policy may restrict installation, and the Codex IDE extension does
not support plugins.

A universal version update requires the same verified publisher, accurate
public metadata and policies, test cases, automated scans, review and a later
developer publish action. Until 0.2.4 is actually live, describe it as a
**prepared skills-only OpenAI update candidate** and continue to identify 0.2.3
as the directory version.

## Other systems

The repository-defined GitHub Copilot marketplace currently distributes
`0.2.3-copilot.1`; `0.2.4-copilot.1` is the inactive update candidate. It is not
a paid GitHub commercial Marketplace listing and adds no publisher-operated
service. Claude Code, OpenCode and Antigravity adapters remain project-local
configuration packages. Presence in GitHub is not proof of installation,
activation or end-to-end testing in a user's account; each README distinguishes
documented compatibility from exercised validation.
