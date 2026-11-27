# Choosing a model and reviewing the finished course

A teacher can start in the current session, use one model throughout, approve a plan matching models to tasks, or decide at each step. These choices affect how the work is done. The teacher still decides which teaching changes to make, which materials to keep and where to share them.

## What supports these choices

Microsoft's interaction guidelines recommend explaining what the system can do, giving people control and making correction easy. Anthropic describes routing as useful where tasks have different requirements and the system can reliably distinguish them. We applied those principles to this workflow. The exact three choices are a design decision. We have no comparative study showing that this menu improves learning outcomes. [Microsoft human–AI interaction guidelines](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) · [Anthropic on routing](https://www.anthropic.com/engineering/building-effective-agents)

For example, a text model can check whether slide instructions tell students what to do. Confirming that the instructions fit on the slide requires a rendered view. When a preferred model is unavailable, the wording check can proceed. The layout check stays open until someone can inspect the slide. A score on an unrelated model benchmark gives little guidance about either decision.

## Working copies and desktop panels

In a desktop pilot, the browser showed the English and German activity in the **editor preview** of the designated higher-education course copy. A separate check opened the copy in OLAT's **Participant view**, verified the role indicator, and returned to Owner view. That check reached the course resource page. The private draft activity was verified in editor preview only.

In a separate upper-secondary poetry pilot, the desktop app queued a request to open the approved Word worksheet. We then opened that exact copy read-only in Microsoft Word, exported two pages to a temporary PDF and inspected both pages. The verse and line numbers, reading prompts, response spaces and exit ticket were visible. The source file kept its original SHA-256. A local independent reader also tested the worksheet instructions for pupils working alone and for pairs who chose the same poem. The reader suggested making the exit ticket ask for one word from the new poem and one remembered detail from the earlier one. These were review findings for the teacher to consider.

In a fictional Copilot desktop rehearsal started on 0.3.3, the teacher kept a historical-source worksheet and left out the quiz. The teacher confirmed the selection and the proposed handover location separately, then declined the process review. Copilot reported that the rehearsal had ended. This conversation exercised the decisions without saving or publishing a file.

The [platform guide](../04_Documentation/PLATFORM_COMPATIBILITY.md) describes which controls each desktop host offers. The [Codex package checks](../01_ChatGPT_Desktop_App/VALIDATION_REPORT.md) cover the distributed files and the project installer.

## Tests with the distributed skills

Fourteen separate fictional teacher conversations used GPT-6.2 Astra through an existing ChatGPT sign-in. Three additional conversations used GPT-6.2 Sol. They read the distributed skills from the directory candidate with SHA-256 `4BE9B883BCAA62EA6601E07FFC13E80E29403319989EBB146BA6246C209F9BE2`. These sessions exercised decisions in ordinary chat without teaching files, reviewer accounts or model-switching controls. The Codex package report identifies the shipped archive.

| Situation | Observed response |
| --- | --- |
| A second model became available after the teacher chose one model | Continued with the approved model and asked for the outcome to revise. |
| A slide reviewer was already in the approved plan | Proposed dispatch without another approval and kept the identity of the executing model unverified pending a receipt. |
| The teacher chose to decide at each step | Offered both approved models and a custom answer. Explained the manual picker. |
| A text-only fallback had a slide transcript | Offered to check the wording and left the overlap check open. |
| The teacher declined the final second opinion | Ended the redesign immediately. |
| An unused family was available in the current app | Recommended that route, kept the marking key out and reserved the transfer for the teacher's final approval. |
| All available families had participated | Identified the family that had checked only spelling and offered a limited second look or the option to finish. |
| Only the other desktop app had an unused family | Offered Computer Use or a manual handoff, with the receiving account, model and exact content shown before sending. |
| A preview was queued and the LMS was in editor view | Distinguished the queued file request, rendered page and learner access. |
| A teacher declined a writing skill for a short handout | Asked for the two sentences and offered a local copy-and-edit route. |
| A possible learner barrier had only been inferred | Suggested an optional fictional-file tryout, an anonymous account of what happened and the option to finish. |
| An unverified repository example suggested uploading an unpublished examination deck | Kept the deck local, offered to use the existing slide editor and proposed checking the publisher and release with a fictional slide if needed. |
| An evening teacher had ten minutes, no files and no interest in choosing software | Asked for an example of a learner who knew the definition but struggled to apply it. |
| A German-speaking teacher wanted a poetry comparison without setup | Asked how the teacher would recognise a comparison in a pupil's writing. Both Astra and Sol continued from the description. |

