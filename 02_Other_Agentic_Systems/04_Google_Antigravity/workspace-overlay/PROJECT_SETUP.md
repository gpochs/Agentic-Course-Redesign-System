# Course redesign project

This folder is for one course only. It was created from the project-local
Google Antigravity adapter without activating a runtime.

It may reside on local storage or a lecturer-controlled personal OneDrive.
OneDrive is cloud-synchronised rather than strictly local, so protected or
assessment material belongs there only when the lecturer's institutional,
privacy, rights and security rules authorise it. Exclude student personal data,
submissions, grades, credentials and secrets by default.

## First actions

1. Add current course files to `00_Source_Materials/`.
2. Add relevant programme, learner, policy, accessibility, assessment, AI-tool, rights, and style context to `00_Context/`.
3. Keep student personal data, submissions, grades, credentials, and secrets out of the project unless a separately approved institutional workflow permits them.
4. Invoke `/course-redesign-start` and ask the orchestrator to inventory the
   files and prepare Gate 0.
5. Review source classifications, teacher-only assessment boundaries, tool/egress permissions, output audiences, manifest fingerprint, and policy fingerprint.
6. Approve or revise Gate 0 before any specialist analysis.

## Important distinctions

- The source manifest proves file integrity; it does not grant access or egress.
- A course-material decision is not a system activation decision.
- A system activation decision is not schedule approval.
- Schedule approval registers an expiring contract but does not trigger an immediate run.
- Every scheduled recurrence creates a fresh run and waits at the configured human gate.

Read `AGENTS.md` for the full orchestration contract and `01_Control/GATES.md` for lecturer decision points.
