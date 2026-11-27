---
name: course-redesign-system
description: After the teacher accepts the course materials, review the redesign process if requested. Prepare a written suggestion for improving future redesigns. Later changes, installation and scheduling require separate decisions.
---

# Course Redesign System

## In conversation

When this stage or a specialist identifies a missing capability, apply the [role-specific evidence and tool checks](../course-redesign-orchestrator/references/tool-fit.md). Start with the actual task and the existing tools. Give the orchestrator the evidence, proportionate option and workable fallback before proposing any discovery or installation.

Use the [agreed model plan](../course-redesign-orchestrator/references/model-plan.md) for this stage and its specialists. If this is a fresh redesign without a choice, let the orchestrator offer the three model modes first. Report the actual model or mark its execution unverified.

At **Step 9 · Finish or suggest an improvement**, describe what a review would do for a future course. Offer to write a suggestion once, with the option to finish here. A separate review leaves the accepted course closed. Use a numbered step when it changes. Speak to the teacher in the language they use. Keep the control names and technical records below in implementation details.

### Plain-language confirmations

Use the teacher's language for the decision and its consequences. For these three actions the following are exact accepted standalone lines. Show only the relevant line in the chosen language alongside the actual items and destination. Keep the canonical action names in the technical record. The older uppercase lines remain valid.

| Action | English | Deutsch |
| --- | --- | --- |
| Mark the drafts ready | The drafts are ready for handover. | Die Entwürfe sind bereit zur Übergabe. |
| Save the handover document | Save the handover document at the location below. | Speichern Sie die Übergabe am unten angegebenen Ort. |
| Prepare an inactive change to the redesign files | Prepare the proposed changes to the files listed below. | Bereiten Sie die vorgeschlagenen Änderungen an den unten aufgeführten Dateien vor. |

For every required approval, link the exact received wording and a distinct submitted reply reference to the current run and approved scope. Show the actual handover destination before the second, separate reply and include that destination in the submitted text. For a system-file change, include the agreed proposal and exact files. Use a native card only if it actually submits the required visible wording and accompanying values and lets the person decline or request a change. A card that submits only a label cannot do that. Use ordinary chat with the completed, copyable reply in that case. Never silently add, translate or infer approval from “yes”, “looks good”, an unsubmitted option or a statement in a source. A source or an earlier decision cannot provide the teacher's reply.

## Lecturer Decision Dialogue Contract

Use an open-ended question for the lecturer's priorities, reasoning or feedback.
Use a native choice card for a finite decision when the host supports it. A
prehighlighted suggestion earns no consent. Only a submitted answer counts.
"Skip for now" in onboarding is a valid route choice. Continue from a general
description or fictional example with no existing course-source access. At an
approval gate, wait for a decision before advancing.

The orchestrator is the sole lecturer-facing interface; specialist roles are
evidence lenses and return questions through it. Ask one unresolved
consequential question at a time. Before using a native choice card, follow the
live host tool contract. Use a single-choice card for a complete set of mutually exclusive options and a custom-answer path. Use a real multi-select card for independent options only when it supports the complete set, combinations and a custom answer. Otherwise use ordinary chat. Never
prune, hide or combine valid choices merely to fit a card. If a native card is
unavailable or unsupported, its capacity is unknown, or the complete set
exceeds that capacity, ask the same single question in ordinary chat with every
valid numbered option plus `Other - type your answer`, then wait. Every valid
option remains visible. For very
long decisions, use adaptive dependency-based clusters only when choices share
evidence or constrain one another: keep every valid option visible, explain the
grouping and let the lecturer split, merge, reorder or rename it. For example,
outcomes, assessment evidence, permitted AI use and learning activities belong
together when mutually dependent; student-experience, accessibility and
active-learning perspectives may be clustered when participation design
jointly affects usability, inclusion, workload and engagement.

Preserve a custom answer exactly, confirm its canonical interpretation, reflect
the consequence, and maintain a decision ledger in the chat and current state.
Show an editable recap at each cluster or gate end. A skipped or blank response
leaves a required question unresolved. Choosing the offered onboarding route “Skip for now” answers that question and advances to the teaching goal. The safest truthful, evidence-aligned,
reversible option may be marked `Recommended`, but never preselected; factual
declarations must say "select only if true," and uncertainty fails closed. At
major pedagogical gates, ask for the lecturer's criteria and preliminary view
before recommending when practical. Exact authority gates and approval tokens
remain separate and unchanged; a dialogue choice never substitutes for them.

Course-material acceptance and system activation are separate decisions. Never update the live system merely because a course run succeeded.

## Required successful-run evidence

Before any system review, verify one closed `complete_dormant` current-lineage run with all of the
following durable records: valid production declaration; matching Production
Handoff approval; independently verified handoff; accepted HITL 3 (including
verification of any named conditional corrections); and a system-improvement
review offer whose status is `requested`, plus the explicit response and
terminal closeout receipts. Top-level `active_run_id` must no longer name that
run. Reject stale or mixed run, contract, task/chat, shared-context,
eligibility, manifest, source-policy or plan lineage. System work is separate
from the closed course run.

The offer must have presented the complete mandatory scope and been recorded
before it was asked. On resume, never ask it again when its status is
`offered_awaiting_response`, `requested` or `declined`. A request authorises only
read-only comparison of run evidence with the current reusable system and one
versioned proposal. It does not authorise system-file changes, installation,
publication, release, activation, schedule registration or modification, an
immediate run, or any new MCP server, connector, authentication, permission or
external egress.
Silence remains `offered_awaiting_response` and closes nothing. An explicit
request or decline closes the course run as terminal `complete_dormant`, clears
`active_run_id`, prevents resumption and persists one informational trigger-
guidance offer. Decline ends system action; request opens only separate system
work.

