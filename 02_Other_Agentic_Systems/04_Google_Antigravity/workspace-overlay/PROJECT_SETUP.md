# Course redesign project

This folder is for one course only. It was created from the project-local
Google Antigravity adapter without activating a runtime. The workflow adapts
to the supplied school, vocational, professional, higher-education, or other
course context; the scaffold assumes no subject or level.

It may reside on local storage or a lecturer-controlled personal OneDrive.
OneDrive is cloud-synchronised rather than strictly local, so protected or
assessment material belongs there only when the lecturer's institutional,
privacy, rights and security rules authorise it. Exclude student personal data,
submissions, grades, credentials and secrets by default.

## First actions

1. Invoke `/course-redesign-start` before disclosing any course source path,
   filename, or list. Declare only the material category and exact processing
   environment for Gate 0A.
2. Review and fingerprint Gate 0A. Personal/unmanaged processing is permitted
   only for privately owned/rightsholder-authorised or appropriately licensed/
   public material with explicit AI-processing authority; public availability
   alone is insufficient. Institution-internal/restricted material is route-
   only there, and mixed/uncertain material fails closed until segregated or
   clarified.
3. For an approved institutional environment, record the exact policy
   reference, approved scope, and non-expired expiry.
4. Only after Gate 0A permits processing, add current course files to
   `00_Source_Materials/` and relevant programme, learner, policy,
   accessibility, assessment, AI-tool, rights, and style context to
   `00_Context/`.
5. Keep student personal data, submissions, grades, credentials, and secrets
   out of the project unless a separately approved institutional workflow
   permits them.
6. Ask the orchestrator to inventory the files and prepare Gate 0.
7. Review source classifications, teacher-only assessment boundaries,
   tool/egress permissions, output audiences, eligibility/manifest/policy
   fingerprints, and expiry where applicable.
8. Approve or revise Gate 0 before any specialist analysis.

## Important distinctions

- The source manifest proves file integrity; it does not grant access or egress.
- A course-material decision is not a system activation decision.
- After accepted HITL 3, silence on the system-review offer waits. An explicit
  request or decline closes the course run as terminal `complete_dormant`; it
  never resumes.
- One informational trigger-guidance offer registers nothing. A manual or
  separately authorised scheduled trigger creates a fresh run and lineage.
- A system activation decision is not schedule approval.
- Schedule approval registers an expiring contract but does not trigger an immediate run.
- Every scheduled recurrence creates a fresh run and waits at the configured human gate.

Read `AGENTS.md` for the full orchestration contract and `01_Control/GATES.md` for lecturer decision points.
