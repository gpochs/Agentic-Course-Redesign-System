# Install and start one course

## Status first

Version `0.2.3` is the current published GitHub release and published OpenAI
Plugins Directory version. Version `0.2.4` is only an inactive source
candidate: it is not yet uploaded, published, installed, enabled or live in a
picker. Keep using v0.2.3 until the later v0.2.4 publication and exact-version
smoke test finish. Host evidence never generalises to other users, devices,
accounts or workspaces.
Publishing any release does not
install or enable the plugin, activate a reusable runtime, register a schedule,
or begin a course run. Report an installation only after the supported plugin
manager and a fresh-task picker check confirm that exact version.

## Public Plugins Directory route

On a supported ChatGPT desktop surface, open **Plugins**, search for **Agentic
Course Redesign**, open the public result, and choose **Install**. Start a new
Work or Codex task, type `@`, and choose **Agentic Course Redesign**. A usable
installation should expose the umbrella entry and all six bundled skills.
Workspace policy, app version and account entitlements may still hide or block
the listing.

When v0.2.4 is ready, the publisher should update the existing OpenAI plugin:

1. keep published v0.2.3 available;
2. open the existing plugin page and choose its plugin-level **Upload** action;
3. upload the exact validated v0.2.4 skills-only ZIP as a new draft;
4. recheck publisher metadata, prompts, tests, regions and attestations;
5. pass the platform scan/review flow and explicitly publish v0.2.4; and
6. verify the live directory version before updating availability claims.

Do not unpublish or delete v0.2.3 first. Use **Unpublish** only when the owner
deliberately wants to delist the current public version or an emergency rollback
requires it.

## Supported custom-marketplace route

OpenAI documents repo marketplaces for Work mode and Codex in the ChatGPT
desktop app. Some Codex CLI releases expose local or Git-backed marketplace
commands. The release-validation host's Codex CLI `0.118.0` did not expose that
command, so no CLI installation is claimed for that build. The Codex IDE
extension does not support plugins.

For this extracted or checked-out repository:

1. Keep the complete repository together at a short, writable path.
2. If the installed CLI exposes `codex plugin marketplace`, add the repository
   root as the local marketplace source:

   ```text
   codex plugin marketplace add "C:\path\to\Agentic-Course-Redesign-System"
   ```

3. Restart the ChatGPT desktop app.
4. Open the Plugins Directory in Work mode or Codex, choose **Agentic Course
   Redesign System**, open **Agentic Course Redesign**, and install it.
5. Start a new Work or Codex chat before invoking a bundled skill.
6. Type `@` and choose **Agentic Course Redesign** for the complete workflow.
   If the app lists bundled skills instead of the parent plugin row, choose the
   entry with that exact name; it is the umbrella orchestrator and routes the
   remaining skills internally.

On CLI builds that provide marketplace commands, start `codex`, enter
`/plugins`, choose the configured marketplace, install or enable the plugin,
and start a new session.

If the CLI command is absent or the custom source does not appear, verify the
installed app/CLI version and workspace policy. Use the portable project-template
route rather than claiming installation succeeded.

## Public GitHub route

An installed app or CLI build that exposes repository marketplaces may use
this pinned public source:

```text
codex plugin marketplace add gpochs/Agentic-Course-Redesign-System --ref v0.2.3
```

Then restart the ChatGPT desktop app, select the new marketplace source, install
the plugin, and start a new chat. Use this pinned v0.2.3 command until a v0.2.4
GitHub release is separately published. Use the command only when the installed CLI
actually exposes `codex plugin marketplace`. Otherwise use the supported
ChatGPT Desktop marketplace UI or the portable project-template fallback; an
absent command is not evidence of successful installation.

Confirm the exact installed version after a restart and fresh-task
picker/umbrella check; do not use a result from this development host as
evidence for another participant.

## Workspace sharing boundary

A workspace admin may publish an installed local plugin to selected workspace
roles if workspace policy permits. That makes it a workspace plugin only. It
does not publish the plugin to OpenAI's universal public directory.

The public v0.2.3 listing was created through the separate OpenAI Platform flow.
Every later public version still requires a new plugin-level upload draft,
automated checks and the applicable publisher review/publish flow. See
`openai-submission/review/LISTING_METADATA_CHECKLIST.md` for the v0.2.4 update
checks.

## Start one isolated course

Before source intake:

- create one project and one short folder for one course only;
- complete Gate 0A using material category and exact processing environment
  plus sensitivity and assessment-security classifications/authority only,
  without disclosing paths, filenames, source lists, content or hashes;
- confirm explicit AI-processing authority; public accessibility alone is not
  enough;
- route institution-internal/restricted material to an approved institutional
  environment; separately classify student personal data and protected
  assessment/answer-key handling; and segregate or clarify mixed/uncertain
  material or security classifications;
- confirm that local or OneDrive storage is permitted for every eligible source class;
- exclude student personal data, submissions, grades, credentials, and secrets;
- decide which approved source classes may leave the device, if any; and
- have Python 3 available for scaffold and validation helpers.

Then:

1. Start a new Work or Codex chat with the plugin enabled.
2. Ask: **Set up a protected redesign project for one course.**
3. Answer Gate 0A one consequential question at a time. Use a native choice
   card only when the live host tool contract can present the complete option
   set plus a custom answer. In the current verified Codex contract, that means
   exactly two or three explicit choices plus client-added free-form `Other`.
   Work's exact maximum is not independently documented or exposed here. If
   capacity is unknown, unavailable or exceeded, ask the same single question
   in ordinary chat with every valid numbered option plus `Other`, followed by
   a wait. Valid choices are never pruned, hidden or combined merely to fit a
   card. Long dependency-based chunks keep every valid option visible, and the
   lecturer may split, merge, reorder or rename the grouping. A blank or Skip
   never counts as approval.
4. Review the exact target and no-overwrite preview.
5. Approve scaffold creation only for that target.
6. Only after Gate 0A permits processing, add current course files under `00_Source_Materials/` and contextual evidence
   under `00_Context/`.
7. Review and approve the source manifest and versioned source-access policy
   before specialist analysis.

The standard project also contains `01_Control/`, `02_Working_Notes/`,
`03_Research/`, `04_Working_Copies/`, `05_Approved/`, `06_QA_and_Review/`, and
`07_System_Improvement/`. The lecturer remains the decision-maker at every gate.

## Portable fallback

If custom marketplace support is unavailable, follow
`PORTABLE_SETUP_WINDOWS.md` or `PORTABLE_SETUP_MACOS.md`. That route copies the
same project `AGENTS.md`, control schemas, and ten custom-agent definitions into
one approved course folder, but it does not install the six skills as a plugin.
