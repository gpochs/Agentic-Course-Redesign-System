# Distribution

The repository supplies the package at `plugins/agentic-course-redesign` and a repository marketplace. Its OpenAI submission source is at `openai-submission/source/agentic-course-redesign`. Both carry identical skills, scripts, project assets and plugin metadata. The public ZIP omits test fixtures and repository administration.

Build the portable workshop bundle with `python validation/check_release_build.py`. Build the directory ZIP with `python validation/check_public_submission_build.py`. The latter checks that two builds have the same SHA-256 and verifies ZIP membership and source bytes. Upload the resulting skills-only ZIP as a draft on the existing publisher listing. Check its automated findings, review status, publication version and directory visibility in the portal.

For a release change, review each affected file and update its SHA-256 in `openai-submission/review/public-package-digests.json`. Update `skill-digests.json` for changed skills. Add intended portable-only files to `portable-files.json`. The builders use these reviewed lists, so a stray file in a checkout cannot enter either ZIP.

A user can install from the supported directory or use a local project scaffold. For an installation smoke test, start a fresh conversation, select the intended release, invoke the umbrella entry, skip onboarding and observe the next teaching question. Access to specific documents, applications and courses depends on the workspace and the lecturer's choice. [Installation](INSTALLATION.md) · [OpenAI plugin support](https://learn.chatgpt.com/docs/plugins)
