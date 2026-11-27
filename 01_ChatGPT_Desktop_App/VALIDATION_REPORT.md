# Codex 0.3.4 release checks

The skills-only ZIP contains 61 files. Two independent builds produced SHA-256 `9FE16EFD2DEA62C680581989E143F50A1762A8D0BF6029DF9FBE07B5574DD12D`. All 63 package checks passed, including the ten role instructions, direct-entry guide links, role-specific tool research and the pending preview status and byte identity with the marketplace runtime. The reviewer pack contains 28 positive and 20 negative cases. The 47 structural forward checks passed. The installed official skill validator accepted all six skills in each package. The standalone plugin validator was unavailable.

The 33 Codex helper tests had 32 passes and one Windows symbolic-link skip. In a disposable Windows project, all 54 files from the tagged 0.3.3 project installation matched the frozen prior hashes. The 0.3.4 installer updated 23 and added four. All 58 project files matched the new package after installation. A repeat preview found zero changes. After the final role guidance was added, the Windows course project matched all 58 files. A fresh Codex app-server scan found all six enabled project skills.

A fresh ChatGPT-backed Codex run used the project instructions from that exact ZIP. A teacher deferred model selection, skipped files and asked to start a lesson about photosynthesis. The assistant went straight to a teaching question about the evidence learners should use to explain a plant’s poor growth. No tool or transfer was requested.

The repository tests exercise all three model-choice modes, the 16 task assignments, a change of account after plan approval, and a fallback route with unverified execution. Separate tests exercise the final review packet, including its exact content and receiver, and show that changing the model, account, cost or file invalidates the transfer receipt. The validator tests run without sending anything to a reviewer. For observed host behaviour and current installation evidence see the [0.3.4 system report](../05_Validation/VALIDATION_REPORT_v0.3.4.md).

## Codex 0.3.3 release checks

A teacher can try two approved drafts, keep the worksheet and leave the quiz out of the handover. The working quiz stays in its original draft location. Each included item still needs a final teaching decision. A requested revision stays open, and excluding every draft stops the handover.

| Check | Observed result |
| --- | --- |
| Public archive | Two builds produced the same 57-file ZIP, SHA-256 `A9204C8EDBFCBE32EB19D5733804457338643A654996D34E86C9DE6FE7D13159`. The 55 runtime files match the repository marketplace package. |
| Public metadata and review cases | All 54 archive checks passed. The reviewer pack includes 21 positive and 16 negative scenarios. |
| Forward checks and helpers | All 47 forward checks passed. Of 32 helper tests, 31 passed on Windows and one symbolic-link test was skipped. The selective-handover test accepts one of two planned drafts, detects an excluded item added to the handover and rejects a final acceptance recorded against that item. |
| OpenAI skill validation | The installed official skill validator accepted six skills in each of the two packages. The standalone plugin validator was unavailable locally. |
| Project installation | An existing Windows course project upgraded six files from its verified 0.3.2 installation. All 54 project files matched after installation. A second preview proposed zero changes. A fresh Codex app-server scan recognised all six skills as enabled at project scope. |
| Model behaviour | In fictional teacher conversations using the ChatGPT subscription, GPT-6.2 Sol kept the worksheet and left the quiz in its working location. GPT-6.2 Astra stopped when the teacher left out all drafts. In German, Astra let the teacher inspect the retained worksheet before making a final decision. These conversation checks used no real course documents. |

The repository includes the full shared validation report for this release and the earlier account of English and German trials across the workflow. [Release validation](../05_Validation/VALIDATION_REPORT_v0.3.3.md) · [Earlier teaching trials](../05_Validation/VALIDATION_REPORT_v0.3.2.md)

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
