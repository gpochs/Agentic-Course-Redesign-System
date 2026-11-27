# Codex 0.3.0 release checks

The 0.3.0 directory ZIP and repo marketplace carry identical runtime files. The ZIP contains 57 files under one plugin root, including six skills and ten project-scoped agent definitions. The revised support link points to the published support page. The privacy link is pinned to the updated notice. The initial portal scan requested a support URL. The release ZIP was rebuilt after that finding.

| Check | Observed result |
| --- | --- |
| Public metadata, runtime parity and review cases | 51 package checks passed, including matching reviewed skill hashes, 16 positive scenarios and 13 negative scenarios. These are reviewer cases. |
| Forward checks | All 46 passed, covering the ten native agent definitions, six skills, lecturer decisions, production handoff, final review and source boundaries. |
| Bundled helper tests | 29 passed. One symbolic-link test was skipped because this Windows environment could not create the test link. |
| Installed OpenAI validators | The six installed skill checks passed in both package trees. The optional local plugin-validator script was unavailable on this installation. |
| Release build | Two fresh public-package builds produced SHA-256 `A784591809BD191E689B5979C6286961A2DAE7A3830BA77F5DD66F563D9744D2`. All files matched the submission source. |
| Project-scoped skill discovery | On Windows with Codex CLI 0.172.0, a fresh native skill scan recognised all six enabled repo-scoped skills. A repeat installer preview found zero changes. |

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
