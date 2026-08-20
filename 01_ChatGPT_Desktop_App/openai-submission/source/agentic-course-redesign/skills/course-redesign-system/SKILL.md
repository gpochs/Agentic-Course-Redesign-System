---
name: course-redesign-system
description: Review, validate, activate, schedule, pause, renew, or roll back the reusable agentic course-redesign system after a successful course run. Use for skills, plugin, AGENTS.md, custom agents, state schemas, memory, validators, runtime activation, or scheduled workflow contracts.
---

# Course Redesign System

Course-material acceptance and system activation are separate decisions. Never update the live system merely because a course run succeeded.

## Improvement proposal

After HITL 3, compare actual run evidence with the current skills, agents, project template, state schema, validators, and documentation. Propose changes under a unique proposal ID/version with:

- problem demonstrated by the run;
- affected system files;
- exact proposed change;
- benefit and possible regression;
- migration/compatibility impact;
- tests and success criteria;
- residual risk and rollback; and
- lecturer choices: keep current, revise proposal, or validate candidate.

Do not include course content, answer keys, personal data, or copyrighted assets in the reusable plugin.

## System gate and validation

Create changes only in an inactive candidate. Validate manifests, JSON/TOML/YAML, skill structure, setup preview/apply/no-overwrite behaviour, manifest hashing, lineage rejection, gate ceilings, answer-key boundaries, target restrictions, retry rules, and documentation. Forward-test in a disposable course folder and verify the original candidate and test fixtures remain unchanged.

The System Gate may approve an activation-ready candidate, but never activates it. Record the exact proposal ID/version, validation run and evidence, residual risk, and rollback reference.

## Separate runtime activation

Activation requires a later lecturer decision naming the exact validated proposal ID/version. Missing or stale lineage leaves top-level state `candidate_not_active`. Activation, keeping inactive, and revise/revalidate are all valid choices.

## Standing schedule contract

Do not register a schedule until the runtime is active and the contract binds to that exact activated version. Present a complete versioned contract containing course/project, task type, canonical mission, goals/non-goals, success/stop criteria, tools/actions, source classes, audiences, source-policy version/fingerprint, assessment-security boundary, protected root, timezone, recurrence, gate ceilings, retry/escalation/termination rules, unique output naming, no-immediate-run rule, activation reference, and non-null expiry.

Run a no-write simulation first: no registration, trigger, web call, or file change.

Register only after one lecturer reply containing exactly and only these completed lines with matching values:

```text
APPROVE SCHEDULES
Schedule contract: <exact contract ID and version>
Expires: <exact local date and time with IANA timezone>
```

Approval registers the schedule but never triggers an immediate content run. Each recurrence creates a fresh run and lineage, revalidates sources/policy, waits at its first required gate, and stops at its stage ceiling. Expiry, material changes, stale baselines, or mismatched runtime/source lineage fail closed. Pause is explicit; renewal requires a new version, expiry, simulation, and approval; rollback disables scheduling and preserves history.
