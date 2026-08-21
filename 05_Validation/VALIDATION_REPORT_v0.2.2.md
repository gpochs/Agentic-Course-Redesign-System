# Repository validation report — v0.2.2 release source

- Proposal: `ACR-SYS-20260820-004`
- Release version: `0.2.2`
- Validation date: 2026-08-21
- Base release: public `v0.2.1`
- Status: **PASS — validated repository release source**
- Authority boundary: repository publication does not install, activate, or
  schedule v0.2.2

This report covers the shared workflow core, the ChatGPT Desktop/Codex custom
plugin and public-source mirror, the Portable Core adapter, GitHub Copilot,
Claude Code, OpenCode, Google Antigravity, current documentation, and the
repository-level release and regression controls. The completed poetry-course
materials were not opened for redesign and no course-material path was changed.

## Workflow outcome

Every explicit orchestration entry now preserves this order:

1. Gate 0 and Gate 1;
2. all five Stage-A specialist perspectives and Gate 2A;
3. bounded research, cross-review, red-team reconciliation, and Gate 2B;
4. blueprint and exact material targets at Gate 3;
5. one-at-a-time production and independent QA;
6. current-lineage `DECLARE PRODUCTION COMPLETE` in one completed reply;
7. a second completed reply repeating the exact current-run handoff target and
   containing `APPROVE PRODUCTION HANDOFF`, followed by independent verification;
8. current-lineage HITL 3 final acceptance;
9. a persisted, exactly-once system-improvement-review offer whose complete
   scope covers skills and umbrella routing, plugin or adapter, AGENTS.md and
   agent configurations, project template/state/migration, validators/tests/QA,
   documentation, workflow-owned durable memory, schedules, permissions/tools/
   egress/automatic behaviour, compatibility, risks, residual risks, and rollback;
10. read-only review and one versioned proposal only after a separate yes;
11. exact System Gate approval, separate runtime activation, and optional
    expiring schedule approval as later independent decisions.

Schema 7 records the resumable terminal checkpoints. The v6-to-v7 helper is
preview-only, never writes its input, preserves protected values, and now runs
the full schema-7 validator before calling either a migrated candidate or an
existing schema-7 input valid.

## Final validation matrix

| Scope | Result |
|---|---|
| Repository semantic and mirror validator | PASS: 314 source files, six shared skills, five adapter manifests, zero findings |
| Repository unit suite | PASS: 47/47 |
| Shared schema-7 validator and migration tests | PASS: 31/31, included in the 47-test repository suite |
| ChatGPT/Codex plugin unit suite | PASS: 22/22 |
| ChatGPT/Codex disposable forward test | PASS: 41/41 |
| Public-source validation | PASS: 37/37, 52 runtime files, six skills, nine positive and eight negative reviewer cases |
| Static parsing | PASS: 12 JSON, 22 TOML, 12 YAML, 22 Python, four SVG |
| Official plugin and quick-skill validators | PASS: 14/14 |
| Public scrub | PASS: 145 scoped files, six skills, ten agents, zero findings |
| Custom/public runtime parity | PASS: 50 scoped runtime files, zero differences |
| Portable and thin adapters | PASS: four v0.2.2 adapters, 48 frozen non-manifest files, 39 overlay files, 30 native role wrappers |
| Google Antigravity | PASS: adapter validator plus 15/15 tests; six skills, four workflows, ten agents, zero secret findings |
| Independent red-team mutation probes | PASS after every reported fail-open or stale-evidence defect was corrected and retested |
| Diff and cache hygiene | PASS: `git diff --check`; zero source-tree `.pyc` files |

The canonical schema trio is byte-identical across the shared core, custom
plugin, public-source mirror, and Antigravity:

| File | Bytes | SHA-256 |
|---|---:|---|
| `state.json` | 48,320 | `AC5B629FA4FA3ED10F959BAC547B9BA3BD5D30636C2F46EA36F30845F5352628` |
| `migrate_state_v6_to_v7.py` | 24,891 | `B280A883DD08A06BD89927F26F6FCC3C1816E9C77E1E4904A98194417CC13031` |
| `validate_state.py` | 77,949 | `4EBFDD48010C5355DB05B092832408210F4D722CF4CACC3CB16852779718DE80` |

Disposable ignored bundles are used only to test deterministic packaging,
inventory binding, checksums, and release-evidence validation. Their generated
report supplies the exact archive hash after the source tree is frozen; no
disposable bundle is a publication or release asset.

## Safety and authority result

- Exactly six skills remain available through the plugin source.
- Both plugin manifests remain skills-only. They add no MCP server, app,
  connector, hook, authentication, permission, schedule, or other integration.
- Default state remains `candidate_not_active`; `schedules=[]`; automatic
  activation and immediate runs remain forbidden.
- The validator rejects combined production/handoff replies, combined HITL 3/
  system-review replies, another run's handoff, token-only or mismatched System
  Gate records, activation without its separate exact-version evidence, and a
  schedule without active-runtime matching, successful no-write simulation,
  exact approval records, recurrence, timezone, and expiry.
- No user automation was created, changed, or removed during candidate work.
- No protected course source or generated course material was modified.

## Pre-release installed-state checkpoint

Before v0.2.2 publication, the user-level installation remained v0.2.1. That
plugin was enabled, its manifest remained byte-identical during candidate work,
the registered marketplace was pinned to the v0.2.1 tag/revision, and a fresh
supported Codex task loaded the umbrella with all six bundled skills available.
This is historical v0.2.1 evidence, not proof of a v0.2.2 installation. The
historical v0.2.1 system-validation JSON is not matching evidence for its
archive; the new evidence guard rejects that mismatch.

The Codex configuration file was automatically reserialised by the desktop app
during an unrelated task startup, changing two bytes. A forensic command audit
found no plugin, marketplace, or automation mutation during that interval;
the Agentic Course Redesign configuration, installed manifest, and all eleven
pre-existing automation files remained semantically and byte-for-byte stable.

## Residual limits and next gates

- Repository publication does not install, activate, or schedule v0.2.2. The
  exact-version installation and fresh-task picker test remain post-release
  verification steps.
- Antigravity's recorded v0.1.0 source hashes passed manifest validation, but
  the optional historical source root was not supplied for a fresh live rehash.
- Universal OpenAI Plugins Directory submission still requires owner identity,
  organization/project access, legal/support pages, territories, attestations,
  safety scans, review, approval, and a later publisher action.
- The requested 31 May/31 December cadence has not been registered. It still
  requires an active matching runtime, a complete per-course contract with exact
  local time, lecturer-confirmed IANA timezone and expiry, a no-write simulation,
  and its separate exact three-line approval. Manual invocation remains
  on-demand and is not an automation trigger.

Rollback is defined in
`01_ChatGPT_Desktop_App/ROLLBACK_v0.2.2.md`. It preserves the published v0.2.2
and v0.2.1 tags and release evidence, uses a later corrective commit or version
for source rollback, and preserves installed runtimes, course projects, course
materials, approval history, and QA evidence.
