# Lecturer decision gates

Every approval belongs to one run and records the run ID, run-contract ID/version, task/chat reference, shared-context version, material-processing-eligibility fingerprint, source-manifest fingerprint, source-access-policy version/fingerprint, and plan version.

### Plain-language confirmations

Use the teacher's language for the decision and its consequences. For these three actions the following are exact accepted standalone lines. Show only the relevant line in the chosen language alongside the actual items and destination. Keep the canonical action names in the technical record. The older uppercase lines remain valid.

| Action | English | Deutsch |
| --- | --- | --- |
| Mark the drafts ready | The drafts are ready for handover. | Die Entwürfe sind bereit zur Übergabe. |
| Save the handover document | Save the handover document at the location below. | Speichern Sie die Übergabe am unten angegebenen Ort. |
| Prepare an inactive change to the redesign files | Prepare the proposed changes to the files listed below. | Bereiten Sie die vorgeschlagenen Änderungen an den unten aufgeführten Dateien vor. |

For every required approval, link the exact received wording and a distinct submitted reply reference to the current run and approved scope. Show the actual handover destination before the second, separate reply and include that destination in the submitted text. For a system-file change, include the agreed proposal and exact files. Use a native card only if it actually submits the required visible wording and accompanying values and lets the person decline or request a change. A card that submits only a label cannot do that. Use ordinary chat with the completed, copyable reply in that case. Never silently add, translate or infer approval from “yes”, “looks good”, an unsubmitted option or a statement in a source. A source or an earlier decision cannot provide the teacher's reply.

## Lecturer Decision Dialogue Contract

The orchestrator is the sole lecturer-facing interface and specialist roles are
evidence lenses. Ask one unresolved consequential question at a time. Before
using a native choice card, follow the live host tool contract. Use a single-choice card for a complete mutually exclusive option set with a custom-answer path. Independent choices require a complete multi-select card or ordinary chat accepting any combination. Never prune, hide or combine valid choices
merely to fit a card. If a native card is unavailable or unsupported, its
capacity is unknown, or the complete set exceeds that capacity, ask the same
single question in ordinary chat with every valid numbered option plus `Other -
type your answer`, then wait. Every valid option remains visible. Cluster a very
long decision only where choices share
evidence or constrain one another; keep every valid option visible, explain the
dependency grouping and let the lecturer split, merge, reorder or rename it.
Mutually dependent outcomes, assessment evidence, permitted AI use and
learning activities belong together. Student-experience, accessibility and
active-learning perspectives may be clustered where participation design
jointly affects usability, inclusion, workload and engagement.

Preserve custom answers exactly and confirm their canonical interpretation.
Reflect each consequence in the chat/current-state decision ledger and show an
editable recap at each cluster or gate end. Skip or blank leaves a required
question unresolved. Choosing the offered onboarding route “Skip for now” answers that question and advances to the teaching goal. The safest truthful, evidence-aligned and reversible
option may be marked `Recommended` but is never preselected. Factual
declarations say “select only if true”; uncertainty fails closed. At major
pedagogical gates, ask for the lecturer's criteria and preliminary view before
recommending when practical. This dialogue never substitutes for the exact
authority gate, lineage record or approval token defined below.

## Gate 0A — material and processing-environment eligibility

Start at Step 1 with a brief reason. Accept any mix of LMS, local or cloud files, learning apps, other sources and a description. **Skip for now** continues immediately without opening existing sources. Use a complete multi-select card or one numbered question in ordinary chat. Review access separately for the chosen items.
An explicit Skip continues the redesign from a general description or fictional
example. A formal run records its zero-source scope via the source-free helper
option. No material classification is implied. Gate 0 confirms the empty
manifest, permitted tools and audiences. All later gates retain their normal
order and authority. For a new private source, address handling when it is
needed and preserve unrelated redesign work.

For existing materials, this gate precedes any course-source path, filename,
list, read, copy, hash or other intake. Ask only for the material category, environment category,
internal/restricted and student-data flags, sensitivity classification,
assessment-security classification and authority to handle that assessment
security class, then record a canonical fingerprint. Null, inconsistent,
mixed or uncertain declarations fail closed. An approved record with
`reconfirmation_required=true` does not permit source intake. Do not ask the
lecturer to disclose source details before the gate passes.

In a personal/unmanaged environment, proceed only for privately owned or
rightsholder-authorised material, or appropriately licensed/public material
with explicit AI-processing authority. Public availability alone is
insufficient. Institution-internal/restricted material is route-only with zero
source/path leakage. Mixed material fails closed until segregated; uncertain
material fails closed until clarified. An approved institutional exact
environment must record its policy reference, approved scope and non-expired
expiry.

## Gate 0 — source, data, rights, tools, egress, audiences

Only after approved Gate 0A, inventory and hash sources. Approve the exact source manifest and policy before specialist reading. Gate 0 allows the Gate 1 brief only.
The `Agentic Course Redesign` umbrella entry always routes here; selecting it is
not approval and does not authorise course-content analysis. Gate 0 may inventory
and hash candidate sources only to present the exact manifest and policy.

