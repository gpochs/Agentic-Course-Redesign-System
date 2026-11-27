# Agentic Course Redesign 0.3.1 validation

## Automated checks

All 22 checks passed on 27 November 2026 in separate clean Windows and Ubuntu checkouts of the same candidate. They used Python 3.14.3 and 3.12.3 respectively, with PyYAML 6.0.3 on both. The checks covered the source tree, both Codex distributions, the four other host editions, the inactive state templates and a scripted course walkthrough. Each environment produced the same digest on two independent source builds. The Windows and Ubuntu ZIP containers differed in compression and header metadata. Every extracted member matched byte for byte across environments. Both inventories, digest sidecars and validation receipts verified.

| Unit suite | Windows | Ubuntu on WSL |
| --- | --- | --- |
| Repository and shared contracts | 109 passed | 109 passed |
| Shared eligibility helpers | 7 passed, 1 skipped | 8 passed |
| Codex plugin | 30 passed, 1 skipped | 31 passed |
| GitHub Copilot adapter | 23 passed | 23 passed |
| Antigravity adapter | 20 passed | 20 passed |
| **Total** | **189 passed, 2 skipped** | **191 passed** |

The two Windows skips require permission to create directory links. Both fixtures ran on Ubuntu. The new shared-core tests check that the installed instructions lead the orchestrator to the optional context dialogue and the materials specialist to the copy-dependency procedure. The existing gate and state tests continue to cover the source-free route through a simulated handoff. Package tests also exercise retries and preservation of local edits when upgrading project skills.

## Live Codex behaviour

Four single-turn trials used GPT-6.2 Sol and GPT-6.2 Astra in ephemeral, read-only Codex CLI sessions with ChatGPT sign-in. The test supplied the candidate skills and their role or materials references directly, used fictional situations and removed API-key and provider overrides from the child environment.

| Scenario | Observed behaviour |
| --- | --- |
| Sol, skipped onboarding | Continued from a one-sentence course description and asked for one learning outcome. |
| Astra, known programme and fixed assessment | Used the known assessment to propose low-stakes practice and asked what successful reasoning would look like. It respected the lecturer’s decision to withhold student details. |
| Sol, copied LMS course with a linked original | When the fictional quiz editor showed the original bank ID, Sol held the edit and offered an approved independent copy, an offline draft, or leaving the item alone. |
| Astra, unknown assessment in a school course | Offered two specific, age-appropriate practice tasks drawing on a known prerequisite. The lecturer could continue with the assessment question open. |

The trials exercised the model replies. The copy-dependency case supplied synthetic editor observations. It did not connect to an LMS. Native discovery, choice-card rendering and the availability of every host’s desktop tools require separate host checks.

## Private artifact pilot

A separate, authorised pilot used a source-enabled project and simulated lecturer decisions. It exercised the project scaffold, eligibility recording, source-manifest verification and access-policy fingerprinting. The first eligibility rehearsal stopped on missing handling authority. A fresh project covered a narrower, authorised set of teaching inputs. Four original source fingerprints matched after the pilot.

The pilot produced separate editable learner and lecturer documents. A second, read-only Codex reviewer tried the learner task and identified ambiguous directions and an incomplete independent response option. The revised files reopened in Word. All five rendered pages received a visual check, and the reviewed working files matched the accepted private copies. The pilot measured neither classroom learning nor formal accessibility conformance. Its simulated decisions did not activate a real course run, publish a lesson or register a schedule.

The [validation guide](README.md) lists commands for reproducing repository and package checks. Live directory review and publication are tracked separately.
