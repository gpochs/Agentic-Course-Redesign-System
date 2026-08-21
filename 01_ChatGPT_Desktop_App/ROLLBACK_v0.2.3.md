# Rollback and recovery for v0.2.3

Release: `ACR-SYS-20260821-005` version `0.2.3`.

Rollback source: published `v0.2.2`. Version v0.2.3 is a validated published
release whose reusable template remains inactive by default. Publication never
starts a course run or registers a schedule; any host installation or
activation remains separately reversible.

## Full-system rollback

1. Stop candidate work and preserve its validation evidence.
2. Restore the canonical targets under `03_Shared_Workflow_Core/**` from the
   reviewed published v0.2.2 source, then restore derived targets under
   `01_ChatGPT_Desktop_App/**` and `02_Other_Agentic_Systems/**` from that same
   source. Do not delete or rewrite course projects.
3. Restore current `04_Documentation/**`, `05_Validation/**` and only the
   repository-level version, provenance, manifest and hash records changed by
   this candidate.
4. Do not delete, move, or rewrite the published v0.2.2 tag or its release
   assets. Keep the published v0.2.1 tag and release assets unchanged.
5. Re-run the complete v0.2.2 validators and generated-mirror comparisons.

Restore canonical shared semantics before platform mirrors. Do not combine a
schema-8 state with schema-7 validators. Preserve every run, source manifest,
approval, handoff, produced artefact and QA record. Disable only an exact
incompatible candidate runtime or schedule if one is later separately created;
preserve its history.

The preview-only migration must not rewrite legacy run objects. Retain any
terminal-history canonical receipts with their source record, and resolve a
nonterminal or malformed legacy run under a separate reviewed recovery action.

Rollback never authorises migration application or a course-material run. It
also never authorises commit, publication, installation, activation, schedule
registration, tool/permission expansion, deletion of history, or rewriting an
existing release.
