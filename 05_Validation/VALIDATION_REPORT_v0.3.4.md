# Choosing a model and reviewing the finished course

A teacher can start in the current session, use one model throughout, approve a plan matching models to tasks, or decide at each step. These choices affect how the work is done. The teacher still decides which teaching changes to make, which materials to keep and where to share them.

## What supports these choices

Microsoft's interaction guidelines recommend explaining what the system can do, giving people control and making correction easy. Anthropic describes routing as useful where tasks have different requirements and the system can reliably distinguish them. We applied those principles to this workflow. The exact three choices are a design decision. We have no comparative study showing that this menu improves learning outcomes. [Microsoft human–AI interaction guidelines](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) · [Anthropic on routing](https://www.anthropic.com/engineering/building-effective-agents)

For example, a text model can check whether slide instructions tell students what to do. Confirming that the instructions fit on the slide requires a rendered view. When a preferred model is unavailable, the wording check can proceed. The layout check stays open until someone can inspect the slide. A score on an unrelated model benchmark gives little guidance about either decision.

## Working copies and desktop panels

In a desktop pilot, the browser showed the English and German activity in the **editor preview** of the designated higher-education course copy. A separate check opened the copy in OLAT's **Participant view**, verified the role indicator, and returned to Owner view. That check reached the course resource page. The private draft activity was verified in editor preview only.

In a separate upper-secondary poetry pilot, the desktop app queued a request to open the approved Word worksheet. We then opened that exact copy read-only in Microsoft Word, exported two pages to a temporary PDF and inspected both pages. The verse and line numbers, reading prompts, response spaces and exit ticket were visible. The source file kept its original SHA-256. This establishes Word rendering independently of the desktop panel.

In a fictional Copilot desktop rehearsal started on 0.3.3, the teacher kept a historical-source worksheet and left out the quiz. The teacher confirmed the selection and the proposed handover location separately, then declined the process review. Copilot reported that the rehearsal had ended. This conversation exercised the decisions without saving or publishing a file.

The [platform guide](../04_Documentation/PLATFORM_COMPATIBILITY.md) describes which controls each desktop host offers. The [Codex package checks](../01_ChatGPT_Desktop_App/VALIDATION_REPORT.md) cover the distributed files and the project installer.

## Tests with the distributed skills

Fourteen separate fictional teacher conversations used GPT-6.2 Astra through an existing ChatGPT sign-in. Three additional conversations used GPT-6.2 Sol. Each read instructions from the final directory ZIP, SHA-256 `4BE9B883BCAA62EA6601E07FFC13E80E29403319989EBB146BA6246C209F9BE2`. The sessions exercised decisions in ordinary chat. They had no teaching files, reviewer accounts or model-switching controls.

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

Antigravity's signed-in command-line client completed a real cross-family review in the same host. Gemini 4 Carbon High drafted a fictional question about comparing 3 late trips out of 10 with 4 out of 20. In a separate conversation, Claude Opus 5.5 High checked the two proportions and pointed out that “more reliable” needed a criterion. It left the worksheet layout and student level unverified. The reviewer received the selected fictional item and a nine-step summary. OpenCode also returned a review through ChatGPT sign-in with GPT-6.2 Astra Fast at Max effort. One command-line attempt subsequently reported a transport reset after producing its answer.

Clean Windows and Ubuntu checkouts of implementation commit `db20037` passed all 21 release commands on both systems, including 129 repository tests. One Windows symbolic-link test was skipped and ran on Ubuntu. Two builds per system reproduced their respective archives. All 448 member names and contents matched across operating systems. The Codex course project matched all 58 expected files. The Copilot user and project installations matched 54 and 56 managed files respectively. Claude Code, Antigravity and OpenCode matched 53, 54 and 56 files respectively in each of their user and project installations.