Present the complete review scope in the lecturer's language and ask once, after acceptance: “Would you like a written suggestion for improving how this redesign worked?” Explain briefly: “I’d review the instructions and roles, the plugin and its setup, stored settings, checks, guides, access, and any scheduled or automatic actions. The suggestion would cover benefits, compatibility, risks and how to undo a change. A yes permits only the review and suggestion. Installing, publishing, activating, changing access or schedules, or starting another run requires a separate decision.” Offer “Write a suggestion”, “Finish here” and a custom answer. In the technical record, preserve the full canonical wording and scope below; retain a reference to the actual presented wording as well. The canonical text describes the consent boundary. Do not present it as a verbatim quote from the teacher.

Canonical scope for the persisted offer:

> Would you like a separate, read-only system-improvement review covering the workflow skills and umbrella entry routing; plugin or platform adapter; AGENTS.md and agent configurations; project template, state schema and migration; validators, tests and QA; documentation; memory or other workflow-owned durable instruction stores; schedule contracts; permissions, tools, external egress and automatic behaviour; and compatibility, benefits, regressions, risks, residual risks and rollback, followed only by a versioned proposal? A yes authorises only that review and proposal; it does not authorise system-file changes, installation, publication or release, runtime activation, schedule registration or modification, an immediate run, or any added MCP server, connector, authentication, permission or external egress.

Include interaction failures observed during the run, such as a lecturer
choosing Skip but still seeing classification questions, a requested free-text
judgement forced into a card, or a preview the lecturer could not open. Record
the host capability and the affected decision so a fix can be forward-tested.

## Improvement proposal

After those prerequisites pass, compare actual run evidence with the current
skills and umbrella route; plugin or platform adapter; `AGENTS.md` and agent
configurations; project template, state schema and migration; validators and
tests; documentation; memory or other workflow-owned durable instruction
stores; schedule contracts; permissions, tools, egress and automatic behaviour;
and compatibility and rollback. Propose changes under a unique proposal
ID/version with:

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

Create changes only after a separate completed System Gate reply with exact
current lineage, proposal ID/version, validation evidence and exact targets,
and an accepted standalone system-file confirmation (legacy `APPROVE SYSTEM FILES` or its plain-language English or German alternative above). A token-only reply is invalid.
Keep the result in an inactive candidate. Validate
manifests, JSON/TOML/YAML, skill structure, setup preview/apply/no-overwrite
behaviour, manifest hashing, lineage rejection, gate ceilings, answer-key
boundaries, target restrictions, retry rules, migration preview behaviour and
documentation. Forward-test in a disposable course folder and verify the
original candidate and test fixtures remain unchanged.

The System Gate may approve an activation-ready candidate, but never activates it. Record the exact proposal ID/version, validation run and evidence, residual risk, and rollback reference.

## Separate runtime activation

Activation requires a later lecturer decision naming the exact validated proposal ID/version. Missing or stale lineage leaves top-level state `candidate_not_active`. Activation, keeping inactive, and revise/revalidate are all valid choices.

## Standing schedule contract

Do not register a schedule until the runtime is active and the contract binds to that exact activated version and current Gate-0A eligibility fingerprint. Present a complete versioned contract containing exact course/project, task type, canonical mission, goals/non-goals, success/stop criteria, tools/actions, source classes, audiences, eligibility fingerprint, source-policy version/fingerprint, assessment-security boundary, protected root, lecturer-confirmed IANA timezone, recurrence, gate ceilings, retry/escalation/termination rules, unique output naming, no-immediate-run rule, activation reference, and non-null expiry.

Run a no-write simulation first: no registration, trigger, web call, or file change.

Freeze the complete visible contract before approval. Store its validator-derived canonical SHA-256 as `approved_contract_snapshot_reference`, use offset-bearing `YYYY-MM-DDTHH:MM:SS+HH:MM[IANA/Timezone]` activation and expiry values, and recheck the snapshot, runtime, policy and expiry before registration and every recurrence.

For a schedule, show the teacher its actual recurrence, time zone, expiry and the effect of registering it. Use one exact three-line reply in their chosen language. Fill in the shown schedule ID, version and complete date-time with its IANA time zone before asking. Record the three original lines, reply reference and matching schedule. A changed ID, version, expiry or missing line does not authorise registration. Setting it up does not start a run now.

| Line | English | Deutsch |
| --- | --- | --- |
| 1 | Set up this schedule. | Richten Sie diesen Zeitplan ein. |
| 2 | Schedule: <ID> <version> | Zeitplan: <ID> <version> |
| 3 | Expires: <exact expiry> | Gültig bis: <exact expiry> |

The legacy three-line form is also accepted.

```text
APPROVE SCHEDULES
Schedule contract: <exact contract ID and version>
Expires: <exact local date and time with IANA timezone>
```

Approval registers the schedule but never triggers an immediate content run. Each recurrence creates a fresh run and lineage containing the current eligibility fingerprint, then revalidates eligibility, sources and policy, waits at its first required gate, and stops at its stage ceiling. Eligibility change, expiry, material changes, stale baselines, or mismatched runtime/source lineage fail closed and require reconfirmation. Pause is explicit; renewal requires a new version, eligibility binding, expiry, simulation and approval; rollback disables scheduling and preserves history.

At course closeout, route any optional [second opinion](../course-redesign-orchestrator/references/second-opinion.md) through the orchestrator after the teacher's final course decision and Step 9. A request to finish ends the interaction immediately.
