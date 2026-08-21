# Install and start one course

## Status first

Version `0.2.3` is the current published repository release at
<https://github.com/gpochs/Agentic-Course-Redesign-System> as a custom
repository marketplace for supported surfaces. The plugin is not in
OpenAI's universal Plugins Directory and has not passed OpenAI review.

The `v0.2.3` release source is inactive by default. Rollback version `v0.2.2`
was installed and passed a post-restart fresh-task smoke test on the tested
host; v0.2.3 requires its own exact-version installation check. Host evidence
does not generalise to other users, devices, accounts or workspaces.
Publishing any release does not
install or enable the plugin, activate a reusable runtime, register a schedule,
or begin a course run. Report an installation only after the supported plugin
manager and a fresh-task picker check confirm that exact version.

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
the plugin, and start a new chat. Use this command only when the installed CLI
actually exposes `codex plugin marketplace`. Otherwise use the supported
ChatGPT Desktop marketplace UI or the portable project-template fallback; an
absent command is not evidence of successful installation.

The rollback evidence confirms installed/enabled user-level `0.2.2` after a
desktop restart and fresh-task picker/umbrella check, with all six bundled
skills available. Confirm `0.2.3` separately after installation and do not use
either result as evidence for another host.

## Workspace sharing boundary

A workspace admin may publish an installed local plugin to selected workspace
roles if workspace policy permits. That makes it a workspace plugin only. It
does not publish the plugin to OpenAI's universal public directory.

Universal discovery requires a separate skills-only submission through the
OpenAI Platform, automated scans, review, approval, and an explicit publisher
publish action. See `openai-submission/review/LISTING_METADATA_CHECKLIST.md` for
the unresolved owner-supplied fields.

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
3. Review the exact target and no-overwrite preview.
4. Approve scaffold creation only for that target.
5. Only after Gate 0A permits processing, add current course files under `00_Source_Materials/` and contextual evidence
   under `00_Context/`.
6. Review and approve the source manifest and versioned source-access policy
   before specialist analysis.

The standard project also contains `01_Control/`, `02_Working_Notes/`,
`03_Research/`, `04_Working_Copies/`, `05_Approved/`, `06_QA_and_Review/`, and
`07_System_Improvement/`. The lecturer remains the decision-maker at every gate.

## Portable fallback

If custom marketplace support is unavailable, follow
`PORTABLE_SETUP_WINDOWS.md` or `PORTABLE_SETUP_MACOS.md`. That route copies the
same project `AGENTS.md`, control schemas, and ten custom-agent definitions into
one approved course folder, but it does not install the six skills as a plugin.
