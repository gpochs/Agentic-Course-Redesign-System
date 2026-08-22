# Course redesign project

This folder is for one course only. It was created from the Agentic Course Redesign plugin without activating the runtime. The workflow adapts to the supplied school, vocational, professional, higher-education or other course context; the scaffold assumes no subject or level.

It may reside on local storage or a lecturer-controlled personal OneDrive.
OneDrive is cloud-synchronised rather than strictly local, so protected or
assessment material belongs there only when the lecturer's institutional,
privacy, rights and security rules authorise it. Exclude student personal data,
submissions, grades, credentials and secrets by default.

## First actions

1. Before disclosing any course source path, filename or list, declare only the material category, exact processing environment, internal/restricted and student-data flags, sensitivity class, assessment-security class and handling authority for Gate 0A.
2. Review and fingerprint Gate 0A. Personal/unmanaged processing is permitted only for privately owned/rightsholder-authorised or appropriately licensed/public material with explicit AI-processing authority; public availability alone is insufficient. It excludes student personal data. Institution-internal/restricted material is route-only there, and mixed/uncertain or incomplete declarations fail closed until segregated or clarified. A record requiring reconfirmation does not permit intake.
3. For an approved institutional environment, record the exact policy reference, approved scope and non-expired expiry.
4. Only after Gate 0A permits processing, add current course files to `00_Source_Materials/` and relevant programme, learner, policy, accessibility, assessment, AI-tool, rights and style context to `00_Context/`.
5. Keep student personal data, submissions, grades, credentials, and secrets out of the project unless a separately approved institutional workflow permits them.
6. Ask the orchestrator to inventory the files and prepare Gate 0.
7. Review source classifications, teacher-only assessment boundaries, tool/egress permissions, output audiences, manifest fingerprint, and policy fingerprint.
8. Approve or revise Gate 0 before any specialist analysis.

The setup helper may create a new absent target without source intake. It will
not enumerate or add to an existing target unless an approved Gate-0A record is
provided with `--eligibility-record`.

## Important distinctions

- The source manifest proves file integrity; it does not grant access or egress.
- A course-material decision is not a system activation decision.
- A completed dormant course run never resumes; a manual or scheduled trigger creates a fresh run and lineage bound to the current Gate-0A fingerprint.
- A system activation decision is not schedule approval.
- Schedule approval registers an expiring contract but does not trigger an immediate run.
- Every scheduled recurrence creates a fresh run, records its immutable approved-contract snapshot and trigger timestamp, and waits at the configured human gate. Active triggers must fall within the contract window; an expired trigger records no course action.

Read `AGENTS.md` for the full orchestration contract and `01_Control/GATES.md` for lecturer decision points.
