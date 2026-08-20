# Rollback and recovery for v0.2.1

Candidate: `ACR-SYS-20260820-003` version `0.2.1`.

## Before activation

No runtime rollback is needed: leave the candidate inactive. Removing or
disabling the plugin must not delete course projects, source manifests,
approvals, produced materials, or QA evidence.

## After user-level installation

1. Stop starting new redesign runs.
2. Disable or uninstall only version `0.2.1` through the app surface that
   installed it.
3. Reinstall the last validated plugin version only if its marketplace source
   and checksum are verified.
4. Start a new task after any installation change.
5. Preserve every course project and its recorded state; never roll back course
   content by deleting files.

Runtime activation and scheduling remain separate later decisions. If either
was independently authorised, suspend that exact version or schedule first and
follow its recorded recovery contract.
