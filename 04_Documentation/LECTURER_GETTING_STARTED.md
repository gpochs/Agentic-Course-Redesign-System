# Lecturer getting started

You do not need to write a master prompt. The installed skill or project
adapter should guide the setup conversationally.

## 1. Confirm the processing environment before sharing a path

The orchestrator first asks Gate 0A questions without requesting a course path,
one unresolved declaration at a time. It uses a clickable card only when the
live host can show the complete mutually exclusive option set plus a
custom-answer path. If that control is unavailable or unsupported, its capacity
is unknown, or the complete set exceeds its capacity, the orchestrator lists
every valid numbered option plus **Other - type your answer** in ordinary chat,
and waits. It never prunes, hides or combines valid choices to fit a card.
State whether the material is privately owned, rightsholder-authorised,
appropriately licensed/public, institution-internal/restricted, mixed or
uncertain; also confirm AI-processing authority for the selected provider,
sensitivity and assessment security.

On a personal or unmanaged system, public availability alone is not enough.
Proceed only for privately owned/rightsholder-authorised or appropriately
licensed/public material with explicit processing authority. For internal or
restricted institutional material, use only an institution-approved exact
environment and record its current policy reference, scope and expiry. Product
availability and institutional policy can change, so verify them at the time
of use. Mixed or uncertain material must be segregated or the run stops.

## 2. Create one project per course

In ChatGPT Desktop, Codex or another supported agentic workspace, create a new
project for one course. Create or select a short isolated folder on your
personal computer or lecturer-controlled storage, for example:

- Windows: `C:\CourseProjects\Biology\Year2`
- macOS/Linux: `~/CourseProjects/Biology/Year2`

A personal OneDrive is convenient across devices but is cloud-synchronised.
Store protected, copyrighted or assessment material there only if the relevant
institutional and rights rules permit it. Do not point the system at a broad
home, drive or multi-course folder.

## 3. Install or copy the correct adapter

- ChatGPT Desktop/Work/Codex: follow `01_ChatGPT_Desktop_App/README.md`.
- GitHub Copilot app/CLI: follow
  `02_Other_Agentic_Systems/01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md` for
  the recommended native plugin. Its project-local overlay remains an
  advanced/manual alternative.
- Claude Code, OpenCode or Antigravity: use only the matching folder under
  `02_Other_Agentic_Systems/`.

An adapter is not activated merely because its source exists in this
repository. Installing the Copilot plugin adds reusable skills and agents but
does not inspect a course, activate a runtime or start a redesign. For a manual
overlay, review it and copy it into the one course workspace using the
documented preview-first route.

## 4. Add course evidence

Put copied current materials in `00_Source_Materials/`, including relevant
plans, slides, workbooks, assessments and keys. Put programme requirements,
learner profile, accessibility guidance, assessment policy, grading rules,
permitted-tool guidance and lecturer style examples in `00_Context/`.

Keep originals elsewhere. Add no unrelated course. Exclude student personal
data, identifiable submissions, grades, credentials and secrets unless a
separately approved institutional workflow explicitly permits them.

## 5. Start the guided run

Start a new task in the course project and say:

> Set up an agentic redesign project for this one course.

In ChatGPT Desktop Work/Codex, type `@` first and choose **Agentic Course
Redesign**. If the app flattens a skills-only plugin, the entry with that name
is the umbrella orchestrator: it starts protected setup or continues the
current verified run and calls the bounded specialist skills when authorised.

The system asks only questions that materially change the analysis. It
preserves a custom answer verbatim, confirms how it will be represented, and
shows an editable recap before continuing through a cluster or gate. A
recommendation identifies the safest truthful evidence-aligned reversible
option, is never preselected, and must not replace your factual declaration.
Blank, skipped or uncertain required answers remain unresolved. Before any
specialist reads protected files, review the exact source manifest, source
classes, data and rights statement, teacher-only assessment boundary,
permitted roles/tools/egress, output audiences and actual workspace.

## 6. Make the decisions

The lecturer remains the expert in the loop. For a very long decision, the
orchestrator may propose a cluster only when choices share evidence or constrain
one another. Every valid option remains visible. You may split, merge, reorder,
rename or defer it. For example,
outcomes, assessment evidence, permitted AI use and learning activity belong in
one cluster when changing one changes the others; student-experience,
accessibility and active-learning perspectives may be considered together when
participation design jointly affects usability, inclusion, workload and
engagement.

1. **HITL 1:** approve, revise or reject preliminary redesign focus areas.
2. **HITL 2:** decide the researched, concrete course changes one by one.
3. **Production handoff:** after all named artefact gates and QA, first declare
   production complete, then separately approve the exact handoff target. The
   handoff must verify before HITL 3 opens.
4. **HITL 3:** inspect the redesigned files and QA evidence, then accept,
   request bounded revisions or reject them.

Only after unconditional HITL 3 acceptance does the system ask whether the
lecturer wants a separate read-only review of the workflow skills and umbrella
entry; plugin or platform adapter; `AGENTS.md` and agent configurations;
project template, state schema and migration; validators, tests and QA;
documentation; memory or other workflow-owned durable instruction stores;
schedule contracts; permissions, tools, external egress and automatic
behaviour; and compatibility, benefits, regressions, risks, residual risks and
rollback.
Saying yes permits only that review and a versioned proposal. A validated
system change, publication or installation, runtime activation and an expiring
schedule are later, separate decisions.

The lecturer must explicitly accept or decline the review offer. After that
answer, an accepted course run is closed as complete and dormant and cannot be
resumed. The orchestrator then offers one short explanation of how to start a
fresh run manually and how an optional schedule can be planned for a named
course, timezone, recurrence and expiry. The offer itself neither starts a run
nor creates automation.

## 7. Keep control

At any time you may pause, narrow scope or reject a proposal. Silence, a prior
approval, installation, a schedule or a tool's availability never authorises a
later gate, a different course, external egress or a new file target.
