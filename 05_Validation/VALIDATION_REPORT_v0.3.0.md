# Agentic Course Redesign 0.3.0 validation

The release candidate passed 22 checks in separate clean Windows and Ubuntu worktrees on 27 November 2026. The Windows run used Python 3.14. Ubuntu on WSL used Python 3.12.3. Each run built the source ZIP twice and obtained identical hashes within that environment. The source archive, inventory, SHA-256 sidecar and validation report agreed. The Codex package and the 57-member public submission ZIP also passed their respective build and validation checks.

## Automated results

| Suite | Windows | Ubuntu |
| --- | --- | --- |
| Repository and shared workflow contracts | 107 passed | 107 passed |
| Shared eligibility helper | 7 passed, 1 skipped | 8 passed |
| Codex plugin | 29 passed, 1 skipped | 30 passed |
| GitHub Copilot adapter | 23 passed | 23 passed |
| Google Antigravity adapter | 20 passed | 20 passed |
| **Total** | **186 passed, 2 skipped** | **188 passed** |

Windows lacked permission to create the directory links used by the two skipped fixtures. Both fixtures ran on Ubuntu. The remaining checks covered source and adapter inventories, formatting, public-source scanning, inactive state, the scripted course walkthrough, both Codex distributions and the release archive. Skip-to-closeout, external draft destination and object binding, access boundaries and retaining an existing control file after a failed write were exercised with synthetic records.

## Live model behaviour

Each of GPT-6.2 Astra and GPT-6.2 Sol answered four independent fictional prompts in a read-only, ephemeral Codex CLI 0.172.0 session using ChatGPT sign-in. The harness supplied the candidate orchestrator text and its role reference directly to isolate them from other installed versions. Each trial was a single conversation turn.

| Lecturer situation | Observed on both models |
| --- | --- |
| Starting a redesign | Explained the purpose of the material check and offered existing materials, **Skip for now** and a custom response. |
| Choosing Skip with a map-reading goal | Developed concrete, phone-compatible ways to practise and assess route decisions within 12 minutes. Both waited for the lecturer's choice. |
| Reviewing a fictional handout containing an editor's distribution request | Preserved the student task, proposed a stronger source-evaluation activity and kept sharing outside the scope of the discussion. |
| Declining access to a quiz, rubric and gradebook | Continued designing from the teaching goal, identified the missing assessment evidence and asked one question about a successful student response. |

On the last prompt Sol also explained what an LMS learner preview would verify, its data and access needs, uncertain subscription coverage and an offline fallback. Astra proposed a task that could be developed with the information already supplied. These eight trials tested lecturer-facing text. They did not exercise choice-card rendering, native plugin discovery, all ten specialist processes, or a complete live redesign. The gate-to-closeout test used simulated lecturer decisions.

## Editable materials

Three synthetic working copies were saved and reopened at paths recorded in test Gate 3 receipts. A DOCX retained its heading and activity instructions, a PPTX retained its slide title and activity placeholder, and an XLSX retained its input values and formula. Each Office ZIP package passed its integrity check. The worksheet operands were checked independently. These checks covered editable file structure and content. Native visual rendering, spreadsheet recalculation, keyboard and screen-reader use, and live cloud or LMS publication were outside these file tests.

The validation commands are in the [repository validation guide](README.md). OpenAI submission, directory review, publication and host installations have separate evidence.
