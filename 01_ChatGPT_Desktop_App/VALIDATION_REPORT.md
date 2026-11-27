# Codex 0.3.2 release checks

The 0.3.2 directory ZIP and repo marketplace carry identical runtime files. The ZIP contains 57 files under one plugin root, including six skills and ten project-scoped agent definitions. The reviewer cases cover combined source types, optional tools, teacher decisions, staged course context and course-level accessibility needs.

| Check | Observed result |
| --- | --- |
| Public metadata, runtime parity and review cases | 53 checks passed against the archive, including matching reviewed skill hashes, 20 positive scenarios and 15 negative scenarios. These are reviewer cases. |
| Forward checks | All 46 passed, covering the ten native agent definitions, six skills, lecturer decisions, production handoff, final review and source boundaries. |
| Bundled helper tests | 30 passed. One symbolic-link test was skipped because this Windows environment could not create the test link. |
| OpenAI skill validation | All six skills in both package trees passed OpenAI’s published quick validator at commit 49f948f. This host lacked a locally installed standalone plugin validator. [Official validator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/scripts/quick_validate.py) |
| Release build | Two fresh public-package builds produced SHA-256 `D130635C717D69E9C7366FD77D4E45D81559191AF136710CDB4A36C6A2D496C2`. All files matched the submission source. |
| Project-scoped skill discovery | A Windows project upgraded from 0.3.1 in two passes. The first replaced 30 verified files. After the final confirmation and handover changes, five more replacements matched the tested candidate's recorded bytes. The installer verified all 54 final files, proposed zero changes on retry, and a fresh Codex app-server scan recognised all six enabled repo-scoped skills. The regression test also checks preservation of a lecturer-edited file. |

Independent English and German model trials checked mixed materials, skipping access, teacher explanations, several decisions in one reply, optional tools and the separate approvals before final review. [Behaviour and evidence](../05_Validation/VALIDATION_REPORT_v0.3.2.md)

## Reproduce

In the tested Codex Plan mode, `request_user_input` accepts two or three explicit options and supplies a free-text Other answer. Ask open-ended teaching questions directly. On a host with a different card contract, use its documented options. Use the ordinary-chat fallback whenever a card cannot show the full choice set and allow a custom answer.

Run these commands from the Codex adapter. Install PyYAML for the static YAML check and the optional installed OpenAI validators when available.

```text
python -m unittest discover -s plugins/agentic-course-redesign/tests -v
python validation/forward_test.py
python validation/validate_static_formats.py
python validation/public_scrub.py
python validation/run_official_validators.py --allow-missing
python validation/check_public_submission_build.py
python validation/check_release_build.py
```

Read the actual per-validator statuses when using the optional discovery flag. Directory publication, host model behaviour, correct rendering of a particular document and successful submission of a real LMS activity require their own checks. Before accepting a course deliverable, reopen it in its intended application and test the learner task. [Reviewer cases](openai-submission/review/test-cases.json)
