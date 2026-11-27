---
name: course-redesign-research
description: Investigate a teaching question the teacher has chosen. Compare research with the actual course and explain which changes the evidence supports and what is still uncertain.
---

# Course Redesign Research

## In conversation

At **Step 4 · Choose what to focus on**, show a specific observation and ask which difficulty the teacher wants to investigate. At **Step 5 · Choose which changes to make**, show one concrete learner action, its rationale and its costs. Keep study citations and qualifications available beside the claim. Use a numbered step when it changes. Speak to the teacher in the language they use. Keep the control names and technical records below in implementation details.

For a literature search, Elicit can help find candidate papers. For an already identified paper, scite can show the context in which other papers cite it. Offer either only when it would improve the approved research task, its availability and costs are clear, and the lecturer chooses it. Use a generic teaching question or public citation identifier. Never send private course documents by default. Follow the link to the original paper, check the relevant passage, population, methods and limits, and read the citing passage before interpreting an automated label. If the lecturer declines, continue using publisher pages, open university repositories or library search already in scope. [Elicit research workflows](https://support.elicit.com/en/articles/14757543-getting-started-with-elicit-which-workflow-should-i-use) · [scite citation context](https://scite.ai/features)

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

Research only an approved focus and only within the current Gate-0A eligibility
fingerprint and source-access policy. If either lineage value is missing,
changed or expired, stop before accessing course sources or sending a query.

Use the [role evidence guide](../course-redesign-orchestrator/references/role-evidence.md)
to select the method and limitation appropriate to the current role. In a
source-free run, use public scholarship only within the approved research
scope. Keep project details out of queries. Label any application to a fictional
course as a design hypothesis until the lecturer tests it.

## Evidence protocol

For each consequential claim record:

- atomic claim;
- source and stable URL/DOI when available;
- source class and authority;
- publication/update date and currentness risk;
- exact supporting location;
- whether the source verifies quotation, date, authorship, interpretation, practice, or rights;
- confidence, limitation, contradiction, and transfer boundary; and
- audience/security classification.

Prefer primary and authoritative sources: original texts/editions, official institutional guidance, legislation/policy, standards, and peer-reviewed research. Use reputable expert commentary for interpretation and implementation. Treat search snippets, vendor claims, blogs, and social media as leads unless the claim is appropriately limited.

## Tools and egress

- Public/open browser research may be used only if the run policy permits it.
- Scite or another connector is optional; availability is not authorisation.
- Never upload protected files, answer keys, assessment prompts, student data, or copyrighted extracts to an external tool unless exact egress is approved.
- If a connector fails, record the exact failure and continue with approved alternatives; do not pretend it worked.

## Text and fact verification

- Name the controlling edition or official record.
- Preserve source text; do not silently modernise spelling or punctuation.
- Distinguish composed/written, first published/performed, and edition used.
- Mark omissions and continued extracts explicitly.
- Verify quotations line by line.
- Never invent a citation, DOI, URL, timestamp, licence, rights holder, or publication fact.
- Keep factual accuracy, citation completeness, and redistribution rights as separate judgements.

## Synthesis

Connect evidence to the exact supplied educational context, course level, discipline, outcomes, assessment construct, workload, accessibility, and local constraints. Treat school, vocational, professional and higher-education contexts as equally valid; label evidence from another context, discipline or learner group as indirect. Report disagreements and open controls instead of forcing consensus.

Finish with a source ledger, claim table, decision implications, limitations, and exact items requiring lecturer judgement or specialist reconciliation.

Keep the integrated dossier and handoff in the task/chat until Gate 2B. Write
them only after the lecturer approves their exact, dated targets under
`03_Research/YYYY-MM-DD_<run-id>/`. That approval does not authorise course-
material production or any target under `04_Working_Copies/` or `05_Approved/`.

## GitHub Copilot native `ask_user` capacity override

This Copilot-only host rule applies the shared core's host-capacity contract to the demonstrated GitHub Copilot host; it changes no option, gate, evidence requirement, or workflow meaning. Keep one unresolved consequential question at a time. Use the native `ask_user` card for the complete valid option set whenever the live GitHub Copilot host accepts it. A live Copilot host has demonstrated at least five explicit choices plus a custom-answer field; this is an observed capability, not a maximum. Do not state or assume an unsupported maximum. Never prune, hide or combine valid choices merely to fit a card. If the host rejects or cannot present the complete valid set, ask one ordinary chat question listing every valid numbered option plus `Other`, then wait. For very long sets, dependency chunks are allowed only when choices share evidence or constrain one another; keep every valid option visible across chunks, explain the grouping, and let the lecturer split, merge, reorder or rename it. A card that returns one choice cannot record a mix of tools or materials. For course sources use a verified multi-select only if it accepts all six options, combinations and a custom answer. Otherwise offer the full numbered set in one chat question. Ask about teaching priorities and feedback in the person's own words. Confirm access to a named task or batch when needed.

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
