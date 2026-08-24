# Rollback and recovery for OpenAI/Codex v0.2.5

Proposal: `ACR-SYS-20260825-009`. Package version: `0.2.5`. Base workflow:
`0.2.4`.

The preserved rollback source is the published and installed OpenAI/Codex
v0.2.4 package. During candidate preparation no rollback action is needed
because v0.2.4 remains unchanged and active.

## Before publication or installation

1. Stop candidate work and preserve its validation evidence.
2. Revert only the v0.2.5 package metadata, listing/review records, focused
   validators and current-status documentation.
3. Preserve all v0.2.4 tags, releases, public archives, installed files,
   course projects, schedule contracts and history.

## If v0.2.5 is later published or installed

1. Preserve the exact failure and smoke-test evidence.
2. Disable or uninstall only exact v0.2.5 on the affected host and restore
   exact validated v0.2.4; verify it in a fresh task.
3. Use the OpenAI Platform's version or publication controls deliberately if a
   public rollback is necessary. Do not delete the plugin or its v0.2.4
   evidence.
4. Revert only the description-maintenance commit if the repository candidate
   must be withdrawn.

Rollback never authorises a course run, workflow/schema migration, publication,
schedule, connector, MCP server, authentication, permission or external egress.
