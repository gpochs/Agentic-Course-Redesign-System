# Rollback and recovery for v0.2.4

Release: `ACR-SYS-20260822-007` version `0.2.4`.

Rollback source: published OpenAI/Codex `v0.2.3` and GitHub Copilot
`0.2.3-copilot.1`. The v0.2.4 source is currently an inactive candidate; no
public or local rollback action is needed unless a later separate publication
or installation occurs.

Rollback applies only to candidate changes within
`03_Shared_Workflow_Core/**`, `01_ChatGPT_Desktop_App/**`,
`02_Other_Agentic_Systems/**`, `04_Documentation/**`, and
`05_Validation/**`.

## Before publication or installation

1. Stop candidate work and preserve validation evidence.
2. Revert only v0.2.4 candidate files to the exact v0.2.3 source.
3. Preserve the v0.2.3 Git tag and release, the published OpenAI archive, the
   local `Published` folder, the operational v0.2.3 package and all
   course-project history unchanged.
4. Do not delete or rewrite course projects, course files, runs, approvals,
   handoffs, schedule records, tags, release assets or published archives.

## If v0.2.4 is later published or installed

1. Stop starting new runs with the incompatible candidate and preserve the
   exact failure/smoke-test evidence.
2. Disable or uninstall only exact v0.2.4 on the affected host, then restore
   exact validated v0.2.3 and verify it in a fresh task.
3. If the OpenAI v0.2.4 update is already public, use the Platform's version or
   publication controls deliberately; do not delete the plugin or its v0.2.3
   evidence. The ordinary update plan keeps v0.2.3 published until v0.2.4 is
   ready, so unpublishing v0.2.3 is not a preparation step.
4. For GitHub Copilot, uninstall `0.2.4-copilot.1`, restore
   `0.2.3-copilot.1`, and remove only the additive marketplace update.
5. Preserve all course projects and any existing schedule history. Disable an
   incompatible schedule rather than deleting its contract or receipts.

Rollback never authorises migration application or a course-material run. It
also never authorises upload, publication, installation, activation, schedule
registration, a new tool, permission, authentication or external egress.
