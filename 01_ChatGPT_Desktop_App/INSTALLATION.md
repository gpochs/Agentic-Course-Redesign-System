# Install and start one course

## Status first

Version `0.2.0` can be tested from this local repository as a custom marketplace
on supported surfaces. The planned GitHub repository is
<https://github.com/gpochs/Agentic-Course-Redesign-System>, but it is not yet
published or verified live. The plugin is not in OpenAI's universal Plugins
Directory and has not passed OpenAI review.

## Supported custom-marketplace route

OpenAI documents repo marketplaces for Work mode and Codex in the ChatGPT
desktop app. Codex CLI can add local or Git-backed marketplace sources. The
Codex IDE extension does not support plugins.

For this extracted or checked-out repository:

1. Keep the complete repository together at a short, writable path.
2. In a terminal, add the repository root as the local marketplace source:

   ```text
   codex plugin marketplace add "C:\path\to\Agentic-Course-Redesign-System"
   ```

3. Restart the ChatGPT desktop app.
4. Open the Plugins Directory in Work mode or Codex, choose **Agentic Course
   Redesign System**, open **Agentic Course Redesign**, and install it.
5. Start a new Work or Codex chat before invoking a bundled skill.

In Codex CLI, start `codex`, enter `/plugins`, choose the configured marketplace,
install or enable the plugin, and start a new session.

If the CLI command is absent or the custom source does not appear, verify the
installed app/CLI version and workspace policy. Use the portable project-template
route rather than claiming installation succeeded.

## Future GitHub route

Only after the repository and `v0.2.0` ref are actually public and verified:

```text
codex plugin marketplace add gpochs/Agentic-Course-Redesign-System --ref v0.2.0
```

Then restart the ChatGPT desktop app, select the new marketplace source, install
the plugin, and start a new chat. Until publication is confirmed, that command
is documentation for the intended release route, not a working-download claim.

## Workspace sharing boundary

A workspace admin may publish an installed local plugin to selected workspace
roles if workspace policy permits. That makes it a workspace plugin only. It
does not publish the plugin to OpenAI's universal public directory.

Universal discovery requires a separate skills-only submission through the
OpenAI Platform, automated scans, review, approval, and an explicit publisher
publish action. See `openai-submission/review/LISTING_METADATA_CHECKLIST.md` for
the unresolved owner-supplied fields.

## Start one isolated course

Before setup:

- create one project and one short folder for one course only;
- confirm that local or OneDrive storage is permitted for every source class;
- exclude student personal data, submissions, grades, credentials, and secrets;
- decide which approved source classes may leave the device, if any; and
- have Python 3 available for scaffold and validation helpers.

Then:

1. Start a new Work or Codex chat with the plugin enabled.
2. Ask: **Set up a protected redesign project for one course.**
3. Review the exact target and no-overwrite preview.
4. Approve scaffold creation only for that target.
5. Add current course files under `00_Source_Materials/` and contextual evidence
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
