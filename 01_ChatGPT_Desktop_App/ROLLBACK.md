# Rollback and recovery

Current candidate: `ACR-SYS-20260822-007` version `0.2.4`.

The exact current rollback procedure is in `ROLLBACK_v0.2.4.md`. Preserve the
published GitHub/OpenAI/Codex v0.2.3 artifacts and GitHub Copilot
`0.2.3-copilot.1`; do not unpublish the current OpenAI version merely to prepare
an update draft.

## Before activation

No rollback action is needed: leave the candidate inactive and do not install
or distribute it. It has not changed global skills, personal memory, protected
course sources, an active runtime or a schedule.

## After local installation

1. Stop starting new redesign runs.
2. Preserve every course project's source manifest, approvals, produced files,
   QA evidence and run history.
3. Disable or uninstall the exact plugin version through the app surface that
   installed it, or remove only its repository-marketplace registration.
4. Do not delete course folders or lecturer files as part of plugin rollback.
5. If a portable scaffold was copied into an unused empty test project, the
   lecturer may archive that whole test project. For a real or non-empty course
   project, remove nothing automatically; restore the last approved project
   configuration from its recorded snapshot or obtain an exact-target plan.

## After runtime activation

Set the runtime to suspended, reject new triggers, preserve the activation and
validation records, and restore the last validated system snapshot. Any future
activation requires a new proposal version, validation and lecturer decision.

## If a schedule was separately registered

Pause/disable that exact schedule first, preserve its contract and run history,
and verify that no trigger is pending. Schedule rollback does not delete course
outputs. Renewal or re-registration requires a new expiring contract, no-write
simulation and exact three-line approval.
