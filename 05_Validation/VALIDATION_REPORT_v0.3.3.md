# Checking a teacher’s decisions about individual drafts

## Scenario

A teacher approves a worksheet and a quiz for development. On seeing the drafts, they decide to keep the worksheet and leave out the quiz. Version 0.3.2 could reject the handover because it expected both reviews to record acceptance. In 0.3.3, the teacher can identify the draft to leave out. The worksheet can proceed to handover when it passes its own review. A draft that still needs revision returns to the teacher.

## Reproduce the checks

From a clean checkout, run `python -B -m unittest discover -s 05_Validation/tests -p test_shared_core.py -v`. The fictional fixtures exercise the state validator through its normal command-line entry point and cover these separate decisions:

- The teacher keeps one draft and leaves out another. The handover lists the kept draft.
- A missing teacher decision, a mismatched draft reference or an unresolved revision prevents handover.
- The teacher can change their mind during the final review of the delivered drafts. The decision stays tied to the item reviewed.
- Earlier completed records remain readable. The current workflow records each new item decision.

## What the desktop pilot showed

In a test of the installed 0.3.2 Copilot edition, a fictional geography teacher chose to start from a description. After a free-text question, the teacher explained that pupils chose the shortest walk even when its contours showed a steep climb. Copilot used the answer to distinguish reading a map from weighing evidence for a particular walker. Its revised brief asked pupils to recommend a route, cite two map details and explain the trade-off. The session did not require access to a course folder.

A fresh 0.3.3 Copilot desktop session used Opus 5.5 Extra High and loaded the installed orchestrator. The teacher kept the worksheet and left out the optional quiz. Copilot listed only the worksheet for handover and kept the quiz's review history. It paused for the teacher to confirm the drafts were ready. The choice of save location still had its own confirmation.

## What was checked in each installation

The Codex project upgrade matched all 54 expected files and discovered six enabled skills. Three read-only Codex conversations with GPT-6.2 Astra or Sol tested keeping one draft, declining every draft, and reviewing a draft in German before making a final decision. [Codex validation report](../01_ChatGPT_Desktop_App/VALIDATION_REPORT.md)

Claude Code, Antigravity, OpenCode and GitHub Copilot each had a user and a project installation. All 403 installed files matched the corresponding release package. The validator in each of the eight locations accepted the worksheet-only handover. Each also blocked both a pending revision and an attempt to include the excluded quiz, giving 24 checks in total. These trials used fictional records. Earlier Office and browser trials have their own report. [0.3.2 validation report](VALIDATION_REPORT_v0.3.2.md) · [Platform compatibility](../04_Documentation/PLATFORM_COMPATIBILITY.md)

## Fresh desktop conversations

After installation, each desktop host received a fictional teaching decision. The teacher had previewed two drafts and wanted to keep one. The rehearsals ended before saving or sharing.

| Host and model | What the teacher saw |
| --- | --- |
| Codex with GPT-6.2 Astra and Sol | The teacher could keep a single draft, decline all drafts or inspect the retained item before deciding in German. The six skills were also discovered in a fresh account-wide Codex session. |
| Claude Code with Fable 5.2 | Claude listed the worksheet, kept the quiz private and waited for a readiness confirmation. The save location remained a separate choice. |
| Antigravity with Gemini 4 Carbon High | Gemini kept the moon-phase sheet and left the quiz in the private review history. It gave the correct next decision, though its three-section reply was longer than the teacher needed. |
| GitHub Copilot with Opus 5.5 Extra High | Copilot loaded the orchestrator, showed the worksheet in the handover and left the optional quiz out. |
| OpenCode with GPT-6.2 Astra Fast at Max | Using ChatGPT sign-in, OpenCode loaded 0.3.3. It listed the market-price worksheet, excluded the quiz and reserved the exact destination for a later reply. |

In a separate Claude Code trial, Opus 5.5 let the teacher decline both drafts and finish immediately. Its reply said nobody else would see the drafts. The test established that the plugin withheld them from handover. Existing readers of a shared working folder would retain access.

One read-only Sol trial checked how the plugin handled conflicting sources. Last year's fictional syllabus described distributing the worksheet and quiz together. The current teacher had chosen the worksheet alone. Sol followed that choice, asked for the intended audience and kept the destination open for confirmation. The trial used the installed skills and sent no files.

## Release and web checks

Fresh Windows and Ubuntu checkouts of the same source passed all 21 release commands, including 121 repository tests, two builds on each operating system and verification of the archives. All 424 member paths and file contents matched across operating systems. The eight GitHub downloads matched the tagged Windows build. [Release downloads](https://github.com/gpochs/Agentic-Course-Redesign-System/releases/tag/v0.3.3)

On 27 November 2026, the installed public listing also ran in ordinary ChatGPT web. With a fictional map-reading lesson, GPT-6.2 Sol returned the older version's question about material categories. The web conversation exercised the currently published 0.2.5 edition. [Publication status](../04_Documentation/PUBLICATION_STATUS.md)
