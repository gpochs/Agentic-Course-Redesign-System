# Shared workflow core

This directory is the course-independent semantic source for all platform
adapters. Version 0.2.2 is an inactive candidate under proposal
`ACR-SYS-20260820-004`; it does not modify the installed or released runtime.

- `agent-skills/` contains six platform-neutral Agent Skills.
- `course-project-template/` is the inactive one-course scaffold without a
  platform-specific agent registry.
- `scripts/` contains preview-first, no-overwrite local utilities.
- `scripts/migrate_state_v6_to_v7.py` previews the fail-closed schema-6 to
  schema-7 migration. It has no apply or write mode.
- `PARTICIPANT_QUICK_START.md` is the platform-neutral onboarding reference.

Schema 7 routes the umbrella entry through Gate 0, persists production
declaration and handoff approval/verification before HITL 3, and records the
mandatory post-HITL-3 system-improvement question exactly once. A request for
that review authorises only read-only review and a versioned proposal. It does
not authorise system-file changes, installation, publication, activation,
scheduling, added permissions or an immediate run.

Platform folders may add discovery metadata, native agent wrappers, rules or
workflows. They must not change source access, lecturer gates, audience
separation, assessment security, exact-target write authority, activation or
schedule semantics. Generated adapter copies record their source hashes and are
checked for drift before release.

The core does not activate itself. Copying the scaffold does not read a course,
approve Gate 0, enable tools, register a runtime or create a schedule.