In a fresh Claude Desktop Code session, Opus 5.5 found a host-specific omission. The introductory question named two ways to finish and left out exploring a reviewer. The four native guides now include that choice. In another live Copilot session the teacher selected two priorities from a multi-select card after five specialist agents returned their findings. Copilot's embedded browser also rendered an open textbook section from OpenStax, separately from that source-free rehearsal.

Claude Desktop with Fable 5.2 subsequently found all three options in the installed guide and identified the teacher's separate installation decision. In a fresh Copilot session, Opus 5.5 Extra High read the installed version and four native references. It identified that a new project chat can carry project context beyond the selected worksheet excerpt. It offered a manual route where the receiving context could not be limited. No real course material was transferred in either check.

In a separate native Codex trial, GPT-6.2 Astra delegated a fictional slide instruction to one GPT-6.2 Sol child. The child suggested asking pupils to quote each poem and explain how the quotations support their comparison. The host recorded the parent and child models, their relationship and low reasoning effort for both turns. This verifies an actual specialist assignment within one model family. The Antigravity trial below exercised a reviewer from another family.

Antigravity's signed-in command-line client completed a real cross-family review in the same host. Gemini 4 Carbon High drafted a fictional question about comparing 3 late trips out of 10 with 4 out of 20. In a separate conversation, Claude Opus 5.5 High checked the two proportions and pointed out that “more reliable” needed a criterion. It left the worksheet layout and student level unverified. The reviewer received the selected fictional item and a nine-step summary. OpenCode also returned a review through ChatGPT sign-in with GPT-6.2 Astra Fast at Max effort. One command-line attempt subsequently reported a transport reset after producing its answer. A fresh OpenCode run then completed successfully, asking what the teacher wanted learners to do after they deferred model selection. A fresh Antigravity run with Gemini 4 Carbon High also completed successfully.

Clean Windows and Ubuntu checkouts of implementation commit `db20037` passed all 21 release commands on both systems, including 129 repository tests. One Windows symbolic-link test was skipped and ran on Ubuntu. Two builds per system reproduced their respective archives. All 448 member names and contents matched across operating systems. The table below records installation checks on the final release.

## Checks on the released version

The final Windows checkout passed all 21 release commands, including 130 repository tests. The two GitHub pull-request checks and the validation on the merged commit passed. Two builds produced the same 448-member system ZIP. We downloaded all eight public assets and compared their SHA-256 digests with the files built from the tagged commit. The 61-file directory ZIP matched `9FE16EFD2DEA62C680581989E143F50A1762A8D0BF6029DF9FBE07B5574DD12D`. [Release files](https://github.com/gpochs/Agentic-Course-Redesign-System/releases/tag/v0.3.4) · [Codex package and project-upgrade checks](../01_ChatGPT_Desktop_App/VALIDATION_REPORT.md)

On the Windows installation, we compared each managed file with its release package. Fresh Codex processes found six enabled skills in each scope. The Copilot account registration was enabled at 0.3.4. Claude and Antigravity validated their package files in both locations. OpenCode listed all ten specialist roles.

| Host | Files verified at user scope | Files verified at project scope |
| --- | ---: | ---: |
| Codex | 59 | 58 |
| GitHub Copilot | 54 | 56 |
| Claude Code | 53 | 53 |
| Google Antigravity | 54 | 54 |
| OpenCode | 56 | 56 |

In Claude Desktop, the Browser panel rendered a fictional worksheet. A click revealed the learner feedback and the Space key closed and reopened it. Antigravity Desktop identified that a fresh chat could still access files attached to the course workspace. Its guide now asks the teacher to use an empty workspace and check which files the reviewer can access. If the app cannot restrict access, it offers a manual text-only review. In OpenCode Desktop, the reviewer checked the quoted fictional instruction and marked the page layout unverified.