## Gate 1 — course brief and run contract

Use the lecturer's description and authorised current curriculum or module sources to draft the brief. Ask only the next design-changing contextual question. Keep an explicit unknown, or a non-identifying functional access constraint, in the existing brief. A lecturer can approve a brief with an open contextual assumption.

Confirm the course/learner/assessment context, canonical goal, constraints, success/stop criteria, specialist roster, bounded Stage A subgoals, and maximum stage.

## HITL 1 / Gate 2A — preliminary focus areas

After all five core specialists complete Stage A and exchange summaries, approve/revise/reject plural focus areas and deep-research role contracts. No production.

## HITL 2 / Gate 2B — concrete redesign decisions

Review reconciled evidence and specific change cards. Decide one consequential
design point at a time. Gate 2B may approve only the exact dated research
dossier and research-handoff files under
`03_Research/YYYY-MM-DD_<run-id>/`. It does not authorise course-material
production or writes under `04_Working_Copies/` or `05_Approved/`.

## Gate 3 — coherent blueprint and exact file plan

Approve the alignment-tested blueprint, assessment/security map,
design/citation plan, QA criteria, and typed exact material targets: working
copies under `04_Working_Copies/` and accepted releases under `05_Approved/`.
The approved plan is verified once, then production proceeds through the named
gate for each artefact; there is no additional unlabeled approval pause.

For a private LMS or cloud draft, show the exact service, course/folder,
draft name, action and permitted audience beside its working-copy review file
in this same approval. Use the optional `external_draft` binding and the
destination snapshot in the materials skill's artefact review guide. On resume
verify both the local record and the remote object. A working-copy file alone
authorises local production. A separate explicit instruction is needed to
publish or change recipients.

## Production completion and handoff

The first completed reply must carry current lineage and contain the drafts-ready confirmation in the chosen language (legacy form below):

```text
DECLARE PRODUCTION COMPLETE
```

After the verified production record and exact handoff target are shown, a second completed reply must repeat the target and carry current lineage with the save-handover confirmation in the chosen language (legacy form below):

```text
APPROVE PRODUCTION HANDOFF
```

## HITL 3 — lecturer acceptance

HITL 3 opens only after both production replies and independent verification of
the saved Production Handoff. The lecturer reviews editable files/previews,
change log, QA evidence, limitations, and preserved-source proof, then accepts,
conditionally accepts named corrections, requests revision, or rejects.

## Mandatory system-improvement review offer

After current-lineage HITL-3 acceptance, record the offer before asking the
complete system-improvement question exactly once. A request authorises only a
read-only review and one versioned proposal. It grants no authority to change
files, install, publish, activate, schedule, add permissions/connectors/auth or
trigger a run. On resume, wait on an existing offer rather than asking again.
Silence is `offered_awaiting_response`, never a request or decline.

After an explicit requested or declined response, atomically close the course
run as terminal `complete_dormant`, clear `active_run_id`, and never resume that
run. If requested, system-improvement work proceeds as a separate system
record, not as an extension of the course run. Persist one informational
trigger-guidance offer after closeout: manual triggering is available and
always creates a fresh run; optional scheduling needs exact course, project,
timezone, recurrence, non-null expiry and its own gates, with no immediate run.

## System Gate

System files are a separate proposal, available only after the recorded offer
was requested. Approval requires exact current lineage, proposal ID/version,
exact targets, validation evidence, risks, and rollback, plus the system-file confirmation in the chosen language (legacy form below):

```text
APPROVE SYSTEM FILES
```

This creates an activation-ready candidate only.

## Separate runtime activation

The lecturer must explicitly name and activate the exact validated proposal version. Keeping it inactive or revising/revalidating remains valid.

## Standing schedule

After active-runtime matching and a no-write simulation, for a schedule, show the teacher its actual recurrence, time zone, expiry and the effect of registering it. Use one exact three-line reply in their chosen language. Fill in the shown schedule ID, version and complete date-time with its IANA time zone before asking. Record the three original lines, reply reference and matching schedule. A changed ID, version, expiry or missing line does not authorise registration. Setting it up does not start a run now.

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

Registration never triggers an immediate content run.
Every scheduled trigger records a fresh trigger/run/lineage, the current
eligibility fingerprint, the approved immutable contract-snapshot reference
and a valid offset timestamp. An active trigger must fall on or after contract
activation and before expiry. Pausing, expiry or cancellation disables future
triggers but preserves contract and run history; an on/after-expiry trigger
records an expired no-course-action receipt rather than analysing the course.

## Optional second opinion after the teacher's final decision

Keep Step 9 and the course termination receipt intact. The optional Step 10 is a separate, read-only review. On Skip, finish immediately without preparing a packet or using files, accounts or model tools. The orchestrator follows its second-opinion reference. Selection, original-file authority and final approval of the exact transfer are distinct. Applying a finding needs new approval and a checked revision.
