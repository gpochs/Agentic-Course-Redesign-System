# Shared workflow core

This directory is the course-independent semantic source for all platform
adapters. Version 0.2.3 is the published release source under proposal
`ACR-SYS-20260821-005`; its reusable template remains inactive by default and
does not modify a course or register a schedule merely by being installed.
The same workflow adapts to lecturer-supplied school, vocational, professional,
higher-education or other explicitly described course contexts. It must not
infer a subject, learner level, qualification framework, assessment form or
institutional policy from the plugin or from an earlier course.

- `agent-skills/` contains six platform-neutral Agent Skills.
- `course-project-template/` is the inactive one-course scaffold without a
  platform-specific agent registry.
- `scripts/` contains preview-first, no-overwrite local utilities.
- `scripts/migrate_state_v7_to_v8.py` previews the fail-closed schema-7 to
  schema-8 migration. It has no apply or write mode. It preserves only bounded,
  immutable terminal run history and inactive schedule history through indexed
  canonical-SHA256 receipts; malformed/non-terminal runs and malformed,
  active or still-registered schedules fail before candidate emission. The
  older v6-to-v7 helper remains available for staged compatibility.
- `PARTICIPANT_QUICK_START.md` is the platform-neutral onboarding reference.

Schema 8 routes the umbrella entry first through Gate 0A, before any course
source path, filename, list, read, copy, hash or other source intake is exposed.
Gate 0A fingerprints the declared material, exact processing environment,
sensitivity, student-data and assessment-security classifications and handling
authority. Null or inconsistent declarations and records awaiting
reconfirmation do not permit intake.
Public availability alone is not processing authority. Institution-internal or
restricted material in a personal/unmanaged environment is route-only, and
mixed or uncertain material fails closed until segregated or clarified.

After verified HITL 3 acceptance, the mandatory system-improvement question is
recorded and asked exactly once. Silence remains a wait, not a decision. Once
the lecturer explicitly requests or declines the review, the course run closes
as terminal `complete_dormant`, clears `active_run_id`, offers informational
fresh-trigger guidance once, and can never resume. Any requested system work is
separate. Every later manual or scheduled trigger creates a fresh run and
lineage bound to the current eligibility fingerprint; scheduling remains a
separate expiring approval and never causes an immediate run. A scheduled
trigger records the immutable approved-contract snapshot and its valid offset
timestamp; active triggers must fall within the activation/expiry window, while
an on/after-expiry trigger records an expired no-course-action receipt.

Platform folders may add discovery metadata, native agent wrappers, rules or
workflows. They must not change source access, lecturer gates, audience
separation, assessment security, exact-target write authority, activation or
schedule semantics. Generated adapter copies record their source hashes and are
checked for drift before release.

The core does not activate itself. Copying the scaffold does not read a course,
approve Gate 0A or Gate 0, enable tools, register a runtime or create a schedule.
