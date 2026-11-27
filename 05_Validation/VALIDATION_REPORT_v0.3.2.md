# Agentic Course Redesign 0.3.2 validation

## What a teacher experienced

English and Swiss Standard German rehearsals used GPT-6.2 Astra and Sol through Codex with ChatGPT sign-in. Each session received the candidate instructions and a fictional course situation. The sessions were read-only, API-key and provider overrides were removed, and no course files or accounts were supplied. There were 19 distinct situations across 23 model replies, including four repeats after fixes. A separate exercise tested a teacher declining an optional writing tool.

| Situation | Observed result |
| --- | --- |
| Start in English or German | Both models offered a description, combinations of existing materials, skipping and a custom answer. The models used ordinary numbered chat because no choice-card component was supplied. |
| Skip or describe several types of material | Sol continued after skipping. Astra initially asked for classification after the teacher chose to describe local slides, a quiz, course pages and a cloud spreadsheet. After a correction, it recognised all four and asked what learners should be able to do. |
| Explain a teaching priority | Astra asked an open question about what a good discussion should look like. |
| Choose a focus or edit several proposals | Sol offered two possible priorities and allowed a combination or a different answer. In a separate exchange it retained one activity, shortened a reflection to two minutes and left out a quiz exactly as directed. |
| Confirm use of a description and approve the plan | The models kept materials closed, distinguished brief approval from file production, and waited for the teacher to approve the worksheet and guide. |
| Authorise a handover and review individual drafts | Early responses mentioned internal records or included an English confirmation in a German conversation. In the final trials both models offered the draft-completion decision in the teacher's language. The separate handover reply named both items and reproduced the exact destination in English and German. Astra offered individual decisions on finished items. |
| Consider improving the process | Astra offered a written suggestion after acceptance. In a German trial with a completed proposal it offered to prepare the stated file change, named the proposal and destination, and explained that later activation required a separate decision. |
| Decline another service | For a quiz, Astra offered a manual learner-view check or a description of the settings and explained which could establish what learners actually see. For two presentations, Sol continued the structural check and identified which visual checks needed a rendered view. A separate Sol trial revised a poetry worksheet after the teacher declined an optional language tool. |

These rehearsals sampled individual decisions with a prepared starting state for each. Visual rendering of decision cards and how actual teachers use the plugin require separate checks. The confirmations to finish production and authorise the exact handover can be submitted in English or German. An actual destination may still appear in the latter so that teachers can see precisely what they are approving.

Two additional German scheduling rehearsals compared a conversational description with exact stored fields. With only the description, Sol inserted an extra word in the contract identifier and version line. The validator rejected that reply. With the stored identifier, version and expiry, Sol produced three German lines that matched the validator. Both exchanges left the schedule unregistered. A host should populate the confirmation from the actual stored contract.

To repeat the mixed-materials check, start a fresh conversation and say, “Ich habe Präsentationen auf meinem Rechner, ein Quiz in einer Lern-App und eine Tabelle im Cloudspeicher. Ich möchte das zuerst nur beschreiben.” The next teaching question should let the lesson progress while those sources stay closed. To test independent decisions, present a worked example, a ten-minute reflection and a quiz. Reply, “Use the worked example, shorten the reflection to two minutes, and leave out the quiz.” The recap should preserve all three decisions and wait for approval before producing files.

## Verification

On 27 November 2026, fresh Windows and Ubuntu checkouts of the same runtime commit (`fa8b713`) passed all 22 validation commands. The suite included the real v0.2.2 migration fixture, source and package validation for every adapter, final-reply and artifact-receipt checks, repeat builds and archive verification. Each environment reproduced its own archive digest. All 422 member names and their extracted bytes matched between the two operating systems.

| Unit suite | Windows | Ubuntu |
| --- | ---: | ---: |
| Repository and shared workflow contracts | 114 | 114 |
| Shared eligibility helpers | 7 passed, 1 skipped | 8 |
| Codex edition | 30 passed, 1 skipped | 31 |
| GitHub Copilot edition | 23 | 23 |
| Antigravity edition | 20 | 20 |
| **Total** | **194 passed, 2 skipped** | **196 passed** |

