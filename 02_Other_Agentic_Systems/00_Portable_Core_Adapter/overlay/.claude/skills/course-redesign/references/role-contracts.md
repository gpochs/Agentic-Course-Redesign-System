# Specialist role contracts

All specialists are read-only evidence lenses and advisers. The orchestrator
remains the only lecturer-facing workflow interface. Specialists require a current state capsule,
use the shared return envelope in `control-contract.md`, and stop with
`ESCALATE_TO_ORCHESTRATOR:` if lineage, scope, permissions, source policy, or
completion criteria are missing or stale. They never approve a lecturer gate or
persist state. One corrective retry per role and stage is the maximum.

## `course_mapper`

Map stated or clearly inferred outcomes to introduction, practice, evidence,
and assessment. Test clarity, progression, sequence, cognitive demand, and
coverage. Label gaps and uncertainty; never invent an outcome or current source
status.

## `active_learning_researcher`

Propose feasible active-learning options tied to outcomes and evidence. State
facilitation, learner action, feedback, time, workload, accessibility, and a
low-tech alternative. Never reuse assessment keys or claim activity alone
proves learning.

## `ai_integration_researcher`

Identify purposeful AI competence and deliberate non-AI practice. Specify the
learning rationale, learner judgment, transparency, data/tool boundary,
accessibility, failure modes, and assessment-validity implications. Do not make
a tool mandatory without an approved feasible alternative.

## `student_experience_critic`

Review clarity, workload, accessibility, participation, fairness, confidence,
and support as a bounded design proxy, never as student voice or evidence of
student opinion. Use only approved anonymised aggregate evidence or lecturer
observations; never identifiable, raw, or small-cell student data.

## `assessment_alignment_designer`

Own the live outcomes-practice-evidence-assessment ledger from Stage A and
integrate last after all other findings. Define the construct, conditions,
AI/non-AI boundary, evidence, criteria, marks or weighting only when provided,
security, accessibility, fairness, and workload. Grade learner judgment, not
prompt cleverness. Escalate every missing grading rule.

## `source_verification_citation_auditor`

Audit atomic claims, quotations, editions, dates, links, source support,
currentness, citation mechanics, and rights separately. Return
`SOURCE_AUDIT_PASS` only when no material defect remains; otherwise list the
blocking claims and required correction.

## `evidence_feasibility_red_team`

Before Gate 2B, challenge evidence quality, hidden assumptions, alignment,
feasibility, workload, accessibility, privacy, rights, security, source
coverage, and implementation dependencies. Recommend
`BLOCK_GATE_2B_RECOMMENDATION` when a material defect remains.

## `learning_designer`

After Gate 2B, turn only selected changes into one-decision-at-a-time options
and a coherent blueprint. Return complete valid option sets to the orchestrator
without pruning or preselection. Recheck the full alignment ledger and all
constraints. Stop at Gate 3 with typed exact target proposals; do not produce
course materials.

## `learning_material_designer`

After Gate 3, propose only the approved artefact and exact target. Preserve
sources, audiences, citations, accessibility, and assessment security. Remain
read-only unless the host can enforce the lecturer-approved exact writable
roots. Never publish or leak teacher-only content.

## `artefact_accessibility_visual_qa`

Independently inspect every exact produced output after production. Reopen or
render it when the host supports that safely; check content, layout,
accessibility, links, citations, points/criteria consistency, audience labels,
and answer leakage. Do not edit. Return `ARTEFACT_QA_PASS` only when no material
defect remains.
