# Rollback and recovery for v0.2.2

Release: `ACR-SYS-20260820-004` version `0.2.2`.

## Release-state boundary

The v0.2.2 repository source and matching evidence are published. Release
publication does not install the plugin, activate a reusable runtime, register
a schedule, or begin a course run. No runtime or schedule rollback is required
unless one of those later actions is separately completed.
The bundled v6-to-v7 migration is preview-only and cannot modify a course state
file.

## Full-system source rollback

1. Stop candidate work and preserve validation output that explains the reason.
2. Restore the canonical `03_Shared_Workflow_Core/**` candidate targets to the
   reviewed v0.2.1 base, then restore derived ChatGPT/Codex, portable, GitHub
   Copilot, Claude Code, OpenCode and Antigravity targets under
   `01_ChatGPT_Desktop_App/**` and `02_Other_Agentic_Systems/**` from that same
   base. Do not delete or rewrite course projects.
3. Restore current `04_Documentation/**`, `05_Validation/**`, repository-level
   version/provenance files, `.gitattributes`, `README.md`, `CHANGELOG.md`, and
   only the manifest/hash records changed for this candidate.
4. Do not delete, move, or rewrite the published v0.2.2 tag or release assets.
   Any source correction after publication must use a later commit or version
   with its own validation and rollback evidence.
5. Re-run the complete v0.2.1 repository, shared-core and adapter validators
   against the restored tree, including generated-mirror consistency.
6. Keep the published v0.2.1 tag and release assets unchanged. Do not use the
   stale attached v0.2.1 validation JSON as proof of the v0.2.1 archive; verify
   the archive and checksum directly.

Rollback order matters: restore canonical shared semantics before derived
mirrors, then validate. Never combine a schema-7 state with schema-6 validators
or claim that a preview migration was applied.

## If a later installation or activation occurs

If an explicitly authorised task installs v0.2.2, first stop new
runs, disable only that exact plugin version through the installing surface,
and verify any replacement version and checksum before use. Preserve every
course project, source manifest, approval, handoff, produced artefact and QA
record. If a later separately authorised runtime or schedule exists, suspend
that exact runtime or schedule under its recorded recovery contract before
changing plugin versions.

Rollback never authorises publication, activation, migration application, or
schedule registration.