The two Windows skips required permission to create directory links. Both passed on Ubuntu. The source-free workflow test checked the route through final handover, per-item acceptance and closeout using simulated teacher decisions.

The directory archive contains 57 reviewed files and matches the repository plugin at runtime. It passed 53 checks against the archive. On Windows, a project upgraded from 0.3.1 through the tested candidate to the finished package. All 54 project files matched their intended release bytes, a second invocation proposed zero changes, and a fresh Codex app-server process discovered the six project-scoped skills as enabled. The [Codex validation report](../01_ChatGPT_Desktop_App/VALIDATION_REPORT.md) gives the archive digest and reproduction commands.

A private vocational numeracy exercise tested an editable presentation and spreadsheet. Earlier teacher approvals were simulated. Sol supplied the learner task, slide sequence, cells and formula. Its native session enforced read-only access, so a local writer created the two Office files. A separate check opened the presentation in PowerPoint, confirmed 11 editable text objects on each slide and visually inspected both rendered slides. Excel calculated a full-pack order of six for a target of 86 units with 14 in stock and packs of 12, seven when the target rose to 87, and zero when stock already covered demand. A zero pack size displayed an input message. Neither file was published to learners.

An independent Astra review found that the original formula could still calculate a fractional pack size pasted over the input validation. The revised formula checks that all three inputs are numeric whole numbers, that demand and stock are nonnegative and that each pack contains at least one item. Excel 16 recalculated a scratch copy in a separate process. All nine cases passed, including an exact pack boundary, one unit over, stock equal to or greater than demand, a zero pack size, a pasted decimal or text, an empty demand cell and negative stock. The preferred private workbook is `Revised-working-copy/Supplier-order-check.xlsx` relative to the pilot folder. The baseline remains in its original working-copy folder.

## Other desktop editions

| Host | Observed on Windows |
| --- | --- |
| Claude Code | Fable 5.2 saved a change to the Claude edition's own source. The adapter installed in both account and project scope, with 50 files at each scope. The host registry showed it enabled. |
| Antigravity | Gemini 4 Carbon High saved a change to its edition's source. Both installations contained 51 files and the host registry showed the plugin enabled. Its strict validator reported that only the first 24,000 bytes of a 31,918-byte instruction body would load. Moving the later procedure to a linked reference allowed validation to pass for all six skills and ten agents. After Skip, a fresh session asked whether learners should find one best route or defend their choice with map evidence. |
| OpenCode | Both installations contained 50 files and OpenCode discovered their agents. GPT-6.2 Astra Fast at Max reasoning used a paired read-only Edge tab, opened the public repository, identified its Codex edition folder and closed that tab. A fresh installed-project session respected Skip and asked the teacher what map evidence learners should use to justify a route. |
| GitHub Copilot | Opus 5.5 at Extra High reasoning wrote its edition's teaching guide. The Copilot CLI reported 0.3.2 enabled. The user installation contained 51 files and the project installation contained 50 files. |

Across the eight user and project installations for these four hosts, all 403 file contents matched their corresponding package.

## Evidence for the interaction choices

- Maier, Schneider and Feuerriegel compared model-led and human-led ideation in a randomised experiment with 486 participants and reported a follow-up with 640. Their human-led conditions supported idea quality while preserving ownership and diversity in those tasks. The plugin applies this finding by asking teachers for their own criteria and making proposed edits reversible. Classroom impact requires a separate study. [CHI 2026, Munich Center for Machine Learning](https://mcml.ai/publications/msf26/)
- Amershi and colleagues tested guidelines for human–AI interaction across a range of products. Their guidance on correcting and dismissing suggestions informed the options to change, combine or leave out specific proposals. [CHI 2019, Microsoft Research](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
- W3C’s supplemental cognitive accessibility guidance recommends familiar words and explanations for unfamiliar abbreviations. The Government Digital Service recommends beginning with one question per page. These design resources informed numbered steps in the teacher’s language and one consequential question at a time. [W3C](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o3p01-clear-words/) · [GOV.UK Design System](https://design-system.service.gov.uk/patterns/question-pages/)
