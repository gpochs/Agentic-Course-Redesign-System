# Shared workflow core

This directory is the course-independent semantic source for all platform
adapters. It preserves the validated v0.1.0 gates and upgrades only packaging
and portability for v0.2.0.

- `agent-skills/` contains six platform-neutral Agent Skills.
- `course-project-template/` is the inactive one-course scaffold without a
  platform-specific agent registry.
- `scripts/` contains preview-first, no-overwrite local utilities.
- `PARTICIPANT_QUICK_START.md` is the platform-neutral onboarding reference.

Platform folders may add discovery metadata, native agent wrappers, rules or
workflows. They must not change source access, lecturer gates, audience
separation, assessment security, exact-target write authority, activation or
schedule semantics. Generated adapter copies record their source hashes and are
checked for drift before release.

The core does not activate itself. Copying the scaffold does not read a course,
approve Gate 0, enable tools, register a runtime or create a schedule.

