---
name: course-redesign-materials
description: Produce and independently validate approved editable course materials in formats required by the supplied context, including documents, slides, PDFs, worksheets, assessment files and facilitator guides. Use after exact-target approval for design, citations, media, accessibility, formatting, rendering or package QA.
---

# Course Redesign Materials

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
live host tool contract. Use a card only when it can present the complete,
mutually exclusive option set and a custom-answer path without omission. Never
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

Start only after Gate 3 has approved the exact typed material targets: working
copies under `04_Working_Copies/` and accepted releases under `05_Approved/`.
Gate 2B research-target approval is not production authority. Verify the
recorded plan and targets, then enter the named gate for the first artefact; do
not add an unlabeled second approval pause. Never edit protected sources; work
from copies into the approved dated output root.
Use the terminology, format, accessibility standard, device/print conditions
and facilitator role supplied by the current school, vocational, professional,
higher-education or other course. Do not assume a literary subject, academic
semester, university classroom or teacher/student naming convention.

Choose the output format that fits the approved learner task, access and review
environment. Use [artifact review](references/artifact-review.md) for editable
documents, slides, sheets, cloud work, websites, apps, quizzes, LMS drafts and
browser previews. Use [role evidence](../course-redesign-orchestrator/references/role-evidence.md)
when resolving a pedagogical or accessibility trade-off.

## Preserve and improve

- Preserve worthwhile pedagogy, lecturer voice, period/discipline structure, authentic examples, media, links, and style cues.
- Use an explicit image-retention/omission register rather than blindly dropping or reinserting assets.
- Preserve aspect ratios; crop intentionally and document derived assets.
- Do not show production notes such as "retained from source", donor-slide IDs, prompts, or internal QA language to students.
- Preserve exact source artefacts where fidelity matters; add only approved,
  context-appropriate explanation, scaffolding or alternatives without silently
  changing the source.

## Human-centred design

- Design for the actual learners, setting, devices, print use, and teacher workflow.
- Give handwriting/stylus fields enough physical space; test at 100% scale.
- Keep one clear task and purpose at a time, realistic lesson timing, and visible assessment status.
- Use semantic headings, logical reading order, descriptive links, meaningful alt text, sufficient contrast, and non-colour cues.
- Avoid cramped tables, arbitrary mid-word wrapping, tiny text, distorted media, and inaccessible image-only instructions.

## Citations and rights

- Use the approved citation style consistently.
- In Word, use real superscript footnote references and the approved footnote size; make DOI/URL targets live.
- In PowerPoint, use readable markers/short source text where appropriate, full notes/reference slides, and real hyperlink relationships.
- Keep factual verification and rights/redistribution status separate.

## Assessment security

Use separate student and teacher targets. Scan visible text, editable layers, text boxes, comments, notes, metadata, alt text, hidden objects, model responses, and derived PDFs for key leakage. Accessible assessment derivatives must expose only the assigned item, never an entire secure bank.

## Missing production or preview access

When an approved deliverable depends on an unavailable editor, preview, format skill or LMS, tell the orchestrator exactly which operation needs it, which data and permissions it involves, and what the installed tools can deliver now. For example, a quiz export can check item wording and scoring keys while the private LMS learner preview is needed to verify release timing. Keep the supported work moving when the lecturer declines a connection. Mark the remaining check as unverified.

## QA gate

For every deliverable:

1. reopen it in the available authoring or delivery application and verify the expected edits;
2. exercise the learner's task and review teacher-only views separately;
3. for paginated documents and slide decks, inspect every rendered page or slide and any requested derivative;
4. for other formats, use the format-specific functional and accessibility checks in the artifact review guide;
5. test links, notes/footnotes, headings, language, contrast, alt text, reading order, response space, tables, media, citations, and metadata;
6. compare points/criteria/weights/timings/AI states across all files;
7. verify source hashes unchanged and no unapproved extras/caches in release folders; and
8. commission independent, read-only pedagogical/factual/accessibility/visual/package audits.

Correct direct defects, rerender, rerun targeted and regression checks, and report hashes, counts, limitations, and unresolved lecturer decisions. Do not promote a failing candidate.

## GitHub Copilot native `ask_user` capacity override

This Copilot-only host rule applies the shared core's host-capacity contract to the demonstrated GitHub Copilot host; it changes no option, gate, evidence requirement, or workflow meaning. Keep one unresolved consequential question at a time. Use the native `ask_user` card for the complete valid option set whenever the live GitHub Copilot host accepts it. A live Copilot host has demonstrated at least five explicit choices plus a custom-answer field; this is an observed capability, not a maximum. Do not state or assume an unsupported maximum. Never prune, hide or combine valid choices merely to fit a card. If the host rejects or cannot present the complete valid set, ask one ordinary chat question listing every valid numbered option plus `Other`, then wait. For very long sets, dependency chunks are allowed only when choices share evidence or constrain one another; keep every valid option visible across chunks, explain the grouping, and let the lecturer split, merge, reorder or rename it.

## GitHub Copilot 1.0.80 BYOK file-mutation override

This Copilot-only transport rule changes no workflow option, gate, approval,
target, evidence requirement, or meaning. With an OpenAI-compatible BYOK
provider such as CommandCode Chat Completions, never use built-in `apply_patch`
for any file mutation in this task. Copilot 1.0.80 can record it as
`type=custom` and poison saved history even when the edit succeeded. Use a
packaged helper or function-style PowerShell/Python. Before every permitted
write, preview the exact target and content or diff, obtain the existing
required approval, verify the expected current SHA-256 before modifying an
existing file, write atomically, then reread and revalidate. If `expected
"function"` occurs, do not retry in this task: start a fresh project task,
recover durable state read-only, and verify whether the preceding edit already
succeeded. No MCP server, additional plugin, or additional permission fixes
poisoned history.
